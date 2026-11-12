<?php
/**
 * Single-Hop 301 Canonical Redirects & HTTP 410 Gone De-Indexing Engine — v3.0
 *
 * - Keeps /videos/ live (HTTP 200 Page 1245 — ZERO redirect to custom-homes!).
 * - Maps all 11 /watch-[slug]/ pages + duplicate -2 slugs single-hop to /videos/[slug]/.
 * - Consolidates legacy regional/service slugs without multi-hop chains.
 * - Serves clean HTTP 410 Gone for retired/off-vertical URLs.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Returns the canonical single-hop 301 redirect lookup map (normalized path => target path).
 *
 * @return array<string, string>
 */
function kp_get_canonical_301_map(): array
{
    return array(
        // 11 Canonical Watch Pages -> /videos/[slug]/ (including full legacy slugs)
        '/watch-sea-to-sky-luxury-compounds-bc-building-code'                          => '/videos/sea-to-sky-luxury-compounds-bc-building-code/',
        '/watch-why-4-storey-multiplexes-fail-lateral-shear'                           => '/videos/why-4-storey-multiplexes-fail-lateral-shear/',
        '/watch-west-vancouver-whistler-step-code-5-cantilever-seismic'                => '/videos/west-vancouver-whistler-step-code-5-cantilever-seismic/',
        '/watch-west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide' => '/videos/west-vancouver-whistler-step-code-5-cantilever-seismic/',
        '/watch-vancouver-multiplex-bcbc-2024-fire-acoustic-water-main'                => '/videos/vancouver-multiplex-bcbc-2024-fire-acoustic-water-main/',
        '/watch-vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide'          => '/videos/vancouver-multiplex-bcbc-2024-fire-acoustic-water-main/',
        '/watch-vancouver-multiplex-bcbc-2024-adaptable-sill-micropile'                => '/videos/vancouver-multiplex-bcbc-2024-adaptable-sill-micropile/',
        '/watch-vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide'          => '/videos/vancouver-multiplex-bcbc-2024-adaptable-sill-micropile/',
        '/watch-bcbc-2024-basement-waterproofing-hydrostatic-radon'                    => '/videos/bcbc-2024-basement-waterproofing-hydrostatic-radon/',
        '/watch-bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide'       => '/videos/bcbc-2024-basement-waterproofing-hydrostatic-radon/',
        '/watch-hydronic-radiant-floor-erv-engineering'                                => '/videos/hydronic-radiant-floor-erv-engineering/',
        '/watch-inverted-roof-terraces-bc'                                             => '/videos/inverted-roof-terraces-bc/',
        '/watch-net-zero-envelopes-bc'                                                 => '/videos/net-zero-envelopes-bc/',
        '/watch-architectural-concrete-bc'                                             => '/videos/architectural-concrete-bc/',
        '/watch-estate-microgrids-bc'                                                  => '/videos/estate-microgrids-bc/',

        // Duplicate -2 Watch Slugs & Short Watch Aliases -> Single-Hop to /videos/[slug]/
        '/watch-architectural-concrete-bc-2'                        => '/videos/architectural-concrete-bc/',
        '/watch-estate-microgrids-bc-2'                             => '/videos/estate-microgrids-bc/',
        '/watch-sea-to-sky-luxury-compounds'                        => '/videos/sea-to-sky-luxury-compounds-bc-building-code/',
        '/watch-why-4-storey-multiplexes-fail'                      => '/videos/why-4-storey-multiplexes-fail-lateral-shear/',
        '/watch-west-vancouver-step-code-5'                         => '/videos/west-vancouver-whistler-step-code-5-cantilever-seismic/',
        '/watch-vancouver-multiplex-fire-acoustic'                  => '/videos/vancouver-multiplex-bcbc-2024-fire-acoustic-water-main/',
        '/watch-vancouver-multiplex-adaptable-micropile'            => '/videos/vancouver-multiplex-bcbc-2024-adaptable-sill-micropile/',
        '/watch-bcbc-2024-basement-waterproofing'                   => '/videos/bcbc-2024-basement-waterproofing-hydrostatic-radon/',

        // Consolidated Service & Corridor Pages (Single-Hop)
        '/west-vancouver-luxury-renovations'                        => '/west-vancouver-custom-homes/',
        '/north-vancouver-multiplex-conversions'                    => '/north-vancouver-custom-homes/',
        '/project-management-wp'                                    => '/feasibility-plan/',
        '/feasibility-retainer'                                     => '/feasibility-plan/',
        '/services-general-contractor-squamish'                     => '/keystone-possibilities-custom-homes/',
        '/credentials'                                              => '/about-us-general-contractor-squamish/#credentials',
        '/contact'                                                  => '/contact-general-contractor-squamish/',
        '/about'                                                    => '/about-us-general-contractor-squamish/',
        '/about-us'                                                 => '/about-us-general-contractor-squamish/',
        '/portfolio'                                                => '/portfolio-general-contractor-squamish/',
        '/squamish-general-contractor'                              => '/squamish-custom-homes/',
        '/squamish-custom-home-builder'                             => '/squamish-custom-homes/',
        '/squamish'                                                 => '/squamish-custom-homes/',
        '/whistler-luxury-builder'                                  => '/whistler-custom-homes/',
        '/whistler'                                                 => '/whistler-custom-homes/',
        '/vancouver-multiplex'                                      => '/vancouver-r1-1-multiplex-builder/',
        '/vancouver-multiplex-development'                          => '/vancouver-r1-1-multiplex-builder/',
        '/coquitlam-custom-homes'                                   => '/coquitlam-custom-homes-multiplex/',
        '/client-portal'                                            => '/client-login/',
        '/client-portal-demo'                                       => '/client-login/',
        '/client-portal-2'                                          => '/client-login/',

        // Legacy Static .html Paths
        '/index.html'                                               => '/',
        '/about-us-general-contractor-squamish.html'                => '/about-us-general-contractor-squamish/',
        '/west-vancouver-custom-homes.html'                         => '/west-vancouver-custom-homes/',
        '/whistler-custom-homes.html'                               => '/whistler-custom-homes/',
        '/squamish-custom-homes.html'                               => '/squamish-custom-homes/',
        '/north-vancouver-custom-homes.html'                        => '/north-vancouver-custom-homes/',
        '/portfolio-general-contractor-squamish.html'               => '/portfolio-general-contractor-squamish/',
        '/contact-general-contractor-squamish.html'                 => '/contact-general-contractor-squamish/',
    );
}

/**
 * Returns normalized URL paths or prefixes that must immediately return HTTP 410 Gone.
 *
 * @return array<int, string>
 */
function kp_get_410_gone_paths(): array
{
    return array(
        '/sample-page',
        '/hello-world',
        '/elementor-hf',
    );
}

/**
 * Executes single-hop 301 redirects and HTTP 410 Gone responses at template_redirect priority 1.
 */
function kp_execute_redirects_and_410(): void
{
    if (is_admin() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST)) {
        return;
    }

    $uri = $_SERVER['REQUEST_URI'] ?? '';
    if ($uri === '') {
        return;
    }

    $raw_path = (string) strtok($uri, '?');
    $norm_path = '/' . trim(strtolower($raw_path), '/');
    if ($norm_path === '//') {
        $norm_path = '/';
    }

    // 1. Exact Single-Hop 301 Redirect Map
    $redirect_map = kp_get_canonical_301_map();
    if (isset($redirect_map[$norm_path])) {
        $target = home_url($redirect_map[$norm_path]);
        wp_redirect($target, 301, 'Keystone-Sovereign-v3');
        exit;
    }

    // Generic fallback for any legacy .html request not in explicit map
    if (substr($norm_path, -5) === '.html') {
        $stripped = substr($norm_path, 0, -5);
        $target_rel = $redirect_map[$stripped] ?? ($stripped . '/');
        wp_redirect(home_url($target_rel), 301, 'Keystone-Sovereign-v3');
        exit;
    }

    // 2. HTTP 410 Gone De-Indexing Check
    $is_410 = in_array($norm_path, kp_get_410_gone_paths(), true);
    if (!$is_410 && preg_match('#/(cjc-1295|mounjaro-muscle|retatrutide-phase|wolverine-stack)#i', $norm_path)) {
        $is_410 = true;
    }

    if ($is_410) {
        status_header(410);
        nocache_headers();
        header('X-Robots-Tag: noindex, nofollow', true);

        $tpl_410 = trailingslashit(get_stylesheet_directory()) . '410.php';
        if (file_exists($tpl_410)) {
            include $tpl_410;
            exit;
        }

        echo '<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><title>410 Gone — Keystone Possibilities Ltd.</title>';
        echo '<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#04070d;color:#f8fafc;font-family:Inter,system-ui,sans-serif;padding:24px}.card{max-width:560px;padding:36px;border-radius:18px;background:#0d1526;border:1px solid rgba(212,175,55,0.35);text-align:center}h1{margin:0 0 12px;font-size:1.6rem;color:#f3d98b}p{color:#cbd5e1;line-height:1.6;margin:0 0 22px}a{display:inline-block;padding:11px 24px;border-radius:999px;background:#d4af37;color:#04070d;font-weight:700;text-decoration:none}</style></head>';
        echo '<body><main class="card"><h1>410 — Resource Permanently Removed</h1><p>This legacy URL has been permanently retired. Explore Keystone Possibilities Ltd. custom home construction, Bill 44 multiplex engineering, and BC Hydro ES54 civil contracting below.</p><a href="' . esc_url(home_url('/')) . '">Return to Keystone Possibilities &rarr;</a></main></body></html>';
        exit;
    }
}
