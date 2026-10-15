<?php
/**
 * Keystone Possibilities — Multi-Job Client & Builder Portal v10 REST API
 * Certified BC Builder #52603 — Cloud Persistence & Local Hub Sync Engine
 *
 * Registers REST API endpoints under namespace `keystone/v1`:
 *   - GET    /wp-json/keystone/v1/portal-jobs
 *   - POST   /wp-json/keystone/v1/portal-jobs
 *   - DELETE /wp-json/keystone/v1/portal-jobs
 *
 * Stores multi-job dictionary in wp_options (`keystone_portal_jobs_v10`) with
 * autoload=false to prevent large base64 PDFs/signatures from bloating autoload memory.
 *
 * @package KeystonePossibilitiesChild
 * @version 10.0.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

define('KEYSTONE_PORTAL_JOBS_OPTION', 'keystone_portal_jobs_v10');
define('KEYSTONE_PORTAL_JOBS_UPDATED_OPTION', 'keystone_portal_jobs_v10_updated_at');

/**
 * Compute and attach CORS + No-Cache headers to Portal REST responses.
 *
 * @param WP_REST_Response $response
 * @return WP_REST_Response
 */
function keystone_portal_v10_attach_headers(WP_REST_Response $response): WP_REST_Response {
    $allowed_origins = array(
        'https://keystonepossibilities.ca',
        'https://www.keystonepossibilities.ca',
        'http://127.0.0.1:9879',
        'http://localhost:9879',
    );

    $origin = isset($_SERVER['HTTP_ORIGIN']) ? trim((string) $_SERVER['HTTP_ORIGIN']) : '';
    if (in_array($origin, $allowed_origins, true)) {
        $response->header('Access-Control-Allow-Origin', $origin);
    } else {
        $response->header('Access-Control-Allow-Origin', 'https://keystonepossibilities.ca');
    }

    $response->header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
    $response->header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-WP-Nonce, X-Portal-Role');
    $response->header('Access-Control-Allow-Credentials', 'true');
    $response->header('Vary', 'Origin');
    $response->header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
    $response->header('Pragma', 'no-cache');
    $response->header('X-LiteSpeed-Cache-Control', 'no-cache');

    return $response;
}

/**
 * Ensure preflight OPTIONS requests to /wp-json/keystone/v1/portal-jobs receive CORS headers.
 */
add_filter('rest_pre_serve_request', function ($served, $result, $request, $server) {
    $route = $request->get_route();
    if (strpos($route, '/keystone/v1/portal-jobs') === 0) {
        $allowed_origins = array(
            'https://keystonepossibilities.ca',
            'https://www.keystonepossibilities.ca',
            'http://127.0.0.1:9879',
            'http://localhost:9879',
        );
        $origin = isset($_SERVER['HTTP_ORIGIN']) ? trim((string) $_SERVER['HTTP_ORIGIN']) : '';
        if (in_array($origin, $allowed_origins, true)) {
            header('Access-Control-Allow-Origin: ' . $origin);
        } else {
            header('Access-Control-Allow-Origin: https://keystonepossibilities.ca');
        }
        header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type, Authorization, X-WP-Nonce, X-Portal-Role');
        header('Access-Control-Allow-Credentials: true');
        header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
        header('X-LiteSpeed-Cache-Control: no-cache');
    }
    return $served;
}, 10, 4);

/**
 * Register REST API routes for Multi-Job Portal v10.
 */
add_action('rest_api_init', function () {
    register_rest_route('keystone/v1', '/portal-jobs', array(
        array(
            'methods'             => WP_REST_Server::READABLE, // GET
            'callback'            => 'keystone_portal_v10_get_jobs',
            'permission_callback' => '__return_true',
        ),
        array(
            'methods'             => WP_REST_Server::CREATABLE, // POST
            'callback'            => 'keystone_portal_v10_save_jobs',
            'permission_callback' => '__return_true',
        ),
        array(
            'methods'             => WP_REST_Server::DELETABLE, // DELETE
            'callback'            => 'keystone_portal_v10_delete_job',
            'permission_callback' => '__return_true',
        ),
    ));
});

/**
 * Load stored portal jobs dictionary safely.
 *
 * @return array
 */
function keystone_portal_v10_load_jobs_dict(): array {
    $jobs = get_option(KEYSTONE_PORTAL_JOBS_OPTION, array());
    if (!is_array($jobs)) {
        return array();
    }
    return $jobs;
}

/**
 * GET /wp-json/keystone/v1/portal-jobs
 *
 * @param WP_REST_Request $request
 * @return WP_REST_Response
 */
function keystone_portal_v10_get_jobs(WP_REST_Request $request): WP_REST_Response {
    $jobs       = keystone_portal_v10_load_jobs_dict();
    $updated_at = get_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, null);
    if (empty($updated_at)) {
        $updated_at = gmdate('c');
    }

    $job_id = sanitize_text_field((string) ($request->get_param('job_id') ?? ''));
    if (!empty($job_id)) {
        $single = isset($jobs[$job_id]) ? $jobs[$job_id] : null;
        $resp = new WP_REST_Response(array(
            'status'     => 'ok',
            'job_id'     => $job_id,
            'job'        => $single,
            'jobs'       => (object) $jobs,
            'count'      => count($jobs),
            'updated_at' => $updated_at,
        ), 200);
        return keystone_portal_v10_attach_headers($resp);
    }

    $resp = new WP_REST_Response(array(
        'status'     => 'ok',
        'jobs'       => (object) $jobs,
        'count'      => count($jobs),
        'updated_at' => $updated_at,
    ), 200);

    return keystone_portal_v10_attach_headers($resp);
}

/**
 * POST /wp-json/keystone/v1/portal-jobs
 * Accepts:
 *   - { "job_id": "...", "job": { ... } }
 *   - { "jobs": { ... } }
 *   - { "action": "delete_job", "job_id": "..." }
 *
 * @param WP_REST_Request $request
 * @return WP_REST_Response
 */
function keystone_portal_v10_save_jobs(WP_REST_Request $request): WP_REST_Response {
    $params = $request->get_json_params();
    if (empty($params) || !is_array($params)) {
        $params = $request->get_body_params();
    }
    if (!is_array($params)) {
        $params = array();
    }

    $action = isset($params['action']) ? sanitize_text_field((string) $params['action']) : '';
    if ($action === 'delete_job') {
        return keystone_portal_v10_delete_job($request);
    }

    $jobs = keystone_portal_v10_load_jobs_dict();
    $saved_job_id = null;
    $now_iso = gmdate('c');

    // Case 1: Batch dictionary of jobs `{ "jobs": { "KP-2026-001": { ... }, ... } }`
    if (isset($params['jobs']) && is_array($params['jobs'])) {
        $replace_all = !empty($params['replace_all']);
        if ($replace_all) {
            $jobs = array();
        }
        foreach ($params['jobs'] as $k => $v) {
            if (!is_array($v)) {
                continue;
            }
            $jid = is_string($k) && !is_numeric($k)
                ? sanitize_text_field($k)
                : sanitize_text_field((string) ($v['job_id'] ?? $v['project_id'] ?? $v['id'] ?? ''));
            if (empty($jid)) {
                continue;
            }
            $v['job_id']     = $jid;
            $v['updated_at'] = $v['updated_at'] ?? $now_iso;
            $jobs[$jid]      = $v;
            $saved_job_id    = $jid;
        }
    }

    // Case 2: Single job `{ "job_id": "...", "job": { ... } }`
    if (isset($params['job']) && is_array($params['job'])) {
        $job_data = $params['job'];
        $jid = sanitize_text_field((string) (
            $params['job_id']
            ?? $job_data['job_id']
            ?? $job_data['project_id']
            ?? $job_data['id']
            ?? ''
        ));
        if (!empty($jid)) {
            $job_data['job_id']     = $jid;
            $job_data['updated_at'] = $job_data['updated_at'] ?? $now_iso;
            $jobs[$jid]             = $job_data;
            $saved_job_id           = $jid;
        }
    }

    // Case 3: Top-level job payload with `job_id` / `project_id` but no nested `job` key
    if ($saved_job_id === null && (!empty($params['job_id']) || !empty($params['project_id']))) {
        $jid = sanitize_text_field((string) ($params['job_id'] ?? $params['project_id']));
        if (!empty($jid)) {
            $job_data = $params;
            unset($job_data['action']);
            $job_data['job_id']     = $jid;
            $job_data['updated_at'] = $job_data['updated_at'] ?? $now_iso;
            $jobs[$jid]             = $job_data;
            $saved_job_id           = $jid;
        }
    }

    if ($saved_job_id === null && !isset($params['jobs'])) {
        $err = new WP_REST_Response(array(
            'status'  => 'error',
            'message' => 'Invalid payload. Provide {"job_id": "...", "job": {...}} or {"jobs": {...}}.',
        ), 400);
        return keystone_portal_v10_attach_headers($err);
    }

    // Persist with autoload = false so large JSON payloads never bloat wp_options autoload
    update_option(KEYSTONE_PORTAL_JOBS_OPTION, $jobs, false);
    update_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, $now_iso, false);

    $resp = new WP_REST_Response(array(
        'status'     => 'saved',
        'job_id'     => $saved_job_id,
        'count'      => count($jobs),
        'updated_at' => $now_iso,
    ), 200);

    return keystone_portal_v10_attach_headers($resp);
}

/**
 * DELETE /wp-json/keystone/v1/portal-jobs
 * Deletes a job by `job_id` from `keystone_portal_jobs_v10`.
 *
 * @param WP_REST_Request $request
 * @return WP_REST_Response
 */
function keystone_portal_v10_delete_job(WP_REST_Request $request): WP_REST_Response {
    $params = $request->get_json_params();
    if (empty($params) || !is_array($params)) {
        $params = $request->get_body_params();
    }
    if (!is_array($params)) {
        $params = array();
    }

    $job_id = sanitize_text_field((string) (
        $params['job_id']
        ?? $params['project_id']
        ?? $params['id']
        ?? $request->get_param('job_id')
        ?? $request->get_param('id')
        ?? ''
    ));

    if (empty($job_id)) {
        $err = new WP_REST_Response(array(
            'status'  => 'error',
            'message' => 'Missing required parameter: job_id',
        ), 400);
        return keystone_portal_v10_attach_headers($err);
    }

    $jobs = keystone_portal_v10_load_jobs_dict();
    $existed = isset($jobs[$job_id]);
    if ($existed) {
        unset($jobs[$job_id]);
    }

    $now_iso = gmdate('c');
    update_option(KEYSTONE_PORTAL_JOBS_OPTION, $jobs, false);
    update_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, $now_iso, false);

    $resp = new WP_REST_Response(array(
        'status'     => 'deleted',
        'job_id'     => $job_id,
        'existed'    => $existed,
        'count'      => count($jobs),
        'updated_at' => $now_iso,
    ), 200);

    return keystone_portal_v10_attach_headers($resp);
}
