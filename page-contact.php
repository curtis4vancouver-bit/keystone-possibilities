<?php
/**
 * Template Name: Contact
 * Template Post Type: page
 *
 * Description: Executive Contact & Feasibility Consultation page.
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

<div id="primary" class="site-main keystone-contact-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">

		<header class="page-header" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(212, 175, 55, 0.12); border: 1px solid #d4af37; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #f6d365; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>📬 EXECUTIVE CONSULTATION &amp; ADVISORY</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 900; color: #ffffff; margin-bottom: 16px;">
				Initiate Advisory &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Retainer Consultation</span>
			</h1>
			<p class="lead" style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 840px; margin: 0 auto;">
				Connect directly with Wayne Stevenson and the Keystone Possibilities advisory desk for property feasibility audits, municipal zoning analysis, or high-performance residential development oversight.
			</p>
		</header>

		<!-- 2-Column Contact Grid -->
		<section class="contact-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 28px; margin: 2.5rem 0;">
			<!-- Column 1: Headquarters & Licensing -->
			<div class="contact-info-card" style="background: rgba(10, 15, 25, 0.85); padding: 2.2rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<span style="color: #38bdf8; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">HEADQUARTERS &amp; LICENSING</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; color: #ffffff; margin-top: 0.6rem; margin-bottom: 16px;">Keystone Possibilities Ltd</h2>
				
				<div style="margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
					<strong style="color: #f6d365; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 4px;">BC Housing Builder Licence:</strong>
					<span style="color: #cbd5e1; font-size: 0.95rem;">#52603 (Nominee: Wayne Stevenson)</span>
				</div>

				<div style="margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
					<strong style="color: #f6d365; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 4px;">Home Warranty Protection:</strong>
					<span style="color: #cbd5e1; font-size: 0.95rem;">Mandatory 2-5-10 WBI Home Warranty Insurance</span>
				</div>

				<div style="margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
					<strong style="color: #f6d365; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 4px;">Primary Service Corridor:</strong>
					<span style="color: #cbd5e1; font-size: 0.95rem;">Metro Vancouver, West Vancouver, North Vancouver, Squamish, and Whistler, BC</span>
				</div>

				<div style="margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px;">
					<strong style="color: #f6d365; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 4px;">Pre-Construction Advisory:</strong>
					<span style="color: #cbd5e1; font-size: 0.95rem;">Turnkey Land &amp; Construction Feasibility Audit</span>
				</div>

				<div>
					<strong style="color: #f6d365; display: block; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 4px;">Direct Registry Verification:</strong>
					<a href="https://lims.bchousing.org/LicenceExpiryPortal/licence/52603" target="_blank" rel="noopener" style="color: #38bdf8; text-decoration: underline; font-size: 0.88rem;">BC Housing Public Registry #52603</a>
				</div>
			</div>

			<!-- Column 2: Advisory Request Form -->
			<div class="contact-form-card" style="background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(4, 7, 13, 0.98)); padding: 2.2rem; border: 1.5px solid #d4af37; border-radius: 18px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);">
				<span style="color: #d4af37; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">DIRECT ADVISORY INTAKE</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; color: #ffffff; margin-top: 0.6rem; margin-bottom: 16px;">Request Consultation</h2>

				<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Executive Contact Consultation" class="keystone-contact-form">
					<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
						<div>
							<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">First Name *</label>
							<input type="text" name="first_name" required placeholder="First Name" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
						</div>
						<div>
							<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Surname *</label>
							<input type="text" name="surname" required placeholder="Surname" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
						</div>
					</div>

					<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px;">
						<div>
							<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Email Address *</label>
							<input type="email" name="client_email" required placeholder="name@domain.com" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
						</div>
						<div>
							<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Phone Number *</label>
							<input type="tel" name="client_phone" required placeholder="(604) 000-0000" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
						</div>
					</div>

					<div style="margin-bottom: 14px;">
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Site Address or Parcel PID *</label>
						<input type="text" name="lot_address" required placeholder="e.g. 1234 Marine Drive, West Vancouver or PID" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
					</div>

					<div style="margin-bottom: 14px;">
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Service Interest</label>
						<select name="service_interest" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
							<option value="retainer">Turnkey Land &amp; Construction Feasibility Audit</option>
							<option value="multiplex">Bill 44 SSMUH Multiplex Development (3–6 Units)</option>
							<option value="luxury">Luxury Custom Home / Step Code 5 Estate</option>
							<option value="investor">Developer / Realtor Feasibility Syndication</option>
						</select>
					</div>

					<div style="margin-bottom: 20px;">
						<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Project Description</label>
						<textarea name="project_scope" rows="3" placeholder="Target square footage, unit count, or development timeline..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
					</div>

					<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
						Submit Advisory Inquiry &rarr;
					</button>
				</form>
			</div>
		</section>

		<!-- Estimator Embed -->
		<section style="margin: 3.5rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					INSTANT PRO-FORMA SIZING
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

	</div>
</div>

<?php
get_footer();
