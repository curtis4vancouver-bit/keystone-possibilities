<?php
/**
 * Template Name: Credentials
 * Template Post Type: page
 *
 * Description: Official Credentials & Licenses Showcase page.
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
$assets_uri = get_stylesheet_directory_uri() . '/assets/certificates';
?>

<div id="primary" class="site-main keystone-credentials-template" style="background-color: #04070d; color: #f8fafc; min-height: 100vh; padding: 40px 20px 80px;">
	<div class="keystone-container" style="max-width: 1100px; margin: 0 auto;">

		<header class="page-header" style="text-align: center; margin-bottom: 40px;">
			<div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; padding: 6px 18px; border-radius: 9999px; font-size: 0.80rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 18px;">
				<span>🛡️ VERIFIED LICENSURE &amp; REGULATORY CERTIFICATIONS</span>
			</div>
			<h1 class="page-title" style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 900; color: #ffffff; margin-bottom: 16px;">
				Official Builder Credentials &amp;<br>
				<span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Regulatory Compliance</span>
			</h1>
			<p class="lead" style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 840px; margin: 0 auto;">
				BC Housing Licensed Residential Builder <strong>#52603</strong> | Mandatory 2-5-10 WBI Home Warranty Insurance Backed | WorkSafeBC COR Safety Certified | Nominee: Wayne Stevenson.
			</p>
			<div class="header-badges" style="display: flex; gap: 1rem; justify-content: center; margin-top: 1.5rem; flex-wrap: wrap;">
				<a href="https://lims.bchousing.org/LicenceExpiryPortal/licence/52603" target="_blank" rel="noopener" style="background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; padding: 0.75rem 1.5rem; font-weight: 800; border-radius: 9999px; text-decoration: none; font-size: 0.88rem; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.35);">
					✓ Verify BC Housing Licence #52603
				</a>
				<div style="background: rgba(10, 15, 25, 0.85); color: #38bdf8; border: 1px solid #38bdf8; padding: 0.75rem 1.5rem; font-weight: 700; border-radius: 9999px; font-size: 0.88rem;">
					🛡️ 2-5-10 WBI Home Warranty Protection
				</div>
			</div>
		</header>

		<!-- Trust Credentials Overview Card -->
		<section style="background: rgba(10, 15, 25, 0.85); border: 1.5px solid rgba(212, 175, 55, 0.3); border-radius: 18px; padding: 2.2rem; margin: 2.5rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.7);">
			<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; color: #ffffff; margin-top: 0; margin-bottom: 12px;">BC Housing Licence &amp; Statutory Warranty Governance</h2>
			<p style="color: #cbd5e1; font-size: 0.98rem; line-height: 1.7; margin-bottom: 12px;">
				Keystone Possibilities operates under active Residential Builder Licence <strong>#52603</strong> issued by BC Housing Licensing &amp; Consumer Services (Nominee: Wayne Stevenson). All residential construction and multiplex infill developments are fully insured under the BC Homeowner Protection Act (SBC 1998 c. 31), providing 2 years on labor &amp; materials, 5 years on the building envelope, and 10 years on structural integrity.
			</p>
			<p style="color: #94a3b8; font-size: 0.88rem; margin: 0;">
				Official BC Housing Registry Record: <a href="https://lims.bchousing.org/LicenceExpiryPortal/licence/52603" target="_blank" rel="noopener" style="color: #38bdf8; text-decoration: underline;">https://lims.bchousing.org/LicenceExpiryPortal/licence/52603</a>
			</p>
		</section>

		<!-- Certificates Grid (Dark Quiet Luxury Tokens) -->
		<section class="certificates-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; margin: 2.5rem 0;">
			<!-- 1. Safety Certificate -->
			<div class="credential-card" style="background: rgba(10, 15, 25, 0.85); padding: 1.8rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; display: flex; flex-direction: column; justify-space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div>
					<span style="color: #38bdf8; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">01. SAFETY &amp; SITE OPERATIONS</span>
					<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0.6rem; margin-bottom: 10px;">Construction Fire Safety Plan (CFSP) &amp; COR</h3>
					<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6;">Official WorkSafeBC Construction Fire Safety Plan certification and site safety protocol compliance for complex multi-family residential developments.</p>
				</div>
				<div style="margin-top: 1.5rem;">
					<a href="<?php echo esc_url( $assets_uri . '/safety-certificate.jpg' ); ?>" target="_blank" rel="noopener" style="display: inline-block; padding: 0.6rem 1.4rem; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; color: #38bdf8; text-decoration: none; border-radius: 9999px; font-size: 0.84rem; font-weight: 700;">View Safety Certificate (JPG) &rarr;</a>
				</div>
			</div>

			<!-- 2. Calculations Certificate -->
			<div class="credential-card" style="background: rgba(10, 15, 25, 0.85); padding: 1.8rem; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; display: flex; flex-direction: column; justify-space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div>
					<span style="color: #f6d365; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">02. STRUCTURAL CALCULATIONS</span>
					<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0.6rem; margin-bottom: 10px;">Structural &amp; Engineering Calculations Safety</h3>
					<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6;">Smart CPD Certification in construction engineering calculations, structural load-bearing design, and building envelope safety compliance.</p>
				</div>
				<div style="margin-top: 1.5rem;">
					<a href="<?php echo esc_url( $assets_uri . '/calculations-certificate.pdf' ); ?>" target="_blank" rel="noopener" style="display: inline-block; padding: 0.6rem 1.4rem; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #f6d365; text-decoration: none; border-radius: 9999px; font-size: 0.84rem; font-weight: 700;">View Calculations Cert (PDF) &rarr;</a>
				</div>
			</div>

			<!-- 3. Financial Certificate -->
			<div class="credential-card" style="background: rgba(10, 15, 25, 0.85); padding: 1.8rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; display: flex; flex-direction: column; justify-space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div>
					<span style="color: #38bdf8; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">03. FINANCIAL GOVERNANCE</span>
					<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0.6rem; margin-bottom: 10px;">CHBA BC Financial Management Certification</h3>
					<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6;">Canadian Home Builders' Association BC certified financial management, project pro-forma budgeting, and construction accounting controls.</p>
				</div>
				<div style="margin-top: 1.5rem;">
					<a href="<?php echo esc_url( $assets_uri . '/financial-certificate.pdf' ); ?>" target="_blank" rel="noopener" style="display: inline-block; padding: 0.6rem 1.4rem; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; color: #38bdf8; text-decoration: none; border-radius: 9999px; font-size: 0.84rem; font-weight: 700;">View Financial Cert (PDF) &rarr;</a>
				</div>
			</div>

			<!-- 4. Enactments Certificate -->
			<div class="credential-card" style="background: rgba(10, 15, 25, 0.85); padding: 1.8rem; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; display: flex; flex-direction: column; justify-space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div>
					<span style="color: #f6d365; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">04. STATUTORY ENACTMENTS &amp; LAW</span>
					<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0.6rem; margin-bottom: 10px;">CHBA BC Construction Law &amp; Enactments</h3>
					<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6;">Mastery certification in BC statutory construction law, Builders Lien Act compliance, Municipal Land Use Bylaws, and contract administration.</p>
				</div>
				<div style="margin-top: 1.5rem;">
					<a href="<?php echo esc_url( $assets_uri . '/enactments-certificate.pdf' ); ?>" target="_blank" rel="noopener" style="display: inline-block; padding: 0.6rem 1.4rem; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #f6d365; text-decoration: none; border-radius: 9999px; font-size: 0.84rem; font-weight: 700;">View Law &amp; Enactments Cert (PDF) &rarr;</a>
				</div>
			</div>

			<!-- 5. PCC Certificate -->
			<div class="credential-card" style="background: rgba(10, 15, 25, 0.85); padding: 1.8rem; border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; display: flex; flex-direction: column; justify-space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div>
					<span style="color: #38bdf8; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">05. PROJECT CONTROL &amp; SUPERVISION</span>
					<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0.6rem; margin-bottom: 10px;">PCC Project Management &amp; Site Supervision</h3>
					<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6;">CHBA BC Professional Construction Supervision certification, site logistics oversight, and quality control systems.</p>
				</div>
				<div style="margin-top: 1.5rem;">
					<a href="<?php echo esc_url( $assets_uri . '/pcc-certificate.pdf' ); ?>" target="_blank" rel="noopener" style="display: inline-block; padding: 0.6rem 1.4rem; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; color: #38bdf8; text-decoration: none; border-radius: 9999px; font-size: 0.84rem; font-weight: 700;">View PCC Supervision Cert (PDF) &rarr;</a>
				</div>
			</div>

			<!-- 6. CSSA1 Certificate -->
			<div class="credential-card" style="background: rgba(10, 15, 25, 0.85); padding: 1.8rem; border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; display: flex; flex-direction: column; justify-space-between; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
				<div>
					<span style="color: #f6d365; font-weight: 800; font-size: 0.80rem; letter-spacing: 0.05em; text-transform: uppercase;">06. BUILDING CODE &amp; CUSTOMER SERVICE</span>
					<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.25rem; margin-top: 0.6rem; margin-bottom: 10px;">CSSA1 Customer Service &amp; BC Code Part 1</h3>
					<p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6;">CHBA BC Customer Service Excellence and BC Building Code 2024 Part 1 competency certification.</p>
				</div>
				<div style="margin-top: 1.5rem;">
					<a href="<?php echo esc_url( $assets_uri . '/cssa1-certificate.pdf' ); ?>" target="_blank" rel="noopener" style="display: inline-block; padding: 0.6rem 1.4rem; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #f6d365; text-decoration: none; border-radius: 9999px; font-size: 0.84rem; font-weight: 700;">View CSSA1 Code Cert (PDF) &rarr;</a>
				</div>
			</div>
		</section>

		<!-- Estimator Embed -->
		<section style="margin: 3.5rem 0;">
			<div style="text-align: center; margin-bottom: 24px;">
				<span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
					LICENSED BUILDER FEASIBILITY AUDIT
				</span>
				<h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0;">
					Bill 44 Multiplex &amp; Infill Yield Estimator
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
					EXECUTIVE CREDENTIALS CONSULTATION
				</span>
				<h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
					Engage BC Housing Builder #52603
				</h3>
				<p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
					Direct submission to Wayne Stevenson for property feasibility audits, high-performance Step Code 5 custom estates, and Bill 44 multiplex advisory.
				</p>
			</div>

			<form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="Builder Credentials Consultation" style="max-width: 640px; margin: 0 auto;">
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
					<input type="text" name="lot_address" required placeholder="e.g. Metro Vancouver, West Van, Whistler, or Squamish, BC" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
				</div>

				<div style="margin-bottom: 24px;">
					<label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Project Scope &amp; Regulatory Inquiries</label>
					<textarea name="project_scope" rows="3" placeholder="Multiplex unit target, warranty verification, or structural engineering scope..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
				</div>

				<button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
					Submit Credentials Consultation &rarr;
				</button>
			</form>
		</section>

	</div>
</div>

<?php
get_footer();
