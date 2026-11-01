<?php
/**
 * Template Name: Homepage
 * Template Post Type: page
 *
 * Description: Main Homepage template for Keystone Possibilities.
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

<div id="primary" class="site-main keystone-homepage-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">

		<!-- Hero Section -->
		<section class="keystone-hero" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>🏛️ BC HOUSING LICENSED BUILDER #52603</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.4rem, 5.5vw, 3.6rem); font-weight: 900; color: #ffffff; line-height: 1.15; margin-bottom: 20px;">
				Luxury Residential Development &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Bill 44 Multiplex Advisory</span>
			</h1>
			<p class="lead" style="font-size: 1.2rem; line-height: 1.7; color: #94a3b8; max-width: 860px; margin: 0 auto 30px;">
				Navigating complex municipal zoning bylaws, Step Code Level 5 net-zero engineering, and high-yield infill multiplex conversions across Metro Vancouver and the Sea-to-Sky corridor.
			</p>

			<!-- 3D Wireframe HUD Container -->
			<div id="blueprint-3d-canvas-container" class="blueprint-3d-canvas-container" style="background: radial-gradient(circle at center, rgba(56, 189, 248, 0.08) 0%, rgba(10, 15, 25, 0.95) 75%); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 20px; padding: 36px 20px; margin: 2rem auto; max-width: 840px; box-shadow: 0 15px 45px rgba(0,0,0,0.8);">
				<div class="hologram-overlay-hud" style="font-family: 'Courier New', Courier, monospace; font-size: 0.85rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.12em; text-transform: uppercase;">
					⚡ 3D WIREFRAME BLUEPRINT MODEL // 60 FPS CELESTIAL GRAPH TELEMETRY
				</div>
				<p style="color: #cbd5e1; font-size: 0.92rem; margin: 12px auto 0; max-width: 620px;">
					Autonomous building information modeling (BIM), structural load calculations, and energy performance simulations aligned with BC Building Code 2024.
				</p>
			</div>
		</section>

		<?php
		if ( function_exists( 'kp_render_founder_avatar_video_card' ) ) {
			kp_render_founder_avatar_video_card( 'home' );
		}
		?>

		<!-- Credibility Track Scroller -->
		<section class="credibility-scroller-wrapper" style="margin: 3rem 0; overflow-x: auto; padding-bottom: 10px;">
			<div class="credibility-track" style="display: flex; gap: 14px; justify-content: center; flex-wrap: wrap;">
				<span class="credibility-badge" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); color: #f6d365; padding: 8px 18px; border-radius: 9999px; font-size: 0.82rem; font-weight: 700;">✓ BC Housing #52603</span>
				<span class="credibility-badge" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8; padding: 8px 18px; border-radius: 9999px; font-size: 0.82rem; font-weight: 700;">🛡️ 2-5-10 WBI Home Warranty</span>
				<span class="credibility-badge" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); color: #f6d365; padding: 8px 18px; border-radius: 9999px; font-size: 0.82rem; font-weight: 700;">🏗️ WorkSafeBC COR Certified</span>
				<span class="credibility-badge" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8; padding: 8px 18px; border-radius: 9999px; font-size: 0.82rem; font-weight: 700;">⚡ Step Code 5 Master Builder</span>
				<span class="credibility-badge" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); color: #f6d365; padding: 8px 18px; border-radius: 9999px; font-size: 0.82rem; font-weight: 700;">📐 Bill 44 Multiplex Specialist</span>
			</div>
		</section>

		<!-- Core Capabilities Grid -->
		<section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 3rem 0;">
			<div style="background: rgba(10, 15, 25, 0.85); padding: 2.2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #38bdf8; font-size: 1.5rem; display: block; margin-bottom: 8px;">🏢</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Bill 44 Multiplex Infill</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">Unlock 3 to 6 residential units on single-family parcels across Vancouver, North/West Vancouver, Squamish, and Whistler with turnkey planning and general contracting.</p>
			</div>
			<div style="background: rgba(10, 15, 25, 0.85); padding: 2.2rem; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #f6d365; font-size: 1.5rem; display: block; margin-bottom: 8px;">🏔️</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Step Code 5 Luxury Estates</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">Architectural estate construction engineered to Step Code Level 5 and Passive House airtightness (&le; 0.6 ACH50), triple-pane glazing, and zero-carbon mechanical HVAC.</p>
			</div>
			<div style="background: rgba(10, 15, 25, 0.85); padding: 2.2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #38bdf8; font-size: 1.5rem; display: block; margin-bottom: 8px;">📋</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0; margin-bottom: 10px;">Turnkey Feasibility Audits</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">Comprehensive pre-acquisition due diligence: zoning classification, civil utility capacity, development cost charges (DCCs), and class D pro-forma yield modeling.</p>
			</div>
		</section>

		<!-- Estimator Embed -->
		<section style="margin: 3.5rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					INSTANT PROPERTY MODELLING
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
		<section style="background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(4, 7, 13, 0.98)); border: 1.5px solid #d4af37; border-radius: 18px; padding: 40px 32px; margin-top: 40px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);">
			<div style="text-align: center; margin-bottom: 28px;">
				<span style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">
					CONSULT WITH WAYNE STEVENSON
				</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
					Schedule an Executive Development Consultation
				</h3>
				<p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
					Direct submission to BC Housing Licensed Builder #52603. Tailored analysis for landowners, developers, and real estate investment syndicates.
				</p>
			</div>

			<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Homepage Executive Consultation" style="max-width: 640px; margin: 0 auto;">
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
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Site Address or Target Municipality *</label>
					<input type="text" name="lot_address" required placeholder="e.g. Vancouver, West Vancouver, Squamish, or Whistler, BC" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
				</div>

				<div style="margin-bottom: 24px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Project Description &amp; Requirements</label>
					<textarea name="project_scope" rows="3" placeholder="Single-family to multiplex conversion, custom estate build, or property audit..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
				</div>

				<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
					Submit Homepage Consultation Request &rarr;
				</button>
			</form>
		</section>

	</div>
</div>

<?php
get_footer();
