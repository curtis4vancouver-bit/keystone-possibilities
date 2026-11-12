<?php
/**
 * WP Cloud _atomic_bur Edge Cache Optimizer, Unified IndexNow & GEO Static Discovery — v3.0
 *
 * Implements [rule_wpcloud_atomic_edge_cache_and_geo_sync_01]:
 * 1. Strips plugin Set-Cookie headers on anonymous frontend GET/HEAD requests so WP Cloud
 *    Nginx/Batcache returns x-ac: HIT (~90ms TTFB instead of ~900ms BYPASS).
 * 2. Unifies IndexNow key onto `567052ceffa24bb89513f2fd8cc7cfd5` and pings IndexNow on publish.
 * 3. Provides PHP fallback serving for `/llms.txt`, `/llms-full.txt`, and `/567052ceffa24bb89513f2fd8cc7cfd5.txt`.
 * 4. Preserves Rule 30 unlaunched retainer price guard and Verified Industry Partners injector.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

if (!defined('KP_INDEXNOW_KEY')) {
    define('KP_INDEXNOW_KEY', '567052ceffa24bb89513f2fd8cc7cfd5');
}

/**
 * Exposes Rank Math SEO & Keystone v3.0 video metadata fields to authenticated WP REST updates.
 */
function kp_v3_register_rest_post_meta(): void
{
    $auth_cb = static function (): bool {
        return current_user_can('edit_posts');
    };
    $string_keys = array(
        'rank_math_title',
        'rank_math_description',
        'rank_math_focus_keyword',
        'rank_math_canonical_url',
        '_kp_youtube_id',
        '_kp_youtube_short_id',
        '_kp_video_duration_iso',
        '_kp_companion_post_url',
    );
    foreach (array('page', 'post') as $post_type) {
        foreach ($string_keys as $meta_key) {
            register_post_meta($post_type, $meta_key, array(
                'show_in_rest'      => true,
                'single'            => true,
                'type'              => 'string',
                'sanitize_callback' => 'sanitize_text_field',
                'auth_callback'     => $auth_cb,
            ));
        }
        register_post_meta($post_type, '_kp_video_duration_sec', array(
            'show_in_rest'      => true,
            'single'            => true,
            'type'              => 'integer',
            'sanitize_callback' => 'absint',
            'auth_callback'     => $auth_cb,
        ));
        register_post_meta($post_type, 'rank_math_robots', array(
            'show_in_rest'  => array(
                'schema' => array(
                    'type'  => 'array',
                    'items' => array('type' => 'string'),
                ),
            ),
            'single'        => true,
            'type'          => 'array',
            'auth_callback' => $auth_cb,
        ));
    }
}
add_action('init', 'kp_v3_register_rest_post_meta', 5);

/**
 * Determines whether the current HTTP request is an anonymous cacheable public GET/HEAD view.
 *
 * @return bool
 */
function kp_is_anonymous_cacheable_frontend_request(): bool
{
    if (is_admin() || (defined('WP_CLI') && WP_CLI) || (defined('DOING_CRON') && DOING_CRON)) {
        return false;
    }
    if ((defined('DOING_AJAX') && DOING_AJAX) || (defined('REST_REQUEST') && REST_REQUEST)) {
        return false;
    }

    $method = strtoupper((string) ($_SERVER['REQUEST_METHOD'] ?? 'GET'));
    if ($method !== 'GET' && $method !== 'HEAD') {
        return false;
    }

    $uri = strtolower((string) ($_SERVER['REQUEST_URI'] ?? ''));
    if (
        strpos($uri, '/wp-admin') === 0 ||
        strpos($uri, '/wp-login.php') === 0 ||
        strpos($uri, '/wp-json/') === 0 ||
        strpos($uri, 'preview=true') !== false
    ) {
        return false;
    }

    if (function_exists('is_user_logged_in') && is_user_logged_in()) {
        return false;
    }

    foreach ($_COOKIE as $cookie_name => $_val) {
        $cname = strtolower((string) $cookie_name);
        if (
            strpos($cname, 'wordpress_logged_in_') === 0 ||
            strpos($cname, 'wp-postpass_') === 0 ||
            strpos($cname, 'woocommerce_') === 0
        ) {
            return false;
        }
    }

    return true;
}

/**
 * Strips plugin Set-Cookie headers and emits public edge-cache headers on anonymous GET/HEAD views.
 */
function kp_enforce_wpcloud_atomic_edge_cache_headers(): void
{
    if (headers_sent() || !kp_is_anonymous_cacheable_frontend_request()) {
        return;
    }

    if (function_exists('is_page') && is_page('client-login')) {
        // Keep Client Portal page personalized / non-cached if needed, or strip third-party tracking cookies only
        header_remove('Set-Cookie');
        return;
    }

    if (function_exists('is_404') && is_404()) {
        return;
    }

    header_remove('Set-Cookie');
    header('Cache-Control: public, max-age=300, s-maxage=86400, stale-while-revalidate=3600', true);
}
add_action('send_headers', 'kp_enforce_wpcloud_atomic_edge_cache_headers', 9999);
add_action('template_redirect', 'kp_enforce_wpcloud_atomic_edge_cache_headers', 9999);

/**
 * Final header scrub right before response body flush in case late plugins emit Set-Cookie in wp_head/wp_footer.
 */
function kp_start_anonymous_cookie_scrub_buffer(): void
{
    if (!kp_is_anonymous_cacheable_frontend_request()) {
        return;
    }
    ob_start(static function (string $buffer): string {
        if (!headers_sent()) {
            header_remove('Set-Cookie');
        }
        return $buffer;
    });
}
add_action('template_redirect', 'kp_start_anonymous_cookie_scrub_buffer', 0);

/**
 * Serves /llms.txt, /llms-full.txt, and /567052ceffa24bb89513f2fd8cc7cfd5.txt cleanly if Nginx passes through to PHP.
 */
function kp_serve_geo_discovery_endpoints(): void
{
    if (is_admin()) {
        return;
    }

    if (isset($_GET['keystone_ls_purge'])) {
        if (function_exists('do_action')) {
            do_action('litespeed_purge_all');
        }
        if (function_exists('kp_v3_flush_edge_cache')) {
            kp_v3_flush_edge_cache();
        } elseif (function_exists('wp_cache_flush')) {
            wp_cache_flush();
        }
        if (class_exists('\\RankMath\\Sitemap\\Cache')) {
            \RankMath\Sitemap\Cache::invalidate_storage();
        }
        if (function_exists('flush_rewrite_rules')) {
            flush_rewrite_rules(false);
        }
        if (!headers_sent()) {
            status_header(200);
            header_remove('Set-Cookie');
            header('Content-Type: text/plain; charset=utf-8', true);
            header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0', true);
            header('X-LiteSpeed-Purge: *', true);
        }
        echo 'KEYSTONE_POSSIBILITIES_V3_EDGE_CACHE_PURGED';
        exit;
    }

    $uri  = (string) ($_SERVER['REQUEST_URI'] ?? '');
    $path = '/' . trim((string) parse_url($uri, PHP_URL_PATH), '/');

    if ($path === '/' . KP_INDEXNOW_KEY . '.txt') {
        if (!headers_sent()) {
            status_header(200);
            header_remove('Set-Cookie');
            header('Content-Type: text/plain; charset=utf-8', true);
            header('Cache-Control: public, max-age=86400, s-maxage=604800', true);
            header('X-Robots-Tag: noindex', true);
        }
        echo KP_INDEXNOW_KEY;
        exit;
    }

    if ($path === '/llms.txt' || $path === '/llms-full.txt') {
        $filename  = ltrim($path, '/');
        $theme_f   = trailingslashit(get_stylesheet_directory()) . $filename;
        $docroot_f = !empty($_SERVER['DOCUMENT_ROOT']) ? rtrim((string) $_SERVER['DOCUMENT_ROOT'], '/\\') . '/' . $filename : '';

        $source = '';
        if ($docroot_f !== '' && is_readable($docroot_f)) {
            $source = (string) file_get_contents($docroot_f);
        }
        if ($source === '' && is_readable($theme_f)) {
            $source = (string) file_get_contents($theme_f);
        }

        if ($source !== '') {
            if (!headers_sent()) {
                status_header(200);
                header_remove('Set-Cookie');
                header('Content-Type: text/plain; charset=utf-8', true);
                header('Cache-Control: public, max-age=3600, s-maxage=86400', true);
                header('X-Robots-Tag: index, follow', true);
            }
            echo $source;
            exit;
        }
    }
}
add_action('init', 'kp_serve_geo_discovery_endpoints', 1);

/**
 * Pings IndexNow (Bing, Yandex, Naver, Seznam) upon publishing or updating public pages/posts.
 *
 * @param string  $new_status New post status.
 * @param string  $old_status Previous post status.
 * @param WP_Post $post       Post object.
 */
function kp_ping_indexnow_on_publish(string $new_status, string $old_status, WP_Post $post): void
{
    if ($new_status !== 'publish' || !in_array($post->post_type, array('page', 'post'), true)) {
        return;
    }
    if (wp_is_post_revision($post->ID) || wp_is_post_autosave($post->ID)) {
        return;
    }

    $permalink = get_permalink($post->ID);
    if (!$permalink || strpos($permalink, 'keystonepossibilities.ca') === false) {
        return;
    }

    $throttle_key = 'kp_idxnow_' . $post->ID;
    if (get_transient($throttle_key)) {
        return;
    }
    set_transient($throttle_key, 1, 5 * MINUTE_IN_SECONDS);

    $payload = array(
        'host'        => 'keystonepossibilities.ca',
        'key'         => KP_INDEXNOW_KEY,
        'keyLocation' => 'https://keystonepossibilities.ca/' . KP_INDEXNOW_KEY . '.txt',
        'urlList'     => array($permalink),
    );

    wp_remote_post('https://api.indexnow.org/indexnow', array(
        'timeout'  => 3,
        'blocking' => false,
        'headers'  => array('Content-Type' => 'application/json; charset=utf-8'),
        'body'     => (string) wp_json_encode($payload, JSON_UNESCAPED_SLASHES),
    ));
}
add_action('transition_post_status', 'kp_ping_indexnow_on_publish', 20, 3);

/**
 * Rule 30 Guard: Purges any legacy unlaunched retainer price strings from database post content.
 *
 * @param string $content Post content HTML.
 * @return string
 */
function keystone_poss_purge_retainer_price_leaks(string $content): string
{
    if (strpos($content, '5,000') === false) {
        return $content;
    }
    $patterns = array(
        '/Commission\s+a\s+\$[0-9]{1,2},000\s+Feasibility\s*(?:&amp;|&)\s*Permitting\s+Audit/i',
        '/\$[0-9]{1,2},000\s+Feasibility\s*(?:&amp;|&)\s*Permitting\s+(?:Audit|Plan|Retainer)/i',
        '/\$[0-9]{1,2},000\s+(?:Pre-Construction\s+)?Feasibility\s+(?:Audit|Plan|Retainer|Dossier)/i',
    );
    $replacements = array(
        'Commission a Pre-Construction Feasibility &amp; Permitting Plan',
        'Pre-Construction Feasibility &amp; Permitting Plan',
        'Pre-Construction Feasibility &amp; Permitting Plan',
    );
    return (string) preg_replace($patterns, $replacements, $content);
}
add_filter('the_content', 'keystone_poss_purge_retainer_price_leaks', 9999);

/**
 * Verified BC Engineering, Architectural & Industry Directory Partners Registry for /industry-partners/.
 *
 * @return array<int, array<string, string>>
 */
function keystone_poss_get_verified_industry_partners(): array
{
    return array(
        array(
            'domain'          => 'fastepp.com',
            'name'            => 'Fast + Epp Structural Engineers',
            'url'             => 'https://www.fastepp.com/',
            'category_badge'  => 'EGBC Structural & Mass Timber Engineering',
            'corridor_region' => 'Vancouver · Sea-to-Sky · Whistler · Worldwide',
            'summary'         => 'Internationally recognized Vancouver structural engineering practice specializing in hybrid mass-timber, alpine high-snow-load cantilevers, and performance-based seismic design across British Columbia.',
        ),
        array(
            'domain'          => 'glotmansimpson.com',
            'name'            => 'Glotman Simpson Consulting Engineers',
            'url'             => 'https://glotmansimpson.com/',
            'category_badge'  => 'EGBC Structural & Seismic Engineering',
            'corridor_region' => 'Vancouver · West Vancouver · North Shore · Whistler',
            'summary'         => 'Leading British Columbia structural consulting engineering firm delivering deep seismic lateral-load engineering, reinforced concrete podiums, and complex hillside custom residential structures.',
        ),
        array(
            'domain'          => 'thurber.ca',
            'name'            => 'Thurber Engineering Ltd.',
            'url'             => 'https://www.thurber.ca/',
            'category_badge'  => 'Geotechnical, Rock Mechanics & Slope Stability',
            'corridor_region' => 'Vancouver · Squamish · Whistler · Vancouver Island',
            'summary'         => 'Premier Canadian geotechnical, environmental, and materials engineering consultancy providing bedrock anchor design, steep-slope hazard assessments, and micropile foundation engineering.',
        ),
        array(
            'domain'          => 'lewkowich.com',
            'name'            => 'Lewkowich Engineering Associates Ltd.',
            'url'             => 'https://www.lewkowich.com/',
            'category_badge'  => 'Vancouver Island Geotechnical & Hydrogeological Engineering',
            'corridor_region' => 'Nanaimo · Victoria · Tofino · Comox Valley · Vancouver Island',
            'summary'         => 'Dedicated Vancouver Island geotechnical and materials engineering specialists supporting coastal bluff stability, seismic site classification, and engineered civil subgrades.',
        ),
        array(
            'domain'          => 'measured.ca',
            'name'            => 'Measured Architecture Inc.',
            'url'             => 'https://measured.ca/',
            'category_badge'  => 'AIBC Contemporary Pacific Northwest Architecture',
            'corridor_region' => 'Vancouver · West Vancouver · Whistler · Gulf Islands',
            'summary'         => 'Award-winning Vancouver architectural practice celebrated for quiet-luxury concrete, steel, and timber residences engineered for multi-generational coastal and mountain performance.',
        ),
        array(
            'domain'          => 'vrba.ca',
            'name'            => 'Victoria Residential Builders Association (VRBA)',
            'url'             => 'https://www.vrba.ca/',
            'category_badge'  => 'Accredited BC Residential Construction Association',
            'corridor_region' => 'Victoria · Oak Bay · Saanich · Southern Vancouver Island',
            'summary'         => 'Professional residential construction association advancing BC Building Code Step Code compliance, builder consumer protection, and housing policy across Southern Vancouver Island.',
        ),
    );
}

/**
 * Injects partner showcase cards into legacy /industry-partners/ content markers when present.
 *
 * @param string $content Post content HTML.
 * @return string
 */
function keystone_poss_inject_featured_industry_partners(string $content): string
{
    if (strpos($content, 'KEYSTONE_PARTNER_CARDS_CONTAINER_END') === false) {
        return $content;
    }
    if (strpos($content, 'data-partner-domain="fastepp.com"') !== false) {
        return $content;
    }

    $cards = array();
    foreach (keystone_poss_get_verified_industry_partners() as $p) {
        $cards[] = '<article class="kp-card" data-partner-domain="' . esc_attr($p['domain']) . '" style="margin-bottom:18px;border-left:3px solid #d4af37;">'
            . '<div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;margin-bottom:8px;">'
            . '<span class="kp-pill-tech">' . esc_html($p['category_badge']) . '</span>'
            . '<span style="font-family:var(--font-mono);font-size:0.72rem;color:#f3d98b;">' . esc_html($p['corridor_region']) . '</span>'
            . '</div>'
            . '<h3 style="margin:0 0 8px;color:#f8fafc;font-size:1.15rem;">' . esc_html($p['name']) . '</h3>'
            . '<p style="margin:0 0 14px;color:#cbd5e1;font-size:0.92rem;">' . esc_html($p['summary']) . '</p>'
            . '<a href="' . esc_url($p['url']) . '" target="_blank" rel="noopener" class="kp-btn-outline" style="min-height:38px;padding:7px 16px;font-size:0.78rem;">Visit ' . esc_html($p['domain']) . ' &rarr;</a>'
            . '</article>';
    }

    return str_replace(
        '<!-- KEYSTONE_PARTNER_CARDS_CONTAINER_END -->',
        implode("\n", $cards) . "\n<!-- KEYSTONE_PARTNER_CARDS_CONTAINER_END -->",
        $content
    );
}
add_filter('the_content', 'keystone_poss_inject_featured_industry_partners', 20);

// Keep atomic v3.0 theme sync API loaded during staged deployment before functions.php is updated last.
if (file_exists(__DIR__ . '/project-sync-api.php')) {
    require_once __DIR__ . '/project-sync-api.php';
}
