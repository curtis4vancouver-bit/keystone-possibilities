<?php
/**
 * 9-Corridor BC Custom Home, Bill 44 SSMUH & ES54 Civil Engineering Data Registry.
 *
 * Powers Corridor Hub templates, Header/Footer navigation meshes, SEO/GEO JSON-LD
 * Service + FAQPage schemas, and the interactive Lot & Cost Feasibility Estimator.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Returns all 9 British Columbia construction corridors keyed by canonical corridor slug.
 *
 * @return array<string, array<string, mixed>>
 */
function kp_get_corridors(): array
{
    return array(
        'west-vancouver' => array(
            'slug'                   => 'west-vancouver',
            'name'                   => 'West Vancouver Custom Home & Steep-Slope Builder',
            'short_name'             => 'West Vancouver',
            'url'                    => '/west-vancouver-custom-homes/',
            'seo_title'              => 'West Vancouver Custom Home Builder | Steep-Slope & ES54 Civil (#52603)',
            'h1'                     => 'West Vancouver Steep-Slope & Architectural Estate Builder',
            'kicker'                 => 'BRITISH PROPERTIES · CAULFEILD · DUNDARAVE · AMBLESIDE',
            'lead'                   => 'Principal-led custom concrete, steel, and heavy-timber estates engineered for West Vancouver granite cliffs, Watercourse Protection Bylaw No. 4364 setbacks, and self-performed BC Hydro ES54 underground power.',
            'bylaw_summary'          => 'District of West Vancouver Zoning Bylaw No. 4662, Watercourse Protection Bylaw No. 4364 (15m top-of-bank riparian setbacks), Steep Slope Development Permit Area (>30% grade), and Energy Step Code 5 / Zero Carbon EL-4.',
            'geotech_profile'        => 'Exposed Coast Plutonic granite bedrock requiring rock-socketed micropiles, post-tensioned DYWIDAG rock anchors, controlled line-drilling/rock splitting, and perimeter bedrock curtain drainage.',
            'snow_seismic_spec'      => 'High seismic lateral acceleration (Sa(0.2) up to 0.94g) + upper-elevation British Properties ground snow loads (Sg = 2.4–3.6 kPa) with cantilevered structural steel moment frames.',
            'cost_band_sf'           => array(650, 980),
            'es54_note'              => 'Direct BC Hydro ES54 underground 400A–600A primary/secondary duct banks and private Pad-Mounted Transformer (PMT) vaults cut into steep rock driveways without third-party utility bottlenecks.',
            'bill44_rules'           => 'SSMUH 3–4 unit infill permitted on eligible RS zones outside high-hazard geotechnical/wildfire exemptions; luxury coach houses and multi-generational estate compounds predominant.',
            'neighborhoods'          => array(
                'British Properties & Chartwell',
                'Caulfeild & Cypress Park Estates',
                'Altamont & West Bay',
                'Ambleside & Dundarave',
                'Horseshoe Bay & Lions Bay',
            ),
            'featured_project_slugs' => array('ballantree-residence', 'st-andrews-residence', 'dickinson-residence'),
            'faqs'                   => array(
                array(
                    'q' => 'What does a steep-slope custom home cost per square foot in West Vancouver?',
                    'a' => 'Architectural custom residences in West Vancouver typically range from $650 to $980+ per square foot in hard construction costs, driven by granite rock excavation, micropile rock anchors, architectural board-formed concrete, and Step Code 5 triple-glazed glazing.',
                ),
                array(
                    'q' => 'How do you navigate West Vancouver Watercourse Protection Bylaw No. 4364?',
                    'a' => 'As demonstrated on our built Ballantree Residence (5610 Ballantree Rd), we coordinate QEP environmental setbacks, geotechnical Schedule B rock-anchor letters of assurance, and cantilevered steel footprints during pre-construction feasibility.',
                ),
                array(
                    'q' => 'Why does self-performed BC Hydro ES54 civil contracting matter in the British Properties?',
                    'a' => 'Large estates with hydronic snow-melt, EV fleets, elevators, and heat pumps frequently require 400A–600A underground service or a private PMT vault. Holding BC Hydro ES54 civil status in-house eliminates months of utility trenching handoff delays.',
                ),
            ),
            'lat'                    => 49.3286,
            'lng'                    => -123.1602,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/West_Vancouver',
        ),

        'whistler' => array(
            'slug'                   => 'whistler',
            'name'                   => 'Whistler Alpine Custom Home & Chalet Builder',
            'short_name'             => 'Whistler',
            'url'                    => '/whistler-custom-homes/',
            'seo_title'              => 'Whistler Custom Home Builder | 8.1 kPa Alpine Estates & ES54 (#52603)',
            'h1'                     => 'Whistler Ski-In / Ski-Out Alpine Estate & Chalet Builder',
            'kicker'                 => 'SUNRIDGE PLATEAU · KADENWOOD · BLUEBERRY HILL · ALTA VISTA',
            'lead'                   => 'Heavy-timber, architectural stone, and structural steel mountain estates engineered for BCBC Part 4 extreme snow loads (up to 8.1 kPa), RMOW Wildfire DPA Class A envelopes, and short seasonal excavation windows.',
            'bylaw_summary'          => 'Resort Municipality of Whistler (RMOW) Zoning & Parking Bylaw No. 303, Green Building Policy (Step Code 4/5 + Zero Carbon EL-4), and Wildfire Protection Development Permit Area (FireSmart non-combustible cladding/soffits).',
            'geotech_profile'        => 'Glaciated granitic ridges and boulder till requiring controlled rock blasting/splitting, deep frost-protected footings (1.2m+ frost depth), heated snow-melt slab aprons, and bedrock anchor tie-backs.',
            'snow_seismic_spec'      => 'Extreme alpine ground snow loads Sg = 6.2 to 8.1 kPa under BCBC 2024 Part 4 Structural Design, cold-roof ventilated ice-dam prevention assemblies, and heavy glulam/steel point-load connections.',
            'cost_band_sf'           => array(680, 1050),
            'es54_note'              => 'Self-performed BC Hydro ES54 alpine utility trenching, heated driveway glycol manifold preparation, and 400A–600A underground service vaults completed before winter freeze-up.',
            'bill44_rules'           => 'RMOW infill employee/auxiliary residential suite provisions and multi-unit chalet rezonings governed by Gross Floor Area (GFA) exclusions and Whistler Housing Authority covenants.',
            'neighborhoods'          => array(
                'Sunridge Plateau & Brio',
                'Kadenwood & Creekside',
                'Blueberry Hill & Alta Vista',
                'White Gold & Whistler Cay',
                'Nicklaus North & Emerald Estates',
            ),
            'featured_project_slugs' => array('sunridge-residence', 'ballantree-residence', 'civil-john-deere-60g'),
            'faqs'                   => array(
                array(
                    'q' => 'How are Whistler roofs and structures engineered for 6.2 to 8.1 kPa snow loads?',
                    'a' => 'Whistler residences require Part 4 P.Eng. structural design using steel moment frames, heavy glulam ridge beams, bedrock-anchored concrete foundations, and ventilated cold-roof assemblies that prevent eave ice-dam hydrostatic backup.',
                ),
                array(
                    'q' => 'What are RMOW Wildfire Development Permit Area requirements?',
                    'a' => 'RMOW Wildfire DPA rules mandate Class A non-combustible metal or slate roofing, ignition-resistant stone/concrete/metal siding clearances, ember-resistant vents, and non-combustible soffit detailing—all executed on our Sunridge Plateau build.',
                ),
                array(
                    'q' => 'How do you protect schedule certainty with Whistler’s short frost-free excavation season?',
                    'a' => 'Because Keystone self-performs excavation and BC Hydro ES54 civil trenching from our nearby Squamish HQ, we mobilize immediately upon permit issuance so concrete foundations and underground utilities lock before November snowpack.',
                ),
            ),
            'lat'                    => 50.1163,
            'lng'                    => -122.9574,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Whistler,_British_Columbia',
        ),

        'squamish' => array(
            'slug'                   => 'squamish',
            'name'                   => 'Squamish Custom Home, Multiplex & ES54 Civil Builder',
            'short_name'             => 'Squamish (HQ)',
            'url'                    => '/squamish-custom-homes/',
            'seo_title'              => 'Squamish Custom Home Builder & General Contractor | #52603 & ES54',
            'h1'                     => 'Squamish Custom Home, Bill 44 Multiplex & Civil Builder',
            'kicker'                 => 'SQUAMISH HEADQUARTERS · GARIBALDI HIGHLANDS · CRUMPIT WOODS · TANTALUS',
            'lead'                   => 'Headquartered at 1 Watts Point Road in Squamish, Wayne Stevenson delivers direct on-site superintendence for Sea-to-Sky custom homes, Bill 44 3–4 unit multiplexes, Flood Construction Level (FCL) foundations, and ES54 civil servicing.',
            'bylaw_summary'          => 'District of Squamish Zoning Bylaw No. 2200 (SSMUH R-1/R-2 3–4 unit infill), Integrated Flood Hazard Management Plan (FCL elevation compliance), Steep Slopes DPA, and Step Code 4/5 + Zero Carbon EL-4.',
            'geotech_profile'        => 'Two distinct regimes: elevated granite benchlands (Crumpit Woods, Garibaldi Highlands, Tantalus) requiring rock breaking/pinning, and alluvial valley floors (Brackendale, Downtown, Dentville) requiring engineered structural fill and FCL elevation.',
            'snow_seismic_spec'      => 'Coastal-mountain transition snow loads (Sg = 2.6–4.2 kPa), high outflow wind uplift detailing (Howe Sound Squamish winds), and BCBC 2024 high-seismic shearwall hold-downs.',
            'cost_band_sf'           => array(450, 680),
            'es54_note'              => 'Local Squamish civil fleet (1 Watts Point Rd) executing direct BC Hydro ES54 underground service conversions, municipal water/storm tie-ins, and rock trenching with zero mobilization surcharge.',
            'bill44_rules'           => 'Up to 3–4 units permitted as-of-right on serviced residential parcels under District of Squamish SSMUH zoning updates, subject to FCL habitable floor elevations and water/electrical capacity.',
            'neighborhoods'          => array(
                'Garibaldi Highlands & University Heights',
                'Crumpit Woods & Plateau Drive',
                'Tantalus Corridor & Skyridge',
                'Brackendale & Garibaldi Estates',
                'Valleycliffe, Hospital Hill & Britannia Beach',
            ),
            'featured_project_slugs' => array('sunridge-residence', 'civil-john-deere-60g', 'civil-engineered-rebar-slab'),
            'faqs'                   => array(
                array(
                    'q' => 'How do Squamish Flood Construction Levels (FCL) impact foundation design and build cost?',
                    'a' => 'In Brackendale, Garibaldi Estates, and Downtown Squamish, habitable floor elevations must sit above statutory Flood Construction Levels. We engineer compacted structural fill pads, flood-vented garages, and non-buoyant perimeter foundations before architectural framing begins.',
                ),
                array(
                    'q' => 'Can I build a 4-unit Bill 44 multiplex on a residential lot in Squamish?',
                    'a' => 'Yes, most serviced single-family lots outside steep-slope/debris-flow hazard exclusions qualify for 3–4 units. The primary cost drivers are upgrading to a 400A–600A BC Hydro ES54 underground service and sizing domestic/fire water mains.',
                ),
                array(
                    'q' => 'Where is Keystone Possibilities headquartered?',
                    'a' => 'Our headquarters and civil yard are located at 1 Watts Point Road, Squamish, BC V8B 0B1, giving Sea-to-Sky landowners daily principal site supervision by Wayne Stevenson (BC Housing #52603).',
                ),
            ),
            'lat'                    => 49.7016,
            'lng'                    => -123.1558,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Squamish,_British_Columbia',
        ),

        'north-vancouver' => array(
            'slug'                   => 'north-vancouver',
            'name'                   => 'North Vancouver Custom Home & SSMUH Multiplex Builder',
            'short_name'             => 'North Vancouver',
            'url'                    => '/north-vancouver-custom-homes/',
            'seo_title'              => 'North Vancouver Custom Home & Multiplex Builder | #52603 & ES54',
            'h1'                     => 'North Vancouver Custom Homes & 4–6 Unit SSMUH Builder',
            'kicker'                 => 'EDGEMONT VILLAGE · CANYON HEIGHTS · LYNN VALLEY · DEEP COVE · LONSDALE',
            'lead'                   => 'Precision hillside custom residences and Bill 44 Small-Scale Multi-Unit Housing across both the District and City of North Vancouver—combining high-rainfall Step Code 5 envelopes with self-performed ES54 utility upgrades.',
            'bylaw_summary'          => 'District of North Vancouver (DNV) SSMUH 3–6 unit zoning & Creek/Slope Hazard DPAs; City of North Vancouver (CNV) RS-1/RS-2 multiplex + coach house bylaws; Step Code 5 & Zero Carbon Step Plan.',
            'geotech_profile'        => 'Dense glacial till over bedrock canyons with high seasonal water tables (>2,500mm annual North Shore precipitation) demanding dual-membrane waterproofing, sub-slab radon depressurization, and engineered storm detention.',
            'snow_seismic_spec'      => 'High seismic zone (Sa(0.2) ~ 0.90g) requiring BCBC 2024 Part 9.23 / Part 4 portal shear frames on narrow multiplex frontages, plus upper-slope snow load increases above Upper Levels Hwy.',
            'cost_band_sf'           => array(475, 720),
            'es54_note'              => '4–6 unit North Shore multiplexes routinely trigger BC Hydro 400A/600A underground duct banks or pad-mounted transformer (PMT) alcoves—self-performed directly under Keystone ES54 registration.',
            'bill44_rules'           => 'Up to 4 units standard on serviced DNV/CNV lots >280 m², expanding up to 6 units within 400m of prescribed Frequent Transit Network (FTN) bus/SeaBus corridors.',
            'neighborhoods'          => array(
                'Edgemont Village & Canyon Heights',
                'Upper Lonsdale, Central & Lower Lonsdale',
                'Lynn Valley & Braemar',
                'Deep Cove, Indian River & Seymour',
                'Pemberton Heights & Boulevard',
            ),
            'featured_project_slugs' => array('st-andrews-residence', 'ballantree-residence', 'prima-residence'),
            'faqs'                   => array(
                array(
                    'q' => 'What is the difference between District of North Vancouver (DNV) and City of North Vancouver (CNV) multiplex rules?',
                    'a' => 'CNV centers around Higher-density Lonsdale/Grand Boulevard urban lots with streamlined coach house and multiplex massing, while DNV spans larger forested parcels (Edgemont, Lynn Valley, Canyon Heights) where creek setbacks, tree protection bylaws, and slope hazard DPAs govern sited footprints.',
                ),
                array(
                    'q' => 'Why do 4-storey North Shore multiplexes require Part 4 structural steel shear frames?',
                    'a' => 'Narrow infill frontages with garage/window openings lack enough solid wood-frame wall length to resist North Shore seismic shear forces, requiring engineered structural steel moment frames and cast-in-place concrete hold-downs.',
                ),
                array(
                    'q' => 'How do you waterproof basements against North Vancouver’s heavy coastal rainfall?',
                    'a' => 'We install continuous elastomeric waterproofing + dimpled drainage boards tied to rigid PVC perimeter drain lines in washed clear crush, paired with BCBC 2024 sub-slab radon rough-ins and backwater sump protection.',
                ),
            ),
            'lat'                    => 49.3200,
            'lng'                    => -123.0724,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/North_Vancouver_(city)',
        ),

        'vancouver-r1-1' => array(
            'slug'                   => 'vancouver-r1-1',
            'name'                   => 'Vancouver R1-1 Multiplex (3–8 Units) & Luxury Custom Builder',
            'short_name'             => 'Vancouver R1-1',
            'url'                    => '/vancouver-r1-1-multiplex-builder/',
            'seo_title'              => 'Vancouver R1-1 Multiplex Builder (4–8 Units) & Custom Homes | #52603',
            'h1'                     => 'Vancouver R1-1 Multiplex & Westside Custom Residence Builder',
            'kicker'                 => 'R1-1 CITYWIDE MULTIPLEX · POINT GREY · KITSILANO · DUNBAR · KERRISDALE · MAIN',
            'lead'                   => 'Turnkey CCDC 5B execution for City of Vancouver R1-1 3-to-8 unit multiplexes (1.0 FSR) and Point Grey / Dunbar custom estates—solving PMT transformer setbacks, NFPA 13D fire water mains, and zero-emission VBBL envelopes.',
            'bylaw_summary'          => 'City of Vancouver R1-1 District Schedule (up to 1.0 FSR for 3–6 strata multiplexes, or up to 8 secured rental units), Vancouver Building By-law (VBBL 2025), NFPA 13D sprinklers, and acoustic STC 55+ separations.',
            'geotech_profile'        => 'Tight urban 33ft and 50ft infill parcels requiring zero-lot-line excavation shoring, underpinning/neighbor monitoring, arborist root-zone bridging, and sanitary/storm sewer separation upgrades.',
            'snow_seismic_spec'      => 'High-seismic Vancouver coastal zone (Sa(0.2) = 0.94g) with Simpson HTT/HDU cast-in-place hold-downs, 1-hour fire-rated acoustic party walls, and adaptable main-floor dwelling thresholds.',
            'cost_band_sf'           => array(430, 620),
            'es54_note'              => 'R1-1 4–6 unit multiplexes exceeding 200A service capacity require BC Hydro underground dip services or on-lot LPT/PMT transformer pads—engineered and excavated directly by Keystone ES54 crews.',
            'bill44_rules'           => 'R1-1 allows 3–4 units on 33ft lots and up to 6 strata units (or 8 rental units) on 50ft+ lots at 1.0 FSR, subject to Density Bonus / Amenity Share elections and Tree Bylaw retention.',
            'neighborhoods'          => array(
                'Point Grey, Kitsilano & West Point Grey',
                'Dunbar-Southlands, Kerrisdale & Shaughnessy',
                'Mount Pleasant, Cambie Corridor & Riley Park',
                'Trout Lake, Grandview-Woodland & Hastings-Sunrise',
                'Oakridge, Marpole & Arbutus Ridge',
            ),
            'featured_project_slugs' => array('dickinson-residence', 'west-ridge-property', 'prima-residence'),
            'faqs'                   => array(
                array(
                    'q' => 'When does a Vancouver R1-1 multiplex trigger an on-site BC Hydro Pad-Mounted Transformer (PMT)?',
                    'a' => 'When combined heat-pump, EV-ready parking, and multi-suite electrical loads exceed 200A–400A overhead capacity, BC Hydro frequently mandates a 600A underground service or on-property LPT/PMT pad with strict 3m clearance setbacks that must be modeled before DP submission.',
                ),
                array(
                    'q' => 'What water-main upgrade is required for NFPA 13D sprinklers in a Vancouver multiplex?',
                    'a' => 'Existing 3/4-inch lead/copper single-family water lines cannot supply multi-unit domestic demand plus NFPA 13D fire sprinkler flow. R1-1 builds typically require a City of Vancouver 1.5-inch to 2-inch copper/HDPE water service upgrade.',
                ),
                array(
                    'q' => 'How does Open-Book CCDC 5B protect landowner equity on a $2.2M–$3.8M Vancouver multiplex?',
                    'a' => 'Instead of burying 18%–25% speculative contractor markups inside opaque allowances, you see every drywalled, framing, mechanical, and civil trade tender at raw cost with statutory 10% Builders Lien holdbacks.',
                ),
            ),
            'lat'                    => 49.2606,
            'lng'                    => -123.1139,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Vancouver',
        ),

        'coquitlam' => array(
            'slug'                   => 'coquitlam',
            'name'                   => 'Coquitlam & Tri-Cities Custom Home & Bill 44 Multiplex Builder',
            'short_name'             => 'Coquitlam / Tri-Cities',
            'url'                    => '/coquitlam-custom-homes-multiplex/',
            'seo_title'              => 'Coquitlam Custom Home & Multiplex Builder | Burke Mountain & Tri-Cities',
            'h1'                     => 'Coquitlam, Burke Mountain & Tri-Cities Custom & Multiplex Builder',
            'kicker'                 => 'BURKE MOUNTAIN · WESTWOOD PLATEAU · MAILLARDVILLE · PORT MOODY · ANMORE',
            'lead'                   => 'Executive hillside custom homes on Burke Mountain & Anmore acreages and high-yield 4–6 unit SSMUH multiplexes near SkyTrain Transit-Oriented Areas across Coquitlam, Port Moody, and Port Coquitlam.',
            'bylaw_summary'          => 'City of Coquitlam SSMUH RS-zone 3–6 unit amendments, Steep Slopes & Watercourse DPAs on Burke Mountain, Port Moody coastal/hillside guidelines, and BC Energy Step Code 4/5.',
            'geotech_profile'        => 'Glacial till and sandstone/granitic benchlands on Burke Mountain & Westwood Plateau requiring terraced engineered retaining walls and perimeter storm detention tanks; deep marine silts in lower valley pockets.',
            'snow_seismic_spec'      => 'Fraser Valley / Coast Mountain foothill snow loads (Sg = 2.2–3.4 kPa at upper plateau elevations) and BCBC 2024 high-seismic shearwall & hold-down schedules.',
            'cost_band_sf'           => array(420, 610),
            'es54_note'              => 'Direct BC Hydro ES54 underground duct banks for Anmore/Belcarra estate service extensions and Tri-Cities 4–6 unit multiplex 400A/600A meter-stack installations.',
            'bill44_rules'           => '4 units permitted on standard serviced Coquitlam RS lots >280 m², increasing to 6 units with zero residential parking minimums within 400m of SkyTrain / Frequent Transit stops.',
            'neighborhoods'          => array(
                'Burke Mountain & Westwood Plateau',
                'Central Coquitlam, Austin Heights & Maillardville',
                'Burquitlam & Lougheed Transit Corridor',
                'Port Moody, Heritage Mountain & Ioco',
                'Anmore, Belcarra & Port Coquitlam',
            ),
            'featured_project_slugs' => array('st-andrews-residence', 'prima-residence', 'civil-engineered-rebar-slab'),
            'faqs'                   => array(
                array(
                    'q' => 'Which Coquitlam lots qualify for 6 units and zero parking minimums under Bill 44?',
                    'a' => 'Serviced residential parcels over 281 m² located within 400 metres of a prescribed Frequent Bus Stop or outside the immediate SkyTrain TOA tier qualify for up to 6 units with no off-street parking minimums, unlocking significantly cleaner site coverage.',
                ),
                array(
                    'q' => 'What site-servicing costs catch Tri-Cities infill builders off guard?',
                    'a' => 'On-site storm water detention chambers, sanitary sewer main extensions, and BC Hydro 400A underground service trenching are the top three unbudgeted items—all modeled upfront in our 48-Hr Lot & Cost Feasibility Plan.',
                ),
            ),
            'lat'                    => 49.2838,
            'lng'                    => -122.7932,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Coquitlam',
        ),

        'sunshine-coast' => array(
            'slug'                   => 'sunshine-coast',
            'name'                   => 'Sunshine Coast Custom Home Builder — Sechelt & Gibsons',
            'short_name'             => 'Sunshine Coast',
            'url'                    => '/sunshine-coast-custom-homes/',
            'seo_title'              => 'Sunshine Coast Custom Home Builder | Sechelt, Gibsons & Halfmoon Bay',
            'h1'                     => 'Sunshine Coast Waterfront & Coastal Custom Home Builder',
            'kicker'                 => 'SECHELT · DAVIS BAY · HALFMOON BAY · GIBSONS · PENDER HARBOUR',
            'lead'                   => 'Proven Sunshine Coast builder with three completed Sechelt residences (Piper, Compass, and Sullivan)—delivering q100 = 0.55 kPa coastal wind resilience, granite bedrock footings, and BC Hydro ES54 underground power.',
            'bylaw_summary'          => 'District of Sechelt Zoning Bylaw No. 580, Town of Gibsons & SCRD Electoral Area coastal flood/bluff geotechnical setbacks, archaeological chance-find protocols, and BC Energy Step Code 4/5.',
            'geotech_profile'        => 'Exposed coastal granite headlands (Sandy Hook, Halfmoon Bay) paired with high-water-table beach/till terraces (Davis Bay, Trail Bay) requiring elastomeric foundation waterproofing and clear-crush weeping tile.',
            'snow_seismic_spec'      => 'High coastal hourly wind pressures (q100 = 0.55 kPa) requiring continuous roof-to-foundation hurricane uplift strapping, marine-grade stainless fasteners, and BCBC Part 9.27 rainscreens.',
            'cost_band_sf'           => array(440, 660),
            'es54_note'              => 'Self-performed BC Hydro ES54 DB2 PVC underground electrical conduits, boulder retaining walls, and coastal cistern/septic civil coordination across Sechelt and Gibsons.',
            'bill44_rules'           => 'Town of Gibsons and District of Sechelt serviced urban lots permit 3–4 unit SSMUH infill; rural SCRD parcels without municipal water/sewer focus on primary residence + auxiliary cottage.',
            'neighborhoods'          => array(
                'Sechelt, Davis Bay & Trail Bay',
                'Sandy Hook, Tuwanek & Porpoise Bay',
                'Halfmoon Bay & Secret Cove',
                'Gibsons, Roberts Creek & Langdale',
                'Pender Harbour, Madeira Park & Egmont',
            ),
            'featured_project_slugs' => array('piper-residence', 'compass-residence', 'sullivan-residence'),
            'faqs'                   => array(
                array(
                    'q' => 'Has Keystone Possibilities built completed custom homes on the Sunshine Coast?',
                    'a' => 'Yes—Wayne Stevenson built three signature custom residences in Sechelt: the Piper Residence (Davis Bay), Compass Residence (Trail Bay), and Sullivan Residence (Sandy Hook), engineered for coastal wind loads, bedrock footings, and ES54 underground power.',
                ),
                array(
                    'q' => 'How do you manage Langdale barge logistics and Sunshine Coast sub-trade scheduling?',
                    'a' => 'We lock structural lumber, triple-glazed window packages, steel beams, and mechanical equipment on consolidated commercial barge runs early in pre-construction so ferry bottlenecks never stall framing.',
                ),
            ),
            'lat'                    => 49.4742,
            'lng'                    => -123.7545,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Sechelt',
        ),

        'pemberton' => array(
            'slug'                   => 'pemberton',
            'name'                   => 'Pemberton Acreage, Alpine Ranch & Microgrid Estate Builder',
            'short_name'             => 'Pemberton',
            'url'                    => '/pemberton-luxury-builder/',
            'seo_title'              => 'Pemberton Custom Home & Acreage Estate Builder | #52603 & ES54 Civil',
            'h1'                     => 'Pemberton Valley Acreage, Ranch & Off-Grid Microgrid Builder',
            'kicker'                 => 'PEMBERTON MEADOWS · THE RIDGE · SUNSTONE · BIRKEN · SLRD AREA C',
            'lead'                   => 'Architectural valley estates, equestrian/agricultural ALR compounds, and solar/BESS microgrid residences backed by heavy-civil long-run ES54 underground power trenching and extreme temperature-swing Step Code 5 envelopes.',
            'bylaw_summary'          => 'Village of Pemberton Zoning Bylaw No. 832 (Sunstone / The Ridge hillside covenants) and SLRD Electoral Area C / Agricultural Land Reserve (ALR) farm home-plate & floor-area caps.',
            'geotech_profile'        => 'Lillooet River floodplain silts in Pemberton Meadows requiring elevated FCL structural fill pads or driven piles, contrasted with blasted granitic rock benches on Sunstone and The Ridge.',
            'snow_seismic_spec'      => 'Interior-coastal climate extremes (-22°C winter lows to +38°C summer highs), heavy valley snow loads (Sg = 3.8–5.4 kPa), and Wildfire DPA non-combustible exterior claddings.',
            'cost_band_sf'           => array(480, 740),
            'es54_note'              => 'Long-distance 200m–600m+ private BC Hydro ES54 primary duct banks, pad-mounted transformers, deep drilled well tie-ins, and hybrid solar/battery microgrid vaults.',
            'bill44_rules'           => 'Village of Pemberton serviced residential lots support SSMUH infill; SLRD Area C / ALR acreages follow provincial ALR primary + secondary residence rules.',
            'neighborhoods'          => array(
                'Sunstone & The Ridge at Pemberton',
                'Pemberton Meadows & Lillooet River Valley',
                'Pemberton Benchlands & Glen',
                'Mount Currie & Owl Ridge',
                'Birken, Devine & D’Arcy (SLRD Area C)',
            ),
            'featured_project_slugs' => array('sunridge-residence', 'civil-john-deere-60g', 'civil-engineered-rebar-slab'),
            'faqs'                   => array(
                array(
                    'q' => 'What are the ALR home-plate and square-footage rules in Pemberton Meadows?',
                    'a' => 'Agricultural Land Reserve parcels require siting residential structures within a contiguous home-plate setback near road frontage and adhering to provincial/SLRD total floor area thresholds for the principal residence and secondary farm dwelling.',
                ),
                array(
                    'q' => 'Can Keystone trench long-run underground BC Hydro power and microgrid vaults on acreage lots?',
                    'a' => 'Yes. As a BC Hydro Registered Civil Contractor (List ES54), we self-perform long-distance primary/secondary duct trenching, transformer pads, and fire-rated battery backup rooms for remote Pemberton properties.',
                ),
            ),
            'lat'                    => 50.3208,
            'lng'                    => -122.8042,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Pemberton,_British_Columbia',
        ),

        'vancouver-island' => array(
            'slug'                   => 'vancouver-island',
            'name'                   => 'Vancouver Island Custom Home & Fiduciary Builder — Victoria to Tofino',
            'short_name'             => 'Vancouver Island',
            'url'                    => '/vancouver-island-custom-homes/',
            'seo_title'              => 'Vancouver Island Custom Home Builder | Victoria, Nanaimo & Tofino (#52603)',
            'h1'                     => 'Vancouver Island Coastal Estate & SSMUH Fiduciary Builder',
            'kicker'                 => 'OAK BAY · SAANICH · NANAIMO · COMOX VALLEY · PARKSVILLE · TOFINO / UCLEULET',
            'lead'                   => 'Open-book CCDC 5B custom coastal estates and urban Bill 44 multiplexes across Southern, Central, and West Coast Vancouver Island—engineered for Cascadia Subduction Zone seismic resilience and marine storm exposure.',
            'bylaw_summary'          => 'Victoria Missing Middle / Oak Bay & Saanich SSMUH 4–6 unit bylaws, Nanaimo & Courtenay Step Code 4/5 + Zero Carbon rules, and coastal Marine Shoreline / Riparian DPAs.',
            'geotech_profile'        => 'Exposed basalt/granite ocean bluffs in Oak Bay, Nanoose Bay, and Ucluelet requiring rock-anchor foundations, alongside glaciomarine clays in Greater Victoria and Nanaimo worked with Island geotechnical partners.',
            'snow_seismic_spec'      => 'Highest Cascadia Subduction Zone seismic hazard in Canada (Victoria/Tofino Sa(0.2) > 1.1g) plus extreme West Coast wind-driven rain pressures requiring pressure-equalized rainscreen cavities.',
            'cost_band_sf'           => array(460, 760),
            'es54_note'              => 'Turnkey BC Hydro ES54 underground utility servicing, coastal rock trenching, rainwater cistern integration, and backup generator/microgrid transfer infrastructure.',
            'bill44_rules'           => 'Victoria, Saanich, Oak Bay, Nanaimo, and Courtenay serviced lots >280 m² qualify for 3–6 unit SSMUH infill under municipal Bill 44 zoning frameworks.',
            'neighborhoods'          => array(
                'Victoria, Oak Bay, Uplands & Saanich',
                'Sidney, North Saanich & Cowichan Valley',
                'Nanaimo, Lantzville, Parksville & Nanoose Bay',
                'Comox Valley, Courtenay & Crown Isle',
                'Tofino, Ucluelet & West Coast Oceanfront',
            ),
            'featured_project_slugs' => array('ballantree-residence', 'piper-residence', 'compass-residence'),
            'faqs'                   => array(
                array(
                    'q' => 'How does Cascadia Subduction Zone seismic engineering affect Vancouver Island custom homes?',
                    'a' => 'Southern and West Coast Vancouver Island sit in Canada’s peak seismic design tier. Under BCBC 2024, large ocean-view glazing walls require engineered steel portal frames, ductile concrete shear walls, and high-capacity bedrock anchor bolts.',
                ),
                array(
                    'q' => 'Which Vancouver Island engineering partners do you coordinate with?',
                    'a' => 'We collaborate directly with EGBC structural and Island geotechnical specialists—including Lewkowich Engineering Associates and Thurber Engineering—under an open-book CCDC 5B fiduciary model.',
                ),
            ),
            'lat'                    => 48.4284,
            'lng'                    => -123.3656,
            'wiki_url'               => 'https://en.wikipedia.org/wiki/Vancouver_Island',
        ),
    );
}

/**
 * Retrieves a single corridor record by canonical corridor key (e.g. 'west-vancouver', 'vancouver-r1-1')
 * or by its WordPress page slug (e.g. 'west-vancouver-custom-homes', 'vancouver-multiplex-development').
 *
 * @param string $slug Corridor key or WordPress page slug.
 * @return array<string, mixed>|null
 */
function kp_get_corridor(string $slug): ?array
{
    $clean = trim(strtolower($slug), '/');
    $corridors = kp_get_corridors();
    if (isset($corridors[$clean])) {
        return $corridors[$clean];
    }
    foreach ($corridors as $corridor) {
        $url_slug = trim(strtolower((string) ($corridor['url'] ?? '')), '/');
        if ($url_slug !== '' && $url_slug === $clean) {
            return $corridor;
        }
    }
    return null;
}
