<?php
/**
 * Template Part: Signature Portfolio Cinema Reel & Multi-Photo Gallery Lightbox
 *
 * Displays all 9 real Signature Residences (42 live gallery URLs) + 2 real 2023 civil field items.
 * Supports $args['mode'] = 'reel' | 'grid' and optional $args['default_filter'].
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_mode           = isset( $args['mode'] ) && in_array( $args['mode'], array( 'reel', 'grid' ), true ) ? $args['mode'] : 'reel';
$kp_default_filter = isset( $args['default_filter'] ) ? sanitize_title( (string) $args['default_filter'] ) : 'all';
$kp_section_id     = isset( $args['section_id'] ) ? sanitize_html_class( (string) $args['section_id'] ) : 'portfolio';
$kp_kicker         = isset( $args['kicker'] ) ? (string) $args['kicker'] : 'VERIFIED BUILT PORTFOLIO · 9 SIGNATURE RESIDENCES (42 PHOTOS) + ES54 CIVIL FLEET';
$kp_heading        = isset( $args['heading'] ) ? (string) $args['heading'] : 'Constructed Across Coastal Granite, Alpine Snow Zones & Urban Infill.';
$kp_subcopy        = isset( $args['subcopy'] ) ? (string) $args['subcopy'] : 'Inspect real completed residences and active heavy-civil excavations supervised under BC Housing Licence #52603. Click any project card to open the full multi-photograph architectural & structural inspection gallery.';

// Ground-truth verified manifest of all 9 Signature Residences (42 live gallery URLs) + 2 real 2023 Civil Field items.
$kp_fallback_projects = array(
	array(
		'id'              => 'ballantree-west-van',
		'title'           => 'Ballantree Residence — British Properties',
		'location'        => '5610 Ballantree Road, British Properties, West Vancouver, BC',
		'corridor'        => 'west-vancouver',
		'corridor_label'  => 'West Vancouver',
		'calc_corridor'   => 'west-vancouver',
		'description'     => 'Navigated District of West Vancouver Watercourse Protection Bylaw No. 4364 (15m top-of-bank setback) and steep slope geotechnical stabilization. Deep concrete micropiles socketed into granite bedrock, post-tensioned rock anchors, and cantilevered structural steel frames.',
		'compliance_tags' => array( 'Geotechnical Micropiles', 'Granite Bedrock Anchors', 'Bylaw 4364 15m Setback' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.57.48-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.58.07-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.58.16-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.29-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.23-pm.png',
		),
	),
	array(
		'id'              => 'sunridge-whistler',
		'title'           => 'Sunridge Residence — Whistler Ski-In / Ski-Out',
		'location'        => 'Sunridge Plateau Drive, Whistler, BC',
		'corridor'        => 'whistler',
		'corridor_label'  => 'Whistler',
		'calc_corridor'   => 'whistler',
		'description'     => 'Engineered under BCBC Part 4 Structural Design for extreme high-altitude ground snow loads (Sg = 6.2 to 8.1 kPa). Heavy timber structural posts, bedrock-anchored concrete foundation, and RMOW OCP Wildfire Protection DPA Class A non-combustible roof assembly.',
		'compliance_tags' => array( 'BCBC Part 4 Snow Load 8.1 kPa', 'RMOW FireSmart DPA', 'Granite Bedrock Tie-Backs' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.07-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.14-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.22-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.30-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.38-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.45-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.51-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.56-pm.png',
		),
	),
	array(
		'id'              => 'st-andrews-north-van',
		'title'           => 'St Andrews Residence — North Shore',
		'location'        => 'St. Andrews Avenue, Lower Lonsdale / North Vancouver, BC',
		'corridor'        => 'north-vancouver',
		'corridor_label'  => 'North Vancouver',
		'calc_corridor'   => 'north-vancouver',
		'description'     => 'Cantilevered flat-roof architectural residence featuring full smart building automation, 400A underground electrical service entrance, continuous acoustic ceiling baffles, and high-performance Section 9.36 envelope assemblies.',
		'compliance_tags' => array( 'BCBC 9.36 Energy Envelope', '400A Underground Service', 'Acoustic Ceiling Baffles' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.07.36-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.11-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.16-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.21-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.27-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.33-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.38-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.46-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.54-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.09.00-pm.png',
		),
	),
	array(
		'id'              => 'dickinson-point-grey',
		'title'           => 'Dickinson Residence — Point Grey Coastal Ridge',
		'location'        => 'Dickinson Road / Point Grey Corridor, Vancouver, BC',
		'corridor'        => 'vancouver',
		'corridor_label'  => 'Vancouver Westside',
		'calc_corridor'   => 'vancouver-r1-1',
		'description'     => 'Three-storey hillside custom residence executed with winter excavation shoring and moisture control under BCBC Part 9.27 Rainscreen standards. Dual-membrane foundation damp-proofing, heavy timber ceiling joist ties, and low-E structural argon glazing.',
		'compliance_tags' => array( 'BCBC Part 9.27 Rainscreen', 'Dual-Membrane Waterproofing', 'Argon Structural Glazing' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.02.40-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.38-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.31-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.02.54-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.39-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.05-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.12-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.56-pm.png',
		),
	),
	array(
		'id'              => 'west-ridge-vancouver',
		'title'           => 'West Ridge Property — Dunbar-Southlands',
		'location'        => 'West Ridge Road / Dunbar-Southlands Corridor, Vancouver, BC',
		'corridor'        => 'vancouver',
		'corridor_label'  => 'Vancouver Westside',
		'calc_corridor'   => 'vancouver-r1-1',
		'description'     => 'Constructed under Vancouver Building By-law (VBBL Part 10) with continuous R-22 effective exterior wall insulation, Simpson HTT/HDU cast-in-place seismic hold-downs engineered for Sa=0.94g ground acceleration, and multi-zone hydronic radiant floors.',
		'compliance_tags' => array( 'VBBL Part 10 Envelope', 'R-22 Continuous Exterior', 'Seismic Hold-Downs (Sa=0.94g)' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.32-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.40-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.48-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.53-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.55.02-pm.png',
		),
	),
	array(
		'id'              => 'prima-vancouver-infill',
		'title'           => 'Prima Residence — Westside Multi-Storey Infill',
		'location'        => 'Prima Street / Vancouver Westside Infill Zone, BC',
		'corridor'        => 'vancouver',
		'corridor_label'  => 'Vancouver R1-1 / Infill',
		'calc_corridor'   => 'vancouver-r1-1',
		'description'     => 'High-density four-storey urban infill residence built to VBBL Part 9 1-hour fire-resistance rated party wall separations, zero-lot-line perimeter shoring, and balanced HRV mechanical ventilation.',
		'compliance_tags' => array( '1-Hr Fire Party Walls', 'Zero-Lot-Line Shoring', 'Dedicated HRV Mechanicals' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.12.46-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.12.55-pm.png',
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.13.00-pm.png',
		),
	),
	array(
		'id'              => 'piper-sechelt',
		'title'           => 'Piper Residence — Davis Bay Coastal',
		'location'        => 'Piper Lane, Davis Bay, Sechelt, Sunshine Coast, BC',
		'corridor'        => 'sunshine-coast',
		'corridor_label'  => 'Sunshine Coast',
		'calc_corridor'   => 'sunshine-coast',
		'description'     => 'Coastal custom residence engineered for 1/100 hourly wind pressures (q100 = 0.55 kPa) and District of Sechelt coastal setback bylaws. Self-performed BC Hydro ES54 underground DB2 PVC conduit and geotextile weeping tile in 150mm washed drain rock.',
		'compliance_tags' => array( 'Wind Uplift q100 = 0.55 kPa', 'BC Hydro ES54 DB2 Ducts', 'Boulder Retaining Civil' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.43-pm.png',
		),
	),
	array(
		'id'              => 'compass-sechelt',
		'title'           => 'Compass Residence — Trail Bay',
		'location'        => 'Compass Lane, Trail Bay, Sechelt, Sunshine Coast, BC',
		'corridor'        => 'sunshine-coast',
		'corridor_label'  => 'Sunshine Coast',
		'calc_corridor'   => 'sunshine-coast',
		'description'     => 'Constructed under BCBC Section 9.14 foundation drainage and coastal moisture management protocols. Features high water-table elastomeric waterproofing membrane, ventilated rainscreen cavity framing, and hurricane roof tie-down strapping.',
		'compliance_tags' => array( 'BCBC 9.14 Drainage', 'Elastomeric Water Barrier', 'Hurricane Roof Strapping' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.52-pm.png',
		),
	),
	array(
		'id'              => 'sullivan-sechelt',
		'title'           => 'Sullivan Residence — Sandy Hook Bedrock Framing',
		'location'        => 'Sullivan Road, Sandy Hook, Sechelt, Sunshine Coast, BC',
		'corridor'        => 'sunshine-coast',
		'corridor_label'  => 'Sunshine Coast',
		'calc_corridor'   => 'sunshine-coast',
		'description'     => 'Stepped poured-concrete foundation footings pinned directly onto cleared coastal granite bedrock, high-load structural steel support columns, glulam beams, and engineered I-joist floor spans.',
		'compliance_tags' => array( 'Granite Bedrock Footings', 'Structural Steel Columns', 'Engineered Glulam Spans' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.20.00-pm.png',
		),
	),
	array(
		'id'              => 'civil-john-deere-60g',
		'title'           => 'Self-Performed Civil Fleet — John Deere 60G Excavator',
		'location'        => 'Sea-to-Sky & North Shore Forested Trenching Corridor, BC',
		'corridor'        => 'civil',
		'corridor_label'  => 'ES54 Civil Fleet',
		'calc_corridor'   => 'squamish',
		'description'     => 'Keystone self-performs bulk rock stripping, perimeter drainage benching, and BC Hydro ES54 underground primary/secondary utility trenching (>=900mm boulevard / >=1050mm roadway cover) without third-party civil broker delays.',
		'compliance_tags' => array( 'BC Hydro ES54 Civil', 'In-House 60G Excavator', 'Zero Civil Sub-Markup' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/john-deere3.jpeg',
		),
	),
	array(
		'id'              => 'civil-slab-rebar-prep',
		'title'           => 'Compacted Clear-Crush & Welded Rebar Slab Preparation',
		'location'        => 'Sea-to-Sky Structural Foundation & Radon Sub-Slab Field Verification, BC',
		'corridor'        => 'civil',
		'corridor_label'  => 'ES54 Civil Fleet',
		'calc_corridor'   => 'squamish',
		'description'     => 'Field-verified compacted 19mm clear crushed rock capillary/radon blanket and welded wire reinforcing steel mat alongside poured architectural foundation walls prior to structural P.Eng. Schedule B pre-pour sign-off.',
		'compliance_tags' => array( 'Schedule B Pre-Pour Gate', 'Compacted Clear Crush', 'Welded Rebar Slab Grid' ),
		'gallery_images'  => array(
			'https://keystonepossibilities.ca/wp-content/uploads/2023/12/whatsapp-image-2023-10-10-at-4.53.58-pm-1.jpeg',
		),
	),
);

$kp_raw_projects = function_exists( 'kp_get_portfolio_projects' ) ? kp_get_portfolio_projects() : $kp_fallback_projects;
if ( ! is_array( $kp_raw_projects ) || empty( $kp_raw_projects ) ) {
	$kp_raw_projects = $kp_fallback_projects;
}

// Index fallback galleries by normalized title prefix so all 42 live gallery URLs are guaranteed intact.
$kp_fallback_by_key = array();
foreach ( $kp_fallback_projects as $fb_item ) {
	$prefix = strtolower( strtok( $fb_item['title'], '—–-' ) );
	$kp_fallback_by_key[ trim( $prefix ) ] = $fb_item;
}

$kp_projects  = array();
$kp_has_civil = false;

foreach ( $kp_raw_projects as $idx => $proj ) {
	if ( ! is_array( $proj ) ) {
		continue;
	}
	$title    = isset( $proj['title'] ) ? (string) $proj['title'] : ( isset( $proj['name'] ) ? (string) $proj['name'] : 'Signature Residence' );
	$prefix   = trim( strtolower( strtok( $title, '—–-' ) ) );
	$matched  = isset( $kp_fallback_by_key[ $prefix ] ) ? $kp_fallback_by_key[ $prefix ] : null;
	$gallery  = array();
	foreach ( array( 'gallery_images', 'gallery', 'images', 'photos' ) as $gkey ) {
		if ( ! empty( $proj[ $gkey ] ) && is_array( $proj[ $gkey ] ) ) {
			$gallery = $proj[ $gkey ];
			break;
		}
	}
	if ( empty( $gallery ) && ! empty( $proj['image'] ) ) {
		$gallery = array( (string) $proj['image'] );
	}
	// Guarantee full multi-photo gallery if helper returned only cover image, and reject watermarked DEZEEN file.
	if ( $matched && count( $gallery ) < count( $matched['gallery_images'] ) ) {
		$gallery = $matched['gallery_images'];
	}
	$gallery = array_values(
		array_filter(
			$gallery,
			function ( $u ) {
				return is_string( $u ) && '' !== $u && false === stripos( $u, 'forest8_' );
			}
		)
	);
	if ( empty( $gallery ) && $matched ) {
		$gallery = $matched['gallery_images'];
	}
	if ( empty( $gallery ) ) {
		continue;
	}

	$corridor_raw = isset( $proj['corridor'] ) ? (string) $proj['corridor'] : ( isset( $proj['category'] ) ? (string) $proj['category'] : ( $matched ? $matched['corridor'] : 'vancouver' ) );
	$corridor_lc  = sanitize_title( $corridor_raw );
	// Normalize corridor filter bucket.
	if ( false !== strpos( $corridor_lc, 'civil' ) || false !== stripos( $title, 'deere' ) || false !== stripos( $title, 'slab' ) ) {
		$bucket        = 'civil';
		$kp_has_civil  = true;
	} elseif ( false !== strpos( $corridor_raw, 'west-van' ) || false !== stripos( $title, 'ballantree' ) ) {
		$bucket = 'west-vancouver';
	} elseif ( false !== strpos( $corridor_raw, 'whistler' ) || false !== stripos( $title, 'sunridge' ) ) {
		$bucket = 'whistler';
	} elseif ( false !== strpos( $corridor_raw, 'north-van' ) || false !== stripos( $title, 'st andrews' ) || false !== stripos( $title, 'st-andrews' ) ) {
		$bucket = 'north-vancouver';
	} elseif ( false !== strpos( $corridor_raw, 'sunshine' ) || false !== strpos( $corridor_raw, 'sechelt' ) || false !== stripos( $title, 'piper' ) || false !== stripos( $title, 'compass' ) || false !== stripos( $title, 'sullivan' ) ) {
		$bucket = 'sunshine-coast';
	} else {
		$bucket = 'vancouver';
	}

	$tags = array();
	foreach ( array( 'compliance_tags', 'tags', 'specs' ) as $tkey ) {
		if ( ! empty( $proj[ $tkey ] ) && is_array( $proj[ $tkey ] ) ) {
			$tags = $proj[ $tkey ];
			break;
		}
	}
	if ( empty( $tags ) && $matched ) {
		$tags = $matched['compliance_tags'];
	}

	$kp_projects[] = array(
		'id'             => isset( $proj['id'] ) ? sanitize_title( (string) $proj['id'] ) : 'proj-' . $idx,
		'title'          => $title,
		'location'       => isset( $proj['location'] ) ? (string) $proj['location'] : ( $matched ? $matched['location'] : 'British Columbia' ),
		'corridor'       => $bucket,
		'corridor_label' => isset( $proj['corridor_label'] ) ? (string) $proj['corridor_label'] : ( $matched ? $matched['corridor_label'] : ucwords( str_replace( '-', ' ', $bucket ) ) ),
		'calc_corridor'  => isset( $proj['calc_corridor'] ) ? (string) $proj['calc_corridor'] : ( $matched ? $matched['calc_corridor'] : ( 'vancouver' === $bucket ? 'vancouver-r1-1' : $bucket ) ),
		'description'    => isset( $proj['description'] ) ? (string) $proj['description'] : ( isset( $proj['summary'] ) ? (string) $proj['summary'] : ( $matched ? $matched['description'] : '' ) ),
		'tags'           => array_slice( array_map( 'strval', $tags ), 0, 4 ),
		'gallery'        => $gallery,
	);
}

// Ensure the 2 real 2023 civil field items are always included alongside the 9 residences.
if ( ! $kp_has_civil ) {
	foreach ( array_slice( $kp_fallback_projects, -2 ) as $civ ) {
		$kp_projects[] = array(
			'id'             => $civ['id'],
			'title'          => $civ['title'],
			'location'       => $civ['location'],
			'corridor'       => 'civil',
			'corridor_label' => $civ['corridor_label'],
			'calc_corridor'  => $civ['calc_corridor'],
			'description'    => $civ['description'],
			'tags'           => $civ['compliance_tags'],
			'gallery'        => $civ['gallery_images'],
		);
	}
}

$kp_uid = wp_unique_id( 'kp-port-' );

if ( empty( $GLOBALS['kp_v3_portfolio_reel_css'] ) ) :
	$GLOBALS['kp_v3_portfolio_reel_css'] = true;
	?>
	<style id="kp-v3-portfolio-reel-styles">
		.kp-port-section {
			padding: clamp(56px, 7vw, 92px) 0;
			background: #04070d;
			color: #f8fafc;
			position: relative;
			border-top: 1px solid rgba(212, 175, 55, 0.14);
		}
		.kp-port-wrap {
			width: min(1340px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-port-top {
			display: flex;
			flex-wrap: wrap;
			justify-content: space-between;
			align-items: flex-end;
			gap: 20px;
			margin-bottom: 24px;
		}
		.kp-port-kicker {
			display: inline-flex;
			align-items: center;
			gap: 8px;
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: #d4af37;
			margin-bottom: 10px;
		}
		.kp-port-kicker::before {
			content: '';
			width: 7px;
			height: 7px;
			border-radius: 50%;
			background: #d4af37;
			box-shadow: 0 0 10px rgba(212, 175, 55, 0.75);
		}
		.kp-port-h2 {
			font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
			font-size: clamp(1.65rem, 3.2vw, 2.45rem);
			font-weight: 700;
			line-height: 1.15;
			letter-spacing: -0.02em;
			color: #f8fafc;
			margin: 0 0 10px;
			max-width: 780px;
		}
		.kp-port-sub {
			font-size: 0.96rem;
			line-height: 1.62;
			color: #cbd5e1;
			max-width: 760px;
			margin: 0;
		}
		.kp-port-toolbar {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			justify-content: space-between;
			gap: 12px;
			margin-bottom: 24px;
		}
		.kp-port-filters {
			display: flex;
			flex-wrap: wrap;
			gap: 8px;
		}
		.kp-port-pill {
			appearance: none;
			background: rgba(10, 16, 29, 0.88);
			border: 1px solid rgba(212, 175, 55, 0.26);
			color: #cbd5e1;
			border-radius: 999px;
			padding: 8px 15px;
			min-height: 38px;
			font-family: 'Inter', sans-serif;
			font-size: 0.78rem;
			font-weight: 600;
			cursor: pointer;
			transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease;
		}
		.kp-port-pill:hover,
		.kp-port-pill.is-active {
			background: linear-gradient(135deg, rgba(212, 175, 55, 0.22), rgba(200, 164, 93, 0.08));
			border-color: #d4af37;
			color: #f8fafc;
		}
		.kp-port-glide {
			display: inline-flex;
			gap: 8px;
		}
		.kp-port-arrow {
			width: 42px;
			height: 42px;
			border-radius: 50%;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.36);
			color: #f8fafc;
			display: inline-flex;
			align-items: center;
			justify-content: center;
			cursor: pointer;
			transition: border-color 0.2s ease, transform 0.2s ease;
		}
		.kp-port-arrow:hover {
			border-color: #d4af37;
			color: #d4af37;
			transform: translateY(-1px);
		}
		.kp-port-track.is-reel {
			display: grid;
			grid-auto-flow: column;
			grid-auto-columns: minmax(305px, 385px);
			gap: 20px;
			overflow-x: auto;
			scroll-snap-type: x mandatory;
			scroll-behavior: smooth;
			padding-bottom: 14px;
			scrollbar-width: thin;
			scrollbar-color: rgba(212, 175, 55, 0.45) rgba(10, 16, 29, 0.6);
		}
		@media (max-width: 480px) {
			.kp-port-track.is-reel {
				grid-auto-columns: minmax(276px, 86vw);
			}
		}
		.kp-port-track.is-grid {
			display: grid;
			grid-template-columns: repeat(auto-fill, minmax(min(100%, 350px), 1fr));
			gap: 22px;
		}
		.kp-port-card {
			scroll-snap-align: start;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.24);
			border-radius: 18px;
			overflow: hidden;
			display: flex;
			flex-direction: column;
			cursor: pointer;
			transition: border-color 0.24s ease, box-shadow 0.24s ease, transform 0.24s ease;
			box-shadow: 0 18px 42px rgba(0, 0, 0, 0.52);
		}
		.kp-port-card:hover {
			border-color: rgba(212, 175, 55, 0.68);
			transform: translateY(-3px);
			box-shadow: 0 24px 54px rgba(0, 0, 0, 0.72), 0 0 24px rgba(212, 175, 55, 0.12);
		}
		.kp-port-card[hidden] {
			display: none !important;
		}
		.kp-port-media {
			position: relative;
			aspect-ratio: 16 / 10;
			background: #04070d;
			overflow: hidden;
		}
		.kp-port-media img {
			width: 100%;
			height: 100%;
			object-fit: cover;
			display: block;
			transition: transform 0.45s ease;
		}
		.kp-port-card:hover .kp-port-media img {
			transform: scale(1.035);
		}
		.kp-port-badges {
			position: absolute;
			top: 12px;
			left: 12px;
			right: 12px;
			display: flex;
			justify-content: space-between;
			align-items: center;
			gap: 8px;
			pointer-events: none;
		}
		.kp-port-corridor-chip {
			background: rgba(4, 7, 13, 0.86);
			backdrop-filter: blur(10px);
			border: 1px solid rgba(212, 175, 55, 0.48);
			color: #f8fafc;
			font-size: 0.7rem;
			font-weight: 700;
			letter-spacing: 0.04em;
			text-transform: uppercase;
			padding: 4px 10px;
			border-radius: 999px;
		}
		.kp-port-count-chip {
			background: rgba(4, 7, 13, 0.88);
			border: 1px solid rgba(56, 189, 248, 0.38);
			color: #e2e8f0;
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.68rem;
			font-weight: 600;
			padding: 4px 9px;
			border-radius: 999px;
		}
		.kp-port-body {
			padding: 18px 20px 20px;
			display: flex;
			flex-direction: column;
			flex: 1;
			gap: 10px;
		}
		.kp-port-title {
			font-family: 'Outfit', sans-serif;
			font-size: 1.12rem;
			font-weight: 700;
			color: #f8fafc;
			margin: 0;
			line-height: 1.28;
		}
		.kp-port-loc {
			font-size: 0.78rem;
			color: #d4af37;
			font-weight: 600;
			margin: 0;
		}
		.kp-port-desc {
			font-size: 0.84rem;
			line-height: 1.56;
			color: #cbd5e1;
			margin: 0;
			display: -webkit-box;
			-webkit-line-clamp: 3;
			-webkit-box-orient: vertical;
			overflow: hidden;
		}
		.kp-port-tags {
			display: flex;
			flex-wrap: wrap;
			gap: 6px;
			margin-top: auto;
			padding-top: 6px;
		}
		.kp-port-tag {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.66rem;
			color: #e2e8f0;
			background: rgba(255, 255, 255, 0.04);
			border: 1px solid rgba(212, 175, 55, 0.22);
			border-radius: 6px;
			padding: 3px 8px;
		}
		.kp-port-cta-row {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding-top: 10px;
			border-top: 1px solid rgba(255, 255, 255, 0.07);
			font-size: 0.78rem;
			font-weight: 700;
			color: #d4af37;
		}
		/* Full-Screen Multi-Photo Lightbox Modal */
		.kp-port-modal {
			position: fixed;
			inset: 0;
			z-index: 99999;
			background: rgba(4, 7, 13, 0.94);
			backdrop-filter: blur(18px);
			display: none;
			align-items: center;
			justify-content: center;
			padding: clamp(12px, 3vw, 28px);
		}
		.kp-port-modal.is-open {
			display: flex;
		}
		.kp-port-dialog {
			width: min(1180px, 100%);
			max-height: 92vh;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.45);
			border-radius: 20px;
			overflow-y: auto;
			display: grid;
			grid-template-columns: 1.45fr 0.85fr;
			box-shadow: 0 30px 80px rgba(0, 0, 0, 0.9);
		}
		@media (max-width: 920px) {
			.kp-port-dialog {
				grid-template-columns: 1fr;
			}
		}
		.kp-port-stage-col {
			background: #04070d;
			padding: 16px;
			display: flex;
			flex-direction: column;
			gap: 12px;
		}
		.kp-port-stage {
			position: relative;
			aspect-ratio: 16 / 10;
			background: #020408;
			border-radius: 12px;
			overflow: hidden;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		.kp-port-stage img {
			max-width: 100%;
			max-height: 100%;
			width: 100%;
			height: 100%;
			object-fit: contain;
		}
		.kp-port-stage-nav {
			position: absolute;
			top: 50%;
			transform: translateY(-50%);
			width: 42px;
			height: 42px;
			border-radius: 50%;
			background: rgba(4, 7, 13, 0.85);
			border: 1px solid rgba(212, 175, 55, 0.55);
			color: #f8fafc;
			cursor: pointer;
			display: inline-flex;
			align-items: center;
			justify-content: center;
		}
		.kp-port-stage-nav.prev { left: 12px; }
		.kp-port-stage-nav.next { right: 12px; }
		.kp-port-thumbs {
			display: flex;
			gap: 8px;
			overflow-x: auto;
			padding-bottom: 4px;
		}
		.kp-port-thumb {
			width: 68px;
			height: 48px;
			border-radius: 8px;
			overflow: hidden;
			border: 2px solid transparent;
			opacity: 0.62;
			cursor: pointer;
			flex-shrink: 0;
			padding: 0;
			background: #04070d;
		}
		.kp-port-thumb.is-active,
		.kp-port-thumb:hover {
			border-color: #d4af37;
			opacity: 1;
		}
		.kp-port-thumb img {
			width: 100%;
			height: 100%;
			object-fit: cover;
			display: block;
		}
		.kp-port-info-col {
			padding: 24px;
			display: flex;
			flex-direction: column;
			gap: 14px;
		}
		.kp-port-close {
			align-self: flex-end;
			background: rgba(255, 255, 255, 0.05);
			border: 1px solid rgba(212, 175, 55, 0.35);
			color: #f8fafc;
			border-radius: 999px;
			padding: 6px 14px;
			font-size: 0.78rem;
			font-weight: 700;
			cursor: pointer;
		}
		.kp-port-modal-btn {
			display: inline-flex;
			align-items: center;
			justify-content: center;
			gap: 8px;
			margin-top: auto;
			padding: 13px 20px;
			border-radius: 999px;
			background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 52%, #b89028 100%);
			color: #04070d !important;
			font-weight: 800;
			font-size: 0.86rem;
			text-decoration: none;
			border: none;
			cursor: pointer;
		}
	</style>
<?php endif; ?>

<section id="<?php echo esc_attr( $kp_section_id ); ?>" class="kp-port-section" data-kp-portfolio="<?php echo esc_attr( $kp_uid ); ?>" data-default-filter="<?php echo esc_attr( $kp_default_filter ); ?>">
	<div class="kp-port-wrap">
		<div class="kp-port-top">
			<div>
				<div class="kp-port-kicker"><?php echo esc_html( $kp_kicker ); ?></div>
				<h2 class="kp-port-h2"><?php echo esc_html( $kp_heading ); ?></h2>
				<p class="kp-port-sub"><?php echo esc_html( $kp_subcopy ); ?></p>
			</div>
			<?php if ( 'reel' === $kp_mode ) : ?>
				<div class="kp-port-glide" aria-label="Portfolio Reel Navigation">
					<button type="button" class="kp-port-arrow" data-port-prev aria-label="Scroll Portfolio Left">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
					</button>
					<button type="button" class="kp-port-arrow" data-port-next aria-label="Scroll Portfolio Right">
						<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
					</button>
				</div>
			<?php endif; ?>
		</div>

		<div class="kp-port-toolbar">
			<div class="kp-port-filters" role="tablist" aria-label="Filter Portfolio by BC Corridor">
				<?php
				$kp_filter_tabs = array(
					'all'             => 'All Verified (' . count( $kp_projects ) . ')',
					'west-vancouver'  => 'West Vancouver',
					'whistler'        => 'Whistler Alpine',
					'north-vancouver' => 'North Vancouver',
					'vancouver'       => 'Vancouver Westside & Infill',
					'sunshine-coast'  => 'Sunshine Coast',
					'civil'           => 'ES54 Civil Fleet',
				);
				foreach ( $kp_filter_tabs as $f_slug => $f_label ) :
					$is_active = ( $kp_default_filter === $f_slug ) || ( ! isset( $kp_filter_tabs[ $kp_default_filter ] ) && 'all' === $f_slug );
					?>
					<button
						type="button"
						class="kp-port-pill<?php echo $is_active ? ' is-active' : ''; ?>"
						data-port-filter="<?php echo esc_attr( $f_slug ); ?>"
					>
						<?php echo esc_html( $f_label ); ?>
					</button>
				<?php endforeach; ?>
			</div>
		</div>

		<div class="kp-port-track is-<?php echo esc_attr( $kp_mode ); ?>" data-port-track>
			<?php foreach ( $kp_projects as $p_idx => $item ) :
				$photo_count = count( $item['gallery'] );
				$hidden_attr = ( 'all' !== $kp_default_filter && isset( $kp_filter_tabs[ $kp_default_filter ] ) && $item['corridor'] !== $kp_default_filter ) ? ' hidden' : '';
				?>
				<article
					class="kp-port-card"
					tabindex="0"
					role="button"
					aria-label="<?php echo esc_attr( 'Inspect ' . $item['title'] . ' (' . $photo_count . ' photos)' ); ?>"
					data-port-card="<?php echo esc_attr( (string) $p_idx ); ?>"
					data-corridor="<?php echo esc_attr( $item['corridor'] ); ?>"<?php echo $hidden_attr; ?>
				>
					<div class="kp-port-media">
						<img
							src="<?php echo esc_url( $item['gallery'][0] ); ?>"
							alt="<?php echo esc_attr( $item['title'] . ' — ' . $item['location'] ); ?>"
							loading="lazy"
							decoding="async"
						/>
						<div class="kp-port-badges">
							<span class="kp-port-corridor-chip"><?php echo esc_html( $item['corridor_label'] ); ?></span>
							<span class="kp-port-count-chip"><?php echo esc_html( $photo_count . ( 1 === $photo_count ? ' PHOTO' : ' PHOTOS' ) ); ?></span>
						</div>
					</div>
					<div class="kp-port-body">
						<h3 class="kp-port-title"><?php echo esc_html( $item['title'] ); ?></h3>
						<p class="kp-port-loc"><?php echo esc_html( $item['location'] ); ?></p>
						<p class="kp-port-desc"><?php echo esc_html( $item['description'] ); ?></p>
						<div class="kp-port-tags">
							<?php foreach ( $item['tags'] as $tag_txt ) : ?>
								<span class="kp-port-tag"><?php echo esc_html( $tag_txt ); ?></span>
							<?php endforeach; ?>
						</div>
						<div class="kp-port-cta-row">
							<span>Open Inspection Gallery</span>
							<span><?php echo esc_html( $photo_count ); ?> Views &rarr;</span>
						</div>
					</div>
				</article>
			<?php endforeach; ?>
		</div>
	</div>

	<div class="kp-port-modal" data-port-modal role="dialog" aria-modal="true" aria-label="Residence Photograph Inspection Lightbox">
		<div class="kp-port-dialog">
			<div class="kp-port-stage-col">
				<div class="kp-port-stage">
					<button type="button" class="kp-port-stage-nav prev" data-stage-prev aria-label="Previous Photograph">&#8592;</button>
					<img src="" alt="" data-stage-img />
					<button type="button" class="kp-port-stage-nav next" data-stage-next aria-label="Next Photograph">&#8594;</button>
				</div>
				<div class="kp-port-thumbs" data-stage-thumbs></div>
			</div>
			<div class="kp-port-info-col">
				<button type="button" class="kp-port-close" data-modal-close>Close Gallery &times;</button>
				<span class="kp-port-corridor-chip" style="align-self:flex-start;" data-modal-corridor></span>
				<h3 class="kp-port-title" style="font-size:1.38rem;" data-modal-title></h3>
				<p class="kp-port-loc" data-modal-loc></p>
				<p class="kp-port-desc" style="-webkit-line-clamp:unset;overflow:visible;" data-modal-desc></p>
				<div class="kp-port-tags" style="margin-top:4px;" data-modal-tags></div>
				<div style="font-family:'JetBrains Mono',monospace;font-size:0.74rem;color:#94a3b8;" data-modal-counter></div>
				<a href="#calculator" class="kp-port-modal-btn" data-modal-calc-btn>
					Model This Corridor in Cost Console &rarr;
				</a>
			</div>
		</div>
	</div>

	<script>
	(function() {
		var root = document.querySelector('[data-kp-portfolio="<?php echo esc_js( $kp_uid ); ?>"]');
		if (!root) return;
		var projects = <?php echo wp_json_encode( $kp_projects ); ?>;
		var track = root.querySelector('[data-port-track]');
		var cards = Array.prototype.slice.call(root.querySelectorAll('[data-port-card]'));
		var pills = Array.prototype.slice.call(root.querySelectorAll('[data-port-filter]'));
		var prevBtn = root.querySelector('[data-port-prev]');
		var nextBtn = root.querySelector('[data-port-next]');

		pills.forEach(function(pill) {
			pill.addEventListener('click', function() {
				var f = pill.getAttribute('data-port-filter');
				pills.forEach(function(p) { p.classList.toggle('is-active', p === pill); });
				cards.forEach(function(c) {
					var match = (f === 'all' || c.getAttribute('data-corridor') === f);
					if (match) c.removeAttribute('hidden');
					else c.setAttribute('hidden', 'hidden');
				});
			});
		});

		if (prevBtn && track) {
			prevBtn.addEventListener('click', function() { track.scrollBy({ left: -400, behavior: 'smooth' }); });
		}
		if (nextBtn && track) {
			nextBtn.addEventListener('click', function() { track.scrollBy({ left: 400, behavior: 'smooth' }); });
		}

		var modal = root.querySelector('[data-port-modal]');
		var stageImg = root.querySelector('[data-stage-img]');
		var thumbsWrap = root.querySelector('[data-stage-thumbs]');
		var titleEl = root.querySelector('[data-modal-title]');
		var locEl = root.querySelector('[data-modal-loc]');
		var corrEl = root.querySelector('[data-modal-corridor]');
		var descEl = root.querySelector('[data-modal-desc]');
		var tagsEl = root.querySelector('[data-modal-tags]');
		var counterEl = root.querySelector('[data-modal-counter]');
		var calcBtn = root.querySelector('[data-modal-calc-btn]');
		var activeProj = null;
		var activePhoto = 0;

		function renderPhoto(idx) {
			if (!activeProj || !activeProj.gallery.length) return;
			activePhoto = (idx + activeProj.gallery.length) % activeProj.gallery.length;
			stageImg.src = activeProj.gallery[activePhoto];
			stageImg.alt = activeProj.title + ' — Photo ' + (activePhoto + 1);
			counterEl.textContent = 'Photograph ' + (activePhoto + 1) + ' of ' + activeProj.gallery.length + ' · BC Builder #52603 Verified Record';
			Array.prototype.forEach.call(thumbsWrap.children, function(btn, bIdx) {
				btn.classList.toggle('is-active', bIdx === activePhoto);
			});
		}

		function openProject(pIdx) {
			activeProj = projects[pIdx];
			if (!activeProj) return;
			titleEl.textContent = activeProj.title;
			locEl.textContent = activeProj.location;
			corrEl.textContent = activeProj.corridor_label;
			descEl.textContent = activeProj.description;
			tagsEl.innerHTML = '';
			(activeProj.tags || []).forEach(function(t) {
				var sp = document.createElement('span');
				sp.className = 'kp-port-tag';
				sp.textContent = t;
				tagsEl.appendChild(sp);
			});
			thumbsWrap.innerHTML = '';
			(activeProj.gallery || []).forEach(function(url, gIdx) {
				var b = document.createElement('button');
				b.type = 'button';
				b.className = 'kp-port-thumb' + (gIdx === 0 ? ' is-active' : '');
				var im = document.createElement('img');
				im.src = url;
				im.alt = 'Thumbnail ' + (gIdx + 1);
				b.appendChild(im);
				b.addEventListener('click', function() { renderPhoto(gIdx); });
				thumbsWrap.appendChild(b);
			});
			renderPhoto(0);
			modal.classList.add('is-open');
			document.body.style.overflow = 'hidden';
		}

		function closeModal() {
			modal.classList.remove('is-open');
			document.body.style.overflow = '';
		}

		cards.forEach(function(card) {
			var idx = parseInt(card.getAttribute('data-port-card'), 10);
			card.addEventListener('click', function() { openProject(idx); });
			card.addEventListener('keydown', function(e) {
				if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openProject(idx); }
			});
		});

		root.querySelector('[data-stage-prev]').addEventListener('click', function() { renderPhoto(activePhoto - 1); });
		root.querySelector('[data-stage-next]').addEventListener('click', function() { renderPhoto(activePhoto + 1); });
		root.querySelector('[data-modal-close]').addEventListener('click', closeModal);
		modal.addEventListener('click', function(e) { if (e.target === modal) closeModal(); });

		calcBtn.addEventListener('click', function(e) {
			var calcSelect = document.querySelector('[data-kp-calc-corridor]');
			if (calcSelect && activeProj && activeProj.calc_corridor) {
				e.preventDefault();
				closeModal();
				calcSelect.value = activeProj.calc_corridor;
				calcSelect.dispatchEvent(new Event('change', { bubbles: true }));
				var calcSec = document.getElementById('calculator') || calcSelect.closest('section');
				if (calcSec) calcSec.scrollIntoView({ behavior: 'smooth' });
			} else {
				closeModal();
				calcBtn.href = '<?php echo esc_url( home_url( '/#calculator' ) ); ?>';
			}
		});

		document.addEventListener('keydown', function(e) {
			if (!modal.classList.contains('is-open')) return;
			if (e.key === 'Escape') closeModal();
			if (e.key === 'ArrowLeft') renderPhoto(activePhoto - 1);
			if (e.key === 'ArrowRight') renderPhoto(activePhoto + 1);
		});
	})();
	</script>
</section>
