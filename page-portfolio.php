<?php
/**
 * Template Name: Portfolio Carousel
 * Template Post Type: page
 *
 * Description: Interactive 3D Portfolio Carousel page.
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

<div id="primary" class="site-main keystone-portfolio-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">

		<header class="page-header" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>🏆 BUILT PROJECTS // ARCHITECTURAL PORTFOLIO</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 900; color: #ffffff; margin-bottom: 16px;">
				Luxury Residential &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Multiplex Portfolio</span>
			</h1>
			<p class="lead" style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 840px; margin: 0 auto;">
				Explore completed high-performance custom residences, Bill 44 infill multiplex transformations, and Step Code 5 alpine chalets delivered across Vancouver, West Vancouver, Squamish, and Whistler.
			</p>
		</header>

		<!-- Portfolio Showcase Grid -->
		<section class="portfolio-showcase-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; margin: 2.5rem 0;">
			<!-- Project 1 -->
			<div class="portfolio-card" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
					<span style="color: #38bdf8; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">VANCOUVER // POINT GREY</span>
					<span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; font-weight: 700;">4-UNIT INFILL</span>
				</div>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.35rem; margin-top: 0; margin-bottom: 10px;">Point Grey Multiplex Conversion</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin-bottom: 16px;">
					Transforming a standard 33×122 RS-1 single-family lot into a 4-unit luxury infill multiplex under Bill 44 SSMUH bylaws. Features private courtyard entries, detached lock-off suites, and zero-carbon mechanical design.
				</p>
				<div style="display: flex; gap: 12px; font-size: 0.82rem; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.08); pt-2; padding-top: 12px;">
					<div><strong>FSR:</strong> 1.0</div>
					<div>&bull;</div>
					<div><strong>Valuation:</strong> $4.2M CAD</div>
					<div>&bull;</div>
					<div><strong>Airtight:</strong> 0.8 ACH</div>
				</div>
			</div>

			<!-- Project 2 -->
			<div class="portfolio-card" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
					<span style="color: #f6d365; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">WEST VANCOUVER // BRITISH PROPERTIES</span>
					<span style="background: rgba(212, 175, 55, 0.15); color: #f6d365; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; font-weight: 700;">CUSTOM ESTATE</span>
				</div>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.35rem; margin-top: 0; margin-bottom: 10px;">British Properties High-Performance Estate</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin-bottom: 16px;">
					7,200 sq ft custom modern estate engineered on steep bedrock terrain. Step Code 5 thermal envelope, continuous exterior insulation, commercial curtain wall glazing, and integrated geothermal heating.
				</p>
				<div style="display: flex; gap: 12px; font-size: 0.82rem; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px;">
					<div><strong>Scale:</strong> 7,200 sq ft</div>
					<div>&bull;</div>
					<div><strong>Valuation:</strong> $11.5M CAD</div>
					<div>&bull;</div>
					<div><strong>Step Code:</strong> Level 5</div>
				</div>
			</div>

			<!-- Project 3 -->
			<div class="portfolio-card" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
					<span style="color: #38bdf8; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">WHISTLER // SUNRIDGE PLATEAU</span>
					<span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; font-weight: 700;">STEP CODE 5 CHALET</span>
				</div>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.35rem; margin-top: 0; margin-bottom: 10px;">Sunridge Alpine Passive Chalet</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin-bottom: 16px;">
					Extreme alpine climate luxury build featuring heavy timber post-and-beam construction, airtightness of 0.48 ACH50, triple-glazed Swiss window profiles, and balanced Zehnder HRV heat recovery.
				</p>
				<div style="display: flex; gap: 12px; font-size: 0.82rem; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px;">
					<div><strong>Scale:</strong> 5,800 sq ft</div>
					<div>&bull;</div>
					<div><strong>Valuation:</strong> $8.9M CAD</div>
					<div>&bull;</div>
					<div><strong>Airtight:</strong> 0.48 ACH</div>
				</div>
			</div>

			<!-- Project 4 -->
			<div class="portfolio-card" style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
					<span style="color: #f6d365; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;">SQUAMISH // HIGHLANDS INFILL</span>
					<span style="background: rgba(212, 175, 55, 0.15); color: #f6d365; font-size: 0.75rem; padding: 4px 10px; border-radius: 9999px; font-weight: 700;">4-UNIT MULTIPLEX</span>
				</div>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.35rem; margin-top: 0; margin-bottom: 10px;">Garibaldi Infill Multiplex Development</h3>
				<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin-bottom: 16px;">
					Modern mountain aesthetic 4-unit multiplex development utilizing prefabricated off-site panelized wall assemblies, EV-ready 400A service, and acoustic mass timber subfloors for sound mitigation.
				</p>
				<div style="display: flex; gap: 12px; font-size: 0.82rem; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px;">
					<div><strong>Units:</strong> 4 Units</div>
					<div>&bull;</div>
					<div><strong>Valuation:</strong> $3.6M CAD</div>
					<div>&bull;</div>
					<div><strong>Assembly:</strong> Panelized</div>
				</div>
			</div>
		</section>

		<!-- Swiper Carousel Markup (Preserved for JavaScript Carousel Integration) -->
		<section class="portfolio-carousel-wrapper" style="margin: 2rem 0; display: none;">
			<div class="swiper swiper-portfolio-container">
				<div class="swiper-wrapper">
					<div class="swiper-slide"><div class="swiper-slide-title">Point Grey Multiplex // Vancouver</div></div>
					<div class="swiper-slide"><div class="swiper-slide-title">British Properties Estate // West Vancouver</div></div>
					<div class="swiper-slide"><div class="swiper-slide-title">Alpine Step Code 5 Chalet // Whistler</div></div>
					<div class="swiper-slide"><div class="swiper-slide-title">Garibaldi Infill Multiplex // Squamish</div></div>
				</div>
				<div class="swiper-pagination"></div>
				<div class="swiper-button-next"></div>
				<div class="swiper-button-prev"></div>
			</div>
		</section>

		<!-- Estimator Embed -->
		<section style="margin: 3.5rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					MODEL YOUR PARCEL
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
					START YOUR ARCHITECTURAL BUILD
				</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
					Connect with Licensed Builder #52603
				</h3>
				<p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
					Direct submission to Wayne Stevenson. Custom architectural residences, infill multiplex joint ventures, and municipal advisory.
				</p>
			</div>

			<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Portfolio & Development Inquiry" style="max-width: 640px; margin: 0 auto;">
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
					<input type="text" name="lot_address" required placeholder="e.g. Vancouver, West Vancouver, Whistler, or Squamish, BC" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
				</div>

				<div style="margin-bottom: 24px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Project Description</label>
					<textarea name="project_scope" rows="3" placeholder="Target square footage, budget, or architectural goals..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
				</div>

				<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
					Submit Portfolio Consultation Request &rarr;
				</button>
			</form>
		</section>

	</div>
</div>

<?php
get_footer();
