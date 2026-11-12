<?php
/**
 * Template Name: Regional Corridor Hub
 * Template Post Type: page
 *
 * Data-driven Regional Corridor Engineering Hub resolving active page slug across all 9 BC corridors:
 * West Vancouver, Whistler, Squamish HQ, North Vancouver, Vancouver R1-1, Coquitlam,
 * Sunshine Coast, Pemberton, and Vancouver Island.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_active_slug = ! empty( $kp_forced_corridor_slug )
	? sanitize_title( (string) $kp_forced_corridor_slug )
	: sanitize_title( (string) get_post_field( 'post_name', get_queried_object_id() ) );

// Normalize all live & legacy regional slugs to canonical 9-corridor keys.
$kp_corridor_alias_map = array(
	'west-vancouver'                    => 'west-vancouver',
	'west-vancouver-custom-homes'       => 'west-vancouver',
	'west-vancouver-luxury-renovations' => 'west-vancouver',
	'whistler'                          => 'whistler',
	'whistler-custom-homes'             => 'whistler',
	'whistler-luxury-builder'           => 'whistler',
	'squamish'                          => 'squamish',
	'squamish-custom-homes'             => 'squamish',
	'squamish-custom-home-builder'      => 'squamish',
	'north-vancouver'                   => 'north-vancouver',
	'north-vancouver-custom-homes'      => 'north-vancouver',
	'north-vancouver-multiplex-conversions' => 'north-vancouver',
	'vancouver'                         => 'vancouver-r1-1',
	'vancouver-multiplex'               => 'vancouver-r1-1',
	'vancouver-r1-1'                    => 'vancouver-r1-1',
	'vancouver-r1-1-multiplex-builder'  => 'vancouver-r1-1',
	'coquitlam'                         => 'coquitlam',
	'coquitlam-custom-homes-multiplex'  => 'coquitlam',
	'sunshine-coast'                    => 'sunshine-coast',
	'sunshine-coast-custom-homes'       => 'sunshine-coast',
	'pemberton'                         => 'pemberton',
	'pemberton-luxury-builder'          => 'pemberton',
	'vancouver-island'                  => 'vancouver-island',
	'vancouver-island-custom-homes'     => 'vancouver-island',
);

$kp_corridor_key = isset( $kp_corridor_alias_map[ $kp_active_slug ] ) ? $kp_corridor_alias_map[ $kp_active_slug ] : 'squamish';

$kp_corridor_registry = array(
	'west-vancouver'   => array(
		'name'             => 'West Vancouver',
		'kicker'           => 'WEST VANCOUVER CLIFFSIDE & BEDROCK COMMAND · BYLAW 4662 & 4364',
		'h1'               => 'West Vancouver Cliffside Custom Estates & Granite Micropile Engineering.',
		'lead'             => 'From 5610 Ballantree Road in the British Properties to Caulfeild and Altamont oceanfront bluffs, Principal Superintendent Wayne Stevenson (#52603) directs deep granodiorite rock anchors, cantilevered structural steel, BC Hydro ES54 underground vaults, and Open-Book CCDC 5B execution.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.57.48-pm.png',
		'hero_caption'     => 'Ballantree Residence — 5610 Ballantree Rd, British Properties, West Vancouver',
		'portfolio_filter' => 'west-vancouver',
		'bylaws'           => array(
			'District of West Vancouver Zoning Bylaw No. 4662 & Bill 44 SSMUH Infill Amendments',
			'Watercourse Protection & Riparian Areas Bylaw No. 4364 (15m Top-of-Bank Setback)',
			'BC Energy Step Code 5 / Zero Carbon Step Code EL-4 Air-Barrier (<1.0 ACH50)',
			'BC Hydro ES54 Underground Primary/Secondary DB2 Conduit & CEC Rule 26-242 PMT Clearances',
		),
		'specs'            => array(
			array( 'title' => 'Granite Micropiles & Tie-Backs', 'desc' => 'Socketed steel micropiles and post-tensioned bedrock anchors engineered with Thurber / Glotman Simpson Schedule B field reviews.' ),
			array( 'title' => 'Thermal-Broken Cantilever Steel', 'desc' => 'Structural steel view cantilevers isolated with structural thermal breaks to prevent interior condensation and pass Step Code 5.' ),
			array( 'title' => 'Open-Book CCDC 5B Cost Control', 'desc' => 'Full 3-bid sub-trade transparency across architectural concrete, curtainwall glazing, and hydronic mechanical packages.' ),
		),
		'faqs'             => array(
			array( 'q' => 'How do you manage steep granite excavation costs in the British Properties?', 'a' => 'Prior to construction, we pair borehole/outcrop probing with line-drilling or hydraulic rock-splitting allowances and 3-bid civil tenders so bedrock removal is quantified openly before foundation formwork begins.' ),
			array( 'q' => 'Can West Vancouver lots accommodate private 400A–800A underground BC Hydro vaults?', 'a' => 'Yes. As a BC Hydro Registered ES54 Civil Contractor, Keystone self-performs DB2 PVC duct banks and Pad-Mounted Transformer vaults compliant with CEC Rule 26-242 3.0m hot-stick clearances.' ),
		),
	),
	'whistler'         => array(
		'name'             => 'Whistler',
		'kicker'           => 'WHISTLER ALPINE ESTATE COMMAND · RMOW BYLAWS 2440/2441 & SNOW LOAD 8.1 kPa',
		'h1'               => 'Whistler Alpine Custom Estates Engineered for 8.1 kPa Snow Loads & Step Code 5.',
		'lead'             => 'Proven on Sunridge Plateau ski-in/ski-out granite ridges: heavy timber and structural steel framing engineered for BCBC Part 4 extreme ground snow loads (Sg = 6.2–8.1 kPa), RMOW Class A FireSmart DPAs, cold-roof ventilation, and 100% Open-Book CCDC 5B management.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.07-pm.png',
		'hero_caption'     => 'Sunridge Residence — Sunridge Plateau Drive, Whistler Ski-In / Ski-Out Zone',
		'portfolio_filter' => 'whistler',
		'bylaws'           => array(
			'Resort Municipality of Whistler (RMOW) Zoning & Parking Bylaw (Bylaws 2440 / 2441 SSMUH)',
			'BCBC 2024 Part 4 Structural Design for High-Altitude Ground Snow Loads (Sg = 6.2 to 8.1 kPa)',
			'RMOW Official Community Plan Wildfire Protection DPA (Class A Non-Combustible Cladding & Roofing)',
			'Mandatory Step Code 5 / Zero Carbon EL-4 Envelope & Cold-Climate Heat Pump Integration',
		),
		'specs'            => array(
			array( 'title' => 'Alpine Cold-Roof & Ice-Dam Prevention', 'desc' => 'Ventilated cold-roof plenums over continuous exterior Rockwool insulation and high-temperature self-adhered waterproofing membranes.' ),
			array( 'title' => 'Seasonal Bedrock & Crane Sequencing', 'desc' => 'Tightly scheduled April–November blasting, bedrock tie-backs, and structural lockup before heavy winter snowpack arrival.' ),
			array( 'title' => 'Hydronic Snow-Melt & 600A–800A ES54', 'desc' => 'Glycol driveway/terrace snow-melt manifolds backed by self-performed BC Hydro ES54 high-amperage underground service vaults.' ),
		),
		'faqs'             => array(
			array( 'q' => 'How do you prevent Whistler winter weather from stalling a custom build schedule?', 'a' => 'Operating from nearby Squamish HQ (40 minutes south), we lock in spring rock blasting and summer foundation/steel erection so the building is fully enclosed and heated before November snowfall.' ),
			array( 'q' => 'What roof assembly prevents ice damming under 8.1 kPa Whistler snowpacks?', 'a' => 'We construct thermally decoupled ventilated cold roofs over continuous exterior insulation and Grace HT ice-and-water membranes so roof deck temperatures remain equalized with ambient alpine air.' ),
		),
	),
	'squamish'         => array(
		'name'             => 'Squamish HQ',
		'kicker'           => 'KEYSTONE HEADQUARTERS · 1 WATTS POINT RD · BYLAWS 2771 / 2200 & FCL',
		'h1'               => 'Squamish Custom Homes, Bill 44 Multiplexes & Flood-Resilient Civil Engineering.',
		'lead'             => 'Headquartered at 1 Watts Point Road in Squamish, Wayne Stevenson (#52603) delivers rapid local supervision across Tantalus, Garibaldi Highlands, Crumpit Woods, and Brackendale—combining Flood Construction Level (FCL) foundations, 3.4 kPa snow-load framing, and self-performed ES54 civil.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/luxury-home-construction-squamish-bc-aerial.jpeg',
		'hero_caption'     => 'Squamish Mountain Corridor — Steel, Timber & Board-Formed Concrete Execution',
		'portfolio_filter' => 'civil',
		'bylaws'           => array(
			'District of Squamish Zoning Bylaw No. 2200 & Bill 44 SSMUH 3–6 Unit Infill Amendments',
			'Squamish Floodplain Management Bylaw & Geodetically Pinned Flood Construction Levels (FCL)',
			'Ground Snow Load Sg = 3.4 kPa + Howe Sound Outflow Wind Uplift Strapping',
			'BC Energy Step Code 4/5 & Zero Carbon EL-4 Heat-Pump / Zehnder ERV Compliance',
		),
		'specs'            => array(
			array( 'title' => 'FCL Structural Fill & Raft Slabs', 'desc' => 'Engineered compacted clear-crush structural pads and hydrostatic perimeter drainage meeting District of Squamish floodplain covenants.' ),
			array( 'title' => '40484 Tantalus Rd Benchmark', 'desc' => 'Live 6-tab Open-Book CCDC 5B Client Portal governance proven on local Squamish custom and Bill 44 multiplex builds.' ),
			array( 'title' => 'Zero Travel Markup (Local HQ)', 'desc' => 'Immediate daily superintendent presence from 1 Watts Point Rd with our own John Deere 60G civil fleet.' ),
		),
		'faqs'             => array(
			array( 'q' => 'How do Squamish Flood Construction Levels (FCL) affect custom home or multiplex foundations?', 'a' => 'In Brackendale, Dentville, and valley-floor zones, habitable floor elevations must sit above designated geodetic FCL benchmarks using engineered structural fill, flood-vented crawlspaces, or non-habitable concrete podium garages.' ),
			array( 'q' => 'Can a standard Squamish single-family lot now build 3 to 6 units under Bill 44?', 'a' => 'Most serviced single-family parcels outside hazardous slope/flood exemptions qualify for 3–4 units (or up to 6 near frequent transit), subject to water main sizing and BC Hydro ES54 400A multi-meter clearance.' ),
		),
	),
	'north-vancouver'  => array(
		'name'             => 'North Vancouver',
		'kicker'           => 'NORTH SHORE FOOTHILL & INFILL COMMAND · DNV / CNV SSMUH & SPEA',
		'h1'               => 'North Vancouver Custom Estates, Steep-Slope Shoring & SSMUH Multiplexes.',
		'lead'             => 'From Edgemont Village and Upper Lonsdale to Deep Cove and Lynn Valley, Keystone Possibilities engineers high-rainfall BCBC 9.27 rainscreen envelopes, glacial-till foundation shoring, active radon/hydrostatic waterproofing, and 4–6 unit missing-middle multiplexes.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.07.36-pm.png',
		'hero_caption'     => 'St Andrews Residence — 400A Cantilevered North Shore Architectural Build',
		'portfolio_filter' => 'north-vancouver',
		'bylaws'           => array(
			'District & City of North Vancouver Bill 44 SSMUH 4–6 Unit Zoning Bylaws',
			'Streamside Protection & Enhancement Area (SPEA) Ravine & Arborist Tree Protection Gates',
			'BCBC 2024 9.13 Hydrostatic Basement Waterproofing & 9.13.4 Sub-Slab Radon Mitigation',
			'Step Code 5 Exterior Stone-Wool Rainscreen Continuity (<1.0 ACH50)',
		),
		'specs'            => array(
			array( 'title' => 'High Water-Table & Ravine Drainage', 'desc' => 'Dual elastomeric membranes, dimple matrix boards, and dual rigid PVC weeping/storm lines engineered for North Shore rainfall.' ),
			array( 'title' => '400A Smart & EVEMS Service', 'desc' => 'Self-performed BC Hydro ES54 underground ducting for multi-family EVEMS load sharing and heat-pump cascades.' ),
			array( 'title' => 'STC 55+ Acoustic Party Walls', 'desc' => 'Decoupled double-stud fire and acoustic separations delivering single-family quietness inside North Shore multiplexes.' ),
		),
		'faqs'             => array(
			array( 'q' => 'What causes basement moisture failures on North Vancouver hillside lots?', 'a' => 'Subsurface groundwater perched atop dense glacial till creates hydrostatic head pressure. We install dual-layer elastomeric waterproofing, washed clear-crush rock beds, and camera-verified perimeter drains before backfill.' ),
		),
	),
	'vancouver-r1-1'   => array(
		'name'             => 'Vancouver R1-1 & Westside',
		'kicker'           => 'CITY OF VANCOUVER R1-1 MULTIPLEX & WESTSIDE ESTATES · VBBL 2025',
		'h1'               => 'Vancouver R1-1 4–8 Unit Multiplexes & Point Grey / Dunbar Custom Estates.',
		'lead'             => 'Complete engineering execution under the City of Vancouver R1-1 Residential Inclusive Schedule (1.0 FSR) and VBBL: zero-lot-line shoring, 2-inch domestic water main upgrades, NFPA 13D/13R fire sprinklers, adaptable sills, and BC Hydro ES54 400A–600A PMT clearances.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.02.40-pm.png',
		'hero_caption'     => 'Dickinson Residence — Point Grey Coastal Ridge, Vancouver (Plus West Ridge & Prima Infill)',
		'portfolio_filter' => 'vancouver',
		'bylaws'           => array(
			'City of Vancouver R1-1 District Schedule (Up to 1.0 FSR · 4–6 Strata Units or 8 Secured Rental)',
			'Vancouver Building By-law (VBBL) Part 4 Lateral Shear, NFPA 13D/13R Sprinklers & 2" Water Mains',
			'BC Hydro ES54 On-Site Pad-Mounted Transformer (PMT) 3.0m Hot-Stick Clearance (CEC Rule 26-242)',
			'VBBL Zero Emissions Building Plan (ZEBP) Heat-Pump & Balanced HRV Requirements',
		),
		'specs'            => array(
			array( 'title' => 'Part 4 Lateral Shear Wall Framing', 'desc' => 'Simpson Strong-Tie ATS continuous multi-storey tie-down rods solving narrow ground-floor glazing drift in 3–4 storey multiplexes.' ),
			array( 'title' => 'On-Site PMT & 2" Water Civil', 'desc' => 'Early pre-offer verification of whether BC Hydro requires an on-site PMT pad—preventing loss of a rear multiplex unit.' ),
			array( 'title' => 'Built Westside Track Record', 'desc' => 'Proven across Dickinson Residence (Point Grey), West Ridge Property (Dunbar), and Prima Residence (4-storey urban infill).' ),
		),
		'faqs'             => array(
			array( 'q' => 'When does a Vancouver R1-1 multiplex trigger an on-site BC Hydro Pad-Mounted Transformer (PMT)?', 'a' => 'Once combined heat-pump, suite range, and EVEMS loads exceed ~200A–400A overhead pole capacity, BC Hydro frequently mandates an on-site PMT requiring 3.0m front operational clearance under CEC Rule 26-242. We audit this in 48 hours before offer.' ),
			array( 'q' => 'Why do 4-storey multiplexes fail structural lateral shear review?', 'a' => 'Narrow street elevations packed with windows leave minimal solid shear wall width. We integrate engineered steel portal frames and Simpson ATS continuous rod tie-downs early in schematic design.' ),
		),
	),
	'coquitlam'        => array(
		'name'             => 'Coquitlam',
		'kicker'           => 'COQUITLAM BURKE MOUNTAIN & SSMUH MULTIPLEX COMMAND · BILL 44 & TOA',
		'h1'               => 'Coquitlam Custom Homes & Bill 44 3–6 Unit Multiplex Construction.',
		'lead'             => 'Delivering slope-engineered custom residences on Burke Mountain and high-yield 4–6 unit SSMUH multiplexes across Maillardville, Austin Heights, and Transit-Oriented Areas (TOAs) under 100% Open-Book CCDC 5B governance.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.12.46-pm.png',
		'hero_caption'     => 'Multi-Storey Urban Infill & Foothill Civil Engineering Standard',
		'portfolio_filter' => 'vancouver',
		'bylaws'           => array(
			'City of Coquitlam SSMUH Zoning Amendments (3–4 Units Standard, 6 Units Near Frequent Transit)',
			'Burke Mountain Foothill Steep-Slope Geotechnical & Storm Detention Tank Engineering',
			'BCBC 2024 Step Code 4/5, NFPA 13D Fire Suppression & Multi-Meter 400A EVEMS Switchgear',
		),
		'specs'            => array(
			array( 'title' => 'On-Site Storm Retention Chambers', 'desc' => 'Self-performed excavation and civil installation of engineered storm attenuation tanks required on Coquitlam infill lots.' ),
			array( 'title' => 'Repeatable 4–6 Unit Multiplex Framing', 'desc' => 'Dick’s Lumber #52603 5-drop pre-cut framing packages and acoustic party-wall assemblies keeping $/SF tightly controlled.' ),
			array( 'title' => 'Transparent Investor & Owner Draws', 'desc' => 'Every progress draw backed by P.Eng. Schedule B sign-offs and statutory 10% Builders Lien Act holdback tracking.' ),
		),
		'faqs'             => array(
			array( 'q' => 'What civil upgrades are typically required on Coquitlam 4-unit and 6-unit SSMUH lots?', 'a' => 'Coquitlam multiplexes typically require upgraded storm/sanitary service connections, on-site storm detention chambers, 2" domestic water supply for sprinklers, and BC Hydro ES54 underground 400A+ multi-metering.' ),
		),
	),
	'sunshine-coast'   => array(
		'name'             => 'Sunshine Coast',
		'kicker'           => 'SUNSHINE COAST WATERFRONT & GRANITE COMMAND · SECHELT, DAVIS BAY & GIBSONS',
		'h1'               => 'Sunshine Coast Waterfront Custom Homes & Coastal Bedrock Engineering.',
		'lead'             => 'With three completed residences in Sechelt (Piper Residence in Davis Bay, Compass Residence in Trail Bay, and Sullivan Residence in Sandy Hook), Wayne Stevenson (#52603) commands coastal granite pinning, q100 = 0.55 kPa wind-uplift framing, and barged/ferry material logistics.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.43-pm.png',
		'hero_caption'     => 'Piper Residence — Davis Bay, Sechelt (Plus Compass & Sullivan Residences)',
		'portfolio_filter' => 'sunshine-coast',
		'bylaws'           => array(
			'District of Sechelt, Town of Gibsons & SCRD Coastal Foreshore & Geotechnical Hazard DPAs',
			'BCBC Hourly Wind Pressure (q100 = 0.55 kPa) Hurricane Roof Strapping & Marine Fasteners',
			'Self-Performed BC Hydro ES54 Underground DB2 Conduit & Engineered Type 2/3 Septic Civil',
		),
		'specs'            => array(
			array( 'title' => '3 Completed Sechelt Residences', 'desc' => 'Verified local execution across Davis Bay, Trail Bay, and Sandy Hook granite and high-water-table coastal lots.' ),
			array( 'title' => 'Coordinated Multi-Drop Supply Logistics', 'desc' => 'Bundled structural steel, glazing, and 5-drop lumber shipments eliminating piecemeal BC Ferries freight delays.' ),
			array( 'title' => 'Granite Footings & Boulder Retaining', 'desc' => 'Stepped concrete foundations pinned directly to cleared coastal bedrock with heavy boulder sea-breeze retaining structures.' ),
		),
		'faqs'             => array(
			array( 'q' => 'How do you keep Sunshine Coast custom build schedules on track across ferry logistics?', 'a' => 'We pre-consolidate structural lumber, rebar, hardware, and glazing into staged full-load drops off IFC blueprints and self-perform site rock/ES54 civil works before framing crews mobilize.' ),
		),
	),
	'pemberton'        => array(
		'name'             => 'Pemberton',
		'kicker'           => 'PEMBERTON ACREAGE COMPOUNDS & 800A MICROGRIDS · SLRD & BENCHLANDS',
		'h1'               => 'Pemberton Luxury Acreage Compounds, Heavy Timber & 800A Microgrid Civil.',
		'lead'             => 'Engineering multi-structure alpine compounds, equestrian/agricultural estates, and Benchlands custom homes across Pemberton and the SLRD—featuring long-run BC Hydro ES54 primary duct banks, private 800A solar/battery vaults, and deep-frost foundations.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/whistler_luxury_estate.jpg',
		'hero_caption'     => 'Alpine Heavy-Timber, Architectural Concrete & 800A Microgrid Compound Standard',
		'portfolio_filter' => 'whistler',
		'bylaws'           => array(
			'Village of Pemberton & Squamish-Lillooet Regional District (SLRD) Acreage & ALR Compound Bylaws',
			'Valley-Floor Floodplain Elevation Pads & Deep Alpine Frost-Protected Foundations',
			'Long-Run BC Hydro ES54 Primary Duct Banks, Private PMT Vaults & 800A Backup Microgrids',
		),
		'specs'            => array(
			array( 'title' => 'Long-Run ES54 Primary Trenching', 'desc' => 'Self-performed multi-hundred-metre DB2 PVC underground primary feeders, pull vaults, and CEC 26-242 transformer pads.' ),
			array( 'title' => 'Extreme Thermal & Snow Resilience', 'desc' => 'Step Code 5 triple-glazed envelopes engineered for both -22°C winter lows and +38°C Pemberton summer peaks.' ),
			array( 'title' => 'Turnkey Civil + Vertical Build', 'desc' => 'Access roads, domestic wells/cisterns, fire-flow storage, septic fields, and architectural compound framing under one CCDC 5B ledger.' ),
		),
		'faqs'             => array(
			array( 'q' => 'Can Keystone handle long private road, well, and BC Hydro primary trenching on Pemberton acreage?', 'a' => 'Yes. Wayne Stevenson’s 20+ year heavy-civil infrastructure background and BC Hydro ES54 registration allow us to self-perform long primary utility corridors and site access civil works.' ),
		),
	),
	'vancouver-island' => array(
		'name'             => 'Vancouver Island',
		'kicker'           => 'VANCOUVER ISLAND & GREATER VICTORIA · HIGH-SEISMIC OCEANFRONT & SSMUH',
		'h1'               => 'Vancouver Island Oceanfront Estates & High-Seismic Missing-Middle Multiplexes.',
		'lead'             => 'Serving Greater Victoria (Oak Bay, Saanich, Westshore) up to Nanaimo and Parksville—combining high-seismic PGA ductile shear wall engineering, Lewkowich geotechnical bluff anchoring, VRBA quality standards, and Open-Book CCDC 5B transparency.',
		'hero_img'         => 'https://keystonepossibilities.ca/wp-content/uploads/2026/08/vancouver_island_oceanfront_estate_concept.jpg',
		'hero_caption'     => 'Coastal Basalt & Granite Oceanfront Structural Standard — Vancouver Island',
		'portfolio_filter' => 'sunshine-coast',
		'bylaws'           => array(
			'City of Victoria, District of Saanich & Oak Bay Bill 44 Missing-Middle SSMUH Bylaws',
			'BCBC 2024 High-Seismic Spectral Acceleration (PGA > 0.58g) Ductile Shear & Hold-Down Design',
			'Marine Foreshore Development Permit Areas, Salt-Spray 316-Stainless Fasteners & ES54 Civil',
		),
		'specs'            => array(
			array( 'title' => 'High-Seismic Ductile Framing', 'desc' => 'Engineered Simpson ATS rod systems, steel moment frames, and bedrock-dowelled concrete grade beams for Cascadia seismic loads.' ),
			array( 'title' => 'Lewkowich & VRBA Alignment', 'desc' => 'Coordinated geotechnical Schedules B/C-B and transparent 3-bid tendering across vetted Island trade partners.' ),
			array( 'title' => 'Remote Owner 24/7 Portal', 'desc' => 'Real-time milestone photos, signed sub-contracts, and 10% lien holdback tracking for mainland and international landowners.' ),
		),
		'faqs'             => array(
			array( 'q' => 'How do out-of-town landowners monitor a Vancouver Island build?', 'a' => 'Every CCDC 5B owner receives private login credentials to the Keystone Portal featuring daily site logs, dated P.Eng. inspection PDFs, 3-bid trade contracts, and live running-capital tracking.' ),
		),
	),
);

$kp_corr = $kp_corridor_registry[ $kp_corridor_key ];

// Merge any custom fields from Builder 1's kp_get_corridor($slug) if defined while preserving complete fallback keys.
if ( function_exists( 'kp_get_corridor' ) ) {
	$ext_corr = kp_get_corridor( $kp_corridor_key );
	if ( is_array( $ext_corr ) && ! empty( $ext_corr ) ) {
		foreach ( array( 'name', 'h1', 'lead', 'kicker' ) as $str_k ) {
			if ( ! empty( $ext_corr[ $str_k ] ) && is_string( $ext_corr[ $str_k ] ) ) {
				$kp_corr[ $str_k ] = $ext_corr[ $str_k ];
			}
		}
		if ( ! empty( $ext_corr['faqs'] ) && is_array( $ext_corr['faqs'] ) ) {
			$kp_corr['faqs'] = $ext_corr['faqs'];
		}
	}
}

get_header();
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(36px,5.5vw,72px) 0;background:radial-gradient(circle at 80% 15%,rgba(212,175,55,0.12),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:1.12fr 0.88fr;gap:clamp(24px,4vw,44px);align-items:center;" class="kp-corr-hero-grid">
			<style>
				@media (max-width: 960px) { .kp-corr-hero-grid { grid-template-columns: 1fr !important; } }
			</style>
			<div>
				<div style="font-family:'JetBrains Mono',monospace;font-size:0.71rem;font-weight:700;color:#d4af37;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:10px;">
					<?php echo esc_html( $kp_corr['kicker'] ); ?>
				</div>
				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.95rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;">
					<?php echo esc_html( $kp_corr['h1'] ); ?>
				</h1>
				<p style="font-size:0.98rem;line-height:1.65;color:#cbd5e1;margin:0 0 22px;">
					<?php echo esc_html( $kp_corr['lead'] ); ?>
				</p>
				<div style="display:flex;flex-wrap:wrap;gap:12px;">
					<a href="#kp-lead-intake-form" style="display:inline-flex;align-items:center;padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
						Request 48-Hr <?php echo esc_html( $kp_corr['name'] ); ?> Lot Review &rarr;
					</a>
					<a href="#calculator" style="display:inline-flex;align-items:center;padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.44);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.86rem;text-decoration:none;">
						Open <?php echo esc_html( $kp_corr['name'] ); ?> $/SF Console &darr;
					</a>
				</div>
			</div>

			<figure style="margin:0;background:#0a101d;border:1px solid rgba(212,175,55,0.38);border-radius:20px;overflow:hidden;box-shadow:0 26px 60px rgba(0,0,0,0.68);">
				<img
					src="<?php echo esc_url( $kp_corr['hero_img'] ); ?>"
					alt="<?php echo esc_attr( $kp_corr['hero_caption'] ); ?>"
					style="width:100%;aspect-ratio:16/10;object-fit:cover;display:block;"
					fetchpriority="high"
				/>
				<figcaption style="padding:13px 18px;font-size:0.8rem;color:#e2e8f0;border-top:1px solid rgba(212,175,55,0.22);">
					<strong style="color:#d4af37;">Verified Reference:</strong> <?php echo esc_html( $kp_corr['hero_caption'] ); ?>
				</figcaption>
			</figure>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:20px;margin-bottom:28px;">
				<?php foreach ( $kp_corr['specs'] as $sp ) : ?>
					<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.26);border-radius:18px;padding:22px;">
						<h2 style="font-family:'Outfit',sans-serif;font-size:1.12rem;font-weight:700;color:#d4af37;margin:0 0 8px;"><?php echo esc_html( $sp['title'] ); ?></h2>
						<p style="font-size:0.88rem;line-height:1.6;color:#cbd5e1;margin:0;"><?php echo esc_html( $sp['desc'] ); ?></p>
					</article>
				<?php endforeach; ?>
			</div>

			<div style="background:#0a101d;border:1px solid rgba(56,189,248,0.28);border-radius:18px;padding:22px 26px;">
				<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#38bdf8;margin-bottom:10px;">
					2026 MUNICIPAL BYLAW, STRUCTURAL &amp; UTILITY COMPLIANCE CHECKLIST — <?php echo esc_html( strtoupper( $kp_corr['name'] ) ); ?>
				</div>
				<ul style="margin:0;padding-left:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:10px;font-size:0.88rem;color:#e2e8f0;line-height:1.55;">
					<?php foreach ( $kp_corr['bylaws'] as $bl ) : ?>
						<li><?php echo esc_html( $bl ); ?></li>
					<?php endforeach; ?>
				</ul>
			</div>
		</div>
	</section>

	<?php get_template_part( 'template-parts/bill44-calculator', null, array( 'default_corridor' => $kp_corridor_key ) ); ?>

	<?php
	get_template_part(
		'template-parts/portfolio-reel',
		null,
		array(
			'mode'           => 'reel',
			'default_filter' => $kp_corr['portfolio_filter'],
			'heading'        => 'Built Portfolio & Heavy-Civil Execution Highlighted for ' . $kp_corr['name'] . '.',
		)
	);
	?>

	<?php get_template_part( 'template-parts/realtor-rule511-card' ); ?>

	<?php
	get_template_part(
		'template-parts/faq-accordion',
		null,
		array(
			'heading' => $kp_corr['name'] . ' Custom Home, Slope & Multiplex FAQs.',
			'faqs'    => $kp_corr['faqs'],
		)
	);
	?>

	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => $kp_corridor_key ) ); ?>
</main>

<?php
get_footer();
