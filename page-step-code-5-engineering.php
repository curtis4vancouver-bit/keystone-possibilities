<?php
/**
 * Template Name: Step Code 5 Engineering
 * Template Post Type: page
 *
 * Description: Step Code 5 Net Zero High Performance Engineering page.
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

<div id="primary" class="site-main keystone-engineering-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">

		<header class="page-header" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>⚡ HIGH PERFORMANCE BUILDING ENVELOPE</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 900; color: #ffffff; margin-bottom: 16px;">
				BC Energy Step Code Level 5 &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Net-Zero Engineering</span>
			</h1>
			<p class="lead" style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 840px; margin: 0 auto;">
				Pioneering zero-carbon building performance, airtight envelope engineering (&le; 0.6 ACH50), thermal bridging elimination, and Zehnder HRV mechanical integration across West Vancouver, Whistler, Squamish, and Vancouver custom homes.
			</p>
		</header>

		<?php
		if ( function_exists( 'kp_render_founder_avatar_video_card' ) ) {
			kp_render_founder_avatar_video_card( 'stepcode5' );
		}
		?>

		<!-- Engineering Specifications Grid -->
		<section class="engineering-specs" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 2rem 0;">
			<div class="spec-card" style="background: rgba(10, 15, 25, 0.85); padding: 2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.7);">
				<span style="color: #38bdf8; font-size: 1.5rem; display: block; margin-bottom: 8px;">💨</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Airtightness Mastery</h3>
				<p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">Achieving &le; 0.6 ACH (Air Changes per Hour at 50 Pa) certified by independent third-party Blower Door Testing. Continuous smart vapour retarder membrane sealing on all structural framing.</p>
			</div>
			<div class="spec-card" style="background: rgba(10, 15, 25, 0.85); padding: 2rem; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.7);">
				<span style="color: #f6d365; font-size: 1.5rem; display: block; margin-bottom: 8px;">🧱</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Thermal Envelope R-Values</h3>
				<p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">R-40+ continuous exterior Rockwool insulation, thermally broken clips, and triple-glazed Argon-filled Innotech low-E window assemblies with U-values &le; 0.85 W/(m²K).</p>
			</div>
			<div class="spec-card" style="background: rgba(10, 15, 25, 0.85); padding: 2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.7);">
				<span style="color: #38bdf8; font-size: 1.5rem; display: block; margin-bottom: 8px;">🌿</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">HRV / ERV Mechanical HVAC</h3>
				<p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">High-efficiency balanced heat recovery ventilation delivering 84%+ sensible recovery efficiency (SRE) and continuous HEPA filtration for pristine indoor mountain air quality.</p>
			</div>
		</section>

		<!-- Estimator Embed -->
		<section style="margin: 3rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					STEP CODE 5 PRE-CONSTRUCTION MODEL
				</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0;">
					Net-Zero Energy &amp; Bill 44 Infill Estimator
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
					NET-ZERO ENGINEERING CONSULTATION
				</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
					Plan Your Step Code 5 Custom Build
				</h3>
				<p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
					Direct submission to Wayne Stevenson (BC Builder #52603). Energy model review, airtightness strategy, and zero-carbon compliance roadmap.
				</p>
			</div>

			<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Step Code 5 Engineering Inquiry" style="max-width: 640px; margin: 0 auto;">
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
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Site Address or Project Location *</label>
					<input type="text" name="lot_address" required placeholder="e.g. West Vancouver, Whistler, or Squamish, BC" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
				</div>

				<div style="margin-bottom: 24px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Energy &amp; Architectural Objectives</label>
					<textarea name="project_scope" rows="3" placeholder="Target ACH airtightness, heating system preferences, or solar/geothermal plans..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
				</div>

				<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
					Submit Step Code 5 Request &rarr;
				</button>
			</form>
		</section>

	</div>
</div>

<?php
get_footer();
