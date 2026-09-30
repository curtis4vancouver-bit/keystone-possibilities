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

    // Pass REST and AJAX endpoints to frontend for interactive lead capture
    wp_localize_script('keystone-lazy-player', 'keystoneData', array(
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'restUrl' => esc_url_raw(rest_url('keystone/v1/lead'))
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
// Disable automatic appending of legacy Bill 44 estimator on /feasibility-plan/ (replaces with clean luxury 1-box calculator)
remove_filter('the_content', 'keystone_possibilities_inject_feasibility_tools', 20);
require_once __DIR__ . '/inc/client-portal-demo.php';

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

// Tier 2: Guardrail - Strip category-sitemap from sitemap_index.xml XML output
add_filter('rank_math/sitemap/index', function (string $xml): string {
    $pattern = '/<sitemap>\s*<loc>[^<]*category-sitemap\.xml<\/loc>.*?<\/sitemap>\s*/is';
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

    // 1. Exclude legacy redirected paths, test URLs, and .html extensions
    $excluded_patterns = array(
        'sample-page',
        '/test/',
        '/demo/',
        'wp-admin',
        'wp-login',
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
        'pemberton-luxury-builder',
        'bc-hydro-registered-civil-contractor',
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
    $uri = (string) ( $_SERVER['REQUEST_URI'] ?? '' );
    $path = (string) strtok($uri, '?');
    
    // Serve /llms.txt dynamically for AI search engines (Perplexity, ChatGPT, Claude)
    if ($path === '/llms.txt' || $path === 'llms.txt') {
        $llms_file = get_stylesheet_directory() . '/llms.txt';
        if (file_exists($llms_file)) {
            header('Content-Type: text/plain; charset=utf-8');
            header('X-Robots-Tag: all');
            readfile($llms_file);
            exit;
        }
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
        
        // Whistler
        '/whistler-luxury-builder.html' => '/whistler-custom-homes/',
        '/whistler-luxury-builder/' => '/whistler-custom-homes/',
        '/whistler-luxury-builder' => '/whistler-custom-homes/',
        '/whistler-luxury-home-builder/' => '/whistler-custom-homes/',
        '/whistler-luxury-home-builder' => '/whistler-custom-homes/',
        
        // West Vancouver
        '/west-vancouver-custom-homes.html' => '/west-vancouver-custom-homes/',
        '/west-vancouver-luxury-builder/' => '/west-vancouver-custom-homes/',
        '/west-vancouver-luxury-builder' => '/west-vancouver-custom-homes/',
        
        // North Vancouver
        '/north-vancouver-home-builder/' => '/north-vancouver-custom-homes/',
        '/north-vancouver-home-builder' => '/north-vancouver-custom-homes/',
        
        // Feasibility Plan
        '/feasibility-study/' => '/feasibility-plan/',
        '/feasibility-study' => '/feasibility-plan/',
        
        // Articles / Blog
        '/blog/' => '/#articles',
        '/blog' => '/#articles',
        '/articles/' => '/#articles',
        '/articles' => '/#articles',
        
        // Obsolete peptide pages redirected to root
        '/cjc-1295-ipamorelin-glp-1-fatigue.html' => '/',
        '/mounjaro-muscle-loss.html' => '/',
        '/retatrutide-phase-3-data.html' => '/',
        '/wolverine-stack.html' => '/',
    );

    if (isset($redirects_301[$path])) {
        wp_redirect(home_url($redirects_301[$path]), 301);
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
// 1. Suppress Astra Default Footer Markup globally
remove_action('astra_footer', 'astra_footer_markup');

// 2. Render Unified Master Luxury Footer
add_action('wp_footer', 'keystone_possibilities_render_master_luxury_footer', 20);
function keystone_possibilities_render_master_luxury_footer() {
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
                    <a href="https://www.youtube.com/@KeystonePossibilities" target="_blank" rel="noopener noreferrer" class="kp-social-icon-btn" aria-label="YouTube Official Channel" style="width: 48px; height: 48px; min-width: 48px; min-height: 48px; border-radius: 50%; background: rgba(15, 23, 42, 0.85); border: 1.5px solid rgba(212, 175, 55, 0.35); color: #f6d365; display: inline-flex; align-items: center; justify-content: center; text-decoration: none !important; transition: all 0.25s ease; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    </a>

                    <!-- High-Converting YouTube Channel Subscribe Pill -->
                    <a href="https://www.youtube.com/@KeystonePossibilities?sub_confirmation=1" target="_blank" rel="noopener noreferrer" class="kp-subscribe-direct-btn" style="display: inline-flex; align-items: center; gap: 9px; min-height: 48px; background: linear-gradient(135deg, rgba(212, 175, 55, 0.18) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1.5px solid #d4af37; padding: 10px 22px; border-radius: 9999px; text-decoration: none !important; color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.22); transition: all 0.25s ease;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="#FF0000" style="filter: drop-shadow(0 0 6px rgba(255, 0, 0, 0.6)); flex-shrink: 0;"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                        <span>SUBSCRIBE &bull; @KeystonePossibilities</span>
                    </a>

                </div>
            </div>

            <!-- B. Centered High-End Copyright & Credentials -->
            <div style="margin-bottom: 32px; line-height: 1.6;">
                <p style="margin: 0 0 6px 0; color: #CBD5E1; font-weight: 500; font-size: 0.86rem; letter-spacing: 0.02em;">
                    Copyright &copy; 2023–2026 Keystone Possibilities Ltd &bull; All Rights Reserved.
                </p>
                <p style="margin: 0; color: #c5a059; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em;">
                    Certified BC Housing Residential Builder #52603 &bull; Fiduciary CCDC 5B Construction Management
                </p>
            </div>

            <!-- C. Regional Divisions & Specialized Services 4-Column Mesh (Unified Obsidian & Gold) -->
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 28px; margin-bottom: 24px; text-align: left;">
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
                        <a href="/north-vancouver-multiplex-conversions/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• North Vancouver Bill 44 Multiplex</a>
                        <a href="/west-vancouver-custom-homes/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• West Vancouver Steep Slope Builds</a>
                    </div>
                    <div>
                        <strong style="color: #ffffff; display: block; margin-bottom: 8px; font-size: 0.85rem;">Civil &amp; Fiduciary PM:</strong>
                        <a href="/bc-hydro-registered-civil-contractor/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• BC Hydro Civil Utility Contractor</a>
                        <a href="/feasibility-plan/" style="color: #94a3b8; text-decoration: none !important; display: block; margin-bottom: 5px; transition: color 0.2s ease;">• Construction Feasibility Studies</a>
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

            <!-- D. Standardized Keystone Empire Network Bar (Gold & Obsidian Continuity) -->
            <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 0.80rem; color: #94a3b8;">
                <div>
                    <span style="color: #d4af37; font-weight: 700; letter-spacing: 0.04em;">⚔️ KEYSTONE EMPIRE NETWORK</span> | Keystone Possibilities — BC Building Code &amp; Construction Consulting
                </div>
                <div>
                    Sister Flagship: <a href="https://keystonerecomposition.com/ai-protocols/" target="_blank" rel="noopener noreferrer" style="color: #f6d365; text-decoration: none !important; font-weight: 600;">Keystone Recomposition — Production AI Protocols, AI Music &amp; Lifestyle Investments &rarr;</a>
                </div>
            </div>

        </div>
    </footer>
    <a href="tel:+16048489688" class="keystone-mobile-call-bar" aria-label="Call Keystone Possibilities (604) 848-9688">
        <span>📞 (604) 848-9688</span>
    </a>
    <?php
}

// ── 6. Real-Time Brand Sanitization & Zero CSS Leak Filter ──────────────────
add_filter('the_content', 'keystone_possibilities_sanitize_content_output', 999);
function keystone_possibilities_sanitize_content_output($content) {
    if (is_front_page() || is_home() || (function_exists('get_the_ID') && get_the_ID() === 563)) {
        $search = array(
            'KEYSTONE RECOMPOSITION',
            'ks-recomposition-header',
            '#ks-recomposition-header',
            'KEYSTONE POSSIBILITY HELP TD'
        );
        $replace = array(
            'KEYSTONE POSSIBILITIES LTD',
            'ks-possibilities-header',
            '#ks-possibilities-header',
            'KEYSTONE POSSIBILITIES LTD — CLIENT &amp; CONSULTING SERVICES'
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
    </style>
    <?php
}

add_action('wp_footer', 'keystone_possibilities_mount_header_logo_script', 99);
function keystone_possibilities_mount_header_logo_script() {
    ?>
    <script id="keystone-mount-logo-engine">
    (function() {
        function injectLogo() {
            var left = document.querySelector('.site-header-primary-section-left-center');
            if (left && !left.querySelector('.brand-edge-logo')) {
                left.innerHTML = '<a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="brand-edge-logo" aria-label="Keystone Possibilities Ltd. Home">' +
                    '<div class="kp-badge-mark">' +
                    '<img src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png" alt="Keystone Possibilities Ltd." class="kp-badge-img">' +
                    '</div>' +
                    '<div class="brand-title-wrap">' +
                    '<span class="title-main">KEYSTONE POSSIBILITIES</span>' +
                    '<span class="title-sub">LICENSED BUILDER #52603</span>' +
                    '</div>' +
                    '</a>';
            }
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', injectLogo);
        } else {
            injectLogo();
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
