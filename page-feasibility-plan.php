<?php
/**
 * Template Name: Feasibility & Cost Plan
 *
 * Pre-construction 6-step technical constructability audit & Open-Book CCDC 5B pro-forma desk.
 * Uses clean @KeystonePossibilitiesLtd briefing ERD0DiVkgYg (or valid kp_video_id_feasibility option),
 * split 2-column above-the-fold 48-Hr Lot & Cost intake, and interactive 9-corridor Bill 44 calculator.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_opt_vid = trim( (string) get_option( 'kp_video_id_feasibility', '' ) );
// Reject legacy wrong-channel option values; default to clean @KeystonePossibilitiesLtd ERD0DiVkgYg.
if ( ! preg_match( '/^[A-Za-z0-9_-]{11}$/', $kp_opt_vid ) || 0 === strpos( $kp_opt_vid, 'y67f-' ) ) {
	$kp_opt_vid = 'ERD0DiVkgYg';
}

$kp_pre_corridor = isset( $_GET['corridor'] ) ? sanitize_title( wp_unslash( $_GET['corridor'] ) ) : 'west-vancouver';

$kp_audit_steps = array(
	array(
		'num'   => 'STEP 01',
		'title' => 'LTSA Title, Statutory Rights-of-Way & Covenant Audit',
		'desc'  => 'Line-by-line review of Land Title & Survey Authority charges, Section 219 geotechnical covenants, restrictive view/height easements, and heritage or tree retention encumbrances prior to design spend.',
	),
	array(
		'num'   => 'STEP 02',
		'title' => 'Geotechnical Bedrock, Shoring & Flood Construction Level (FCL)',
		'desc'  => 'Profiling granodiorite rock-blasting or micro-splitting volumes, steep-slope micropile/tie-back exposure, riparian creek setbacks (e.g., DWV Bylaw 4364), and Sea-to-Sky FCL structural elevation gates.',
	),
	array(
		'num'   => 'STEP 03',
		'title' => 'BC Hydro ES54 400A–800A & Private PMT Vault Audit',
		'desc'  => 'Evaluating primary feeder proximity, DB2 PVC underground duct routing (>=900mm boulevard / >=1050mm road cover), and CEC Rule 26-242 3.0m Pad-Mounted Transformer hot-stick clearances.',
	),
	array(
		'num'   => 'STEP 04',
		'title' => 'Bill 44 SSMUH / Vancouver R1-1 Density & Envelope Modeling',
		'desc'  => 'Comparing single-family custom estate yield against 3–6 unit Bill 44 SSMUH or 1.0 FSR R1-1 multiplex massing, including 2" domestic water main upgrades, NFPA 13D/13R sprinklers, and STC 55+ party walls.',
	),
	array(
		'num'   => 'STEP 05',
		'title' => '13-Division Open-Book CCDC 5B Pro-Forma & Trade Calibration',
		'desc'  => 'Transparent division-by-division construction budget calibrated against live Sea-to-Sky and Metro Vancouver 3-bid trade tenders, Dick’s Lumber #52603 supply pricing, and 10% Builders Lien holdback schedules.',
	),
	array(
		'num'   => 'STEP 06',
		'title' => 'Critical-Path Gantt & Municipal Building Permit Roadmap',
		'desc'  => 'Sequencing BCLS topographic pinning, Letters of Assurance (Schedules A, B, C-A, C-B), HOT2000 Step Code 4/5 & EL-4 energy modeling, and municipal DP/BP intake windows.',
	),
);

$kp_feasibility_faqs = array(
	array(
		'q' => 'Can we submit an MLS listing or PID before removing subjects on a BC lot?',
		'a' => 'Yes. Landowners, buyers, and BC Realtors regularly submit active MLS listings or PIDs prior to subject removal. Wayne Stevenson reviews slope/rock risk, ES54 underground power routing, and realistic $/SF CCDC 5B construction ranges within 48 business hours.',
	),
	array(
		'q' => 'How is feasibility planning structured when transitioning into an active build?',
		'a' => 'Pre-construction feasibility and open-book budgeting transition seamlessly into our CCDC 5B Construction Management agreement, where 100% of sub-trade tenders, consultant schedules, and lumber takeoffs are managed transparently inside the Keystone Client Portal.',
	),
	array(
		'q' => 'Do you coordinate directly with our existing AIBC Architect or Structural Engineer?',
		'a' => 'Absolutely. We routinely join schematic design alongside Measured Architecture, Fast + Epp, Glotman Simpson, Thurber Engineering, Lewkowich Engineering, or your retained design studio to value-engineer cantilevers, glazing, and mechanicals before permit submission.',
	),
);
?>

<main id="primary" class="kp-v3-page">
	<?php
	// Ensure shared v3 shell CSS is printed before the hero by pre-loading lead-intake-form in embed mode inside the split hero.
	?>
	<section class="kp-v3-hero">
		<div class="kp-v3-container">
			<div class="kp-v3-split" style="align-items:start;">
				<div>
					<div class="kp-v3-kicker">PRE-CONSTRUCTION CONSTRUCTABILITY &amp; COST DESK &bull; BC #52603</div>
					<h1 class="kp-v3-h1">48-Hour Lot Constructability &amp; Open-Book CCDC 5B Cost Planning.</h1>
					<p class="kp-v3-lead">
						Eliminate six-figure rock, shoring, and BC Hydro ES54 transformer surprises before you remove subjects or freeze architectural drawings. Principal Superintendent Wayne Stevenson audits your parcel across every geotechnical, zoning, and structural gate.
					</p>

					<?php
					get_template_part(
						'template-parts/watch-player',
						null,
						array(
							'compact'   => true,
							'video_id'  => $kp_opt_vid,
							'pill'      => 'Feasibility & Bedrock Briefing',
							'title'     => 'Sea-to-Sky & Metro Vancouver Pre-Construction Bedrock, Step Code & ES54 Audit',
							'duration'  => '08:15',
							'watch_url' => home_url( '/videos/sea-to-sky-luxury-compounds-bc-building-code/' ),
						)
					);
					?>
				</div>

				<div>
					<?php
					get_template_part(
						'template-parts/lead-intake-form',
						null,
						array(
							'embed_only'       => true,
							'default_corridor' => $kp_pre_corridor,
						)
					);
					?>
				</div>
			</div>
		</div>
	</section>

	<section class="kp-v3-section">
		<div class="kp-v3-container">
			<div class="kp-v3-kicker">6-STEP TECHNICAL RISK &amp; PRO-FORMA PROTOCOL</div>
			<h2 class="kp-v3-h2">What Wayne Stevenson Audits Before Shovel Hits Bedrock.</h2>
			<p class="kp-v3-lead" style="max-width:780px;">
				Every feasibility dossier is engineered from the perspective of an active site superintendent—connecting LTSA legal encumbrances directly to excavator access, crane picks, ES54 civil trenching, and verified 3-bid sub-trade pricing.
			</p>

			<div class="kp-v3-grid-3" style="margin-top:26px;">
				<?php foreach ( $kp_audit_steps as $step ) : ?>
					<article class="kp-v3-card">
						<span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;"><?php echo esc_html( $step['num'] ); ?></span>
						<h3 style="font-family:'Outfit',sans-serif;font-size:1.14rem;font-weight:700;color:#f8fafc;margin:0;line-height:1.3;"><?php echo esc_html( $step['title'] ); ?></h3>
						<p style="font-size:0.88rem;line-height:1.6;color:#cbd5e1;margin:0;"><?php echo esc_html( $step['desc'] ); ?></p>
					</article>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<?php get_template_part( 'template-parts/bill44-calculator', null, array( 'default_corridor' => $kp_pre_corridor ) ); ?>

	<?php
	get_template_part(
		'template-parts/faq-accordion',
		null,
		array(
			'heading' => 'Pre-Construction Feasibility & Open-Book Budgeting FAQs.',
			'faqs'    => $kp_feasibility_faqs,
		)
	);
	?>
</main>

<?php
get_footer();
