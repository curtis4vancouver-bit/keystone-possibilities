<?php
/**
 * Template Name: Realtor & Architect Desk
 * Template Post Type: page
 *
 * Dedicated BC Realtor® (BCFSA Rule 5-11 / RESA s. 6–7) & AIBC Architect Pre-Offer Partner Desk:
 * 1) 30-Second Pre-Offer MLS® / PID Constructability Dropzone
 * 2) Interactive 0.50% Managing-Brokerage Referral Calculator + Written DOR Modal
 * 3) AIBC Early-Stage Value-Engineering Track
 * 4) Interactive 4-Tab Sample 48-Hour Feasibility Dossier
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<main id="primary" class="kp-v3-page">
	<style id="kp-v3-partner-desk-styles">
		.kp-pd-dropzone {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.44);
			border-radius: 20px;
			padding: clamp(18px, 3vw, 28px);
			box-shadow: 0 24px 60px rgba(0, 0, 0, 0.68);
		}
		.kp-pd-tabs {
			display: flex;
			flex-wrap: wrap;
			gap: 8px;
			margin-bottom: 18px;
		}
		.kp-pd-tab {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.28);
			color: #cbd5e1;
			border-radius: 999px;
			padding: 9px 16px;
			font-size: 0.8rem;
			font-weight: 700;
			cursor: pointer;
		}
		.kp-pd-tab.is-active,
		.kp-pd-tab:hover {
			background: rgba(212, 175, 55, 0.18);
			border-color: #d4af37;
			color: #f8fafc;
		}
		.kp-pd-pane {
			display: none;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.34);
			border-radius: 20px;
			padding: clamp(20px, 3vw, 30px);
		}
		.kp-pd-pane.is-active {
			display: grid;
			grid-template-columns: 1.05fr 0.95fr;
			gap: 24px;
			align-items: center;
		}
		@media (max-width: 900px) {
			.kp-pd-pane.is-active {
				grid-template-columns: 1fr;
			}
		}
	</style>

	<!-- 1. SPLIT HERO + 30-SECOND PRE-OFFER MLS® / PID DROPZONE -->
	<section style="padding:clamp(34px,5vw,68px) 0;background:radial-gradient(circle at 82% 14%,rgba(212,175,55,0.12),transparent 46%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:1.1fr 0.9fr;gap:clamp(24px,4vw,44px);align-items:center;" class="kp-pd-hero-grid">
			<style>
				@media (max-width: 960px) { .kp-pd-hero-grid { grid-template-columns: 1fr !important; } }
			</style>
			<div>
				<div style="font-family:'JetBrains Mono',monospace;font-size:0.71rem;font-weight:700;color:#d4af37;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:10px;">
					BC REALTOR&reg; &amp; AIBC ARCHITECT PARTNER DESK &bull; BCFSA RULE 5-11 COMPLIANT
				</div>
				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.95rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;">
					De-Risk Difficult Lots Before Subject Removal. Keep Schematic Designs On-Budget.
				</h1>
				<p style="font-size:0.98rem;line-height:1.65;color:#cbd5e1;margin:0 0 18px;">
					Drop an active MLS&reg; number, PID, or schematic site plan directly to Principal Superintendent Wayne Stevenson (#52603). Within <strong>48 business hours</strong>, your buyer or studio receives a written bedrock, BC Hydro ES54 transformer, and Class-C $/SF constructability brief—backed by our compliant <strong>0.50% Managing-Brokerage CCDC 5B referral</strong>.
				</p>
				<div style="display:flex;flex-wrap:wrap;gap:10px;font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#e2e8f0;">
					<span style="background:#0a101d;border:1px solid rgba(212,175,55,0.3);border-radius:999px;padding:6px 12px;">&#10003; RESA s. 6–7 Managing Brokerage Only</span>
					<span style="background:#0a101d;border:1px solid rgba(56,189,248,0.3);border-radius:999px;padding:6px 12px;">&#10003; Written Rule 5-11 DOR Included</span>
				</div>
			</div>

			<div class="kp-pd-dropzone">
				<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
					<span style="font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:700;color:#f8fafc;">30-Second Pre-Offer MLS&reg; / PID Dropzone</span>
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#38bdf8;font-weight:700;">48-HR TURNAROUND</span>
				</div>
				<form data-pd-quick-drop style="display:flex;flex-direction:column;gap:12px;">
					<div>
						<label for="kp-pd-mls" style="display:block;font-size:0.74rem;font-weight:700;color:#cbd5e1;margin-bottom:5px;">MLS&reg; Number, PID, or Street Address *</label>
						<input id="kp-pd-mls" type="text" placeholder="e.g., MLS R2948110 · 5600-blk British Properties" required style="width:100%;min-height:46px;padding:10px 14px;border-radius:12px;background:#04070d;border:1px solid rgba(212,175,55,0.34);color:#f8fafc;font-size:0.88rem;" />
					</div>
					<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
						<div>
							<label for="kp-pd-role" style="display:block;font-size:0.74rem;font-weight:700;color:#cbd5e1;margin-bottom:5px;">Partner Track</label>
							<select id="kp-pd-role" style="width:100%;min-height:46px;padding:10px 12px;border-radius:12px;background:#04070d;border:1px solid rgba(212,175,55,0.34);color:#f8fafc;font-size:0.85rem;">
								<option value="BC Realtor® — BCFSA Rule 5-11 Pre-Offer">BC Realtor&reg; (Pre-Offer)</option>
								<option value="AIBC Architect / EGBC Engineer">AIBC Architect / Engineer</option>
							</select>
						</div>
						<div>
							<label for="kp-pd-city" style="display:block;font-size:0.74rem;font-weight:700;color:#cbd5e1;margin-bottom:5px;">Corridor</label>
							<select id="kp-pd-city" style="width:100%;min-height:46px;padding:10px 12px;border-radius:12px;background:#04070d;border:1px solid rgba(212,175,55,0.34);color:#f8fafc;font-size:0.85rem;">
								<option value="west-vancouver">West Vancouver</option>
								<option value="whistler">Whistler</option>
								<option value="squamish">Squamish HQ</option>
								<option value="north-vancouver">North Vancouver</option>
								<option value="vancouver-r1-1">Vancouver R1-1</option>
								<option value="coquitlam">Coquitlam</option>
								<option value="sunshine-coast">Sunshine Coast</option>
								<option value="pemberton">Pemberton</option>
								<option value="vancouver-island">Vancouver Island</option>
							</select>
						</div>
					</div>
					<button type="submit" style="width:100%;min-height:48px;border:none;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.9rem;cursor:pointer;">
						Load Into Priority Partner Desk &rarr;
					</button>
				</form>
			</div>
		</div>
	</section>

	<!-- 2. BCFSA RULE 5-11 & RESA S. 6–7 (0.50%) MANAGING-BROKERAGE CALCULATOR + DOR MODAL -->
	<?php get_template_part( 'template-parts/realtor-rule511-card', null, array( 'full_desk' => true ) ); ?>

	<!-- 3. INTERACTIVE 4-TAB SAMPLE 48-HOUR FEASIBILITY DOSSIER -->
	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;border-top:1px solid rgba(212,175,55,0.14);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">
				INSIDE THE 48-HOUR PRE-OFFER &amp; SCHEMATIC DOSSIER
			</div>
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.55rem,2.9vw,2.25rem);font-weight:700;color:#f8fafc;margin:0 0 20px;">
				Inspect What Your Client or Design Studio Receives Within 48 Hours.
			</h2>

			<div class="kp-pd-tabs" role="tablist">
				<button type="button" class="kp-pd-tab is-active" data-pd-tab="0">01 · Granite Slope &amp; Micropile Profile</button>
				<button type="button" class="kp-pd-tab" data-pd-tab="1">02 · BC Hydro ES54 &amp; PMT Clearance</button>
				<button type="button" class="kp-pd-tab" data-pd-tab="2">03 · Bill 44 / R1-1 Density Yield</button>
				<button type="button" class="kp-pd-tab" data-pd-tab="3">04 · AIBC Early Value-Engineering</button>
			</div>

			<div class="kp-pd-pane is-active" data-pd-pane="0">
				<div>
					<h3 style="font-family:'Outfit',sans-serif;font-size:1.3rem;color:#d4af37;margin:0 0 10px;">Subgrade Rock, Micropile &amp; Creek Setback Exposure</h3>
					<p style="font-size:0.92rem;line-height:1.62;color:#cbd5e1;margin:0 0 12px;">
						Before your buyer removes subjects on a steep British Properties, Whistler, or North Shore bluff, we map visible granodiorite outcrops, crane reach, temporary shotcrete shoring, and 15m riparian creek setbacks—quantifying civil variance before deposit lock-in.
					</p>
					<ul style="margin:0;padding-left:18px;font-size:0.86rem;color:#e2e8f0;line-height:1.65;">
						<li>Line-drilling / hydraulic rock-splitting vs controlled blasting allowance</li>
						<li>Socketed micropile &amp; post-tensioned tie-back anchor exposure</li>
						<li>Flood Construction Level (FCL) &amp; pumped storm attenuation flags</li>
					</ul>
				</div>
				<div style="background:#04070d;border:1px solid rgba(212,175,55,0.28);border-radius:14px;padding:16px;">
					<svg viewBox="0 0 420 210" width="100%" role="img" aria-label="Granite Slope Micropile Schematic">
						<rect width="420" height="210" fill="#04070d"/>
						<path d="M20 45 L165 45 L295 150 L400 175 L400 200 L20 200 Z" fill="#0f172a" stroke="#d4af37" stroke-width="1.5"/>
						<rect x="115" y="22" width="140" height="72" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="1.5"/>
						<line x1="135" y1="94" x2="135" y2="168" stroke="#d4af37" stroke-width="3" stroke-dasharray="5,3"/>
						<line x1="235" y1="94" x2="215" y2="175" stroke="#d4af37" stroke-width="3" stroke-dasharray="5,3"/>
						<text x="126" y="54" fill="#f8fafc" font-family="monospace" font-size="10">CANTILEVERED ENVELOPE</text>
						<text x="40" y="186" fill="#d4af37" font-family="monospace" font-size="10">SOCKETED GRANITE MICROPILES (300 kPa)</text>
					</svg>
				</div>
			</div>

			<div class="kp-pd-pane" data-pd-pane="1">
				<div>
					<h3 style="font-family:'Outfit',sans-serif;font-size:1.3rem;color:#d4af37;margin:0 0 10px;">BC Hydro ES54 400A–800A &amp; CEC Rule 26-242 PMT Check</h3>
					<p style="font-size:0.92rem;line-height:1.62;color:#cbd5e1;margin:0 0 12px;">
						On-site Pad-Mounted Transformers (PMTs) routinely catch buyers and architects off guard—consuming prime front-yard setback area due to mandatory 3.0m hot-stick operational clearance. As a registered ES54 civil contractor, we flag PMT spatial geometry in 48 hours.
					</p>
					<ul style="margin:0;padding-left:18px;font-size:0.86rem;color:#e2e8f0;line-height:1.65;">
						<li>DB2 PVC duct trench routing (&ge;900mm boulevard / &ge;1050mm driveway)</li>
						<li>CEC Rule 26-242 3.0m front &amp; window/combustible wall clearances</li>
						<li>Self-performed ES54 civil cost vs third-party utility broker delays</li>
					</ul>
				</div>
				<div style="background:#04070d;border:1px solid rgba(56,189,248,0.3);border-radius:14px;padding:18px;font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:#e2e8f0;line-height:1.7;">
					<div style="color:#38bdf8;font-weight:700;margin-bottom:6px;">ES54 SPATIAL CLEARANCE MATRIX</div>
					<div>&bull; PMT Front Hot-Stick Zone: <strong>3.00m Unobstructed</strong></div>
					<div>&bull; Boulevard Duct Cover: <strong>&ge; 900mm DB2 PVC</strong></div>
					<div>&bull; Vehicular Crossing Cover: <strong>&ge; 1,050mm Concrete/DB2</strong></div>
					<div>&bull; Hydro-Vac Tolerance Zone: <strong>1,500–2,200 PSI (&le;1.0m)</strong></div>
				</div>
			</div>

			<div class="kp-pd-pane" data-pd-pane="2">
				<div>
					<h3 style="font-family:'Outfit',sans-serif;font-size:1.3rem;color:#d4af37;margin:0 0 10px;">Bill 44 SSMUH (3–6 Units) &amp; Vancouver R1-1 Feasibility</h3>
					<p style="font-size:0.92rem;line-height:1.62;color:#cbd5e1;margin:0;">
						Evaluate whether a teardown parcel performs better as a signature custom home or a 4–6 unit Bill 44 / 1.0 FSR R1-1 multiplex—factoring in 2" domestic water main upgrades, NFPA 13D/13R sprinklers, storm detention tanks, and Part 4 lateral shear walls.
					</p>
				</div>
				<div style="background:#04070d;border:1px solid rgba(212,175,55,0.3);border-radius:14px;padding:18px;font-size:0.85rem;color:#cbd5e1;line-height:1.65;">
					<strong style="color:#f8fafc;display:block;margin-bottom:6px;">Pre-Offer Multiplex Checkpoints:</strong>
					1. Transit-Oriented Area (TOA) vs 3–4–6 unit SSMUH tier<br/>
					2. Frontage &amp; lane access for multi-gang 400A/600A metering<br/>
					3. Net salable strata SF vs Open-Book CCDC 5B hard build cost
				</div>
			</div>

			<div class="kp-pd-pane" data-pd-pane="3">
				<div>
					<h3 style="font-family:'Outfit',sans-serif;font-size:1.3rem;color:#d4af37;margin:0 0 10px;">AIBC Studio Schematic Cost &amp; Detail Calibration</h3>
					<p style="font-size:0.92rem;line-height:1.62;color:#cbd5e1;margin:0;">
						Nothing frustrates an architectural studio or client more than tendering a completed permit set only to discover bids sit 35% above budget. Under pre-construction CCDC 5B advisory, we price structural steel cantilevers, board-formed concrete lifts, and glazing packages live during schematic design.
					</p>
				</div>
				<div style="background:#04070d;border:1px solid rgba(212,175,55,0.3);border-radius:14px;padding:18px;font-size:0.85rem;color:#cbd5e1;line-height:1.65;">
					<strong style="color:#f8fafc;display:block;margin-bottom:6px;">Architectural Collaboration Deliverables:</strong>
					&bull; Live 3-bid sub-trade budget checks at SD, DD, and 75% BP<br/>
					&bull; Thermal-bridge &amp; Step Code 5 / EL-4 assembly coordination<br/>
					&bull; Shared 13-sheet IFC digital portal for CRP &amp; Schedule B reviews
				</div>
			</div>
		</div>
	</section>

	<?php
	get_template_part(
		'template-parts/lead-intake-form',
		null,
		array(
			'default_audience' => 'BC Realtor® — BCFSA Rule 5-11 Pre-Offer',
			'default_corridor' => 'west-vancouver',
			'heading'          => 'Submit an MLS® Parcel, Schematic Set, or Brokerage DOR Request.',
		)
	);
	?>

	<script>
	(function() {
		var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-pd-tab]'));
		var panes = Array.prototype.slice.call(document.querySelectorAll('[data-pd-pane]'));
		tabs.forEach(function(tab) {
			tab.addEventListener('click', function() {
				var idx = tab.getAttribute('data-pd-tab');
				tabs.forEach(function(t) { t.classList.toggle('is-active', t === tab); });
				panes.forEach(function(p) { p.classList.toggle('is-active', p.getAttribute('data-pd-pane') === idx); });
			});
		});

		var qDrop = document.querySelector('[data-pd-quick-drop]');
		if (qDrop) {
			qDrop.addEventListener('submit', function(e) {
				e.preventDefault();
				var mls = document.getElementById('kp-pd-mls');
				var role = document.getElementById('kp-pd-role');
				var city = document.getElementById('kp-pd-city');
				var form = document.getElementById('kp-lead-intake-form');
				if (!form) return;
				var lotF = form.querySelector('[name="lot_address"]');
				var audF = form.querySelector('[name="audience"]');
				var locF = form.querySelector('[name="location"]');
				if (lotF && mls) lotF.value = mls.value;
				if (audF && role) audF.value = role.value;
				if (locF && city) locF.value = city.value;
				form.scrollIntoView({ behavior: 'smooth', block: 'center' });
				var nameF = form.querySelector('[name="name"]');
				if (nameF) setTimeout(function() { nameF.focus(); }, 420);
			});
		}
	})();
	</script>
</main>

<?php
get_footer();
