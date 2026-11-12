<?php
/**
 * Template Part: WCAG Accessible Executive Consultation & 48-Hr Lot Constructability Desk
 *
 * Submits via POST /wp-json/keystone/v1/lead with Audience selector:
 * - Landowner / Custom Home Buyer
 * - BC Realtor® — BCFSA Rule 5-11 Pre-Offer
 * - AIBC Architect / EGBC Engineer
 * - Bill 44 Multiplex / JV Investor
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'kp_v3_render_core_shell_css' ) ) {
	/**
	 * Prints shared Quiet-Luxury v3.0 page shell tokens & responsive layout classes once per request.
	 */
	function kp_v3_render_core_shell_css() {
		if ( ! empty( $GLOBALS['kp_v3_core_shell_css_printed'] ) ) {
			return;
		}
		$GLOBALS['kp_v3_core_shell_css_printed'] = true;
		?>
		<style id="kp-v3-core-shell-styles">
			:root {
				--kp-obsidian: #04070d;
				--kp-slate: #0a101d;
				--kp-slate-2: #0f172a;
				--kp-gold: #d4af37;
				--kp-champagne: #c8a45d;
				--kp-ivory: #f8fafc;
				--kp-muted: #cbd5e1;
				--kp-dim: #94a3b8;
				--kp-steel: #38bdf8;
				--kp-hairline: rgba(212, 175, 55, 0.28);
			}
			.kp-v3-page {
				background: #04070d;
				color: #f8fafc;
				font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
				overflow-x: clip;
			}
			.kp-v3-page *,
			.kp-v3-page *::before,
			.kp-v3-page *::after {
				box-sizing: border-box;
			}
			.kp-v3-container {
				width: min(1340px, calc(100% - 32px));
				margin: 0 auto;
			}
			.kp-v3-hero {
				padding: clamp(32px, 5vw, 68px) 0 clamp(44px, 6vw, 76px);
				background: radial-gradient(circle at 82% 14%, rgba(212, 175, 55, 0.11) 0%, transparent 46%),
				            radial-gradient(circle at 12% 8%, rgba(56, 189, 248, 0.07) 0%, transparent 40%),
				            #04070d;
				border-bottom: 1px solid rgba(212, 175, 55, 0.16);
			}
			.kp-v3-split {
				display: grid;
				grid-template-columns: 1.12fr 0.88fr;
				gap: clamp(22px, 3.6vw, 44px);
				align-items: center;
			}
			@media (max-width: 980px) {
				.kp-v3-split {
					grid-template-columns: 1fr;
				}
			}
			.kp-v3-kicker {
				display: inline-flex;
				align-items: center;
				gap: 8px;
				font-family: 'JetBrains Mono', monospace;
				font-size: 0.71rem;
				font-weight: 600;
				letter-spacing: 0.07em;
				text-transform: uppercase;
				color: #d4af37;
				background: rgba(10, 16, 29, 0.88);
				border: 1px solid rgba(212, 175, 55, 0.34);
				border-radius: 999px;
				padding: 6px 13px;
				margin-bottom: 14px;
				max-width: 100%;
			}
			.kp-v3-h1 {
				font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
				font-size: clamp(1.85rem, 3.8vw, 3.05rem);
				font-weight: 800;
				line-height: 1.11;
				letter-spacing: -0.025em;
				color: #f8fafc;
				margin: 0 0 14px;
				text-wrap: balance;
			}
			.kp-v3-h2 {
				font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
				font-size: clamp(1.5rem, 2.9vw, 2.25rem);
				font-weight: 700;
				line-height: 1.16;
				letter-spacing: -0.02em;
				color: #f8fafc;
				margin: 0 0 12px;
			}
			.kp-v3-lead {
				font-size: clamp(0.95rem, 1.3vw, 1.06rem);
				line-height: 1.65;
				color: #cbd5e1;
				margin: 0 0 20px;
			}
			.kp-v3-quote {
				background: rgba(10, 16, 29, 0.86);
				border-left: 3px solid #d4af37;
				border-radius: 0 14px 14px 0;
				padding: 13px 16px;
				font-size: 0.9rem;
				line-height: 1.58;
				color: #e2e8f0;
				margin: 0 0 18px;
			}
			.kp-v3-section {
				padding: clamp(52px, 6.5vw, 88px) 0;
				border-top: 1px solid rgba(212, 175, 55, 0.14);
			}
			.kp-v3-grid-3 {
				display: grid;
				grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));
				gap: 20px;
			}
			.kp-v3-grid-2 {
				display: grid;
				grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr));
				gap: 22px;
			}
			.kp-v3-card {
				background: #0a101d;
				border: 1px solid rgba(212, 175, 55, 0.24);
				border-radius: 18px;
				padding: clamp(18px, 2.6vw, 26px);
				display: flex;
				flex-direction: column;
				gap: 10px;
				transition: border-color 0.22s ease, transform 0.22s ease;
			}
			.kp-v3-card:hover {
				border-color: rgba(212, 175, 55, 0.58);
				transform: translateY(-2px);
			}
			.kp-v3-btn-gold {
				display: inline-flex;
				align-items: center;
				justify-content: center;
				gap: 8px;
				min-height: 46px;
				padding: 11px 22px;
				border-radius: 999px;
				background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 52%, #b89028 100%);
				color: #04070d !important;
				font-family: 'Outfit', sans-serif;
				font-size: 0.88rem;
				font-weight: 800;
				text-decoration: none !important;
				border: none;
				cursor: pointer;
				box-shadow: 0 10px 26px rgba(212, 175, 55, 0.28);
			}
			.kp-v3-btn-outline {
				display: inline-flex;
				align-items: center;
				justify-content: center;
				gap: 8px;
				min-height: 46px;
				padding: 11px 20px;
				border-radius: 999px;
				background: rgba(10, 16, 29, 0.85);
				border: 1px solid rgba(212, 175, 55, 0.42);
				color: #f8fafc !important;
				font-family: 'Outfit', sans-serif;
				font-size: 0.86rem;
				font-weight: 700;
				text-decoration: none !important;
				cursor: pointer;
			}
		</style>
		<?php
	}
}
kp_v3_render_core_shell_css();

$kp_form_id          = isset( $args['form_id'] ) ? sanitize_html_class( (string) $args['form_id'] ) : 'kp-lead-intake-form';
$kp_default_corridor = isset( $args['default_corridor'] ) ? sanitize_title( (string) $args['default_corridor'] ) : 'squamish';
$kp_default_audience = isset( $args['default_audience'] ) ? (string) $args['default_audience'] : 'Landowner / Custom Home Buyer';
$kp_embed_only       = ! empty( $args['embed_only'] );
$kp_heading          = isset( $args['heading'] ) ? (string) $args['heading'] : 'Request Your 48-Hour Lot & Constructability Dossier.';
$kp_subcopy          = isset( $args['subcopy'] ) ? (string) $args['subcopy'] : 'Reviewed directly by Principal & Heavy-Civil Superintendent Wayne Stevenson (#52603) at 1 Watts Point Road, Squamish—never routed to junior sales brokers.';

if ( empty( $GLOBALS['kp_v3_lead_form_css'] ) ) :
	$GLOBALS['kp_v3_lead_form_css'] = true;
	?>
	<style id="kp-v3-lead-form-styles">
		.kp-intake-section {
			padding: clamp(54px, 7vw, 90px) 0;
			background: linear-gradient(180deg, #04070d 0%, #080e1b 100%);
			color: #f8fafc;
			border-top: 1px solid rgba(212, 175, 55, 0.16);
		}
		.kp-intake-grid {
			display: grid;
			grid-template-columns: 0.88fr 1.12fr;
			gap: clamp(24px, 3.5vw, 40px);
			align-items: start;
		}
		@media (max-width: 960px) {
			.kp-intake-grid {
				grid-template-columns: 1fr;
			}
		}
		.kp-intake-card {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.36);
			border-radius: 20px;
			padding: clamp(18px, 3vw, 30px);
			box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65);
		}
		.kp-intake-row {
			display: grid;
			grid-template-columns: 1fr 1fr;
			gap: 14px;
			margin-bottom: 14px;
		}
		@media (max-width: 600px) {
			.kp-intake-row {
				grid-template-columns: 1fr;
			}
		}
		.kp-intake-field {
			display: flex;
			flex-direction: column;
			gap: 5px;
			margin-bottom: 14px;
		}
		.kp-intake-row .kp-intake-field {
			margin-bottom: 0;
		}
		.kp-intake-field label {
			font-size: 0.75rem;
			font-weight: 700;
			letter-spacing: 0.03em;
			color: #cbd5e1;
		}
		.kp-intake-input,
		.kp-intake-select,
		.kp-intake-textarea {
			width: 100%;
			min-height: 46px;
			padding: 10px 14px;
			border-radius: 12px;
			background: #04070d;
			border: 1px solid rgba(212, 175, 55, 0.3);
			color: #f8fafc;
			font-family: 'Inter', sans-serif;
			font-size: 0.88rem;
			outline: none;
		}
		.kp-intake-textarea {
			min-height: 96px;
			resize: vertical;
		}
		.kp-intake-input:focus,
		.kp-intake-select:focus,
		.kp-intake-textarea:focus {
			border-color: #d4af37;
			box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.16);
		}
		.kp-intake-status {
			display: none;
			margin-top: 14px;
			padding: 13px 16px;
			border-radius: 12px;
			font-size: 0.85rem;
			line-height: 1.5;
		}
		.kp-intake-status.is-ok {
			display: block;
			background: rgba(212, 175, 55, 0.14);
			border: 1px solid #d4af37;
			color: #f8fafc;
		}
		.kp-intake-status.is-err {
			display: block;
			background: rgba(239, 68, 68, 0.14);
			border: 1px solid #ef4444;
			color: #fecaca;
		}
	</style>
<?php endif; ?>

<?php if ( ! $kp_embed_only ) : ?>
<section id="consultation-desk" class="kp-intake-section">
	<div class="kp-v3-container">
		<div class="kp-intake-grid">
			<div>
				<div class="kp-v3-kicker">DIRECT PRINCIPAL CONSULTATION DESK · 48-HR SLA</div>
				<h2 class="kp-v3-h2"><?php echo esc_html( $kp_heading ); ?></h2>
				<p class="kp-v3-lead"><?php echo esc_html( $kp_subcopy ); ?></p>

				<div class="kp-v3-card" style="margin-top:18px;">
					<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#d4af37;font-weight:700;">HEADQUARTERS &amp; DIRECT DISPATCH</div>
					<div style="font-family:'Outfit',sans-serif;font-size:1.15rem;font-weight:700;color:#f8fafc;">Wayne Stevenson — BC Housing #52603</div>
					<div style="font-size:0.88rem;color:#cbd5e1;line-height:1.6;">
						<strong>Address:</strong> 1 Watts Point Road, Squamish, BC V8B 0B1<br/>
						<strong>Direct Line:</strong> <a href="tel:+16048489688" style="color:#d4af37;font-weight:700;text-decoration:none;">(604) 848-9688</a><br/>
						<strong>Credentials:</strong> BC Housing #52603 &bull; BC Hydro ES54 Civil &bull; WorkSafeBC #201703481 &bull; Mandatory 2-5-10 Warranty
					</div>
				</div>
			</div>
<?php endif; ?>

			<div class="kp-intake-card">
				<form id="<?php echo esc_attr( $kp_form_id ); ?>" data-kp-v3-lead-form="1" action="<?php echo esc_url( rest_url( 'keystone/v1/lead' ) ); ?>" method="post" novalidate>
					<div class="kp-intake-row">
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-audience">I Am Inquiring As *</label>
							<select id="<?php echo esc_attr( $kp_form_id ); ?>-audience" name="audience" class="kp-intake-select" required>
								<?php
								$kp_audiences = array(
									'Landowner / Custom Home Buyer',
									'BC Realtor® — BCFSA Rule 5-11 Pre-Offer',
									'AIBC Architect / EGBC Engineer',
									'Bill 44 Multiplex / JV Investor',
								);
								foreach ( $kp_audiences as $aud_opt ) :
									?>
									<option value="<?php echo esc_attr( $aud_opt ); ?>" <?php selected( $kp_default_audience, $aud_opt ); ?>>
										<?php echo esc_html( $aud_opt ); ?>
									</option>
								<?php endforeach; ?>
							</select>
						</div>

						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-corridor">BC Municipal Corridor *</label>
							<select id="<?php echo esc_attr( $kp_form_id ); ?>-corridor" name="location" class="kp-intake-select" required>
								<?php
								$kp_corridors_opt = array(
									'west-vancouver'   => 'West Vancouver (British Properties / Caulfeild)',
									'whistler'         => 'Whistler (Sunridge / Kadenwood / Alpine)',
									'squamish'         => 'Squamish HQ (Tantalus / Garibaldi Highlands)',
									'north-vancouver'  => 'North Vancouver (Edgemont / Upper Lonsdale)',
									'vancouver-r1-1'   => 'Vancouver (R1-1 Multiplex / Point Grey / Westside)',
									'coquitlam'        => 'Coquitlam (Burke Mountain / SSMUH Multiplex)',
									'sunshine-coast'   => 'Sunshine Coast (Sechelt / Davis Bay / Gibsons)',
									'pemberton'        => 'Pemberton (Acreage Compounds / Meadows)',
									'vancouver-island' => 'Vancouver Island & Greater Victoria',
								);
								foreach ( $kp_corridors_opt as $c_val => $c_lbl ) :
									?>
									<option value="<?php echo esc_attr( $c_val ); ?>" <?php selected( $kp_default_corridor, $c_val ); ?>>
										<?php echo esc_html( $c_lbl ); ?>
									</option>
								<?php endforeach; ?>
							</select>
						</div>
					</div>

					<div class="kp-intake-row">
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-name">Full Name &amp; Firm / Brokerage (if applicable) *</label>
							<input type="text" id="<?php echo esc_attr( $kp_form_id ); ?>-name" name="name" class="kp-intake-input" placeholder="e.g., Jordan Vance / Angell Hasman" required />
						</div>
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-phone">Direct Mobile or Office Line *</label>
							<input type="tel" id="<?php echo esc_attr( $kp_form_id ); ?>-phone" name="phone" class="kp-intake-input" placeholder="(604) 555-0192" required />
						</div>
					</div>

					<div class="kp-intake-row">
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-email">Email Address (For 48-Hr PDF Dossier) *</label>
							<input type="email" id="<?php echo esc_attr( $kp_form_id ); ?>-email" name="email" class="kp-intake-input" placeholder="name@domain.ca" required />
						</div>
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-lot">Civic Address, PID or MLS&reg; Number</label>
							<input type="text" id="<?php echo esc_attr( $kp_form_id ); ?>-lot" name="lot_address" class="kp-intake-input" placeholder="e.g., MLS R2941802 or PID 014-882-910" />
						</div>
					</div>

					<div class="kp-intake-row">
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-type">Build Scope</label>
							<select id="<?php echo esc_attr( $kp_form_id ); ?>-type" name="project_type" class="kp-intake-select">
								<option value="Slope-Critical Custom Estate">Slope-Critical Custom Estate (CCDC 5B)</option>
								<option value="Bill 44 4-6 Unit Multiplex">Bill 44 4–6 Unit SSMUH / R1-1 Multiplex</option>
								<option value="BC Hydro ES54 Civil & 400A-800A PMT">BC Hydro ES54 Underground Civil &amp; 400A–800A PMT</option>
								<option value="Pre-Offer Realtor / Architect Feasibility">48-Hr Pre-Offer Subject-Removal Audit</option>
								<option value="Joint Venture / Landowner Assembly">BC Multiplex / Coastal Joint-Venture Partnership</option>
							</select>
						</div>
						<div class="kp-intake-field">
							<label for="<?php echo esc_attr( $kp_form_id ); ?>-budget">Target Construction Envelope</label>
							<select id="<?php echo esc_attr( $kp_form_id ); ?>-budget" name="budget" class="kp-intake-select">
								<option value="$2.5M – $4.0M CAD">$2.5M – $4.0M CAD</option>
								<option value="$4.0M – $6.5M CAD" selected>$4.0M – $6.5M CAD</option>
								<option value="$6.5M – $10.0M+ CAD">$6.5M – $10.0M+ CAD</option>
								<option value="ES54 Civil / Pre-Construction Audit">Standalone ES54 Civil / Pre-Offer Audit</option>
							</select>
						</div>
					</div>

					<div class="kp-intake-field">
						<label for="<?php echo esc_attr( $kp_form_id ); ?>-msg">Site Notes, Subject-Removal Deadline, or Architectural Stage</label>
						<textarea id="<?php echo esc_attr( $kp_form_id ); ?>-msg" name="message" class="kp-intake-textarea" placeholder="Share slope/geotech questions, target square footage, subject-removal date, or Managing Brokerage name if requesting a BCFSA Rule 5-11 DOR schedule..."></textarea>
					</div>

					<button type="submit" class="kp-v3-btn-gold" style="width:100%;min-height:50px;font-size:0.94rem;">
						Dispatch to Wayne Stevenson (#52603) — 48-Hr Review &rarr;
					</button>

					<div class="kp-intake-status" data-lead-status role="status" aria-live="polite"></div>
				</form>
			</div>

<?php if ( ! $kp_embed_only ) : ?>
		</div>
	</div>
</section>
<?php endif; ?>

<?php if ( empty( $GLOBALS['kp_v3_lead_form_js'] ) ) :
	$GLOBALS['kp_v3_lead_form_js'] = true;
	?>
	<script>
	(function() {
		document.addEventListener('submit', function(e) {
			var form = e.target;
			if (!form || !form.matches || !form.matches('form[data-kp-v3-lead-form="1"]')) return;
			e.preventDefault();
			e.stopImmediatePropagation();

			var statusEl = form.querySelector('[data-lead-status]');
			var btn = form.querySelector('button[type="submit"]');
			var fd = new FormData(form);
			var name = String(fd.get('name') || '').trim();
			var email = String(fd.get('email') || '').trim();
			var phone = String(fd.get('phone') || '').trim();

			if (!name || !email || !phone) {
				if (statusEl) {
					statusEl.className = 'kp-intake-status is-err';
					statusEl.textContent = 'Please enter your name, direct phone number, and email address so Wayne Stevenson can deliver your 48-hour constructability dossier.';
				}
				return;
			}

			var audience = String(fd.get('audience') || '');
			var rawMsg = String(fd.get('message') || '').trim();
			var payload = {
				name: name,
				email: email,
				phone: phone,
				audience: audience,
				location: String(fd.get('location') || ''),
				lot_address: String(fd.get('lot_address') || ''),
				project_type: String(fd.get('project_type') || '') + (audience ? ' [' + audience + ']' : ''),
				budget: String(fd.get('budget') || ''),
				message: rawMsg,
				source_url: window.location.href
			};

			var origLabel = btn ? btn.textContent : '';
			if (btn) { btn.disabled = true; btn.textContent = 'Dispatching Dossier Request...'; }

			fetch(form.getAttribute('action') || '/wp-json/keystone/v1/lead', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			})
			.then(function(r) { return r.json().catch(function() { return { success: r.ok }; }); })
			.then(function(res) {
				if (statusEl) {
					statusEl.className = 'kp-intake-status is-ok';
					statusEl.textContent = (res && res.message) ? res.message : 'Received at Squamish HQ (#52603). Principal Superintendent Wayne Stevenson will review your parcel/scope within 48 business hours.';
				}
				form.reset();
			})
			.catch(function() {
				if (statusEl) {
					statusEl.className = 'kp-intake-status is-err';
					statusEl.textContent = 'Network interruption—please call Wayne Stevenson directly at (604) 848-9688.';
				}
			})
			.finally(function() {
				if (btn) { btn.disabled = false; btn.textContent = origLabel; }
			});
		}, true);
	})();
	</script>
<?php endif; ?>
