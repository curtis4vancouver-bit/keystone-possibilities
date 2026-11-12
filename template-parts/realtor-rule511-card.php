<?php
/**
 * Template Part: BCFSA Rule 5-11 & RESA s. 6–7 (0.50%) Managing-Brokerage Referral Calculator
 *
 * Models $2.5M–$10.0M CCDC 5B custom home & Bill 44 multiplex build scopes with transparent
 * Managing-Brokerage referral remittance + written Disclosure of Remuneration (DOR) modal.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_section_id = isset( $args['section_id'] ) ? sanitize_html_class( (string) $args['section_id'] ) : 'realtor-architect-desk';
$kp_is_page    = ! empty( $args['full_desk'] );
$kp_r511_uid   = wp_unique_id( 'kp-r511-' );

if ( empty( $GLOBALS['kp_v3_rule511_css'] ) ) :
	$GLOBALS['kp_v3_rule511_css'] = true;
	?>
	<style id="kp-v3-rule511-styles">
		.kp-r511-section {
			padding: clamp(54px, 6.5vw, 88px) 0;
			background: linear-gradient(180deg, #04070d 0%, #070d19 100%);
			color: #f8fafc;
			border-top: 1px solid rgba(212, 175, 55, 0.16);
		}
		.kp-r511-wrap {
			width: min(1340px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-r511-card {
			display: grid;
			grid-template-columns: 1.05fr 0.95fr;
			gap: 26px;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.36);
			border-radius: 22px;
			padding: clamp(20px, 3.5vw, 36px);
			box-shadow: 0 26px 60px rgba(0, 0, 0, 0.65);
		}
		@media (max-width: 960px) {
			.kp-r511-card {
				grid-template-columns: 1fr;
			}
		}
		.kp-r511-kicker {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: #d4af37;
			margin-bottom: 8px;
		}
		.kp-r511-h2 {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.5rem, 2.8vw, 2.15rem);
			font-weight: 700;
			line-height: 1.18;
			color: #f8fafc;
			margin: 0 0 12px;
		}
		.kp-r511-copy {
			font-size: 0.94rem;
			line-height: 1.62;
			color: #cbd5e1;
			margin: 0 0 18px;
		}
		.kp-r511-checks {
			display: flex;
			flex-direction: column;
			gap: 10px;
			margin-bottom: 20px;
		}
		.kp-r511-check {
			display: flex;
			align-items: flex-start;
			gap: 10px;
			font-size: 0.85rem;
			color: #e2e8f0;
			line-height: 1.5;
		}
		.kp-r511-check span.dot {
			color: #d4af37;
			font-weight: 800;
			flex-shrink: 0;
		}
		.kp-r511-calc-box {
			background: #04070d;
			border: 1px solid rgba(212, 175, 55, 0.34);
			border-radius: 18px;
			padding: clamp(18px, 2.8vw, 26px);
			display: flex;
			flex-direction: column;
			gap: 14px;
		}
		.kp-r511-presets {
			display: flex;
			flex-wrap: wrap;
			gap: 7px;
		}
		.kp-r511-preset {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.28);
			color: #cbd5e1;
			border-radius: 999px;
			padding: 5px 12px;
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			cursor: pointer;
		}
		.kp-r511-preset.is-active,
		.kp-r511-preset:hover {
			border-color: #d4af37;
			color: #f8fafc;
			background: rgba(212, 175, 55, 0.16);
		}
		.kp-r511-split {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 10px;
		}
		@media (max-width: 480px) {
			.kp-r511-split {
				grid-template-columns: 1fr;
			}
		}
		.kp-r511-milestone {
			background: #0a101d;
			border: 1px solid rgba(255, 255, 255, 0.08);
			border-radius: 12px;
			padding: 12px;
		}
		.kp-r511-actions {
			display: flex;
			flex-wrap: wrap;
			gap: 10px;
			margin-top: 4px;
		}
		.kp-r511-btn-gold {
			display: inline-flex;
			align-items: center;
			justify-content: center;
			min-height: 46px;
			padding: 10px 20px;
			border-radius: 999px;
			background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 52%, #b89028 100%);
			color: #04070d !important;
			font-weight: 800;
			font-size: 0.85rem;
			text-decoration: none;
			border: none;
			cursor: pointer;
		}
		.kp-r511-btn-ghost {
			display: inline-flex;
			align-items: center;
			justify-content: center;
			min-height: 46px;
			padding: 10px 18px;
			border-radius: 999px;
			background: transparent;
			border: 1px solid rgba(212, 175, 55, 0.42);
			color: #f8fafc !important;
			font-weight: 700;
			font-size: 0.83rem;
			text-decoration: none;
			cursor: pointer;
		}
		.kp-dor-modal {
			position: fixed;
			inset: 0;
			z-index: 99999;
			background: rgba(4, 7, 13, 0.94);
			backdrop-filter: blur(14px);
			display: none;
			align-items: center;
			justify-content: center;
			padding: 16px;
		}
		.kp-dor-modal.is-open {
			display: flex;
		}
		.kp-dor-sheet {
			width: min(720px, 100%);
			max-height: 90vh;
			overflow-y: auto;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.5);
			border-radius: 18px;
			padding: clamp(20px, 3.5vw, 30px);
			color: #f8fafc;
		}
	</style>
<?php endif; ?>

<section id="<?php echo esc_attr( $kp_section_id ); ?>" class="kp-r511-section" data-kp-r511="<?php echo esc_attr( $kp_r511_uid ); ?>">
	<div class="kp-r511-wrap">
		<div class="kp-r511-card">
			<div>
				<div class="kp-r511-kicker">BC REALTOR&reg; &amp; AIBC ARCHITECT PRE-OFFER DESK · BCFSA RULE 5-11</div>
				<h2 class="kp-r511-h2">48-Hour Pre-Offer Lot Constructability + Compliant 0.50% Managing-Brokerage Referral.</h2>
				<p class="kp-r511-copy">
					Protect your buyer before subject removal on steep granite, riparian, or Bill 44 SSMUH parcels—and receive a transparent, fully disclosed <strong>0.50% CCDC 5B build referral remitted strictly to your licensed Managing Brokerage</strong> under BCFSA Rule 5-11 and RESA s. 6–7.
				</p>

				<div class="kp-r511-checks">
					<div class="kp-r511-check">
						<span class="dot">&#10003;</span>
						<span><strong>48-Hour Pre-Offer Subject-Removal Dossier:</strong> Bedrock/shoring exposure, BC Hydro ES54 400A–800A PMT clearance, and Class-C $/SF pro-forma before subjects come off.</span>
					</div>
					<div class="kp-r511-check">
						<span class="dot">&#10003;</span>
						<span><strong>100% Managing-Brokerage &amp; Written DOR Compliance:</strong> Paid directly to the licensed Managing Brokerage (never to an individual or unlicensed party) with written Disclosure of Remuneration signed by the client prior to CCDC 5B execution.</span>
					</div>
					<div class="kp-r511-check">
						<span class="dot">&#10003;</span>
						<span><strong>AIBC Architect &amp; EGBC Early Value-Engineering Track:</strong> Schematic cantilever, glazing, and mechanical cost checks that preserve design intent without mid-tender redesigns.</span>
					</div>
				</div>

				<div class="kp-r511-actions">
					<?php if ( ! $kp_is_page ) : ?>
						<a href="<?php echo esc_url( home_url( '/realtor-architect-desk/' ) ); ?>" class="kp-r511-btn-gold">
							Open Realtor&reg; &amp; Architect Desk &rarr;
						</a>
					<?php else : ?>
						<a href="#kp-lead-intake-form" class="kp-r511-btn-gold" data-r511-register>
							Submit MLS&reg; / PID for 48-Hr Review &rarr;
						</a>
					<?php endif; ?>
					<button type="button" class="kp-r511-btn-ghost" data-open-dor>
						Preview Written BCFSA Rule 5-11 DOR Schedule
					</button>
				</div>
			</div>

			<div class="kp-r511-calc-box" aria-live="polite">
				<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#d4af37;font-weight:700;">MANAGING-BROKERAGE REFERRAL CALCULATOR (0.50%)</span>
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#38bdf8;">RESA s. 6–7 COMPLIANT</span>
				</div>

				<div>
					<label for="<?php echo esc_attr( $kp_r511_uid ); ?>-range" style="display:flex;justify-content:space-between;font-size:0.8rem;font-weight:700;color:#cbd5e1;margin-bottom:6px;">
						<span>Executed CCDC 5B Construction Scope</span>
						<strong style="color:#f8fafc;font-family:'JetBrains Mono',monospace;" data-r511-scope>$4,500,000 CAD</strong>
					</label>
					<input
						type="range"
						id="<?php echo esc_attr( $kp_r511_uid ); ?>-range"
						min="2500000"
						max="10000000"
						step="250000"
						value="4500000"
						style="width:100%;accent-color:#d4af37;cursor:pointer;"
						data-r511-slider
					/>
				</div>

				<div class="kp-r511-presets">
					<button type="button" class="kp-r511-preset" data-r511-val="2500000">$2.5M Multiplex</button>
					<button type="button" class="kp-r511-preset is-active" data-r511-val="4500000">$4.5M Estate</button>
					<button type="button" class="kp-r511-preset" data-r511-val="6500000">$6.5M Cliffside</button>
					<button type="button" class="kp-r511-preset" data-r511-val="10000000">$10.0M Alpine Compound</button>
				</div>

				<div style="background:#0a101d;border:1px solid rgba(212,175,55,0.44);border-radius:14px;padding:14px 16px;">
					<div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;color:#f3e5ab;font-weight:700;">Total Gross Managing-Brokerage Referral (0.50% + GST)</div>
					<div style="font-family:'Outfit',sans-serif;font-size:1.95rem;font-weight:800;color:#d4af37;margin-top:2px;" data-r511-total>$22,500 CAD</div>
					<div style="font-size:0.75rem;color:#94a3b8;margin-top:2px;">Paid via corporate EFT/trust cheque strictly to Managing Brokerage upon verified build milestones.</div>
				</div>

				<div class="kp-r511-split">
					<div class="kp-r511-milestone">
						<div style="font-size:0.68rem;text-transform:uppercase;color:#94a3b8;font-weight:700;">Tranche 1 (50% · Building Permit &amp; Mobilization)</div>
						<div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:700;color:#f8fafc;margin-top:4px;" data-r511-half1>$11,250 CAD</div>
					</div>
					<div class="kp-r511-milestone">
						<div style="font-size:0.68rem;text-transform:uppercase;color:#94a3b8;font-weight:700;">Tranche 2 (50% · Structural Lockup Gate)</div>
						<div style="font-family:'JetBrains Mono',monospace;font-size:1.05rem;font-weight:700;color:#f8fafc;margin-top:4px;" data-r511-half2>$11,250 CAD</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="kp-dor-modal" data-dor-modal role="dialog" aria-modal="true" aria-label="BCFSA Rule 5-11 Disclosure of Remuneration Schedule">
		<div class="kp-dor-sheet">
			<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px;">
				<span class="kp-r511-kicker" style="margin:0;">BCFSA REAL ESTATE SERVICES RULES — RULE 5-11 &amp; RESA S. 6–7</span>
				<button type="button" class="kp-r511-preset" data-close-dor>Close &times;</button>
			</div>
			<h3 style="font-family:'Outfit',sans-serif;font-size:1.35rem;margin:0 0 10px;color:#f8fafc;">Written Disclosure of Remuneration (DOR) &amp; Managing-Brokerage Protocol</h3>
			<p style="font-size:0.88rem;line-height:1.62;color:#cbd5e1;margin:0 0 14px;">
				Keystone Possibilities Ltd. (BC Housing Licensed Builder #52603) maintains strict statutory compliance with the BC Financial Services Authority (BCFSA) Real Estate Services Rules:
			</p>
			<ol style="font-size:0.86rem;line-height:1.65;color:#e2e8f0;padding-left:20px;margin:0 0 18px;">
				<li><strong>Managing-Brokerage Remittance Only:</strong> All referral remuneration (0.50% of executed base CCDC 5B construction scope, excluding land acquisition and municipal DCCs) is invoiced by and paid exclusively to the referring licensee’s <strong>Managing Brokerage</strong> pursuant to RESA s. 6–7. Zero payments are ever made directly to individual licensees or unlicensed parties.</li>
				<li><strong>Mandatory Written Client Disclosure (Rule 5-11):</strong> Prior to CCDC 5B construction management execution, the licensee delivers written Disclosure of Remuneration to the client stating the exact dollar calculation (<span data-dor-live-amt>$22,500 CAD</span> at current slider setting), which is countersigned into the open-book project binder.</li>
				<li><strong>Zero Construction Markup Inflation:</strong> Referral remuneration is funded out of Keystone Possibilities Ltd.’s corporate business development allocation—never added as a hidden trade markup on the client’s open-book CCDC 5B ledger.</li>
			</ol>
			<button type="button" class="kp-r511-btn-gold" data-dor-to-form>Register Brokerage &amp; Request DOR Packet &rarr;</button>
		</div>
	</div>

	<script>
	(function() {
		var root = document.querySelector('[data-kp-r511="<?php echo esc_js( $kp_r511_uid ); ?>"]');
		if (!root) return;
		var slider = root.querySelector('[data-r511-slider]');
		var presets = Array.prototype.slice.call(root.querySelectorAll('[data-r511-val]'));
		var scopeEl = root.querySelector('[data-r511-scope]');
		var totalEl = root.querySelector('[data-r511-total]');
		var h1El = root.querySelector('[data-r511-half1]');
		var h2El = root.querySelector('[data-r511-half2]');
		var dorAmt = root.querySelector('[data-dor-live-amt]');
		var dorModal = root.querySelector('[data-dor-modal]');

		function updateR511() {
			var v = parseInt(slider.value, 10) || 4500000;
			var fee = Math.round(v * 0.005);
			var half = Math.round(fee / 2);
			scopeEl.textContent = '$' + v.toLocaleString() + ' CAD';
			totalEl.textContent = '$' + fee.toLocaleString() + ' CAD';
			h1El.textContent = '$' + half.toLocaleString() + ' CAD';
			h2El.textContent = '$' + (fee - half).toLocaleString() + ' CAD';
			if (dorAmt) dorAmt.textContent = '$' + fee.toLocaleString() + ' CAD';
			presets.forEach(function(p) {
				p.classList.toggle('is-active', parseInt(p.getAttribute('data-r511-val'), 10) === v);
			});
		}

		slider.addEventListener('input', updateR511);
		slider.addEventListener('change', updateR511);
		presets.forEach(function(btn) {
			btn.addEventListener('click', function() {
				slider.value = btn.getAttribute('data-r511-val');
				updateR511();
			});
		});

		var openDor = root.querySelector('[data-open-dor]');
		var closeDor = root.querySelector('[data-close-dor]');
		var dorToForm = root.querySelector('[data-dor-to-form]');
		if (openDor) openDor.addEventListener('click', function() { dorModal.classList.add('is-open'); });
		if (closeDor) closeDor.addEventListener('click', function() { dorModal.classList.remove('is-open'); });
		dorModal.addEventListener('click', function(e) { if (e.target === dorModal) dorModal.classList.remove('is-open'); });
		if (dorToForm) {
			dorToForm.addEventListener('click', function() {
				dorModal.classList.remove('is-open');
				var form = document.getElementById('kp-lead-intake-form');
				if (form) {
					var aud = form.querySelector('[name="audience"]');
					if (aud) { aud.value = 'BC Realtor® — BCFSA Rule 5-11 Pre-Offer'; aud.dispatchEvent(new Event('change')); }
					form.scrollIntoView({ behavior: 'smooth' });
				} else {
					window.location.href = '<?php echo esc_url( home_url( '/realtor-architect-desk/#kp-lead-intake-form' ) ); ?>';
				}
			});
		}
		updateR511();
	})();
	</script>
</section>
