<?php
/**
 * Template Part: Accessible Quiet-Luxury FAQ Accordion (<details>/<summary>)
 *
 * Synced 1:1 with FAQPage JSON-LD schema.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_default_faqs = array(
	array(
		'q' => 'How does Keystone Possibilities’ Open-Book CCDC 5B contract protect owners compared to a traditional general contractor?',
		'a' => 'Under a CCDC 5B Construction Management structure, every sub-trade scope is tendered across 3 vetted BC specialists and shared 100% open-book inside your 24/7 Client Portal alongside raw supplier invoices, Dick’s Lumber #52603 trade discounts, and statutory 10% Builders Lien Act holdback tracking—eliminating opaque 20%–26% sub-markup cascades.',
	),
	array(
		'q' => 'Why does BC Hydro ES54 Registered Civil Contractor status matter on custom estates and Bill 44 multiplexes?',
		'a' => 'Upgrading coastal estates or 4–6 unit Bill 44 multiplexes to 400A–800A underground service or private Pad-Mounted Transformers (PMTs) requires strict adherence to BC Hydro ES54 DB2 PVC duct depths (>=900mm boulevard / >=1050mm roadway) and CEC Rule 26-242 3.0m hot-stick clearances. Self-performing ES54 civil trenching prevents multi-month energizing bottlenecks.',
	),
	array(
		'q' => 'What is included in a 48-Hour Pre-Offer Lot & MLS Constructability Review?',
		'a' => 'Principal Superintendent Wayne Stevenson personally audits LTSA title covenants, municipal creek/FCL/slope development permit areas, bedrock shoring or micropile risk, BC Hydro ES54 transformer capacity, and Class-C $/SF pro-forma ranges across 9 BC corridors so landowners, Realtors, and architects know true build costs before subject removal.',
	),
	array(
		'q' => 'How does the 0.50% BC Realtor Managing-Brokerage Referral comply with BCFSA Rule 5-11?',
		'a' => 'All 0.50% CCDC 5B build referrals are remitted strictly to the licensed Managing Brokerage under RESA s. 6–7 (never to an individual or unlicensed party) and paired with a written BCFSA Rule 5-11 Disclosure of Remuneration acknowledged by the client prior to construction contract execution.',
	),
	array(
		'q' => 'Who supervises active excavation, structural formwork, and building envelope hold-points on site?',
		'a' => 'Wayne Stevenson—Principal of Keystone Possibilities Ltd. (BC Housing Licensed Residential Builder #52603, mandatory 2-5-10 Year New Home Warranty) with 20+ years of heavy-civil infrastructure superintendence including Peter Kiewit & Sons—personally directs critical-path geotechnical, structural Schedule B, Step Code 5 air-barrier, and ES54 civil milestones.',
	),
);

$kp_faqs       = ! empty( $args['faqs'] ) && is_array( $args['faqs'] ) ? $args['faqs'] : $kp_default_faqs;
$kp_section_id = isset( $args['section_id'] ) ? sanitize_html_class( (string) $args['section_id'] ) : 'faq';
$kp_kicker     = isset( $args['kicker'] ) ? (string) $args['kicker'] : 'EXECUTIVE TECHNICAL FAQ · SCHEMA-SYNCED BRIEFING';
$kp_heading    = isset( $args['heading'] ) ? (string) $args['heading'] : 'Direct Engineering, Fiduciary & Regulatory Answers.';

if ( empty( $GLOBALS['kp_v3_faq_css'] ) ) :
	$GLOBALS['kp_v3_faq_css'] = true;
	?>
	<style id="kp-v3-faq-styles">
		.kp-faq-section {
			padding: clamp(52px, 6.5vw, 84px) 0;
			background: #04070d;
			color: #f8fafc;
			border-top: 1px solid rgba(212, 175, 55, 0.14);
		}
		.kp-faq-wrap {
			width: min(1040px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-faq-kicker {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: #d4af37;
			margin-bottom: 8px;
		}
		.kp-faq-h2 {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.5rem, 2.8vw, 2.15rem);
			font-weight: 700;
			color: #f8fafc;
			margin: 0 0 24px;
			line-height: 1.18;
		}
		.kp-faq-list {
			display: flex;
			flex-direction: column;
			gap: 12px;
		}
		.kp-faq-item {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.24);
			border-radius: 16px;
			overflow: hidden;
			transition: border-color 0.2s ease;
		}
		.kp-faq-item[open] {
			border-color: rgba(212, 175, 55, 0.58);
		}
		.kp-faq-item summary {
			list-style: none;
			cursor: pointer;
			padding: 18px 22px;
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 14px;
			font-family: 'Outfit', sans-serif;
			font-size: 1.02rem;
			font-weight: 700;
			color: #f8fafc;
			line-height: 1.35;
		}
		.kp-faq-item summary::-webkit-details-marker {
			display: none;
		}
		.kp-faq-icon {
			width: 28px;
			height: 28px;
			border-radius: 50%;
			border: 1px solid rgba(212, 175, 55, 0.42);
			color: #d4af37;
			display: inline-flex;
			align-items: center;
			justify-content: center;
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.95rem;
			flex-shrink: 0;
			transition: transform 0.2s ease;
		}
		.kp-faq-item[open] .kp-faq-icon {
			transform: rotate(45deg);
		}
		.kp-faq-ans {
			padding: 0 22px 20px;
			font-size: 0.92rem;
			line-height: 1.66;
			color: #cbd5e1;
			border-top: 1px solid rgba(255, 255, 255, 0.06);
			padding-top: 14px;
		}
	</style>
<?php endif; ?>

<section id="<?php echo esc_attr( $kp_section_id ); ?>" class="kp-faq-section">
	<div class="kp-faq-wrap">
		<div class="kp-faq-kicker"><?php echo esc_html( $kp_kicker ); ?></div>
		<h2 class="kp-faq-h2"><?php echo esc_html( $kp_heading ); ?></h2>
		<div class="kp-faq-list">
			<?php foreach ( $kp_faqs as $f_idx => $faq ) :
				$question = isset( $faq['q'] ) ? $faq['q'] : ( $faq['question'] ?? '' );
				$answer   = isset( $faq['a'] ) ? $faq['a'] : ( $faq['answer'] ?? '' );
				if ( '' === $question || '' === $answer ) {
					continue;
				}
				?>
				<details class="kp-faq-item"<?php echo 0 === $f_idx ? ' open' : ''; ?>>
					<summary>
						<span><?php echo esc_html( $question ); ?></span>
						<span class="kp-faq-icon" aria-hidden="true">+</span>
					</summary>
					<div class="kp-faq-ans">
						<?php echo wp_kses_post( wpautop( $answer ) ); ?>
					</div>
				</details>
			<?php endforeach; ?>
		</div>
	</div>
</section>
