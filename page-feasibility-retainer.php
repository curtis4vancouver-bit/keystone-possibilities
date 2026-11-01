<?php
/**
 * Template Name: Feasibility Retainer
 * Template Post Type: page
 *
 * Description: Property Feasibility & Risk Mitigation Audit Retainer landing page.
 * Upgraded with Dark Quiet Luxury tokens (#04070d, #d4af37, #38bdf8), Bill 44 Estimator & Lead Form.
 *
 * @package KeystonePossibilitiesChild
 * @version 2.8.0
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

get_header();
?>

<div id="primary" class="site-main keystone-retainer-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">

		<header class="page-header" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.12); border: 1px solid #d4af37; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #f6d365; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>💎 TURNKEY FEASIBILITY AUDIT // PRE-ACQUISITION DE-RISKING</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 900; color: #ffffff; margin-bottom: 16px;">
				Property Feasibility &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Risk Mitigation Audit</span>
			</h1>
			<p class="lead" style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 840px; margin: 0 auto;">
				De-risk your residential parcel, multiplex acquisition, or high-performance custom build prior to committing capital. We analyze municipal zoning bylaws, Step Code 5 envelope parameters, BC Hydro grid capacity, and civil servicing constraints across Metro Vancouver and the Sea-to-Sky corridor.
			</p>
		</header>

		<?php
		if ( function_exists( 'kp_render_founder_avatar_video_card' ) ) {
			kp_render_founder_avatar_video_card( 'feasibility' );
		}
		?>

		<!-- Feasibility Deliverables Cards -->
		<section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 2.5rem 0;">
			<div style="background: rgba(10, 15, 25, 0.85); padding: 2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #38bdf8; font-size: 1.5rem; display: block; margin-bottom: 8px;">📐</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Bylaw &amp; Density Yield</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">Exhaustive review of SSMUH / Bill 44 small-scale multi-unit housing parameters, setbacks, floor space ratio (FSR), height allowances, and building massing potential.</p>
			</div>
			<div style="background: rgba(10, 15, 25, 0.85); padding: 2rem; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #f6d365; font-size: 1.5rem; display: block; margin-bottom: 8px;">⚡</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Infrastructure &amp; Servicing</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">Evaluation of BC Hydro 200A/400A service availability, municipal sanitary/storm sewer capacity, water meter sizing, and offsite civil engineering obligations.</p>
			</div>
			<div style="background: rgba(10, 15, 25, 0.85); padding: 2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #38bdf8; font-size: 1.5rem; display: block; margin-bottom: 8px;">📊</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Class D Pro-Forma Budget</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">Comprehensive pre-construction financial modeling covering soft costs, municipal DCCs, development levies, hard construction estimates, and projected net yields.</p>
			</div>
		</section>

		<!-- Interactive Feasibility Calculator Card -->
		<section id="feasibility-calculator" style="background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(4, 7, 13, 0.98)); border: 1.5px solid rgba(212, 175, 55, 0.4); border-radius: 18px; padding: 36px 32px; margin: 3rem 0; box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #f6d365; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					INSTANT YIELD MODELLING
				</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0;">
					Bill 44 Infill Multiplex Yield Calculator
				</h2>
			</div>

			<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin-bottom: 24px;">
				<div>
					<label for="lot-size" style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Lot Size (Sq Meters):</label>
					<input type="number" id="lot-size" value="350" min="100" max="5000" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.95rem; box-sizing: border-box;">
				</div>
				<div>
					<label for="zoning" style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Current Zoning Designation:</label>
					<select id="zoning" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.95rem; box-sizing: border-box;">
						<option value="R1-1">Vancouver R1-1 Single Detached / Multiplex</option>
						<option value="RS-1">North Van / West Van Single Family</option>
						<option value="RL-1">Squamish Infill Zone</option>
						<option value="R3">Whistler Residential</option>
					</select>
				</div>
			</div>

			<div style="margin-bottom: 24px;">
				<label style="display: flex; align-items: center; gap: 10px; font-size: 0.90rem; color: #cbd5e1; cursor: pointer;">
					<input type="checkbox" id="transit-proximity" checked style="width: 18px; height: 18px; accent-color: #38bdf8;">
					Frequent Transit Service Area (FTSA) Proximity (&lt; 400m from bus/skytrain corridor)
				</label>
			</div>

			<div class="calc-results" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; background: rgba(5, 8, 14, 0.7); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 20px;">
				<div>
					<div style="font-size: 0.78rem; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px;">Projected Units</div>
					<div id="yield-units" style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 900; color: #38bdf8;">4 Units</div>
				</div>
				<div>
					<div style="font-size: 0.78rem; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px;">Max Site Coverage</div>
					<div id="yield-coverage" style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 900; color: #f6d365;">45%</div>
				</div>
				<div>
					<div style="font-size: 0.78rem; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px;">Gross Buildable Value</div>
					<div id="yield-roi" style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 900; color: #ffffff;">$3,500,000 CAD</div>
				</div>
			</div>
		</section>

		<script>
		document.addEventListener('DOMContentLoaded', function() {
			var lotInput = document.getElementById('lot-size');
			var zoningSelect = document.getElementById('zoning');
			var ftsaCheck = document.getElementById('transit-proximity');
			var unitsEl = document.getElementById('yield-units');
			var coverageEl = document.getElementById('yield-coverage');
			var roiEl = document.getElementById('yield-roi');

			function recalculateYield() {
				if (!lotInput || !unitsEl) return;
				var sqM = parseFloat(lotInput.value) || 350;
				var isFtsa = ftsaCheck ? ftsaCheck.checked : false;
				var units = 4;
				var coverage = 45;
				var baseRate = 875000;

				if (sqM >= 280) {
					units = isFtsa ? 6 : 4;
					coverage = isFtsa ? 50 : 45;
				} else {
					units = 3;
					coverage = 40;
				}

				var totalEst = units * baseRate;
				unitsEl.textContent = units + ' Units';
				coverageEl.textContent = coverage + '%';
				roiEl.textContent = '$' + totalEst.toLocaleString('en-CA') + ' CAD';
			}

			if (lotInput) lotInput.addEventListener('input', recalculateYield);
			if (zoningSelect) zoningSelect.addEventListener('change', recalculateYield);
			if (ftsaCheck) ftsaCheck.addEventListener('change', recalculateYield);
		});
		</script>

		<!-- Estimator Embed -->
		<section style="margin: 3.5rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					DETAILED PRO-FORMA SIZING
				</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0;">
					Bill 44 Multiplex &amp; Construction Estimator
				</h2>
			</div>
			<?php echo do_shortcode( '[keystone_bill44_estimator]' ); ?>
		</section>

		<!-- Entry Content Loop -->
		<div class="entry-content" style="margin: 2rem 0;">
			<?php
			while ( have_posts() ) :
				the_post();
				the_content();
			endwhile;
			?>
		</div>

		<!-- Direct Lead Intake Form -->
		<section id="kp-feasibility-intake" style="background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(4, 7, 13, 0.98)); border: 1.5px solid #d4af37; border-radius: 18px; padding: 40px 32px; margin-top: 40px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);">
			<div style="text-align: center; margin-bottom: 28px;">
				<span style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">
					LOCK IN ADVISORY CAPACITY
				</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
					Commission Turnkey Land &amp; Construction Feasibility Audit
				</h3>
				<p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
					Direct submission to Wayne Stevenson (BC Housing Licensed Builder #52603). Receive our comprehensive pre-construction feasibility dossier and municipal development roadmap.
				</p>
			</div>

			<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Turnkey Land &amp; Construction Feasibility Plan" style="max-width: 640px; margin: 0 auto;">
				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
					<div>
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">First Name *</label>
						<input type="text" name="first_name" required placeholder="First Name" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
					</div>
					<div>
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Surname *</label>
						<input type="text" name="surname" required placeholder="Surname" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
					</div>
				</div>

				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
					<div>
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Email Address *</label>
						<input type="email" name="client_email" required placeholder="name@domain.com" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
					</div>
					<div>
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Phone Number *</label>
						<input type="tel" name="client_phone" required placeholder="(604) 000-0000" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
					</div>
				</div>

				<div style="margin-bottom: 16px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Property Address or PID *</label>
					<input type="text" name="lot_address" required placeholder="e.g. 1234 Marine Drive, West Vancouver or PID" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
				</div>

				<div style="margin-bottom: 24px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Development Vision &amp; Time Horizon</label>
					<textarea name="project_scope" rows="3" placeholder="Target timeline, multiplex unit objective, or pre-acquisition subject removal deadline..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
				</div>

				<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
					Request Turnkey Feasibility Plan &rarr;
				</button>
			</form>
		</section>

	</div>
</div>

<?php
get_footer();
