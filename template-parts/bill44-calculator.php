<?php
/**
 * Template Part: Interactive 9-Corridor Bill 44 SSMUH, Slope & Open-Book CCDC 5B Console
 *
 * Pre-selectable via $args['default_corridor'], square-footage slider 2,200–12,000 SF,
 * Build Mode toggle (Custom Estate vs Bill 44 4–6 Unit Multiplex), ES54 Civil Servicing tier,
 * live CCDC 5B fiduciary savings vs traditional 20%+ GC sub-markup cascade, live bylaw/snow/geotech
 * readout, and 1-click auto-populate into #kp-lead-intake-form.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_default_corridor = isset( $args['default_corridor'] ) ? sanitize_title( (string) $args['default_corridor'] ) : 'west-vancouver';
$kp_section_id       = isset( $args['section_id'] ) ? sanitize_html_class( (string) $args['section_id'] ) : 'calculator';

$kp_corridor_models = array(
	'west-vancouver'   => array(
		'name'         => 'West Vancouver (British Properties / Caulfeild)',
		'estate_low'   => 690,
		'estate_high'  => 980,
		'multi_low'    => 510,
		'multi_high'   => 675,
		'bylaw'        => 'DWV Bylaw No. 4364 (15m Creek Setback) + Bill 44 SSMUH Infill',
		'loads'        => 'Coastal Granite Micropiles · Seismic Sa(0.2) = 0.88g · Step Code 5 / EL-4',
		'geotech_note' => 'Steep granodiorite bluff benching, rock anchors, and pumped storm attenuation.',
		'horizon'      => '16–22 Months (Build) + 5–8 Mo Permit',
	),
	'whistler'         => array(
		'name'         => 'Whistler (Sunridge / Kadenwood / Alta Vista)',
		'estate_low'   => 720,
		'estate_high'  => 1050,
		'multi_low'    => 545,
		'multi_high'   => 710,
		'bylaw'        => 'RMOW Zoning + Wildfire Protection DPA Class A Non-Combustible Cladding',
		'loads'        => 'Extreme Ground Snow Sg = 6.2–8.1 kPa · Cold-Roof Ice-Dam Ventilation · Step Code 5',
		'geotech_note' => 'Blasted granite ridge tie-backs, heated driveway snow-melt manifolds & alpine logistics.',
		'horizon'      => '18–24 Months (Seasonal Rock Window)',
	),
	'squamish'         => array(
		'name'         => 'Squamish HQ (Tantalus / Garibaldi Highlands / Brackendale)',
		'estate_low'   => 540,
		'estate_high'  => 760,
		'multi_low'    => 425,
		'multi_high'   => 560,
		'bylaw'        => 'District of Squamish Bill 44 SSMUH (3–6 Units) & Flood Construction Level (FCL)',
		'loads'        => 'Snow Load Sg = 3.4 kPa · FCL Structural Fill / Raft Slab · Step Code 4/5 & EL-4',
		'geotech_note' => 'Keystone HQ dispatch (1 Watts Point Rd) — immediate self-performed ES54 civil & rock prep.',
		'horizon'      => '12–16 Months (Fast-Track Local Supervision)',
	),
	'north-vancouver'  => array(
		'name'         => 'North Vancouver (Edgemont / Upper Lonsdale / Lynn Valley)',
		'estate_low'   => 595,
		'estate_high'  => 840,
		'multi_low'    => 455,
		'multi_high'   => 595,
		'bylaw'        => 'DNV / CNV SSMUH 4–6 Unit Zoning & Streamside Protection (SPEA)',
		'loads'        => 'High Coastal Rainfall BCBC 9.27 Rainscreen · Glacial Till Shoring · Step Code 5',
		'geotech_note' => 'High hydrostatic water-table perimeter drainage, active sub-slab radon stack & tree protection.',
		'horizon'      => '14–19 Months',
	),
	'vancouver-r1-1'   => array(
		'name'         => 'Vancouver R1-1 Multiplex & Point Grey / Westside',
		'estate_low'   => 640,
		'estate_high'  => 920,
		'multi_low'    => 465,
		'multi_high'   => 615,
		'bylaw'        => 'City of Vancouver R1-1 District Schedule (1.0 FSR, up to 6–8 Units) & VBBL 2025',
		'loads'        => 'NFPA 13D/13R Fire Sprinklers · 2" Domestic Water Main · ES54 400A–600A PMT Pad',
		'geotech_note' => 'Zero-lot-line shoring, adaptable threshold sills, STC 55+ party walls & PMT 3.0m hot-stick clearance.',
		'horizon'      => '14–18 Months',
	),
	'coquitlam'        => array(
		'name'         => 'Coquitlam (Burke Mountain / Maillardville / Austin Heights)',
		'estate_low'   => 530,
		'estate_high'  => 735,
		'multi_low'    => 420,
		'multi_high'   => 545,
		'bylaw'        => 'City of Coquitlam SSMUH 3–6 Unit Multiplex & Transit-Oriented Areas (TOA)',
		'loads'        => 'Foothill Slope Detention Tanks · Step Code 4/5 · Multi-Meter 400A EVEMS Switchgear',
		'geotech_note' => 'Engineered storm retention chambers, steep-grade benching on Burke Mountain & ES54 DB2 ducting.',
		'horizon'      => '13–17 Months',
	),
	'sunshine-coast'   => array(
		'name'         => 'Sunshine Coast (Sechelt / Davis Bay / Gibsons / Halfmoon Bay)',
		'estate_low'   => 560,
		'estate_high'  => 795,
		'multi_low'    => 440,
		'multi_high'   => 575,
		'bylaw'        => 'District of Sechelt / SCRD Coastal Foreshore Setback & Geotechnical Hazard DPAs',
		'loads'        => 'Hourly Wind Uplift q100 = 0.55 kPa · Hurricane Strapping · Marine-Grade Fasteners',
		'geotech_note' => 'Coastal granite blasting, boulder retaining structures, coordinated ferry/barge material drops.',
		'horizon'      => '14–19 Months',
	),
	'pemberton'        => array(
		'name'         => 'Pemberton (Meadows / Benchlands / Acreage Compounds)',
		'estate_low'   => 575,
		'estate_high'  => 825,
		'multi_low'    => 450,
		'multi_high'   => 590,
		'bylaw'        => 'Village of Pemberton / SLRD Acreage Compound & Agricultural Floodplain Bylaws',
		'loads'        => 'Deep Alpine Frost Penetration · Heavy Timber Snow Framing · 800A Solar/Battery Microgrid',
		'geotech_note' => 'Long-run self-performed BC Hydro ES54 primary duct banks, private PMT vaults & well/septic civil.',
		'horizon'      => '15–20 Months',
	),
	'vancouver-island' => array(
		'name'         => 'Vancouver Island & Greater Victoria (Oak Bay / Saanich / Nanaimo)',
		'estate_low'   => 565,
		'estate_high'  => 815,
		'multi_low'    => 435,
		'multi_high'   => 575,
		'bylaw'        => 'Victoria / Saanich Missing-Middle SSMUH & Coastal Bluff Marine DPAs',
		'loads'        => 'High Seismic Zone PGA > 0.58g · Simpson ATS Continuous Rod Shear Walls · Step Code 4/5',
		'geotech_note' => 'Exposed coastal basalt/granite pinning, marine salt-spray rainscreen detailing & VRBA trade network.',
		'horizon'      => '14–19 Months',
	),
);

// Normalize common slug aliases (e.g. vancouver -> vancouver-r1-1, west-vancouver-custom-homes -> west-vancouver).
$kp_slug_aliases = array(
	'vancouver'                              => 'vancouver-r1-1',
	'vancouver-multiplex'                    => 'vancouver-r1-1',
	'vancouver-r1-1-multiplex-builder'       => 'vancouver-r1-1',
	'west-vancouver-custom-homes'            => 'west-vancouver',
	'whistler-custom-homes'                  => 'whistler',
	'squamish-custom-homes'                  => 'squamish',
	'north-vancouver-custom-homes'           => 'north-vancouver',
	'coquitlam-custom-homes-multiplex'       => 'coquitlam',
	'sunshine-coast-custom-homes'            => 'sunshine-coast',
	'pemberton-luxury-builder'               => 'pemberton',
	'vancouver-island-custom-homes'          => 'vancouver-island',
);
if ( isset( $kp_slug_aliases[ $kp_default_corridor ] ) ) {
	$kp_default_corridor = $kp_slug_aliases[ $kp_default_corridor ];
}
if ( ! isset( $kp_corridor_models[ $kp_default_corridor ] ) ) {
	$kp_default_corridor = 'west-vancouver';
}

$kp_calc_uid = wp_unique_id( 'kp-calc-' );

if ( empty( $GLOBALS['kp_v3_bill44_calc_css'] ) ) :
	$GLOBALS['kp_v3_bill44_calc_css'] = true;
	?>
	<style id="kp-v3-bill44-calc-styles">
		.kp-calc-section {
			padding: clamp(56px, 7vw, 92px) 0;
			background: #04070d;
			color: #f8fafc;
			border-top: 1px solid rgba(212, 175, 55, 0.16);
		}
		.kp-calc-wrap {
			width: min(1340px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-calc-shell {
			display: grid;
			grid-template-columns: 1.08fr 0.92fr;
			gap: 24px;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.34);
			border-radius: 22px;
			padding: clamp(18px, 3.5vw, 34px);
			box-shadow: 0 28px 64px rgba(0, 0, 0, 0.65);
		}
		@media (max-width: 980px) {
			.kp-calc-shell {
				grid-template-columns: 1fr;
			}
		}
		.kp-calc-kicker {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: #d4af37;
			margin-bottom: 8px;
		}
		.kp-calc-h2 {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.55rem, 2.9vw, 2.25rem);
			font-weight: 700;
			line-height: 1.16;
			color: #f8fafc;
			margin: 0 0 10px;
		}
		.kp-calc-lead {
			font-size: 0.94rem;
			line-height: 1.6;
			color: #cbd5e1;
			margin: 0 0 24px;
			max-width: 820px;
		}
		.kp-calc-controls {
			display: flex;
			flex-direction: column;
			gap: 18px;
		}
		.kp-calc-field label {
			display: flex;
			justify-content: space-between;
			align-items: center;
			font-size: 0.78rem;
			font-weight: 700;
			letter-spacing: 0.04em;
			text-transform: uppercase;
			color: #cbd5e1;
			margin-bottom: 8px;
		}
		.kp-calc-select {
			width: 100%;
			min-height: 46px;
			padding: 10px 14px;
			border-radius: 12px;
			background: #04070d;
			border: 1px solid rgba(212, 175, 55, 0.34);
			color: #f8fafc;
			font-size: 0.9rem;
			font-weight: 600;
		}
		.kp-calc-seg {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 8px;
			background: #04070d;
			padding: 5px;
			border-radius: 14px;
			border: 1px solid rgba(212, 175, 55, 0.25);
		}
		@media (max-width: 480px) {
			.kp-calc-seg {
				grid-template-columns: 1fr;
			}
		}
		.kp-calc-seg button {
			min-height: 42px;
			border-radius: 10px;
			border: 1px solid transparent;
			background: transparent;
			color: #cbd5e1;
			font-size: 0.82rem;
			font-weight: 700;
			cursor: pointer;
			padding: 8px 12px;
		}
		.kp-calc-seg button.is-active {
			background: linear-gradient(135deg, rgba(212, 175, 55, 0.24), rgba(200, 164, 93, 0.1));
			border-color: #d4af37;
			color: #f8fafc;
		}
		.kp-calc-range {
			width: 100%;
			accent-color: #d4af37;
			cursor: pointer;
		}
		.kp-calc-output {
			background: #04070d;
			border: 1px solid rgba(212, 175, 55, 0.36);
			border-radius: 18px;
			padding: clamp(18px, 3vw, 26px);
			display: flex;
			flex-direction: column;
			gap: 14px;
		}
		.kp-calc-price-big {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.65rem, 3.2vw, 2.35rem);
			font-weight: 800;
			color: #d4af37;
			line-height: 1.12;
		}
		.kp-calc-kpi-grid {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 10px;
		}
		@media (max-width: 480px) {
			.kp-calc-kpi-grid {
				grid-template-columns: 1fr;
			}
		}
		.kp-calc-kpi {
			background: #0a101d;
			border: 1px solid rgba(255, 255, 255, 0.08);
			border-radius: 12px;
			padding: 12px 14px;
		}
		.kp-calc-kpi-lbl {
			font-size: 0.68rem;
			text-transform: uppercase;
			letter-spacing: 0.06em;
			color: #94a3b8;
			font-weight: 700;
		}
		.kp-calc-kpi-val {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.96rem;
			font-weight: 700;
			color: #f8fafc;
			margin-top: 4px;
		}
		.kp-calc-savings-box {
			background: linear-gradient(135deg, rgba(212, 175, 55, 0.13), rgba(56, 189, 248, 0.06));
			border: 1px solid rgba(212, 175, 55, 0.44);
			border-radius: 14px;
			padding: 14px 16px;
		}
		.kp-calc-spec-list {
			display: flex;
			flex-direction: column;
			gap: 8px;
			font-size: 0.8rem;
			color: #cbd5e1;
			line-height: 1.5;
			border-top: 1px solid rgba(255, 255, 255, 0.08);
			padding-top: 12px;
		}
		.kp-calc-cta {
			width: 100%;
			min-height: 48px;
			border-radius: 999px;
			border: none;
			background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 52%, #b89028 100%);
			color: #04070d;
			font-family: 'Outfit', sans-serif;
			font-size: 0.92rem;
			font-weight: 800;
			cursor: pointer;
			padding: 12px 20px;
			margin-top: auto;
			transition: transform 0.18s ease, box-shadow 0.18s ease;
		}
		.kp-calc-cta:hover {
			transform: translateY(-1px);
			box-shadow: 0 12px 28px rgba(212, 175, 55, 0.36);
		}
	</style>
<?php endif; ?>

<section id="<?php echo esc_attr( $kp_section_id ); ?>" class="kp-calc-section" data-kp-calc="<?php echo esc_attr( $kp_calc_uid ); ?>">
	<div class="kp-calc-wrap">
		<div class="kp-calc-kicker">OPEN-BOOK CCDC 5B PRO-FORMA CONSOLE · 9 BC ENGINEERING CORRIDORS</div>
		<h2 class="kp-calc-h2">Model Slope, Bill 44 Density, ES54 Civil &amp; Fiduciary Savings Before You Offer.</h2>
		<p class="kp-calc-lead">Compare transparent Open-Book CCDC 5B construction management (raw 3-bid trade tenders + builder lumber/supply discounts) against traditional opaque general contractor sub-markup cascades.</p>

		<div class="kp-calc-shell">
			<div class="kp-calc-controls">
				<div class="kp-calc-field">
					<label for="<?php echo esc_attr( $kp_calc_uid ); ?>-corridor">
						<span>1. BC Municipal Corridor</span>
						<span style="color:#d4af37;font-family:'JetBrains Mono',monospace;">2026 BYLAW SYNCED</span>
					</label>
					<select id="<?php echo esc_attr( $kp_calc_uid ); ?>-corridor" class="kp-calc-select" data-kp-calc-corridor>
						<?php foreach ( $kp_corridor_models as $c_slug => $c_data ) : ?>
							<option value="<?php echo esc_attr( $c_slug ); ?>" <?php selected( $kp_default_corridor, $c_slug ); ?>>
								<?php echo esc_html( $c_data['name'] ); ?>
							</option>
						<?php endforeach; ?>
					</select>
				</div>

				<div class="kp-calc-field">
					<label><span>2. Structural Program Mode</span></label>
					<div class="kp-calc-seg" role="group" aria-label="Build Mode">
						<button type="button" class="is-active" data-calc-mode="estate">Architectural Custom Estate</button>
						<button type="button" data-calc-mode="multiplex">Bill 44 4–6 Unit Multiplex</button>
					</div>
				</div>

				<div class="kp-calc-field">
					<label for="<?php echo esc_attr( $kp_calc_uid ); ?>-sf">
						<span>3. Conditioned Gross Floor Area</span>
						<strong style="color:#f8fafc;font-family:'JetBrains Mono',monospace;font-size:0.9rem;" data-calc-sf-readout>4,800 SF</strong>
					</label>
					<input
						type="range"
						id="<?php echo esc_attr( $kp_calc_uid ); ?>-sf"
						class="kp-calc-range"
						min="2200"
						max="12000"
						step="100"
						value="4800"
						data-calc-sf
					/>
					<div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#94a3b8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
						<span>2,200 SF</span>
						<span>6,500 SF</span>
						<span>12,000 SF</span>
					</div>
				</div>

				<div class="kp-calc-field">
					<label for="<?php echo esc_attr( $kp_calc_uid ); ?>-slope"><span>4. Topography, Shoring &amp; Bedrock Profile</span></label>
					<select id="<?php echo esc_attr( $kp_calc_uid ); ?>-slope" class="kp-calc-select" data-calc-slope>
						<option value="1.00">Competent Glacial Till / Bench (&lt;12% Grade · Standard Strip Footings)</option>
						<option value="1.14" selected>Steep Coastal / Alpine Slope (15%–30% Grade · Rock Pinning / Micropiles)</option>
						<option value="1.26">Cliffside Granite / High Hydrostatic FCL / Barged Access (&gt;30% Grade)</option>
					</select>
				</div>

				<div class="kp-calc-field">
					<label for="<?php echo esc_attr( $kp_calc_uid ); ?>-es54"><span>5. Self-Performed BC Hydro ES54 Civil &amp; Service Tier</span></label>
					<select id="<?php echo esc_attr( $kp_calc_uid ); ?>-es54" class="kp-calc-select" data-calc-es54>
						<option value="28000">200A Underground Secondary Duct Bank (DB2 PVC &ge;900mm Cover)</option>
						<option value="58000" selected>400A Estate / Multiplex Multi-Meter Switchgear + ES54 Civil Trenching</option>
						<option value="115000">600A–800A Primary Duct Bank + Private PMT Vault (CEC Rule 26-242 3.0m Clearance)</option>
					</select>
				</div>
			</div>

			<div class="kp-calc-output" aria-live="polite">
				<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#38bdf8;font-weight:700;">CLASS-C OPEN-BOOK CCDC 5B ENVELOPE</span>
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#d4af37;" data-calc-horizon></span>
				</div>

				<div class="kp-calc-price-big" data-calc-total>$3.84M – $5.42M CAD</div>

				<div class="kp-calc-kpi-grid">
					<div class="kp-calc-kpi">
						<div class="kp-calc-kpi-lbl">All-In Open-Book $/SF</div>
						<div class="kp-calc-kpi-val" data-calc-psf>$795 – $1,125 / SF</div>
					</div>
					<div class="kp-calc-kpi">
						<div class="kp-calc-kpi-lbl">ES54 Civil &amp; PMT Allocation</div>
						<div class="kp-calc-kpi-val" data-calc-civil>$58,000 Direct Civil</div>
					</div>
				</div>

				<div class="kp-calc-savings-box">
					<div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#f3e5ab;margin-bottom:4px;">
						Estimated Open-Book CCDC 5B Fiduciary Capital Preserved
					</div>
					<div style="font-family:'Outfit',sans-serif;font-size:1.35rem;font-weight:800;color:#f8fafc;" data-calc-savings>
						$410,000 – $595,000 Preserved
					</div>
					<div style="font-size:0.76rem;color:#cbd5e1;margin-top:4px;line-height:1.45;">
						Replaces traditional opaque 20%–25% GC sub-trade &amp; change-order markups with 100% open-book 3-bid tenders, direct #52603 trade pricing, and self-performed ES54 civil excavation.
					</div>
				</div>

				<div class="kp-calc-spec-list">
					<div><strong style="color:#f8fafc;">Active Bylaw Regime:</strong> <span data-calc-bylaw></span></div>
					<div><strong style="color:#f8fafc;">Structural &amp; Step Code Loads:</strong> <span data-calc-loads></span></div>
					<div><strong style="color:#f8fafc;">Superintendent Field Focus:</strong> <span data-calc-geotech></span></div>
				</div>

				<button type="button" class="kp-calc-cta" data-calc-populate>
					Load Scenario Into 48-Hr Principal Review &rarr;
				</button>
			</div>
		</div>
	</div>

	<script>
	(function() {
		var root = document.querySelector('[data-kp-calc="<?php echo esc_js( $kp_calc_uid ); ?>"]');
		if (!root) return;
		var models = <?php echo wp_json_encode( $kp_corridor_models ); ?>;
		var corrSel = root.querySelector('[data-kp-calc-corridor]');
		var modeBtns = Array.prototype.slice.call(root.querySelectorAll('[data-calc-mode]'));
		var sfInput = root.querySelector('[data-calc-sf]');
		var slopeSel = root.querySelector('[data-calc-slope]');
		var es54Sel = root.querySelector('[data-calc-es54]');
		var activeMode = 'estate';

		var sfOut = root.querySelector('[data-calc-sf-readout]');
		var totalOut = root.querySelector('[data-calc-total]');
		var psfOut = root.querySelector('[data-calc-psf]');
		var civilOut = root.querySelector('[data-calc-civil]');
		var savOut = root.querySelector('[data-calc-savings]');
		var horOut = root.querySelector('[data-calc-horizon]');
		var bylawOut = root.querySelector('[data-calc-bylaw]');
		var loadsOut = root.querySelector('[data-calc-loads]');
		var geoOut = root.querySelector('[data-calc-geotech]');

		function fmtM(n) {
			if (n >= 1000000) return '$' + (n / 1000000).toFixed(2) + 'M';
			return '$' + Math.round(n / 1000).toLocaleString() + 'K';
		}

		function recalc() {
			var slug = corrSel.value;
			var m = models[slug] || models['west-vancouver'];
			var sf = parseInt(sfInput.value, 10) || 4800;
			var slopeMult = parseFloat(slopeSel.value) || 1.0;
			var civilCost = parseInt(es54Sel.value, 10) || 58000;

			var baseLow = activeMode === 'multiplex' ? m.multi_low : m.estate_low;
			var baseHigh = activeMode === 'multiplex' ? m.multi_high : m.estate_high;

			var psfLow = Math.round(baseLow * slopeMult);
			var psfHigh = Math.round(baseHigh * slopeMult);

			var lowTotal = (psfLow * sf) + civilCost;
			var highTotal = (psfHigh * sf) + civilCost;

			// Fiduciary open-book CCDC 5B delta (~10.5% net savings vs opaque 22%+ GC sub-markup cascade + civil sub markup).
			var savLow = Math.round((lowTotal * 0.102) / 5000) * 5000;
			var savHigh = Math.round((highTotal * 0.118) / 5000) * 5000;

			sfOut.textContent = sf.toLocaleString() + ' SF';
			totalOut.textContent = fmtM(lowTotal) + ' – ' + fmtM(highTotal) + ' CAD';
			psfOut.textContent = '$' + psfLow.toLocaleString() + ' – $' + psfHigh.toLocaleString() + ' / SF';
			civilOut.textContent = '$' + civilCost.toLocaleString() + ' Self-Performed';
			savOut.textContent = '$' + savLow.toLocaleString() + ' – $' + savHigh.toLocaleString() + ' Preserved';
			horOut.textContent = m.horizon;
			bylawOut.textContent = m.bylaw;
			loadsOut.textContent = m.loads;
			geoOut.textContent = m.geotech_note;
		}

		modeBtns.forEach(function(btn) {
			btn.addEventListener('click', function() {
				activeMode = btn.getAttribute('data-calc-mode');
				modeBtns.forEach(function(b) { b.classList.toggle('is-active', b === btn); });
				if (activeMode === 'multiplex' && parseInt(sfInput.value, 10) < 5200) {
					sfInput.value = '6200';
				}
				recalc();
			});
		});

		[corrSel, sfInput, slopeSel, es54Sel].forEach(function(el) {
			el.addEventListener('input', recalc);
			el.addEventListener('change', recalc);
		});

		root.querySelector('[data-calc-populate]').addEventListener('click', function() {
			var slug = corrSel.value;
			var m = models[slug] || models['west-vancouver'];
			var sf = parseInt(sfInput.value, 10) || 4800;
			var summary = 'Console Scenario: ' + m.name + ' | ' + (activeMode === 'multiplex' ? 'Bill 44 4-6 Unit Multiplex' : 'Custom Architectural Estate') + ' | ' + sf.toLocaleString() + ' SF | Est. ' + totalOut.textContent + ' (' + psfOut.textContent + ')';

			var form = document.getElementById('kp-lead-intake-form');
			if (form) {
				var locField = form.querySelector('[name="location"]');
				if (locField) locField.value = slug;
				var typeField = form.querySelector('[name="project_type"]');
				if (typeField) typeField.value = activeMode === 'multiplex' ? 'Bill 44 4-6 Unit Multiplex' : 'Slope-Critical Custom Estate';
				var budField = form.querySelector('[name="budget"]');
				if (budField) budField.value = totalOut.textContent;
				var msgField = form.querySelector('[name="message"]');
				if (msgField) {
					msgField.value = summary + (msgField.value ? '\n' + msgField.value : '');
				}
				form.scrollIntoView({ behavior: 'smooth', block: 'center' });
				var firstInput = form.querySelector('input[name="name"]');
				if (firstInput) setTimeout(function() { firstInput.focus(); }, 450);
			} else {
				window.location.href = '<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>?corridor=' + encodeURIComponent(slug);
			}
		});

		recalc();
	})();
	</script>
</section>
