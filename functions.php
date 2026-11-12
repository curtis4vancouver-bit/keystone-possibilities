<?php
/**
 * Keystone Possibilities Sovereign Child Theme v3.0 — Core Bootstrap (`astra-child`)
 *
 * Clean modular architecture (ZERO inline <head> CSS bloat):
 * - Disables Astra default header/footer in favor of custom `header.php` & `footer.php`
 * - Loads v3.0 data registries (`inc/data-portfolio-credentials.php`, `inc/data-corridors.php`)
 * - Enqueues cacheable filemtime()-versioned CSS/JS (`inc/enqueue.php`)
 * - Enforces single-hop 301 redirects & HTTP 410 Gone de-indexing (`inc/redirects-410.php`)
 * - Emits unified @graph JSON-LD schema & VideoObject/OG:Video (`inc/seo-schema.php`)
 * - Powers `/llms.txt`, `/llms-full.txt`, IndexNow & Batcache surgical flush (`inc/geo-cache-indexnow.php`)
 * - Hardens Client Portal v10 API (`inc/portal-api-v10.php`) & atomic theme sync (`inc/project-sync-api.php`)
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

define('KEYSTONE_POSSIBILITIES_THEME_VERSION', '3.0.0');

// ── 1. Sovereign Child Theme Setup & Astra Chrome Suppression ────────────────
add_action('after_setup_theme', 'kp_v3_setup_child_theme', 20);
function kp_v3_setup_child_theme(): void
{
    remove_all_actions('astra_header');
    remove_all_actions('astra_footer');

    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
    ));

    register_nav_menus(array(
        'primary' => 'Keystone Primary Sovereign Navigation',
        'footer'  => 'Keystone Footer Corridor & Hub Links',
    ));
}

add_filter('astra_the_title_enabled', '__return_false');
add_filter('astra_featured_image_enabled', '__return_false');
add_filter('astra_page_layout', static function (): string {
    return 'no-sidebar';
});
add_filter('astra_get_content_layout', static function (): string {
    return 'page-builder';
});

// ── 2. Load Modular `inc/` Subsystems ────────────────────────────────────────
$kp_inc_modules = array(
    'inc/data-portfolio-credentials.php',
    'inc/data-corridors.php',
    'inc/enqueue.php',
    'inc/redirects-410.php',
    'inc/seo-schema.php',
    'inc/geo-cache-indexnow.php',
    'inc/video-sitemap-engine.php',
    'inc/founder-avatar-video-card.php',
    'inc/bill44-estimator.php',
    'inc/lead-capture.php',
    'inc/portal-api-v10.php',
    'inc/project-sync-api.php',
    'inc/portfolio-residences.php',
    'inc/client-portal-demo.php',
);

foreach ($kp_inc_modules as $kp_rel_module) {
    $kp_abs_module = trailingslashit(get_stylesheet_directory()) . $kp_rel_module;
    if (file_exists($kp_abs_module)) {
        require_once $kp_abs_module;
    }
}

// ── 3. Rank Math Sitemap Sanitizer, Cache Bypass & Broken Video Suppression ──
add_filter('rank_math/sitemap/enable_caching', '__return_false');
add_filter('rank_math/snippet/rich_snippet_video', '__return_false');
add_filter('rank_math/schema/video', '__return_false');
add_filter('rank_math/sitemap/entry', 'keystone_possibilities_sanitize_rank_math_sitemap', 10, 3);

/**
 * Scrubs non-canonical, draft, noindex, off-vertical, and redirected URLs from Rank Math XML sitemaps.
 *
 * @param array<string, mixed>|false $url    Sitemap entry array.
 * @param string                     $type   Object type (`post`, `term`, `user`).
 * @param mixed                      $object Backing WP_Post / WP_Term / WP_User.
 * @return array<string, mixed>|false
 */
function keystone_possibilities_sanitize_rank_math_sitemap($url, $type, $object)
{
    if (empty($url) || !is_array($url) || empty($url['loc'])) {
        return false;
    }

    $loc = (string) $url['loc'];

    $excluded_patterns = array(
        'sample-page',
        '/test/',
        '/demo/',
        'wp-admin',
        '.html',
        'cjc-1295-ipamorelin-glp-1-fatigue',
        'mounjaro-muscle-loss',
        'retatrutide-phase-3-data',
        'wolverine-stack',
        'glp-1',
        'peptide',
        'keystone_recomposition',
        '/tag/',
        '/author/',
        '/date/',
        '/watch-',
        '/client-login',
        '/client-portal',
        '/west-vancouver-luxury-renovations',
        '/north-vancouver-multiplex-conversions',
        '/project-management-wp',
        '/feasibility-retainer',
        '/services-general-contractor-squamish',
    );

    foreach ($excluded_patterns as $pattern) {
        if (stripos($loc, $pattern) !== false) {
            return false;
        }
    }

    if (in_array((string) $type, array('term', 'author', 'user'), true)) {
        return false;
    }

    if (is_object($object) && isset($object->ID)) {
        $post_id = (int) $object->ID;
        if (isset($object->post_status) && $object->post_status !== 'publish') {
            return false;
        }
        $robots = get_post_meta($post_id, 'rank_math_robots', true);
        if (is_array($robots) && in_array('noindex', $robots, true)) {
            return false;
        }
        if (is_string($robots) && stripos($robots, 'noindex') !== false) {
            return false;
        }
    }

    return $url;
}

// ── 4. Dynamic Robots Noindex on Thin Archives & 404s ────────────────────────
add_action('wp_head', 'keystone_possibilities_noindex_thin_archives', 2);
function keystone_possibilities_noindex_thin_archives(): void
{
    if (is_tag() || is_date() || is_author() || is_search() || is_404()) {
        echo '<meta name="robots" content="noindex, follow" />' . "\n";
    }
}

// ── 5. Canonical 301 Redirect & HTTP 410 Gone Dispatcher ─────────────────────
add_action('template_redirect', 'keystone_possibilities_dispatch_redirects_and_410', 1);
function keystone_possibilities_dispatch_redirects_and_410(): void
{
    if (function_exists('kp_execute_redirects_and_410')) {
        kp_execute_redirects_and_410();
        return;
    }

    $uri  = $_SERVER['REQUEST_URI'] ?? '';
    $path = strtolower((string) strtok($uri, '?'));
    $fallback_301 = array(
        '/about-us-general-contractor-squamish.html' => '/about-us-general-contractor-squamish/',
        '/west-vancouver-custom-homes.html'          => '/west-vancouver-custom-homes/',
    );
    if (isset($fallback_301[$path])) {
        wp_redirect(home_url($fallback_301[$path]), 301);
        exit;
    }
    if ($path === '/sample-page' || $path === '/sample-page/') {
        status_header(410);
        nocache_headers();
        exit;
    }
}

// ── 6. Privacy-Enhanced Click-to-Play [keystone_video] Shortcode & JS Defer ──
add_shortcode('keystone_video', 'keystone_possibilities_video_shortcode');
function keystone_possibilities_video_shortcode($atts = array()): string
{
    $args = shortcode_atts(array(
        'id'    => '',
        'title' => 'Keystone Possibilities Engineering Briefing',
        'start' => '0',
    ), is_array($atts) ? $atts : array(), 'keystone_video');

    $vid = preg_replace('/[^A-Za-z0-9_-]/', '', (string) $args['id']);
    if ($vid === '' || strlen($vid) !== 11) {
        return '';
    }

    wp_enqueue_script('keystone-lazy-player');
    $poster = 'https://i.ytimg.com/vi/' . $vid . '/maxresdefault.jpg';

    return sprintf(
        '<div class="kp-cinema-stage" data-kp-yt-facade="%1$s" data-kp-yt-title="%2$s" data-kp-yt-start="%3$d" role="button" tabindex="0" aria-label="Play video: %2$s">'
        . '<img src="%4$s" alt="%2$s" loading="lazy" decoding="async">'
        . '<span class="kp-cinema-play-btn" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>'
        . '</div>',
        esc_attr($vid),
        esc_attr((string) $args['title']),
        (int) $args['start'],
        esc_url($poster)
    );
}

add_filter('script_loader_tag', 'keystone_possibilities_defer_theme_scripts', 10, 2);
function keystone_possibilities_defer_theme_scripts(string $tag, string $handle): string
{
    $deferred_handles = array(
        'keystone-lazy-player',
        'keystone-portfolio-carousel',
        'kp-navigation-ui',
        'kp-estimator-calc',
        'kp-lead-form',
    );
    if (in_array($handle, $deferred_handles, true) && stripos($tag, ' defer') === false) {
        return str_replace(' src=', ' defer src=', $tag);
    }
    return $tag;
}

// ── 7. Legacy Post Content Inline-CSS Sanitizer (Regression Guard) ───────────
add_filter('the_content', 'keystone_possibilities_sanitize_content_output', 9);
function keystone_possibilities_sanitize_content_output(string $content): string
{
    if ($content === '' || (stripos($content, 'kp-regional-grid') === false && stripos($content, '<style') === false)) {
        return $content;
    }

    $patterns = array(
        '/<style\b[^>]*>[\s\S]*?<\/style>/i',
        '/(<p>\s*)?\.kp-regional-grid\s*(?:>|&gt;)\s*p\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-regional-grid\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-glass:empty\s*\{[^}]*\}\s*(<\/p>)?/i',
    );

    return (string) preg_replace($patterns, '', $content);
}
