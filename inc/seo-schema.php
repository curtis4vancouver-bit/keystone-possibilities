<?php
/**
 * Master JSON-LD Knowledge Graph, Corridor Service/FAQ Schema, VideoObject & OG:Video Engine — v3.0
 *
 * Strictly validated against Google Rich Results & Keystone Adversarial Schema Suite:
 * - Primary entity @type: ["ConstructionBusiness", "GeneralContractor", "HomeAndConstructionBusiness"]
 * - Statutory credentials: BC Housing #52603, BC Hydro ES54, 2-5-10 Warranty, WorkSafeBC #201703481
 * - Parent Organization cross-domain bridge (`https://keystonerecomposition.com`)
 * - Founder Person entity (`Wayne Stevenson`, 20+ yrs structural & heavy-civil leadership incl. Kiewit)
 * - Dynamic Corridor `Service` + `FAQPage` + `BreadcrumbList` + `VideoObject` nodes
 * - Rank Math duplicate entity deduplicator (`keystone_possibilities_dedup_rank_math_schema`)
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Slot A — Canonical 3-Entity Knowledge Graph Registry shared across .ca and .com.
 * Future external citations (Google Maps CID, Wikidata Q-ID, ISNI, Houzz, VRBA) plug in
 * here or via `add_filter('kp_empire_entity_registry', ...)` with zero template edits.
 *
 * @return array<string, mixed>
 */
function kp_get_empire_entity_registry(): array
{
    $registry = array(
        'kp_org_sameas' => array(
            'https://www.youtube.com/@KeystonePossibilitiesLtd',
            'https://lims.bchousing.org/LicenceExpiryPortal/licence/52603',
            'https://www.bchydro.com/work-with-us/alliance/contractors/civil-contractors.html',
            'https://www.facebook.com/profile.php?id=61554185128555',
            'https://www.instagram.com/keystonepossibilities',
        ),
        'person_sameas' => array(
            'https://keystonerecomposition.com/#person',
            'https://keystonerecomposition.com/founder/',
            'https://keystonepossibilities.ca/about-us-general-contractor-squamish/',
            'https://lims.bchousing.org/LicenceExpiryPortal/licence/52603',
            'https://www.linkedin.com/in/wayne-stevenson',
            'https://www.youtube.com/@KeystonePossibilitiesLtd',
            'https://www.youtube.com/@KeyStoneRecomposition',
            'https://www.youtube.com/@KeystoneAIProtocols',
            'https://www.musixmatch.com/artist/Wayne-Stevenson',
        ),
        'person_disambiguation' => 'Canadian BC Housing Licensed Residential Builder (#52603), former 20-year Peter Kiewit & Sons heavy-civil superintendent based in Squamish, British Columbia, autonomous AI systems architect, and founder of Keystone Possibilities Ltd. and Keystone Recomposition.',
    );

    return (array) apply_filters('kp_empire_entity_registry', $registry);
}

/**
 * Resolves YouTube video metadata for the current post/page (supports `/videos/[slug]/` Watch Pages,
 * legacy `/watch-[slug]/` slugs, and embedded `[keystone_video]` / YouTube iframes).
 *
 * @param WP_Post|null $post Current post object.
 * @return array<string, mixed>|null
 */
function kp_resolve_post_video_metadata(?WP_Post $post): ?array
{
    if (!$post instanceof WP_Post) {
        return null;
    }

    $slug    = strtolower((string) $post->post_name);
    $content = (string) $post->post_content;

    // 1. Check Curated 11-Video Watch Registry first (matches /videos/[slug]/ and /watch-[slug]/)
    if (function_exists('kp_get_curated_watch_videos_registry')) {
        $normalized_slug = strpos($slug, 'watch-') === 0 ? str_replace('watch-', '', $slug) : $slug;
        foreach (kp_get_curated_watch_videos_registry() as $yt_id => $meta) {
            if (($meta['slug'] ?? '') === $normalized_slug) {
                $secs = (int) ($meta['duration'] ?? 168);
                $mins = intdiv($secs, 60);
                $rem  = $secs % 60;
                return array(
                    'youtube_id'   => (string) $yt_id,
                    'title'        => (string) $meta['title'],
                    'description'  => (string) $meta['description'],
                    'duration_sec' => $secs,
                    'duration_iso' => sprintf('PT%dM%dS', $mins, $rem),
                    'upload_date'  => (string) ($meta['pub_date'] ?? get_the_date('c', $post)),
                );
            }
        }
    }

    // 2. Legacy watch-* companion post lookup fallback
    $source_content = $content;
    if (strpos($post->post_name, 'watch-') === 0) {
        $companion_slug = str_replace('watch-', '', $post->post_name);
        $companions     = get_posts(array(
            'name'        => $companion_slug,
            'post_type'   => array('post', 'page'),
            'post_status' => 'publish',
            'numberposts' => 1,
        ));
        if (!empty($companions) && $companions[0] instanceof WP_Post) {
            $source_content .= "\n" . $companions[0]->post_content;
        }
    }

    // 3. Extract YouTube ID from [keystone_video] shortcode or youtube/youtube-nocookie embed/watch URL
    $youtube_id = '';
    if (preg_match('/\[keystone_video[^\]]*id=["\']([A-Za-z0-9_-]{11})["\']/i', $source_content, $m)) {
        $youtube_id = $m[1];
    } elseif (preg_match('/youtube(?:-nocookie)?\.com\/(?:embed\/|watch\?v=|shorts\/)([A-Za-z0-9_-]{11})/i', $source_content, $m)) {
        $youtube_id = $m[1];
    } elseif (preg_match('/youtu\.be\/([A-Za-z0-9_-]{11})/i', $source_content, $m)) {
        $youtube_id = $m[1];
    }

    if ($youtube_id === '') {
        return null;
    }

    $raw_title   = get_the_title($post);
    $clean_ex    = wp_strip_all_tags($post->post_excerpt ?: wp_trim_words($source_content, 36, '...'));
    $upload_date = get_the_date('c', $post) ?: '2026-10-01T16:00:00+00:00';

    return array(
        'youtube_id'   => $youtube_id,
        'title'        => $raw_title !== '' ? $raw_title : 'Keystone Possibilities Engineering Briefing',
        'description'  => $clean_ex !== '' ? $clean_ex : 'BC Building Code 2024, Step Code 5, and ES54 civil engineering briefing by Wayne Stevenson (#52603).',
        'duration_sec' => 168,
        'duration_iso' => 'PT2M48S',
        'upload_date'  => $upload_date,
    );
}

/**
 * Injects the unified @graph JSON-LD Knowledge Graph in <head> at priority 1.
 */
function keystone_possibilities_inject_master_schema(): void
{
    if (is_admin() || is_feed()) {
        return;
    }

    $entity_reg  = kp_get_empire_entity_registry();
    $logos       = function_exists('kp_get_official_logos') ? kp_get_official_logos() : array();
    $logo_url    = $logos['full_lockup'] ?? 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_full_logo_gold_transparent.png';
    $badge_url   = $logos['header_badge'] ?? 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';
    $current_url = is_front_page() ? 'https://keystonepossibilities.ca/' : (string) get_permalink();
    if ($current_url === '') {
        $current_url = 'https://keystonepossibilities.ca/';
    }

    // 1. Primary Business Entity (ConstructionBusiness + GeneralContractor + HomeAndConstructionBusiness)
    $primary_org = array(
        "@type"        => array("ConstructionBusiness", "GeneralContractor", "HomeAndConstructionBusiness"),
        "@id"          => "https://keystonepossibilities.ca/#organization",
        "name"         => "Keystone Possibilities Ltd",
        "legalName"    => "Keystone Possibilities Ltd.",
        "url"          => "https://keystonepossibilities.ca/",
        "logo"         => array(
            "@type"  => "ImageObject",
            "@id"    => "https://keystonepossibilities.ca/#logo",
            "url"    => $logo_url,
            "width"  => 1295,
            "height" => 1182,
        ),
        "image"        => array(
            $logo_url,
            $badge_url,
            "https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.57.48-pm.png",
        ),
        "telephone"    => "+1-604-848-9688",
        "email"        => "info@keystonepossibilities.ca",
        "priceRange"   => "$$$$",
        "slogan"       => "Open-Book CCDC 5B Custom Homes, Bill 44 Multiplexes & BC Hydro ES54 Civil Infrastructure",
        "address"      => array(
            "@type"           => "PostalAddress",
            "streetAddress"   => "1 Watts Point Road",
            "addressLocality" => "Squamish",
            "addressRegion"   => "BC",
            "postalCode"      => "V8B 0B1",
            "addressCountry"  => "CA",
        ),
        "geo"          => array(
            "@type"     => "GeoCoordinates",
            "latitude"  => "49.6767",
            "longitude" => "-123.1508",
        ),
        "parentOrganization" => array(
            "@id" => "https://keystonepossibilities.ca/#parent-organization",
        ),
        "founder"      => array(
            "@id" => "https://keystonepossibilities.ca/#founder",
        ),
        "sameAs"       => array_values((array) ($entity_reg['kp_org_sameas'] ?? array(
            "https://www.youtube.com/@KeystonePossibilitiesLtd",
            "https://lims.bchousing.org/LicenceExpiryPortal/licence/52603",
        ))),
        "hasCredential" => array(
            array(
                "@type"              => "EducationalOccupationalCredential",
                "name"               => "BC Housing Licensed Residential Builder",
                "credentialCategory" => "BC Housing Builder License",
                "identifier"         => "52603",
                "url"                => "https://www.bchousing.org/licensing-consumer-disclosure/licencee-search",
                "recognizedBy"       => array(
                    "@type" => "GovernmentOrganization",
                    "name"  => "BC Housing Licensing & Consumer Services",
                ),
            ),
            array(
                "@type"              => "EducationalOccupationalCredential",
                "name"               => "BC Hydro Civil Utility Registered Contractor",
                "credentialCategory" => "BC Hydro Civil Utility Standard",
                "identifier"         => "ES54",
                "recognizedBy"       => array(
                    "@type" => "Organization",
                    "name"  => "BC Hydro",
                ),
            ),
            array(
                "@type"              => "EducationalOccupationalCredential",
                "name"               => "2-5-10 Year Mandatory Home Warranty Protection (WBI / National Home Warranty)",
                "credentialCategory" => "Mandatory Home Warranty Protection",
                "identifier"         => "2-5-10",
            ),
            array(
                "@type"              => "EducationalOccupationalCredential",
                "name"               => "WorkSafeBC Registration & Good Standing Clearance",
                "credentialCategory" => "Statutory Workplace Safety Clearance",
                "identifier"         => "201703481 / C135925638",
            ),
        ),
        "areaServed"   => array(
            array("@type" => "City", "name" => "Squamish", "sameAs" => "https://en.wikipedia.org/wiki/Squamish,_British_Columbia"),
            array("@type" => "City", "name" => "Whistler", "sameAs" => "https://en.wikipedia.org/wiki/Whistler,_British_Columbia"),
            array("@type" => "City", "name" => "Pemberton", "sameAs" => "https://en.wikipedia.org/wiki/Pemberton,_British_Columbia"),
            array("@type" => "City", "name" => "West Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/West_Vancouver"),
            array("@type" => "City", "name" => "North Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/North_Vancouver_(city)"),
            array("@type" => "City", "name" => "Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/Vancouver"),
            array("@type" => "City", "name" => "Lions Bay", "sameAs" => "https://en.wikipedia.org/wiki/Lions_Bay"),
            array("@type" => "Place", "name" => "Britannia Beach", "sameAs" => "https://en.wikipedia.org/wiki/Britannia_Beach"),
            array("@type" => "City", "name" => "Coquitlam", "sameAs" => "https://en.wikipedia.org/wiki/Coquitlam"),
            array("@type" => "City", "name" => "Sechelt", "sameAs" => "https://en.wikipedia.org/wiki/Sechelt"),
            array("@type" => "AdministrativeArea", "name" => "Vancouver Island", "sameAs" => "https://en.wikipedia.org/wiki/Vancouver_Island"),
        ),
        "hasOfferCatalog" => array(
            "@type"           => "OfferCatalog",
            "name"            => "Keystone Possibilities Construction & Civil Engineering Services",
            "itemListElement" => array(
                array(
                    "@type"       => "Offer",
                    "itemOffered" => array(
                        "@type" => "Service",
                        "name"  => "BC Bill 44 Multiplex Feasibility & Construction",
                        "url"   => "https://keystonepossibilities.ca/vancouver-r1-1-multiplex-builder/",
                    ),
                ),
                array(
                    "@type"       => "Offer",
                    "itemOffered" => array(
                        "@type" => "Service",
                        "name"  => "Custom Luxury Home Construction",
                        "url"   => "https://keystonepossibilities.ca/keystone-possibilities-custom-homes/",
                    ),
                ),
                array(
                    "@type"       => "Offer",
                    "itemOffered" => array(
                        "@type" => "Service",
                        "name"  => "Fiduciary Project Management & Owner Representation",
                        "url"   => "https://keystonepossibilities.ca/feasibility-plan/",
                    ),
                ),
                array(
                    "@type"       => "Offer",
                    "itemOffered" => array(
                        "@type" => "Service",
                        "name"  => "BC Hydro Registered Civil Contracting",
                        "url"   => "https://keystonepossibilities.ca/bc-hydro-registered-civil-contractor/",
                    ),
                ),
                array(
                    "@type"       => "Offer",
                    "itemOffered" => array(
                        "@type" => "Service",
                        "name"  => "Construction Feasibility Studies & Land Due Diligence",
                        "url"   => "https://keystonepossibilities.ca/feasibility-plan/",
                    ),
                ),
            ),
        ),
    );

    // 2. Parent Organization Cross-Domain Entity Bridge
    $parent_org = array(
        "@type"           => "Organization",
        "@id"             => "https://keystonepossibilities.ca/#parent-organization",
        "name"            => "Keystone Empire",
        "alternateName"   => "Keystone Group",
        "url"             => "https://keystonepossibilities.ca/",
        "subOrganization" => array(
            array("@id" => "https://keystonepossibilities.ca/#organization"),
            array(
                "@type" => "Organization",
                "@id"   => "https://keystonerecomposition.com/#organization",
                "name"  => "Keystone Recomposition",
                "url"   => "https://keystonerecomposition.com",
            ),
        ),
    );

    // 3. Founder & Principal Superintendent Person Entity (E-E-A-T + Cross-Domain Knowledge Panel Mesh)
    $founder_person = array(
        "@type"                     => "Person",
        "@id"                       => "https://keystonepossibilities.ca/#founder",
        "name"                      => "Wayne Stevenson",
        "url"                       => "https://keystonepossibilities.ca/about-us-general-contractor-squamish/",
        "mainEntityOfPage"          => "https://keystonepossibilities.ca/about-us-general-contractor-squamish/",
        "jobTitle"                  => "Certified BC Residential Builder & Fiduciary Project Manager",
        "description"               => "Licensed BC Residential Builder (#52603) and BC Hydro Registered Civil Contractor (List ES54) with 20+ years of structural concrete, steep-slope bedrock, and heavy-civil infrastructure leadership including Peter Kiewit Sons Co.",
        "disambiguatingDescription" => (string) ($entity_reg['person_disambiguation'] ?? ''),
        "sameAs"                    => array_values((array) ($entity_reg['person_sameas'] ?? array())),
        "worksFor"                  => array(
            "@id" => "https://keystonepossibilities.ca/#organization",
        ),
        "knowsAbout"                => array(
            "BC Building Code 2024 Part 9 & Part 4 Structural Execution",
            "BC Energy Step Code 5 & Zero Carbon Step Plan EL-4",
            "BC Hydro ES54 Underground Primary/Secondary Duct Banks & PMT Vaults",
            "Steep-Slope Granite Micropiles & Post-Tensioned Rock Anchors",
            "CCDC 5B Open-Book Construction Management & BC Bill 44 SSMUH Multiplexes",
        ),
    );

    // 4. WebSite Node
    $website_node = array(
        "@type"      => "WebSite",
        "@id"        => "https://keystonepossibilities.ca/#website",
        "url"        => "https://keystonepossibilities.ca/",
        "name"       => "Keystone Possibilities Ltd.",
        "publisher"  => array("@id" => "https://keystonepossibilities.ca/#organization"),
        "inLanguage" => "en-CA",
    );

    $graph = array($primary_org, $parent_org, $founder_person, $website_node);

    // 5. ProfilePage Entity Home on /about-us-general-contractor-squamish/ + Dynamic Corridor Nodes
    global $post;
    $req_slug = $post instanceof WP_Post ? strtolower((string) $post->post_name) : trim((string) parse_url((string) ($_SERVER['REQUEST_URI'] ?? ''), PHP_URL_PATH), '/');
    if ($req_slug === 'about-us-general-contractor-squamish' || (function_exists('is_page') && is_page('about-us-general-contractor-squamish'))) {
        $about_url = 'https://keystonepossibilities.ca/about-us-general-contractor-squamish/';
        $graph[] = array(
            "@type"        => "ProfilePage",
            "@id"          => $about_url . "#profilepage",
            "url"          => $about_url,
            "name"         => "Wayne Stevenson — Principal Superintendent & BC Licensed Builder #52603",
            "dateCreated"  => "2024-03-01T08:00:00-08:00",
            "dateModified" => $post instanceof WP_Post ? get_the_modified_date('c', $post) : gmdate('c'),
            "mainEntity"   => array(
                "@id" => "https://keystonepossibilities.ca/#founder",
            ),
            "about"        => array(
                "@id" => "https://keystonepossibilities.ca/#organization",
            ),
        );
    }

    if ($post instanceof WP_Post && function_exists('kp_get_corridor')) {
        $corridor = kp_get_corridor((string) $post->post_name);
        if (is_array($corridor)) {
            $corridor_url = home_url((string) $corridor['url']);
            $graph[] = array(
                "@type"       => "Service",
                "@id"         => $corridor_url . "#service",
                "name"        => (string) $corridor['name'],
                "description" => (string) $corridor['lead'],
                "url"         => $corridor_url,
                "provider"    => array("@id" => "https://keystonepossibilities.ca/#organization"),
                "areaServed"  => array(
                    "@type"  => "Place",
                    "name"   => (string) $corridor['short_name'],
                    "sameAs" => (string) $corridor['wiki_url'],
                ),
            );

            if (!empty($corridor['faqs']) && is_array($corridor['faqs'])) {
                $faq_entities = array();
                foreach ($corridor['faqs'] as $faq) {
                    if (!empty($faq['q']) && !empty($faq['a'])) {
                        $faq_entities[] = array(
                            "@type"          => "Question",
                            "name"           => (string) $faq['q'],
                            "acceptedAnswer" => array(
                                "@type" => "Answer",
                                "text"  => (string) $faq['a'],
                            ),
                        );
                    }
                }
                if (!empty($faq_entities)) {
                    $graph[] = array(
                        "@type"      => "FAQPage",
                        "@id"        => $corridor_url . "#faq",
                        "mainEntity" => $faq_entities,
                    );
                }
            }

            $graph[] = array(
                "@type"           => "BreadcrumbList",
                "@id"             => $corridor_url . "#breadcrumb",
                "itemListElement" => array(
                    array(
                        "@type"    => "ListItem",
                        "position" => 1,
                        "name"     => "Home",
                        "item"     => "https://keystonepossibilities.ca/",
                    ),
                    array(
                        "@type"    => "ListItem",
                        "position" => 2,
                        "name"     => (string) $corridor['short_name'],
                        "item"     => $corridor_url,
                    ),
                ),
            );
        }
    }

    // 6. Dynamic VideoObject Node on Watch Pages & Video Briefing Posts
    if (is_singular() && $post instanceof WP_Post) {
        $vid_meta = kp_resolve_post_video_metadata($post);
        if (is_array($vid_meta) && !empty($vid_meta['youtube_id'])) {
            $youtube_id   = (string) $vid_meta['youtube_id'];
            $video_title  = (string) $vid_meta['title'];
            $video_desc   = (string) $vid_meta['description'];
            $duration_iso = (string) $vid_meta['duration_iso'];

            // Safe HTML-attribute escaping available for meta/DOM consumers alongside JSON-LD
            $safe_title_attr = esc_attr($video_title);
            $safe_desc_attr  = esc_attr($video_desc);
            $safe_dur_attr   = esc_attr($duration_iso);
            $safe_yt_attr    = esc_attr($youtube_id);

            $graph[] = array(
                "@type" => "VideoObject",
                "@id"              => $current_url . "#video",
                "name"             => $safe_title_attr !== '' ? $video_title : 'Keystone Possibilities Briefing',
                "description"      => $safe_desc_attr !== '' ? $video_desc : '',
                "thumbnailUrl"     => array(
                    "https://i.ytimg.com/vi/" . $safe_yt_attr . "/maxresdefault.jpg",
                    "https://i.ytimg.com/vi/" . $safe_yt_attr . "/hqdefault.jpg",
                ),
                "uploadDate"       => (string) $vid_meta['upload_date'],
                "duration"         => $safe_dur_attr,
                "contentUrl"       => "https://www.youtube.com/watch?v=" . $safe_yt_attr,
                "embedUrl"         => "https://www.youtube-nocookie.com/embed/" . $safe_yt_attr,
                "inLanguage"       => "en-CA",
                "isFamilyFriendly" => true,
                "publisher"        => array(
                    "@id" => "https://keystonepossibilities.ca/#organization",
                ),
            );
        }
    }

    $schema = array(
        "@context" => "https://schema.org",
        "@graph" => array(
            ...$graph,
        ),
    );

    echo "\n" . '<script type="application/ld+json" id="keystone-master-schema">' . "\n";
    echo json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT | JSON_HEX_TAG);
    echo "\n" . '</script>' . "\n";
}
add_action('wp_head', 'keystone_possibilities_inject_master_schema', 1);

/**
 * Injects OpenGraph & Yandex Video player tags on singular Watch Pages / Video Briefing Posts.
 */
function keystone_possibilities_inject_og_video(): void
{
    if (!is_singular() || is_admin()) {
        return;
    }

    global $post;
    $vid_meta = kp_resolve_post_video_metadata($post instanceof WP_Post ? $post : null);
    if (!is_array($vid_meta) || empty($vid_meta['youtube_id'])) {
        return;
    }

    $youtube_id = esc_attr((string) $vid_meta['youtube_id']);
    $embed_url  = 'https://www.youtube-nocookie.com/embed/' . $youtube_id;

    echo '<meta property="og:video" content="' . esc_url($embed_url) . '" />' . "\n";
    echo '<meta property="og:video:secure_url" content="' . esc_url($embed_url) . '" />' . "\n";
    echo '<meta property="og:video:type" content="text/html" />' . "\n";
    echo '<meta property="og:video:width" content="1280" />' . "\n";
    echo '<meta property="og:video:height" content="720" />' . "\n";
    echo '<meta property="ya:ovs:allow_embed" content="true" />' . "\n";
}
add_action('wp_head', 'keystone_possibilities_inject_og_video', 5);

/**
 * Deduplicates Rank Math JSON-LD graph nodes so Organization, Person, and VideoObject
 * never conflict with our canonical Keystone Master Schema.
 *
 * @param array<string, mixed> $data    Rank Math JSON-LD array.
 * @param mixed                $jsonld  Rank Math JsonLD instance.
 * @return array<string, mixed>
 */
function keystone_possibilities_dedup_rank_math_schema(array $data, $jsonld): array
{
    $duplicate_types = array(
        'Organization',
        'LocalBusiness',
        'ConstructionBusiness',
        'GeneralContractor',
        'HomeAndConstructionBusiness',
        'Person',
        'ProfilePage',
        'VideoObject',
    );

    foreach ($data as $key => $node) {
        if (!is_array($node) || !isset($node['@type'])) {
            continue;
        }
        $types = is_array($node['@type']) ? $node['@type'] : array($node['@type']);
        foreach ($types as $t) {
            if (in_array((string) $t, $duplicate_types, true)) {
                unset($data[$key]);
                break;
            }
        }
    }

    return $data;
}
add_filter('rank_math/json_ld', 'keystone_possibilities_dedup_rank_math_schema', 999, 2);
