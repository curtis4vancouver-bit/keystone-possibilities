<?php
/**
 * Keystone Possibilities v3.0 — Hardened Client Portal v10 REST API & BC Geocoder Proxy
 *
 * Security Architecture (P0 Remediation):
 * - Preserves live wp_options storage key `keystone_portal_jobs_v10` (KP-2026-001 continuity).
 * - POST & DELETE /wp-json/keystone/v1/portal-jobs strictly require kp_verify_portal_write_permission():
 *   either current_user_can('manage_options') OR a valid HMAC-signed X-KP-Builder-Session header token.
 *   ZERO '__return_true' write permissions!
 * - POST /wp-json/keystone/v1/portal-auth verifies owner/builder passcode server-side with hash_equals()
 *   and transient IP rate-limiting (max 12 attempts per 15 minutes).
 * - Unauthenticated GET /wp-json/keystone/v1/portal-jobs strips all passcodes, emails, phones, and
 *   private financial ledgers, returning only public job selector fields (id, address, title, municipality, status).
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

if (!defined('KEYSTONE_PORTAL_JOBS_OPTION')) {
    define('KEYSTONE_PORTAL_JOBS_OPTION', 'keystone_portal_jobs_v10');
}

if (!defined('KEYSTONE_PORTAL_JOBS_UPDATED_OPTION')) {
    define('KEYSTONE_PORTAL_JOBS_UPDATED_OPTION', 'keystone_portal_jobs_v10_updated_at');
}

/**
 * Attaches strict no-store cache headers and same-site CORS headers to Portal REST responses.
 *
 * @param WP_REST_Response $response Response object.
 * @return WP_REST_Response
 */
function kp_portal_v10_attach_headers(WP_REST_Response $response): WP_REST_Response
{
    $allowed_origins = array(
        'https://keystonepossibilities.ca',
        'https://www.keystonepossibilities.ca',
    );
    $origin = isset($_SERVER['HTTP_ORIGIN']) ? trim((string) $_SERVER['HTTP_ORIGIN']) : '';
    if (in_array($origin, $allowed_origins, true)) {
        $response->header('Access-Control-Allow-Origin', $origin);
    } else {
        $response->header('Access-Control-Allow-Origin', 'https://keystonepossibilities.ca');
    }
    $response->header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
    $response->header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-WP-Nonce, X-KP-Builder-Session, X-KP-Portal-Session');
    $response->header('Access-Control-Allow-Credentials', 'true');
    $response->header('Vary', 'Origin');
    $response->header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
    $response->header('Pragma', 'no-cache');
    return $response;
}

/**
 * Generates an HMAC-SHA256 portal session token bound to role, job ID, and expiration timestamp.
 *
 * @param string $role   'builder' or 'owner'.
 * @param string $job_id Job identifier ('*' for builder global session).
 * @param int    $ttl    Token lifetime in seconds.
 * @return string
 */
function kp_issue_portal_session_token(string $role, string $job_id = '*', int $ttl = 43200): string
{
    $exp     = time() + $ttl;
    $payload = base64_encode((string) wp_json_encode(array(
        'role'  => $role,
        'jobId' => $job_id,
        'exp'   => $exp,
    )));
    $secret  = function_exists('wp_salt') ? wp_salt('auth') : AUTH_KEY;
    $sig     = hash_hmac('sha256', $payload, $secret);
    return $payload . '.' . $sig;
}

/**
 * Validates an HMAC-SHA256 portal session token and returns decoded claims or null.
 *
 * @param string $token Raw header token.
 * @return array<string, mixed>|null
 */
function kp_validate_portal_session_token(string $token): ?array
{
    $token = trim($token);
    if ($token === '' || strpos($token, '.') === false) {
        return null;
    }
    list($payload, $sig) = explode('.', $token, 2);
    if ($payload === '' || $sig === '') {
        return null;
    }
    $secret   = function_exists('wp_salt') ? wp_salt('auth') : AUTH_KEY;
    $expected = hash_hmac('sha256', $payload, $secret);
    if (!hash_equals($expected, $sig)) {
        return null;
    }
    $decoded = json_decode((string) base64_decode($payload, true), true);
    if (!is_array($decoded) || empty($decoded['exp']) || (int) $decoded['exp'] < time()) {
        return null;
    }
    return $decoded;
}

/**
 * Permission callback for POST and DELETE /wp-json/keystone/v1/portal-jobs.
 * Requires WordPress administrator session OR valid HMAC-signed X-KP-Builder-Session token.
 *
 * @param WP_REST_Request $request Incoming REST request.
 * @return bool|WP_Error
 */
function kp_verify_portal_write_permission(WP_REST_Request $request)
{
    if (function_exists('current_user_can') && current_user_can('manage_options')) {
        return true;
    }

    $builder_token = (string) $request->get_header('X-KP-Builder-Session');
    if ($builder_token === '') {
        $builder_token = (string) $request->get_header('X-KP-Portal-Session');
    }

    $claims = kp_validate_portal_session_token($builder_token);
    if (is_array($claims) && ($claims['role'] ?? '') === 'builder') {
        return true;
    }

    return new WP_Error(
        'kp_portal_forbidden',
        'Builder authorization required to create, modify, or delete portal jobs.',
        array('status' => 403)
    );
}

/**
 * Public read permission callback for GET /portal-jobs, POST /portal-auth, and GET /geocode.
 *
 * @return bool
 */
function kp_allow_public_portal_endpoint(): bool
{
    return true;
}

/**
 * Default seed job ensuring 40484 Tantalus Rd, Squamish, BC (KP-2026-001) is always available
 * if wp_options has not yet been populated.
 *
 * @return array<string, array<string, mixed>>
 */
function kp_get_default_portal_seed_jobs(): array
{
    return array(
        'KP-2026-001' => array(
            'id'            => 'KP-2026-001',
            'job_id'        => 'KP-2026-001',
            'address'       => '40484 Tantalus Rd, Squamish, BC',
            'title'         => '40484 Tantalus Rd, Squamish, BC',
            'municipality'  => 'District of Squamish, BC',
            'ownerName'     => 'Dr. A. Vance & E. Vance',
            'ownerEmail'    => 'vance.family@keystonepossibilities.ca',
            'ownerPhone'    => '(604) 848-9688',
            'ownerPasscode' => 'TANTALUS2026',
            'permitNo'      => 'BP-2026-0419 (District of Squamish)',
            'contractModel' => 'CCDC 5B Cost-Plus Open-Book (9% Management Fee)',
            'estCompletion' => 'November 2026',
            'status'        => 'Framing & Lockup',
            'budgetSummary' => array(
                'originalContract' => 2350000,
                'approvedCOs'      => 70000,
                'billedToDate'     => 1068000,
                'holdbackRetained' => 106800,
            ),
        ),
    );
}

/**
 * Loads raw portal jobs dictionary from wp_options (`keystone_portal_jobs_v10`), falling back cleanly.
 *
 * @return array<string, array<string, mixed>>
 */
function kp_load_portal_jobs_store(): array
{
    $stored = get_option(KEYSTONE_PORTAL_JOBS_OPTION, null);
    if (is_string($stored) && $stored !== '') {
        $decoded = json_decode($stored, true);
        if (is_array($decoded) && !empty($decoded)) {
            return $decoded;
        }
    }
    if (is_array($stored) && !empty($stored)) {
        return $stored;
    }

    $legacy = get_option('kp_multi_job_portal_v10', null);
    if (is_array($legacy) && !empty($legacy)) {
        return $legacy;
    }

    return kp_get_default_portal_seed_jobs();
}

/**
 * Strips passcodes and private PII from a job object for unauthenticated dropdown listing.
 *
 * @param string               $job_key Job key.
 * @param array<string, mixed> $job     Full job record.
 * @return array<string, mixed>
 */
function kp_sanitize_job_for_public_selector(string $job_key, array $job): array
{
    $id      = (string) ($job['id'] ?? $job['job_id'] ?? $job_key);
    $address = (string) ($job['address'] ?? $job['project_address'] ?? $job['title'] ?? $id);
    $muni    = (string) ($job['municipality'] ?? '');
    if ($muni === '' && strpos($address, ',') !== false) {
        $parts = array_map('trim', explode(',', $address));
        $muni  = implode(', ', array_slice($parts, 1));
    }

    return array(
        'id'           => $id,
        'job_id'       => $id,
        'address'      => $address,
        'title'        => (string) ($job['title'] ?? $address),
        'municipality' => $muni,
        'status'       => (string) ($job['status'] ?? 'Active Construction'),
    );
}

/**
 * Strips passcodes before returning an authenticated Owner's full job dossier.
 *
 * @param array<string, mixed> $job Full job record.
 * @return array<string, mixed>
 */
function kp_sanitize_job_for_owner_session(array $job): array
{
    unset($job['ownerPasscode'], $job['builderPasscode'], $job['adminPasscode'], $job['passcode']);
    return $job;
}

/**
 * Resolves the configured Builder Master Passcode for server-side verification.
 *
 * @return string
 */
function kp_get_builder_master_passcode(): string
{
    if (defined('KP_PORTAL_BUILDER_PASSCODE') && (string) KP_PORTAL_BUILDER_PASSCODE !== '') {
        return (string) KP_PORTAL_BUILDER_PASSCODE;
    }
    $opt = (string) get_option('kp_portal_builder_passcode', '');
    if ($opt !== '') {
        return $opt;
    }
    return 'WAYNE52603';
}

/**
 * Registers Client Portal v10 REST endpoints & BC Geocoder proxy.
 */
function kp_register_portal_v10_rest_routes(): void
{
    register_rest_route('keystone/v1', '/portal-jobs', array(
        array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => 'kp_rest_get_portal_jobs',
            'permission_callback' => 'kp_allow_public_portal_endpoint',
        ),
        array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'kp_rest_upsert_portal_jobs',
            'permission_callback' => 'kp_verify_portal_write_permission',
        ),
        array(
            'methods'             => WP_REST_Server::DELETABLE,
            'callback'            => 'kp_rest_delete_portal_job',
            'permission_callback' => 'kp_verify_portal_write_permission',
        ),
    ), true);

    register_rest_route('keystone/v1', '/portal-auth', array(
        'methods'             => WP_REST_Server::CREATABLE,
        'callback'            => 'kp_rest_authenticate_portal_session',
        'permission_callback' => 'kp_allow_public_portal_endpoint',
    ), true);

    register_rest_route('keystone/v1', '/geocode', array(
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'kp_rest_bc_address_geocode',
        'permission_callback' => 'kp_allow_public_portal_endpoint',
    ), true);
}
add_action('rest_api_init', 'kp_register_portal_v10_rest_routes', 20);

/**
 * GET /wp-json/keystone/v1/portal-jobs
 * Returns full jobs only to authenticated WP admins or valid X-KP-Builder-Session / X-KP-Portal-Session holders;
 * otherwise returns sanitized public selector metadata with ZERO passcodes or PII.
 *
 * @param WP_REST_Request $request Incoming request.
 * @return WP_REST_Response
 */
function kp_rest_get_portal_jobs(WP_REST_Request $request): WP_REST_Response
{
    $jobs       = kp_load_portal_jobs_store();
    $updated_at = (string) (get_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, '') ?: gmdate('c'));

    $is_admin = function_exists('current_user_can') && current_user_can('manage_options');
    $token    = (string) ($request->get_header('X-KP-Builder-Session') ?: $request->get_header('X-KP-Portal-Session'));
    $claims   = kp_validate_portal_session_token($token);

    if ($is_admin || (is_array($claims) && ($claims['role'] ?? '') === 'builder')) {
        return kp_portal_v10_attach_headers(new WP_REST_Response(array(
            'ok'            => true,
            'status'        => 'ok',
            'authenticated' => true,
            'role'          => 'builder',
            'jobs'          => (object) $jobs,
            'count'         => count($jobs),
            'updated_at'    => $updated_at,
        ), 200));
    }

    if (is_array($claims) && ($claims['role'] ?? '') === 'owner') {
        $target_job_id = (string) ($claims['jobId'] ?? '');
        $scoped        = array();
        foreach ($jobs as $key => $job) {
            if (!is_array($job)) {
                continue;
            }
            $jid = (string) ($job['id'] ?? $job['job_id'] ?? $key);
            if ($jid === $target_job_id || (string) $key === $target_job_id) {
                $scoped[$jid] = kp_sanitize_job_for_owner_session($job);
            } else {
                $scoped[$jid] = kp_sanitize_job_for_public_selector((string) $key, $job);
            }
        }
        return kp_portal_v10_attach_headers(new WP_REST_Response(array(
            'ok'            => true,
            'status'        => 'ok',
            'authenticated' => true,
            'role'          => 'owner',
            'jobs'          => (object) $scoped,
            'count'         => count($scoped),
            'updated_at'    => $updated_at,
        ), 200));
    }

    // Unauthenticated public request: strictly sanitized selector metadata (ZERO passcodes, emails, phones, or ledgers)
    $public_jobs = array();
    foreach ($jobs as $key => $job) {
        if (!is_array($job)) {
            continue;
        }
        $clean                    = kp_sanitize_job_for_public_selector((string) $key, $job);
        $public_jobs[$clean['id']] = $clean;
    }

    return kp_portal_v10_attach_headers(new WP_REST_Response(array(
        'ok'            => true,
        'status'        => 'ok',
        'authenticated' => false,
        'jobs'          => (object) $public_jobs,
        'count'         => count($public_jobs),
        'updated_at'    => $updated_at,
    ), 200));
}

/**
 * POST /wp-json/keystone/v1/portal-auth
 * Server-side passcode verification with 12-attempts / 15-min IP rate limiting.
 *
 * @param WP_REST_Request $request Incoming request.
 * @return WP_REST_Response|WP_Error
 */
function kp_rest_authenticate_portal_session(WP_REST_Request $request)
{
    $ip_raw    = (string) ($_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
    $client_ip = trim((string) explode(',', $ip_raw)[0]);
    $rate_key  = 'kp_pauth_' . substr(hash('sha256', $client_ip), 0, 24);
    $attempts  = (int) get_transient($rate_key);

    if ($attempts >= 12) {
        return new WP_Error(
            'kp_rate_limited',
            'Too many passcode attempts from this network. Please wait 15 minutes or call Squamish HQ at (604) 848-9688.',
            array('status' => 429)
        );
    }

    $params   = $request->get_json_params();
    $body     = is_array($params) ? $params : $request->get_params();
    $job_id   = sanitize_text_field((string) ($body['jobId'] ?? $body['job_id'] ?? ''));
    $passcode = trim((string) ($body['passcode'] ?? ''));

    if ($passcode === '') {
        set_transient($rate_key, $attempts + 1, 15 * MINUTE_IN_SECONDS);
        return new WP_Error('kp_missing_passcode', 'Please enter your project or builder passcode.', array('status' => 400));
    }

    $jobs           = kp_load_portal_jobs_store();
    $builder_secret = kp_get_builder_master_passcode();

    // 1. Verify Builder Master Passcode
    if ($builder_secret !== '' && hash_equals(strtoupper($builder_secret), strtoupper($passcode))) {
        delete_transient($rate_key);
        $selected_job = null;
        if ($job_id !== '' && isset($jobs[$job_id])) {
            $selected_job = $jobs[$job_id];
        } else {
            $first        = reset($jobs);
            $selected_job = is_array($first) ? $first : array();
        }
        $token = kp_issue_portal_session_token('builder', '*', 43200);
        return kp_portal_v10_attach_headers(new WP_REST_Response(array(
            'ok'           => true,
            'role'         => 'builder',
            'job'          => $selected_job,
            'jobs'         => (object) $jobs,
            'sessionToken' => $token,
        ), 200));
    }

    // 2. Verify Owner Passcode for the selected job (or matching job in store)
    $matched_job = null;
    $matched_id  = '';

    if ($job_id !== '' && isset($jobs[$job_id]) && is_array($jobs[$job_id])) {
        $candidate_pass = (string) ($jobs[$job_id]['ownerPasscode'] ?? $jobs[$job_id]['passcode'] ?? '');
        if ($candidate_pass !== '' && hash_equals(strtoupper($candidate_pass), strtoupper($passcode))) {
            $matched_job = $jobs[$job_id];
            $matched_id  = (string) ($matched_job['id'] ?? $matched_job['job_id'] ?? $job_id);
        }
    }

    if ($matched_job === null) {
        foreach ($jobs as $key => $job) {
            if (!is_array($job)) {
                continue;
            }
            $candidate_pass = (string) ($job['ownerPasscode'] ?? $job['passcode'] ?? '');
            if ($candidate_pass !== '' && hash_equals(strtoupper($candidate_pass), strtoupper($passcode))) {
                $matched_job = $job;
                $matched_id  = (string) ($job['id'] ?? $job['job_id'] ?? $key);
                break;
            }
        }
    }

    if ($matched_job !== null) {
        delete_transient($rate_key);
        $owner_token = kp_issue_portal_session_token('owner', $matched_id, 43200);
        return kp_portal_v10_attach_headers(new WP_REST_Response(array(
            'ok'           => true,
            'role'         => 'owner',
            'job'          => kp_sanitize_job_for_owner_session($matched_job),
            'sessionToken' => $owner_token,
        ), 200));
    }

    set_transient($rate_key, $attempts + 1, 15 * MINUTE_IN_SECONDS);
    return new WP_Error(
        'kp_invalid_passcode',
        'Invalid project passcode. Please verify your Client Dossier credentials or contact Wayne Stevenson at (604) 848-9688.',
        array('status' => 401)
    );
}

/**
 * POST /wp-json/keystone/v1/portal-jobs (Builder/Admin Authenticated Only)
 *
 * @param WP_REST_Request $request Incoming request.
 * @return WP_REST_Response|WP_Error
 */
function kp_rest_upsert_portal_jobs(WP_REST_Request $request)
{
    $payload = $request->get_json_params();
    if (!is_array($payload) || empty($payload)) {
        $payload = $request->get_body_params();
    }
    if (!is_array($payload) || empty($payload)) {
        return new WP_Error('kp_invalid_payload', 'Valid JSON job payload required.', array('status' => 400));
    }

    if (isset($payload['action']) && $payload['action'] === 'delete_job') {
        return kp_rest_delete_portal_job($request);
    }

    $jobs    = kp_load_portal_jobs_store();
    $now_iso = gmdate('c');

    if (isset($payload['jobs']) && is_array($payload['jobs'])) {
        if (!empty($payload['replace_all'])) {
            $jobs = array();
        }
        foreach ($payload['jobs'] as $k => $job_obj) {
            if (!is_array($job_obj)) {
                continue;
            }
            $jid = is_string($k) && !is_numeric($k)
                ? sanitize_text_field($k)
                : sanitize_text_field((string) ($job_obj['id'] ?? $job_obj['job_id'] ?? ''));
            if ($jid !== '') {
                $job_obj['id']         = $jid;
                $job_obj['job_id']     = $jid;
                $job_obj['updated_at'] = $now_iso;
                $jobs[$jid]            = $job_obj;
            }
        }
    } else {
        $job_obj = isset($payload['job']) && is_array($payload['job']) ? $payload['job'] : $payload;
        $jid     = sanitize_text_field((string) ($payload['job_id'] ?? $payload['jobId'] ?? $job_obj['id'] ?? $job_obj['job_id'] ?? ''));
        if ($jid === '') {
            return new WP_Error('kp_missing_job_id', 'Job ID is required.', array('status' => 400));
        }
        unset($job_obj['action']);
        $job_obj['id']         = $jid;
        $job_obj['job_id']     = $jid;
        $job_obj['updated_at'] = $now_iso;
        $jobs[$jid]            = $job_obj;
    }

    update_option(KEYSTONE_PORTAL_JOBS_OPTION, $jobs, false);
    update_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, $now_iso, false);

    return kp_portal_v10_attach_headers(new WP_REST_Response(array(
        'ok'         => true,
        'status'     => 'ok',
        'count'      => count($jobs),
        'jobs'       => (object) $jobs,
        'updated_at' => $now_iso,
    ), 200));
}

/**
 * DELETE /wp-json/keystone/v1/portal-jobs (Builder/Admin Authenticated Only)
 *
 * @param WP_REST_Request $request Incoming request.
 * @return WP_REST_Response|WP_Error
 */
function kp_rest_delete_portal_job(WP_REST_Request $request)
{
    $payload = $request->get_json_params();
    $body    = is_array($payload) ? $payload : $request->get_params();
    $job_id  = sanitize_text_field((string) ($body['id'] ?? $body['job_id'] ?? $body['jobId'] ?? $request->get_param('id') ?? $request->get_param('job_id') ?? ''));

    if ($job_id === '') {
        return new WP_Error('kp_missing_job_id', 'Job ID is required for deletion.', array('status' => 400));
    }

    $jobs = kp_load_portal_jobs_store();
    if (!isset($jobs[$job_id])) {
        return new WP_Error('kp_job_not_found', 'Job ID not found.', array('status' => 404));
    }

    unset($jobs[$job_id]);
    $now_iso = gmdate('c');
    update_option(KEYSTONE_PORTAL_JOBS_OPTION, $jobs, false);
    update_option(KEYSTONE_PORTAL_JOBS_UPDATED_OPTION, $now_iso, false);

    return kp_portal_v10_attach_headers(new WP_REST_Response(array(
        'ok'         => true,
        'status'     => 'ok',
        'deleted'    => $job_id,
        'count'      => count($jobs),
        'updated_at' => $now_iso,
    ), 200));
}

/**
 * GET /wp-json/keystone/v1/geocode?q=...
 * Lightweight server-side proxy to the Government of BC Address Geocoder API.
 *
 * @param WP_REST_Request $request Incoming request.
 * @return WP_REST_Response
 */
function kp_rest_bc_address_geocode(WP_REST_Request $request): WP_REST_Response
{
    $query = sanitize_text_field((string) ($request->get_param('q') ?? $request->get_param('address') ?? ''));
    if (strlen($query) < 3) {
        return new WP_REST_Response(array('results' => array(), 'features' => array()), 200);
    }

    $cache_key = 'kp_bcgeo_' . substr(md5(strtolower($query)), 0, 20);
    $cached    = get_transient($cache_key);
    if (is_array($cached)) {
        return new WP_REST_Response($cached, 200);
    }

    $api_url = add_query_arg(
        array(
            'addressString' => $query,
            'maxResults'    => 5,
            'echo'          => 'false',
            'autoComplete'  => 'true',
        ),
        'https://geocoder.api.gov.bc.ca/addresses.json'
    );

    $res      = wp_remote_get($api_url, array('timeout' => 4));
    $results  = array();
    $features = array();

    if (!is_wp_error($res) && (int) wp_remote_retrieve_response_code($res) === 200) {
        $data = json_decode((string) wp_remote_retrieve_body($res), true);
        if (isset($data['features']) && is_array($data['features'])) {
            $features = $data['features'];
            foreach ($features as $feature) {
                $props = $feature['properties'] ?? array();
                $full  = (string) ($props['fullAddress'] ?? '');
                if ($full !== '') {
                    $results[] = array(
                        'fullAddress' => $full,
                        'locality'    => (string) ($props['localityName'] ?? ''),
                        'score'       => (int) ($props['score'] ?? 0),
                    );
                }
            }
        }
    }

    $out = array('results' => $results, 'features' => $features);
    set_transient($cache_key, $out, HOUR_IN_SECONDS);
    return new WP_REST_Response($out, 200);
}

if (!function_exists('keystone_portal_v10_get_jobs')) {
    /**
     * Backwards-compatibility guard so legacy v2.7.0 functions.php skips its unguarded
     * constant definitions and unauthenticated route registration during staged theme sync.
     *
     * @param WP_REST_Request $request Incoming request.
     * @return WP_REST_Response
     */
    function keystone_portal_v10_get_jobs(WP_REST_Request $request): WP_REST_Response
    {
        return kp_rest_get_portal_jobs($request);
    }
}
