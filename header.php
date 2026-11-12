<?php
/**
 * Sovereign Quiet-Luxury Site Header — Keystone Possibilities v3.0
 * BC Housing Licensed Residential Builder #52603 · BC Hydro ES54 Civil Contractor
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

$kp_logos     = function_exists('kp_get_official_logos') ? kp_get_official_logos() : array();
$kp_badge_url = $kp_logos['header_badge'] ?? 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';
$kp_corridors = function_exists('kp_get_corridors') ? kp_get_corridors() : array();
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <?php wp_head(); ?>
</head>
<body <?php body_class('kp-sovereign-v3'); ?>>
<?php wp_body_open(); ?>

<a class="kp-skip-link" href="#primary">Skip to main content</a>

<!-- 1. TOP STATUTORY CREDENTIAL & DIRECT CONTACT UTILITY STRIP -->
<div class="kp-utility-bar" role="region" aria-label="Builder Licence and Direct Contact">
    <div class="kp-container kp-utility-inner">
        <div class="kp-utility-left">
            <span class="kp-utility-dot" aria-hidden="true"></span>
            <span>BC HOUSING #52603 &middot; BC HYDRO ES54 CIVIL &middot; 2-5-10 WARRANTY &middot; OPEN-BOOK CCDC 5B</span>
        </div>
        <div class="kp-utility-right">
            <a href="https://www.youtube.com/@KeystonePossibilitiesLtd" target="_blank" rel="noopener noreferrer" class="kp-utility-yt" aria-label="Keystone Possibilities Official YouTube Channel">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                <span>@KeystonePossibilitiesLtd</span>
            </a>
            <a href="tel:+16048489688" class="kp-utility-phone" id="ks-top-help-td">
                <span aria-hidden="true">&#128222;</span> (604) 848-9688
            </a>
            <a href="<?php echo esc_url(home_url('/client-login/')); ?>" class="kp-utility-login-pill">
                Client Login
            </a>
        </div>
    </div>
</div>

<!-- 2. PRIMARY STICKY QUIET-LUXURY NAVIGATION BAR -->
<header class="kp-site-header site-header" id="ks-possibilities-header">
    <div class="kp-container kp-header-inner">
        <a href="<?php echo esc_url(home_url('/')); ?>" class="brand-edge-logo" aria-label="Keystone Possibilities Ltd. Home">
            <div class="kp-badge-mark">
                <img src="<?php echo esc_url($kp_badge_url); ?>" alt="Keystone Possibilities Ltd. Keyhole-Arch Shield" class="kp-badge-img" width="44" height="44" decoding="async">
            </div>
            <div class="brand-title-wrap">
                <span class="title-main">KEYSTONE POSSIBILITIES</span>
                <span class="title-sub">LICENSED BUILDER #52603</span>
            </div>
        </a>

        <nav class="kp-primary-nav" aria-label="Primary Navigation">
            <ul class="kp-nav-list">
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/')); ?>" class="kp-nav-link <?php echo is_front_page() ? 'is-active' : ''; ?>">Home</a>
                </li>
                <li class="kp-nav-item kp-nav-item--has-dropdown">
                    <button type="button" class="kp-nav-link" data-kp-dropdown-toggle aria-expanded="false" aria-haspopup="true">
                        Corridors <span aria-hidden="true">&#9662;</span>
                    </button>
                    <div class="kp-corridors-dropdown" role="menu" aria-label="9 BC Service Corridors">
                        <span class="kp-dropdown-kicker">9 BC Construction &amp; SSMUH Corridors</span>
                        <div class="kp-dropdown-grid">
                            <?php foreach ($kp_corridors as $corridor) : ?>
                                <a href="<?php echo esc_url(home_url((string) $corridor['url'])); ?>" class="kp-dropdown-link" role="menuitem">
                                    <strong><?php echo esc_html((string) $corridor['short_name']); ?></strong>
                                    <span>$<?php echo esc_html((string) ($corridor['cost_band_sf'][0] ?? '450')); ?>–$<?php echo esc_html((string) ($corridor['cost_band_sf'][1] ?? '750')); ?>/sf</span>
                                </a>
                            <?php endforeach; ?>
                        </div>
                    </div>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/keystone-possibilities-custom-homes/')); ?>" class="kp-nav-link <?php echo is_page('keystone-possibilities-custom-homes') ? 'is-active' : ''; ?>">Master Series</a>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/portfolio-general-contractor-squamish/')); ?>" class="kp-nav-link <?php echo is_page('portfolio-general-contractor-squamish') ? 'is-active' : ''; ?>">Portfolio</a>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/bc-hydro-registered-civil-contractor/')); ?>" class="kp-nav-link <?php echo is_page('bc-hydro-registered-civil-contractor') ? 'is-active' : ''; ?>">ES54 Civil</a>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/realtor-architect-desk/')); ?>" class="kp-nav-link <?php echo is_page('realtor-architect-desk') ? 'is-active' : ''; ?>">Realtor &amp; Architect Desk</a>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/about-us-general-contractor-squamish/')); ?>" class="kp-nav-link <?php echo is_page('about-us-general-contractor-squamish') ? 'is-active' : ''; ?>">About &amp; Certs</a>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/private-investors/')); ?>" class="kp-nav-link <?php echo is_page('private-investors') ? 'is-active' : ''; ?>">Investors</a>
                </li>
                <li class="kp-nav-item">
                    <a href="<?php echo esc_url(home_url('/contact-general-contractor-squamish/')); ?>" class="kp-nav-link <?php echo is_page('contact-general-contractor-squamish') ? 'is-active' : ''; ?>">Contact</a>
                </li>
            </ul>
        </nav>

        <div class="kp-header-actions">
            <a href="<?php echo esc_url(home_url('/feasibility-plan/')); ?>" class="kp-header-cta">
                48-Hr Lot &amp; Cost Plan &rarr;
            </a>
            <button type="button" class="kp-mobile-toggle" id="kpMobileNavToggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="kpMobileNavDrawer">
                &#9776; Menu
            </button>
        </div>
    </div>
</header>

<!-- 3. MOBILE NAVIGATION DRAWER (#kpMobileNavDrawer) -->
<div class="kp-mobile-drawer-backdrop" id="kpMobileNavBackdrop" aria-hidden="true"></div>
<aside class="kp-mobile-drawer" id="kpMobileNavDrawer" aria-label="Mobile Navigation Drawer" aria-hidden="true">
    <div class="kp-drawer-top">
        <span class="kp-dropdown-kicker" style="border:0;padding:0;margin:0;">KEYSTONE POSSIBILITIES #52603</span>
        <button type="button" class="kp-lightbox-close" id="kpMobileNavClose" aria-label="Close navigation menu">&times;</button>
    </div>

    <a href="<?php echo esc_url(home_url('/feasibility-plan/')); ?>" class="kp-drawer-cta-card">
        <strong>48-Hr Lot &amp; Cost Feasibility Plan &rarr;</strong>
        <span>Interactive Custom Build, Bill 44 SSMUH &amp; ES54 Civil Scope Engine</span>
    </a>

    <nav class="kp-drawer-links" aria-label="Mobile Primary Links">
        <a href="<?php echo esc_url(home_url('/')); ?>" class="kp-drawer-link"><span>Home</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/keystone-possibilities-custom-homes/')); ?>" class="kp-drawer-link"><span>Master Series</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/portfolio-general-contractor-squamish/')); ?>" class="kp-drawer-link"><span>9-Residence Portfolio</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/bc-hydro-registered-civil-contractor/')); ?>" class="kp-drawer-link"><span>BC Hydro ES54 Civil</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/realtor-architect-desk/')); ?>" class="kp-drawer-link"><span>Realtor &amp; Architect Desk</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/about-us-general-contractor-squamish/')); ?>" class="kp-drawer-link"><span>About Wayne &amp; 17 Certificates</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/videos/')); ?>" class="kp-drawer-link"><span>Engineering Video Briefings</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/private-investors/')); ?>" class="kp-drawer-link"><span>Private Investors</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/client-login/')); ?>" class="kp-drawer-link"><span>Client Portal Login</span><span>&rarr;</span></a>
        <a href="<?php echo esc_url(home_url('/contact-general-contractor-squamish/')); ?>" class="kp-drawer-link"><span>Contact &middot; (604) 848-9688</span><span>&rarr;</span></a>
    </nav>

    <div>
        <span class="kp-dropdown-kicker">9 BC Service Corridors</span>
        <div class="kp-drawer-corridors-grid">
            <?php foreach ($kp_corridors as $corridor) : ?>
                <a href="<?php echo esc_url(home_url((string) $corridor['url'])); ?>" class="kp-drawer-corridor-chip">
                    <?php echo esc_html((string) $corridor['short_name']); ?>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
</aside>

<main id="primary" class="kp-site-main">
