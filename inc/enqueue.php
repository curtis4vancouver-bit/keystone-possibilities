<?php
/**
 * Clean Asset Enqueue & Resource Hints — Keystone Possibilities v3.0
 * Eliminates 159.5 KB inline <head> CSS bloat via cacheable filemtime()-versioned stylesheets.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Adds preconnect hints for Google Fonts & YouTube-Nocookie poster delivery.
 *
 * @param array<int, string|array<string, mixed>> $urls          Resource hint URLs.
 * @param string                                  $relation_type Hint relation type.
 * @return array<int, string|array<string, mixed>>
 */
function kp_v3_resource_hints(array $urls, string $relation_type): array
{
    if ('preconnect' === $relation_type) {
        $urls[] = 'https://fonts.googleapis.com';
        $urls[] = array(
            'href'        => 'https://fonts.gstatic.com',
            'crossorigin' => 'anonymous',
        );
    }
    return $urls;
}
add_filter('wp_resource_hints', 'kp_v3_resource_hints', 10, 2);

/**
 * Helper to resolve cache-busting filemtime version string for child theme assets.
 *
 * @param string $rel_path Relative path inside child theme.
 * @return string
 */
function kp_v3_asset_ver(string $rel_path): string
{
    $abs = trailingslashit(get_stylesheet_directory()) . ltrim($rel_path, '/');
    if (file_exists($abs)) {
        $mtime = @filemtime($abs);
        if (is_int($mtime) && $mtime > 0) {
            return (string) $mtime;
        }
    }
    return '3.0.0';
}

/**
 * Enqueues v3.0 Quiet Luxury stylesheets & deferred interactive scripts.
 */
function kp_v3_enqueue_assets(): void
{
    $theme_uri = trailingslashit(get_stylesheet_directory_uri());
    $theme_dir = trailingslashit(get_stylesheet_directory());

    // 1. Typography: Cormorant Garamond, Outfit, Inter & JetBrains Mono
    wp_enqueue_style(
        'kp-google-fonts',
        'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Outfit:wght@500;600;700;800;900&display=swap',
        array(),
        null
    );

    // 2. Core Design System Stylesheets
    wp_enqueue_style(
        'kp-tokens-base',
        $theme_uri . 'assets/css/tokens-base.css',
        array('kp-google-fonts'),
        kp_v3_asset_ver('assets/css/tokens-base.css')
    );

    wp_enqueue_style(
        'kp-header-footer',
        $theme_uri . 'assets/css/header-footer.css',
        array('kp-tokens-base'),
        kp_v3_asset_ver('assets/css/header-footer.css')
    );

    wp_enqueue_style(
        'keystone-possibilities-child-style',
        get_stylesheet_uri(),
        array('kp-tokens-base', 'kp-header-footer'),
        kp_v3_asset_ver('style.css')
    );

    // Flagship Hero, Cinema, Portfolio Reels, 17-Cert Museum & Feasibility Calculator
    wp_enqueue_style(
        'kp-front-page',
        $theme_uri . 'assets/css/front-page.css',
        array('keystone-possibilities-child-style'),
        kp_v3_asset_ver('assets/css/front-page.css')
    );

    // Corridors, Technical Hubs, Partner Desk, Videos & Blog Editorial
    wp_enqueue_style(
        'kp-corridors-hubs',
        $theme_uri . 'assets/css/corridors-hubs.css',
        array('keystone-possibilities-child-style'),
        kp_v3_asset_ver('assets/css/corridors-hubs.css')
    );

    // Conditional Client Portal v10 Assets (Owned by Builder 2 — enqueue automatically if present)
    if (is_page('client-login')) {
        if (file_exists($theme_dir . 'assets/css/portal-v10.css')) {
            wp_enqueue_style(
                'kp-portal-v10',
                $theme_uri . 'assets/css/portal-v10.css',
                array('keystone-possibilities-child-style'),
                kp_v3_asset_ver('assets/css/portal-v10.css')
            );
        }
        if (file_exists($theme_dir . 'assets/js/portal-v10.js')) {
            wp_enqueue_script(
                'kp-portal-v10',
                $theme_uri . 'assets/js/portal-v10.js',
                array(),
                kp_v3_asset_ver('assets/js/portal-v10.js'),
                true
            );
            wp_localize_script('kp-portal-v10', 'kpPortalConfig', array(
                'jobsUrl' => esc_url_raw(rest_url('keystone/v1/portal-jobs')),
                'authUrl' => esc_url_raw(rest_url('keystone/v1/portal-auth')),
                'nonce'   => wp_create_nonce('wp_rest'),
            ));
        }
    }

    // 3. Deferred Frontend JS Modules
    wp_enqueue_script(
        'kp-navigation-ui',
        $theme_uri . 'assets/js/navigation-ui.js',
        array(),
        kp_v3_asset_ver('assets/js/navigation-ui.js'),
        true
    );

    wp_enqueue_script(
        'kp-estimator-calc',
        $theme_uri . 'assets/js/estimator-calc.js',
        array(),
        kp_v3_asset_ver('assets/js/estimator-calc.js'),
        true
    );

    wp_enqueue_script(
        'kp-lead-form',
        $theme_uri . 'assets/js/lead-form.js',
        array(),
        kp_v3_asset_ver('assets/js/lead-form.js'),
        true
    );

    wp_localize_script('kp-lead-form', 'keystoneData', array(
        'ajaxUrl'           => admin_url('admin-ajax.php'),
        'restUrl'           => esc_url_raw(rest_url('keystone/v1/lead')),
        'geocodeRestUrl'    => esc_url_raw(rest_url('keystone/v1/geocode')),
        'portalJobsRestUrl' => esc_url_raw(rest_url('keystone/v1/portal-jobs')),
        'portalAuthRestUrl' => esc_url_raw(rest_url('keystone/v1/portal-auth')),
    ));

    wp_enqueue_script(
        'keystone-lazy-player',
        $theme_uri . 'js/lazy-player.js',
        array(),
        kp_v3_asset_ver('js/lazy-player.js'),
        true
    );

    wp_enqueue_script(
        'keystone-portfolio-carousel',
        $theme_uri . 'js/portfolio-carousel.js',
        array(),
        kp_v3_asset_ver('js/portfolio-carousel.js'),
        true
    );
}
add_action('wp_enqueue_scripts', 'kp_v3_enqueue_assets', 20);
