<?php
/**
 * Keystone Possibilities Child Theme - SEO & ParentOrganization Schema Engine
 * Keystone Empire Network — Master Authority Schema & Footer Cross-Link Mesh
 * 
 * @package KeystonePossibilitiesChild
 * @version 2.5.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// ── 1. Master JSON-LD Schema Injection (Local GEO + ParentOrganization Schema) ──
add_action('wp_head', 'keystone_possibilities_inject_master_schema', 1);
function keystone_possibilities_inject_master_schema() {
    // Only inject on frontend
    if (is_admin()) return;

    $canonical_credentials = array(
        array(
            "@type" => "EducationalOccupationalCredential",
            "name" => "BC Housing Licensed Residential Builder #52603",
            "credentialCategory" => "Professional License",
            "recognizedBy" => array(
                "@type" => "GovernmentOrganization",
                "name" => "BC Housing Licensing and Consumer Services",
                "url" => "https://www.bchousing.org"
            ),
            "url" => "https://lims.bchousing.org/LicenceExpiryPortal/licence/52603"
        ),
        array(
            "@type" => "EducationalOccupationalCredential",
            "name" => "2-5-10 National Home Warranty",
            "credentialCategory" => "Statutory New Home Warranty Protection"
        ),
        array(
            "@type" => "EducationalOccupationalCredential",
            "name" => "BC Hydro Registered Civil Contractor List ES54",
            "credentialCategory" => "Civil Utility Contracting Certification"
        )
    );

    $master_schema = array(
        "@context" => "https://schema.org",
        "@graph" => array(
            // Primary Business Entity
            array(
                "@type" => array("ConstructionBusiness", "GeneralContractor", "HomeAndConstructionBusiness"),
                "@id" => "https://keystonepossibilities.ca/#organization",
                "name" => "Keystone Possibilities Ltd",
                "legalName" => "Keystone Possibilities Ltd.",
                "url" => "https://keystonepossibilities.ca",
                "logo" => array(
                    "@type" => "ImageObject",
                    "@id" => "https://keystonepossibilities.ca/#logo",
                    "url" => "https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png",
                    "contentUrl" => "https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png",
                    "caption" => "Keystone Possibilities Ltd — BC Builder License #52603"
                ),
                "image" => "https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png",
                "description" => "Certified BC Housing Licensed Residential Builder (License #52603) and BC Hydro Civil Utility Contractor (ES54) specializing in start-to-finish luxury custom home construction, 2-5-10 National Home Warranty builds, underground civil infrastructure, and fiduciary CCDC 5B project management across West Vancouver, Whistler, Squamish, North Vancouver, Pemberton, and Vancouver.",
                "telephone" => "+1-604-848-9688",
                "email" => "info@keystonepossibilities.ca",
                "priceRange" => "$$$$",
                "currenciesAccepted" => "CAD",
                "paymentAccepted" => "Bank Transfer, Check, Financing",
                "hasCredential" => $canonical_credentials,
                "identifier" => array(
                    array(
                        "@type" => "PropertyValue",
                        "propertyID" => "BC Housing Licensed Residential Builder",
                        "name" => "BC Housing Builder License",
                        "value" => "52603",
                        "url" => "https://lims.bchousing.org/LicenceExpiryPortal/licence/52603"
                    ),
                    array(
                        "@type" => "PropertyValue",
                        "propertyID" => "BC Hydro Civil Utility Registered Contractor",
                        "name" => "BC Hydro Civil Utility Standard",
                        "value" => "ES54"
                    ),
                    array(
                        "@type" => "PropertyValue",
                        "propertyID" => "Mandatory Home Warranty Protection",
                        "name" => "New Home Warranty Protection",
                        "value" => "2-5-10 National Home Warranty"
                    )
                ),
                "license" => "https://lims.bchousing.org/LicenceExpiryPortal/licence/52603",
                "address" => array(
                    "@type" => "PostalAddress",
                    "streetAddress" => "1 Watts Point Road",
                    "addressLocality" => "Squamish",
                    "addressRegion" => "BC",
                    "postalCode" => "V8B 0B1",
                    "addressCountry" => "CA"
                ),
                "geo" => array(
                    "@type" => "GeoCoordinates",
                    "latitude" => 49.6767,
                    "longitude" => -123.1508
                ),
                "areaServed" => array(
                    array("@type" => "City", "name" => "West Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/West_Vancouver"),
                    array("@type" => "City", "name" => "Whistler", "sameAs" => "https://en.wikipedia.org/wiki/Whistler,_British_Columbia"),
                    array("@type" => "City", "name" => "Squamish", "sameAs" => "https://en.wikipedia.org/wiki/Squamish,_British_Columbia"),
                    array("@type" => "City", "name" => "North Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/North_Vancouver_(city)"),
                    array("@type" => "City", "name" => "Pemberton", "sameAs" => "https://en.wikipedia.org/wiki/Pemberton,_British_Columbia"),
                    array("@type" => "City", "name" => "Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/Vancouver"),
                    array("@type" => "AdministrativeArea", "name" => "British Properties, West Vancouver", "geo" => array("@type" => "GeoCoordinates", "latitude" => 49.3458, "longitude" => -123.1425)),
                    array("@type" => "AdministrativeArea", "name" => "Caulfeild, West Vancouver", "geo" => array("@type" => "GeoCoordinates", "latitude" => 49.3512, "longitude" => -123.2389)),
                    array("@type" => "AdministrativeArea", "name" => "Altamont, West Vancouver", "geo" => array("@type" => "GeoCoordinates", "latitude" => 49.3421, "longitude" => -123.2085)),
                    array("@type" => "AdministrativeArea", "name" => "Dundarave, West Vancouver", "geo" => array("@type" => "GeoCoordinates", "latitude" => 49.3338, "longitude" => -123.1812)),
                    array("@type" => "AdministrativeArea", "name" => "Sunridge Plateau, Whistler", "geo" => array("@type" => "GeoCoordinates", "latitude" => 50.1163, "longitude" => -122.9574)),
                    array("@type" => "AdministrativeArea", "name" => "Kadenwood, Whistler", "geo" => array("@type" => "GeoCoordinates", "latitude" => 50.0987, "longitude" => -122.9754)),
                    array("@type" => "AdministrativeArea", "name" => "Alta Lake, Whistler", "geo" => array("@type" => "GeoCoordinates", "latitude" => 50.1121, "longitude" => -122.9812)),
                    array("@type" => "AdministrativeArea", "name" => "Green Lake, Whistler", "geo" => array("@type" => "GeoCoordinates", "latitude" => 50.1450, "longitude" => -122.9410)),
                    array("@type" => "AdministrativeArea", "name" => "The Heights, Squamish", "geo" => array("@type" => "GeoCoordinates", "latitude" => 49.7350, "longitude" => -123.1320)),
                    array("@type" => "City", "name" => "Lions Bay", "sameAs" => "https://en.wikipedia.org/wiki/Lions_Bay"),
                    array("@type" => "City", "name" => "Britannia Beach", "sameAs" => "https://en.wikipedia.org/wiki/Britannia_Beach")
                ),
                "knowsAbout" => array(
                    "Start-to-Finish Luxury Custom Home Construction (BC Housing License #52603)",
                    "2-5-10 National Home Warranty Protection",
                    "BC Hydro ES54 Civil Underground Ducting and Servicing",
                    "BC Building Code 2024",
                    "BC Energy Step Code 4 and Step Code 5",
                    "Passive House High-Performance Envelopes",
                    "Whistler Alpine Heavy Timber & High Snow Load Engineering",
                    "Granite Bedrock Micropile and Post-Tensioned Rock Anchors",
                    "District of West Vancouver Watercourse Protection Bylaw 4364",
                    "Simpson Strong-Tie ATS Continuous Rod Tie-Down Systems",
                    "High-Seismic Structural Engineering (Sa=0.94g)"
                ),
                "hasOfferCatalog" => array(
                    "@type" => "OfferCatalog",
                    "name" => "Keystone Possibilities Custom Home & Civil Construction Services",
                    "itemListElement" => array(
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Start-to-Finish Luxury Custom Home & Estate Construction",
                                "description" => "Turnkey design-build custom home contracting (BC Housing License #52603) with mandatory 2-5-10 National Home Warranty, Step Code 5 energy performance, and alpine/coastal engineering across West Vancouver, Whistler, Squamish, and North Vancouver."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "BC Hydro Registered Civil Contracting (List ES54)",
                                "description" => "ES54 certified underground utility trenching, 200A–600A+ primary/secondary ducting, pad-mounted transformer (PMT) vaults, civil excavation, and municipal infrastructure connections."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Custom Home & Civil Pre-Construction Cost & Servicing Planning",
                                "description" => "Pre-construction architectural budgeting, geotechnical bedrock review, BC Hydro ES54 civil utility cost modeling, and municipal permit strategy."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Fiduciary Project Management & Owner Representation",
                                "description" => "100% transparent CCDC 5B cost-plus accounting, trade bidding oversight, municipal permit acceleration, and owner advocacy."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Major Custom Renovations, Carriage Homes & Multi-Generational Builds",
                                "description" => "Full-gut structural retrofits, architectural additions, carriage homes, and custom multi-generational builds."
                            )
                        )
                    )
                ),
                "sameAs" => array(
                    "https://www.facebook.com/profile.php?id=61554185128555",
                    "https://www.youtube.com/@KeystonePossibilitiesLtd",
                    "https://www.instagram.com/keystonepossibilities",
                    "https://www.tiktok.com/@keystone.possibil",
                    "https://lims.bchousing.org/LicenceExpiryPortal/licence/52603"
                ),
                "founder" => array(
                    "@type" => "Person",
                    "@id" => "https://keystonepossibilities.ca/#founder",
                    "name" => "Wayne Stevenson",
                    "jobTitle" => "Certified BC Residential Builder & Fiduciary Project Manager",
                    "url" => "https://keystonepossibilities.ca/about-us-general-contractor-squamish/",
                    "sameAs" => array(
                        "https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y",
                        "https://musicbrainz.org/artist/1a30328b-20b2-48bd-8e56-2884d3b040c0",
                        "https://www.musixmatch.com/artist/Wayne-Stevenson",
                        "https://www.youtube.com/@KeyStoneRecomposition",
                        "https://www.youtube.com/@KeystoneAIProtocols",
                        "https://www.youtube.com/@KeystonePossibilitiesLtd",
                        "https://lims.bchousing.org/LicenceExpiryPortal/licence/52603",
                        "https://keystonerecomposition.com/founder/"
                    ),
                    "hasCredential" => $canonical_credentials,
                    "knowsAbout" => array(
                        "Luxury Custom Home Building (BC Housing #52603)",
                        "2-5-10 National Home Warranty Standards",
                        "BC Hydro ES54 Civil Utility Contracting",
                        "Step Code 5 Net-Zero Custom Homes",
                        "Fiduciary CCDC 5B Cost-Plus Project Management",
                        "BC Building Code 2024"
                    )
                )
            ),
            // WebSite Node with SearchAction
            array(
                "@type" => "WebSite",
                "@id" => "https://keystonepossibilities.ca/#website",
                "url" => "https://keystonepossibilities.ca",
                "name" => "Keystone Possibilities Ltd",
                "publisher" => array("@id" => "https://keystonepossibilities.ca/#organization"),
                "potentialAction" => array(
                    "@type" => "SearchAction",
                    "target" => "https://keystonepossibilities.ca/?s={search_term_string}",
                    "query-input" => "required name=search_term_string"
                )
            )
        )
    );

    if (is_front_page()) {
        $master_schema["@graph"][] = array(
            "@type" => "FAQPage",
            "@id" => "https://keystonepossibilities.ca/#faq",
            "mainEntity" => array(
                array(
                    "@type" => "Question",
                    "name" => "How does CCDC 5B Open-Book Construction Management protect my capital better than a fixed-price contract?",
                    "acceptedAnswer" => array(
                        "@type" => "Answer",
                        "text" => "In custom alpine and coastal construction, fixed-price builders embed 18% to 28% hidden risk contingencies into the base price and charge punitive markups on owner selections or geotechnical adjustments. Under CCDC 5B Construction Management, Keystone Possibilities acts as your legally aligned fiduciary: every trade division is competitively tendered to 3 pre-qualified subcontractors, you see raw unedited bids and invoices in our 24/7 Client Portal, 100% of trade discounts are passed directly to you, and you have the contractual option to lock a Guaranteed Maximum Price (GMP) once drawings and rock excavation are finalized."
                    )
                ),
                array(
                    "@type" => "Question",
                    "name" => "Why does hiring a builder who is also a BC Hydro ES54 Registered Civil Contractor save 4–8 months?",
                    "acceptedAnswer" => array(
                        "@type" => "Answer",
                        "text" => "Modern luxury estates with heated driveways, air-to-water heat pump plants, elevators, and multi-EV chargers routinely require 400A to 1200A+ primary power with on-site pad-mounted transformers (PMDFs) or Vista switchgear. Because Keystone Possibilities is a BC Hydro ES54 Registered Civil Contractor, we execute underground primary duct banks (ES54 Section H), concrete transformer pads (Section F), and copper grounding grids (Section R) concurrently with foundation excavation—compressing your critical path by 4 to 8 months."
                    )
                ),
                array(
                    "@type" => "Question",
                    "name" => "How do you achieve BCBC 2024 Step Code 5 & Zero Carbon EL-4 with floor-to-ceiling ocean or mountain glass?",
                    "acceptedAnswer" => array(
                        "@type" => "Answer",
                        "text" => "We integrate Schöck Isokorb structural thermal breaks at all slab cantilevers, specify triple-pane thermally broken European curtain walls positioned inside the continuous exterior mineral-wool insulation plane, and engineer concealed Eccentrically Braced Steel Frames (EBF) that satisfy BC Building Code 2024 Division B Part 4 seismic drift limits (<= 0.025 hs) without obstructing panoramic sightlines."
                    )
                ),
                array(
                    "@type" => "Question",
                    "name" => "Who actually supervises my job site day-to-day?",
                    "acceptedAnswer" => array(
                        "@type" => "Answer",
                        "text" => "We strictly limit our active project volume so founder and licensed Master Builder Wayne Stevenson (BC Housing License #52603) provides direct on-site superintendence across every structural pour, envelope tie-in, and civil utility inspection."
                    )
                )
            )
        );
    }

    echo "\n<!-- Keystone Possibilities 2026 Master Authority Schema -->\n";
    echo '<script type="application/ld+json">' . json_encode($master_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
}

// ── 2. Automatic Google-Compliant VideoObject Schema Injector (Fallback when Rank Math inactive) ──
add_filter('rank_math/snippet/rich_snippet_video', '__return_false');
add_filter('rank_math/schema/video', '__return_empty_array');
add_filter('rank_math/snippet/rich_snippet_videoobject_entity', '__return_false');

add_action('wp_head', 'keystone_possibilities_inject_video_schema', 2);
function keystone_possibilities_inject_video_schema() {
    if (is_admin() || class_exists('RankMath')) return;
    
    global $post;
    if (!$post) return;

    $is_watch_page = ('page' === $post->post_type && 0 === strpos($post->post_name, 'watch-'));
    if (!is_singular('post') && !$is_watch_page) return;

    $post_id = $post->ID;
    if ($is_watch_page) {
        $slug = str_replace('watch-', '', $post->post_name);
        $parent_posts = get_posts(array(
            'name'        => $slug,
            'post_type'   => 'post',
            'post_status' => 'publish',
            'numberposts' => 1
        ));
        if (!empty($parent_posts)) {
            $post_id = $parent_posts[0]->ID;
        }
    }

    $video_id = keystone_possibilities_extract_youtube_id_helper($post_id);
    if (!empty($video_id)) {
        $video_title = get_post_meta($post_id, 'video_title', true);
        if (empty($video_title)) {
            $video_title = wp_strip_all_tags(html_entity_decode(get_the_title($post_id), ENT_QUOTES, 'UTF-8'));
        }

        $video_desc = get_post_meta($post_id, 'video_description', true);
        if (empty($video_desc)) {
            $video_desc = wp_strip_all_tags(html_entity_decode(get_the_excerpt($post_id) ? get_the_excerpt($post_id) : wp_trim_words($post->post_content, 35), ENT_QUOTES, 'UTF-8'));
        }
        if (empty($video_desc)) {
            $video_desc = $video_title . ' - Certified BC Builder #52603 multiplex and construction consulting.';
        }

        $duration_iso = keystone_possibilities_resolve_positive_duration_iso($post_id);
        $upload_date = get_the_date('c', $post_id);

        $video_schema = array(
            "@context" => "https://schema.org",
            "@type" => "VideoObject",
            "@id" => trailingslashit(get_permalink($post_id)) . "#videoobject",
            "name" => $video_title,
            "description" => $video_desc,
            "thumbnailUrl" => array(
                "https://img.youtube.com/vi/{$video_id}/maxresdefault.jpg",
                "https://img.youtube.com/vi/{$video_id}/hqdefault.jpg"
            ),
            "uploadDate" => $upload_date,
            "duration" => $duration_iso,
            "contentUrl" => "https://www.youtube.com/watch?v={$video_id}",
            "embedUrl" => "https://www.youtube-nocookie.com/embed/{$video_id}",
            "inLanguage" => "en-CA",
            "isFamilyFriendly" => true,
            "publisher" => array(
                "@type" => "Organization",
                "@id" => "https://keystonepossibilities.ca/#organization",
                "name" => "Keystone Possibilities Ltd.",
                "logo" => array(
                    "@type" => "ImageObject",
                    "url" => "https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png"
                )
            )
        );
        echo "\n<!-- Keystone Possibilities Dynamic VideoObject Schema -->\n";
        echo '<script type="application/ld+json">' . wp_json_encode($video_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
    }
}

function keystone_possibilities_resolve_positive_duration_iso($post_id) {
    $video_duration = get_post_meta($post_id, 'video_duration', true);
    if (empty($video_duration)) {
        $video_duration = get_post_meta($post_id, 'keystone_video_duration', true);
    }
    $default_iso = 'PT5M30S';
    if (empty($video_duration)) {
        return $default_iso;
    }
    $video_duration = strtoupper(trim((string) $video_duration));
    if (in_array($video_duration, array('0', 'P0D', 'PT0S', 'PT0M', 'PT0M0S', '00:00', '0:00', '00:00:00'), true)) {
        return $default_iso;
    }
    if (strpos($video_duration, 'PT') === 0) {
        if (preg_match('/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/', $video_duration, $m)) {
            $h = !empty($m[1]) ? intval($m[1]) : 0;
            $min = !empty($m[2]) ? intval($m[2]) : 0;
            $s = !empty($m[3]) ? intval($m[3]) : 0;
            if (($h * 3600 + $min * 60 + $s) <= 0) {
                return $default_iso;
            }
            return $video_duration;
        }
        return $default_iso;
    }
    if (is_numeric($video_duration)) {
        $s = intval($video_duration);
        if ($s <= 0) return $default_iso;
        $h = floor($s / 3600);
        $m = floor(($s / 60) % 60);
        $sec = $s % 60;
        return 'PT' . ($h > 0 ? $h . 'H' : '') . ($m > 0 ? $m . 'M' : '') . ($sec > 0 ? $sec . 'S' : '');
    }
    if (preg_match('/^(?:(\d+):)?(\d+):(\d+)$/', $video_duration, $m)) {
        $h = isset($m[1]) && $m[1] !== '' ? intval($m[1]) : 0;
        $min = intval($m[2]);
        $sec = intval($m[3]);
        if (($h * 3600 + $min * 60 + $sec) <= 0) return $default_iso;
        return 'PT' . ($h > 0 ? $h . 'H' : '') . ($min > 0 ? $min . 'M' : '') . ($sec > 0 ? $sec . 'S' : '');
    }
    return $default_iso;
}

// ── 2.5 OpenGraph Video Meta Tags (Google Video Indexing Engine) ─────────────
add_action('wp_head', 'keystone_possibilities_inject_og_video', 5);
function keystone_possibilities_inject_og_video() {
    if (is_admin()) return;
    global $post;
    if (!$post) return;
    $is_watch_page = ('page' === $post->post_type && 0 === strpos($post->post_name, 'watch-'));
    if (!is_singular('post') && !$is_watch_page && !is_singular('page')) return;

    $post_id = $post->ID;
    if ($is_watch_page) {
        $slug = str_replace('watch-', '', $post->post_name);
        $parent_posts = get_posts(array(
            'name'        => $slug,
            'post_type'   => 'post',
            'post_status' => 'publish',
            'numberposts' => 1
        ));
        if (!empty($parent_posts)) {
            $post_id = $parent_posts[0]->ID;
        }
    }

    $youtube_id = get_post_meta($post_id, 'keystone_youtube_id', true);
    if (empty($youtube_id)) {
        $video_url = get_post_meta($post_id, 'video_url', true);
        if (!empty($video_url) && preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $video_url, $m)) {
            $youtube_id = $m[1];
        }
    }
    if (empty($youtube_id)) {
        $content = $post->post_content;
        if (preg_match('/\[keystone_video[^\]]*id=["\']([a-zA-Z0-9_-]{11})["\']/i', $content, $m)) {
            $youtube_id = $m[1];
        } elseif (preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $content, $m)) {
            $youtube_id = $m[1];
        }
    }
    if (empty($youtube_id)) return;

    $embed_url = 'https://www.youtube-nocookie.com/embed/' . esc_attr($youtube_id);
    echo "\n<!-- Keystone Possibilities OpenGraph Video Meta Tags -->\n";
    echo '<meta property="og:video" content="' . $embed_url . '" />' . "\n";
    echo '<meta property="og:video:secure_url" content="' . $embed_url . '" />' . "\n";
    echo '<meta property="og:video:type" content="text/html" />' . "\n";
    echo '<meta property="og:video:width" content="1280" />' . "\n";
    echo '<meta property="og:video:height" content="720" />' . "\n";
    echo '<meta property="ya:ovs:allow_embed" content="true" />' . "\n";
    echo "<!-- End Keystone Possibilities OpenGraph Video -->\n";
}

// ── 2.8 Rank Math Video Sitemap Integration ──────────────────────────────────
add_filter('rank_math/sitemap/video/post', 'keystone_possibilities_rank_math_video_sitemap', 10, 2);
function keystone_possibilities_rank_math_video_sitemap($video, $post_id) {
    if (!is_array($video)) return $video;
    $youtube_id = get_post_meta($post_id, 'keystone_youtube_id', true);
    if (empty($youtube_id)) {
        $p = get_post($post_id);
        if ($p && preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $p->post_content, $m)) {
            $youtube_id = $m[1];
        }
    }
    if (!empty($youtube_id)) {
        $video['thumbnail_loc'] = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
        $video['title']         = get_the_title($post_id);
        $video['player_loc']    = "https://www.youtube-nocookie.com/embed/{$youtube_id}";
        $video['uploader']      = "Keystone Possibilities Ltd.";
        $video['uploader_info'] = "https://keystonepossibilities.ca/";
    }
    return $video;
}

/**
 * Sanitize a single JSON-LD node (Organization / Person / ImageObject) in Rank Math output.
 */
function keystone_possibilities_sanitize_schema_node(&$node) {
    if (!is_array($node)) {
        return;
    }

    $canonical_logo_url = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';
    $canonical_credentials = array(
        array(
            '@type' => 'EducationalOccupationalCredential',
            'name' => 'BC Housing Licensed Residential Builder #52603',
            'credentialCategory' => 'Professional License'
        ),
        array(
            '@type' => 'EducationalOccupationalCredential',
            'name' => '2-5-10 National Home Warranty',
            'credentialCategory' => 'Statutory New Home Warranty Protection'
        ),
        array(
            '@type' => 'EducationalOccupationalCredential',
            'name' => 'BC Hydro Registered Civil Contractor List ES54',
            'credentialCategory' => 'Civil Utility Contracting Certification'
        )
    );
    $canonical_areas = array(
        array('@type' => 'City', 'name' => 'West Vancouver'),
        array('@type' => 'City', 'name' => 'North Vancouver'),
        array('@type' => 'City', 'name' => 'Whistler'),
        array('@type' => 'City', 'name' => 'Squamish'),
        array('@type' => 'City', 'name' => 'Pemberton'),
        array('@type' => 'City', 'name' => 'Vancouver')
    );

    if (isset($node['name']) && $node['name'] === 'Wayne') {
        $node['name'] = 'Wayne Stevenson';
    }

    $types = isset($node['@type']) ? (array) $node['@type'] : array();

    if (in_array('Person', $types, true)) {
        if (empty($node['name']) || $node['name'] === 'Wayne' || stripos($node['name'], 'Wayne') !== false) {
            $node['name'] = 'Wayne Stevenson';
        }
        $node['jobTitle'] = 'Certified BC Residential Builder & Fiduciary Project Manager';
        $node['url'] = 'https://keystonepossibilities.ca/about-us-general-contractor-squamish/';
        $node['hasCredential'] = $canonical_credentials;
        $node['sameAs'] = array(
            'https://www.youtube.com/@KeystonePossibilitiesLtd',
            'https://lims.bchousing.org/LicenceExpiryPortal/licence/52603',
            'https://keystonerecomposition.com/about/'
        );
    }

    if (array_intersect($types, array('Organization', 'LocalBusiness', 'ConstructionBusiness', 'GeneralContractor', 'HomeAndConstructionBusiness'))) {
        $node['@type'] = array('ConstructionBusiness', 'GeneralContractor', 'Organization');
        $node['name'] = 'Keystone Possibilities Ltd';
        $node['legalName'] = 'Keystone Possibilities Ltd.';
        $node['url'] = 'https://keystonepossibilities.ca';
        $node['email'] = 'info@keystonepossibilities.ca';
        $node['telephone'] = '+1-604-848-9688';
        $node['hasCredential'] = $canonical_credentials;
        $node['areaServed'] = $canonical_areas;
        $node['sameAs'] = array(
            'https://www.facebook.com/profile.php?id=61554185128555',
            'https://www.youtube.com/@KeystonePossibilitiesLtd',
            'https://www.instagram.com/keystonepossibilities',
            'https://www.tiktok.com/@keystone.possibil',
            'https://lims.bchousing.org/LicenceExpiryPortal/licence/52603'
        );
        if (isset($node['logo']) && is_array($node['logo'])) {
            $node['logo']['url'] = $canonical_logo_url;
            $node['logo']['contentUrl'] = $canonical_logo_url;
            $node['logo']['caption'] = 'Keystone Possibilities Ltd — BC Builder License #52603';
        } else {
            $node['logo'] = array(
                '@type' => 'ImageObject',
                '@id' => 'https://keystonepossibilities.ca/#logo',
                'url' => $canonical_logo_url,
                'contentUrl' => $canonical_logo_url,
                'caption' => 'Keystone Possibilities Ltd — BC Builder License #52603'
            );
        }
        $node['image'] = $canonical_logo_url;
    }

    if (in_array('ImageObject', $types, true)) {
        if (isset($node['@id']) && strpos($node['@id'], '#logo') !== false) {
            $node['url'] = $canonical_logo_url;
            $node['contentUrl'] = $canonical_logo_url;
            $node['caption'] = 'Keystone Possibilities Ltd — BC Builder License #52603';
        }
    }

    foreach ($node as $k => &$child) {
        if (is_array($child)) {
            keystone_possibilities_sanitize_schema_node($child);
        }
    }
}

// ── 2.9 Google-Compliant Watch Page & VideoObject Schema Injection in Rank Math ────
add_filter('rank_math/json_ld', 'keystone_possibilities_rank_math_watch_page_schema', 999, 2);
function keystone_possibilities_rank_math_watch_page_schema($data, $jsonld) {
    if (!is_array($data) || is_admin()) {
        return $data;
    }

    $canonical_logo_url = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';

    // 1. Sanitize legacy staging URLs, personal emails, screenshot logos, and old handles across ALL pages
    array_walk_recursive($data, function(&$item, $key) use ($canonical_logo_url) {
        if (!is_string($item)) {
            return;
        }
        if (strpos($item, 'staging-a826-keystonepossibilities.wpcomstaging.com') !== false) {
            $item = str_replace('https://staging-a826-keystonepossibilities.wpcomstaging.com', 'https://keystonepossibilities.ca', $item);
        }
        if (strpos($item, 'keystonepossibilities.wordpress.com') !== false) {
            $item = str_replace(
                array('https://keystonepossibilities.wordpress.com', 'http://keystonepossibilities.wordpress.com'),
                'https://keystonepossibilities.ca',
                $item
            );
        }
        if (stripos($item, 'curtis4vancouver@gmail.com') !== false) {
            $item = str_ireplace('curtis4vancouver@gmail.com', 'info@keystonepossibilities.ca', $item);
        }
        if (preg_match('#/@KeystonePossibilities(?!Ltd)#i', $item)) {
            $item = preg_replace('#/@KeystonePossibilities(?!Ltd)#i', '/@KeystonePossibilitiesLtd', $item);
        }
        if (stripos($item, 'screenshot-2023-') !== false || strpos($item, '/wp-content/uploads/logo.png') !== false) {
            $item = $canonical_logo_url;
        }
        if ($key === 'name' && $item === 'Wayne') {
            $item = 'Wayne Stevenson';
        }
    });

    // 2. Enrich & sanitize all Organization and Person nodes in Rank Math graph on ALL pages
    keystone_possibilities_sanitize_schema_node($data);

    global $post;
    if (!$post) return $data;
    $is_watch_page = ('page' === $post->post_type && 0 === strpos((string) $post->post_name, 'watch-'));
    if (!is_singular('post') && !$is_watch_page) {
        return $data;
    }

    $video_id = keystone_possibilities_extract_youtube_id_helper($post);
    if (empty($video_id)) {
        return $data;
    }

    $permalink     = get_permalink($post);
    $video_node_id = trailingslashit($permalink) . '#videoobject';
    $post_title    = wp_strip_all_tags(html_entity_decode(get_the_title($post), ENT_QUOTES, 'UTF-8'));
    $excerpt       = wp_strip_all_tags(html_entity_decode(get_the_excerpt($post), ENT_QUOTES, 'UTF-8'));
    if (empty($excerpt)) {
        $excerpt = wp_trim_words(wp_strip_all_tags(html_entity_decode($post->post_content, ENT_QUOTES, 'UTF-8')), 35, '...');
    }

    // High-res YouTube 16:9 thumbnails (zero Jetpack Photon &#038;ssl=1 corruption)
    $thumbnails = array(
        "https://img.youtube.com/vi/{$video_id}/maxresdefault.jpg",
        "https://img.youtube.com/vi/{$video_id}/hqdefault.jpg"
    );

    $duration_iso = keystone_possibilities_resolve_positive_duration_iso($post->ID);

    // Construct Compliant Single VideoObject Node
    $video_object = array(
        '@type'            => 'VideoObject',
        '@id'              => $video_node_id,
        'name'             => $post_title,
        'description'      => $excerpt,
        'uploadDate'       => get_the_date('c', $post),
        'duration'         => $duration_iso,
        'thumbnailUrl'     => $thumbnails,
        'embedUrl'         => "https://www.youtube-nocookie.com/embed/{$video_id}",
        'contentUrl'       => "https://www.youtube.com/watch?v={$video_id}",
        'inLanguage'       => 'en-CA',
        'isFamilyFriendly' => true,
        'mainEntityOfPage' => array('@id' => $permalink),
        'publisher'        => array('@id' => home_url('/#organization'))
    );

    // Strip any Rank Math auto-detected or custom schema-* VideoObject / duplicate BlogPosting keys
    $seen_article = false;
    foreach (array_keys($data) as $key) {
        if ($key === '@graph' || !is_array($data[$key])) {
            continue;
        }
        $type = isset($data[$key]['@type']) ? (array)$data[$key]['@type'] : array();
        foreach ($type as $t) {
            $tl = strtolower((string)$t);
            if ($tl === 'videoobject') {
                unset($data[$key]);
                break;
            }
            if (in_array($tl, array('article', 'blogposting', 'techarticle', 'newsarticle'), true)) {
                if ($seen_article) {
                    unset($data[$key]);
                } else {
                    $seen_article = true;
                    $data[$key]['author'] = array('@id' => 'https://keystonepossibilities.ca/#founder');
                    $data[$key]['video']  = array('@id' => $video_node_id);
                }
                break;
            }
        }
    }

    // Inject canonical VideoObject directly into Rank Math graph
    $data['VideoObject'] = $video_object;

    if (isset($data['WebPage']) && is_array($data['WebPage'])) {
        $data['WebPage']['video'] = array('@id' => $video_node_id);
    }

    // Also sanitize @graph array if already assembled
    if (isset($data['@graph']) && is_array($data['@graph'])) {
        $clean_graph = array();
        $graph_seen_article = false;
        foreach ($data['@graph'] as $node) {
            $type = isset($node['@type']) ? (array)$node['@type'] : array();
            $types_lower = array_map('strtolower', array_map('strval', $type));
            if (in_array('videoobject', $types_lower, true)) {
                continue; // Strip Rank Math P0D / duplicate VideoObject nodes
            }
            if (array_intersect($types_lower, array('article', 'blogposting', 'techarticle', 'newsarticle'))) {
                if ($graph_seen_article) {
                    continue; // Strip duplicate BlogPosting node
                }
                $graph_seen_article = true;
                $node['author'] = array('@id' => 'https://keystonepossibilities.ca/#founder');
                $node['video']  = array('@id' => $video_node_id);
            }
            if (in_array('webpage', $types_lower, true)) {
                $node['video'] = array('@id' => $video_node_id);
            }
            $clean_graph[] = $node;
        }
        $clean_graph[] = $video_object;
        $data['@graph'] = $clean_graph;
    }

    return $data;
}
add_filter('rank_math/json_ld', 'keystone_possibilities_rank_math_watch_page_schema', 99999, 2);

// ── 3. Keystone Empire Network Standardized Footer Bar (Deprecated / Disabled to prevent duplicate footers) ──
function keystone_possibilities_render_empire_footer() {
    return;
}

// ── 4. Rank Math XML Sitemap Sanitizer & Cache Bypass ────────────────────────
add_filter( 'rank_math/sitemap/enable_caching', '__return_false' );
add_filter( 'rank_math/sitemap/exclude_taxonomy', function( $exclude, $taxonomy ) {
    if ( in_array( $taxonomy, array( 'category', 'post_tag', 'post_format' ), true ) ) {
        return true;
    }
    return $exclude;
}, 10, 2 );

add_filter( 'rank_math/sitemap/entry', function( $url, $type = '', $object = null ) {
    if ( empty( $url ) || ! is_array( $url ) || empty( $url['loc'] ) ) return $url;
    $loc = (string) $url['loc'];
    $excluded_patterns = array(
        '/tag/', '/author/', '/date/', 'sample-page', '/test/', '/demo/', 'wp-admin',
        'locations.kml', 'locations-sitemap', 'category-sitemap', 'post_tag-sitemap',
        '/client-portal-demo/', '/project-management-wp/', '__trashed', '/trash/',
        'purge_all_caches', 'gsc_ping_all', 'keystone_video_sitemap'
    );
    foreach ( $excluded_patterns as $pat ) {
        if ( stripos( $loc, $pat ) !== false ) {
            return false;
        }
    }
    if ( is_object( $object ) && isset( $object->ID ) ) {
        $post_id = (int) $object->ID;
        if ( 'publish' !== get_post_status( $post_id ) ) {
            return false;
        }
        $robots = get_post_meta( $post_id, 'rank_math_robots', true );
        if ( ( is_array( $robots ) && in_array( 'noindex', $robots, true ) ) || ( is_string( $robots ) && stripos( $robots, 'noindex' ) !== false ) ) {
            return false;
        }
        if ( ! empty( get_post_meta( $post_id, 'rank_math_redirection_id', true ) ) || ! empty( get_post_meta( $post_id, 'rank_math_redirection_url', true ) ) ) {
            return false;
        }
    }
    return $url;
}, 10, 3 );

// ── 5. Sanitize robots.txt & Expose AI Crawler Directives (/llms.txt) ─────────
add_filter( 'robots_txt', function( $output, $public ) {
    $custom = "User-agent: *\nDisallow: /wp-admin/\nDisallow: /*?share=\nAllow: /wp-admin/admin-ajax.php\nAllow: /wp-content/uploads/\nAllow: /wp-content/themes/\nAllow: /wp-includes/\n\n# AI Search Engine Crawlers\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: https://keystonepossibilities.ca/sitemap_index.xml\nSitemap: https://keystonepossibilities.ca/keystone-video-sitemap.xml\n";
    return $custom;
}, 99, 2 );

// ── 6. Custom XML Video Sitemap Engine (/keystone-video-sitemap.xml & /video-sitemap.xml) ─
add_action('init', 'keystone_possibilities_register_video_sitemap_rewrite', 5);
function keystone_possibilities_register_video_sitemap_rewrite() {
    if (isset($_GET['keystone_ls_purge'])) {
        header('X-LiteSpeed-Purge: *');
        header('Cache-Control: no-cache, no-store, must-revalidate, max-age=0');
        header('X-LiteSpeed-Cache-Control: no-cache');
        delete_transient('keystone_video_sitemap_xml_cache');
        delete_transient('rank_math_sitemap_cache');
        if (class_exists('\\RankMath\\Sitemap\\Cache')) {
            \RankMath\Sitemap\Cache::invalidate_storage();
        }
        wp_cache_flush();
        status_header(200);
        echo 'KEYSTONE_POSSIBILITIES_CACHE_PURGED_ALL_13_VIDEOS';
        exit;
    }
    add_rewrite_rule('^keystone-video-sitemap\.xml$', 'index.php?keystone_video_sitemap=1', 'top');
    add_rewrite_rule('^video-sitemap\.xml$', 'index.php?keystone_video_sitemap=1', 'top');
}

add_filter('query_vars', 'keystone_possibilities_video_sitemap_query_vars');
function keystone_possibilities_video_sitemap_query_vars($vars) {
    $vars[] = 'keystone_video_sitemap';
    $vars[] = 'video_sitemap';
    return $vars;
}

add_action('template_redirect', 'keystone_possibilities_serve_video_sitemap', 0);
function keystone_possibilities_serve_video_sitemap() {
    $request_uri = $_SERVER['REQUEST_URI'] ?? '';
    if (preg_match('#/(?:keystone-)?video-sitemap(?:[0-9]+)?\.xml(\.gz)?#i', (string) $request_uri) === 1 || get_query_var('keystone_video_sitemap') || get_query_var('video_sitemap') || isset($_GET['keystone_video_sitemap']) || isset($_GET['video_sitemap'])) {
        keystone_possibilities_render_video_sitemap_xml();
        exit;
    }
}

add_filter('rank_math/sitemap/video/content', '__return_empty_string', 999);

function keystone_possibilities_render_video_sitemap_xml() {
    if (!defined('DONOTCACHEPAGE')) define('DONOTCACHEPAGE', true);
    if (!defined('DONOTCACHEDB'))   define('DONOTCACHEDB', true);
    if (!defined('DONOTMINIFY'))    define('DONOTMINIFY', true);

    status_header(200);
    header('Content-Type: application/xml; charset=utf-8');
    header('Cache-Control: no-cache, no-store, must-revalidate, max-age=0');
    header('Pragma: no-cache');
    header('Expires: 0');
    header('X-LiteSpeed-Cache-Control: no-cache');
    header('X-Robots-Tag: index, follow', true);

    echo keystone_possibilities_generate_video_sitemap_markup();
    exit;
}

add_action('save_post', 'keystone_possibilities_invalidate_video_sitemap');
add_action('deleted_post', 'keystone_possibilities_invalidate_video_sitemap');
function keystone_possibilities_invalidate_video_sitemap($post_id) {
    if (wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
        return;
    }
    delete_transient('keystone_video_sitemap_xml_cache');
    delete_transient('rank_math_sitemap_cache');
}

add_filter('rank_math/sitemap/index', 'keystone_possibilities_inject_video_sitemap_into_rank_math', 99);
function keystone_possibilities_inject_video_sitemap_into_rank_math($xml) {
    header('Cache-Control: no-cache, no-store, must-revalidate, max-age=0');
    header('X-LiteSpeed-Cache-Control: no-cache');
    $sitemap_url = esc_url(home_url('/keystone-video-sitemap.xml?v=3'));
    $lastmod = gmdate('Y-m-d\TH:i:s+00:00');

    // Remove any existing keystone-video-sitemap entry before appending fresh v=3 entry
    $xml = preg_replace('/<sitemap>\s*<loc>[^<]*keystone-video-sitemap\.xml[^<]*<\/loc>.*?<\/sitemap>\s*/is', '', (string) $xml);

    $custom_node  = "\t<sitemap>\n";
    $custom_node .= "\t\t<loc>" . $sitemap_url . "</loc>\n";
    $custom_node .= "\t\t<lastmod>" . esc_html($lastmod) . "</lastmod>\n";
    $custom_node .= "\t</sitemap>\n";

    return $xml . $custom_node;
}

function keystone_possibilities_extract_youtube_id_helper($post) {
    if (is_numeric($post)) {
        $post = get_post($post);
    }
    if (!$post) return false;

    $post_id = (int) $post->ID;
    if ('page' === $post->post_type && 0 === strpos((string) $post->post_name, 'watch-')) {
        $meta_id = get_post_meta($post_id, 'keystone_youtube_id', true);
        if (!empty($meta_id) && preg_match('/^[a-zA-Z0-9_-]{11}$/', trim($meta_id))) {
            return trim($meta_id);
        }
        $slug = substr((string) $post->post_name, 6);
        $parent_posts = get_posts(array('name' => $slug, 'post_type' => 'post', 'post_status' => 'publish', 'numberposts' => 1));
        if (!empty($parent_posts)) {
            $post = $parent_posts[0];
            $post_id = (int) $post->ID;
        }
    }

    // Canonical 1-to-1 video mapping for all 6 active @KeystonePossibilitiesLtd episodes (prevents crosslink collisions)
    $default_post_videos = array(
        1953 => 'nPXnGzAEY6k', // BCBC 2024 Luxury Basement Waterproofing, Hydrostatic & Radon Guide
        1907 => 'SIHMOJ5AOyw', // Vancouver Multiplex BCBC 2024 Adaptable Sill & Micropile Guide
        1848 => 'eV_Oo5ekaWc', // Vancouver Multiplex BCBC 2024 Fire Acoustic & 2-Inch Water Main
        1771 => 'kLsNyKvQswg', // West Vancouver Whistler BCBC 2024 Step Code 5 Cantilever Seismic
        1760 => 'kLsNyKvQswg', // Alias ID guard
        1697 => 'JwtaaZlrFeE', // Why 4-Storey Multiplexes Fail Lateral Shear
        1679 => 'ERD0DiVkgYg', // Sea to Sky Luxury Compounds BC Building Code
    );

    if (isset($default_post_videos[$post_id])) {
        return $default_post_videos[$post_id];
    }

    $meta_id = get_post_meta($post_id, 'keystone_youtube_id', true);
    if (!empty($meta_id) && preg_match('/^[a-zA-Z0-9_-]{11}$/', trim($meta_id)) && trim($meta_id) !== 'maxresdefau') {
        return trim($meta_id);
    }

    $video_url = get_post_meta($post_id, 'video_url', true);
    if (!empty($video_url) && preg_match('/(?:youtube(?:-nocookie)?\.com\/(?:[^\/\s]+\/.+\/|(?:v|e(?:mbed)?|shorts)\/|.*[?&]v=)|youtu\.be\/)([\w-]{11})/i', $video_url, $m)) {
        if ($m[1] !== 'maxresdefau') return $m[1];
    }

    $content = (string) $post->post_content;
    if (!empty($content)) {
        if (preg_match('/\[keystone_video[^\]]*id=["\']([a-zA-Z0-9_-]{11})["\']/i', $content, $m)) {
            if ($m[1] !== 'maxresdefau') return $m[1];
        }
        if (preg_match('/youtube-nocookie\.com\/embed\/([a-zA-Z0-9_-]{11})/i', $content, $m)) {
            if ($m[1] !== 'maxresdefau') return $m[1];
        }
        if (preg_match('/(?:youtube\.com\/(?:[^\/\s]+\/.+\/|(?:v|e(?:mbed)?|shorts)\/|.*[?&]v=)|youtu\.be\/)([\w-]{11})/i', $content, $m)) {
            if ($m[1] !== 'maxresdefau') return $m[1];
        }
    }

    return false;
}

// Auto-create dedicated /watch-{slug}/ theater watch page whenever a Possibilities video post is published/updated
add_action('transition_post_status', 'keystone_possibilities_auto_create_watch_page', 10, 3);
function keystone_possibilities_auto_create_watch_page($new_status, $old_status, $post) {
    if ('publish' !== $new_status || 'post' !== $post->post_type) {
        return;
    }
    $youtube_id = keystone_possibilities_extract_youtube_id_helper($post);
    if (empty($youtube_id)) {
        return;
    }
    update_post_meta($post->ID, 'keystone_youtube_id', $youtube_id);
    $post_slug = !empty($post->post_name) ? sanitize_title($post->post_name) : sanitize_title($post->post_title);
    $watch_slug = 'watch-' . $post_slug;
    $blog_permalink = get_permalink($post->ID);
    $clean_title = wp_strip_all_tags(html_entity_decode($post->post_title, ENT_QUOTES, 'UTF-8'));

    $theater_content = '<div class="watch-theater-embed" style="position: relative; width: 100%; max-width: 940px; aspect-ratio: 16 / 9; margin: 0 auto 26px auto; border-radius: 18px; overflow: hidden; border: 1px solid rgba(212, 175, 55, 0.55); box-shadow: 0 22px 50px rgba(0, 0, 0, 0.85); background: #04070d;"><iframe src="https://www.youtube-nocookie.com/embed/' . esc_attr($youtube_id) . '?rel=0&modestbranding=1" title="' . esc_attr($clean_title) . '" style="width: 100%; height: 100%; border: 0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="eager"></iframe></div>' . "\n\n";
    $theater_content .= '<p class="wp-block-paragraph" style="text-align:center; margin-top:28px; margin-bottom:36px;"><a href="' . esc_url($blog_permalink) . '" style="background: linear-gradient(135deg, #f6d365 0%, #d4af37 55%, #aa820a 100%); color: #04070d; padding: 15px 32px; border-radius: 9999px; text-decoration: none; font-weight: 900; display: inline-block; text-transform: uppercase; letter-spacing: 0.06em;">Read the Full BC Builder #52603 Engineering Blueprint &rarr;</a></p>';

    remove_action('transition_post_status', 'keystone_possibilities_auto_create_watch_page', 10);
    $page_by_path = get_page_by_path($watch_slug, OBJECT, 'page');
    if ($page_by_path && !empty($page_by_path->ID)) {
        wp_update_post(array(
            'ID'           => (int) $page_by_path->ID,
            'post_title'   => 'Watch: ' . $clean_title,
            'post_name'    => $watch_slug,
            'post_content' => $theater_content,
            'post_status'  => 'publish',
        ));
        $page_id = (int) $page_by_path->ID;
    } else {
        $page_id = wp_insert_post(array(
            'post_title'   => 'Watch: ' . $clean_title,
            'post_name'    => $watch_slug,
            'post_content' => $theater_content,
            'post_status'  => 'publish',
            'post_type'    => 'page',
            'post_author'  => $post->post_author,
        ));
    }
    if (!is_wp_error($page_id) && $page_id > 0) {
        update_post_meta($page_id, 'keystone_youtube_id', $youtube_id);
    }
    add_action('transition_post_status', 'keystone_possibilities_auto_create_watch_page', 10, 3);
}

function keystone_possibilities_generate_video_sitemap_markup() {
    $posts = get_posts(array(
        'numberposts'      => 100,
        'post_type'        => array('post'),
        'post_status'      => 'publish',
        'orderby'          => 'date',
        'order'            => 'DESC',
        'suppress_filters' => false,
        'no_found_rows'    => true,
    ));

    $entries = array();
    $seen_vids = array();
    $seen_locs = array();

    foreach ($posts as $p) {
        $video_id = keystone_possibilities_extract_youtube_id_helper($p);
        if (!$video_id || isset($seen_vids[$video_id])) {
            continue;
        }

        // Map to dedicated /watch-{slug}/ page if present, else canonical post permalink
        $watch_slug = 'watch-' . $p->post_name;
        $watch_page = get_page_by_path($watch_slug, OBJECT, 'page');
        if ($watch_page && 'publish' === $watch_page->post_status) {
            $loc = esc_url(get_permalink($watch_page->ID));
        } else {
            $loc = esc_url(get_permalink($p->ID));
        }

        if (isset($seen_locs[$loc])) {
            continue;
        }
        $seen_vids[$video_id] = true;
        $seen_locs[$loc]      = true;

        $pub_date = get_the_date('c', $p->ID);
        $thumb    = "https://img.youtube.com/vi/{$video_id}/maxresdefault.jpg";

        $raw_title = get_post_meta($p->ID, 'video_title', true);
        $title     = !empty($raw_title) ? $raw_title : get_the_title($p->ID);
        $title     = htmlspecialchars(wp_strip_all_tags(html_entity_decode($title, ENT_QUOTES, 'UTF-8')), ENT_XML1, 'UTF-8');
        if (mb_strlen($title) > 100) {
            $title = mb_substr($title, 0, 97) . '...';
        }

        $raw_desc = get_post_meta($p->ID, 'video_description', true);
        if (empty($raw_desc)) {
            $raw_desc = get_the_excerpt($p->ID);
        }
        if (empty($raw_desc)) {
            $raw_desc = wp_trim_words($p->post_content, 35);
        }
        $desc = htmlspecialchars(mb_strimwidth(wp_strip_all_tags(html_entity_decode($raw_desc, ENT_QUOTES, 'UTF-8')), 0, 2040, '...'), ENT_XML1, 'UTF-8');

        $entries[] = array(
            'loc'        => $loc,
            'thumb'      => $thumb,
            'title'      => $title,
            'desc'       => $desc,
            'player_loc' => "https://www.youtube-nocookie.com/embed/{$video_id}",
            'pub_date'   => $pub_date,
            'duration'   => 330,
            'video_id'   => $video_id,
        );
    }

    $out  = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    $out .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' . "\n";
    $out .= '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">' . "\n";

    foreach ($entries as $e) {
        $out .= "\t<url>\n";
        $out .= "\t\t<loc>{$e['loc']}</loc>\n";
        $out .= "\t\t<video:video>\n";
        $out .= "\t\t\t<video:thumbnail_loc>{$e['thumb']}</video:thumbnail_loc>\n";
        $out .= "\t\t\t<video:title>{$e['title']}</video:title>\n";
        $out .= "\t\t\t<video:description>{$e['desc']}</video:description>\n";
        $out .= "\t\t\t<video:player_loc allow_embed=\"yes\">{$e['player_loc']}</video:player_loc>\n";
        $out .= "\t\t\t<video:duration>{$e['duration']}</video:duration>\n";
        $out .= "\t\t\t<video:publication_date>{$e['pub_date']}</video:publication_date>\n";
        $out .= "\t\t\t<video:family_friendly>yes</video:family_friendly>\n";
        $out .= "\t\t\t<video:uploader info=\"https://keystonepossibilities.ca/\">Keystone Possibilities Ltd.</video:uploader>\n";
        $out .= "\t\t</video:video>\n";
        $out .= "\t</url>\n";
    }

    $out .= '</urlset>';
    return $out;
}
