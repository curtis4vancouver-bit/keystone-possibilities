<?php
/**
 * Template Name: Watch Briefing Theater
 * Template Post Type: page
 *
 * Dedicated Google Watch Page template (/videos/[slug]/):
 * - Above-the-fold (<580px) 4K @KeystonePossibilitiesLtd youtube-nocookie.com theater
 * - Interactive Clip chapter-seek bar
 * - AI-Overview Direct Engineering Answer Box
 * - Sticky Parcel Constructability Sidebar + Companion Full Technical Blog Post link
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_post_id   = get_queried_object_id();
$kp_page_slug = sanitize_title( (string) get_post_field( 'post_name', $kp_post_id ) );
$kp_norm_slug = preg_replace( '/^watch-/', '', $kp_page_slug );
$kp_norm_slug = preg_replace( '/-2$/', '', $kp_norm_slug );

$kp_watch_registry = array(
	'west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide' => array(
		'yt_id'     => 'kLsNyKvQswg',
		'duration'  => '08:42',
		'post_slug' => 'west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide',
		'answer'    => 'Achieving BC Energy Step Code 5 / Zero Carbon EL-4 on cantilevered West Vancouver and Whistler granite slopes requires structural thermal breaks (e.g., Schöck Isokorb or high-density Armatherm pads) at every projecting steel beam, paired with >=60mm continuous exterior Rockwool insulation (<1.0 ACH50 blower-door verified), socketed granite micropiles, and self-performed BC Hydro ES54 underground 400A–800A duct banks.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Granite Micropile & Slope Hold-Points' ),
			array( 'sec' => 118, 'label' => '01:58 · Thermal-Broken Steel Cantilevers' ),
			array( 'sec' => 264, 'label' => '04:24 · Step Code 5 (<1.0 ACH50) Envelope' ),
			array( 'sec' => 395, 'label' => '06:35 · BC Hydro ES54 Civil Integration' ),
		),
	),
	'why-4-storey-multiplexes-fail-lateral-shear' => array(
		'yt_id'     => 'JwtaaZlrFeE',
		'duration'  => '07:19',
		'post_slug' => 'why-4-storey-multiplexes-fail-lateral-shear',
		'answer'    => 'Four-storey Bill 44 SSMUH and Vancouver R1-1 multiplexes routinely fail BCBC 2024 Part 4 lateral shear review when ground-floor street frontages prioritize wide glazing and parking portals without engineered steel moment frames or Simpson Strong-Tie ATS continuous multi-storey tie-down rods anchored into thickened seismic grade beams.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Ground-Floor Glazing Drift Failure' ),
			array( 'sec' => 105, 'label' => '01:45 · Simpson ATS Continuous Rod Tie-Downs' ),
			array( 'sec' => 240, 'label' => '04:00 · STC 55+ Fire & Acoustic Party Walls' ),
			array( 'sec' => 350, 'label' => '05:50 · Pre-Offer Structural Grid Check' ),
		),
	),
	'estate-microgrids-bc' => array(
		'yt_id'     => 'HBy6NQQS3ks',
		'duration'  => '09:14',
		'post_slug' => 'estate-microgrids-bc',
		'answer'    => 'Modern coastal estates and multi-unit compounds combining air-to-water heat pumps, hydronic driveway snow-melt, and dual EV chargers exceed standard 200A/400A capacity—requiring a 600A–800A underground service entrance, BC Hydro ES54 DB2 PVC primary duct banks (>=900mm boulevard / >=1050mm road cover), and a private Pad-Mounted Transformer (PMT) vault with 3.0m hot-stick clearance under CEC Rule 26-242.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · 400A vs 800A Electrification Loads' ),
			array( 'sec' => 132, 'label' => '02:12 · CEC Rule 26-242 3.0m PMT Clearance' ),
			array( 'sec' => 290, 'label' => '04:50 · ES54 DB2 PVC Trench & Mandrel QA' ),
			array( 'sec' => 430, 'label' => '07:10 · Battery & Generator Microgrid Switchgear' ),
		),
	),
	'sea-to-sky-luxury-compounds-bc-building-code' => array(
		'yt_id'     => 'ERD0DiVkgYg',
		'duration'  => '08:15',
		'post_slug' => 'sea-to-sky-luxury-compounds-bc-building-code',
		'answer'    => 'Building multi-structure Sea-to-Sky compounds across Squamish, Whistler, and Pemberton requires synchronizing geodetic Flood Construction Levels (FCL), high-altitude ground snow loads (3.4 kPa in Squamish up to 8.1 kPa in Whistler), RMOW FireSmart Class A non-combustible exteriors, and long-run BC Hydro ES54 underground primary feeders under one Open-Book CCDC 5B critical path.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Sea-to-Sky FCL & Bedrock Profiling' ),
			array( 'sec' => 130, 'label' => '02:10 · 3.4 kPa to 8.1 kPa Snow-Load Framing' ),
			array( 'sec' => 270, 'label' => '04:30 · Long-Run ES54 Civil & FireSmart DPAs' ),
		),
	),
	'architectural-concrete-bc' => array(
		'yt_id'     => 'qs7xlawF32k',
		'duration'  => '08:06',
		'post_slug' => 'architectural-concrete-bc',
		'answer'    => 'Museum-grade architectural board-formed concrete and cantilevered floating stairs require engineered Doka/Peri high-pressure formwork, symmetrical cone-tie grids, low-slump superplasticized 35 MPa CSA A23.1 mixes consolidated via internal pencil vibrators, and embedded steel stringer plates welded to seismic shear cores prior to Schedule B pre-pour sign-off.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Doka/Peri Form-Tie & Reveal Geometry' ),
			array( 'sec' => 140, 'label' => '02:20 · 35 MPa Mix Consolidation & Mockups' ),
			array( 'sec' => 285, 'label' => '04:45 · Cantilevered Stair Steel Embeds' ),
		),
	),
	'net-zero-building-envelopes' => array(
		'yt_id'     => 'sLXAtWGjeiA',
		'duration'  => '08:34',
		'post_slug' => 'net-zero-building-envelopes',
		'answer'    => 'BCBC 2024 Step Code 5 / Net-Zero Ready envelopes rely on a continuous, blower-door-verified (<0.6 to 1.0 ACH50) vapour-permeable air barrier taped across all slab-to-wall and roof-to-wall transitions, outboard 60mm–100mm rigid mineral-wool insulation, thermally broken triple-glazed fenestration, and 19mm ventilated rainscreen strapping.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Mid-Construction <=1.0 ACH50 Gate' ),
			array( 'sec' => 145, 'label' => '02:25 · Outboard Rockwool & Rainscreen Cavity' ),
			array( 'sec' => 295, 'label' => '04:55 · Triple-Glazed Sill Pan & Liquid Flashing' ),
		),
	),
	'net-zero-envelopes-bc' => array(
		'yt_id'     => 'sLXAtWGjeiA',
		'duration'  => '08:34',
		'post_slug' => 'net-zero-building-envelopes',
		'answer'    => 'BCBC 2024 Step Code 5 / Net-Zero Ready envelopes rely on a continuous, blower-door-verified (<0.6 to 1.0 ACH50) air barrier, outboard rigid mineral-wool insulation, thermally broken triple-glazed windows, and ventilated BCBC 9.27 rainscreen cavities.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Step Code 5 Air-Tightness Detailing' ),
			array( 'sec' => 160, 'label' => '02:40 · Exterior Continuous Mineral Wool' ),
		),
	),
	'inverted-roof-terraces-bc' => array(
		'yt_id'     => 'W7eIvbv23Ew',
		'duration'  => '07:48',
		'post_slug' => 'inverted-roof-terraces-bc',
		'answer'    => 'Leak-free coastal inverted roof terraces and Whistler 8.1 kPa alpine cold roofs require 2-ply SBS torch-on or hot-rubberized monolithic waterproofing sloped >=2% to clamped bi-level drains, topped with extruded polystyrene (XPS) drainage-mat insulation and pedestal pavers—or decoupled ventilated cold-roof rafters in deep snow zones.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Inverted Protected-Membrane Assembly' ),
			array( 'sec' => 135, 'label' => '02:15 · Bi-Level Drains & Door Threshold Pans' ),
			array( 'sec' => 275, 'label' => '04:35 · Alpine Cold-Roof Ice-Dam Prevention' ),
		),
	),
	'inverted-roof-terraces-alpine-cold-roofs-bc' => array(
		'yt_id'     => 'W7eIvbv23Ew',
		'duration'  => '07:48',
		'post_slug' => 'inverted-roof-terraces-bc',
		'answer'    => 'Inverted protected-membrane roof terraces and alpine cold roofs prevent thermal shock and ice damming across coastal and mountain BC climates.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Inverted Terrace Waterproofing' ),
			array( 'sec' => 180, 'label' => '03:00 · Alpine Cold-Roof Plenum Design' ),
		),
	),
	'hydronic-radiant-floor-erv-engineering' => array(
		'yt_id'     => 'v7r2uwF4eWU',
		'duration'  => '08:11',
		'post_slug' => 'hydronic-radiant-floor-erv-engineering',
		'answer'    => 'High-performance BCBC 2024 mechanical rooms pair oxygen-barrier PEX-a hydronic radiant loops (pressure-tested to 100 PSI prior to slab/gypcrete pour) driven by cold-climate air-to-water heat pumps with dedicated acoustically attenuated ERV/HRV balanced ventilation—commission-tested to TECA standards without cross-suite recirculation.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Manifold Zoning & 100 PSI Pre-Pour Test' ),
			array( 'sec' => 150, 'label' => '02:30 · Air-to-Water Heat Pump Buffer Sizing' ),
			array( 'sec' => 290, 'label' => '04:50 · Dedicated ERV Balancing & Acoustics' ),
		),
	),
	'bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide' => array(
		'yt_id'     => 'nPXnGzAEY6k',
		'duration'  => '08:29',
		'post_slug' => 'bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide',
		'answer'    => 'Under BCBC 2024 Sections 9.13 and 9.14, coastal hillside basements require dual-layer elastomeric liquid/sheet waterproofing terminated above grade, high-compressive dimple drainage mat, dual rigid PVC weeping and storm lines bedded in washed clear crush, and a sealed 15-mil sub-slab vapour barrier over gas-permeable radon rock vented via a dedicated radon stack.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Hydrostatic Perched-Water Failure Modes' ),
			array( 'sec' => 140, 'label' => '02:20 · Dual-Membrane & Rigid Weeping Tile' ),
			array( 'sec' => 285, 'label' => '04:45 · BCBC 2024 Sub-Slab Radon Stack QA' ),
		),
	),
	'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide' => array(
		'yt_id'     => 'SIHMOJ5AOyw',
		'duration'  => '07:55',
		'post_slug' => 'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide',
		'answer'    => 'Delivering zero-step adaptable suite entries on tight Vancouver R1-1 multiplex lots without water ingress requires recessed concrete slab pockets, stainless trench drains tied to storm retention, liquid-applied upturned sill membranes, and compact micropile/shotcrete perimeter shoring along zero-lot-line excavations.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · Adaptable Zero-Step Sill Trench Drains' ),
			array( 'sec' => 150, 'label' => '02:30 · Tight-Access Micropile & Shotcrete Shoring' ),
		),
	),
	'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide' => array(
		'yt_id'     => 'eV_Oo5ekaWc',
		'duration'  => '08:22',
		'post_slug' => 'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide',
		'answer'    => 'Passing Vancouver R1-1 and BCBC 2024 multiplex occupancy demands decoupled double-stud or resilient-channel 1-hr/2-hr fire separations achieving STC 55+ acoustic isolation (with fire/acoustic putty pads on all outlet boxes), paired with a 2-inch municipal domestic water service upgrade feeding NFPA 13D/13R fire sprinkler risers.',
		'chapters'  => array(
			array( 'sec' => 0,   'label' => '00:00 · 2-Inch Municipal Water Main & NFPA 13R' ),
			array( 'sec' => 155, 'label' => '02:35 · STC 55+ Decoupled Party-Wall Framing' ),
			array( 'sec' => 300, 'label' => '05:00 · Firestopping & Putty-Pad Inspection' ),
		),
	),
);

$kp_watch_aliases = array(
	'west-vancouver-whistler-step-code-5-cantilever-seismic'   => 'west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide',
	'bcbc-2024-basement-waterproofing-hydrostatic-radon'       => 'bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide',
	'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile'   => 'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide',
	'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main'   => 'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide',
	'turnkey-feasibility-plan-briefing'                        => 'sea-to-sky-luxury-compounds-bc-building-code',
	'bc-bill-44-multiplex-engineering-briefing'                => 'why-4-storey-multiplexes-fail-lateral-shear',
	'bc-step-code-5-custom-home-briefing'                      => 'west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide',
);
$kp_lookup_slug = isset( $kp_watch_aliases[ $kp_norm_slug ] ) ? $kp_watch_aliases[ $kp_norm_slug ] : $kp_norm_slug;

$kp_entry = isset( $kp_watch_registry[ $kp_lookup_slug ] )
	? $kp_watch_registry[ $kp_lookup_slug ]
	: $kp_watch_registry['west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide'];

$kp_meta_yt = trim( (string) get_post_meta( $kp_post_id, '_kp_youtube_id', true ) );
if ( preg_match( '/^[A-Za-z0-9_-]{11}$/', $kp_meta_yt ) && 0 !== strpos( $kp_meta_yt, 'y67f-' ) ) {
	$kp_entry['yt_id'] = $kp_meta_yt;
}

$kp_clean_title = preg_replace( '/^Watch:\s*/i', '', get_the_title( $kp_post_id ) );
?>

<main id="primary" class="kp-v3-page">
	<style id="kp-v3-watch-theater-page-styles">
		.kp-wt-above-fold {
			padding: clamp(16px, 2.6vw, 32px) 0 clamp(36px, 5vw, 60px);
			background: #04070d;
		}
		.kp-wt-grid {
			width: min(1340px, calc(100% - 32px));
			margin: 0 auto;
			display: grid;
			grid-template-columns: 1.55fr 0.72fr;
			gap: clamp(20px, 3vw, 34px);
			align-items: start;
		}
		@media (max-width: 1020px) {
			.kp-wt-grid {
				grid-template-columns: 1fr;
			}
		}
		.kp-wt-sidebar {
			position: sticky;
			top: 88px;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.38);
			border-radius: 20px;
			padding: 22px;
			display: flex;
			flex-direction: column;
			gap: 14px;
		}
		.kp-wt-answer-box {
			margin-top: 20px;
			background: linear-gradient(135deg, rgba(10, 16, 29, 0.96), rgba(15, 23, 42, 0.9));
			border: 1px solid rgba(212, 175, 55, 0.42);
			border-left: 4px solid #d4af37;
			border-radius: 16px;
			padding: 20px 22px;
		}
		.kp-wt-prose {
			margin-top: 24px;
			font-size: 0.96rem;
			line-height: 1.72;
			color: #cbd5e1;
		}
		.kp-wt-prose h2,
		.kp-wt-prose h3 {
			font-family: 'Outfit', sans-serif;
			color: #f8fafc;
			margin-top: 1.6em;
		}
		.kp-wt-prose a {
			color: #d4af37;
		}
		.kp-wt-prose iframe {
			display: none; /* Prevent duplicate raw post_content iframe below primary theater */
		}
	</style>

	<section class="kp-wt-above-fold">
		<div class="kp-wt-grid">
			<div>
				<nav aria-label="Breadcrumb" style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#94a3b8;margin-bottom:8px;">
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>" style="color:#d4af37;text-decoration:none;">Home</a>
					<span> / </span>
					<a href="<?php echo esc_url( home_url( '/videos/' ) ); ?>" style="color:#d4af37;text-decoration:none;">Videos</a>
					<span> / </span>
					<span style="color:#cbd5e1;">4K Briefing</span>
				</nav>

				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.38rem,2.5vw,2.05rem);font-weight:800;line-height:1.16;color:#f8fafc;margin:0 0 12px;">
					<?php echo esc_html( $kp_clean_title ); ?>
				</h1>

				<!-- Primary Video Theater strictly <580px from top of viewport -->
				<?php
				get_template_part(
					'template-parts/watch-player',
					null,
					array(
						'compact'   => true,
						'video_id'  => $kp_entry['yt_id'],
						'title'     => $kp_clean_title,
						'duration'  => $kp_entry['duration'],
						'watch_url' => home_url( '/' . $kp_entry['post_slug'] . '/' ),
						'chapters'  => $kp_entry['chapters'],
					)
				);
				?>

				<!-- AI-Overview Direct Engineering Answer Box -->
				<div class="kp-wt-answer-box">
					<div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:700;color:#d4af37;letter-spacing:0.06em;margin-bottom:6px;">
						DIRECT SUPERINTENDENT ENGINEERING SPECIFICATION &bull; WAYNE STEVENSON (#52603)
					</div>
					<p style="margin:0;font-size:0.94rem;line-height:1.65;color:#f8fafc;">
						<?php echo esc_html( $kp_entry['answer'] ); ?>
					</p>
					<div style="margin-top:12px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.08);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;">
						<span style="font-size:0.78rem;color:#94a3b8;">BC Housing Licensed Builder #52603 &bull; BC Hydro ES54 Civil</span>
						<a href="<?php echo esc_url( home_url( '/' . $kp_entry['post_slug'] . '/' ) ); ?>" style="font-size:0.82rem;font-weight:700;color:#d4af37;text-decoration:none;">
							Read Companion Technical Blueprint &rarr;
						</a>
					</div>
				</div>

				<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
					<div class="kp-wt-prose">
						<?php the_content(); ?>
					</div>
				<?php endwhile; endif; ?>
			</div>

			<aside class="kp-wt-sidebar" aria-label="48-Hour Parcel Constructability Desk">
				<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;color:#d4af37;">APPLY THIS SPEC TO YOUR LOT</span>
				<h2 style="font-family:'Outfit',sans-serif;font-size:1.22rem;font-weight:700;color:#f8fafc;margin:0;line-height:1.28;">
					48-Hour Parcel &amp; MLS&reg; Constructability Audit
				</h2>
				<p style="font-size:0.85rem;line-height:1.58;color:#cbd5e1;margin:0;">
					Have Wayne Stevenson (#52603) check bedrock shoring, Step Code 5 assemblies, BC Hydro ES54 PMT clearances, and Open-Book CCDC 5B $/SF costs on your lot.
				</p>
				<a href="#kp-lead-intake-form" style="display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:10px 18px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.86rem;text-decoration:none;">
					Request 48-Hr Review &darr;
				</a>
				<a href="<?php echo esc_url( home_url( '/' . $kp_entry['post_slug'] . '/' ) ); ?>" style="display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 16px;border-radius:999px;border:1px solid rgba(212,175,55,0.38);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.82rem;text-decoration:none;">
					Full Written Code Blueprint &rarr;
				</a>
				<a href="<?php echo esc_url( home_url( '/videos/' ) ); ?>" style="font-size:0.78rem;color:#38bdf8;text-decoration:none;text-align:center;font-weight:600;">
					&larr; Back to All 11 Watch Briefings
				</a>
			</aside>
		</div>
	</section>

	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'west-vancouver' ) ); ?>
</main>

<?php
get_footer();
