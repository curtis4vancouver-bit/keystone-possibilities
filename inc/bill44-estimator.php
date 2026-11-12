<?php
/**
 * Keystone Possibilities v3.0 — 9-Corridor Lot & Cost Engine + CCDC 5B Savings Shortcodes
 *
 * Provides:
 * 1. [keystone_bill44_estimator] / [keystone_custom_build_planner] — Interactive 9-Corridor
 *    Custom Estate, BC Bill 44 SSMUH Multiplex & BC Hydro ES54 Civil Cost Estimator
 *    wired to `assets/js/estimator-calc.js` and `assets/js/lead-form.js` (zero inline CSS/JS bloat).
 * 2. [keystone_open_book_calculator] — Interactive CCDC 5B Open-Book Fee Savings Slider.
 *
 * Note: The BC Address Geocoder REST proxy (`/wp-json/keystone/v1/geocode`) is registered
 * once in `inc/portal-api-v10.php` to guarantee zero duplicate route registration.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Backwards-compatible wrapper delegating to `kp_handle_bc_geocoder_proxy` if called directly.
 *
 * @param WP_REST_Request $request Incoming REST request.
 * @return WP_REST_Response
 */
function keystone_possibilities_handle_geocode_proxy(WP_REST_Request $request): WP_REST_Response
{
    if (function_exists('kp_rest_bc_address_geocode')) {
        return kp_rest_bc_address_geocode($request);
    }
    if (function_exists('kp_handle_bc_geocoder_proxy')) {
        return kp_handle_bc_geocoder_proxy($request);
    }
    return new WP_REST_Response(array('results' => array(), 'features' => array()), 200);
}

/**
 * Renders the 9-Corridor Custom Home, Bill 44 SSMUH & BC Hydro ES54 Feasibility Estimator.
 *
 * @param array<string, mixed>|string $atts Shortcode attributes (`corridor` default `'west-vancouver'`).
 * @return string
 */
function keystone_possibilities_bill44_estimator_shortcode($atts = array()): string
{
    $parsed           = is_array($atts) ? $atts : array();
    $default_corridor = isset($parsed['corridor']) ? sanitize_key((string) $parsed['corridor']) : 'west-vancouver';
    $corridors        = function_exists('kp_get_corridors') ? kp_get_corridors() : array();

    ob_start();
    ?>
    <div class="kp-feasibility-grid" data-kp-estimator data-default-corridor="<?php echo esc_attr($default_corridor); ?>">
        <div class="kp-calc-panel">
            <span class="kp-eyebrow">Interactive 9-Corridor Pre-Construction Engine</span>
            <h3 class="kp-section-title">Model Hard Costs, Bill 44 Units &amp; ES54 Servicing</h3>
            <p class="kp-section-lead">Select your BC municipality, project archetype, and planned square footage to benchmark 2026 CCDC 5B open-book construction ranges.</p>

            <div class="kp-field" style="margin-top: 18px;">
                <label class="kp-label" for="kp-est-corridor-select">1. Select BC Corridor</label>
                <select id="kp-est-corridor-select" class="kp-select" data-kp-est-corridor>
                    <?php if (!empty($corridors)) : ?>
                        <?php foreach ($corridors as $slug => $c) : ?>
                            <option value="<?php echo esc_attr($slug); ?>" <?php selected($slug, $default_corridor); ?>>
                                <?php echo esc_html($c['short_name']); ?> ($<?php echo (int) $c['cost_band_sf'][0]; ?>–$<?php echo (int) $c['cost_band_sf'][1]; ?>/SF)
                            </option>
                        <?php endforeach; ?>
                    <?php else : ?>
                        <option value="west-vancouver">West Vancouver ($650–$980/SF)</option>
                        <option value="whistler">Whistler ($680–$1,050/SF)</option>
                        <option value="squamish">Squamish HQ ($450–$680/SF)</option>
                        <option value="north-vancouver">North Vancouver ($475–$720/SF)</option>
                        <option value="vancouver-r1-1">Vancouver R1-1 ($430–$620/SF)</option>
                    <?php endif; ?>
                </select>
            </div>

            <div class="kp-field" style="margin-top: 14px;">
                <span class="kp-label">2. Select Build Archetype</span>
                <div class="kp-calc-option-grid">
                    <button type="button" class="kp-calc-option is-selected" data-kp-est-type="custom-estate">Custom Estate</button>
                    <button type="button" class="kp-calc-option" data-kp-est-type="bill44-multiplex">Bill 44 Multiplex</button>
                    <button type="button" class="kp-calc-option" data-kp-est-type="steep-slope-alpine">Steep-Slope / Alpine</button>
                </div>
            </div>

            <div class="kp-field" style="margin-top: 14px;">
                <label class="kp-label" for="kp-est-sqft-range">
                    3. Planned Gross Floor Area: <strong data-kp-est-sqft-val style="color: var(--gold-light);">4,200 sq. ft.</strong>
                </label>
                <input type="range" id="kp-est-sqft-range" class="kp-range-slider" min="1800" max="10000" step="200" value="4200" data-kp-est-sqft>
            </div>

            <div class="kp-field" style="margin-top: 14px;">
                <label class="kp-label" for="kp-est-civic-addr">4. Property Civic Address (BC Geocoder Autocomplete)</label>
                <input type="text" id="kp-est-civic-addr" class="kp-input" placeholder="e.g. 5610 Ballantree Rd, West Vancouver or 1 Watts Point Rd, Squamish" data-kp-address-input autocomplete="off">
            </div>

            <div style="display: flex; flex-wrap: wrap; gap: 16px; margin-top: 14px; font-size: 0.85rem; color: var(--text-secondary);">
                <label style="display: inline-flex; align-items: center; gap: 8px; cursor: pointer;">
                    <input type="checkbox" data-kp-est-civil checked> Include BC Hydro ES54 Civil &amp; PMT Vault
                </label>
                <label style="display: inline-flex; align-items: center; gap: 8px; cursor: pointer;">
                    <input type="checkbox" data-kp-est-transit> Within 400m Frequent Transit (FTN)
                </label>
            </div>
        </div>

        <div class="kp-calc-output">
            <div>
                <div class="kp-mono" style="font-size: 0.75rem; color: var(--gold-primary); letter-spacing: 0.1em; text-transform: uppercase;">
                    <span data-kp-out-corridor>WEST VANCOUVER</span> · CCDC 5B BENCHMARK
                </div>
                <div class="kp-calc-big-number" data-kp-out-headline style="margin-top: 6px;">$2,815,000 – $4,301,000</div>
                <p data-kp-out-bylaw style="font-size: 0.84rem; color: var(--text-muted); margin-top: 8px;">
                    DWV Bylaw 4662 · Watercourse Bylaw 4364 (15m setback) · Steep-Slope Granite Micropiles
                </p>

                <div class="kp-calc-breakdown-row">
                    <span>Hard Construction Benchmark</span>
                    <strong data-kp-out-rate>$650 – $980 / sq. ft.</strong>
                </div>
                <div class="kp-calc-breakdown-row">
                    <span>BC Hydro ES54 &amp; Site Civil</span>
                    <strong data-kp-out-civil>$85,000 – $185,000</strong>
                </div>
                <div class="kp-calc-breakdown-row">
                    <span>Zoning / Bill 44 Envelope</span>
                    <strong data-kp-out-units>3–4 Units (or Luxury Estate + Coach House)</strong>
                </div>
                <div class="kp-calc-breakdown-row">
                    <span>Est. Open-Book CCDC 5B Fee Delta</span>
                    <strong data-kp-out-savings style="color: var(--gold-light);">$320,220</strong>
                </div>
            </div>

            <form class="kp-quick-intake-grid" data-kp-lead-form data-project-type="48-Hour Lot &amp; Cost Feasibility Dossier" style="margin-top: 18px;">
                <input type="text" name="name" class="kp-input" placeholder="Your Full Name *" required>
                <div class="kp-form-row-2">
                    <input type="email" name="email" class="kp-input" placeholder="Email Address *" required>
                    <input type="tel" name="phone" class="kp-input" placeholder="Phone Number *" required>
                </div>
                <button type="submit" class="kp-btn kp-btn-gold" style="width: 100%;">Request 48-Hr Lot &amp; Cost Dossier &rarr;</button>
                <div class="kp-form-status" aria-live="polite"></div>
            </form>
        </div>
    </div>
    <?php
    return (string) ob_get_clean();
}
add_shortcode('keystone_bill44_estimator', 'keystone_possibilities_bill44_estimator_shortcode');
add_shortcode('keystone_custom_build_planner', 'keystone_possibilities_bill44_estimator_shortcode');

/**
 * Renders the CCDC 5B Open-Book vs Traditional Fixed-Markup Fee Calculator.
 *
 * @param array<string, mixed>|string $atts Shortcode attributes.
 * @return string
 */
function keystone_possibilities_open_book_calculator_shortcode($atts = array()): string
{
    ob_start();
    ?>
    <div class="kp-calc-panel" data-kp-ccdc-calc style="max-width: 980px; margin: 2rem auto;">
        <span class="kp-eyebrow">CCDC 5B Open-Book Fee Transparency</span>
        <h3 class="kp-section-title">Compare Traditional GC Markup vs. Open-Book Pass-Through</h3>
        <p class="kp-section-lead">Adjust your estimated hard construction budget to see the fee delta retained in your property equity when sub-trade invoices pass through at 0% hidden markup.</p>

        <div class="kp-field" style="margin-top: 18px;">
            <label class="kp-label" for="kp-ccdc-budget-range">
                Hard Construction &amp; Civil Budget: <strong data-kp-ccdc-budget style="color: var(--gold-light);">$3,000,000</strong>
            </label>
            <input type="range" id="kp-ccdc-budget-range" class="kp-range-slider" min="900000" max="8000000" step="100000" value="3000000" data-kp-ccdc-slider>
        </div>

        <div class="kp-grid-3" style="margin-top: 20px;">
            <div class="kp-card">
                <span class="kp-mono" style="font-size: 0.74rem; color: var(--text-muted);">OPAQUE COST-PLUS / FIXED GC (~19%)</span>
                <div style="font-family: var(--font-display); font-size: 1.75rem; font-weight: 800; color: var(--text-ivory); margin-top: 6px;" data-kp-ccdc-traditional>$570,000</div>
                <p style="font-size: 0.84rem; color: var(--text-muted); margin-top: 6px;">Includes hidden sub-trade rebates and change-order escalation margins.</p>
            </div>
            <div class="kp-card">
                <span class="kp-mono" style="font-size: 0.74rem; color: var(--gold-primary);">KEYSTONE CCDC 5B OPEN-BOOK (~10%)</span>
                <div style="font-family: var(--font-display); font-size: 1.75rem; font-weight: 800; color: var(--gold-light); margin-top: 6px;" data-kp-ccdc-openbook>$300,000</div>
                <p style="font-size: 0.84rem; color: var(--text-secondary); margin-top: 6px;">100% original sub-trade invoices audited in your private Client Portal.</p>
            </div>
            <div class="kp-card" style="border-color: var(--gold-primary);">
                <span class="kp-mono" style="font-size: 0.74rem; color: var(--blue-tech);">NET EQUITY RETAINED BY OWNER</span>
                <div style="font-family: var(--font-display); font-size: 1.85rem; font-weight: 800; color: var(--gold-primary); margin-top: 6px;" data-kp-ccdc-delta>$270,000</div>
                <p style="font-size: 0.84rem; color: var(--text-secondary); margin-top: 6px;">Direct capital preserved for architectural glazing, millwork, or ES54 civil scope.</p>
            </div>
        </div>
    </div>
    <?php
    return (string) ob_get_clean();
}
add_shortcode('keystone_open_book_calculator', 'keystone_possibilities_open_book_calculator_shortcode');
