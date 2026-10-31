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

// ── 11. Rule 33 Quiet Luxury <head> Stylesheet for Sovereign GEO & Partner Pages ─
add_action('wp_head', 'keystone_poss_render_sovereign_geo_luxury_css', 999);
function keystone_poss_render_sovereign_geo_luxury_css(): void {
    if (is_admin()) {
        return;
    }
    ?>
    <style id="kp-sovereign-geo-luxury-css">
    html body .kp-sovereign-geo-wrapper {
        background-color: #04070d !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: clip !important;
        padding: 0 0 80px 0 !important;
        margin: 0 !important;
    }
    html body .kp-sovereign-geo-wrapper *,
    html body .kp-sovereign-geo-wrapper *::before,
    html body .kp-sovereign-geo-wrapper *::after {
        box-sizing: border-box !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-geo-hero {
        position: relative !important;
        text-align: center !important;
        padding: 64px 24px 54px 24px !important;
        background: radial-gradient(ellipse at 50% 0%, rgba(212, 175, 55, 0.16) 0%, rgba(56, 189, 248, 0.08) 42%, rgba(4, 7, 13, 1) 78%) !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.30) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-geo-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 0 24px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-eyebrow-pill {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 9px !important;
        padding: 8px 20px !important;
        border-radius: 9999px !important;
        background-color: rgba(56, 189, 248, 0.14) !important;
        border: 1px solid rgba(56, 189, 248, 0.55) !important;
        color: #38bdf8 !important;
        -webkit-text-fill-color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.76rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.11em !important;
        text-transform: uppercase !important;
        margin: 0 auto 22px auto !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.55), 0 0 16px rgba(56, 189, 248, 0.14) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-eyebrow-dot {
        width: 8px !important;
        height: 8px !important;
        border-radius: 9999px !important;
        background-color: #d4af37 !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.9) !important;
        display: inline-block !important;
        flex-shrink: 0 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-hero-lead {
        font-size: clamp(1.02rem, 1.3vw, 1.15rem) !important;
        color: #cbd5e1 !important;
        max-width: 900px !important;
        margin: 0 auto 30px auto !important;
        line-height: 1.72 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-cta-row {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 16px !important;
        margin: 10px auto 0 auto !important;
    }
    html body .kp-sovereign-geo-wrapper a.kp-gold-3d-pill,
    html body .entry-content .kp-sovereign-geo-wrapper a.kp-gold-3d-pill {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        min-height: 52px !important;
        padding: 14px 32px !important;
        border-radius: 9999px !important;
        background: linear-gradient(135deg, #f8df7e 0%, #d4af37 52%, #b68d24 100%) !important;
        background-color: #d4af37 !important;
        color: #04070d !important;
        -webkit-text-fill-color: #04070d !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        text-decoration: none !important;
        border: 1.5px solid #fef08a !important;
        box-shadow: 0 12px 30px rgba(212, 175, 55, 0.42), inset 0 1.5px 0 rgba(255, 255, 255, 0.65), inset 0 -2px 0 rgba(0, 0, 0, 0.22) !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease !important;
        cursor: pointer !important;
    }
    html body .kp-sovereign-geo-wrapper a.kp-gold-3d-pill:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 16px 36px rgba(212, 175, 55, 0.58), inset 0 1.5px 0 rgba(255, 255, 255, 0.8) !important;
        color: #04070d !important;
        -webkit-text-fill-color: #04070d !important;
        text-decoration: none !important;
    }
    html body .kp-sovereign-geo-wrapper a.kp-obsidian-blue-pill,
    html body .entry-content .kp-sovereign-geo-wrapper a.kp-obsidian-blue-pill {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 9px !important;
        min-height: 52px !important;
        padding: 14px 28px !important;
        border-radius: 9999px !important;
        background: rgba(56, 189, 248, 0.14) !important;
        background-color: rgba(56, 189, 248, 0.14) !important;
        background-image: none !important;
        color: #38bdf8 !important;
        -webkit-text-fill-color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.86rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        text-decoration: none !important;
        border: 1.5px solid rgba(56, 189, 248, 0.65) !important;
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.72), 0 0 18px rgba(56, 189, 248, 0.18) !important;
        transition: all 0.22s ease !important;
        cursor: pointer !important;
    }
    html body .kp-sovereign-geo-wrapper a.kp-obsidian-blue-pill:hover {
        border-color: #d4af37 !important;
        background-color: rgba(212, 175, 55, 0.16) !important;
        color: #f6d365 !important;
        -webkit-text-fill-color: #f6d365 !important;
        text-decoration: none !important;
        transform: translateY(-2px) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-trust-strip {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 20px !important;
        margin: 38px auto 0 auto !important;
        max-width: 1152px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-trust-stat {
        background: linear-gradient(180deg, rgba(13, 21, 38, 0.92) 0%, rgba(4, 7, 13, 0.96) 100%) !important;
        background-color: #04070d !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-radius: 18px !important;
        padding: 24px 22px !important;
        text-align: left !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.68), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-trust-kicker {
        display: block !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.11em !important;
        text-transform: uppercase !important;
        color: #38bdf8 !important;
        margin-bottom: 7px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-trust-val {
        display: block !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.06rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-bottom: 6px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-trust-sub {
        display: block !important;
        font-size: 0.84rem !important;
        color: #94a3b8 !important;
        line-height: 1.52 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-corridor-nav-bar {
        margin: 38px auto 14px auto !important;
        padding: 26px 28px !important;
        background: linear-gradient(180deg, rgba(11, 18, 32, 0.94) 0%, rgba(4, 7, 13, 0.98) 100%) !important;
        background-color: #04070d !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-radius: 18px !important;
        text-align: center !important;
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.65) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-corridor-nav-label {
        display: block !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.76rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #d4af37 !important;
        margin-bottom: 16px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-corridor-pills-wrap {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 10px !important;
    }
    html body .kp-sovereign-geo-wrapper a.kp-corridor-pill,
    html body .entry-content .kp-sovereign-geo-wrapper a.kp-corridor-pill {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        padding: 9px 18px !important;
        border-radius: 9999px !important;
        background: rgba(56, 189, 248, 0.14) !important;
        background-color: rgba(56, 189, 248, 0.14) !important;
        background-image: none !important;
        border: 1px solid rgba(56, 189, 248, 0.50) !important;
        color: #38bdf8 !important;
        -webkit-text-fill-color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.79rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
    }
    html body .kp-sovereign-geo-wrapper a.kp-corridor-pill:hover,
    html body .kp-sovereign-geo-wrapper a.kp-corridor-pill.is-active {
        background-color: rgba(212, 175, 55, 0.18) !important;
        border-color: #d4af37 !important;
        color: #f6d365 !important;
        -webkit-text-fill-color: #f6d365 !important;
        text-decoration: none !important;
        box-shadow: 0 0 16px rgba(212, 175, 55, 0.26) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-section-block {
        margin-top: 52px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-section-header {
        text-align: center !important;
        max-width: 860px !important;
        margin: 0 auto 32px auto !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-section-tag {
        display: inline-block !important;
        padding: 6px 16px !important;
        border-radius: 9999px !important;
        background-color: rgba(56, 189, 248, 0.14) !important;
        border: 1px solid rgba(56, 189, 248, 0.50) !important;
        color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.74rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.10em !important;
        text-transform: uppercase !important;
        margin-bottom: 14px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-pillars-grid {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 20px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-glass-card {
        background: linear-gradient(180deg, rgba(12, 20, 36, 0.92) 0%, rgba(4, 7, 13, 0.97) 100%) !important;
        background-color: #04070d !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-radius: 18px !important;
        padding: 28px 26px !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 16px 38px rgba(0, 0, 0, 0.70), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: transform 0.24s ease, border-color 0.24s ease !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-glass-card:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(212, 175, 55, 0.68) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-card-kicker {
        display: inline-block !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.73rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.11em !important;
        text-transform: uppercase !important;
        color: #d4af37 !important;
        margin-bottom: 10px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-glass-card h3 {
        margin: 0 0 12px 0 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.22rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        line-height: 1.32 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-glass-card p {
        margin: 0 0 14px 0 !important;
        font-size: 0.94rem !important;
        line-height: 1.68 !important;
        color: #cbd5e1 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-glass-card ul {
        margin: 0 !important;
        padding-left: 18px !important;
        color: #e2e8f0 !important;
        font-size: 0.90rem !important;
        line-height: 1.68 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-glass-card li {
        margin-bottom: 8px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-subcorridor-grid {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 20px !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-subcorridor-card {
        background: linear-gradient(180deg, rgba(11, 18, 32, 0.94) 0%, rgba(4, 7, 13, 0.98) 100%) !important;
        background-color: #04070d !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-left: 3.5px solid #38bdf8 !important;
        border-radius: 18px !important;
        padding: 26px 26px !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.62) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-faq-list {
        display: flex !important;
        flex-direction: column !important;
        gap: 20px !important;
        max-width: 980px !important;
        margin: 0 auto !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-faq-item {
        background: linear-gradient(180deg, rgba(12, 20, 36, 0.92) 0%, rgba(4, 7, 13, 0.97) 100%) !important;
        background-color: #04070d !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        border-radius: 18px !important;
        padding: 26px 30px !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.65) !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-faq-q {
        margin: 0 0 10px 0 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.12rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        line-height: 1.38 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-faq-a {
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1.72 !important;
        color: #cbd5e1 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-industry-partners-sandbox {
        border-radius: 18px !important;
        border: 1px solid rgba(212, 175, 55, 0.35) !important;
        background-color: #04070d !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-partner-registry-baseline a {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 8px 18px !important;
        border-radius: 9999px !important;
        background-color: rgba(56, 189, 248, 0.14) !important;
        border: 1px solid rgba(56, 189, 248, 0.52) !important;
        color: #38bdf8 !important;
        -webkit-text-fill-color: #38bdf8 !important;
        text-decoration: none !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
    }
    html body .kp-sovereign-geo-wrapper .kp-bottom-cta-vault {
        margin-top: 56px !important;
        padding: 44px 32px !important;
        border-radius: 18px !important;
        background: radial-gradient(ellipse at 50% 0%, rgba(212, 175, 55, 0.14) 0%, rgba(4, 7, 13, 0.98) 76%) !important;
        background-color: #04070d !important;
        border: 1.5px solid rgba(212, 175, 55, 0.48) !important;
        box-shadow: 0 20px 52px rgba(0, 0, 0, 0.84), 0 0 28px rgba(212, 175, 55, 0.12) !important;
        text-align: center !important;
    }
    @media (max-width: 1024px) {
        html body .kp-sovereign-geo-wrapper .kp-trust-strip {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }
        html body .kp-sovereign-geo-wrapper .kp-pillars-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }
    }
    @media (max-width: 680px) {
        html body .kp-sovereign-geo-wrapper .kp-geo-hero { padding: 44px 16px 36px 16px !important; }
        html body .kp-sovereign-geo-wrapper .kp-geo-container { padding: 0 16px !important; }
        html body .kp-sovereign-geo-wrapper .kp-trust-strip,
        html body .kp-sovereign-geo-wrapper .kp-pillars-grid,
        html body .kp-sovereign-geo-wrapper .kp-subcorridor-grid {
            grid-template-columns: 1fr !important;
        }
        html body .kp-sovereign-geo-wrapper .kp-glass-card,
        html body .kp-sovereign-geo-wrapper .kp-subcorridor-card,
        html body .kp-sovereign-geo-wrapper .kp-faq-item {
            padding: 24px 20px !important;
        }
        html body .kp-sovereign-geo-wrapper .kp-bottom-cta-vault { padding: 32px 20px !important; }
    }
    </style>
    <?php
}

// ── 12. Rule 30 Zero Unlaunched Retainer Price Guard on Content Output ───────
add_filter('the_content', 'keystone_poss_purge_retainer_price_leaks', 9999);
function keystone_poss_purge_retainer_price_leaks(string $content): string {
    if (strpos($content, '5,000') === false) {
        return $content;
    }
    $patterns = array(
        '/Commission\s+a\s+\$5,000\s+Feasibility\s*(?:&amp;|&)\s*Permitting\s+Audit/i',
        '/\$5,000\s+Feasibility\s*(?:&amp;|&)\s*Permitting\s+(?:Audit|Plan|Retainer)/i',
        '/\$5,000\s+(?:Pre-Construction\s+)?Feasibility\s+(?:Audit|Plan|Retainer|Dossier)/i',
    );
    $replacements = array(
        'Commission a Pre-Construction Feasibility &amp; Permitting Plan',
        'Pre-Construction Feasibility &amp; Permitting Plan',
        'Pre-Construction Feasibility &amp; Permitting Plan',
    );
    return (string) preg_replace($patterns, $replacements, $content);
}
