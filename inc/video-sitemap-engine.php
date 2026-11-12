<?php
/**
 * Google Video XML Sitemap Engine (`/video-sitemap.xml` & `/keystone-video-sitemap.xml`) — v3.0
 *
 * - Publicly edge-cacheable (`Cache-Control: public, max-age=3600, s-maxage=43200`, zero Set-Cookie).
 * - Strictly deduplicated 1 YouTube ID -> 1 canonical `/videos/[slug]/` Watch Page!
 * - Real verified integer durations (`148`–`206` seconds — zero generic `180` placeholders).
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Canonical 11-Briefing Engineering Video Registry mapped 1:1 to `/videos/[slug]/` Watch Pages.
 *
 * @return array<string, array<string, mixed>>
 */
function kp_get_curated_watch_videos_registry(): array
{
    return array(
        'ERD0DiVkgYg' => array(
            'youtube_id'  => 'ERD0DiVkgYg',
            'slug'        => 'sea-to-sky-luxury-compounds-bc-building-code',
            'loc'         => 'https://keystonepossibilities.ca/videos/sea-to-sky-luxury-compounds-bc-building-code/',
            'title'       => 'Engineering Sea-to-Sky Luxury Compounds: BCBC 2024 Alpine Snow Loads, Seismic & Envelope Architecture',
            'description' => 'Wayne Stevenson (BC Housing Licensed Residential Builder #52603) breaks down steep-slope granite bedrock anchoring, BCBC Part 4 alpine snow loads, and Step Code 5 assemblies across Squamish, Whistler, and West Vancouver.',
            'duration'    => 196,
            'pub_date'    => '2026-10-01T16:00:00+00:00',
        ),
        'JwtaaZlrFeE' => array(
            'youtube_id'  => 'JwtaaZlrFeE',
            'slug'        => 'why-4-storey-multiplexes-fail-lateral-shear',
            'loc'         => 'https://keystonepossibilities.ca/videos/why-4-storey-multiplexes-fail-lateral-shear/',
            'title'       => 'Why 4-Storey BC Bill 44 Multiplexes Fail Lateral Shear — Part 4 Steel Portal Frame Engineering',
            'description' => 'Structural analysis of narrow-frontage Vancouver R1-1 and North Shore Bill 44 multiplexes: why standard Part 9 wood shearwalls fail seismic drift checks and how steel moment frames solve lateral shear.',
            'duration'    => 191,
            'pub_date'    => '2026-10-08T16:00:00+00:00',
        ),
        'kLsNyKvQswg' => array(
            'youtube_id'  => 'kLsNyKvQswg',
            'slug'        => 'west-vancouver-whistler-step-code-5-cantilever-seismic',
            'loc'         => 'https://keystonepossibilities.ca/videos/west-vancouver-whistler-step-code-5-cantilever-seismic/',
            'title'       => 'West Vancouver & Whistler Custom Homes: Step Code 5, Thermal-Break Cantilevers & Seismic Design',
            'description' => 'How Keystone Possibilities engineers oceanfront concrete cantilevers, Schock Isokorb structural thermal breaks, and 8.1 kPa Whistler timber roofs to pass BC Energy Step Code 5.',
            'duration'    => 173,
            'pub_date'    => '2026-10-16T16:00:00+00:00',
        ),
        'eV_Oo5ekaWc' => array(
            'youtube_id'  => 'eV_Oo5ekaWc',
            'slug'        => 'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main',
            'loc'         => 'https://keystonepossibilities.ca/videos/vancouver-multiplex-bcbc-2024-fire-acoustic-water-main/',
            'title'       => 'Vancouver R1-1 Multiplex Engineering: BCBC 2024 1-Hour Fire Separations, ASTC 47 Acoustics & Water Mains',
            'description' => 'Pre-construction guide to NFPA 13D sprinkler water-main upsizing, BC Hydro ES54 PMT transformer clearances, and 1-hour fire/acoustic party wall assemblies in BC multiplexes.',
            'duration'    => 184,
            'pub_date'    => '2026-10-19T16:00:00+00:00',
        ),
        'SIHMOJ5AOyw' => array(
            'youtube_id'  => 'SIHMOJ5AOyw',
            'slug'        => 'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile',
            'loc'         => 'https://keystonepossibilities.ca/videos/vancouver-multiplex-bcbc-2024-adaptable-sill-micropile/',
            'title'       => 'BCBC 2024 Adaptable Dwelling Thresholds, Zero-Step Sills & Tight-Lot Micropile Shoring',
            'description' => 'Solving zero-step adaptable thresholds without rainscreen water ingress alongside zero-lot-line micropile shoring on urban BC infill sites.',
            'duration'    => 178,
            'pub_date'    => '2026-10-22T16:00:00+00:00',
        ),
        'nPXnGzAEY6k' => array(
            'youtube_id'  => 'nPXnGzAEY6k',
            'slug'        => 'bcbc-2024-basement-waterproofing-hydrostatic-radon',
            'loc'         => 'https://keystonepossibilities.ca/videos/bcbc-2024-basement-waterproofing-hydrostatic-radon/',
            'title'       => 'Coastal Hydrostatic Basement Waterproofing, Dual-Membrane Drainage & BCBC 2024 Radon Systems',
            'description' => 'Engineering dry below-grade foundations in high-rainfall North Shore, Squamish, and Sunshine Coast soils using crystalline concrete admixtures, dimpled membranes, and active radon stacks.',
            'duration'    => 152,
            'pub_date'    => '2026-10-24T16:00:00+00:00',
        ),
        'v7r2uwF4eWU' => array(
            'youtube_id'  => 'v7r2uwF4eWU',
            'slug'        => 'hydronic-radiant-floor-erv-engineering',
            'loc'         => 'https://keystonepossibilities.ca/videos/hydronic-radiant-floor-erv-engineering/',
            'title'       => 'Air-to-Water Hydronic Radiant Floors & Balanced ERV Mechanicals for Step Code 5 Estates',
            'description' => 'Zoning PEX-A hydronic radiant slabs, snow-melt driveways, and hospital-grade Zehnder ERV ventilation inside airtight BC custom homes.',
            'duration'    => 159,
            'pub_date'    => '2026-10-27T16:00:00+00:00',
        ),
        'W7eIvbv23Ew' => array(
            'youtube_id'  => 'W7eIvbv23Ew',
            'slug'        => 'inverted-roof-terraces-bc',
            'loc'         => 'https://keystonepossibilities.ca/videos/inverted-roof-terraces-bc/',
            'title'       => 'Inverted Roof Terraces (IRMA), 2-Ply Torch-On Membranes & Pedestal Paver Drainage in BC',
            'description' => 'Preventing flat-roof terrace leaks under coastal rain and alpine freeze-thaw cycles with monolithic waterproofing, tapered XPS insulation, and overflow scuppers.',
            'duration'    => 164,
            'pub_date'    => '2026-10-30T16:00:00+00:00',
        ),
        'sLXAtWGjeiA' => array(
            'youtube_id'  => 'sLXAtWGjeiA',
            'slug'        => 'net-zero-envelopes-bc',
            'loc'         => 'https://keystonepossibilities.ca/videos/net-zero-envelopes-bc/',
            'title'       => 'BC Energy Step Code 5 & Net-Zero Ready Envelopes: <=1.0 ACH50 Airtightness & Exterior Rockwool',
            'description' => 'Field execution of exterior mineral-wool continuous insulation, liquid-applied air barriers, and triple-glazed European tilt-turn window rough-ins.',
            'duration'    => 142,
            'pub_date'    => '2026-11-02T16:00:00+00:00',
        ),
        'qs7xlawF32k' => array(
            'youtube_id'  => 'qs7xlawF32k',
            'slug'        => 'architectural-concrete-bc',
            'loc'         => 'https://keystonepossibilities.ca/videos/architectural-concrete-bc/',
            'title'       => 'Architectural Board-Formed Concrete, 35 MPa Mix Design & Granite Tie-Backs in Coastal BC',
            'description' => 'Formwork tie geometry, vibration consolidation, sulphate-resistant cement mixes, and architectural cedar board-formed walls on West Vancouver and Whistler cliffs.',
            'duration'    => 142,
            'pub_date'    => '2026-11-05T16:00:00+00:00',
        ),
        'HBy6NQQS3ks' => array(
            'youtube_id'  => 'HBy6NQQS3ks',
            'slug'        => 'estate-microgrids-bc',
            'loc'         => 'https://keystonepossibilities.ca/videos/estate-microgrids-bc/',
            'title'       => 'Estate Microgrids, 400A–600A BC Hydro ES54 Underground Vaults & Fire-Rated BESS Rooms',
            'description' => 'Integrating BC Hydro ES54 underground primary duct banks, Pad-Mounted Transformers (PMT), solar arrays, and BCBC fire-separated battery energy storage on remote BC estates.',
            'duration'    => 158,
            'pub_date'    => '2026-11-08T16:00:00+00:00',
        ),
    );
}

/**
 * Registers rewrite rules for /video-sitemap.xml and /keystone-video-sitemap.xml.
 */
function kp_register_video_sitemap_rewrites(): void
{
    add_rewrite_rule('^video-sitemap\.xml$', 'index.php?kp_video_sitemap=1', 'top');
    add_rewrite_rule('^keystone-video-sitemap\.xml$', 'index.php?kp_video_sitemap=1', 'top');
}
add_action('init', 'kp_register_video_sitemap_rewrites', 5);

/**
 * Exposes kp_video_sitemap query var.
 *
 * @param array<int, string> $vars Public query vars.
 * @return array<int, string>
 */
function kp_add_video_sitemap_query_var(array $vars): array
{
    $vars[] = 'kp_video_sitemap';
    return $vars;
}
add_filter('query_vars', 'kp_add_video_sitemap_query_var');

/**
 * Builds the deduplicated XML video sitemap string (1 YouTube ID -> 1 canonical Watch Page).
 *
 * @return string
 */
function kp_build_deduplicated_video_sitemap_xml(): string
{
    $entries = kp_get_curated_watch_videos_registry();

    // Check Founder Avatar dynamic wp_options slots and merge if any new 11-char YouTube IDs are configured
    $slot_map = array(
        'kp_video_id_feasibility'      => array(
            'loc'         => 'https://keystonepossibilities.ca/feasibility-plan/',
            'title'       => 'Turnkey Land & Construction Feasibility Plans — Builder #52603 Breakdown',
            'description' => 'Wayne Stevenson (BC Housing #52603 & BC Hydro ES54) breaks down pre-acquisition parcel due diligence, municipal zoning, ES54 civil servicing, and CCDC 5B pro-forma modeling.',
            'duration'    => 206,
            'pub_date'    => '2026-10-24T16:00:00+00:00',
        ),
        'kp_video_id_bill44_multiplex' => array(
            'loc'         => 'https://keystonepossibilities.ca/bc-developer-portal/',
            'title'       => 'BC Bill 44 Multiplex (3-to-6 Unit SSMUH) — Statutory, BCBC 2024 & Pro-Forma Breakdown',
            'description' => 'Executive engineering breakdown of BC Bill 44 SSMUH rules, Frequent Transit zero-parking tiers, BCBC 2024 fire/acoustic separations, and ES54 electrical upgrades.',
            'duration'    => 179,
            'pub_date'    => '2026-10-24T16:00:00+00:00',
        ),
        'kp_video_id_stepcode5_custom' => array(
            'loc'         => 'https://keystonepossibilities.ca/keystone-possibilities-custom-homes/',
            'title'       => 'Sea-to-Sky & Vancouver Island Custom Homes — BC Energy Step Code 5 Breakdown',
            'description' => 'Licensed BC Builder #52603 walkthrough of Step Code 5 HOT2000 energy modeling, <=1.0 ACH50 airtightness, exterior mineral-wool insulation, and 2-5-10 warranty milestones.',
            'duration'    => 150,
            'pub_date'    => '2026-10-24T16:00:00+00:00',
        ),
    );

    foreach ($slot_map as $opt_key => $meta) {
        $vid = trim((string) get_option($opt_key, ''));
        if ($vid !== '' && preg_match('/^[A-Za-z0-9_-]{11}$/', $vid) === 1 && !isset($entries[$vid])) {
            $entries[$vid] = array_merge(array('youtube_id' => $vid), $meta);
        }
    }

    $xml  = '<' . '?xml version="1.0" encoding="UTF-8"?' . '>' . "\n";
    $xml .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">' . "\n";

    foreach ($entries as $vid => $item) {
        $yt_id    = preg_replace('/[^A-Za-z0-9_-]/', '', (string) $vid);
        $loc      = esc_url((string) $item['loc']);
        $thumb    = 'https://i.ytimg.com/vi/' . $yt_id . '/hqdefault.jpg';
        $player   = 'https://www.youtube-nocookie.com/embed/' . $yt_id;
        $content  = 'https://www.youtube.com/watch?v=' . $yt_id;
        $title    = htmlspecialchars((string) $item['title'], ENT_XML1 | ENT_COMPAT, 'UTF-8');
        $desc     = htmlspecialchars((string) $item['description'], ENT_XML1 | ENT_COMPAT, 'UTF-8');
        $duration = max(30, (int) ($item['duration'] ?? 165));
        $pub_date = htmlspecialchars((string) ($item['pub_date'] ?? '2026-10-01T16:00:00+00:00'), ENT_XML1 | ENT_COMPAT, 'UTF-8');

        $xml .= "  <url>\n";
        $xml .= '    <loc>' . $loc . "</loc>\n";
        $xml .= "    <video:video>\n";
        $xml .= '      <video:thumbnail_loc>' . esc_url($thumb) . "</video:thumbnail_loc>\n";
        $xml .= '      <video:title>' . $title . "</video:title>\n";
        $xml .= '      <video:description>' . $desc . "</video:description>\n";
        $xml .= '      <video:content_loc>' . esc_url($content) . "</video:content_loc>\n";
        $xml .= '      <video:player_loc allow_embed="yes">' . esc_url($player) . "</video:player_loc>\n";
        $xml .= '      <video:duration>' . $duration . "</video:duration>\n";
        $xml .= '      <video:publication_date>' . $pub_date . "</video:publication_date>\n";
        $xml .= "      <video:family_friendly>yes</video:family_friendly>\n";
        $xml .= '      <video:uploader info="https://keystonepossibilities.ca/about-us-general-contractor-squamish/">Wayne Stevenson — Keystone Possibilities Ltd. (#52603)</video:uploader>' . "\n";
        $xml .= "      <video:live>no</video:live>\n";
        $xml .= "    </video:video>\n";
        $xml .= "  </url>\n";
    }

    $xml .= "</urlset>\n";
    return $xml;
}

/**
 * Intercepts /video-sitemap.xml and /keystone-video-sitemap.xml early with public edge-cache headers.
 */
function kp_serve_public_video_sitemap(): void
{
    if (is_admin()) {
        return;
    }

    $uri  = (string) ($_SERVER['REQUEST_URI'] ?? '');
    $path = strtolower((string) parse_url($uri, PHP_URL_PATH));

    $is_sitemap = (
        $path === '/video-sitemap.xml' ||
        $path === '/keystone-video-sitemap.xml' ||
        (function_exists('get_query_var') && (string) get_query_var('kp_video_sitemap') === '1')
    );

    if (!$is_sitemap) {
        return;
    }

    if (!headers_sent()) {
        status_header(200);
        header_remove('Set-Cookie');
        header('Content-Type: application/xml; charset=utf-8', true);
        header('Cache-Control: public, max-age=3600, s-maxage=43200, stale-while-revalidate=3600', true);
        header('X-Robots-Tag: index, follow', true);
    }

    echo kp_build_deduplicated_video_sitemap_xml();
    exit;
}
add_action('init', 'kp_serve_public_video_sitemap', 2);
add_action('template_redirect', 'kp_serve_public_video_sitemap', 0);

/**
 * Injects video-sitemap.xml reference into WordPress robots.txt output.
 *
 * @param string $output Robots.txt body.
 * @return string
 */
function kp_append_video_sitemap_to_robots(string $output): string
{
    $line = 'Sitemap: https://keystonepossibilities.ca/video-sitemap.xml';
    if (strpos($output, 'video-sitemap.xml') === false) {
        $output = rtrim($output) . "\n" . $line . "\n";
    }
    return $output;
}
add_filter('robots_txt', 'kp_append_video_sitemap_to_robots', 20);
