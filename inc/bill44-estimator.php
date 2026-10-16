<?php
/**
 * Keystone Possibilities - Custom Home, Estate & BC Hydro Civil Pre-Construction
 * Cost & Servicing Planner + Fiduciary Open-Book Cost Calculator Suite
 *
 * Provides:
 * 1. [keystone_bill44_estimator] / [keystone_custom_build_planner] - Interactive
 *    address lookup, Project Archetype selector (Luxury Custom Single-Family Estate,
 *    Mountain Modern Custom Home, BC Hydro ES54 Underground Civil & PMT Servicing,
 *    Custom Duplex / Carriage House), BC Hydro ES54 servicing breakdown, and
 *    "Request Your Custom Home & Civil Pre-Construction Cost Dossier" lead capture gate.
 * 2. [keystone_open_book_calculator] - Interactive slider comparing Cost-Plus 18% vs
 *    Keystone CCDC 5B wholesale trade pass-through, showcasing $135k-$315k+ in fee savings.
 * 3. REST Proxy /wp-json/keystone/v1/geocode - Server-side proxy for BC Geocoder API
 *    guaranteeing zero CORS blocks and high-speed address autocompletion.
 *
 * @package KeystonePossibilitiesChild
 * @version 2.8.0
 */

if (!defined('ABSPATH')) {
    exit;
}

// ── 1. Register Geocoder REST Proxy Endpoint ─────────────────────────────────
add_action('rest_api_init', function () {
    register_rest_route('keystone/v1', '/geocode', array(
        'methods'             => 'GET',
        'callback'            => 'keystone_possibilities_handle_geocode_proxy',
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

// ── 2. Shortcode: [keystone_bill44_estimator] & [keystone_custom_build_planner] ──
add_shortcode('keystone_bill44_estimator', 'keystone_possibilities_bill44_estimator_shortcode');
add_shortcode('keystone_custom_build_planner', 'keystone_possibilities_bill44_estimator_shortcode');
function keystone_possibilities_bill44_estimator_shortcode($atts) {
    ob_start();
    ?>
    <div id="kp-bill44-estimator-wrapper" class="kp-tool-container" style="background: #0a0f19; border: 1.5px solid rgba(212, 175, 55, 0.45); border-radius: 18px; padding: 2rem 1.5rem; max-width: 1040px; margin: 1.5rem auto 2.5rem auto; box-shadow: 0 18px 45px rgba(0,0,0,0.75); font-family: 'Inter', -apple-system, sans-serif; color: #f8fafc;">
        
        <!-- Header / Authority Badge -->
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.12); border: 1px solid rgba(212, 175, 55, 0.45); padding: 6px 16px; border-radius: 9999px; margin-bottom: 10px; flex-wrap: wrap; justify-content: center;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 10px #38bdf8;"></span>
                <span style="color: #f6d365; font-family: 'Outfit', sans-serif; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.07em;">BC Housing Licensed Builder #52603 • BC Hydro Civil Contractor ES54 • 2-5-10 National Home Warranty</span>
            </div>
            <h2 style="font-family: 'Outfit', sans-serif; font-size: clamp(1.5rem, 2.8vw, 2.1rem); font-weight: 800; text-transform: uppercase; letter-spacing: 0.03em; margin: 0 0 0.45rem 0; background: linear-gradient(135deg, #ffffff 35%, #d4af37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Custom Home, Estate &amp; BC Hydro Civil Pre-Construction Cost &amp; Servicing Planner
            </h2>
            <p style="color: #94a3b8; font-size: 0.96rem; max-width: 760px; margin: 0 auto; line-height: 1.55;">
                Select your <strong style="color: #f8fafc;">Project Archetype</strong> and enter your West Vancouver, Whistler, Squamish, or North Vancouver property address to model turnkey custom construction budgets, BC Hydro ES54 underground servicing &amp; PMT vault requirements, and open-book CCDC 5B fee savings.
            </p>
        </div>

        <!-- Address Search & Project Archetype Config Cockpit -->
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 1.35rem; margin-bottom: 1.5rem; position: relative;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <label for="kp-b44-archetype" style="display: block; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; color: #d4af37; margin-bottom: 6px; letter-spacing: 0.05em;">
                        🏛️ Select Project Archetype:
                    </label>
                    <select id="kp-b44-archetype" style="width: 100%; height: 48px !important; background: #04070d !important; border: 1.5px solid rgba(212, 175, 55, 0.55) !important; border-radius: 10px !important; padding: 0 14px !important; color: #f8fafc !important; font-size: 0.94rem !important; font-weight: 600; outline: none;">
                        <option value="Luxury Custom Single-Family Estate" data-rate="650" data-civil="95000" data-spec="Step Code 5 Net-Zero • Architectural Concrete &amp; Timber" selected>Luxury Custom Single-Family Estate</option>
                        <option value="Mountain Modern Custom Home" data-rate="525" data-civil="65000" data-spec="High Snow-Load Alpine Envelope • 2-5-10 Warranty">Mountain Modern Custom Home</option>
                        <option value="BC Hydro ES54 Underground Civil &amp; PMT Servicing" data-rate="285" data-civil="145000" data-spec="Primary/Secondary Duct Banks • PMT Vault &amp; Rock Trenching">BC Hydro ES54 Underground Civil &amp; PMT Servicing</option>
                        <option value="Custom Duplex / Carriage House" data-rate="445" data-civil="55000" data-spec="Multi-Generational Suite • Dual Metering &amp; Acoustic STC 58">Custom Duplex / Carriage House</option>
                    </select>
                </div>

                <div style="position: relative;">
                    <label for="kp-b44-address" style="display: block; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; color: #38bdf8; margin-bottom: 6px; letter-spacing: 0.05em;">
                        📍 Property Civic Address (West Van, Whistler, Squamish, North Van):
                    </label>
                    <input type="text" id="kp-b44-address" placeholder="e.g. 38118 Cleveland Ave, Squamish or 1420 Chartwell Dr, West Vancouver" style="width: 100%; height: 48px !important; box-sizing: border-box; background: #04070d !important; border: 1.5px solid rgba(56, 189, 248, 0.45) !important; border-radius: 10px !important; padding: 0 14px !important; color: #f8fafc !important; font-size: 0.94rem !important; outline: none; transition: border-color 0.2s;" autocomplete="off">
                    <div id="kp-b44-suggestions" style="display: none; position: absolute; top: 100%; left: 0; right: 0; background: #0b1329; border: 1px solid #d4af37; border-radius: 0 0 10px 10px; max-height: 220px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.8);"></div>
                </div>
            </div>

            <!-- Target Area & Civil Servicing Profile -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
                <div>
                    <label for="kp-b44-lotsize" style="display: block; font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Planned Living / Project Area (Sq. Ft.):</label>
                    <select id="kp-b44-lotsize" style="width: 100%; height: 46px !important; background: #04070d !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 8px !important; padding: 0 12px !important; color: #f8fafc !important; font-size: 0.9rem !important; outline: none;">
                        <option value="2800">2,800 sq. ft. — Custom Carriage / Compact Residence</option>
                        <option value="4200" selected>4,200 sq. ft. — Custom Single-Family Residence</option>
                        <option value="6000">6,000 sq. ft. — Luxury Mountain / Coastal Estate</option>
                        <option value="8500">8,500+ sq. ft. — Multi-Generational Estate Compound</option>
                    </select>
                </div>
                <div>
                    <label for="kp-b44-transit" style="display: block; font-size: 0.82rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">BC Hydro ES54 Civil &amp; Bedrock Profile:</label>
                    <select id="kp-b44-transit" style="width: 100%; height: 46px !important; background: #04070d !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 8px !important; padding: 0 12px !important; color: #f8fafc !important; font-size: 0.9rem !important; outline: none;">
                        <option value="inside" selected>400A–600A Underground ES54 Duct Bank + Bedrock Anchoring</option>
                        <option value="pmt">Pad-Mounted Transformer (PMT) Vault + Heavy Rock Excavation</option>
                        <option value="outside">Standard 200A–400A Underground BC Hydro Civil Tie-In</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Live Calculation Dashboard -->
        <div id="kp-b44-results-card" style="background: linear-gradient(180deg, rgba(15, 23, 42, 0.92) 0%, rgba(4, 7, 13, 0.98) 100%); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Selected Archetype &amp; Site:</span>
                    <div id="kp-b44-display-addr" style="color: #38bdf8; font-weight: 800; font-size: 1.05rem; font-family: 'Outfit', sans-serif;">Luxury Custom Single-Family Estate — West Vancouver / Sea-to-Sky</div>
                </div>
                <div style="text-align: right;">
                    <span style="color: #94a3b8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Builder &amp; Civil Authority:</span>
                    <div style="color: #d4af37; font-weight: 800; font-size: 0.92rem;">BC Housing #52603 • BC Hydro ES54</div>
                </div>
            </div>

            <!-- Key Metric Cards Grid -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
                
                <!-- Card 1: Selected Archetype Tier -->
                <div style="background: rgba(4, 7, 13, 0.75); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 18px; padding: 1.1rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;">Hard Cost Benchmark</span>
                    <div id="kp-b44-units" style="color: #d4af37; font-size: 2rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">$650 / SF</div>
                    <span id="kp-b44-units-sub" style="color: #38bdf8; font-size: 0.78rem; font-weight: 600;">2-5-10 National Home Warranty</span>
                </div>

                <!-- Card 2: Planned Area -->
                <div style="background: rgba(4, 7, 13, 0.75); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 18px; padding: 1.1rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;">Planned Build Area</span>
                    <div id="kp-b44-fsr" style="color: #38bdf8; font-size: 2rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">4,200 SF</div>
                    <span id="kp-b44-spec-sub" style="color: #94a3b8; font-size: 0.78rem;">Step Code 5 / Net-Zero Envelope</span>
                </div>

                <!-- Card 3: BC Hydro ES54 Servicing Allowance -->
                <div style="background: rgba(4, 7, 13, 0.75); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 18px; padding: 1.1rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;">BC Hydro ES54 &amp; Civil</span>
                    <div id="kp-b44-rent" style="color: #f8fafc; font-size: 2rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">$95,000</div>
                    <span style="color: #38bdf8; font-size: 0.78rem;">Duct Bank, PMT &amp; Rock Trenching</span>
                </div>

                <!-- Card 4: Open-Book Fiduciary Savings -->
                <div style="background: rgba(4, 7, 13, 0.75); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 18px; padding: 1.1rem; text-align: center;">
                    <span style="color: #94a3b8; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em;">Open-Book Fee Savings</span>
                    <div id="kp-b44-strata" style="color: #f6d365; font-size: 2rem; font-weight: 900; font-family: 'Outfit', sans-serif; margin: 4px 0;">$245,700</div>
                    <span style="color: #94a3b8; font-size: 0.78rem;">Saved vs. 18% Traditional GC</span>
                </div>
            </div>

            <!-- Turnkey Cost & BC Hydro ES54 Servicing Breakdown Callout -->
            <div style="background: rgba(15, 23, 42, 0.8); border-left: 3px solid #38bdf8; border-radius: 0 12px 12px 0; padding: 12px 16px; font-size: 0.88rem; line-height: 1.55; color: #cbd5e1;">
                <strong style="color: #38bdf8;">⚡ BC Hydro ES54 Civil &amp; Pre-Construction Breakdown:</strong> Estimated turnkey hard construction &amp; civil budget is modeled at <span id="kp-b44-hardcost" style="color:#ffffff; font-weight:800;">$2,825,000</span> (including BC Energy Step Code 4/5 envelope, geotechnical bedrock anchoring, and statutory 2-5-10 National Home Warranty). As a certified <strong>BC Hydro ES54 Civil Contractor</strong>, Wayne Stevenson executes underground primary/secondary duct banks, 200A–600A service drops, and Pad-Mounted Transformer (PMT) vaults directly—eliminating $65k–$120k third-party utility surprises and 9-month hydro delays.
            </div>
        </div>

        <!-- High-Converting Lead Capture Gate -->
        <div style="background: #04070d; border: 1.5px solid #d4af37; border-radius: 18px; padding: 1.75rem; box-shadow: 0 0 35px rgba(212, 175, 55, 0.15);">
            <div style="text-align: center; margin-bottom: 1.25rem;">
                <h3 style="font-family: 'Outfit', sans-serif; font-size: clamp(1.2rem, 2.2vw, 1.45rem); font-weight: 800; text-transform: uppercase; color: #d4af37; margin: 0 0 0.45rem 0; letter-spacing: 0.05em;">
                    Request Your Custom Home &amp; Civil Pre-Construction Cost Dossier
                </h3>
                <p style="color: #94a3b8; font-size: 0.92rem; max-width: 680px; margin: 0 auto; line-height: 1.5;">
                    Receive Wayne Stevenson's bank-ready pre-construction evaluation: custom home &amp; estate hard-cost trade breakdown, geotechnical bedrock assessment, BC Hydro ES54 underground servicing &amp; PMT vault plan, and CCDC 5B open-book schedule.
                </p>
            </div>

            <form id="kp-b44-gate-form" data-project-type="Custom Home & Civil Pre-Construction Cost Dossier" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 0.9rem;">
                <input type="text" name="fullName" placeholder="Full Name *" required style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.18); border-radius: 10px; padding: 12px 14px; color: #f8fafc; font-size: 0.95rem; outline: none;">
                <input type="email" name="email" placeholder="Email Address *" required style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.18); border-radius: 10px; padding: 12px 14px; color: #f8fafc; font-size: 0.95rem; outline: none;">
                <input type="tel" name="phone" placeholder="Phone Number *" required style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.18); border-radius: 10px; padding: 12px 14px; color: #f8fafc; font-size: 0.95rem; outline: none;">
                <input type="hidden" name="lotAddress" id="kp-b44-hidden-addr" value="">
                <button type="submit" class="kp-btn-primary" style="grid-column: 1 / -1; background: linear-gradient(135deg, #d4af37 0%, #aa820a 100%); color: #04070d !important; border: 1px solid #f6d365; border-radius: 9999px; padding: 15px 24px; font-family: 'Outfit', sans-serif; font-weight: 900; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.06em; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
                    🚀 Request Your Custom Home &amp; Civil Pre-Construction Cost Dossier →
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
        const archetypeSelect = document.getElementById('kp-b44-archetype');
        const lotSelect = document.getElementById('kp-b44-lotsize');
        const transitSelect = document.getElementById('kp-b44-transit');
        const hiddenAddr = document.getElementById('kp-b44-hidden-addr');
        const displayAddr = document.getElementById('kp-b44-display-addr');
        const gateForm = document.getElementById('kp-b44-gate-form');

        if (!addrInput || !lotSelect || !transitSelect) return;

        let debounceTimer;

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

        document.addEventListener('click', function (e) {
            if (!addrInput.contains(e.target) && !suggestBox.contains(e.target)) {
                suggestBox.style.display = 'none';
            }
        });

        if (archetypeSelect) archetypeSelect.addEventListener('change', recalculate);
        lotSelect.addEventListener('change', recalculate);
        transitSelect.addEventListener('change', recalculate);

        function recalculate() {
            const areaSqFt = parseFloat(lotSelect.value) || 4200;
            const selectedOpt = archetypeSelect ? archetypeSelect.options[archetypeSelect.selectedIndex] : null;
            const archetypeName = selectedOpt ? selectedOpt.value : 'Luxury Custom Single-Family Estate';
            const ratePerSf = selectedOpt ? (parseFloat(selectedOpt.getAttribute('data-rate')) || 650) : 650;
            const baseCivil = selectedOpt ? (parseFloat(selectedOpt.getAttribute('data-civil')) || 95000) : 95000;
            const specNote = selectedOpt ? (selectedOpt.getAttribute('data-spec') || 'Step Code 5 / Net-Zero Envelope') : 'Step Code 5 / Net-Zero Envelope';

            let civilAdjustment = 0;
            let warrantyNote = '2-5-10 National Home Warranty';
            if (transitSelect.value === 'pmt') {
                civilAdjustment = 45000;
                warrantyNote = 'ES54 PMT Vault + Rock Excavation';
            } else if (transitSelect.value === 'inside') {
                civilAdjustment = 15000;
                warrantyNote = '2-5-10 Warranty + ES54 Duct Bank';
            }

            const totalCivil = baseCivil + civilAdjustment;
            const buildHardCost = Math.round(areaSqFt * ratePerSf);
            const totalProjectHardCost = buildHardCost + totalCivil;
            const traditionalMarkup = Math.round(totalProjectHardCost * 0.18);
            const keystoneFee = Math.round(totalProjectHardCost * 0.09);
            const openBookSavings = traditionalMarkup - keystoneFee;

            document.getElementById('kp-b44-units').innerText = '$' + ratePerSf.toLocaleString() + ' / SF';
            document.getElementById('kp-b44-units-sub').innerText = warrantyNote;
            document.getElementById('kp-b44-fsr').innerText = areaSqFt.toLocaleString() + ' SF';
            const specSub = document.getElementById('kp-b44-spec-sub');
            if (specSub) specSub.innerText = specNote;
            document.getElementById('kp-b44-rent').innerText = '$' + totalCivil.toLocaleString();
            document.getElementById('kp-b44-strata').innerText = '$' + openBookSavings.toLocaleString();
            document.getElementById('kp-b44-hardcost').innerText = '$' + totalProjectHardCost.toLocaleString();

            const addrText = addrInput.value.trim();
            if (addrText) {
                hiddenAddr.value = addrText + ' (' + archetypeName + ')';
                displayAddr.innerText = archetypeName + ' — ' + addrText;
            } else {
                displayAddr.innerText = archetypeName + ' — West Vancouver / Whistler / Squamish';
            }
            if (gateForm) {
                gateForm.setAttribute('data-project-type', 'Custom Home & Civil Pre-Construction Cost Dossier: ' + archetypeName);
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
    <div id="kp-open-book-calc-wrapper" class="kp-tool-container" style="background: #0a0f19; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 18px; padding: 2.2rem 1.5rem; max-width: 1040px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.7); font-family: 'Inter', -apple-system, sans-serif; color: #f8fafc;">
        
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 1.75rem;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.12); border: 1px solid rgba(212, 175, 55, 0.4); padding: 5px 16px; border-radius: 9999px; margin-bottom: 12px;">
                <span style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em;">CCDC 5B Fiduciary Cost Transparency</span>
            </div>
            <h2 style="font-family: 'Outfit', sans-serif; font-size: clamp(1.5rem, 2.6vw, 2rem); font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; margin: 0 0 0.5rem 0; background: linear-gradient(135deg, #ffffff 40%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Fiduciary Open-Book Cost Calculator
            </h2>
            <p style="color: #94a3b8; font-size: 0.98rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">
                Compare traditional "Cost-Plus 18%–20%" paper contractor markups against Keystone Possibilities' transparent CCDC 5B management fee and 100% wholesale trade pass-through on custom homes and BC Hydro civil works.
            </p>
        </div>

        <!-- Slider Cockpit -->
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 1.75rem; margin-bottom: 1.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; flex-wrap: wrap;">
                <label for="kp-ob-budget-slider" style="font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; text-transform: uppercase; color: #f8fafc;">
                    Custom Home or Civil Construction Hard Cost (Materials &amp; Subtrades)
                </label>
                <div id="kp-ob-budget-display" style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 900; color: #38bdf8;">
                    $2,500,000
                </div>
            </div>
            <input type="range" id="kp-ob-budget-slider" min="800000" max="6000000" step="100000" value="2500000" style="width: 100%; height: 10px; border-radius: 5px; background: #1e293b; outline: none; cursor: pointer; accent-color: #38bdf8;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-top: 6px;">
                <span>$800,000 (BC Hydro Civil / Custom Renovation)</span>
                <span>$2,500,000 (Mountain Modern Custom Home)</span>
                <span>$6,000,000+ (Architectural Estate)</span>
            </div>
        </div>

        <!-- Comparative Output Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; margin-bottom: 1.75rem;">
            
            <!-- Traditional Cost-Plus -->
            <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 18px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem;">⚠️</span>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; text-transform: uppercase; color: #f6d365; margin: 0;">Traditional Cost-Plus</h3>
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">Standard 18% GC Markup on all invoices:</div>
                <div id="kp-ob-trad-fee" style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: #d4af37; margin-bottom: 12px;">
                    $450,000
                </div>
                <ul style="padding-left: 20px; font-size: 0.85rem; color: #94a3b8; line-height: 1.6; margin: 0;">
                    <li>Contractor profits more when costs escalate</li>
                    <li>Hidden sub-trade rebates pocketed</li>
                    <li>No incentive to value-engineer rock &amp; civil works</li>
                </ul>
            </div>

            <!-- Keystone Open-Book Pass-Through -->
            <div style="background: rgba(56, 189, 248, 0.08); border: 1.5px solid #38bdf8; border-radius: 18px; padding: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem;">🛡️</span>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; text-transform: uppercase; color: #38bdf8; margin: 0;">Keystone Open-Book</h3>
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;">Fixed Fiduciary CM Fee + 0% Trade Markups:</div>
                <div id="kp-ob-keystone-fee" style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: #38bdf8; margin-bottom: 12px;">
                    $225,000
                </div>
                <ul style="padding-left: 20px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; margin: 0;">
                    <li>100% of wholesale lumber, concrete &amp; trade discounts to you</li>
                    <li>Zero incentive to inflate change orders</li>
                    <li>Transparent bank-audited CCDC 5B draw schedules</li>
                </ul>
            </div>

        </div>

        <!-- Animated Net Savings Banner -->
        <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(56, 189, 248, 0.12) 100%); border: 1.5px solid #d4af37; border-radius: 18px; padding: 1.6rem; text-align: center; box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);">
            <span style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em;">Net Direct Hard Cash Savings Kept in Your Custom Home Equity</span>
            <div id="kp-ob-savings" style="font-family: 'Outfit', sans-serif; font-size: 2.8rem; font-weight: 900; color: #d4af37; margin: 6px 0; text-shadow: 0 0 20px rgba(212, 175, 55, 0.4);">
                $225,000 SAVED
            </div>
            <p style="color: #f8fafc; font-size: 0.95rem; max-width: 640px; margin: 0 auto; line-height: 1.5;">
                By working directly with Wayne Stevenson (BC Housing Builder #52603 &amp; BC Hydro ES54 Civil Contractor) under CCDC 5B open-book management, you eliminate six-figure phantom contractor markups.
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

        if (!slider) return;

        function updateCalc() {
            const budget = parseFloat(slider.value) || 2500000;
            budgetDisplay.innerText = '$' + budget.toLocaleString();

            const trad = Math.round(budget * 0.18);
            tradFee.innerText = '$' + trad.toLocaleString();

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

// ── 4. Reframe /feasibility-plan/ (Page 1409) Header, Badges & Interactive Planner ──
add_filter('rank_math/frontend/title', function ($title) {
    if (is_page('feasibility-plan') || (is_singular() && preg_match('#feasibility-plan#i', $_SERVER['REQUEST_URI'] ?? ''))) {
        return 'Custom Home, Estate & BC Hydro Civil Pre-Construction Cost & Servicing Planner | BC #52603';
    }
    return $title;
}, 99);

add_filter('rank_math/frontend/description', function ($desc) {
    if (is_page('feasibility-plan') || (is_singular() && preg_match('#feasibility-plan#i', $_SERVER['REQUEST_URI'] ?? ''))) {
        return 'Custom Home, Estate & BC Hydro Civil (ES54) Pre-Construction Cost & Servicing Planner across West Vancouver, Whistler, Squamish & North Vancouver. BC Licensed Builder #52603 & 2-5-10 Warranty.';
    }
    return $desc;
}, 99);

add_filter('the_content', 'keystone_possibilities_inject_feasibility_tools', 20);
function keystone_possibilities_inject_feasibility_tools($content) {
    if (is_page('feasibility-plan') || (is_singular() && preg_match('#feasibility-plan#i', $_SERVER['REQUEST_URI'] ?? ''))) {
        $estimator = do_shortcode('[keystone_bill44_estimator]');
        $open_book = do_shortcode('[keystone_open_book_calculator]');

        ob_start();
        ?>
        <div class="kp-feasibility-page-wrapper" style="background-color: #04070d; color: #e2e8f0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding-bottom: 4rem; margin: 0 auto; width: 100%; max-width: 100% !important;">

            <!-- 1. Hero Header: Custom Home, Estate & BC Hydro Civil Pre-Construction Cost & Servicing Planner -->
            <header style="text-align: center; padding: 2.2rem 1.5rem 1.5rem 1.5rem; background: radial-gradient(circle at top center, rgba(212, 175, 55, 0.16) 0%, rgba(10, 15, 25, 0.9) 60%, rgba(4, 7, 13, 1) 100%); border-bottom: 1px solid rgba(212, 175, 55, 0.22);">
                <div style="max-width: 1080px; margin: 0 auto; text-align: center;">
                    
                    <!-- Credential Authority Badge -->
                    <div style="text-align: center; margin-bottom: 12px;">
                        <span class="kp-badge" style="display: inline-flex; align-items: center; gap: 8px; font-family: 'Outfit', sans-serif; font-size: 0.78rem; font-weight: 800; color: #f6d365; background: rgba(212, 175, 55, 0.12); padding: 6px 20px; border-radius: 9999px; border: 1px solid rgba(212, 175, 55, 0.45); text-transform: uppercase; letter-spacing: 0.08em; box-shadow: 0 0 18px rgba(212, 175, 55, 0.2);">
                            🏛️ BC Housing Licensed Builder #52603 • BC Hydro Civil Contractor ES54 • 2-5-10 National Home Warranty
                        </span>
                    </div>

                    <!-- Regional Corridor Switcher Pills -->
                    <div style="display: flex; justify-content: center; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 1rem;">
                        <a href="/west-vancouver-custom-homes/" style="display: inline-flex; align-items: center; padding: 6px 16px; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; text-decoration: none; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 9999px;">West Vancouver →</a>
                        <a href="/whistler-custom-homes/" style="display: inline-flex; align-items: center; padding: 6px 16px; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; text-decoration: none; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 9999px;">Whistler →</a>
                        <a href="/squamish-custom-homes/" style="display: inline-flex; align-items: center; padding: 6px 16px; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; text-decoration: none; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 9999px;">Squamish →</a>
                        <a href="/north-vancouver-custom-homes/" style="display: inline-flex; align-items: center; padding: 6px 16px; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; text-decoration: none; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 9999px;">North Vancouver →</a>
                        <a href="/bc-hydro-registered-civil-contractor/" style="display: inline-flex; align-items: center; padding: 6px 16px; font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-decoration: none; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 9999px;">BC Hydro Civil ES54 →</a>
                        <span style="display: inline-flex; align-items: center; padding: 6px 18px; font-size: 0.78rem; font-weight: 800; color: #f6d365; background: rgba(212, 175, 55, 0.2); border: 1.5px solid #d4af37; border-radius: 9999px;">📐 Cost &amp; Build Plan</span>
                    </div>

                    <!-- H1 Master Headline -->
                    <h1 class="hero-master-title" style="font-family: 'Cinzel', 'Outfit', serif !important; font-size: clamp(1.75rem, 3.2vw, 2.75rem) !important; font-weight: 900 !important; line-height: 1.18 !important; letter-spacing: 0.01em !important; color: #FFFFFF !important; max-width: 980px !important; margin: 0 auto 0.75rem auto !important; text-align: center !important; text-transform: uppercase !important;">
                        CUSTOM HOME, ESTATE &amp; BC HYDRO CIVIL<br>
                        <span class="gold-gradient" style="background: linear-gradient(135deg, #FFF2C6 0%, #D4AF37 50%, #A38025 100%) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; display: inline-block;">PRE-CONSTRUCTION COST &amp; SERVICING PLANNER</span>
                    </h1>

                    <p style="font-size: 1rem; line-height: 1.6; color: #cbd5e1; max-width: 840px; margin: 0 auto;">
                        De-risk your luxury custom home, architectural mountain/coastal estate, or BC Hydro ES54 underground utility build before blueprint lock-in across West Vancouver, Whistler, Squamish, and North Vancouver.
                    </p>
                </div>
            </header>

            <!-- 2. Interactive Custom Home, Estate & BC Hydro Civil Planner (Above the Fold) -->
            <section id="custom-build-planner" style="padding: 0 1rem;">
                <?php echo $estimator; ?>
            </section>

            <!-- 3. Open-Book Cost Transparency Calculator -->
            <section id="fiduciary-calculator" style="padding: 0 1rem;">
                <?php echo $open_book; ?>
            </section>

            <!-- 4. 2026 British Columbia Custom Home & Civil Cost Benchmarks -->
            <section style="padding: 3rem 1.5rem; max-width: 1120px; margin: 0 auto;">
                <div style="text-align: center; margin-bottom: 2.5rem;">
                    <div style="color: #f6d365; font-size: 0.8rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 0.5rem;">
                        2026 SEA-TO-SKY &amp; NORTH SHORE BENCHMARKS
                    </div>
                    <h2 style="font-family: 'Outfit', sans-serif; font-size: clamp(1.7rem, 3vw, 2.3rem); font-weight: 900; color: #ffffff; margin: 0 0 0.75rem 0;">
                        Turnkey Custom Home, Estate &amp; BC Hydro ES54 Civil Standards
                    </h2>
                    <p style="color: #94a3b8; max-width: 760px; margin: 0 auto; font-size: 0.98rem; line-height: 1.6;">
                        Transparent CCDC 5B pre-construction budgeting grounded in active sub-trade tenders across West Vancouver, Whistler, Squamish, and North Vancouver:
                    </p>
                </div>

                <div class="kp-grid-3col" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 1.5rem;">
                    <!-- Card 1 -->
                    <div class="kp-card" style="border-top: 4px solid #d4af37; border-radius: 18px; padding: 1.8rem;">
                        <span class="kp-badge" style="font-size: 0.72rem; padding: 4px 12px; margin-bottom: 0.8rem;">WEST VANCOUVER &amp; WHISTLER</span>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #ffffff; margin-bottom: 0.3rem;">
                            $550 – $850+ <span style="font-size: 0.95rem; color: #94a3b8; font-weight: 500;">/ sq. ft.</span>
                        </div>
                        <h3 style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; margin: 0.3rem 0 0.7rem 0;">
                            Luxury Custom Single-Family Estates
                        </h3>
                        <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; margin: 0;">
                            Bespoke architectural concrete, heavy timber post-and-beam, granitic bedrock micropiling, Step Code 5 triple-pane glazing, and statutory 2-5-10 National Home Warranty.
                        </p>
                    </div>

                    <!-- Card 2 -->
                    <div class="kp-card" style="border-top: 4px solid #38bdf8; border-radius: 18px; padding: 1.8rem;">
                        <span class="kp-badge" style="color: #38bdf8; border-color: rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.1); font-size: 0.72rem; padding: 4px 12px; margin-bottom: 0.8rem;">SQUAMISH &amp; NORTH VANCOUVER</span>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #ffffff; margin-bottom: 0.3rem;">
                            $425 – $575 <span style="font-size: 0.95rem; color: #94a3b8; font-weight: 500;">/ sq. ft.</span>
                        </div>
                        <h3 style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; margin: 0.3rem 0 0.7rem 0;">
                            Mountain Modern Homes, Renovations &amp; Carriage Builds
                        </h3>
                        <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; margin: 0;">
                            High-performance coastal &amp; mountain custom residences, structural additions, luxury duplexes, and multi-generational carriage homes engineered to Step Code 4/5.
                        </p>
                    </div>

                    <!-- Card 3 -->
                    <div class="kp-card" style="border-top: 4px solid #f6d365; border-radius: 18px; padding: 1.8rem;">
                        <span class="kp-badge" style="font-size: 0.72rem; padding: 4px 12px; margin-bottom: 0.8rem;">BC HYDRO LIST ES54 CIVIL</span>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 900; color: #ffffff; margin-bottom: 0.3rem;">
                            $55K – $185K+ <span style="font-size: 0.95rem; color: #94a3b8; font-weight: 500;">turnkey civil</span>
                        </div>
                        <h3 style="color: #f6d365; font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; margin: 0.3rem 0 0.7rem 0;">
                            BC Hydro ES54 Underground Civil &amp; PMT Vaults
                        </h3>
                        <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.6; margin: 0;">
                            Direct ES54 civil utility execution: primary/secondary underground duct banks, 200A–600A service upgrades, Pad-Mounted Transformer (PMT) vaults, and bedrock excavation.
                        </p>
                    </div>
                </div>
            </section>

            <!-- 5. Master Builder Superintendence Card (Wayne Stevenson) -->
            <section style="padding: 1rem 1.5rem 3rem 1.5rem; max-width: 1120px; margin: 0 auto;">
                <div class="kp-card" style="border: 1.5px solid rgba(212, 175, 55, 0.45); border-radius: 18px; padding: clamp(24px, 4vw, 38px); background: #070b14;">
                    <div style="display: flex; flex-wrap: wrap; gap: 28px; align-items: center;">
                        <div style="flex: 0 0 240px; margin: 0 auto; text-align: center;">
                            <div style="border-radius: 14px; overflow: hidden; border: 2px solid #d4af37; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7); max-width: 230px; margin: 0 auto;">
                                <img decoding="async" src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/wayne_whistler_builder_avatar.jpg" alt="Wayne Stevenson — Licensed Residential Builder #52603 and BC Hydro ES54 Civil Superintendent" style="width: 100%; height: auto; display: block;" loading="lazy">
                            </div>
                            <div style="margin-top: 12px;">
                                <strong style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.15rem; display: block;">Wayne Stevenson</strong>
                                <span style="color: #d4af37; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Licensed Builder #52603 &amp; Civil Superintendent</span>
                            </div>
                        </div>
                        <div style="flex: 1 1 480px;">
                            <span class="kp-badge" style="margin-bottom: 10px;">DIRECT BUILDER LEADERSHIP</span>
                            <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.75rem; font-weight: 900; color: #ffffff; margin: 0 0 0.85rem 0;">
                                On-Site Custom Home &amp; Civil Authority. Zero Paper Brokerage.
                            </h3>
                            <p style="color: #cbd5e1; font-size: 0.96rem; line-height: 1.7; margin: 0 0 1.2rem 0;">
                                Every custom home build and pre-construction servicing plan is led directly by Wayne Stevenson. With decades of hands-on structural concrete, steep-slope bedrock anchoring, and BC Hydro ES54 underground utility execution across West Vancouver, Whistler, Squamish, and North Vancouver, you receive direct builder accountability from initial concept to 2-5-10 warranty occupancy.
                            </p>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; font-size: 0.85rem; color: #cbd5e1; margin-bottom: 1.4rem;">
                                <div><strong style="color: #f6d365;">• BC Housing License:</strong> #52603</div>
                                <div><strong style="color: #f6d365;">• BC Hydro Status:</strong> ES54 Civil Contractor</div>
                                <div><strong style="color: #f6d365;">• Home Warranty:</strong> Statutory 2-5-10 WBI</div>
                                <div><strong style="color: #f6d365;">• Contract Model:</strong> CCDC 5B Open-Book</div>
                            </div>
                            <a href="tel:+16048489688" class="kp-btn-primary" style="display: inline-flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #d4af37 0%, #c4a265 50%, #aa8232 100%); color: #04070d !important; font-family: 'Outfit', sans-serif !important; font-weight: 900 !important; font-size: 0.88rem !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; padding: 13px 28px !important; border-radius: 9999px !important; text-decoration: none !important; border: 1px solid #f6d365 !important;">
                                SPEAK DIRECTLY WITH WAYNE: (604) 848-9688
                            </a>
                        </div>
                    </div>
                </div>
            </section>

        </div>
        <?php
        return ob_get_clean();
    }
    return $content;
}
