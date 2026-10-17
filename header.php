<?php
/**
 * The header for Keystone Possibilities Child Theme.
 * Certified BC Housing Builder #52603 — Architectural Dark Quiet Luxury
 *
 * @package KeystonePossibilitiesChild
 * @version 2.6.0
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, interactive-widget=resizes-content">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Inter:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
    <?php wp_head(); ?>
</head>
<body <?php body_class( 'keystone-possibilities-dark-luxury' ); ?>>
<?php wp_body_open(); ?>

<?php
if ( ! defined( 'KP_HEADER_RENDERED' ) ) {
    define( 'KP_HEADER_RENDERED', true );
}
?>
<div id="page" class="hfeed site">

    <!-- COMPACT SITE NAVIGATION HEADER (Slim 52px Single-Row on Mobile, Full Luxury Bar on Desktop) -->
    <header class="site-nav-header" id="kpSiteNavHeader">
        <div class="nav-container">
            
            <!-- Wayne's Real Logo Branding on Left Edge -->
            <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="brand-edge-logo" aria-label="Keystone Possibilities Ltd. Home">
                <div class="kp-badge-mark">
                    <img src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png" alt="Keystone Possibilities Ltd." class="kp-badge-img">
                </div>
                <div class="brand-title-wrap">
                    <span class="title-main">KEYSTONE POSSIBILITIES</span>
                    <span class="title-sub">LICENSED BUILDER #52603</span>
                </div>
            </a>

            <!-- Desktop Navigation Menu (Wayne's Exact Requested Order & Shortened Labels) -->
            <nav aria-label="Main Navigation" class="kp-desktop-nav-wrap">
                <ul class="nav-links-menu">
                    <li><a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="nav-link-item <?php echo is_front_page() ? 'active' : ''; ?>">HOME</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>" class="nav-link-item <?php echo is_page( 'feasibility-plan' ) ? 'active' : ''; ?>">CUSTOM BUILD &amp; COST PLAN</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/client-login/' ) ); ?>" class="nav-link-item <?php echo is_page( 'client-login' ) ? 'active' : ''; ?>">CLIENT LOGIN</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/keystone-possibilities-custom-homes/' ) ); ?>" class="nav-link-item <?php echo is_page( 'keystone-possibilities-custom-homes' ) ? 'active' : ''; ?>">MASTER BUILDER SERIES</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/portfolio-general-contractor-squamish/' ) ); ?>" class="nav-link-item <?php echo is_page( 'portfolio-general-contractor-squamish' ) ? 'active' : ''; ?>">PORTFOLIO</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/about-us-general-contractor-squamish/' ) ); ?>" class="nav-link-item <?php echo is_page( 'about-us-general-contractor-squamish' ) ? 'active' : ''; ?>">ABOUT US</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/private-investors/' ) ); ?>" class="nav-link-item <?php echo is_page( 'private-investors' ) ? 'active' : ''; ?>">PRIVATE INVESTORS</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/bc-hydro-registered-civil-contractor/' ) ); ?>" class="nav-link-item <?php echo is_page( 'bc-hydro-registered-civil-contractor' ) ? 'active' : ''; ?>">CIVIL</a></li>
                    <li><a href="<?php echo esc_url( home_url( '/contact-general-contractor-squamish/' ) ); ?>" class="nav-link-item <?php echo is_page( 'contact-general-contractor-squamish' ) ? 'active' : ''; ?>">CONTACT</a></li>
                </ul>
            </nav>

            <!-- Right Action Items (Social Icons on Desktop + High-Contrast ☰ MENU ▾ Pill on Mobile) -->
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

    <!-- MOBILE NAVIGATION DRAWER (Scrollable Dropdown with Highlighted Custom Build & Cost Plan Card at Top) -->
    <div class="mobile-menu-drawer" id="mobileDrawer" aria-label="Mobile Navigation Drawer">
        <a href="<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>" class="mobile-drawer-featured-cta">
            <span class="drawer-cta-badge">⭐ FEATURED BUILDER TOOL · LICENSE #52603</span>
            <span class="drawer-cta-title">📐 CUSTOM BUILD &amp; COST PLAN — Custom Homes (#52603) &amp; BC Hydro Civil (ES54)</span>
            <span class="drawer-cta-sub">Interactive Lot Feasibility, Cost Breakdown &amp; Civil Scope Calculator →</span>
        </a>
        <a href="<?php echo esc_url( home_url( '/' ) ); ?>" class="mobile-drawer-link <?php echo is_front_page() ? 'active' : ''; ?>">🏠 HOME</a>
        <a href="<?php echo esc_url( home_url( '/client-login/' ) ); ?>" class="mobile-drawer-link">🔐 CLIENT LOGIN</a>
        <a href="<?php echo esc_url( home_url( '/keystone-possibilities-custom-homes/' ) ); ?>" class="mobile-drawer-link">🎬 MASTER BUILDER SERIES</a>
        <a href="<?php echo esc_url( home_url( '/portfolio-general-contractor-squamish/' ) ); ?>" class="mobile-drawer-link">🏛️ PORTFOLIO</a>
        <a href="<?php echo esc_url( home_url( '/about-us-general-contractor-squamish/' ) ); ?>" class="mobile-drawer-link">👤 ABOUT US</a>
        <a href="<?php echo esc_url( home_url( '/private-investors/' ) ); ?>" class="mobile-drawer-link">📈 PRIVATE INVESTORS</a>
        <a href="<?php echo esc_url( home_url( '/bc-hydro-registered-civil-contractor/' ) ); ?>" class="mobile-drawer-link">⚡ CIVIL (ES54)</a>
        <a href="<?php echo esc_url( home_url( '/contact-general-contractor-squamish/' ) ); ?>" class="mobile-drawer-link">📞 CONTACT — (604) 848-9688</a>
    </div>

    <div id="content" class="site-content">
