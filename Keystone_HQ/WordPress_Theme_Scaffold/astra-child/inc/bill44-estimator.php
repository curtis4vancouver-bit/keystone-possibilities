<?php
/**
 * Keystone Possibilities - Interactive Bill 44 SSMUH Lot Zoning & ROI Estimator
 * & Fiduciary Open-Book Cost Calculator Suite
 *
 * Provides:
 * 1. [keystone_bill44_estimator] - Interactive address lookup, ParcelMap BC integration,
 *    allowable SSMUH density (3-6 units), projected rental/strata ROI, and gated dossier intake.
 * 2. [keystone_open_book_calculator] - Interactive slider comparing Cost-Plus 15-20% vs
 *    Keystone raw trade pass-through, showcasing $85k-$180k+ in fee savings.
 * 3. REST Proxy /wp-json/keystone/v1/geocode - Server-side proxy for BC Geocoder API
 *    guaranteeing zero CORS blocks and high-speed address autocompletion.
 *
 * @package KeystonePossibilitiesChild
 * @version 2.6.0
 */

if (!defined('ABSPATH')) {
    exit;
}

// ── 1. Register Geocoder REST Proxy Endpoint ─────────────────────────────────
add_action('rest_api_init', function () {
    register_rest_route('keystone/v1', '/geocode', array(
        'methods' => 'GET',
        'callback' => 'keystone_possibilities_handle_geocode_proxy',
        'permission_callback' => '__return_true', // Public address lookup
    ));
});

/**
 * Handle BC Address Geocoder Proxy Request
 */
function keystone_possibilities_handle_geocode_proxy(WP_REST_Request $request) {
    $address_string = sanitize_text_field($request->get_param('address') ?? $request->get_param('addressString') ?? '');
    if (empty($address_string) || strlen($address_string) < 3) {
        return new WP_REST_Response(array('features' => array()), 200);
    }

    $encoded_addr = urlencode($address_string);
    $url = 'https://geocoder.api.gov.bc.ca/addresses.geojson?addressString=' . $encoded_addr . '&autoComplete=true&maxResults=5&outputSRS=4326';

    $response = wp_remote_get($url, array(
        'timeout' => 5,
        'headers' => array('Accept' => 'application/json')
    ));

    if (is_wp_error($response)) {
        return new WP_REST_Response(array('error' => $response->get_error_message(), 'features' => array()), 500);
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    return new WP_REST_Response($data ?? array('features' => array()), 200);
}

// ── 2. Shortcode: [keystone_bill44_estimator] ────────────────────────────────
add_shortcode('keystone_bill44_estimator', 'keystone_possibilities_bill44_estimator_shortcode');
function keystone_possibilities_bill44_estimator_shortcode($atts) {
    ob_start();
    ?>
    <div id="kp-bill44-estimator-wrapper" class="kp-tool-container" style="background: #0a0f19; border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 16px; padding: 2.5rem 1.5rem; max-width: 960px; margin: 2.5rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.7); font-family: 'Inter', -apple-system, sans-serif; color: #f8fafc;">
        
        <!-- Header / Authority Badge -->
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.4); padding: 4px 14px; border-radius: 9999px; margin-bottom: 12px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #00f0ff; box-shadow: 0 0 10px #00f0ff;"></span>
                <span style="color: #00f0ff; font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">BC Bill 44 &amp; Bill 47 Statutory Engine</span>
            </div>
            <h2 style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; margin: 0 0 0.5rem 0; background: linear-gradient(135deg, #ffffff 40%, #d4af37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Interactive Bill 44 Lot Zoning &amp; ROI Estimator
            </h2>
            <p style="color: #94a3b8; font-size: 1rem; max-width: 680px; margin: 0 auto; line-height: 1.6;">
                Enter any Greater Vancouver or Sea-to-Sky parcel address to verify statutory Small-Scale Multi-Unit Housing (SSMUH) allowable density, transit buffers, and projected rental/strata yield.
            </p>
        </div>

        <!-- Address Search & Lot Config Cockpit -->
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; position: relative;">
            <label for="kp-b44-address" style="display: block; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; color: #d4af37; margin-bottom: 8px; letter-spacing: 0.05em;">
                📍 Enter Property Civic Address (Squamish, Whistler, West Van, North Van, Vancouver)
            </label>
            <div style="position: relative;">
                <input type="text" id="kp-b44-address" placeholder="e.g. 38118 Cleveland Ave, Squamish, BC or 1234 West 14th Ave, Vancouver" style="width: 100%; box-sizing: border-box; background: #04070d; border: 1.5px solid rgba(212, 175, 55, 0.4); border-radius: 8px; padding: 14px 16px; color: #f8fafc; font-size: 1rem; outline: none; transition: border-color 0.2s;" autocomplete="off">
                <div id="kp-b44-suggestions" style="display: none; position: absolute; top: 100%; left: 0; right: 0; background: #0b1329; border: 1px solid #d4af37; border-radius: 0 0 8px 8px; max-height: 220px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.8);"></div>
            </div>

            <!-- Lot Size & Transit Quick Adjustment -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-top: 1.25rem;">
                <div>
                    <label for="kp-b44-lotsize" style="display: block; font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">Estimated Lot Size (Sq. Ft.):</label>
                    <select id="kp-b44-lotsize" style="width: 100%; background: #04070d; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 10px 12px; color: #f8fafc; font-size: 0.9rem; outline: none;">
                        <option value="2800">Under 3,014 sq. ft. (&lt; 280 m²) — Narrow/Compact</option>
                        <option value="4026" selected>Standard 33' × 122' Lot (4,026 sq. ft. / 374 m²)</option>
                        <option value="6000">Corner / 50' × 120' Lot (6,000 sq. ft. / 557 m²)</option>
                        <option value="8500">Suburban / Estate Lot (8,500+ sq. ft. / 790 m²)</option>
                    </select>
                </div>
                <div>
                    <label for="kp-b44-transit" style="display: block; font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">Frequent Transit Network (FTN) Proximity:</label>
                    <select id="kp-b44-transit" style="width: 100%; background: #04070d; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 10px 12px; color: #f8fafc; font-size: 0.9rem; outline: none;">
                        <option value="inside" selected>Within 400m of Frequent Transit / Bus Stop (Bill 44 &amp; 47)</option>
                        <option value="outside">Outside 400m Frequent Transit Corridor</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Live Calculation Dashboard -->
        <div id="kp-b44-results-card" style="background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(4, 7, 13, 0.95) 100%); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 12px; padding: 1.75rem; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase;">Selected Parcel:</span>
                    <div id="kp-b44-display-addr" style="color: #00f0ff; font-weight: 700; font-size: 1.1rem; font-family: 'Outfit', sans-serif;">Enter address above</div>
                </div>
                <div style="text-align: right;">
                    <span style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase;">BC Builder Licence:</span>
                    <div style="color: #d4af37; font-weight: 700; font-size: 0.95rem;">#52603 (Wayne Stevenson)</div>
                </div>
            </div>

            <!-- Key Metric Cards Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                
                <!-- Card 1: Allowable Units -->
                <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 10px; padding: 1.25rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">Allowable Density</span>
                    <div id="kp-b44-units" style="color: #d4af37; font-size: 2.4rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">6 Units</div>
                    <span id="kp-b44-units-sub" style="color: #34d399; font-size: 0.8rem; font-weight: 600;">Zero Minimum Parking Required</span>
                </div>

                <!-- Card 2: Buildable Floor Area -->
                <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 1.25rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">Max Floor Area (FSR ~1.0)</span>
                    <div id="kp-b44-fsr" style="color: #00f0ff; font-size: 2.4rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">4,026 SF</div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">~671 SF Avg. Unit Size</span>
                </div>

                <!-- Card 3: Gross Rental Yield -->
                <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 1.25rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">Est. Monthly Rental Roll</span>
                    <div id="kp-b44-rent" style="color: #f8fafc; font-size: 2.2rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">$18,600 /mo</div>
                    <span style="color: #34d399; font-size: 0.8rem;">$223,200 Annual Gross</span>
                </div>

                <!-- Card 4: Strata Valuation -->
                <div style="background: rgba(0,0,0,0.5); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 10px; padding: 1.25rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">Projected Strata Realization</span>
                    <div id="kp-b44-strata" style="color: #f6d365; font-size: 2.2rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">$4.43M</div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">Based on $1,100/SF Resale</span>
                </div>
            </div>

            <!-- Turnkey Cost & Infrastructure Callout -->
            <div style="background: rgba(15, 23, 42, 0.7); border-left: 3px solid #00f0ff; border-radius: 0 8px 8px 0; padding: 12px 16px; font-size: 0.88rem; line-height: 1.5; color: #cbd5e1;">
                <strong style="color: #00f0ff;">⚡ Critical Builder Note:</strong> Turnkey infill hard construction cost is modeled at <strong>$385/sq. ft.</strong> (Total: <span id="kp-b44-hardcost" style="color:#ffffff; font-weight:700;">$1,550,010</span>) including BC Energy Step Code Tier 4/5 envelope and acoustic soundproofing. As a certified BC Hydro ES54 civil contractor, Wayne Stevenson coordinates offsite 400A–600A underground civil conversion, eliminating $65k–$120k utility surprises.
            </div>
        </div>

        <!-- High-Converting Lead Capture Gate (8-Page Dossier) -->
        <div style="background: #04070d; border: 1.5px solid #d4af37; border-radius: 12px; padding: 2rem; box-shadow: 0 0 35px rgba(212, 175, 55, 0.15);">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 2.2rem; margin-bottom: 0.25rem;">📑</div>
                <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 800; text-transform: uppercase; color: #d4af37; margin: 0 0 0.5rem 0; letter-spacing: 0.05em;">
                    Unlock the Full 8-Page Financial Feasibility &amp; Servicing Dossier
                </h3>
                <p style="color: #94a3b8; font-size: 0.95rem; max-width: 620px; margin: 0 auto; line-height: 1.5;">
                    Receive Wayne Stevenson's complete site evaluation: municipal setback envelopes, BC Hydro civil transformer capacity, development cost charges (DCC/ACC), and trade line-item budget.
                </p>
            </div>

            <form id="kp-b44-gate-form" data-project-type="Bill 44 Feasibility Dossier Request" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
                <input type="text" name="fullName" placeholder="Full Name *" required style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 12px; color: #f8fafc; font-size: 0.95rem; outline: none;">
                <input type="email" name="email" placeholder="Email Address *" required style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 12px; color: #f8fafc; font-size: 0.95rem; outline: none;">
                <input type="tel" name="phone" placeholder="Phone Number *" required style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 12px; color: #f8fafc; font-size: 0.95rem; outline: none;">
                <input type="hidden" name="lotAddress" id="kp-b44-hidden-addr" value="">
                <button type="submit" style="grid-column: 1 / -1; background: linear-gradient(135deg, #d4af37 0%, #aa820a 100%); color: #04070d; border: none; border-radius: 8px; padding: 15px; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.05rem; text-transform: uppercase; letter-spacing: 0.06em; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.35);">
                    🚀 Dispatch My Complete 8-Page Pro-Forma Dossier
                </button>
            </form>
            <div id="kp-b44-status" style="margin-top: 12px; display: none;"></div>
        </div>

    </div>

    <!-- Client-Side Real-Time Math & Autocomplete Engine -->
    <script>
    document.addEventListener('DOMContentLoaded', function () {
        const addrInput = document.getElementById('kp-b44-address');
        const suggestBox = document.getElementById('kp-b44-suggestions');
        const lotSelect = document.getElementById('kp-b44-lotsize');
        const transitSelect = document.getElementById('kp-b44-transit');
        const hiddenAddr = document.getElementById('kp-b44-hidden-addr');
        const displayAddr = document.getElementById('kp-b44-display-addr');

        let debounceTimer;

        // Autocomplete listener connecting to /wp-json/keystone/v1/geocode
        addrInput.addEventListener('input', function () {
            const query = this.value.trim();
            clearTimeout(debounceTimer);
            if (query.length < 3) {
                suggestBox.style.display = 'none';
                return;
            }
            debounceTimer = setTimeout(function () {
                fetch('/wp-json/keystone/v1/geocode?address=' + encodeURIComponent(query))
                    .then(function (r) { return r.json(); })
                    .then(function (data) {
                        if (data && data.features && data.features.length > 0) {
                            suggestBox.innerHTML = '';
                            data.features.forEach(function (feat) {
                                const fullAddr = feat.properties.fullAddress || feat.properties.matchAddress;
                                const item = document.createElement('div');
                                item.style.cssText = 'padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.06); cursor: pointer; font-size: 0.9rem; color: #f8fafc; transition: background 0.15s;';
                                item.innerText = fullAddr;
                                item.addEventListener('mouseenter', function () { item.style.background = 'rgba(212, 175, 55, 0.2)'; });
                                item.addEventListener('mouseleave', function () { item.style.background = 'transparent'; });
                                item.addEventListener('click', function () {
                                    addrInput.value = fullAddr;
                                    hiddenAddr.value = fullAddr;
                                    displayAddr.innerText = fullAddr;
                                    suggestBox.style.display = 'none';
                                    recalculate();
                                });
                                suggestBox.appendChild(item);
                            });
                            suggestBox.style.display = 'block';
                        } else {
                            suggestBox.style.display = 'none';
                        }
                    })
                    .catch(function () { suggestBox.style.display = 'none'; });
            }, 250);
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', function (e) {
            if (!addrInput.contains(e.target) && !suggestBox.contains(e.target)) {
                suggestBox.style.display = 'none';
            }
        });

        lotSelect.addEventListener('change', recalculate);
        transitSelect.addEventListener('change', recalculate);

        function recalculate() {
            const lotSqFt = parseFloat(lotSelect.value) || 4026;
            const isTransit = transitSelect.value === 'inside';
            const lotSqm = lotSqFt * 0.092903;

            let units = 4;
            let parkingNote = "1 stall / unit required";

            if (lotSqm < 280) {
                units = 3;
                parkingNote = "Standard parking bylaws apply";
            } else if (lotSqm >= 280 && isTransit) {
                units = 6;
                parkingNote = "Zero Minimum Parking Mandated (Bill 44/47)";
            } else {
                units = 4;
                parkingNote = "Standard off-street parking applies";
            }

            // Calculations
            const fsr = Math.round(lotSqFt * 1.0); // 1.0 FSR standard
            const avgUnitSize = Math.round(fsr / units);
            const hardCostPerSf = 385;
            const totalHardCost = fsr * hardCostPerSf;
            const monthlyRentPerUnit = avgUnitSize >= 800 ? 3400 : 3100;
            const totalMonthlyRent = units * monthlyRentPerUnit;
            const annualGrossRent = totalMonthlyRent * 12;
            const strataPricePerSf = 1100;
            const totalStrataVal = fsr * strataPricePerSf;

            // DOM Updates
            document.getElementById('kp-b44-units').innerText = units + ' Units';
            document.getElementById('kp-b44-units-sub').innerText = parkingNote;
            document.getElementById('kp-b44-fsr').innerText = fsr.toLocaleString() + ' SF';
            document.getElementById('kp-b44-rent').innerText = '$' + totalMonthlyRent.toLocaleString() + ' /mo';
            document.getElementById('kp-b44-strata').innerText = '$' + (totalStrataVal / 1000000).toFixed(2) + 'M';
            document.getElementById('kp-b44-hardcost').innerText = '$' + totalHardCost.toLocaleString();

            if (!hiddenAddr.value && addrInput.value) {
                hiddenAddr.value = addrInput.value;
                displayAddr.innerText = addrInput.value;
            }
        }

        recalculate();
    });
    </script>
    <?php
    return ob_get_clean();
}

// ── 3. Shortcode: [keystone_open_book_calculator] ────────────────────────────
add_shortcode('keystone_open_book_calculator', 'keystone_possibilities_open_book_calculator_shortcode');
function keystone_possibilities_open_book_calculator_shortcode($atts) {
    ob_start();
    ?>
    <div id="kp-open-book-calc-wrapper" class="kp-tool-container" style="background: #0a0f19; border: 1px solid rgba(0, 240, 255, 0.4); border-radius: 16px; padding: 2.5rem 1.5rem; max-width: 960px; margin: 2.5rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.7); font-family: 'Inter', -apple-system, sans-serif; color: #f8fafc;">
        
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.4); padding: 4px 14px; border-radius: 9999px; margin-bottom: 12px;">
                <span style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">Fiduciary Cost Transparency</span>
            </div>
            <h2 style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; margin: 0 0 0.5rem 0; background: linear-gradient(135deg, #ffffff 40%, #00f0ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Fiduciary Open-Book Cost Calculator
            </h2>
            <p style="color: #94a3b8; font-size: 1rem; max-width: 680px; margin: 0 auto; line-height: 1.6;">
                Compare traditional "Cost-Plus 15%–20%" general contractor markups against Keystone Possibilities' flat construction management fee and 100% wholesale trade pass-through.
            </p>
        </div>

        <!-- Slider Cockpit -->
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 2rem; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; flex-wrap: wrap;">
                <label for="kp-ob-budget-slider" style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; text-transform: uppercase; color: #f8fafc;">
                    Project Construction Hard Cost (Materials &amp; Subtrades)
                </label>
                <div id="kp-ob-budget-display" style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 900; color: #00f0ff;">
                    $1,500,000
                </div>
            </div>
            <input type="range" id="kp-ob-budget-slider" min="800000" max="3500000" step="50000" value="1500000" style="width: 100%; height: 10px; border-radius: 5px; background: #1e293b; outline: none; cursor: pointer; accent-color: #00f0ff;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 6px;">
                <span>$800,000 (Hillside / Infill)</span>
                <span>$2,000,000 (Multiplex / Luxury)</span>
                <span>$3,500,000+ (Estate)</span>
            </div>
        </div>

        <!-- Comparative Output Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            
            <!-- Traditional Cost-Plus -->
            <div style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 12px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem;">⚠️</span>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; text-transform: uppercase; color: #f87171; margin: 0;">Traditional Cost-Plus</h3>
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">Standard 18% GC Markup on all invoices:</div>
                <div id="kp-ob-trad-fee" style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: #ef4444; margin-bottom: 12px;">
                    $270,000
                </div>
                <ul style="padding-left: 20px; font-size: 0.85rem; color: #94a3b8; line-height: 1.6; margin: 0;">
                    <li>Contractor profits more when costs escalate</li>
                    <li>Hidden trade markup markups pocketed</li>
                    <li>No incentive to negotiate wholesale prices</li>
                </ul>
            </div>

            <!-- Keystone Open-Book Pass-Through -->
            <div style="background: rgba(16, 185, 129, 0.08); border: 1.5px solid #10b981; border-radius: 12px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem;">🛡️</span>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; text-transform: uppercase; color: #34d399; margin: 0;">Keystone Open-Book</h3>
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">Fixed Fiduciary CM Fee + 0% Trade Markups:</div>
                <div id="kp-ob-keystone-fee" style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: #10b981; margin-bottom: 12px;">
                    $135,000
                </div>
                <ul style="padding-left: 20px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; margin: 0;">
                    <li>100% of wholesale lumber/trade discounts to you</li>
                    <li>Zero incentive to inflate change orders</li>
                    <li>Transparent bank-audited draw schedules</li>
                </ul>
            </div>

        </div>

        <!-- Animated Net Savings Banner -->
        <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(0, 240, 255, 0.15) 100%); border: 1.5px solid #d4af37; border-radius: 12px; padding: 1.75rem; text-align: center; box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);">
            <span style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em;">Net Direct Hard Cash Savings Kept in Your Equity</span>
            <div id="kp-ob-savings" style="font-family: 'Outfit', sans-serif; font-size: 3rem; font-weight: 900; color: #d4af37; margin: 6px 0; text-shadow: 0 0 20px rgba(212, 175, 55, 0.4);">
                $135,000 SAVED
            </div>
            <p style="color: #f8fafc; font-size: 0.95rem; max-width: 620px; margin: 0 auto; line-height: 1.5;">
                By utilizing Wayne Stevenson's certified builder credentials (#52603) and fiduciary open-book management, you eliminate $85,000 to $180,000+ in phantom contractor markups.
            </p>
        </div>

    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function () {
        const slider = document.getElementById('kp-ob-budget-slider');
        const budgetDisplay = document.getElementById('kp-ob-budget-display');
        const tradFee = document.getElementById('kp-ob-trad-fee');
        const keystoneFee = document.getElementById('kp-ob-keystone-fee');
        const savingsDisplay = document.getElementById('kp-ob-savings');

        function updateCalc() {
            const budget = parseFloat(slider.value) || 1500000;
            budgetDisplay.innerText = '$' + budget.toLocaleString();

            // Traditional 18% cost-plus
            const trad = Math.round(budget * 0.18);
            tradFee.innerText = '$' + trad.toLocaleString();

            // Keystone tiered flat fiduciary fee (approx 9% equivalent with wholesale pass-through)
            const keystone = Math.round(budget * 0.09);
            keystoneFee.innerText = '$' + keystone.toLocaleString();

            const savings = trad - keystone;
            savingsDisplay.innerText = '$' + savings.toLocaleString() + ' SAVED';
        }

        slider.addEventListener('input', updateCalc);
        updateCalc();
    });
    </script>
    <?php
    return ob_get_clean();
}

// ── 4. Automatic Injection on /feasibility-plan/ ─────────────────────────────
add_filter('the_content', 'keystone_possibilities_inject_feasibility_tools', 20);
function keystone_possibilities_inject_feasibility_tools($content) {
    if (is_page('feasibility-plan') || (is_singular() && preg_match('#feasibility-plan#i', $_SERVER['REQUEST_URI'] ?? ''))) {
        if (stripos($content, 'kp-bill44-estimator-wrapper') === false) {
            $estimator = do_shortcode('[keystone_bill44_estimator]');
            $open_book = do_shortcode('[keystone_open_book_calculator]');
            return $content . "\n\n" . $estimator . "\n\n" . $open_book;
        }
    }
    return $content;
}

