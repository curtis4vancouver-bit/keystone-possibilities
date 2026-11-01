<?php
/**
 * Keystone Possibilities — Live Website Project Sync REST API
 * Certified BC Builder #52603 — 1-Click Studio to Live Cloud Sync Engine
 *
 * Registers REST API endpoint:
 *   POST /wp-json/keystone/v1/sync-project
 *
 * Authenticated via KEYSTONE_PORTAL_SYNC_SECRET (header X-Keystone-Secret or query param 'secret')
 * Updates stored project state in `wp_options` under `keystone_portal_jobs_v10` and refreshes
 * public portfolio cards and client-login state.
 *
 * @package KeystonePossibilitiesChild
 * @version 10.1.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

if (!defined('KEYSTONE_PORTAL_JOBS_OPTION')) {
    define('KEYSTONE_PORTAL_JOBS_OPTION', 'keystone_portal_jobs_v10');
}

if (!defined('KEYSTONE_PORTAL_JOBS_UPDATED_OPTION')) {
    define('KEYSTONE_PORTAL_JOBS_UPDATED_OPTION', 'keystone_portal_jobs_v10_updated_at');
}

if (!defined('KEYSTONE_PORTAL_SYNC_SECRET')) {
    define('KEYSTONE_PORTAL_SYNC_SECRET', 'keystone_portal_sync_secret_52603_wayne');
}

/**
 * Register the /wp-json/keystone/v1/sync-project REST route.
 */
add_action('rest_api_init', function () {
    register_rest_route('keystone/v1', '/sync-project', array(
        'methods'             => WP_REST_Server::CREATABLE, // POST
        'callback'            => 'keystone_portal_sync_project_handler',
        'permission_callback' => 'keystone_portal_sync_project_permissions_check',
    ));
});

/**
 * Permission check for project sync endpoint.
 *
 * @param WP_REST_Request $request
 * @return bool|WP_Error
 */
function keystone_portal_sync_project_permissions_check(WP_REST_Request $request) {
    // 1. Check X-Keystone-Secret header
    $secret_header = $request->get_header('x-keystone-secret');
    if (!empty($secret_header) && hash_equals(KEYSTONE_PORTAL_SYNC_SECRET, (string) $secret_header)) {
        return true;
    }

    // 2. Check secret parameter in body or query string
    $secret_param = $request->get_param('secret');
    if (!empty($secret_param) && hash_equals(KEYSTONE_PORTAL_SYNC_SECRET, (string) $secret_param)) {
        return true;
    }

    // 3. Fallback: Authenticated WordPress administrator
    if (function_exists('current_user_can') && current_user_can('manage_options')) {
        return true;
    }

    return new WP_Error(
        'rest_forbidden_sync',
        __('Forbidden: Invalid or missing KEYSTONE_PORTAL_SYNC_SECRET.', 'keystone-possibilities'),
        array('status' => 403)
    );
}

/**
 * Main handler for POST /wp-json/keystone/v1/sync-project
 *
 * @param WP_REST_Request $request
 * @return WP_REST_Response|WP_Error
 */
function keystone_portal_sync_project_handler(WP_REST_Request $request) {
    $params = $request->get_json_params();
    if (empty($params) || !is_array($params)) {
        $params = $request->get_params();
    }

    $job_id = !empty($params['job_id']) ? sanitize_text_field($params['job_id']) : '';
    if (empty($job_id)) {
        $job_id = !empty($params['jobId']) ? sanitize_text_field($params['jobId']) : 'KP-2026-001';
    }

    $active_stage_code = !empty($params['active_stage_code']) ? sanitize_text_field($params['active_stage_code']) : '';
    if (empty($active_stage_code) && !empty($params['whereWeAreStage'])) {
        $active_stage_code = sanitize_text_field($params['whereWeAreStage']);
    }

    $percent_complete = isset($params['percent_complete']) ? floatval($params['percent_complete']) : null;
    if ($percent_complete === null && isset($params['whereWeArePct'])) {
        $percent_complete = floatval($params['whereWeArePct']);
    }

    $completed_stages = isset($params['completed_stages']) && is_array($params['completed_stages'])
        ? array_map('sanitize_text_field', $params['completed_stages'])
        : array();

    $site_photos = isset($params['site_photos']) && is_array($params['site_photos'])
        ? $params['site_photos']
        : array();

    // Load existing jobs dictionary
    $jobs = get_option(KEYSTONE_PORTAL_JOBS_OPTION, array());
    if (!is_array($jobs)) {
        $jobs = array();
    }

    $target_job = isset($jobs[$job_id]) && is_array($jobs[$job_id]) ? $jobs[$job_id] : array();

    // Merge incoming parameters
    $target_job['job_id'] = $job_id;
    $target_job['jobId']  = $job_id;

    if (!empty($active_stage_code)) {
        $target_job['whereWeAreStage']  = $active_stage_code;
        $target_job['active_stage_code'] = $active_stage_code;
    }
    if ($percent_complete !== null) {
        $target_job['whereWeArePct']    = $percent_complete;
        $target_job['percent_complete'] = $percent_complete;
    }
    if (!empty($completed_stages)) {
        $target_job['completed_stages'] = $completed_stages;
    }
    if (!empty($site_photos)) {
        $target_job['site_photos'] = $site_photos;
    }

    // Additional metadata if provided
    $optional_keys = array(
        'title', 'address', 'municipality', 'pid', 'permitNum',
        'ownerName', 'ownerPhone', 'ownerEmail', 'ownerPasscode',
        'contractPrice', 'scopeSummary', 'whereWeAreDate',
        'contractPdf', 'builderSig', 'ownerSig', 'warranty',
        'planSets', 'takeoffParams', 'draws', 'vaultDocs', 'contacts', 'trades'
    );
    foreach ($optional_keys as $k) {
        if (isset($params[$k])) {
            $target_job[$k] = $params[$k];
        }
    }

    $now_iso = gmdate('Y-m-d\TH:i:s\Z');
    $target_job['lastSyncedAt'] = $now_iso;
    $target_job['updated_at']   = $now_iso;

    // Update dictionary
    $jobs[$job_id] = $target_job;

    // Persist to wp_options with autoload=false
    update_option(KEYSTONE_PORTAL_JOBS_OPTION, $jobs, false);
    update_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, time(), false);

    // Refresh client login and portfolio cache if present
    if (function_exists('keystone_portal_refresh_public_cache')) {
        keystone_portal_refresh_public_cache($job_id, $target_job);
    }

    $receipt_id = 'KP_SYNC_' . strtoupper(substr(md5($job_id . time()), 0, 10));
    $live_url   = 'https://keystonepossibilities.ca/project/' . strtolower($job_id);

    $response_data = array(
        'ok'               => true,
        'status'           => 'synced_to_live_site',
        'job_id'           => $job_id,
        'url'              => $live_url,
        'receipt'          => $receipt_id,
        'active_stage'     => isset($target_job['whereWeAreStage']) ? $target_job['whereWeAreStage'] : '',
        'percent_complete' => isset($target_job['whereWeArePct']) ? $target_job['whereWeArePct'] : 0,
        'timestamp'        => $now_iso,
    );

    $response = new WP_REST_Response($response_data, 200);

    // Attach CORS & Cache-Control headers
    if (function_exists('keystone_portal_v10_attach_headers')) {
        return keystone_portal_v10_attach_headers($response);
    }

    $response->header('Access-Control-Allow-Origin', '*');
    $response->header('Access-Control-Allow-Methods', 'POST, OPTIONS');
    $response->header('Access-Control-Allow-Headers', 'Content-Type, X-Keystone-Secret');
    $response->header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');

    return $response;
}
