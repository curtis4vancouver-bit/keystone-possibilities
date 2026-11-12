<?php
/**
 * Template Part: 17-Certificate Statutory & Qualification Museum Vault
 *
 * Displays all 17 visually verified genuine certificates with printed ground-truth captions,
 * category filter pills, and High-Resolution Document Zoom Lightbox Modal.
 * Supports $args['mode'] = 'reel' | 'grid'.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_mode       = isset( $args['mode'] ) && in_array( $args['mode'], array( 'reel', 'grid' ), true ) ? $args['mode'] : 'reel';
$kp_section_id = isset( $args['section_id'] ) ? sanitize_html_class( (string) $args['section_id'] ) : 'credentials';
$kp_kicker     = isset( $args['kicker'] ) ? (string) $args['kicker'] : 'STATUTORY & TECHNICAL QUALIFICATION ARCHIVE · 17 PRIMARY DOCUMENTS';
$kp_heading    = isset( $args['heading'] ) ? (string) $args['heading'] : 'Every Licence, Utility Registry & Building Code Credential—Open for Inspection.';
$kp_subcopy    = isset( $args['subcopy'] ) ? (string) $args['subcopy'] : 'Click any certificate in Wayne Stevenson’s museum vault to inspect the full-resolution document issued by BC Housing, BC Hydro, WorkSafeBC, CHBA BC, Smart CPD, and St. John Ambulance.';

// Ground-truth visually verified 17 certificates (exact printed titles, issuers & live WP URLs).
$kp_fallback_credentials = array(
	array(
		'id'         => 'cert-01-bc-housing-52603',
		'title'      => 'Residential Builder Licence Certificate — #52603',
		'issuer'     => 'BC Housing Licensing & Consumer Services',
		'meta'       => 'Licence #52603 · General Contractor · Active Standing (Exp. May 31, 2027)',
		'category'   => 'statutory',
		'cat_label'  => 'Statutory & Utility',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/ResidentialBuilderLicenceCertificate.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-02-bc-hydro-es54',
		'title'      => 'Official BC Hydro Registered Civil Contractor Directory Listing',
		'issuer'     => 'BC Hydro ES54 Underground Civil Infrastructure Registry',
		'meta'       => 'Wayne Stevenson · 1 Watts Point Rd, Squamish · WP ID 1668 / Full Registry Sheet ID 1665',
		'category'   => 'statutory',
		'cat_label'  => 'Statutory & Utility',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/bc-hydro-civil-contractor-verified-proof.png',
		'alt_sheet'  => 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/bc-hydro-registered-civil-contractor-registry-proof.png',
	),
	array(
		'id'         => 'cert-03-worksafebc-clearance',
		'title'      => 'WorkSafeBC Registration & Good Standing Clearance Letter',
		'issuer'     => 'WorkSafeBC Employer Assessment & Clearance Registry',
		'meta'       => 'Account #201703481 · Clearance Reference #C135925638 · Active Good Standing',
		'category'   => 'statutory',
		'cat_label'  => 'Statutory & Utility',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/WCB-Clearance-Letter.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-04-bcbc-2024-mod1',
		'title'      => '2024 BC Building Code Module 1',
		'issuer'     => 'Smart CPD Continuing Professional Development',
		'meta'       => '7 Accredited BC Housing CPD Points · Completed 25 Sep 2025',
		'category'   => 'bcbc-2024',
		'cat_label'  => 'BCBC 2024',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/certificate-2024-bc-building-code-module-1-684c6359f085d1dbed0df52c.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-05-bcbc-2024-mod2',
		'title'      => '2024 BC Building Code Module 2',
		'issuer'     => 'Smart CPD Continuing Professional Development',
		'meta'       => '7 Accredited BC Housing CPD Points · Completed 28 Oct 2025',
		'category'   => 'bcbc-2024',
		'cat_label'  => 'BCBC 2024',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/certificate-2024-bc-building-code-module-2-690143d7a56f94ec4a08b97a.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-06-bcbc-2024-mod3',
		'title'      => '2024 BC Building Code Module - 3',
		'issuer'     => 'Smart CPD Continuing Professional Development',
		'meta'       => '7 Accredited BC Housing CPD Points · Completed 28 Oct 2025',
		'category'   => 'bcbc-2024',
		'cat_label'  => 'BCBC 2024',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/bc-building-code-2024-module-3.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-07-chba-part1',
		'title'      => 'BC Building Code Part 1 Course',
		'issuer'     => 'Canadian Home Builders’ Association of BC (CHBA BC)',
		'meta'       => '42 Group A Accredited Qualification Points · Core Builder Qualification',
		'category'   => 'chba',
		'cat_label'  => 'CHBA Qualifications',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/chba_1.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-08-chba-warranty',
		'title'      => 'Service & Warranty Course',
		'issuer'     => 'Canadian Home Builders’ Association of BC (CHBA BC)',
		'meta'       => '28 Group A Accredited Qualification Points · 2-5-10 Home Warranty Standard',
		'category'   => 'chba',
		'cat_label'  => 'CHBA Qualifications',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/chba_2.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-09-chba-financial',
		'title'      => 'Financial Management Course',
		'issuer'     => 'Canadian Home Builders’ Association of BC (CHBA BC)',
		'meta'       => '28 Group B Accredited Qualification Points · Construction Trust & Cost Control',
		'category'   => 'chba',
		'cat_label'  => 'CHBA Qualifications',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/chba_3.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-10-chba-science',
		'title'      => 'Building Science for New Homes Course',
		'issuer'     => 'Canadian Home Builders’ Association of BC (CHBA BC)',
		'meta'       => '24 Group A Accredited Qualification Points · High-Performance Envelopes & Vapour Control',
		'category'   => 'chba',
		'cat_label'  => 'CHBA Qualifications',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/chba_4.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-11-chba-part2',
		'title'      => 'BC Building Code Part 2 Course',
		'issuer'     => 'Canadian Home Builders’ Association of BC (CHBA BC)',
		'meta'       => '66 Group A Accredited Qualification Points · Structural & Part 9/Part 3 Mastery',
		'category'   => 'chba',
		'cat_label'  => 'CHBA Qualifications',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/chba_5.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-12-chba-supervision',
		'title'      => 'Project Management & Site Supervision Course',
		'issuer'     => 'Canadian Home Builders’ Association of BC (CHBA BC)',
		'meta'       => '30 Group A + 8 Group B Points · Critical-Path Superintendence & Trade Governance',
		'category'   => 'chba',
		'cat_label'  => 'CHBA Qualifications',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/chba_6.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-13-first-aid',
		'title'      => 'Basic First Aid (Emergency) & Level A CPR/AED Certificate',
		'issuer'     => 'St. John Ambulance Canada',
		'meta'       => 'Active Site Safety Certification · Valid Through June 30, 2028',
		'category'   => 'cpd-safety',
		'cat_label'  => 'CPD & Safety',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/first-aid-certificate.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-14-cpd-calculations',
		'title'      => 'Practical Construction Calculations (Online) - 7 CPD',
		'issuer'     => 'Smart CPD Accredited Training',
		'meta'       => '7 Accredited CPD Points · Structural & Volumetric Takeoff Calculations',
		'category'   => 'cpd-safety',
		'cat_label'  => 'CPD & Safety',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2024/04/screenshot-2024-04-08-at-10.11.40-am.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-15-cpd-site-safety',
		'title'      => 'Construction Site Safety Awareness 1 (Online) - 6 CPD',
		'issuer'     => 'Smart CPD Accredited Training',
		'meta'       => '6 Accredited CPD Points · WorkSafeBC Excavation & Jobsite Hazard Controls',
		'category'   => 'cpd-safety',
		'cat_label'  => 'CPD & Safety',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2024/04/screenshot-2024-04-08-at-10.11.00-am.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-16-cpd-fire-safety',
		'title'      => 'Construction Fire Safety Plan (Online) - 4 CPD',
		'issuer'     => 'Smart CPD Accredited Training',
		'meta'       => '4 Accredited CPD Points · High-Resolution Certificate Record (WP ID 323)',
		'category'   => 'cpd-safety',
		'cat_label'  => 'CPD & Safety',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2024/04/screenshot-2024-04-08-at-10.12.07-am.png',
		'alt_sheet'  => '',
	),
	array(
		'id'         => 'cert-17-cpd-financial-planning',
		'title'      => 'Financial Planning (Online) - 3 CPD',
		'issuer'     => 'Smart CPD Accredited Training',
		'meta'       => '3 Accredited CPD Points · Open-Book Pro-Forma & Draw Governance',
		'category'   => 'cpd-safety',
		'cat_label'  => 'CPD & Safety',
		'image'      => 'https://keystonepossibilities.ca/wp-content/uploads/2024/04/screenshot-2024-04-08-at-10.12.34-am.png',
		'alt_sheet'  => '',
	),
);

$kp_raw_certs = function_exists( 'kp_get_verified_credentials' ) ? kp_get_verified_credentials() : $kp_fallback_credentials;
if ( ! is_array( $kp_raw_certs ) || count( $kp_raw_certs ) < 17 ) {
	$kp_raw_certs = $kp_fallback_credentials;
}

// Normalize any incoming array structure while rejecting decorative AI badge graphics (ID 1463 / 1618).
$kp_certs = array();
foreach ( $kp_raw_certs as $c_idx => $cert ) {
	if ( ! is_array( $cert ) ) {
		continue;
	}
	$img = '';
	foreach ( array( 'image', 'url', 'source_url', 'src' ) as $ikey ) {
		if ( ! empty( $cert[ $ikey ] ) && is_string( $cert[ $ikey ] ) ) {
			$img = $cert[ $ikey ];
			break;
		}
	}
	if ( '' === $img || false !== stripos( $img, 'civil-utilities' ) || false !== stripos( $img, 'bc_builder_badge_52603' ) ) {
		continue;
	}
	$cat_raw = strtolower( (string) ( $cert['category'] ?? '' ) );
	if ( false !== strpos( $cat_raw, 'statut' ) || false !== strpos( $cat_raw, 'util' ) || false !== strpos( $cat_raw, 'licen' ) ) {
		$cat_slug  = 'statutory';
		$cat_label = 'Statutory & Utility';
	} elseif ( false !== strpos( $cat_raw, '2024' ) || false !== strpos( $cat_raw, 'bcbc' ) ) {
		$cat_slug  = 'bcbc-2024';
		$cat_label = 'BCBC 2024';
	} elseif ( false !== strpos( $cat_raw, 'chba' ) ) {
		$cat_slug  = 'chba';
		$cat_label = 'CHBA Qualifications';
	} else {
		$cat_slug  = 'cpd-safety';
		$cat_label = 'CPD & Safety';
	}

	$kp_certs[] = array(
		'id'        => isset( $cert['id'] ) ? sanitize_title( (string) $cert['id'] ) : 'cert-' . ( $c_idx + 1 ),
		'title'     => isset( $cert['title'] ) ? (string) $cert['title'] : ( isset( $cert['caption'] ) ? (string) $cert['caption'] : 'Verified Credential' ),
		'issuer'    => isset( $cert['issuer'] ) ? (string) $cert['issuer'] : 'Accredited BC Authority',
		'meta'      => isset( $cert['meta'] ) ? (string) $cert['meta'] : ( isset( $cert['details'] ) ? (string) $cert['details'] : 'Verified Primary Document' ),
		'category'  => $cat_slug,
		'cat_label' => isset( $cert['cat_label'] ) ? (string) $cert['cat_label'] : $cat_label,
		'image'     => $img,
		'alt_sheet' => isset( $cert['alt_sheet'] ) ? (string) $cert['alt_sheet'] : ( isset( $cert['full_sheet_url'] ) ? (string) $cert['full_sheet_url'] : '' ),
	);
}

if ( count( $kp_certs ) < 17 ) {
	$kp_certs = $kp_fallback_credentials;
}

$kp_vault_uid = wp_unique_id( 'kp-vault-' );

if ( empty( $GLOBALS['kp_v3_credential_vault_css'] ) ) :
	$GLOBALS['kp_v3_credential_vault_css'] = true;
	?>
	<style id="kp-v3-credential-vault-styles">
		.kp-vault-section {
			padding: clamp(56px, 7vw, 90px) 0;
			background: linear-gradient(180deg, #060a14 0%, #04070d 100%);
			color: #f8fafc;
			border-top: 1px solid rgba(212, 175, 55, 0.16);
		}
		.kp-vault-wrap {
			width: min(1340px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-vault-header {
			display: flex;
			flex-wrap: wrap;
			justify-content: space-between;
			align-items: flex-end;
			gap: 18px;
			margin-bottom: 22px;
		}
		.kp-vault-kicker {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: #d4af37;
			margin-bottom: 8px;
		}
		.kp-vault-h2 {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.6rem, 3vw, 2.35rem);
			font-weight: 700;
			line-height: 1.16;
			color: #f8fafc;
			margin: 0 0 10px;
			max-width: 780px;
		}
		.kp-vault-sub {
			font-size: 0.95rem;
			line-height: 1.6;
			color: #cbd5e1;
			max-width: 760px;
			margin: 0;
		}
		.kp-vault-filters {
			display: flex;
			flex-wrap: wrap;
			gap: 8px;
			margin-bottom: 24px;
		}
		.kp-vault-pill {
			background: rgba(10, 16, 29, 0.9);
			border: 1px solid rgba(212, 175, 55, 0.26);
			color: #cbd5e1;
			border-radius: 999px;
			padding: 8px 15px;
			min-height: 38px;
			font-size: 0.78rem;
			font-weight: 600;
			cursor: pointer;
			transition: all 0.2s ease;
		}
		.kp-vault-pill:hover,
		.kp-vault-pill.is-active {
			background: rgba(212, 175, 55, 0.16);
			border-color: #d4af37;
			color: #f8fafc;
		}
		.kp-vault-track.is-reel {
			display: grid;
			grid-auto-flow: column;
			grid-auto-columns: minmax(265px, 310px);
			gap: 18px;
			overflow-x: auto;
			scroll-snap-type: x mandatory;
			scroll-behavior: smooth;
			padding-bottom: 14px;
		}
		@media (max-width: 480px) {
			.kp-vault-track.is-reel {
				grid-auto-columns: minmax(252px, 82vw);
			}
		}
		.kp-vault-track.is-grid {
			display: grid;
			grid-template-columns: repeat(auto-fill, minmax(min(100%, 285px), 1fr));
			gap: 20px;
		}
		.kp-vault-card {
			scroll-snap-align: start;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.24);
			border-radius: 16px;
			padding: 14px;
			display: flex;
			flex-direction: column;
			gap: 12px;
			cursor: pointer;
			transition: border-color 0.22s ease, transform 0.22s ease, box-shadow 0.22s ease;
		}
		.kp-vault-card:hover {
			border-color: #d4af37;
			transform: translateY(-3px);
			box-shadow: 0 20px 44px rgba(0, 0, 0, 0.65);
		}
		.kp-vault-card[hidden] {
			display: none !important;
		}
		.kp-vault-mat {
			background: linear-gradient(145deg, #f8f5ee 0%, #ebe4d5 100%);
			border-radius: 10px;
			padding: 12px;
			aspect-ratio: 4 / 3;
			display: flex;
			align-items: center;
			justify-content: center;
			overflow: hidden;
			box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.12);
		}
		.kp-vault-mat img {
			width: 100%;
			height: 100%;
			object-fit: contain;
			display: block;
		}
		.kp-vault-cat {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.66rem;
			font-weight: 700;
			text-transform: uppercase;
			letter-spacing: 0.06em;
			color: #d4af37;
		}
		.kp-vault-title {
			font-family: 'Outfit', sans-serif;
			font-size: 0.98rem;
			font-weight: 700;
			color: #f8fafc;
			line-height: 1.32;
			margin: 0;
		}
		.kp-vault-issuer {
			font-size: 0.78rem;
			color: #cbd5e1;
			margin: 0;
		}
		.kp-vault-meta {
			font-size: 0.72rem;
			color: #94a3b8;
			margin: auto 0 0;
			padding-top: 8px;
			border-top: 1px solid rgba(255, 255, 255, 0.07);
		}
		.kp-vault-modal {
			position: fixed;
			inset: 0;
			z-index: 99999;
			background: rgba(4, 7, 13, 0.95);
			backdrop-filter: blur(16px);
			display: none;
			align-items: center;
			justify-content: center;
			padding: clamp(12px, 3vw, 28px);
		}
		.kp-vault-modal.is-open {
			display: flex;
		}
		.kp-vault-dialog {
			width: min(1020px, 100%);
			max-height: 92vh;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.48);
			border-radius: 18px;
			padding: 20px;
			overflow-y: auto;
			display: flex;
			flex-direction: column;
			gap: 14px;
		}
		.kp-vault-zoom-stage {
			background: #f6f2e9;
			border-radius: 12px;
			padding: 14px;
			max-height: 64vh;
			overflow: auto;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		.kp-vault-zoom-stage img {
			max-width: 100%;
			max-height: 60vh;
			object-fit: contain;
			transition: transform 0.25s ease;
		}
		.kp-vault-zoom-stage.is-zoomed img {
			max-height: none;
			width: 135%;
			max-width: none;
		}
	</style>
<?php endif; ?>

<section id="<?php echo esc_attr( $kp_section_id ); ?>" class="kp-vault-section" data-kp-vault="<?php echo esc_attr( $kp_vault_uid ); ?>">
	<div class="kp-vault-wrap">
		<div class="kp-vault-header">
			<div>
				<div class="kp-vault-kicker"><?php echo esc_html( $kp_kicker ); ?></div>
				<h2 class="kp-vault-h2"><?php echo esc_html( $kp_heading ); ?></h2>
				<p class="kp-vault-sub"><?php echo esc_html( $kp_subcopy ); ?></p>
			</div>
			<?php if ( 'reel' === $kp_mode ) : ?>
				<div class="kp-port-glide" aria-label="Credential Vault Navigation">
					<button type="button" class="kp-port-arrow" data-vault-prev aria-label="Scroll Certificates Left">&#8592;</button>
					<button type="button" class="kp-port-arrow" data-vault-next aria-label="Scroll Certificates Right">&#8594;</button>
				</div>
			<?php endif; ?>
		</div>

		<div class="kp-vault-filters" role="tablist" aria-label="Filter Verified Certificates">
			<button type="button" class="kp-vault-pill is-active" data-vault-filter="all">All Verified (<?php echo count( $kp_certs ); ?>)</button>
			<button type="button" class="kp-vault-pill" data-vault-filter="statutory">Statutory &amp; Utility</button>
			<button type="button" class="kp-vault-pill" data-vault-filter="bcbc-2024">BCBC 2024</button>
			<button type="button" class="kp-vault-pill" data-vault-filter="chba">CHBA Qualifications</button>
			<button type="button" class="kp-vault-pill" data-vault-filter="cpd-safety">CPD &amp; Safety</button>
		</div>

		<div class="kp-vault-track is-<?php echo esc_attr( $kp_mode ); ?>" data-vault-track>
			<?php foreach ( $kp_certs as $c_idx => $c_item ) : ?>
				<article
					class="kp-vault-card"
					tabindex="0"
					role="button"
					aria-label="<?php echo esc_attr( 'Inspect ' . $c_item['title'] ); ?>"
					data-vault-card="<?php echo esc_attr( (string) $c_idx ); ?>"
					data-vault-cat="<?php echo esc_attr( $c_item['category'] ); ?>"
				>
					<div class="kp-vault-mat">
						<img
							src="<?php echo esc_url( $c_item['image'] ); ?>"
							alt="<?php echo esc_attr( $c_item['title'] . ' — ' . $c_item['issuer'] ); ?>"
							loading="lazy"
							decoding="async"
						/>
					</div>
					<span class="kp-vault-cat"><?php echo esc_html( $c_item['cat_label'] ); ?></span>
					<h3 class="kp-vault-title"><?php echo esc_html( $c_item['title'] ); ?></h3>
					<p class="kp-vault-issuer"><?php echo esc_html( $c_item['issuer'] ); ?></p>
					<p class="kp-vault-meta"><?php echo esc_html( $c_item['meta'] ); ?></p>
				</article>
			<?php endforeach; ?>
		</div>
	</div>

	<div class="kp-vault-modal" data-vault-modal role="dialog" aria-modal="true" aria-label="Certificate High-Resolution Document Viewer">
		<div class="kp-vault-dialog">
			<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
				<div>
					<div class="kp-vault-cat" data-vmodal-cat></div>
					<h3 class="kp-vault-title" style="font-size:1.22rem;" data-vmodal-title></h3>
					<div class="kp-vault-issuer" data-vmodal-meta></div>
				</div>
				<div style="display:flex;gap:8px;flex-wrap:wrap;">
					<button type="button" class="kp-vault-pill" data-vmodal-alt style="display:none;">Switch Full Registry Sheet</button>
					<button type="button" class="kp-vault-pill" data-vmodal-zoom>Toggle 135% Zoom</button>
					<button type="button" class="kp-vault-pill" data-vmodal-prev>&larr; Prev</button>
					<button type="button" class="kp-vault-pill" data-vmodal-next>Next &rarr;</button>
					<button type="button" class="kp-vault-pill" data-vmodal-close>Close &times;</button>
				</div>
			</div>
			<div class="kp-vault-zoom-stage" data-vmodal-stage>
				<img src="" alt="" data-vmodal-img />
			</div>
		</div>
	</div>

	<script>
	(function() {
		var root = document.querySelector('[data-kp-vault="<?php echo esc_js( $kp_vault_uid ); ?>"]');
		if (!root) return;
		var certs = <?php echo wp_json_encode( $kp_certs ); ?>;
		var track = root.querySelector('[data-vault-track]');
		var cards = Array.prototype.slice.call(root.querySelectorAll('[data-vault-card]'));
		var pills = Array.prototype.slice.call(root.querySelectorAll('[data-vault-filter]'));
		var prevBtn = root.querySelector('[data-vault-prev]');
		var nextBtn = root.querySelector('[data-vault-next]');

		pills.forEach(function(pill) {
			pill.addEventListener('click', function() {
				var f = pill.getAttribute('data-vault-filter');
				pills.forEach(function(p) { p.classList.toggle('is-active', p === pill); });
				cards.forEach(function(c) {
					var show = (f === 'all' || c.getAttribute('data-vault-cat') === f);
					if (show) c.removeAttribute('hidden');
					else c.setAttribute('hidden', 'hidden');
				});
			});
		});

		if (prevBtn && track) prevBtn.addEventListener('click', function() { track.scrollBy({ left: -340, behavior: 'smooth' }); });
		if (nextBtn && track) nextBtn.addEventListener('click', function() { track.scrollBy({ left: 340, behavior: 'smooth' }); });

		var modal = root.querySelector('[data-vault-modal]');
		var stage = root.querySelector('[data-vmodal-stage]');
		var imgEl = root.querySelector('[data-vmodal-img]');
		var catEl = root.querySelector('[data-vmodal-cat]');
		var titleEl = root.querySelector('[data-vmodal-title]');
		var metaEl = root.querySelector('[data-vmodal-meta]');
		var altBtn = root.querySelector('[data-vmodal-alt]');
		var activeIdx = 0;
		var showingAlt = false;

		function showCert(idx) {
			activeIdx = (idx + certs.length) % certs.length;
			var c = certs[activeIdx];
			showingAlt = false;
			stage.classList.remove('is-zoomed');
			imgEl.src = c.image;
			imgEl.alt = c.title;
			catEl.textContent = c.cat_label + ' · Document ' + (activeIdx + 1) + ' of ' + certs.length;
			titleEl.textContent = c.title;
			metaEl.textContent = c.issuer + ' — ' + c.meta;
			altBtn.style.display = c.alt_sheet ? 'inline-block' : 'none';
			modal.classList.add('is-open');
			document.body.style.overflow = 'hidden';
		}

		function closeVault() {
			modal.classList.remove('is-open');
			document.body.style.overflow = '';
		}

		cards.forEach(function(card) {
			var idx = parseInt(card.getAttribute('data-vault-card'), 10);
			card.addEventListener('click', function() { showCert(idx); });
			card.addEventListener('keydown', function(e) {
				if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showCert(idx); }
			});
		});

		altBtn.addEventListener('click', function() {
			var c = certs[activeIdx];
			if (!c || !c.alt_sheet) return;
			showingAlt = !showingAlt;
			imgEl.src = showingAlt ? c.alt_sheet : c.image;
		});
		root.querySelector('[data-vmodal-zoom]').addEventListener('click', function() { stage.classList.toggle('is-zoomed'); });
		root.querySelector('[data-vmodal-prev]').addEventListener('click', function() { showCert(activeIdx - 1); });
		root.querySelector('[data-vmodal-next]').addEventListener('click', function() { showCert(activeIdx + 1); });
		root.querySelector('[data-vmodal-close]').addEventListener('click', closeVault);
		modal.addEventListener('click', function(e) { if (e.target === modal) closeVault(); });
		document.addEventListener('keydown', function(e) {
			if (!modal.classList.contains('is-open')) return;
			if (e.key === 'Escape') closeVault();
			if (e.key === 'ArrowLeft') showCert(activeIdx - 1);
			if (e.key === 'ArrowRight') showCert(activeIdx + 1);
		});
	})();
	</script>
</section>
