<?php
/**
 * Template Name: Regional Hub - Vancouver
 * Template Post Type: page
 *
 * Description: Regional Hub template for City of Vancouver (R1-1 Multiplex & Bill 44 Infill).
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

<div id="primary" class="site-main keystone-regional-hub keystone-vancouver-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">
		
		<header class="page-header" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>📍 REGIONAL HUB // GEO: 49.28270° N, 123.12070° W</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 900; color: #ffffff; margin-bottom: 16px;">
				City of Vancouver Multiplex Advisory &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">R1-1 Infill Engineering</span>
			</h1>
			<p class="lead" style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 840px; margin: 0 auto;">
				Capitalizing on Vancouver R1-1 multiplex zoning reforms, 0.70–1.25 FSR density bonuses, BC Building Code 2024 compliance, and Bill 44 small-scale multi-unit housing (SSMUH) site yields across Kitsilano, Point Grey, Dunbar, and East Vancouver.
			</p>
		</header>

		<!-- Vancouver Municipal Zoning Matrix Card -->
		<section class="zoning-matrix-card" style="background: rgba(10, 15, 25, 0.85); padding: 2.5rem; border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 18px; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);">
			<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 800; color: #d4af37; margin-top: 0; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.04em;">
				🏛️ Vancouver Municipal Zoning Matrix
			</h2>
			<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px;">
				<div style="background: rgba(4, 7, 13, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px;">
					<strong style="color: #38bdf8; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 6px;">Base Zoning:</strong>
					<span style="color: #f8fafc; font-size: 0.95rem;">R1-1 Multiplex District Schedule</span>
				</div>
				<div style="background: rgba(4, 7, 13, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px;">
					<strong style="color: #38bdf8; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 6px;">Allowable Units:</strong>
					<span style="color: #f8fafc; font-size: 0.95rem;">4 to 6 units per single-family lot based on dimensions</span>
				</div>
				<div style="background: rgba(4, 7, 13, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px;">
					<strong style="color: #38bdf8; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 6px;">FSR Range:</strong>
					<span style="color: #f8fafc; font-size: 0.95rem;">Up to 1.0 FSR for multiplex (1.25 FSR near transit nodes)</span>
				</div>
				<div style="background: rgba(4, 7, 13, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 18px;">
					<strong style="color: #38bdf8; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 6px;">Height Limits:</strong>
					<span style="color: #f8fafc; font-size: 0.95rem;">3 Storeys / 11.5 meters</span>
				</div>
			</div>
		</section>

		<!-- Interactive Bill 44 Estimator Embed -->
		<section style="margin: 3rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					CALCULATE YOUR SITE POTENTIAL
				</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0;">
					Vancouver Bill 44 Infill Feasibility Estimator
				</h2>
			</div>
			<?php echo do_shortcode( '[keystone_bill44_estimator]' ); ?>
		</section>

		<!-- Entry Content Loop (if post has Gutenberg blocks) -->
		<div class="entry-content" style="margin: 2rem 0;">
			<?php
			while ( have_posts() ) :
				the_post();
				the_content();
			endwhile;
			?>
		</div>

		<!-- Direct AJAX Lead Intake Form -->
		<section style="background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(4, 7, 13, 0.98)); border: 1.5px solid #d4af37; border-radius: 18px; padding: 40px 32px; margin-top: 40px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);">
			<div style="text-align: center; margin-bottom: 28px;">
				<span style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">
					VANCOUVER INFILL ADVISORY
				</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
					Request a Vancouver Site Feasibility Audit
				</h3>
				<p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
					Direct submission to Wayne Stevenson (BC Builder #52603). Full zoning review, BC Hydro civil capacity check, and pro forma yield model.
				</p>
			</div>

			<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Vancouver Multiplex Feasibility Inquiry" style="max-width: 640px; margin: 0 auto;">
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
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Vancouver Property / Lot Address *</label>
					<input type="text" name="lot_address" required placeholder="e.g. 2480 W 4th Ave, Vancouver, BC" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
				</div>

				<div style="margin-bottom: 24px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Development Vision &amp; Notes</label>
					<textarea name="project_scope" rows="3" placeholder="Describe current lot dimensions, tenant status, or target unit yield..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
				</div>

				<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
					Submit Vancouver Feasibility Request &rarr;
				</button>
			</form>
		</section>

	</div>
</div>

<?php
get_footer();
