<?php
/**
 * Flagship Front Page — Keystone Possibilities Ltd. v3.0 Sovereign Rebuild
 *
 * Implements Wayne Stevenson's approved "Best of Both" Master Combined Flagship:
 * 1) Split Principal Hero + Above-the-Fold 48-Hr Lot & MLS® Quick-Intake (Y < 660px mobile CTA)
 * 2) 4K Watch Superintendent Briefing Theater (kLsNyKvQswg + JwtaaZlrFeE + HBy6NQQS3ks)
 * 3) Signature Portfolio Cinema Reel (9 real residences / 42 photos + 2 real civil items)
 * 4) 17-Certificate Statutory & Qualification Museum Reel
 * 5) Interactive 9-Corridor Bill 44, Slope & Open-Book CCDC 5B Command Console
 * 6) 9-Corridor BC Engineering Matrix
 * 7) Realtor® (BCFSA Rule 5-11) & AIBC Architect Pre-Offer Desk Teaser
 * 8) Visible Executive FAQ Accordion + Direct Principal Consultation Desk
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_wayne_portrait = 'https://keystonepossibilities.ca/wp-content/uploads/2026/10/wayne_possibilities_coastal_estate.jpg';
$kp_sunridge_thumb = 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.07-pm.png';

$kp_matrix_corridors = array(
	array(
		'slug'  => 'west-vancouver',
		'url'   => home_url( '/west-vancouver-custom-homes/' ),
		'title' => 'West Vancouver',
		'sub'   => 'British Properties · Caulfeild · Altamont',
		'spec'  => 'Granite bedrock micropiles, post-tensioned rock anchors, DWV Creek Bylaw 4364 (15m setback), and Step Code 5 / EL-4 cliffside estates.',
		'tag'   => 'BUILT: BALLANTREE RESIDENCE',
	),
	array(
		'slug'  => 'whistler',
		'url'   => home_url( '/whistler-custom-homes/' ),
		'title' => 'Whistler Alpine',
		'sub'   => 'Sunridge Plateau · Kadenwood · Alta Vista',
		'spec'  => 'BCBC Part 4 extreme ground snow loads (Sg = 6.2–8.1 kPa), RMOW Class A FireSmart DPAs, cold-roof ventilation, and hydronic snow-melt.',
		'tag'   => 'BUILT: SUNRIDGE RESIDENCE',
	),
	array(
		'slug'  => 'squamish',
		'url'   => home_url( '/squamish-custom-homes/' ),
		'title' => 'Squamish HQ',
		'sub'   => 'Tantalus · Garibaldi Highlands · Brackendale',
		'spec'  => '1 Watts Point Rd headquarters dispatch. Flood Construction Level (FCL) structural rafts, 3.4 kPa snow loads, Bill 44 multiplexes & ES54 civil.',
		'tag'   => 'ACTIVE HQ · #52603',
	),
	array(
		'slug'  => 'north-vancouver',
		'url'   => home_url( '/north-vancouver-custom-homes/' ),
		'title' => 'North Vancouver',
		'sub'   => 'Edgemont · Upper Lonsdale · Lynn Valley',
		'spec'  => 'Glacial-till perimeter shoring, coastal rainscreen capillary breaks (BCBC 9.27), active sub-slab radon stacks, and DNV/CNV SSMUH infill.',
		'tag'   => 'BUILT: ST ANDREWS RESIDENCE',
	),
	array(
		'slug'  => 'vancouver-r1-1',
		'url'   => home_url( '/vancouver-r1-1-multiplex-builder/' ),
		'title' => 'Vancouver R1-1 & Westside',
		'sub'   => 'Point Grey · Dunbar · Kitsilano · R1-1 6-Plex',
		'spec'  => '1.0 FSR R1-1 multiplex engineering: 2" water mains, NFPA 13D/13R sprinklers, STC 55+ party walls, and ES54 400A–600A PMT clearances.',
		'tag'   => 'BUILT: DICKINSON · WEST RIDGE · PRIMA',
	),
	array(
		'slug'  => 'coquitlam',
		'url'   => home_url( '/coquitlam-custom-homes-multiplex/' ),
		'title' => 'Coquitlam',
		'sub'   => 'Burke Mountain · Maillardville · TOA Corridors',
		'spec'  => 'Bill 44 3–6 unit SSMUH infill and Burke Mountain slope benching, engineered storm detention chambers, and 400A EVEMS multi-metering.',
		'tag'   => 'SSMUH & FOOTHILL CIVIL',
	),
	array(
		'slug'  => 'sunshine-coast',
		'url'   => home_url( '/sunshine-coast-custom-homes/' ),
		'title' => 'Sunshine Coast',
		'sub'   => 'Sechelt · Davis Bay · Trail Bay · Sandy Hook',
		'spec'  => 'Coastal wind uplift (q100 = 0.55 kPa), granite footing pinning, boulder retaining walls, ES54 underground DB2 conduit, and barged drops.',
		'tag'   => 'BUILT: PIPER · COMPASS · SULLIVAN',
	),
	array(
		'slug'  => 'pemberton',
		'url'   => home_url( '/pemberton-luxury-builder/' ),
		'title' => 'Pemberton Compounds',
		'sub'   => 'Pemberton Meadows · Benchlands · SLRD Acreage',
		'spec'  => 'Private acreage estates, long-run BC Hydro ES54 primary duct banks, private 800A solar/battery microgrid vaults, and deep-frost foundations.',
		'tag'   => '800A MICROGRID & ES54 CIVIL',
	),
	array(
		'slug'  => 'vancouver-island',
		'url'   => home_url( '/vancouver-island-custom-homes/' ),
		'title' => 'Vancouver Island',
		'sub'   => 'Greater Victoria · Oak Bay · Saanich · Nanaimo',
		'spec'  => 'High-seismic zone (PGA > 0.58g) ductile shear walls, coastal basalt/granite anchoring, missing-middle multiplexes, and VRBA trade governance.',
		'tag'   => 'HIGH-SEISMIC COASTAL',
	),
);
?>

<style id="kp-v3-front-page-styles">
	.kp-fp-main {
		background: #04070d;
		color: #f8fafc;
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
		overflow-x: clip;
	}
	.kp-fp-main *,
	.kp-fp-main *::before,
	.kp-fp-main *::after {
		box-sizing: border-box;
	}
	.kp-fp-hero {
		padding: clamp(16px, 3.2vw, 44px) 0 clamp(36px, 5vw, 68px);
		background: radial-gradient(circle at 82% 16%, rgba(212, 175, 55, 0.12) 0%, transparent 46%),
		            radial-gradient(circle at 12% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
		            #04070d;
	}
	.kp-fp-wrap {
		width: min(1340px, calc(100% - 32px));
		margin: 0 auto;
	}
	.kp-fp-hero-grid {
		display: grid;
		grid-template-columns: 1.15fr 0.85fr;
		gap: clamp(22px, 3.5vw, 44px);
		align-items: center;
	}
	@media (max-width: 980px) {
		.kp-fp-hero-grid {
			grid-template-columns: 1fr;
		}
	}
	.kp-fp-kicker {
		display: inline-block;
		font-family: 'JetBrains Mono', monospace;
		font-size: clamp(0.62rem, 1.8vw, 0.72rem);
		font-weight: 700;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: #d4af37;
		background: rgba(10, 16, 29, 0.9);
		border: 1px solid rgba(212, 175, 55, 0.36);
		border-radius: 999px;
		padding: 5px 12px;
		margin-bottom: 10px;
		line-height: 1.35;
	}
	.kp-fp-h1 {
		font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
		font-size: clamp(1.52rem, 3.6vw, 2.95rem);
		font-weight: 800;
		line-height: 1.09;
		letter-spacing: -0.025em;
		color: #f8fafc;
		margin: 0 0 10px;
		text-wrap: balance;
	}
	.kp-fp-quote {
		margin: 0 0 12px;
		padding: 9px 13px;
		background: rgba(10, 16, 29, 0.82);
		border-left: 3px solid #d4af37;
		border-radius: 0 12px 12px 0;
		font-size: clamp(0.8rem, 1.15vw, 0.91rem);
		line-height: 1.48;
		color: #e2e8f0;
	}
	.kp-fp-quick-card {
		background: #0a101d;
		border: 1px solid rgba(212, 175, 55, 0.42);
		border-radius: 16px;
		padding: 13px 15px;
		box-shadow: 0 18px 44px rgba(0, 0, 0, 0.58);
	}
	.kp-fp-quick-head {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 6px;
		margin-bottom: 9px;
	}
	.kp-fp-quick-title {
		font-family: 'Outfit', sans-serif;
		font-size: 0.86rem;
		font-weight: 700;
		color: #f8fafc;
	}
	.kp-fp-quick-sla {
		font-family: 'JetBrains Mono', monospace;
		font-size: 0.63rem;
		font-weight: 700;
		color: #38bdf8;
		background: rgba(56, 189, 248, 0.11);
		border: 1px solid rgba(56, 189, 248, 0.34);
		border-radius: 999px;
		padding: 2px 8px;
	}
	.kp-fp-quick-form {
		display: grid;
		grid-template-columns: 1.25fr 0.95fr auto;
		gap: 8px;
		align-items: center;
	}
	@media (max-width: 720px) {
		.kp-fp-quick-form {
			grid-template-columns: 1fr 1fr;
		}
		.kp-fp-quick-btn {
			grid-column: 1 / -1;
		}
	}
	.kp-fp-qinput,
	.kp-fp-qselect {
		width: 100%;
		min-height: 41px;
		padding: 8px 11px;
		border-radius: 10px;
		background: #04070d;
		border: 1px solid rgba(212, 175, 55, 0.3);
		color: #f8fafc;
		font-size: 0.81rem;
		outline: none;
	}
	.kp-fp-quick-btn {
		min-height: 44px;
		padding: 9px 18px;
		border-radius: 999px;
		border: none;
		background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 52%, #b89028 100%);
		color: #04070d !important;
		font-family: 'Outfit', sans-serif;
		font-size: 0.85rem;
		font-weight: 800;
		cursor: pointer;
		white-space: nowrap;
		box-shadow: 0 8px 22px rgba(212, 175, 55, 0.32);
	}
	.kp-fp-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin-top: 9px;
	}
	.kp-fp-chip {
		background: rgba(255, 255, 255, 0.04);
		border: 1px solid rgba(212, 175, 55, 0.22);
		color: #cbd5e1;
		border-radius: 999px;
		padding: 4px 10px;
		font-size: 0.69rem;
		cursor: pointer;
	}
	.kp-fp-chip:hover {
		border-color: #d4af37;
		color: #f8fafc;
	}
	.kp-fp-portrait-card {
		position: relative;
		border-radius: 22px;
		overflow: hidden;
		border: 1px solid rgba(212, 175, 55, 0.38);
		background: #0a101d;
		box-shadow: 0 28px 68px rgba(0, 0, 0, 0.72);
	}
	.kp-fp-portrait-card > img {
		width: 100%;
		aspect-ratio: 4 / 4.35;
		object-fit: cover;
		object-position: center top;
		display: block;
	}
	.kp-fp-floating-badge {
		position: absolute;
		left: 14px;
		right: 14px;
		bottom: 14px;
		background: rgba(4, 7, 13, 0.9);
		backdrop-filter: blur(14px);
		border: 1px solid rgba(212, 175, 55, 0.48);
		border-radius: 14px;
		padding: 10px 12px;
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.kp-fp-floating-badge img {
		width: 58px;
		height: 44px;
		border-radius: 8px;
		object-fit: cover;
		border: 1px solid rgba(212, 175, 55, 0.4);
		flex-shrink: 0;
	}
	/* 9-Corridor Matrix */
	.kp-fp-matrix-sec {
		padding: clamp(54px, 6.5vw, 88px) 0;
		background: #04070d;
		border-top: 1px solid rgba(212, 175, 55, 0.14);
	}
	.kp-fp-matrix-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr));
		gap: 18px;
		margin-top: 24px;
	}
	.kp-fp-mcard {
		background: #0a101d;
		border: 1px solid rgba(212, 175, 55, 0.24);
		border-radius: 18px;
		padding: 20px 22px;
		text-decoration: none !important;
		color: #f8fafc;
		display: flex;
		flex-direction: column;
		gap: 8px;
		transition: border-color 0.22s ease, transform 0.22s ease, box-shadow 0.22s ease;
	}
	.kp-fp-mcard:hover {
		border-color: #d4af37;
		transform: translateY(-3px);
		box-shadow: 0 20px 44px rgba(0, 0, 0, 0.6);
	}
</style>

<main id="primary" class="kp-fp-main">

	<!-- 1. SPLIT PRINCIPAL HERO + ABOVE-THE-FOLD 48-HR LOT & MLS® QUICK-INTAKE -->
	<section class="kp-fp-hero">
		<div class="kp-fp-wrap">
			<div class="kp-fp-hero-grid">
				<div>
					<div class="kp-fp-kicker">BC BUILDER #52603 &bull; BC HYDRO ES54 &bull; 20+ YRS KIEWIT HEAVY CIVIL &bull; 2-5-10 WARRANTY</div>

					<h1 class="kp-fp-h1">Slope-Critical Custom Estates &amp; Bill 44 Multiplexes&mdash;Engineered by a Heavy-Civil Superintendent.</h1>

					<blockquote class="kp-fp-quote">
						&ldquo;After 20+ years running heavy-civil rock, shoring, and utility infrastructure—including Peter Kiewit &amp; Sons—I supervise every foundation, BC Hydro ES54 trench, and structural hold-point myself on a <strong>100% Open-Book CCDC 5B Fiduciary Ledger</strong>.&rdquo;
						<span style="display:block;margin-top:4px;font-weight:700;color:#d4af37;font-size:0.78rem;">&mdash; Wayne Stevenson, Principal &amp; Licensed Builder #52603</span>
					</blockquote>

					<div class="kp-fp-quick-card">
						<div class="kp-fp-quick-head">
							<span class="kp-fp-quick-title">48-Hour Lot &amp; MLS&reg; Constructability Quick-Intake</span>
							<span class="kp-fp-quick-sla">DIRECT PRINCIPAL REVIEW</span>
						</div>
						<form class="kp-fp-quick-form" data-kp-hero-quick-intake>
							<input
								type="text"
								class="kp-fp-qinput"
								name="quick_lot"
								aria-label="Civic Address, PID, or MLS Number"
								placeholder="Address, PID or MLS® #"
							/>
							<select class="kp-fp-qselect" name="quick_corridor" aria-label="Select BC Corridor">
								<option value="west-vancouver">West Vancouver</option>
								<option value="whistler">Whistler Alpine</option>
								<option value="squamish">Squamish HQ</option>
								<option value="north-vancouver">North Vancouver</option>
								<option value="vancouver-r1-1">Vancouver R1-1 / Westside</option>
								<option value="coquitlam">Coquitlam</option>
								<option value="sunshine-coast">Sunshine Coast</option>
								<option value="pemberton">Pemberton</option>
								<option value="vancouver-island">Vancouver Island</option>
							</select>
							<button type="submit" class="kp-fp-quick-btn">Request 48-Hr Review &rarr;</button>
						</form>
						<div class="kp-fp-chips" aria-label="Sample Parcel Scenarios">
							<button type="button" class="kp-fp-chip" data-sample-lot="British Properties Steep Granite Bluff" data-sample-corridor="west-vancouver">British Properties Cliffside</button>
							<button type="button" class="kp-fp-chip" data-sample-lot="Vancouver R1-1 50x122 6-Unit Multiplex" data-sample-corridor="vancouver-r1-1">Vancouver R1-1 6-Plex</button>
							<button type="button" class="kp-fp-chip" data-sample-lot="Whistler 8.1 kPa Alpine Snow Parcel" data-sample-corridor="whistler">Whistler 8.1 kPa Snow</button>
							<button type="button" class="kp-fp-chip" data-sample-lot="Squamish Tantalus FCL + ES54 400A" data-sample-corridor="squamish">Squamish FCL + ES54</button>
						</div>
					</div>
				</div>

				<div class="kp-fp-portrait-card">
					<img
						src="<?php echo esc_url( $kp_wayne_portrait ); ?>"
						alt="Wayne Stevenson — Principal & Heavy-Civil Superintendent, Keystone Possibilities Ltd. (BC Builder #52603)"
						fetchpriority="high"
						decoding="async"
					/>
					<div class="kp-fp-floating-badge">
						<img src="<?php echo esc_url( $kp_sunridge_thumb ); ?>" alt="Sunridge Residence Whistler Verified Envelope" loading="lazy" />
						<div>
							<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#d4af37;font-weight:700;">VERIFIED BUILT ENVELOPE &bull; SUNRIDGE WHISTLER</div>
							<div style="font-size:0.8rem;font-weight:700;color:#f8fafc;line-height:1.3;">BCBC Part 4 Snow Load (8.1 kPa) &bull; Granite Tie-Backs &bull; Open-Book CCDC 5B</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- 2. 4K WATCH SUPERINTENDENT BRIEFING THEATER -->
	<?php get_template_part( 'template-parts/watch-player' ); ?>

	<!-- 3. SIGNATURE PORTFOLIO CINEMA REEL (9 RESIDENCES / 42 PHOTOS + ES54 CIVIL) -->
	<?php get_template_part( 'template-parts/portfolio-reel', null, array( 'mode' => 'reel' ) ); ?>

	<!-- 4. 17-CERTIFICATE STATUTORY & QUALIFICATION MUSEUM REEL -->
	<?php get_template_part( 'template-parts/credential-vault', null, array( 'mode' => 'reel' ) ); ?>

	<!-- 5. INTERACTIVE 9-CORRIDOR BILL 44, SLOPE & OPEN-BOOK CCDC 5B COMMAND CONSOLE -->
	<?php get_template_part( 'template-parts/bill44-calculator', null, array( 'default_corridor' => 'west-vancouver' ) ); ?>

	<!-- 6. 9-CORRIDOR BC ENGINEERING MATRIX -->
	<section id="corridors" class="kp-fp-matrix-sec">
		<div class="kp-fp-wrap">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#d4af37;margin-bottom:8px;">
				REGIONAL GEOTECHNICAL, SNOW-LOAD &amp; ZONING COMMAND &bull; 9 BC CORRIDORS
			</div>
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.55rem,2.9vw,2.3rem);font-weight:700;color:#f8fafc;margin:0 0 10px;line-height:1.16;">
				Local Bylaw, Bedrock &amp; BC Hydro ES54 Execution Across Coastal BC.
			</h2>
			<p style="font-size:0.95rem;color:#cbd5e1;max-width:780px;margin:0;line-height:1.6;">
				Select your municipality to inspect corridor-specific 2026 zoning bylaws, flood/snow/seismic structural parameters, built portfolio residences, and pre-calibrated CCDC 5B $/SF cost models.
			</p>

			<div class="kp-fp-matrix-grid">
				<?php foreach ( $kp_matrix_corridors as $mc ) : ?>
					<a href="<?php echo esc_url( $mc['url'] ); ?>" class="kp-fp-mcard">
						<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
							<span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:#d4af37;font-weight:700;"><?php echo esc_html( $mc['tag'] ); ?></span>
							<span style="color:#d4af37;font-weight:800;">&rarr;</span>
						</div>
						<h3 style="font-family:'Outfit',sans-serif;font-size:1.2rem;font-weight:700;color:#f8fafc;margin:0;"><?php echo esc_html( $mc['title'] ); ?></h3>
						<div style="font-size:0.78rem;color:#38bdf8;font-weight:600;"><?php echo esc_html( $mc['sub'] ); ?></div>
						<p style="font-size:0.84rem;color:#cbd5e1;line-height:1.55;margin:2px 0 0;"><?php echo esc_html( $mc['spec'] ); ?></p>
					</a>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<!-- 7. REALTOR® (BCFSA RULE 5-11) & AIBC ARCHITECT PRE-OFFER DESK TEASER -->
	<?php get_template_part( 'template-parts/realtor-rule511-card' ); ?>

	<!-- 8. VISIBLE EXECUTIVE FAQ ACCORDION + DIRECT PRINCIPAL CONSULTATION DESK -->
	<?php get_template_part( 'template-parts/faq-accordion' ); ?>
	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'west-vancouver' ) ); ?>

</main>

<script>
(function() {
	var qForm = document.querySelector('[data-kp-hero-quick-intake]');
	if (!qForm) return;
	var qLot = qForm.querySelector('[name="quick_lot"]');
	var qCor = qForm.querySelector('[name="quick_corridor"]');

	Array.prototype.forEach.call(document.querySelectorAll('[data-sample-lot]'), function(chip) {
		chip.addEventListener('click', function() {
			if (qLot) qLot.value = chip.getAttribute('data-sample-lot') || '';
			if (qCor) qCor.value = chip.getAttribute('data-sample-corridor') || 'west-vancouver';
		});
	});

	qForm.addEventListener('submit', function(e) {
		e.preventDefault();
		var mainForm = document.getElementById('kp-lead-intake-form');
		if (!mainForm) return;
		var lotDest = mainForm.querySelector('[name="lot_address"]');
		var corDest = mainForm.querySelector('[name="location"]');
		if (lotDest && qLot && qLot.value) lotDest.value = qLot.value;
		if (corDest && qCor && qCor.value) corDest.value = qCor.value;
		mainForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
		var nameInput = mainForm.querySelector('[name="name"]');
		if (nameInput) setTimeout(function() { nameInput.focus(); }, 450);
	});
})();
</script>

<?php
get_footer();
