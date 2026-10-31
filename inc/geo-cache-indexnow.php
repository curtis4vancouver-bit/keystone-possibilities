<?php
/**
 * Keystone Possibilities Child Theme — GEO Root Synchronizer, Full-Page Edge/LiteSpeed Cache Enabler,
 * AI-Crawler .htaccess Allowlist, Utility Noindex Guard, and IndexNow Batch Syndication Engine.
 *
 * Certified BC Housing Licensed Residential Builder #52603 | BC Hydro Civil Contractor (ES54)
 *
 * @package KeystonePossibilitiesChild
 * @version 2026.10.31.1
 */

if (!defined('ABSPATH')) {
    exit;
}

if (!defined('KEYSTONE_POSS_GEO_SYNC_VERSION')) {
    define('KEYSTONE_POSS_GEO_SYNC_VERSION', '2026.10.31.1');
}

// ── 1. Expose Rank Math SEO Meta Fields to Authenticated WP REST API ─────────
add_action('init', 'keystone_poss_register_rank_math_rest_meta', 5);
function keystone_poss_register_rank_math_rest_meta(): void {
    $meta_keys = array(
        'rank_math_title',
        'rank_math_description',
        'rank_math_focus_keyword',
        'rank_math_canonical_url',
    );
    foreach (array('page', 'post') as $post_type) {
        foreach ($meta_keys as $meta_key) {
            register_post_meta($post_type, $meta_key, array(
                'show_in_rest'      => true,
                'single'            => true,
                'type'              => 'string',
                'sanitize_callback' => 'sanitize_text_field',
                'auth_callback'     => function (): bool {
                    return current_user_can('edit_posts');
                },
            ));
        }
    }
}

// ── 2. Canonical Legacy 301 Redirect Map (PHP + .htaccess Single-Hop 200 OK) ─
function keystone_poss_get_canonical_301_map(): array {
    return array(
        // Fix #1c Core GSC & Legacy 404 Slugs
        '/bill-44-multiplex-guide/'                                                   => '/north-vancouver-multiplex-conversions/',
        '/bill-44-multiplex-guide'                                                    => '/north-vancouver-multiplex-conversions/',
        '/portfolio-old/'                                                             => '/portfolio-general-contractor-squamish/',
        '/portfolio-old'                                                              => '/portfolio-general-contractor-squamish/',
        '/projects/'                                                                  => '/portfolio-general-contractor-squamish/',
        '/projects'                                                                   => '/portfolio-general-contractor-squamish/',
        '/2026/09/05/why-4-storey-multiplexes-snap-holdowns-bcbc-2024-simpson-ats-guide/' => '/2026/10/08/why-4-storey-multiplexes-fail-lateral-shear/',
        '/2026/09/05/why-4-storey-multiplexes-snap-holdowns-bcbc-2024-simpson-ats-guide'  => '/2026/10/08/why-4-storey-multiplexes-fail-lateral-shear/',
        '/victoria-bill-44-multiplex-builder/'                                        => '/vancouver-island-custom-homes/',
        '/victoria-bill-44-multiplex-builder'                                         => '/vancouver-island-custom-homes/',
        '/victoria-custom-homes/'                                                     => '/vancouver-island-custom-homes/',
        '/victoria-custom-homes'                                                      => '/vancouver-island-custom-homes/',

        // Fix #1c 7 Old llms-full.txt / llms.txt Dead Slugs
        '/ai-construction-engineering/'                                               => '/services-general-contractor-squamish/',
        '/ai-construction-engineering'                                                => '/services-general-contractor-squamish/',
        '/bc-developer-portal/'                                                       => '/feasibility-plan/',
        '/bc-developer-portal'                                                        => '/feasibility-plan/',
        '/case-study-builder/'                                                        => '/portfolio-general-contractor-squamish/',
        '/case-study-builder'                                                         => '/portfolio-general-contractor-squamish/',
        '/credentials/'                                                               => '/about-us-general-contractor-squamish/',
        '/credentials'                                                                => '/about-us-general-contractor-squamish/',
        '/feasibility-retainer/'                                                      => '/feasibility-plan/',
        '/feasibility-retainer'                                                       => '/feasibility-plan/',
        '/mexico-gateway/'                                                            => '/',
        '/mexico-gateway'                                                             => '/',
        '/step-code-5-engineering/'                                                   => '/2026/10/27/hydronic-radiant-floor-erv-engineering/',
        '/step-code-5-engineering'                                                    => '/2026/10/27/hydronic-radiant-floor-erv-engineering/',

        // Legacy Regional Short-Slugs & Old llms.txt Links
        '/project-management/'                                                        => '/services-general-contractor-squamish/',
        '/project-management'                                                         => '/services-general-contractor-squamish/',
        '/vancouver/'                                                                 => '/north-vancouver-multiplex-conversions/',
        '/vancouver'                                                                  => '/north-vancouver-multiplex-conversions/',
        '/vancouver-multiplex/'                                                       => '/2026/10/22/vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide/',
        '/vancouver-multiplex'                                                        => '/2026/10/22/vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide/',
        '/west-vancouver/'                                                            => '/west-vancouver-custom-homes/',
        '/west-vancouver'                                                             => '/west-vancouver-custom-homes/',
        '/north-vancouver/'                                                           => '/north-vancouver-custom-homes/',
        '/north-vancouver'                                                            => '/north-vancouver-custom-homes/',
        '/squamish/'                                                                  => '/squamish-custom-homes/',
        '/squamish'                                                                   => '/squamish-custom-homes/',
        '/whistler/'                                                                  => '/whistler-custom-homes/',
        '/whistler'                                                                   => '/whistler-custom-homes/',
        '/contact/'                                                                   => '/contact-general-contractor-squamish/',
        '/contact'                                                                    => '/contact-general-contractor-squamish/',
    );
}

// ── 3. Priority-0 301 Redirects, /llms*.txt Fallback & Sync Endpoint ─────────
add_action('init', 'keystone_poss_priority_zero_geo_router', 0);
add_action('template_redirect', 'keystone_poss_priority_zero_geo_router', 0);
function keystone_poss_priority_zero_geo_router(): void {
    // A. Explicit Authenticated Root GEO + .htaccess + IndexNow Sync Trigger
    if (isset($_GET['keystone_poss_sync_geo']) && $_GET['keystone_poss_sync_geo'] === 'sovereign_execute') {
        if (!function_exists('is_user_logged_in') || !is_user_logged_in() || !current_user_can('manage_options')) {
            if (current_action() === 'init') {
                return;
            }
            status_header(403);
            header('Content-Type: application/json; charset=utf-8');
            header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
            echo wp_json_encode(array('status' => 'error', 'message' => 'Authenticated administrator session required.'));
            exit;
        }
        $telemetry = keystone_poss_sync_root_geo_and_htaccess(true);
        status_header(200);
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
        header('X-LiteSpeed-Cache-Control: no-cache');
        header('X-LiteSpeed-Purge: *');
        echo wp_json_encode($telemetry, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
        exit;
    }

    if (is_admin() || (defined('REST_REQUEST') && REST_REQUEST) || (defined('DOING_CRON') && DOING_CRON) || (defined('DOING_AJAX') && DOING_AJAX)) {
        return;
    }

    $uri  = (string) ($_SERVER['REQUEST_URI'] ?? '');
    $path = (string) strtok($uri, '?');

    // B0. Serve clean /robots.txt at priority 0 if dynamic request reaches PHP
    if ($path === '/robots.txt') {
        if (!headers_sent()) {
            header_remove('Set-Cookie');
            status_header(200);
            header('Content-Type: text/plain; charset=utf-8');
            header('Cache-Control: public, max-age=300, s-maxage=86400');
            header('X-LiteSpeed-Cache-Control: public,max-age=86400');
        }
        echo keystone_poss_build_clean_robots_txt();
        exit;
    }

    // B. Serve /llms.txt and /llms-full.txt cleanly if static file was bypassed
    if ($path === '/llms.txt' || $path === '/llms-full.txt') {
        $rel_file = ($path === '/llms-full.txt') ? '/llms-full.txt' : '/llms.txt';
        $theme_file = get_stylesheet_directory() . $rel_file;
        $root_file  = ABSPATH . ltrim($rel_file, '/');
        $serve_file = file_exists($theme_file) ? $theme_file : (file_exists($root_file) ? $root_file : '');
        if ($serve_file !== '') {
            if (!headers_sent()) {
                header_remove('Set-Cookie');
                status_header(200);
                header('Content-Type: text/plain; charset=utf-8');
                header('Cache-Control: public, max-age=300, s-maxage=86400');
                header('X-LiteSpeed-Cache-Control: public,max-age=86400');
                header('X-Robots-Tag: all');
            }
            readfile($serve_file);
            exit;
        }
    }

    // C. Serve dynamic IndexNow verification key file (/32hex.txt)
    $key = keystone_poss_resolve_indexnow_key();
    if ($path === '/' . $key . '.txt') {
        if (!headers_sent()) {
            header_remove('Set-Cookie');
            status_header(200);
            header('Content-Type: text/plain; charset=utf-8');
            header('Cache-Control: public, max-age=86400, s-maxage=604800');
            header('X-LiteSpeed-Cache-Control: public,max-age=604800');
        }
        echo $key;
        exit;
    }

    // D. Execute Priority-0 Single-Hop 301 Redirects
    $map = keystone_poss_get_canonical_301_map();
    if (isset($map[$path])) {
        if (!headers_sent()) {
            header_remove('Set-Cookie');
            header('Cache-Control: public, max-age=3600, s-maxage=86400');
        }
        wp_safe_redirect(home_url($map[$path]), 301);
        exit;
    }
}

// ── 4. Utility Login/Portal Noindex Guard (/client-login/, /project-management-wp/) ─
function keystone_poss_is_utility_noindex_request(): bool {
    $uri  = (string) ($_SERVER['REQUEST_URI'] ?? '');
    $path = '/' . trim((string) strtok($uri, '?'), '/') . '/';
    if (in_array($path, array('/client-login/', '/project-management-wp/', '/client-portal-demo/'), true)) {
        return true;
    }
    if (function_exists('is_page') && did_action('wp') && is_page(array('client-login', 'project-management-wp', 'client-portal-demo'))) {
        return true;
    }
    return false;
}

add_action('send_headers', 'keystone_poss_emit_utility_noindex_headers', 1);
add_action('template_redirect', 'keystone_poss_emit_utility_noindex_headers', 1);
function keystone_poss_emit_utility_noindex_headers(): void {
    if (!headers_sent() && keystone_poss_is_utility_noindex_request()) {
        header('X-Robots-Tag: noindex, nofollow', true);
        header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0', true);
        header('X-LiteSpeed-Cache-Control: no-cache', true);
    }
}

add_filter('rank_math/frontend/robots', function (array $robots): array {
    if (keystone_poss_is_utility_noindex_request()) {
        $robots['index']  = 'noindex';
        $robots['follow'] = 'nofollow';
        unset($robots['noindex'], $robots['nofollow']);
    }
    return $robots;
}, 999, 1);

add_action('wp_head', function (): void {
    if (!class_exists('RankMath') && keystone_poss_is_utility_noindex_request()) {
        echo '<meta name="robots" content="noindex, nofollow" />' . "\n";
    }
}, 1);

add_filter('rank_math/sitemap/entry', function ($url, $type = '', $object = null) {
    if (empty($url) || !is_array($url) || empty($url['loc'])) {
        return $url;
    }
    $loc = (string) $url['loc'];
    foreach (array('/client-login', '/project-management-wp', '/client-portal-demo') as $blocked) {
        if (stripos($loc, $blocked) !== false) {
            return false;
        }
    }
    return $url;
}, 5, 3);

// ── 5. Full-Page Edge & LiteSpeed Cache Enablement (Anonymous Public GET Only) ─
function keystone_poss_is_cacheable_anonymous_frontend_get(): bool {
    $method = strtoupper((string) ($_SERVER['REQUEST_METHOD'] ?? 'GET'));
    if (!in_array($method, array('GET', 'HEAD'), true)) {
        return false;
    }
    if (!empty($_GET)) {
        return false;
    }
    if (
        (function_exists('is_admin') && is_admin()) ||
        (function_exists('is_user_logged_in') && is_user_logged_in()) ||
        (defined('REST_REQUEST') && REST_REQUEST) ||
        (defined('DOING_AJAX') && DOING_AJAX) ||
        (defined('DOING_CRON') && DOING_CRON) ||
        (defined('WP_CLI') && WP_CLI) ||
        (defined('XMLRPC_REQUEST') && XMLRPC_REQUEST)
    ) {
        return false;
    }

    // Never cache if any WordPress authentication, password, or comment cookie is present
    if (!empty($_COOKIE) && is_array($_COOKIE)) {
        foreach (array_keys($_COOKIE) as $cookie_name) {
            $cn = (string) $cookie_name;
            if (
                strpos($cn, 'wordpress_logged_in_') === 0 ||
                strpos($cn, 'wordpress_sec_') === 0 ||
                strpos($cn, 'wp-postpass_') === 0 ||
                strpos($cn, 'comment_author_') === 0
            ) {
                return false;
            }
        }
    }

    $uri  = (string) ($_SERVER['REQUEST_URI'] ?? '');
    $path = strtolower((string) strtok($uri, '?'));
    $excluded_prefixes = array(
        '/wp-admin',
        '/wp-login',
        '/wp-json',
        '/xmlrpc.php',
        '/client-login',
        '/project-management-wp',
        '/client-portal',
        '/feed',
    );
    foreach ($excluded_prefixes as $prefix) {
        if (strpos($path, $prefix) === 0) {
            return false;
        }
    }
    if (strpos($path, 'sitemap') !== false || substr($path, -4) === '.xml') {
        return false;
    }
    if (function_exists('is_404') && did_action('wp') && (is_404() || is_search() || is_feed())) {
        return false;
    }

    return true;
}

function keystone_poss_apply_public_edge_cache_headers(): void {
    if (headers_sent() || !keystone_poss_is_cacheable_anonymous_frontend_get()) {
        return;
    }
    $code = http_response_code();
    if ($code !== false && $code !== 200) {
        return;
    }
    // Strip plugin Set-Cookie (e.g. official-facebook-pixel _fbp) that forces Atomic/LiteSpeed cache MISS
    header_remove('Set-Cookie');
    header_remove('Pragma');
    header_remove('Expires');
    header('Cache-Control: public, max-age=300, s-maxage=604800', true);
    header('X-LiteSpeed-Cache-Control: public,max-age=604800', true);
}

add_action('init', function (): void {
    if (function_exists('header_register_callback')) {
        header_register_callback('keystone_poss_apply_public_edge_cache_headers');
    }
}, 1);
add_action('init', 'keystone_poss_apply_public_edge_cache_headers', 99999);
add_action('send_headers', 'keystone_poss_apply_public_edge_cache_headers', 99999);
add_action('template_redirect', 'keystone_poss_apply_public_edge_cache_headers', 99999);
add_action('wp_head', 'keystone_poss_apply_public_edge_cache_headers', 99999);
add_action('wp_footer', 'keystone_poss_apply_public_edge_cache_headers', 99999);
add_action('shutdown', 'keystone_poss_apply_public_edge_cache_headers', 0);

// ── 6. Authoritative Clean robots.txt Generator & Filter ─────────────────────
function keystone_poss_build_clean_robots_txt(): string {
    return implode("\n", array(
        'User-agent: *',
        'Disallow: /wp-admin/',
        'Disallow: /client-login/',
        'Disallow: /project-management-wp/',
        'Disallow: /*?share=',
        'Allow: /wp-admin/admin-ajax.php',
        'Allow: /wp-content/uploads/',
        'Allow: /wp-content/themes/',
        'Allow: /wp-includes/',
        'Allow: /llms.txt',
        'Allow: /llms-full.txt',
        '',
        '# AI & Generative Search Engine Crawlers (GEO)',
        'User-agent: GPTBot',
        'Allow: /',
        'Allow: /llms.txt',
        'Allow: /llms-full.txt',
        '',
        'User-agent: OAI-SearchBot',
        'Allow: /',
        '',
        'User-agent: ChatGPT-User',
        'Allow: /',
        '',
        'User-agent: ClaudeBot',
        'Allow: /',
        'Allow: /llms.txt',
        'Allow: /llms-full.txt',
        '',
        'User-agent: PerplexityBot',
        'Allow: /',
        'Allow: /llms.txt',
        'Allow: /llms-full.txt',
        '',
        'User-agent: Google-Extended',
        'Allow: /',
        '',
        'User-agent: Applebot-Extended',
        'Allow: /',
        '',
        'Sitemap: https://keystonepossibilities.ca/sitemap_index.xml',
        'Sitemap: https://keystonepossibilities.ca/keystone-video-sitemap.xml',
        '',
    ));
}

add_filter('robots_txt', function ($output, $public): string {
    return keystone_poss_build_clean_robots_txt();
}, 999999, 2);

// ── 7. IndexNow Key Resolver & Canonical URL Collector ───────────────────────
function keystone_poss_resolve_indexnow_key(): string {
    // 1. Reuse Rank Math Instant Indexing key if present and valid 32-char hex/alnum
    $rm_opts = get_option('rank-math-options-instant-indexing');
    if (is_array($rm_opts) && !empty($rm_opts['indexnow_api_key'])) {
        $candidate = trim((string) $rm_opts['indexnow_api_key']);
        if (preg_match('/^[a-f0-9]{32}$/i', $candidate)) {
            update_option('keystone_poss_indexnow_key', strtolower($candidate), false);
            return strtolower($candidate);
        }
    }

    // 2. Check stored keystone_poss_indexnow_key
    $stored = trim((string) get_option('keystone_poss_indexnow_key', ''));
    if (preg_match('/^[a-f0-9]{32}$/i', $stored)) {
        return strtolower($stored);
    }

    // 3. Default deterministic 32-char hex key
    $default_key = defined('KEYSTONE_POSSIBILITIES_INDEXNOW_KEY')
        ? strtolower(trim((string) KEYSTONE_POSSIBILITIES_INDEXNOW_KEY))
        : '8f4b2e9a1c6d7e3f5a0b9c8d7e6f5a4b';
    if (!preg_match('/^[a-f0-9]{32}$/', $default_key)) {
        $default_key = bin2hex(random_bytes(16));
    }
    update_option('keystone_poss_indexnow_key', $default_key, false);
    return $default_key;
}

function keystone_poss_collect_canonical_indexnow_urls(): array {
    $urls = array(
        home_url('/'),
        home_url('/industry-partners/'),
        home_url('/vancouver-island-custom-homes/'),
        home_url('/llms.txt'),
        home_url('/llms-full.txt'),
    );

    $excluded_slugs = array(
        'client-login',
        'project-management-wp',
        'client-portal-demo',
        'videos',
        'whistler-luxury-builder',
        'squamish-custom-home-builder',
        'sample-page',
    );

    $redirect_sources = array_keys(keystone_poss_get_canonical_301_map());

    $items = get_posts(array(
        'post_type'      => array('post', 'page'),
        'post_status'    => 'publish',
        'posts_per_page' => 200,
        'no_found_rows'  => true,
    ));

    foreach ($items as $item) {
        if (in_array((string) $item->post_name, $excluded_slugs, true)) {
            continue;
        }
        $robots = get_post_meta($item->ID, 'rank_math_robots', true);
        if ((is_array($robots) && in_array('noindex', $robots, true)) || (is_string($robots) && stripos($robots, 'noindex') !== false)) {
            continue;
        }
        $permalink = get_permalink($item->ID);
        if (!$permalink) {
            continue;
        }
        $path = (string) wp_parse_url($permalink, PHP_URL_PATH);
        if (in_array($path, $redirect_sources, true)) {
            continue;
        }
        $urls[] = $permalink;
    }

    return array_values(array_unique(array_filter($urls)));
}

// ── 8. Build # BEGIN KEYSTONE_POSS_GEO_CACHE .htaccess Block ─────────────────
function keystone_poss_build_htaccess_block(): string {
    $lines = array(
        '# BEGIN KEYSTONE_POSS_GEO_CACHE',
        '<IfModule LiteSpeed>',
        'CacheLookup on',
        '</IfModule>',
        '<IfModule mod_rewrite.c>',
        'RewriteEngine On',
        '# AI & Search Crawler Bot-Challenge Bypass Flags',
        'RewriteCond %{HTTP_USER_AGENT} (GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|anthropic-ai|PerplexityBot|Perplexity-User|Applebot-Extended|Google-Extended|Bingbot|AdIdxBot|DuckDuckBot|IndexNow) [NC]',
        'RewriteRule .* - [E=verifycaptcha:drop,E=noabort:1,E=noconntimeout:1]',
        '',
        '# Canonical Single-Hop 301 Redirects for Legacy 404 & Old GEO Slugs',
        'RewriteRule ^bill-44-multiplex-guide/?$ /north-vancouver-multiplex-conversions/ [R=301,L]',
        'RewriteRule ^portfolio-old/?$ /portfolio-general-contractor-squamish/ [R=301,L]',
        'RewriteRule ^projects/?$ /portfolio-general-contractor-squamish/ [R=301,L]',
        'RewriteRule ^2026/09/05/why-4-storey-multiplexes-snap-holdowns-bcbc-2024-simpson-ats-guide/?$ /2026/10/08/why-4-storey-multiplexes-fail-lateral-shear/ [R=301,L]',
        'RewriteRule ^victoria-bill-44-multiplex-builder/?$ /vancouver-island-custom-homes/ [R=301,L]',
        'RewriteRule ^ai-construction-engineering/?$ /services-general-contractor-squamish/ [R=301,L]',
        'RewriteRule ^bc-developer-portal/?$ /feasibility-plan/ [R=301,L]',
        'RewriteRule ^case-study-builder/?$ /portfolio-general-contractor-squamish/ [R=301,L]',
        'RewriteRule ^credentials/?$ /about-us-general-contractor-squamish/ [R=301,L]',
        'RewriteRule ^feasibility-retainer/?$ /feasibility-plan/ [R=301,L]',
        'RewriteRule ^mexico-gateway/?$ / [R=301,L]',
        'RewriteRule ^step-code-5-engineering/?$ /2026/10/27/hydronic-radiant-floor-erv-engineering/ [R=301,L]',
        'RewriteRule ^project-management/?$ /services-general-contractor-squamish/ [R=301,L]',
        '</IfModule>',
        '# END KEYSTONE_POSS_GEO_CACHE',
    );
    return implode("\n", $lines) . "\n\n";
}

// ── 9. Resolve All Writable Webroots (Atomic /srv/htdocs/ + Standard ABSPATH) ─
function keystone_poss_resolve_writable_webroots(): array {
    $candidates = array();
    if (!empty($_SERVER['DOCUMENT_ROOT'])) {
        $candidates[] = rtrim((string) $_SERVER['DOCUMENT_ROOT'], '/\\');
    }
    if (defined('WP_CONTENT_DIR')) {
        $candidates[] = rtrim(dirname((string) WP_CONTENT_DIR), '/\\');
    }
    if (defined('ABSPATH')) {
        $candidates[] = rtrim((string) ABSPATH, '/\\');
    }
    $roots = array();
    foreach (array_values(array_unique($candidates)) as $dir) {
        if ($dir !== '' && @is_dir($dir) && @is_writable($dir)) {
            $roots[] = $dir . '/';
        }
    }
    return !empty($roots) ? $roots : array(ABSPATH);
}

// ── 10. Master Idempotent Root GEO, .htaccess & IndexNow Synchronizer ────────
function keystone_poss_sync_root_geo_and_htaccess(bool $force = false): array {
    $webroots = keystone_poss_resolve_writable_webroots();
    $telemetry = array(
        'status'               => 'ok',
        'version'              => KEYSTONE_POSS_GEO_SYNC_VERSION,
        'timestamp_utc'        => gmdate('c'),
        'forced'               => $force,
        'webroots'             => $webroots,
        'llms_copied'          => false,
        'llms_full_copied'     => false,
        'robots_file_cleaned'  => false,
        'robots_rm_cleaned'    => false,
        'utility_noindex_set'  => array(),
        'htaccess_updated'     => false,
        'htaccess_backup'      => '',
        'indexnow_key'         => '',
        'indexnow_file'        => '',
        'indexnow_file_ok'     => false,
        'indexnow_api_code'    => 0,
        'indexnow_bing_code'   => 0,
        'submitted_urls_count' => 0,
        'submitted_urls'       => array(),
    );

    $theme_dir    = get_stylesheet_directory();
    $clean_robots = keystone_poss_build_clean_robots_txt();
    $key          = keystone_poss_resolve_indexnow_key();
    $telemetry['indexnow_key'] = $key;

    foreach ($webroots as $root_dir) {
        // A. Copy theme llms.txt & llms-full.txt -> writable webroot for <100ms direct static serving
        if (file_exists($theme_dir . '/llms.txt')) {
            if (@copy($theme_dir . '/llms.txt', $root_dir . 'llms.txt')) {
                $telemetry['llms_copied'] = true;
            }
        }
        if (file_exists($theme_dir . '/llms-full.txt')) {
            if (@copy($theme_dir . '/llms-full.txt', $root_dir . 'llms-full.txt')) {
                $telemetry['llms_full_copied'] = true;
            }
        }

        // B. Backup & write clean static robots.txt in webroot so nginx/LiteSpeed serves clean video sitemap
        $root_robots = $root_dir . 'robots.txt';
        if (file_exists($root_robots)) {
            $robots_bak = $root_dir . 'robots.txt.bak-20261031';
            if (!file_exists($robots_bak)) {
                @copy($root_robots, $robots_bak);
            }
        }
        if (@file_put_contents($root_robots, $clean_robots) !== false) {
            $telemetry['robots_file_cleaned'] = true;
        }

        // C. Safely backup & prepend # BEGIN KEYSTONE_POSS_GEO_CACHE to webroot .htaccess
        $htaccess_path = $root_dir . '.htaccess';
        $backup_path   = $root_dir . '.htaccess.bak-20261031';
        $existing_ht   = '';
        if (file_exists($htaccess_path) && is_readable($htaccess_path)) {
            $existing_ht = (string) file_get_contents($htaccess_path);
            if (!file_exists($backup_path)) {
                if (@copy($htaccess_path, $backup_path)) {
                    $telemetry['htaccess_backup'] = $backup_path;
                }
            } else {
                $telemetry['htaccess_backup'] = $backup_path;
            }
        }
        $cleaned_ht = preg_replace(
            '/# BEGIN KEYSTONE_POSS_GEO_CACHE.*?# END KEYSTONE_POSS_GEO_CACHE\s*/is',
            '',
            $existing_ht
        );
        $new_ht = keystone_poss_build_htaccess_block() . ltrim((string) $cleaned_ht);
        if (@file_put_contents($htaccess_path, $new_ht) !== false) {
            $telemetry['htaccess_updated'] = true;
        }

        // D. Write 32-char hex IndexNow key verification file <webroot>/<key>.txt
        $key_file = $root_dir . $key . '.txt';
        if (@file_put_contents($key_file, $key) !== false) {
            $telemetry['indexnow_file']    = $key_file;
            $telemetry['indexnow_file_ok'] = true;
        }
    }

    // E. Clean Rank Math robots_txt_content option & Code Snippets / options if cached
    $rm_gen = get_option('rank-math-options-general');
    if (is_array($rm_gen) && isset($rm_gen['robots_txt_content'])) {
        $rm_gen['robots_txt_content'] = $clean_robots;
        update_option('rank-math-options-general', $rm_gen);
        $telemetry['robots_rm_cleaned'] = true;
    }

    // F. Persist Rank Math noindex,nofollow postmeta on utility login/portal pages
    foreach (array('client-login', 'project-management-wp', 'client-portal-demo') as $util_slug) {
        $pg = get_page_by_path($util_slug, OBJECT, 'page');
        if ($pg && !empty($pg->ID)) {
            update_post_meta($pg->ID, 'rank_math_robots', array('noindex', 'nofollow'));
            $telemetry['utility_noindex_set'][] = array('slug' => $util_slug, 'id' => (int) $pg->ID);
        }
    }

    // G. Submit IndexNow Batch POST to api.indexnow.org + www.bing.com
    $urls = keystone_poss_collect_canonical_indexnow_urls();
    $telemetry['submitted_urls']       = $urls;
    $telemetry['submitted_urls_count'] = count($urls);

    $host    = (string) wp_parse_url(home_url('/'), PHP_URL_HOST);
    $payload = wp_json_encode(array(
        'host'        => $host,
        'key'         => $key,
        'keyLocation' => home_url('/' . $key . '.txt'),
        'urlList'     => $urls,
    ));

    $post_args = array(
        'headers' => array('Content-Type' => 'application/json; charset=utf-8'),
        'body'    => $payload,
        'timeout' => 15,
    );

    $resp_api  = wp_remote_post('https://api.indexnow.org/indexnow', $post_args);
    $resp_bing = wp_remote_post('https://www.bing.com/indexnow', $post_args);

    $telemetry['indexnow_api_code']  = is_wp_error($resp_api) ? 0 : (int) wp_remote_retrieve_response_code($resp_api);
    $telemetry['indexnow_bing_code'] = is_wp_error($resp_bing) ? 0 : (int) wp_remote_retrieve_response_code($resp_bing);

    // H. Flush Object Cache & Rank Math Sitemap Storage
    delete_transient('keystone_video_sitemap_xml_cache');
    delete_transient('rank_math_sitemap_cache');
    if (class_exists('\\RankMath\\Sitemap\\Cache')) {
        \RankMath\Sitemap\Cache::invalidate_storage();
    }
    if (function_exists('wp_cache_flush')) {
        wp_cache_flush();
    }

    update_option('keystone_poss_geo_sync_ver', KEYSTONE_POSS_GEO_SYNC_VERSION, true);
    return $telemetry;
}

add_action('init', function (): void {
    if (get_option('keystone_poss_geo_sync_ver') !== KEYSTONE_POSS_GEO_SYNC_VERSION) {
        keystone_poss_sync_root_geo_and_htaccess(false);
    }
}, 20);
