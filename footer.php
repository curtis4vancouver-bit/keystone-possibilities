<?php
/**
 * Sovereign Quiet-Luxury Site Footer & Accessible Asset Lightbox — Keystone Possibilities v3.0
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

$kp_logos       = function_exists('kp_get_official_logos') ? kp_get_official_logos() : array();
$kp_full_lockup = $kp_logos['full_lockup'] ?? 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_full_logo_gold_transparent.png';
$kp_corridors   = function_exists('kp_get_corridors') ? kp_get_corridors() : array();
?>
</main><!-- #primary -->

<footer class="kp-site-footer" id="kp-master-luxury-footer">
    <div class="kp-container">
        <div class="kp-footer-grid">
            <!-- Column 1: Full Gold Transparent Lockup + Squamish HQ -->
            <div>
                <a href="<?php echo esc_url(home_url('/')); ?>" aria-label="Keystone Possibilities Ltd. Home">
                    <img src="<?php echo esc_url($kp_full_lockup); ?>" alt="Keystone Possibilities Ltd. — Licensed BC Residential Builder #52603" class="kp-footer-lockup-img" width="126" height="115" loading="lazy" decoding="async">
                </a>
                <p style="margin:0;font-size:0.84rem;line-height:1.6;color:var(--text-secondary);">
                    Principal-supervised architectural custom residences, Bill 44 SSMUH multiplexes, and self-performed BC Hydro ES54 underground civil infrastructure under 100% open-book CCDC 5B contracts.
                </p>
                <div class="kp-footer-hq-meta">
                    <span><strong style="color:var(--text-ivory);">Squamish HQ:</strong> 1 Watts Point Road, Squamish, BC V8B 0B1</span>
                    <span><strong style="color:var(--text-ivory);">Direct Line:</strong> <a href="tel:+16048489688">(604) 848-9688</a></span>
                    <span><strong style="color:var(--text-ivory);">Desk Email:</strong> <a href="mailto:info@keystonepossibilities.ca">info@keystonepossibilities.ca</a></span>
                </div>
                <a href="https://www.youtube.com/@KeystonePossibilitiesLtd" target="_blank" rel="noopener noreferrer" class="kp-footer-yt-pill">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    <span>@KeystonePossibilitiesLtd</span>
                </a>
            </div>

            <!-- Column 2: All 9 BC Construction Corridors -->
            <div>
                <h3 class="kp-footer-col-title">9 BC Service Corridors</h3>
                <ul class="kp-footer-list">
                    <?php foreach ($kp_corridors as $corridor) : ?>
                        <li>
                            <a href="<?php echo esc_url(home_url((string) $corridor['url'])); ?>">
                                <?php echo esc_html((string) $corridor['short_name']); ?> Custom Homes
                            </a>
                        </li>
                    <?php endforeach; ?>
                </ul>
            </div>

            <!-- Column 3: Technical, Feasibility & Partner Hubs -->
            <div>
                <h3 class="kp-footer-col-title">Technical &amp; Partner Hubs</h3>
                <ul class="kp-footer-list">
                    <li><a href="<?php echo esc_url(home_url('/feasibility-plan/')); ?>">48-Hr Lot &amp; Cost Feasibility Plan</a></li>
                    <li><a href="<?php echo esc_url(home_url('/realtor-architect-desk/')); ?>">Realtor &amp; Architect Desk (Rule 5-11)</a></li>
                    <li><a href="<?php echo esc_url(home_url('/bc-developer-portal/')); ?>">BC Bill 44 &amp; Step Code 5 Portal</a></li>
                    <li><a href="<?php echo esc_url(home_url('/bc-hydro-registered-civil-contractor/')); ?>">BC Hydro ES54 Civil Contracting</a></li>
                    <li><a href="<?php echo esc_url(home_url('/portfolio-general-contractor-squamish/')); ?>">Signature 9-Residence Portfolio</a></li>
                    <li><a href="<?php echo esc_url(home_url('/about-us-general-contractor-squamish/')); ?>">Wayne Stevenson &amp; 17 Credentials</a></li>
                    <li><a href="<?php echo esc_url(home_url('/industry-partners/')); ?>">Verified EGBC &amp; AIBC Partners</a></li>
                    <li><a href="<?php echo esc_url(home_url('/videos/')); ?>">Engineering Video Briefings</a></li>
                    <li><a href="<?php echo esc_url(home_url('/client-login/')); ?>">24/7 Client Portal Login</a></li>
                    <li><a href="<?php echo esc_url(home_url('/privacy-policy/')); ?>">Privacy Policy</a></li>
                </ul>
            </div>

            <!-- Column 4: Statutory Standing & Keystone Empire Sister Credit -->
            <div>
                <h3 class="kp-footer-col-title">Statutory Registrations</h3>
                <ul class="kp-footer-list" style="margin-bottom:18px;">
                    <li>BC Housing Licensed Builder <strong style="color:var(--text-ivory);">#52603</strong></li>
                    <li>BC Hydro Civil Registry <strong style="color:var(--text-ivory);">List ES54</strong></li>
                    <li>WorkSafeBC Clearance <strong style="color:var(--text-ivory);">#201703481</strong></li>
                    <li>Statutory 2-5-10 Home Warranty</li>
                    <li>Open-Book CCDC 5B Fiduciary Ledger</li>
                </ul>

                <div class="kp-empire-card">
                    <h4>Keystone Empire Ecosystem</h4>
                    <p>Explore our sister evidence-based performance &amp; sovereign engineering division.</p>
                    <a href="https://keystonerecomposition.com/" target="_blank" rel="noopener" class="kp-empire-link">
                        Keystone Recomposition &rarr;
                    </a>
                </div>
            </div>
        </div>

        <div class="kp-footer-bottom">
            <span>&copy; 2023&ndash;<?php echo esc_html(gmdate('Y')); ?> Keystone Possibilities Ltd. All Rights Reserved.</span>
            <span>Principal Superintendent: Wayne Stevenson &middot; BC Housing #52603 &middot; Squamish, British Columbia</span>
        </div>
    </div>
</footer>

<!-- Shared Accessible High-Resolution Asset & Gallery Lightbox Modal -->
<div class="kp-lightbox-backdrop" id="kpLightboxModal" role="dialog" aria-modal="true" aria-hidden="true" aria-labelledby="kpLightboxTitle">
    <div class="kp-lightbox-dialog">
        <div class="kp-lightbox-topbar">
            <div>
                <h3 class="kp-lightbox-title" id="kpLightboxTitle" data-kp-lightbox-title>Keystone Possibilities — Verified Asset</h3>
                <p class="kp-lightbox-sub" data-kp-lightbox-sub></p>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <button type="button" class="kp-reel-arrow" data-kp-lightbox-prev aria-label="Previous image" style="display:none;">&larr;</button>
                <button type="button" class="kp-reel-arrow" data-kp-lightbox-next aria-label="Next image" style="display:none;">&rarr;</button>
                <button type="button" class="kp-lightbox-close" data-kp-lightbox-close aria-label="Close modal">&times;</button>
            </div>
        </div>
        <div class="kp-lightbox-stage">
            <img src="" alt="" data-kp-lightbox-img loading="lazy" decoding="async">
        </div>
        <div class="kp-lightbox-thumbs" data-kp-lightbox-thumbs style="display:none;"></div>
    </div>
</div>

<?php wp_footer(); ?>
</body>
</html>
