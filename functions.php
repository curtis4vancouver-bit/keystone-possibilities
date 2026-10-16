<?php
/**
 * Keystone Possibilities Child Theme Functions
 * Certified BC Builder #52603 — Authority, SEO & GEO Schema Engine
 * 
 * @package KeystonePossibilitiesChild
 * @version 2.5.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// ── 1. Enqueue Parent, Child Stylesheets & Media Facade Engine ──────────────
add_action('wp_enqueue_scripts', 'keystone_possibilities_enqueue_styles', 15);
function keystone_possibilities_enqueue_styles() {
    wp_enqueue_style('astra-parent-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('keystone-possibilities-style', get_stylesheet_uri(), array('astra-parent-style'), '2.6.0');
    wp_enqueue_script('keystone-lazy-player', get_stylesheet_directory_uri() . '/js/lazy-player.js', array(), '2.6.0', true);
    wp_enqueue_script('keystone-portfolio-carousel', get_stylesheet_directory_uri() . '/js/portfolio-carousel.js', array(), '2.6.0', true);

    // Pass REST and AJAX endpoints to frontend for interactive lead capture & multi-job portal
    wp_localize_script('keystone-lazy-player', 'keystoneData', array(
        'ajaxUrl'           => admin_url('admin-ajax.php'),
        'restUrl'           => esc_url_raw(rest_url('keystone/v1/lead')),
        'portalJobsRestUrl' => esc_url_raw(rest_url('keystone/v1/portal-jobs')),
    ));
}

// Apply defer attribute to scripts for 100/100 Mobile PageSpeed
add_filter('script_loader_tag', 'keystone_possibilities_add_defer_attribute', 10, 2);
function keystone_possibilities_add_defer_attribute($tag, $handle) {
    if ('keystone-lazy-player' === $handle || 'keystone-portfolio-carousel' === $handle) {
        return str_replace(' src', ' defer="defer" src', $tag);
    }
    return $tag;
}

// ── 2. Require Master JSON-LD Schema, Portfolio & Lead Capture Engines ──────
require_once __DIR__ . '/inc/seo-schema.php';
// Prevent duplicate empire bar output from seo-schema.php (retains clean integrated blue mesh bar)
remove_action('wp_footer', 'keystone_possibilities_render_empire_footer', 30);
if (file_exists(__DIR__ . '/inc/portfolio-residences.php')) {
    require_once __DIR__ . '/inc/portfolio-residences.php';
}
require_once __DIR__ . '/inc/lead-capture.php';
require_once __DIR__ . '/inc/bill44-estimator.php';
require_once __DIR__ . '/inc/client-portal-demo.php';
if (file_exists(__DIR__ . '/inc/multi-job-portal-api.php')) {
    require_once __DIR__ . '/inc/multi-job-portal-api.php';
}

// ── 3. WebP Video Facade Player Shortcode ([keystone_video]) ─────────────────
add_shortcode('keystone_video', 'keystone_possibilities_lazy_video_shortcode');
function keystone_possibilities_lazy_video_shortcode($atts) {
    $args = shortcode_atts(array(
        'id'   => '',
        'type' => 'youtube',
        'placeholder_img' => '',
    ), $atts);

    if (empty($args['id'])) {
        return '<p style="color: #FC8181; font-family: monospace;">[Error] Media Asset ID is missing.</p>';
    }

    $media_id   = esc_attr($args['id']);
    $media_type = esc_attr(strtolower($args['type']));
    
    $bg_img = '';
    if (!empty($args['placeholder_img'])) {
        $bg_img = esc_url($args['placeholder_img']);
    } else {
        $bg_img = 'https://i.ytimg.com/vi_webp/' . $media_id . '/maxresdefault.webp';
    }

    ob_start();
    ?>
    <div class="luxury-video-facade keystone-lazy-video-container" 
         data-video-id="<?php echo $media_id; ?>" 
         data-video-type="<?php echo $media_type; ?>" 
         role="region" 
         aria-label="Video Player Placeholder">
        
        <div class="facade-background" style="background-image: url('<?php echo $bg_img; ?>');"></div>
        <div class="facade-overlay"></div>
        
        <button class="play-button keystone-play-button" aria-label="Play Construction Overview Video">
            <svg class="play-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
            </svg>
        </button>
        <noscript>
            <iframe src="https://www.youtube.com/embed/<?php echo $media_id; ?>?rel=0" width="100%" height="100%" style="position: absolute; top: 0; left: 0;" frameborder="0" allowfullscreen></iframe>
        </noscript>
    </div>
    <?php
    return ob_get_clean();
}

// ── 4. Rank Math XML Sitemap Sanitizer & Cache Bypass ────────────────────────

// Tier 1: Natively exclude 'category', 'post_tag', and 'post_format' taxonomies from Rank Math sitemap generation
add_filter('rank_math/sitemap/exclude_taxonomy', function (bool $exclude, string $type): bool {
    if (in_array($type, array('category', 'post_tag', 'post_format'), true)) {
        return true;
    }
    return $exclude;
}, 10, 2);

// Enforce strict exclusion of empty terms across all remaining taxonomies
add_filter('rank_math/sitemap/exclude_empty_terms', '__return_true');

// Disable Rank Math KML / Locations sitemap to prevent redirecting locations.kml in sitemaps
add_filter('rank_math/sitemap/locations', '__return_empty_string');
add_filter('rank_math/sitemap/locations/data', '__return_empty_array');

// Tier 2: Guardrail - Strip category-sitemap, local-sitemap, and locations-sitemap from sitemap_index.xml XML output
add_filter('rank_math/sitemap/index', function (string $xml): string {
    $pattern = '/<sitemap>\s*<loc>[^<]*(?:category-sitemap\.xml|local-sitemap\.xml|locations-sitemap\.xml|locations\.kml)<\/loc>.*?<\/sitemap>\s*/is';
    $cleaned = preg_replace($pattern, '', $xml);
    return is_string($cleaned) ? $cleaned : $xml;
}, 11);

// Tier 3: Intercept direct requests to category-sitemap.xml and return HTTP 410 Gone
add_action('template_redirect', function (): void {
    $request_uri = $_SERVER['REQUEST_URI'] ?? '';
    if (preg_match('#/category-sitemap(?:[0-9]+)?\.xml(\.gz)?$#i', (string) $request_uri) === 1) {
        status_header(410);
        nocache_headers();
        header('Content-Type: text/plain; charset=utf-8');
        header('X-Robots-Tag: noindex, nofollow');
        echo '410 Gone: category-sitemap.xml has been intentionally retired and removed from sitemap_index.xml.';
        exit;
    }
}, 0);

add_filter('rank_math/sitemap/entry', 'keystone_possibilities_sanitize_rank_math_sitemap', 10, 3);
function keystone_possibilities_sanitize_rank_math_sitemap($url, $type, $object) {
    if (empty($url) || !is_array($url) || empty($url['loc'])) {
        return false;
    }

    $loc = $url['loc'];

    // 1. Exclude legacy redirected paths, test URLs, locations.kml, and .html extensions
    // Note: /pemberton-luxury-builder/ and /bc-hydro-registered-civil-contractor/ are canonical 200 OK pages and MUST remain indexed
    $excluded_patterns = array(
        'sample-page',
        '/test/',
        '/demo/',
        'wp-admin',
        'wp-login',
        'locations.kml',
        'about-us-general-contractor-squamish.html',
        'squamish-custom-home-builder',
        'squamish-general-contractor',
        'west-vancouver-luxury-builder',
        'whistler-luxury-home-builder',
        'whistler-luxury-builder',
        'north-vancouver-home-builder',
        'feasibility-study',
        'cjc-1295-ipamorelin-glp-1-fatigue',
        'mounjaro-muscle-loss',
        'retatrutide-phase-3-data',
        'wolverine-stack',
        'glp-1',
        'peptide',
        'the-journey',
        'keystone_recomposition',
        '52603',
        '/tag/',
        '/author/',
        '/date/',
        '.html' // Force clean directory URLs in XML sitemaps
    );

    foreach ($excluded_patterns as $pat) {
        if (stripos($loc, $pat) !== false) {
            return false; // Strips from XML sitemap
        }
    }

    // Filter pure date archives (e.g. /2026/ or /2026/05/)
    if (preg_match('~^https?://[^/]+/\d{4}/(?:\d{2}/)?$~i', $loc)) {
        return false;
    }

    // Boundary-aware check for standalone test and demo slugs
    $url_path = parse_url($loc, PHP_URL_PATH) ?? '';
    if (preg_match('#/(test|demo)(/|$|\.php|\.html)#i', $url_path)) {
        return false;
    }

    // 2. Drop taxonomy archives, authors, and users from sitemaps if thin
    if (in_array($type, array('term', 'author', 'user'), true)) {
        return false;
    }

    // 3. Inspect Post object for noindex robots meta & publish status
    if (is_object($object) && isset($object->ID)) {
        $robots = get_post_meta($object->ID, 'rank_math_robots', true);
        if (is_array($robots) && in_array('noindex', $robots, true)) {
            return false;
        }
        if (is_string($robots) && stripos($robots, 'noindex') !== false) {
            return false;
        }
        if (get_post_status($object->ID) !== 'publish') {
            return false;
        }
    }

    // 4. Inspect Term object for noindex robots meta
    if ($type === 'term' && is_object($object) && isset($object->term_id)) {
        $term_robots = get_term_meta($object->term_id, 'rank_math_robots', true);
        if (is_array($term_robots) && in_array('noindex', $term_robots, true)) {
            return false;
        }
    }

    return $url;
}

// Disable sitemap caching for instant updates
add_filter('rank_math/sitemap/enable_caching', '__return_false');

// Dynamic Robots Noindex for Thin Archives (Resolves 37 Crawled - Not Indexed GSC notices)
add_filter('rank_math/frontend/robots', function (array $robots): array {
    if (is_tag() || is_category() || is_date() || is_author() || is_search() || is_paged() || is_404()) {
        $robots['index']  = 'noindex';
        $robots['follow'] = 'follow';
        unset($robots['noindex']);
    }
    return $robots;
}, 10, 1);

add_action('wp_head', function () {
    if (is_tag() || is_date() || is_author() || is_search() || is_404() || is_category() || is_paged()) {
        echo '<meta name="robots" content="noindex, follow" />' . "\n";
    }
}, 1);

// Suppress corrupt auto-detected Video Schema (Fix maxresdefau 11-char bug)
add_filter('rank_math/snippet/rich_snippet_video', '__return_empty_array');
add_filter('rank_math/schema/video', '__return_empty_array');

// ── 4.5. 301 Redirect, /llms.txt & 410 Handler ──────────────────────────────
add_action('template_redirect', 'keystone_possibilities_handle_301_410_redirects', 1);
function keystone_possibilities_handle_301_410_redirects() {
    // 1. Strip Jetpack/social ?share= and ?nb= query parameters via 301 to canonical URL
    if (isset($_GET['share'])) {
        wp_safe_redirect(remove_query_arg(array('share', 'nb')), 301);
        exit;
    }

    // 2. Redirect RSS/Atom feeds with noindex header to canonical custom homes hub
    if (is_feed()) {
        header('X-Robots-Tag: noindex, follow', true);
        wp_safe_redirect(home_url('/keystone-possibilities-custom-homes/'), 301);
        exit;
    }

    $uri = (string) ( $_SERVER['REQUEST_URI'] ?? '' );
    $path = (string) strtok($uri, '?');
    
    // Serve /llms.txt dynamically for AI search engines (Perplexity, ChatGPT, Claude)
    if ($path === '/llms.txt' || $path === 'llms.txt') {
        $llms_file = get_stylesheet_directory() . '/llms.txt';
        if (file_exists($llms_file)) {
            status_header(200);
            header('Content-Type: text/plain; charset=utf-8');
            header('X-Robots-Tag: all');
            readfile($llms_file);
            exit;
        }
    }

    // Prefix match for any /2026/03/02/the-2026-structural-reset* variants
    if (stripos($path, '/2026/03/02/the-2026-structural-reset') === 0 || stripos($path, '/2026/03/02/squamish-structural-reset') === 0) {
        wp_safe_redirect(home_url('/2026/09/05/why-4-storey-multiplexes-snap-holdowns/'), 301);
        exit;
    }

    // Strict 301 redirects mapping all legacy/variant slugs to verified 200 OK live URLs
    $redirects_301 = array(
        '/about-us-general-contractor-squamish.html' => '/about-us-general-contractor-squamish/',
        '/about-us-general-contractor-squamish' => '/about-us-general-contractor-squamish/',
        
        // Squamish
        '/squamish-custom-home-builder.html' => '/squamish-custom-homes/',
        '/squamish-custom-home-builder/' => '/squamish-custom-homes/',
        '/squamish-custom-home-builder' => '/squamish-custom-homes/',
        '/squamish-general-contractor/' => '/squamish-custom-homes/',
        '/squamish-general-contractor' => '/squamish-custom-homes/',
        '/squamish-sauna/' => '/squamish-custom-homes/',
        '/squamish-sauna' => '/squamish-custom-homes/',
        '/project-management/squamish_custom_homes/' => '/squamish-custom-homes/',
        '/project-management/squamish_custom_homes' => '/squamish-custom-homes/',
        
        // Whistler
        '/whistler-luxury-builder.html' => '/whistler-custom-homes/',
        '/whistler-luxury-builder/' => '/whistler-custom-homes/',
        '/whistler-luxury-builder' => '/whistler-custom-homes/',
        '/whistler-luxury-home-builder/' => '/whistler-custom-homes/',
        '/whistler-luxury-home-builder' => '/whistler-custom-homes/',
        '/whistler-sauna/' => '/whistler-custom-homes/',
        '/whistler-sauna' => '/whistler-custom-homes/',
        
        // West Vancouver
        '/west-vancouver-custom-homes.html' => '/west-vancouver-custom-homes/',
        '/west-vancouver-luxury-renovations.html' => '/west-vancouver-luxury-renovations/',
        '/west-vancouver-luxury-builder/' => '/west-vancouver-custom-homes/',
        '/west-vancouver-luxury-builder' => '/west-vancouver-custom-homes/',
        '/west-vancouver-sauna/' => '/west-vancouver-custom-homes/',
        '/west-vancouver-sauna' => '/west-vancouver-custom-homes/',
        '/west_vancouver-sauna/' => '/west-vancouver-custom-homes/',
        '/west_vancouver-sauna' => '/west-vancouver-custom-homes/',
        
        // North Vancouver
        '/north-vancouver-home-builder/' => '/north-vancouver-custom-homes/',
        '/north-vancouver-home-builder' => '/north-vancouver-custom-homes/',
        '/north-vancouver-sauna/' => '/north-vancouver-custom-homes/',
        '/north-vancouver-sauna' => '/north-vancouver-custom-homes/',
        '/north_vancouver-sauna/' => '/north-vancouver-custom-homes/',
        '/north_vancouver-sauna' => '/north-vancouver-custom-homes/',

        // Sunshine Coast / Portfolio
        '/sunshine-coast-sauna/' => '/sunshine-coast-custom-homes/',
        '/sunshine-coast-sauna' => '/sunshine-coast-custom-homes/',
        '/portfolio/' => '/portfolio-general-contractor-squamish/',
        '/portfolio' => '/portfolio-general-contractor-squamish/',
        
        // Feasibility Plan & Consulting
        '/feasibility-study/' => '/feasibility-plan/',
        '/feasibility-study' => '/feasibility-plan/',
        '/consulting/' => '/feasibility-plan/',
        '/consulting' => '/feasibility-plan/',
        '/bill-44-multiplex-feasibility/' => '/feasibility-plan/',
        '/bill-44-multiplex-feasibility' => '/feasibility-plan/',

        // Client Portal & Videos
        '/client-portal-2/' => '/client-portal-demo/',
        '/client-portal-2' => '/client-portal-demo/',
        '/client-portal/' => '/client-portal-demo/',
        '/client-portal' => '/client-portal-demo/',
        '/videos/' => '/keystone-possibilities-custom-homes/',
        '/videos' => '/keystone-possibilities-custom-homes/',
        
        // Unpublished 2026 & Legacy Post Slugs -> Canonical Published 200 OK Engineering Teardowns
        '/2026/05/19/squamish-permit-delays/' => '/2026/06/06/building-fourplex-squamish/',
        '/2026/05/19/squamish-permit-delays' => '/2026/06/06/building-fourplex-squamish/',
        '/2026/04/28/bc-bill-44-multiplex-guide/' => '/feasibility-plan/',
        '/2026/04/28/bc-bill-44-multiplex-guide' => '/feasibility-plan/',
        '/2026/04/12/bc-building-code-updates/' => '/2026/08/31/vancouver-r1-1-step-code-5/',
        '/2026/04/12/bc-building-code-updates' => '/2026/08/31/vancouver-r1-1-step-code-5/',
        '/2026/03/02/the-2026-structural-reset/' => '/2026/09/05/why-4-storey-multiplexes-snap-holdowns/',
        '/2026/03/02/the-2026-structural-reset' => '/2026/09/05/why-4-storey-multiplexes-snap-holdowns/',
        '/2026/03/02/squamish-structural-reset/' => '/2026/09/05/why-4-storey-multiplexes-snap-holdowns/',
        '/2026/03/02/squamish-structural-reset' => '/2026/09/05/why-4-storey-multiplexes-snap-holdowns/',
        '/2025/11/22/plan-spring-build-in-winter/' => '/2026/07/14/mountain-construction-bc/',
        '/2025/11/22/plan-spring-build-in-winter' => '/2026/07/14/mountain-construction-bc/',

        // Articles / Blog
        '/blog/' => '/#articles',
        '/blog' => '/#articles',
        '/articles/' => '/#articles',
        '/articles' => '/#articles',
        
        // Obsolete legacy paths redirected to root
        '/cjc-1295-ipamorelin-glp-1-fatigue.html' => '/',
        '/mounjaro-muscle-loss.html' => '/',
        '/retatrutide-phase-3-data.html' => '/',
        '/wolverine-stack.html' => '/',
    );

    if (isset($redirects_301[$path])) {
        wp_safe_redirect(home_url($redirects_301[$path]), 301);
        exit;
    }

    // 410 Gone for obsolete legacy files/directories
    $gone_paths = array(
        '/keystone_recomposition_/',
        '/logo/',
        '/keystone-recomposition-ltd/',
        '/keystone_recomposition_ltd_invert-removebg-preview/',
        '/the-journey/',
    );

    $normalized_path = '/' . trim((string) $path, '/') . '/';
    if (in_array($normalized_path, $gone_paths, true)) {
        status_header(410);
        nocache_headers();
        echo '410 Gone - Resource permanently removed.';
        exit;
    }
}

// ── 5. Master Luxury Footer & Global Color Harmonization Standard ──────────
// 1. Suppress Astra Default Footer Markup & Duplicate Copyright globally
remove_action('astra_footer', 'astra_footer_markup');
add_filter('astra_footer_copyright_layout', '__return_false');

// 2. Render Unified Master Luxury Footer (with single-render guard)
add_action('wp_footer', 'keystone_possibilities_render_master_luxury_footer', 20);
function keystone_possibilities_render_master_luxury_footer() {
    global $kp_master_footer_rendered;
    if (!empty($kp_master_footer_rendered)) {
        return;
    }
    $kp_master_footer_rendered = true;
    ?>
    <footer id="kp-master-luxury-footer" class="kp-master-luxury-footer" style="background-color: #04070D !important; border-top: 1px solid rgba(212, 175, 55, 0.25); padding: 48px 20px calc(5rem + env(safe-area-inset-bottom, 0px)) 20px; color: #94A3B8; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 0.84rem; text-align: center; position: relative; z-index: 10; width: 100%; box-sizing: border-box; overflow-x: clip;">
        <div style="max-width: 1200px; margin: 0 auto;">
            
            <!-- A. Centered Social Matrix & YouTube Subscribe Directing -->
            <div style="margin-bottom: 24px;">
                <div style="display: flex; justify-content: center; align-items: center; gap: 16px; flex-wrap: wrap; margin-bottom: 18px;">
                    
                    <!-- Facebook Page -->
                    <a href="https://www.facebook.com/profile.php?id=61554185128555" target="_blank" rel="noopener noreferrer" class="kp-social-icon-btn" aria-label="Facebook Page" style="width: 48px; height: 48px; min-width: 48px; min-height: 48px; border-radius: 50%; background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(212, 175, 55, 0.35); color: #f6d365; display: inline-flex; align-items: center; justify-content: center; text-decoration: none !important; transition: all 0.25s ease; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    </a>

                    <!-- Instagram Account -->
                    <a href="https://www.instagram.com/keystonepossibilities" target="_blank" rel="noopener noreferrer" class="kp-social-icon-btn" aria-label="Instagram Account" style="width: 48px; height: 48px; min-width: 48px; min-height: 48px; border-radius: 50%; background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(212, 175, 55, 0.35); color: #f6d365; display: inline-flex; align-items: center; justify-content: center; text-decoration: none !important; transition: all 0.25s ease; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.13-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    </a>

                    <!-- YouTube Official Channel -->
                    <a href="https://www.youtube.com/@KeystonePossibilitiesLtd" target="_blank" rel="noopener noreferrer" class="kp-social-icon-btn" aria-label="YouTube Official Channel" style="width: 48px; height: 48px; min-width: 48px; min-height: 48px; border-radius: 50%; background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(212, 175, 55, 0.35); color: #f6d365; display: inline-flex; align-items: center; justify-content: center; text-decoration: none !important; transition: all 0.25s ease; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    </a>

                    <!-- High-Converting YouTube Channel Subscribe Pill -->
                    <a href="https://www.youtube.com/@KeystonePossibilitiesLtd?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="kp-subscribe-direct-btn" style="display: inline-flex; align-items: center; gap: 9px; min-height: 48px; background: linear-gradient(135deg, rgba(212, 175, 55, 0.18) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1.5px solid #d4af37; padding: 10px 22px; border-radius: 9999px; text-decoration: none !important; color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.22); transition: all 0.25s ease;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="#d4af37" style="filter: drop-shadow(0 0 6px rgba(212, 175, 55, 0.5)); flex-shrink: 0;"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                        <span>SUBSCRIBE &bull; @KeystonePossibilitiesLtd</span>
                    </a>

                </div>
            </div>

            <!-- B. Centered High-End Copyright & Credentials -->
            <div data-nosnippet style="margin-bottom: 32px; line-height: 1.6;">
                <p style="margin: 0 0 6px 0; color: #CBD5E1; font-weight: 500; font-size: 0.86rem; letter-spacing: 0.02em;">
                    Copyright &copy; 2023–2026 Keystone Possibilities Ltd &bull; All Rights Reserved.
                </p>
                <p style="margin: 0; color: #c5a059; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em;">
                    Certified BC Housing Residential Builder #52603 &bull; Fiduciary CCDC 5B Construction Management
                </p>
            </div>

            <!-- C. Regional Divisions & Specialized Services 4-Column Mesh (Unified Obsidian & Gold) -->
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 28px; margin-bottom: 12px; text-align: left;">
                <div style="color: #d4af37; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 16px; font-size: 0.78rem; display: flex; align-items: center; justify-content: center; gap: 8px; text-align: center;">
                    <span>🏛️</span> KEYSTONE POSSIBILITIES — REGIONAL DIVISIONS &amp; SPECIALIZED SERVICES
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; line-height: 1.6;">
                    <div>
                        <strong style="color: #ffffff; display: block; margin-bottom: 8px; font-size: 0.85rem;">Sea-to-Sky Corridor:</strong>
                        <a href="/squamish-custom-homes/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• Squamish Custom Home Builder</a>
                        <a href="/whistler-custom-homes/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• Whistler Luxury Estate Builder</a>
                        <a href="/pemberton-luxury-builder/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• Pemberton Acreage Builder</a>
                    </div>
                    <div>
                        <strong style="color: #ffffff; display: block; margin-bottom: 8px; font-size: 0.85rem;">Metro Vancouver:</strong>
                        <a href="/north-vancouver-custom-homes/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• North Vancouver Luxury Builder</a>
                        <a href="/west-vancouver-custom-homes/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• North &amp; West Vancouver Custom Homes</a>
                        <a href="/west-vancouver-luxury-renovations/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• West Vancouver Steep Slope Builds</a>
                    </div>
                    <div>
                        <strong style="color: #ffffff; display: block; margin-bottom: 8px; font-size: 0.85rem;">Civil &amp; Fiduciary PM:</strong>
                        <a href="/bc-hydro-registered-civil-contractor/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• BC Hydro Civil Utility Contractor</a>
                        <a href="/feasibility-plan/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• Custom Build &amp; Cost Plan</a>
                        <a href="/private-investors/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• Private Investor Joint Ventures</a>
                    </div>
                    <div>
                        <strong style="color: #ffffff; display: block; margin-bottom: 8px; font-size: 0.85rem;">Direct Authority &amp; Contact:</strong>
                        <span style="color: #94a3b8; display: block; margin-bottom: 4px;">BC Housing License #52603</span>
                        <a href="tel:+16048489688" style="color: #f6d365; text-decoration: none !important; font-weight: 700; display: block; margin-bottom: 6px; font-size: 0.90rem;">📞 (604) 848-9688</a>
                        <a href="/contact-general-contractor-squamish/" style="color: #94a3b8; text-decoration: none !important; display: block; transition: color 0.2s ease;">• Schedule Fiduciary Consultation</a>
                    </div>
                </div>
            </div>

        </div>
    </footer>
    <a href="tel:+16048489688" id="kp-floating-phone" class="keystone-mobile-call-bar" aria-label="Call Keystone Possibilities (604) 848-9688">
        <span>📞 (604) 848-9688</span>
    </a>
    <?php
}

// Ensure Astra primary nav menu item for /feasibility-plan/ displays "CUSTOM BUILD & COST PLAN"
add_filter('wp_nav_menu_objects', function($items) {
    if (!is_array($items)) return $items;
    foreach ($items as $item) {
        if (!empty($item->url) && stripos($item->url, 'feasibility-plan') !== false) {
            $item->title = 'Custom Build & Cost Plan';
        }
    }
    return $items;
}, 20);

// ── 6. Real-Time Brand Sanitization & Zero CSS Leak Filter ──────────────────
add_filter('the_content', 'keystone_possibilities_sanitize_content_output', 999);
function keystone_possibilities_sanitize_content_output($content) {
    if (is_front_page() || is_home() || (function_exists('get_the_ID') && get_the_ID() === 563)) {
        $search = array(
            'KEYSTONE RECOMPOSITION',
            'ks-recomposition-header',
            '#ks-recomposition-header',
            'KEYSTONE POSSIBILITY HELP TD',
            'BILL 44 MULTIPLEX INFILL, MANAGED WITH',
            'Start-to-Finish Luxury Custom Homes, Bill 44 Multiplex Development &amp; Turnkey BC Hydro Civil Contracting (ES54)',
            'Start-to-Finish Luxury Custom Homes, Bill 44 Multiplex Development & Turnkey BC Hydro Civil Contracting (ES54)',
            'START WITH A FEASIBILITY PLAN &rarr;',
            'START WITH A FEASIBILITY PLAN →',
            'START WITH A FEASIBILITY PLAN',
            'START YOUR FEASIBILITY PLAN &rarr;',
            'START YOUR FEASIBILITY PLAN →',
            'START YOUR FEASIBILITY PLAN',
            'Start With a Property Feasibility Plan',
            'BOOK YOUR FEASIBILITY CALL &rarr;',
            'BOOK YOUR FEASIBILITY CALL →',
            '<a href="/north-vancouver-multiplex-conversions/" class="municipal-pill">Vancouver Infill →</a>',
            '<a href="/north-vancouver-multiplex-conversions/" class="municipal-pill">Vancouver Infill &rarr;</a>',
            '<option value="Vancouver Infill">Vancouver Infill (Bill 44)</option>',
            '<option value="Luxury Custom Estate">Luxury Custom Estate ($3M &#8211; $15M+)</option>',
            '<option value="Luxury Custom Estate">Luxury Custom Estate ($3M – $15M+)</option>',
            '<option value="Hillside Rock Concrete Build">Hillside Rock &amp; Concrete Build</option>',
            '<option value="Bill 44 Multiplex Infill">Bill 44 Multiplex Infill (3-6 Units)</option>',
            '<option value="BC Hydro Civil Infrastructure">BC Hydro Civil &amp; Transformer Vaults</option>',
            'Bill 44 Multiplex Retainer (3-6 Units)',
            'Bill 44 Multiplex Conversion (3-6 Units)',
            'Request My Custom Feasibility Plan →',
            '<span>📐 Feasibility Plan</span>',
            'Building ultra-luxury mountain residences and complex multiplex infill requires',
            '<h2>Sea-to-Sky &amp; Vancouver Infill</h2>',
            '<h2>Sea-to-Sky & Vancouver Infill</h2>',
            'and Bill 44 multiplex conversions engineered across',
            '<div class="portfolio-badge">Squamish Infill</div>',
            '<h4>Highlands Multiplex Infill</h4>',
            'Bill 44 high-efficiency multiplex development optimizing allowable density with turnkey civil infrastructure, separate hydro metering, and luxury tenant suites.',
            '<h2>Start With An Exhaustive Feasibility Plan</h2>',
            '<span>Book Feasibility Consultation →</span>',
            '<span>Book Feasibility Consultation &rarr;</span>',
            'regarding your custom estate or multiplex development project.'
        );
        $replace = array(
            'KEYSTONE POSSIBILITIES LTD',
            'ks-possibilities-header',
            '#ks-possibilities-header',
            'KEYSTONE POSSIBILITIES LTD — CLIENT &amp; CONSULTING SERVICES',
            'BC HYDRO CIVIL INFRASTRUCTURE, MANAGED WITH',
            'Start-to-Finish Luxury Custom Homes, Architectural Mountain &amp; Coastal Estates, and Turnkey BC Hydro Civil Contracting (ES54)',
            'Start-to-Finish Luxury Custom Homes, Architectural Mountain & Coastal Estates, and Turnkey BC Hydro Civil Contracting (ES54)',
            'START YOUR CUSTOM HOME OR CIVIL PROJECT PLAN &rarr;',
            'START YOUR CUSTOM HOME OR CIVIL PROJECT PLAN →',
            'START YOUR CUSTOM HOME OR CIVIL PROJECT PLAN',
            'START YOUR CUSTOM HOME OR CIVIL PROJECT PLAN &rarr;',
            'START YOUR CUSTOM HOME OR CIVIL PROJECT PLAN →',
            'START YOUR CUSTOM HOME OR CIVIL PROJECT PLAN',
            'Start With a Custom Home or Civil Pre-Construction Plan',
            'START YOUR CUSTOM BUILD OR CIVIL PLAN &rarr;',
            'START YOUR CUSTOM BUILD OR CIVIL PLAN →',
            '<a href="/bc-hydro-registered-civil-contractor/" class="municipal-pill">BC Hydro Civil ES54 →</a>',
            '<a href="/bc-hydro-registered-civil-contractor/" class="municipal-pill">BC Hydro Civil ES54 &rarr;</a>',
            '<option value="Vancouver">Vancouver (Custom Homes &amp; Estates)</option>',
            '<option value="Luxury Custom Home / Architectural Estate (Builder #52603)">Luxury Custom Home / Architectural Estate (Builder #52603)</option>',
            '<option value="Luxury Custom Home / Architectural Estate (Builder #52603)">Luxury Custom Home / Architectural Estate (Builder #52603)</option>',
            '<option value="BC Hydro Civil Infrastructure & Underground Servicing (ES54)">BC Hydro Civil Infrastructure &amp; Underground Servicing (ES54)</option>',
            '<option value="Major Custom Renovation / Structural Addition">Major Custom Renovation / Structural Addition</option>',
            '<option value="Carriage House, Luxury Duplex or Multi-Generational Build">Carriage House, Luxury Duplex or Multi-Generational Build</option>',
            'Luxury Custom Home / Architectural Estate (Builder #52603)',
            'Major Custom Renovation / Structural Addition',
            'Request My Custom Home &amp; Civil Pre-Construction Plan →',
            '<span>📐 Cost &amp; Build Plan</span>',
            'Building ultra-luxury mountain residences, custom coastal estates, and BC Hydro ES54 civil infrastructure requires',
            '<h2>Sea-to-Sky &amp; North Shore Custom Homes &amp; Civil</h2>',
            '<h2>Sea-to-Sky &amp; North Shore Custom Homes &amp; Civil</h2>',
            'and BC Hydro ES54 civil infrastructure engineered across',
            '<div class="portfolio-badge">Squamish Custom &amp; Civil</div>',
            '<h4>Highlands Custom Estate &amp; Civil Servicing</h4>',
            'Mountain modern custom residence and carriage house build featuring turnkey BC Hydro ES54 underground civil infrastructure, PMT vault servicing, and Step Code 5 envelope.',
            '<h2>Start With a Custom Home or Civil Pre-Construction Plan</h2>',
            '<span>Start Your Custom Home or Civil Project Plan →</span>',
            '<span>Start Your Custom Home or Civil Project Plan &rarr;</span>',
            'regarding your luxury custom home, architectural estate, or BC Hydro ES54 civil project.'
        );
        $content = str_replace($search, $replace, $content);
        // Replace inline linear-gradient h2 with clean class to eliminate white glare box
        $content = preg_replace('/(<h2[^>]*?)\s*style=["\'][^"\']*linear-gradient[^"\']*["\']([^>]*>)/i', '$1 class="kp-hero-title"$2', $content);
    }

    // Strip leaking inline styles, <style> tags, or p-wrapped CSS rules across all content
    $content = preg_replace('/<style\b[^>]*>[\s\S]*?<\/style>/i', '', $content);

    $css_leak_patterns = array(
        '/(<p>\s*)?\.kp-regional-grid\s*(?:>|&gt;)\s*p[\s\S]*?(?:grid-column:\s*1\s*!important;\s*\}\s*\}|@media[^{]*\{[^{}]*\{[^{}]*\}\s*\})\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-regional-grid\s*(?:>|&gt;)\s*p\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-glass:empty\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-regional-grid\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?@media\s*\(\s*max-width:\s*768px\s*\)\s*\{\s*\.kp-regional-grid[\s\S]*?\}\s*\}/i',
        '/(<p>\s*)?\.kp-gold-title[\s\S]*?#ks-(?:possibilities|recomposition)-header\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-gold-title\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-glass(?::hover)?\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-h-scroll\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-scroll-card\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?\.kp-step\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?header\.entry-header\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?#ks-top-help-td\s*\{[^}]*\}\s*(<\/p>)?/i',
        '/(<p>\s*)?#ks-(?:possibilities|recomposition)-header\s*\{[^}]*\}\s*(<\/p>)?/i',
    );
    $content = preg_replace($css_leak_patterns, '', $content);

    return $content;
}
// ── 7. Critical Hero Title CSS (Eliminates White Glare Box & Enforces Quiet Luxury Gold)
add_action('wp_head', 'keystone_possibilities_inject_critical_hero_css', 99);
function keystone_possibilities_inject_critical_hero_css() {
    ?>
    <style id="keystone-hero-title-critical-fix">
    #ks-possibilities-header h2,
    #ks-recomposition-header h2,
    .kp-hero-title {
        margin: 0 !important;
        padding: 0 !important;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #d4af37 !important; /* Elegant warm quiet luxury gold */
        background: none !important;
        background-image: none !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.9), 0 0 20px rgba(212, 175, 55, 0.35) !important;
        display: inline-block !important;
    }
    </style>
    <?php
}

// ── 8. Google-Compliant Above-The-Fold Video Watch Theater Injector ─────────
add_filter('the_content', 'keystone_possibilities_ensure_watch_theater', 5);
function keystone_possibilities_ensure_watch_theater($content) {
    if (!is_singular('post') || is_admin() || is_feed()) {
        return $content;
    }

    global $post;
    if (!$post) return $content;

    // Detect YouTube ID from post meta or content
    $video_id = get_post_meta($post->ID, 'keystone_youtube_id', true);
    if (empty($video_id)) {
        $video_url = get_post_meta($post->ID, 'video_url', true);
        if (!empty($video_url) && preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $video_url, $m)) {
            $video_id = $m[1];
        }
    }
    if (empty($video_id)) {
        if (preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $content, $m)) {
            $video_id = $m[1];
        }
    }

    if (empty($video_id)) {
        return $content;
    }

    // Check if an iframe already exists in the first 300 characters
    $first_chunk = substr(trim(strip_tags($content ?? '', '<iframe>')), 0, 300);
    if (stripos($first_chunk, '<iframe') !== false) {
        return $content;
    }

    // Strip duplicate iframes or embed blocks placed deeper in the article
    $sanitized_content = preg_replace('/<figure class="wp-block-embed[^>]*>.*?<\/figure>/is', '', $content);
    $sanitized_content = preg_replace('/<iframe[^>]*src="[^"]*youtube[^"]*"[^>]*><\/iframe>/is', '', $sanitized_content);

    // Build Compliant 16:9 Above-the-Fold Watch Theater (Dominant primary entity)
    $theater_html = '
    <div class="watch-theater-embed">
        <iframe src="https://www.youtube-nocookie.com/embed/' . esc_attr($video_id) . '?rel=0&modestbranding=1" 
                title="' . esc_attr(get_the_title($post)) . '" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen 
                loading="eager">
        </iframe>
    </div>';

    return $theater_html . $sanitized_content;
}

// ── 7. 2026 Master Portfolio Carousel Controller (Inline Footer Engine) ──────
add_action('wp_footer', 'keystone_possibilities_render_carousel_script', 99);
function keystone_possibilities_render_carousel_script() {
    ?>
    <script id="keystone-portfolio-carousel-inline">
    (function() {
        function initCarousels() {
            const sections = document.querySelectorAll('.residence-section');
            if (!sections.length) return;

            sections.forEach((section) => {
                const track = section.querySelector('.residence-carousel-track');
                if (!track) return;

                const cards = track.querySelectorAll('.residence-card');
                const total = cards.length;
                if (total <= 1) return;

                let headerBar = section.querySelector('.residence-carousel-header-bar');
                if (!headerBar) {
                    const titleHeading = section.querySelector('.residence-title-heading');
                    if (titleHeading) {
                        headerBar = document.createElement('div');
                        headerBar.className = 'residence-carousel-header-bar';
                        titleHeading.parentNode.insertBefore(headerBar, titleHeading);
                        headerBar.appendChild(titleHeading);
                    }
                }

                if (headerBar && !headerBar.querySelector('.residence-carousel-controls')) {
                    const controls = document.createElement('div');
                    controls.className = 'residence-carousel-controls';

                    const badge = document.createElement('span');
                    badge.className = 'residence-counter-badge';
                    badge.textContent = `01 / ${String(total).padStart(2, '0')}`;

                    const prevBtn = document.createElement('button');
                    prevBtn.className = 'residence-nav-btn prev';
                    prevBtn.setAttribute('aria-label', 'Previous photo');
                    prevBtn.innerHTML = '&#8249;';

                    const nextBtn = document.createElement('button');
                    nextBtn.className = 'residence-nav-btn next';
                    nextBtn.setAttribute('aria-label', 'Next photo');
                    nextBtn.innerHTML = '&#8250;';

                    controls.appendChild(badge);
                    controls.appendChild(prevBtn);
                    controls.appendChild(nextBtn);
                    headerBar.appendChild(controls);

                    prevBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        const cardWidth = cards[0].getBoundingClientRect().width + 20;
                        track.scrollBy({ left: -cardWidth, behavior: 'smooth' });
                    });

                    nextBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        const cardWidth = cards[0].getBoundingClientRect().width + 20;
                        track.scrollBy({ left: cardWidth, behavior: 'smooth' });
                    });

                    if ('IntersectionObserver' in window) {
                        const observer = new IntersectionObserver((entries) => {
                            entries.forEach(entry => {
                                if (entry.isIntersecting) {
                                    const cardIndex = Array.from(cards).indexOf(entry.target);
                                    if (cardIndex !== -1) {
                                        badge.textContent = `${String(cardIndex + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
                                    }
                                }
                            });
                        }, { root: track, threshold: 0.6 });
                        cards.forEach(card => observer.observe(card));
                    }
                }
            });
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initCarousels);
        } else {
            initCarousels();
        }
    })();
    </script>
    <?php
}



// ── Disarm Jetpack Photon CDN (Serve 100% Direct Origin High-Res Images) ───
add_filter('jetpack_photon_skip_image', '__return_true');
add_filter('jetpack_photon_pre_image_url', function($url, $args) { return $url; }, 10, 2);
// =============================================================================
// KEYSTONE POSSIBILITIES — 2026 ARCHITECTURAL DARK QUIET LUXURY HEADER & FOOTER
// Certified BC Housing Builder #52603 | Wayne Stevenson Master Builder Engine
// =============================================================================

add_action('wp_head', 'keystone_possibilities_luxury_header_overrides', 99);
function keystone_possibilities_luxury_header_overrides() {
    ?>
    <style id="keystone-luxury-header-overrides">
        /* Main Header Dark Luxury Styling */
        #masthead {
            background-color: #05080E !important;
            border-bottom: 1px solid rgba(212, 175, 55, 0.22) !important;
        }
        .site-primary-header-wrap {
            max-width: 1680px !important;
            margin: 0 auto !important;
            padding: 0 20px !important;
        }
        .ast-builder-grid-row {
            grid-template-columns: auto 1fr auto !important;
            align-items: center !important;
        }
        .site-header-primary-section-left {
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }
        .site-header-primary-section-left-center {
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
        }
        /* Wayne's Real Logo Badge Lockup */
        .brand-edge-logo {
            display: inline-flex !important;
            align-items: center !important;
            gap: 10px !important;
            text-decoration: none !important;
            padding: 4px 0 !important;
            transition: opacity 0.2s ease !important;
            flex-shrink: 0 !important;
        }
        .brand-edge-logo:hover {
            opacity: 0.9 !important;
        }
        .kp-badge-mark {
            width: 44px !important;
            height: 44px !important;
            border-radius: 9px !important;
            overflow: hidden !important;
            border: none !important;
            box-shadow: 0 0 16px rgba(212, 175, 55, 0.45) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: transparent !important;
            flex-shrink: 0 !important;
        }
        .kp-badge-img {
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important;
            display: block !important;
        }
        .brand-title-wrap {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            line-height: 1.15 !important;
        }
        .brand-title-wrap .title-main {
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.92rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: #FFFFFF !important;
            white-space: nowrap !important;
        }
        .brand-title-wrap .title-sub {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.65rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.14em !important;
            text-transform: uppercase !important;
            color: #D4AF37 !important;
            white-space: nowrap !important;
            margin-top: 1px !important;
        }
        /* Navigation Links: Perfectly Centered in Header */
        .site-header-primary-section-center {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin: 0 auto !important;
            width: 100% !important;
        }
        #ast-hf-menu-1 {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin: 0 auto !important;
        }
        #ast-hf-menu-1 > li > a {
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            padding: 0 10px !important;
            color: #CBD5E1 !important;
            text-transform: uppercase !important;
            transition: color 0.2s ease !important;
        }
        #ast-hf-menu-1 > li > a:hover {
            color: #E6C275 !important;
        }
        #ast-hf-menu-1 > li.current-menu-item > a {
            color: #D4AF37 !important;
            font-weight: 700 !important;
        }

        /* Luxury Form Select & Input Standards (Zero Text Clipping) */
        .kp-feasibility-page-wrapper select,
        .kp-feasibility-page-wrapper input[type="text"],
        .kp-feasibility-page-wrapper input[type="tel"],
        .kp-feasibility-page-wrapper input[type="email"] {
            height: 52px !important;
            min-height: 52px !important;
            line-height: 52px !important;
            padding: 0 16px !important;
            font-size: 0.95rem !important;
            box-sizing: border-box !important;
            background-color: #070b14 !important;
            color: #ffffff !important;
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            border-radius: 8px !important;
            display: block !important;
        }
        .kp-feasibility-page-wrapper select option {
            background-color: #070b14 !important;
            color: #ffffff !important;
            padding: 10px !important;
        }
        /* Hide Astra Default Footer on Home Page */
        .home #colophon {
            display: none !important;
        }
        .home .keystone-mobile-call-bar {
            display: none !important;
        }

        /* Feasibility Plan (Page 1409) Layout & Title Suppression */
        .page-id-1409 .entry-header,
        .page-id-1409 .ast-single-post-order,
        .page-id-1409 .entry-title,
        .page-id-1409 #colophon,
        .page-id-1409 .keystone-mobile-call-bar {
            display: none !important;
        }
        .page-id-1409 .site-content {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            background-color: #04070d !important;
        }
        .page-id-1409 .ast-container {
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-top: 0 !important;
            margin: 0 !important;
        }
        .page-id-1409 #primary {
            margin: 0 !important;
            padding: 0 !important;
        }
        .page-id-1409 .ast-article-single {
            padding: 0 !important;
            margin: 0 !important;
        }
        .page-id-1409 .entry-content {
            margin-top: 0 !important;
        }
        .page-id-1409 .entry-content[data-ast-blocks-layout] > *,
        .page-id-1409 .entry-content > *,
        .page-id-1409 .kp-feasibility-page-wrapper {
            max-width: 100% !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* =========================================================================
           GLOBAL LUXURY SUITE PAGE TITLE SUPPRESSION & FULL-BLEED ARCHITECTURE
           Pages: 1255 (Civil), 1219 (Investors), 2 (About Us), 114 (Portfolio), 547 (Series)
           ========================================================================= */
        .page-id-283 .entry-header,
        .page-id-283 .ast-single-post-order,
        .page-id-283 .entry-title,
        .page-id-283 #colophon,
        .page-id-283 .keystone-mobile-call-bar,
        .page-id-1255 .entry-header,
        .page-id-1255 .ast-single-post-order,
        .page-id-1255 .entry-title,
        .page-id-1255 #colophon,
        .page-id-1255 .keystone-mobile-call-bar,
        .page-id-1219 .entry-header,
        .page-id-1219 .ast-single-post-order,
        .page-id-1219 .entry-title,
        .page-id-1219 #colophon,
        .page-id-1219 .keystone-mobile-call-bar,
        .page-id-2 .entry-header,
        .page-id-2 .ast-single-post-order,
        .page-id-2 .entry-title,
        .page-id-2 #colophon,
        .page-id-2 .keystone-mobile-call-bar,
        .page-id-114 .entry-header,
        .page-id-114 .ast-single-post-order,
        .page-id-114 .entry-title,
        .page-id-114 #colophon,
        .page-id-114 .keystone-mobile-call-bar,
        .page-id-547 .entry-header,
        .page-id-547 .ast-single-post-order,
        .page-id-547 .entry-title,
        .page-id-547 #colophon,
        .page-id-547 .keystone-mobile-call-bar {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            visibility: hidden !important;
            position: absolute !important;
            pointer-events: none !important;
        }

        .page-id-283 .site-content,
        .page-id-1255 .site-content,
        .page-id-1219 .site-content,
        .page-id-2 .site-content,
        .page-id-114 .site-content,
        .page-id-547 .site-content {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            background-color: #04070d !important;
        }

        .page-id-283 .ast-container,
        .page-id-1255 .ast-container,
        .page-id-1219 .ast-container,
        .page-id-2 .ast-container,
        .page-id-114 .ast-container,
        .page-id-547 .ast-container {
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-top: 0 !important;
            margin: 0 !important;
        }

        .page-id-283 #primary,
        .page-id-1255 #primary,
        .page-id-1219 #primary,
        .page-id-2 #primary,
        .page-id-114 #primary,
        .page-id-547 #primary {
            margin: 0 !important;
            padding: 0 !important;
        }

        .page-id-283 .ast-article-single,
        .page-id-1255 .ast-article-single,
        .page-id-1219 .ast-article-single,
        .page-id-2 .ast-article-single,
        .page-id-114 .ast-article-single,
        .page-id-547 .ast-article-single {
            padding: 0 !important;
            margin: 0 !important;
        }

        .page-id-283 .entry-content,
        .page-id-1255 .entry-content,
        .page-id-1219 .entry-content,
        .page-id-2 .entry-content,
        .page-id-114 .entry-content,
        .page-id-547 .entry-content {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* Wayne's Gold Button Law Across All Pages */
        a.btn-gold-action,
        a[style*="linear-gradient"],
        .kp-btn-primary,
        .kp-btn-gold {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 800 !important;
        }
        a.btn-gold-action *,
        a[style*="linear-gradient"] *,
        .kp-btn-primary *,
        .kp-btn-gold * {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 800 !important;
        }


        /* Luxury Button & Card Classes */
        .kp-btn-primary {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: linear-gradient(135deg, #d4af37 0%, #c4a265 50%, #aa8232 100%) !important;
            color: #04070d !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 900 !important;
            font-size: 0.92rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            padding: 13px 28px !important;
            border-radius: 9999px !important;
            text-decoration: none !important;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
            border: 1px solid #f6d365 !important;
            transition: all 0.25s ease !important;
            cursor: pointer !important;
        }
        .kp-btn-primary:hover {
            background: linear-gradient(135deg, #f6d365 0%, #d4af37 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(212, 175, 55, 0.6) !important;
            color: #04070d !important;
        }
        .kp-btn-secondary {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: rgba(15, 23, 42, 0.95) !important;
            color: #ffffff !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.92rem !important;
            letter-spacing: 0.05em !important;
            padding: 13px 26px !important;
            border-radius: 9999px !important;
            text-decoration: none !important;
            border: 1px solid rgba(212, 175, 55, 0.45) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6) !important;
            transition: all 0.25s ease !important;
            cursor: pointer !important;
        }
        .kp-btn-secondary:hover {
            border-color: #00f0ff !important;
            color: #00f0ff !important;
            transform: translateY(-2px) !important;
        }
        .kp-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(4, 7, 13, 0.98) 100%) !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            border-radius: 16px !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7) !important;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
        }
        .kp-card:hover {
            border-color: rgba(212, 175, 55, 0.65) !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 25px rgba(212, 175, 55, 0.2) !important;
            transform: translateY(-3px) !important;
        }
        .kp-badge {
            display: inline-flex !important;
            align-items: center !important;
            gap: 8px !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.78rem !important;
            font-weight: 800 !important;
            color: #f6d365 !important;
            background: rgba(212, 175, 55, 0.12) !important;
            padding: 6px 16px !important;
            border-radius: 9999px !important;
            border: 1px solid rgba(212, 175, 55, 0.35) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
        }
        .kp-gold-glow {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            color: #d4af37 !important;
            background: none !important;
            -webkit-text-fill-color: initial !important;
            text-shadow: 0 2px 12px rgba(0, 0, 0, 0.9), 0 0 20px rgba(212, 175, 55, 0.4) !important;
        }

        /* Feasibility Plan Responsive Grid & Mobile Standards */
        @media (max-width: 980px) {
            .kp-grid-3col {
                grid-template-columns: 1fr !important;
            }
            .kp-grid-2col {
                grid-template-columns: 1fr !important;
            }
        }
        @media (max-width: 680px) {
            .kp-feasibility-page-wrapper {
                padding-left: 8px !important;
                padding-right: 8px !important;
            }
            #fiduciary-calculator div[style*="grid-template-columns: repeat(3, 1fr)"] {
                grid-template-columns: 1fr !important;
            }
            form[action*="contact-general-contractor-squamish"] {
                grid-template-columns: 1fr !important;
            }
            form[action*="contact-general-contractor-squamish"] > div {
                grid-column: span 1 !important;
            }
        }

        /* 2026 Slim 52px Mobile Header + ☰ MENU ▾ Pill + Scrollable Dropdown Drawer */
        body:has(#kpSiteNavHeader) #masthead,
        header#masthead {
            display: none !important;
            height: 0 !important;
            overflow: hidden !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        .site-nav-header#kpSiteNavHeader {
            position: sticky !important;
            top: 0 !important;
            z-index: 10002 !important;
            background: rgba(4, 7, 13, 0.97) !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
            border-bottom: 1px solid rgba(212, 175, 55, 0.34) !important;
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.78) !important;
            width: 100% !important;
        }
        #kpSiteNavHeader .nav-container {
            max-width: 1680px !important;
            margin: 0 auto !important;
            padding: 0 20px !important;
            height: 60px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 16px !important;
            box-sizing: border-box !important;
        }
        #kpSiteNavHeader .nav-links-menu {
            display: flex !important;
            align-items: center !important;
            gap: clamp(10px, 1.1vw, 20px) !important;
            list-style: none !important;
            margin: 0 0 0 16px !important;
            padding: 0 !important;
        }
        #kpSiteNavHeader .nav-link-item {
            color: #CBD5E1 !important;
            text-decoration: none !important;
            font-size: clamp(0.72rem, 0.76vw, 0.80rem) !important;
            font-weight: 600 !important;
            letter-spacing: 0.07em !important;
            text-transform: uppercase !important;
            padding: 6px 2px !important;
            white-space: nowrap !important;
        }
        #kpSiteNavHeader .nav-link-item:hover,
        #kpSiteNavHeader .nav-link-item.active {
            color: #D4AF37 !important;
        }
        #kpSiteNavHeader .nav-right-actions {
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            margin-left: auto !important;
            flex-shrink: 0 !important;
        }
        #kpSiteNavHeader .mobile-hamburger#kpMobileNavToggle {
            display: none;
            align-items: center !important;
            justify-content: center !important;
            gap: 6px !important;
            padding: 7px 14px !important;
            border-radius: 9999px !important;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.24) 0%, rgba(10, 18, 34, 0.96) 55%, rgba(56, 189, 248, 0.22) 100%) !important;
            border: 1.5px solid #d4af37 !important;
            box-shadow: 0 0 14px rgba(212, 175, 55, 0.35), 0 0 10px rgba(56, 189, 248, 0.22) !important;
            color: #FFF2C6 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.75rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }
        #kpSiteNavHeader .mobile-hamburger#kpMobileNavToggle:hover,
        #kpSiteNavHeader .mobile-hamburger#kpMobileNavToggle.is-open {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.55), 0 0 14px rgba(212, 175, 55, 0.45) !important;
            color: #ffffff !important;
        }
        .mobile-menu-drawer#mobileDrawer {
            display: none !important;
            position: fixed !important;
            top: 52px !important;
            left: 0 !important;
            right: 0 !important;
            bottom: auto !important;
            max-height: calc(100vh - 64px) !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            background: rgba(4, 7, 13, 0.98) !important;
            backdrop-filter: blur(22px) !important;
            -webkit-backdrop-filter: blur(22px) !important;
            border-bottom: 2px solid #d4af37 !important;
            box-shadow: 0 24px 54px rgba(0, 0, 0, 0.92), 0 0 24px rgba(212, 175, 55, 0.22) !important;
            z-index: 10001 !important;
            padding: 12px 14px 20px 14px !important;
            flex-direction: column !important;
            gap: 8px !important;
            box-sizing: border-box !important;
        }
        .mobile-menu-drawer#mobileDrawer.open {
            display: flex !important;
        }
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-featured-cta {
            display: flex !important;
            flex-direction: column !important;
            gap: 4px !important;
            padding: 12px 14px !important;
            margin-bottom: 4px !important;
            border-radius: 14px !important;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.20) 0%, rgba(10, 18, 34, 0.96) 55%, rgba(56, 189, 248, 0.16) 100%) !important;
            border: 1.5px solid #d4af37 !important;
            box-shadow: 0 10px 26px rgba(0, 0, 0, 0.75), 0 0 18px rgba(212, 175, 55, 0.25), inset 0 0 14px rgba(56, 189, 248, 0.12) !important;
            text-decoration: none !important;
            text-transform: none !important;
        }
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-featured-cta .drawer-cta-badge {
            display: inline-flex !important;
            align-items: center !important;
            align-self: flex-start !important;
            padding: 2px 9px !important;
            border-radius: 9999px !important;
            background: rgba(56, 189, 248, 0.16) !important;
            border: 1px solid rgba(56, 189, 248, 0.55) !important;
            color: #38bdf8 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.64rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
        }
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-featured-cta .drawer-cta-title {
            color: #FFF2C6 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.86rem !important;
            font-weight: 900 !important;
            line-height: 1.3 !important;
            letter-spacing: 0.02em !important;
        }
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-featured-cta .drawer-cta-sub {
            color: #cbd5e1 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            line-height: 1.35 !important;
        }
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-link {
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            gap: 10px !important;
            padding: 10px 14px !important;
            border-radius: 12px !important;
            background: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(212, 175, 55, 0.25) !important;
            color: #F8FAFC !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 0.84rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            text-decoration: none !important;
            transition: all 0.18s ease !important;
        }
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-link:hover,
        .mobile-menu-drawer#mobileDrawer a.mobile-drawer-link.active {
            border-color: #d4af37 !important;
            background: rgba(212, 175, 55, 0.14) !important;
            color: #FFF2C6 !important;
        }
        .dock-btn-plan,
        .dock-btn-plan * {
            color: #04070d !important;
            -webkit-text-fill-color: #04070d !important;
            font-weight: 800 !important;
            text-decoration: none !important;
        }
        @media (max-width: 1024px) {
            #kpSiteNavHeader .kp-desktop-nav-wrap,
            #kpSiteNavHeader .nav-links-menu {
                display: none !important;
            }
            #kpSiteNavHeader .mobile-hamburger#kpMobileNavToggle {
                display: inline-flex !important;
            }
            #rank-math-analytics-stats-wrapper,
            #rank-math-analytics-stats-bar,
            .rank-math-analytics-stats-bar,
            [id*="rank-math-analytics"],
            [class*="rank-math-analytics"] {
                display: none !important;
                visibility: hidden !important;
                pointer-events: none !important;
            }
        }
        @media (max-width: 768px) {
            .site-nav-header#kpSiteNavHeader {
                height: 52px !important;
                min-height: 52px !important;
                max-height: 52px !important;
            }
            #kpSiteNavHeader .nav-container {
                height: 52px !important;
                min-height: 52px !important;
                max-height: 52px !important;
                padding: 0 12px !important;
                gap: 8px !important;
            }
            #kpSiteNavHeader .brand-edge-logo {
                gap: 8px !important;
                min-width: 0 !important;
                flex: 1 1 auto !important;
                overflow: hidden !important;
            }
            #kpSiteNavHeader .kp-badge-mark {
                width: 32px !important;
                height: 32px !important;
                border-radius: 7px !important;
                flex-shrink: 0 !important;
            }
            #kpSiteNavHeader .brand-title-wrap {
                min-width: 0 !important;
                overflow: hidden !important;
            }
            #kpSiteNavHeader .brand-title-wrap .title-main {
                font-size: 0.78rem !important;
                letter-spacing: 0.04em !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }
            #kpSiteNavHeader .brand-title-wrap .title-sub {
                font-size: 0.55rem !important;
                letter-spacing: 0.10em !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }
            #kpSiteNavHeader .social-icon-btn {
                display: none !important;
            }
            #kpSiteNavHeader .nav-right-actions {
                margin-left: auto !important;
                flex-shrink: 0 !important;
            }
            #kpSiteNavHeader .mobile-hamburger#kpMobileNavToggle {
                display: inline-flex !important;
                padding: 6px 12px !important;
                font-size: 0.72rem !important;
                height: 34px !important;
            }
        }
    </style>
    <?php
}

add_action('wp_body_open', 'keystone_possibilities_render_slim_nav_header', 5);
function keystone_possibilities_render_slim_nav_header() {
    if (defined('KP_HEADER_RENDERED')) {
        return;
    }
    define('KP_HEADER_RENDERED', true);
    ?>
    <header class="site-nav-header" id="kpSiteNavHeader">
        <div class="nav-container">
            <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="brand-edge-logo" aria-label="Keystone Possibilities Ltd. Home">
                <div class="kp-badge-mark">
                    <img src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png" alt="Keystone Possibilities Ltd." class="kp-badge-img">
                </div>
                <div class="brand-title-wrap">
                    <span class="title-main">KEYSTONE POSSIBILITIES</span>
                    <span class="title-sub">LICENSED BUILDER #52603</span>
                </div>
            </a>
            <nav aria-label="Main Navigation" class="kp-desktop-nav-wrap">
                <ul class="nav-links-menu">
                    <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="nav-link-item <?php echo is_front_page() ? 'active' : ''; ?>">HOME</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>" class="nav-link-item">CUSTOM BUILD &amp; COST PLAN</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/client-portal/' ) ); ?>" class="nav-link-item">CLIENT LOGIN</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/#master-builder-series' ) ); ?>" class="nav-link-item">MASTER BUILDER SERIES</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/#portfolio' ) ); ?>" class="nav-link-item">PORTFOLIO</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/about-us-general-contractor-squamish/' ) ); ?>" class="nav-link-item">ABOUT US</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/private-investors/' ) ); ?>" class="nav-link-item">PRIVATE INVESTORS</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/bc-hydro-registered-civil-contractor/' ) ); ?>" class="nav-link-item">CIVIL</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/contact-general-contractor-squamish/' ) ); ?>" class="nav-link-item">CONTACT</a></li>
                </ul>
            </nav>
            <div class="nav-right-actions">
                <a href="https://facebook.com" target="_blank" rel="noopener" class="social-icon-btn" aria-label="Facebook">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="https://instagram.com" target="_blank" rel="noopener" class="social-icon-btn" aria-label="Instagram">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.13-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                </a>
                <button type="button" class="mobile-hamburger" id="kpMobileNavToggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="mobileDrawer">
                    <span class="mobile-menu-pill-text">☰ MENU ▾</span>
                </button>
            </div>
        </div>
    </header>
    <div class="mobile-menu-drawer" id="mobileDrawer" aria-label="Mobile Navigation Drawer">
        <a href="<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>" class="mobile-drawer-featured-cta">
            <span class="drawer-cta-badge">⭐ FEATURED BUILDER TOOL · LICENSE #52603</span>
            <span class="drawer-cta-title">📐 CUSTOM BUILD &amp; COST PLAN — Custom Homes (#52603) &amp; BC Hydro Civil (ES54)</span>
            <span class="drawer-cta-sub">Interactive Lot Feasibility, Cost Breakdown &amp; Civil Scope Calculator →</span>
        </a>
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="mobile-drawer-link <?php echo is_front_page() ? 'active' : ''; ?>">🏠 HOME</a>
        <a href="<?php echo esc_url( home_url( '/client-portal/' ) ); ?>" class="mobile-drawer-link">🔐 CLIENT LOGIN</a>
        <a href="<?php echo esc_url( home_url( '/#master-builder-series' ) ); ?>" class="mobile-drawer-link">🎬 MASTER BUILDER SERIES</a>
        <a href="<?php echo esc_url( home_url( '/#portfolio' ) ); ?>" class="mobile-drawer-link">🏛️ PORTFOLIO</a>
        <a href="<?php echo esc_url( home_url( '/about-us-general-contractor-squamish/' ) ); ?>" class="mobile-drawer-link">👤 ABOUT US</a>
        <a href="<?php echo esc_url( home_url( '/private-investors/' ) ); ?>" class="mobile-drawer-link">📈 PRIVATE INVESTORS</a>
        <a href="<?php echo esc_url( home_url( '/bc-hydro-registered-civil-contractor/' ) ); ?>" class="mobile-drawer-link">⚡ CIVIL (ES54)</a>
        <a href="<?php echo esc_url( home_url( '/contact-general-contractor-squamish/' ) ); ?>" class="mobile-drawer-link">📞 CONTACT — (604) 848-9688</a>
    </div>
    <?php
}

add_action('wp_footer', 'keystone_possibilities_mount_header_logo_script', 99);
function keystone_possibilities_mount_header_logo_script() {
    ?>
    <script id="keystone-mount-logo-engine">
    (function() {
        function initHeaderAndDrawer() {
            var toggle = document.getElementById('kpMobileNavToggle');
            var drawer = document.getElementById('mobileDrawer');
            if (toggle && drawer && !toggle.dataset.kpBound) {
                toggle.dataset.kpBound = '1';
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    var isOpen = drawer.classList.toggle('open');
                    toggle.classList.toggle('is-open', isOpen);
                    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                });
                drawer.querySelectorAll('a').forEach(function(link) {
                    link.addEventListener('click', function() {
                        drawer.classList.remove('open');
                        toggle.classList.remove('is-open');
                        toggle.setAttribute('aria-expanded', 'false');
                    });
                });
                document.addEventListener('keydown', function(e) {
                    if (e.key === 'Escape' && drawer.classList.contains('open')) {
                        drawer.classList.remove('open');
                        toggle.classList.remove('is-open');
                        toggle.setAttribute('aria-expanded', 'false');
                    }
                });
            }
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initHeaderAndDrawer);
        } else {
            initHeaderAndDrawer();
        }
    })();
    </script>
    <?php
}

// ── Cleanly Suppress Astra Default Entry Titles Across All Pages ─────────────
add_filter('astra_the_title_enabled', 'keystone_possibilities_suppress_page_titles', 10, 1);
function keystone_possibilities_suppress_page_titles($enabled) {
    if (is_page()) {
        return false;
    }
    return $enabled;
}
add_filter('rank_math/sitemap/enable_caching', '__return_false');

// ── Cleanly Suppress Astra Default Featured Image Banners Across All Pages ──
add_filter('astra_featured_image_enabled', function($enabled) {
    if (is_page()) {
        return false;
    }
    return $enabled;
}, 99);
add_filter('astra_blog_post_thumb_enabled', function($enabled) {
    if (is_page()) {
        return false;
    }
    return $enabled;
}, 99);
add_filter('astra_page_post_thumb_enabled', function($enabled) {
    if (is_page()) {
        return false;
    }
    return $enabled;
}, 99);

// ── 9. Multi-Job Client & Builder Portal v10 REST API Fallback ─────────────
if (!function_exists('keystone_portal_v10_get_jobs')) {
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
}
