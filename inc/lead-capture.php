<?php
/**
 * Keystone Possibilities v3.0 — Lead Capture, Brokerage Referral Intake & Notification Engine
 *
 * Provides zero-loss lead capture for custom home, BC Bill 44 multiplex, BC Hydro ES54 civil,
 * and BCFSA Rule 5-11 Managing Brokerage referral inquiries.
 * Handles both REST API (`/wp-json/keystone/v1/lead`) and WP AJAX (`keystone_lead_capture` / `keystone_submit_lead`).
 * Persists leads to `wp_options` (`keystone_leads_log`) and dispatches executive HTML email notifications.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

// ── 1. Register REST API Endpoint ───────────────────────────────────────────
add_action('rest_api_init', function (): void {
    register_rest_route('keystone/v1', '/lead', array(
        'methods'             => 'POST',
        'callback'            => 'keystone_possibilities_handle_lead_rest',
        'permission_callback' => '__return_true',
    ));
});

// ── 2. Register WordPress AJAX Actions (Logged-in & Guest) ───────────────────
add_action('wp_ajax_keystone_lead_capture', 'keystone_possibilities_handle_lead_ajax');
add_action('wp_ajax_nopriv_keystone_lead_capture', 'keystone_possibilities_handle_lead_ajax');
add_action('wp_ajax_keystone_submit_lead', 'keystone_possibilities_handle_lead_ajax');
add_action('wp_ajax_nopriv_keystone_submit_lead', 'keystone_possibilities_handle_lead_ajax');

/**
 * Handle REST API Lead Submission.
 *
 * @param WP_REST_Request $request Incoming REST request.
 * @return WP_REST_Response|WP_Error
 */
function keystone_possibilities_handle_lead_rest(WP_REST_Request $request)
{
    $params = $request->get_json_params();
    if (empty($params) || !is_array($params)) {
        $params = $request->get_body_params();
    }
    return keystone_possibilities_process_lead(is_array($params) ? $params : array());
}

/**
 * Handle WP AJAX Lead Submission.
 */
function keystone_possibilities_handle_lead_ajax(): void
{
    $params   = is_array($_POST) ? wp_unslash($_POST) : array();
    $response = keystone_possibilities_process_lead($params);

    if (is_wp_error($response)) {
        wp_send_json_error(array('message' => $response->get_error_message()), 400);
    } else {
        wp_send_json_success($response->get_data());
    }
}

/**
 * Core Lead Processing, Rate-Limiting, Storage & Email Dispatch.
 *
 * @param array<string, mixed> $data Raw form/JSON fields.
 * @return WP_REST_Response|WP_Error
 */
function keystone_possibilities_process_lead(array $data)
{
    // Silent honeypot trap for automated spam bots
    if (!empty($data['website_url_hp']) || !empty($data['company_website_hp'])) {
        return new WP_REST_Response(array(
            'success' => true,
            'message' => 'Thank you. Your consultation request has been logged.',
        ), 200);
    }

    $ip_address = sanitize_text_field((string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0'));
    $rate_key   = 'kp_lead_rl_' . substr(hash('sha256', $ip_address), 0, 16);
    $attempts   = (int) get_transient($rate_key);
    if ($attempts >= 15) {
        return new WP_Error(
            'rate_limited',
            'Too many submissions from this network. Please call Wayne Stevenson directly at (604) 848-9688.',
            array('status' => 429)
        );
    }
    set_transient($rate_key, $attempts + 1, 10 * MINUTE_IN_SECONDS);

    // 1. Sanitize input fields (supports residential, civil, investor & realtor/architect referral forms)
    $name         = sanitize_text_field((string) ($data['name'] ?? $data['fullName'] ?? 'Prospective Client'));
    $email        = sanitize_email((string) ($data['email'] ?? ''));
    $phone        = sanitize_text_field((string) ($data['phone'] ?? $data['phoneNumber'] ?? ''));
    $project_type = sanitize_text_field((string) ($data['project_type'] ?? $data['service'] ?? $data['corridor'] ?? '48-Hr Lot & Cost Feasibility'));
    $location     = sanitize_text_field((string) ($data['location'] ?? $data['corridor'] ?? $data['city'] ?? $data['region'] ?? 'Sea-to-Sky / Metro Vancouver'));
    $lot_address  = sanitize_text_field((string) ($data['lot_address'] ?? $data['lotAddress'] ?? $data['address'] ?? $data['project_address'] ?? ''));
    $budget       = sanitize_text_field((string) ($data['budget'] ?? 'Not Specified'));
    $brokerage    = sanitize_text_field((string) ($data['brokerage'] ?? $data['managing_brokerage'] ?? $data['firm'] ?? ''));
    $message      = sanitize_textarea_field((string) ($data['message'] ?? $data['details'] ?? $data['notes'] ?? $data['scope'] ?? ''));
    $source_url   = esc_url_raw((string) ($data['source_url'] ?? $_SERVER['HTTP_REFERER'] ?? home_url('/')));
    $timestamp    = current_time('mysql');

    if ($email === '' && $phone === '') {
        return new WP_Error(
            'missing_contact',
            'Please provide either a valid email address or phone number.',
            array('status' => 400)
        );
    }

    if ($brokerage !== '') {
        $message = trim("[Brokerage / Firm: {$brokerage}]\n" . $message);
    }

    $lead_record = array(
        'id'           => uniqid('kp_lead_', true),
        'timestamp'    => $timestamp,
        'name'         => $name !== '' ? $name : 'Prospective Client',
        'email'        => $email,
        'phone'        => $phone,
        'project_type' => $project_type,
        'location'     => $location,
        'lot_address'  => $lot_address,
        'budget'       => $budget,
        'brokerage'    => $brokerage,
        'message'      => $message,
        'source_url'   => $source_url,
        'ip_address'   => $ip_address,
        'status'       => 'new',
    );

    // 2. Persist lead to WordPress Database (wp_options log, capped at 500 newest entries)
    $leads_log = get_option('keystone_leads_log', array());
    if (!is_array($leads_log)) {
        $leads_log = array();
    }
    array_unshift($leads_log, $lead_record);
    if (count($leads_log) > 500) {
        $leads_log = array_slice($leads_log, 0, 500);
    }
    update_option('keystone_leads_log', $leads_log, false);

    // 3. Dispatch Instant Executive Notification to Wayne Stevenson
    $to          = 'keystone4vancouver@gmail.com, keystonepossibilities@gmail.com';
    $subject_loc = $lot_address !== '' ? $lot_address : $location;
    $subject     = '[KEYSTONE INQUIRY] ' . $lead_record['name'] . ' — ' . $project_type . ' (' . $subject_loc . ')';

    $headers = array(
        'Content-Type: text/html; charset=UTF-8',
        'From: Keystone Possibilities <info@keystonepossibilities.ca>',
    );
    if ($email !== '') {
        $headers[] = 'Reply-To: ' . $lead_record['name'] . ' <' . $email . '>';
    }

    $body = '<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #04070d; color: #f8fafc; margin: 0; padding: 20px; }
.container { max-width: 620px; margin: 0 auto; background: #0a101d; border: 1px solid #d4af37; border-radius: 12px; padding: 28px; }
.header { border-bottom: 1px solid rgba(212, 175, 55, 0.3); padding-bottom: 16px; margin-bottom: 20px; }
.gold { color: #d4af37; font-weight: 800; font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.05em; }
.sub { color: #94a3b8; font-size: 0.85rem; margin-top: 4px; }
.row { margin-bottom: 11px; font-size: 0.94rem; }
.label { color: #38bdf8; font-weight: 700; width: 148px; display: inline-block; }
.value { color: #f8fafc; }
.msg-box { background: rgba(13, 21, 38, 0.9); border-left: 3px solid #d4af37; padding: 14px; margin-top: 16px; border-radius: 0 8px 8px 0; color: #e2e8f0; line-height: 1.55; font-size: 0.94rem; }
.footer { margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 0.78rem; color: #94a3b8; }
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="gold">Keystone Possibilities Ltd.</div>
        <div class="sub">Executive Pre-Construction, Civil &amp; Partner Desk Intake</div>
    </div>
    <div class="row"><span class="label">Client Name:</span><span class="value"><strong>' . esc_html($lead_record['name']) . '</strong></span></div>
    <div class="row"><span class="label">Email:</span><span class="value"><a href="mailto:' . esc_attr($email) . '" style="color:#38bdf8;">' . esc_html($email) . '</a></span></div>
    <div class="row"><span class="label">Phone:</span><span class="value"><a href="tel:' . esc_attr($phone) . '" style="color:#38bdf8;">' . esc_html($phone) . '</a></span></div>
    ' . ($lot_address !== '' ? '<div class="row"><span class="label">Civic Lot Address:</span><span class="value" style="color:#f3d98b; font-weight:700;">' . esc_html($lot_address) . '</span></div>' : '') . '
    ' . ($brokerage !== '' ? '<div class="row"><span class="label">Brokerage / Firm:</span><span class="value">' . esc_html($brokerage) . '</span></div>' : '') . '
    <div class="row"><span class="label">Project Scope:</span><span class="value">' . esc_html($project_type) . '</span></div>
    <div class="row"><span class="label">Corridor / Site:</span><span class="value">' . esc_html($location) . '</span></div>
    <div class="row"><span class="label">Target Budget:</span><span class="value">' . esc_html($budget) . '</span></div>
    <div class="row"><span class="label">Received At:</span><span class="value">' . esc_html($timestamp) . ' (Pacific)</span></div>
    <div class="row"><span class="label">Source Page:</span><span class="value"><a href="' . esc_url($source_url) . '" style="color:#94a3b8;">' . esc_html($source_url) . '</a></span></div>
    ' . ($message !== '' ? '<div class="msg-box"><strong>Project / Parcel Notes:</strong><br>' . nl2br(esc_html($message)) . '</div>' : '') . '
    <div class="footer">
        BC Housing Licensed Residential Builder #52603 · BC Hydro ES54 Registered Civil Contractor<br>
        1 Watts Point Road, Squamish, BC V8B 0B1 · (604) 848-9688
    </div>
</div>
</body>
</html>';

    $mail_sent = wp_mail($to, $subject, $body, $headers);
    if (!$mail_sent) {
        error_log('Keystone Lead Dispatch Warning: wp_mail failed for lead ID ' . $lead_record['id']);
    }

    return new WP_REST_Response(array(
        'success' => true,
        'message' => 'Thank you, ' . $lead_record['name'] . '. Wayne Stevenson (#52603) has received your parcel & project details and will follow up within 24–48 business hours.',
        'lead_id' => $lead_record['id'],
    ), 200);
}

// ── 3. One-Time Database Sanitization Migration (Preserved for Regression Parity) ──
add_action('init', 'keystone_possibilities_run_v252_migration', 6);
function keystone_possibilities_run_v252_migration(): void
{
    $migration_key = 'keystone_migration_v252_css_cleaned';
    if (get_option($migration_key)) {
        return;
    }

    $home = get_post(563);
    if ($home instanceof WP_Post && !empty($home->post_content)) {
        $content  = (string) $home->post_content;
        $patterns = array(
            '/<style\b[^>]*>[\s\S]*?<\/style>/i',
            '/(<p>\s*)?\.kp-regional-grid\s*(?:>|&gt;)\s*p\s*\{[^}]*\}\s*(<\/p>)?/i',
            '/(<p>\s*)?\.kp-glass:empty\s*\{[^}]*\}\s*(<\/p>)?/i',
            '/(<p>\s*)?\.kp-regional-grid\s*\{[^}]*\}\s*(<\/p>)?/i',
        );
        $cleaned = (string) preg_replace($patterns, '', $content);
        $cleaned = str_replace('KEYSTONE RECOMPOSITION', 'KEYSTONE POSSIBILITIES LTD', $cleaned);
        if ($cleaned !== $content) {
            wp_update_post(array(
                'ID'           => 563,
                'post_content' => $cleaned,
            ));
        }
    }

    update_option($migration_key, current_time('mysql'), false);
}
