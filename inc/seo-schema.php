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
                    "url" => "https://keystonepossibilities.ca/wp-content/uploads/logo.png",
                    "contentUrl" => "https://keystonepossibilities.ca/wp-content/uploads/logo.png",
                    "caption" => "Keystone Possibilities Ltd — BC Builder License #52603"
                ),
                "image" => "https://keystonepossibilities.ca/wp-content/uploads/logo.png",
                "description" => "Certified BC Housing Licensed Residential Builder (License #52603) and BC Hydro Civil Utility Contractor (ES54) specializing in BC Bill 44 multiplex conversions, custom luxury estate construction, and fiduciary project management across Squamish, Whistler, Pemberton, West Vancouver, and North Vancouver.",
                "telephone" => "+1-604-848-9688",
                "email" => "info@keystonepossibilities.ca",
                "priceRange" => "$$$$",
                "currenciesAccepted" => "CAD",
                "paymentAccepted" => "Bank Transfer, Check, Financing",
                "parentOrganization" => array(
                    "@type" => "Organization",
                    "@id" => "https://keystonepossibilities.ca/#parent-organization",
                    "name" => "Keystone Empire",
                    "alternateName" => "Keystone Group",
                    "url" => "https://keystonepossibilities.ca",
                    "description" => "Master parent organization network governing Keystone Possibilities Ltd. and Keystone Recomposition.",
                    "subOrganization" => array(
                        array(
                            "@type" => "Organization",
                            "@id" => "https://keystonepossibilities.ca/#organization",
                            "name" => "Keystone Possibilities Ltd.",
                            "url" => "https://keystonepossibilities.ca"
                        ),
                        array(
                            "@type" => "Organization",
                            "@id" => "https://keystonerecomposition.com/#organization",
                            "name" => "Keystone Recomposition",
                            "url" => "https://keystonerecomposition.com"
                        )
                    ),
                    "sameAs" => array(
                        "https://keystonepossibilities.ca",
                        "https://keystonerecomposition.com"
                    )
                ),
                "identifier" => array(
                    array(
                        "@type" => "PropertyValue",
                        "propertyID" => "BC Housing Licensed Residential Builder",
                        "name" => "BC Housing Builder License",
                        "value" => "52603",
                        "url" => "https://www.bchousing.org/licensing-consumer-disclosure/licencee-search"
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
                        "value" => "2-5-10 Year Mandatory Home Warranty Protection (WBI / National Home Warranty)"
                    )
                ),
                "license" => "https://www.bchousing.org/licensing-consumer-disclosure/licencee-search",
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
                    array("@type" => "City", "name" => "Squamish", "sameAs" => "https://en.wikipedia.org/wiki/Squamish,_British_Columbia"),
                    array("@type" => "City", "name" => "Whistler", "sameAs" => "https://en.wikipedia.org/wiki/Whistler,_British_Columbia"),
                    array("@type" => "City", "name" => "West Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/West_Vancouver"),
                    array("@type" => "City", "name" => "North Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/North_Vancouver_(city)"),
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
                    array("@type" => "City", "name" => "Pemberton", "sameAs" => "https://en.wikipedia.org/wiki/Pemberton,_British_Columbia"),
                    array("@type" => "City", "name" => "Lions Bay", "sameAs" => "https://en.wikipedia.org/wiki/Lions_Bay"),
                    array("@type" => "City", "name" => "Britannia Beach", "sameAs" => "https://en.wikipedia.org/wiki/Britannia_Beach")
                ),
                "knowsAbout" => array(
                    "BC Building Code 2024",
                    "Vancouver Building By-law Part 10 R-22 Effective",
                    "Simpson Strong-Tie ATS Continuous Rod Tie-Down Systems",
                    "High-Seismic Infill Engineering (Sa=0.94g)",
                    "BC Energy Step Code 4 and Step Code 5",
                    "Passive House High-Performance Envelopes",
                    "District of West Vancouver Watercourse Protection Bylaw 4364",
                    "Whistler Alpine Heavy Timber & High Snow Load Engineering",
                    "Granite Bedrock Micropile and Post-Tensioned Rock Anchors",
                    "BC Bill 44 Multiplex Density and Infill Conversions",
                    "BC Hydro ES54 Civil Underground Ducting and Servicing"
                ),
                "hasOfferCatalog" => array(
                    "@type" => "OfferCatalog",
                    "name" => "Keystone Possibilities Construction & Fiduciary Services",
                    "itemListElement" => array(
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "BC Bill 44 Multiplex Feasibility & Construction",
                                "description" => "Turnkey feasibility, architectural drafting, civil utility servicing, and high-density multiplex build-out under BC Bill 44 missing middle legislation."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Custom Luxury Home Construction",
                                "description" => "Turnkey design-build contracting with mandatory 2-5-10 Year Home Warranty, Step Code 5 energy performance, and high-altitude alpine framing across West Vancouver and Whistler."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Fiduciary Project Management & Owner Representation",
                                "description" => "100% transparent cost-plus accounting, trade bidding oversight, municipal permit acceleration, and owner advocacy."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "BC Hydro Registered Civil Contracting",
                                "description" => "ES54 certified underground utility trenching, ducting, civil excavation, and municipal infrastructure connections."
                            )
                        ),
                        array(
                            "@type" => "Offer",
                            "itemOffered" => array(
                                "@type" => "Service",
                                "name" => "Construction Feasibility Studies & Land Due Diligence",
                                "description" => "Pre-acquisition site feasibility, geotechnical review, civil utility costing, and municipal zoning risk assessments."
                            )
                        )
                    )
                ),
                "sameAs" => array(
                    "https://www.facebook.com/profile.php?id=61554185128555",
                    "https://www.youtube.com/@KeystonePossibilities",
                    "https://www.instagram.com/keystonepossibilities",
                    "https://keystonerecomposition.com"
                ),
                "founder" => array(
                    "@type" => "Person",
                    "@id" => "https://keystonepossibilities.ca/#founder",
                    "name" => "Wayne Stevenson",
                    "jobTitle" => "Certified BC Residential Builder & Fiduciary Project Manager",
                    "url" => "https://keystonepossibilities.ca/about-us-general-contractor-squamish/",
                    "sameAs" => array(
                        "https://keystonerecomposition.com/about/",
                        "https://www.bchousing.org/licensing-consumer-disclosure/licencee-search"
                    ),
                    "hasCredential" => array(
                        "@type" => "EducationalOccupationalCredential",
                        "name" => "BC Housing Licensed Residential Builder (Licence #52603)",
                        "credentialCategory" => "Professional License",
                        "recognizedBy" => array(
                            "@type" => "GovernmentOrganization",
                            "name" => "BC Housing Licensing and Consumer Services",
                            "url" => "https://www.bchousing.org"
                        ),
                        "validIn" => array(
                            "@type" => "AdministrativeArea",
                            "name" => "British Columbia, Canada"
                        )
                    ),
                    "knowsAbout" => array(
                        "BC Building Code 2024",
                        "Step Code 5 Net-Zero Custom Homes",
                        "Vancouver Multiplex Zoning Bill 44",
                        "Fiduciary Cost-Plus Project Management"
                    )
                )
            ),
            // Parent Organization Entity (Keystone Empire / Keystone Group)
            array(
                "@type" => "Organization",
                "@id" => "https://keystonepossibilities.ca/#parent-organization",
                "name" => "Keystone Empire",
                "alternateName" => "Keystone Group",
                "url" => "https://keystonepossibilities.ca",
                "description" => "Master parent organization network governing Keystone Possibilities Ltd. and Keystone Recomposition.",
                "subOrganization" => array(
                    array(
                        "@type" => "Organization",
                        "@id" => "https://keystonepossibilities.ca/#organization",
                        "name" => "Keystone Possibilities Ltd.",
                        "url" => "https://keystonepossibilities.ca"
                    ),
                    array(
                        "@type" => "Organization",
                        "@id" => "https://keystonerecomposition.com/#organization",
                        "name" => "Keystone Recomposition",
                        "url" => "https://keystonerecomposition.com"
                    )
                ),
                "sameAs" => array(
                    "https://keystonepossibilities.ca",
                    "https://keystonerecomposition.com"
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

    echo "\n<!-- Keystone Possibilities 2026 Master Authority & ParentOrganization Schema -->\n";
    echo '<script type="application/ld+json">' . json_encode($master_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
}

// ── 2. Automatic Google-Compliant VideoObject Schema Injector ────────────────
add_action('wp_head', 'keystone_possibilities_inject_video_schema', 2);
function keystone_possibilities_inject_video_schema() {
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

    $video_id = get_post_meta($post_id, 'keystone_youtube_id', true);
    
    if (empty($video_id)) {
        $video_url = get_post_meta($post_id, 'video_url', true);
        if (!empty($video_url) && preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $video_url, $m)) {
            $video_id = $m[1];
        }
    }

    if (empty($video_id)) {
        $content = $post->post_content;
        if (preg_match('/\[keystone_video[^\]]*id=["\']([a-zA-Z0-9_-]{11})["\']/i', $content, $m)) {
            $video_id = $m[1];
        } elseif (preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $content, $m)) {
            $video_id = $m[1];
        }
    }

    if (!empty($video_id)) {
        $video_title = get_post_meta($post_id, 'video_title', true);
        if (empty($video_title)) {
            $video_title = get_the_title($post_id);
        }

        $video_desc = get_post_meta($post_id, 'video_description', true);
        if (empty($video_desc)) {
            $video_desc = wp_strip_all_tags(get_the_excerpt($post_id) ? get_the_excerpt($post_id) : wp_trim_words($post->post_content, 35));
        }
        if (empty($video_desc)) {
            $video_desc = esc_attr(get_the_title($post_id)) . ' - Certified BC Builder #52603 multiplex and construction consulting.';
        }

        $video_duration = get_post_meta($post_id, 'video_duration', true);
        if (empty($video_duration)) {
            $video_duration = get_post_meta($post_id, 'keystone_video_duration', true);
        }
        $duration_iso = 'PT5M0S'; // Default fallback 5 minutes
        if (!empty($video_duration)) {
            $video_duration = trim($video_duration);
            if (stripos($video_duration, 'PT') === 0) {
                $duration_iso = $video_duration;
            } elseif (is_numeric($video_duration)) {
                $total_seconds = intval($video_duration);
                $hours = floor($total_seconds / 3600);
                $minutes = floor(($total_seconds / 60) % 60);
                $seconds = $total_seconds % 60;
                $duration_iso = 'PT' . ($hours > 0 ? $hours . 'H' : '') . ($minutes > 0 ? $minutes . 'M' : '') . ($seconds > 0 ? $seconds . 'S' : ($hours == 0 && $minutes == 0 ? '0S' : ''));
            } elseif (preg_match('/^(?:(\d+):)?(\d+):(\d+)$/', $video_duration, $m)) {
                $hours = isset($m[1]) && $m[1] !== '' ? intval($m[1]) : 0;
                $minutes = intval($m[2]);
                $seconds = intval($m[3]);
                $duration_iso = 'PT' . ($hours > 0 ? $hours . 'H' : '') . ($minutes > 0 ? $minutes . 'M' : '') . ($seconds > 0 ? $seconds . 'S' : ($hours == 0 && $minutes == 0 ? '0S' : ''));
            }
        }

        $upload_date = get_the_date('c', $post_id);

        $video_schema = array(
            "@context" => "https://schema.org",
            "@type" => "VideoObject",
            "@id" => get_permalink($post_id) . "#videoobject",
            "name" => esc_attr($video_title),
            "description" => esc_attr($video_desc),
            "thumbnailUrl" => array(
                "https://img.youtube.com/vi/{$video_id}/maxresdefault.jpg",
                "https://img.youtube.com/vi/{$video_id}/hqdefault.jpg"
            ),
            "uploadDate" => $upload_date,
            "duration" => esc_attr($duration_iso),
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
                    "url" => "https://keystonepossibilities.ca/wp-content/uploads/logo.png"
                )
            )
        );
        echo "\n<!-- Keystone Possibilities Dynamic VideoObject Schema -->\n";
        echo '<script type="application/ld+json">' . json_encode($video_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . "</script>\n";
    }
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

// ── 2.9 Google-Compliant Watch Page & VideoObject Schema Injection in Rank Math ────
add_filter('rank_math/json_ld', 'keystone_possibilities_rank_math_watch_page_schema', 999, 2);
function keystone_possibilities_rank_math_watch_page_schema($data, $jsonld) {
    if (!is_array($data) || is_admin()) {
        return $data;
    }

    // 1. Sanitize any legacy staging URLs in Rank Math output
    array_walk_recursive($data, function(&$item) {
        if (is_string($item) && strpos($item, 'staging-a826-keystonepossibilities.wpcomstaging.com') !== false) {
            $item = str_replace('https://staging-a826-keystonepossibilities.wpcomstaging.com', 'https://keystonepossibilities.ca', $item);
        }
    });

    if (!is_singular('post')) {
        return $data;
    }

    global $post;
    if (!$post) return $data;

    // Detect YouTube Video ID
    $video_id = get_post_meta($post->ID, 'keystone_youtube_id', true);
    if (empty($video_id)) {
        $video_url = get_post_meta($post->ID, 'video_url', true);
        if (!empty($video_url) && preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $video_url, $m)) {
            $video_id = $m[1];
        }
    }
    if (empty($video_id)) {
        if (preg_match('/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i', $post->post_content, $m)) {
            $video_id = $m[1];
        }
    }

    if (empty($video_id)) {
        return $data;
    }

    $permalink     = get_permalink($post);
    $video_node_id = trailingslashit($permalink) . '#videoobject';
    $post_title    = get_the_title($post);
    $excerpt       = wp_strip_all_tags(get_the_excerpt($post));
    if (empty($excerpt)) {
        $excerpt = wp_trim_words(wp_strip_all_tags($post->post_content), 35, '...');
    }

    // High-res with guaranteed hqdefault fallback (eliminates 404s)
    $thumbnails = array(
        "https://img.youtube.com/vi/{$video_id}/maxresdefault.jpg",
        "https://img.youtube.com/vi/{$video_id}/hqdefault.jpg"
    );
    if (has_post_thumbnail($post)) {
        $feat = get_the_post_thumbnail_url($post, 'full');
        if ($feat) {
            array_unshift($thumbnails, $feat);
        }
    }

    // Parse duration
    $video_duration = get_post_meta($post->ID, 'video_duration', true);
    if (empty($video_duration)) {
        $video_duration = get_post_meta($post->ID, 'keystone_video_duration', true);
    }
    $duration_iso = 'PT5M0S';
    if (!empty($video_duration)) {
        $video_duration = trim($video_duration);
        if (stripos($video_duration, 'PT') === 0) {
            $duration_iso = $video_duration;
        } elseif (is_numeric($video_duration)) {
            $s = intval($video_duration);
            $h = floor($s / 3600);
            $m = floor(($s / 60) % 60);
            $sec = $s % 60;
            $duration_iso = 'PT' . ($h > 0 ? $h . 'H' : '') . ($m > 0 ? $m . 'M' : '') . ($sec > 0 ? $sec . 'S' : '');
        }
    }

    // Construct Compliant VideoObject Node
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

    // Inject VideoObject directly into Rank Math graph
    $data['VideoObject'] = $video_object;

    // Transform WebPage Node to ItemPage & Bind mainEntity (Watch Page Criteria)
    if (isset($data['WebPage'])) {
        $data['WebPage']['@type'] = array('WebPage', 'ItemPage');
        $data['WebPage']['mainEntity'] = array('@id' => $video_node_id);
    }

    // Demote/unset text-only Article and BlogPosting schemas so Google treats page as Watch Page
    unset($data['Article']);
    unset($data['BlogPosting']);

    // Also inject into @graph array if present
    if (isset($data['@graph']) && is_array($data['@graph'])) {
        $clean_graph = array();
        foreach ($data['@graph'] as $node) {
            $type = isset($node['@type']) ? (array)$node['@type'] : array();
            if (in_array('Article', $type) || in_array('BlogPosting', $type)) {
                continue; // Demote Article/BlogPosting nodes to avoid conflicting text-only categorization
            }
            if (in_array('WebPage', $type)) {
                $node['@type'] = array('WebPage', 'ItemPage');
                $node['mainEntity'] = array('@id' => $video_node_id);
            }
            $clean_graph[] = $node;
        }
        $clean_graph[] = $video_object;
        $data['@graph'] = $clean_graph;
    }

    return $data;
}

// ── 3. Keystone Empire Network Standardized Footer Bar ───────────────────────
add_action('wp_footer', 'keystone_possibilities_render_empire_footer', 30);
function keystone_possibilities_render_empire_footer() {
    ?>
    <!-- Keystone Empire Network Standardized Footer Bar -->
    <div class="keystone-empire-footer-bar" style="background:#04070d; border-top:1px solid rgba(196,162,101,0.25); padding:16px 20px; text-align:center; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; color:#94a3b8; font-size:0.82rem;">
        <div style="max-width:1200px; margin:0 auto; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px;">
            <div style="display:flex; align-items:center; gap:10px; text-align:left;">
                <span style="color:#c4a265; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; font-size:0.78rem; display:inline-flex; align-items:center; gap:6px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#c4a265" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                    KEYSTONE EMPIRE NETWORK
                </span>
                <span style="color:rgba(255,255,255,0.2);">|</span>
                <span style="color:#cbd5e1; font-size:0.8rem; font-weight:500;">Keystone Possibilities — BC Building Code &amp; Construction Consulting</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px; font-size:0.8rem;">
                <span style="color:#64748b;">Sister Flagship:</span>
                <a href="https://keystonerecomposition.com" target="_blank" rel="noopener" style="color:#c4a265; font-weight:600; text-decoration:none; transition:color 0.2s; display:inline-flex; align-items:center; gap:4px;">
                    Keystone Recomposition — Evidence-Based Clinical Peptides &amp; Protocol Analytics &#8594;
                </a>
            </div>
        </div>
    </div>
    <?php
}

// ── 4. Rank Math XML Sitemap Sanitizer & Cache Bypass ────────────────────────
add_filter( 'rank_math/sitemap/enable_caching', '__return_false' );
add_filter( 'rank_math/sitemap/entry', function( $url, $type = '', $object = null ) {
    if ( empty( $url['loc'] ) ) return $url;
    $excluded_patterns = array(
        '/tag/', '/author/', '/date/', 'sample-page', 'test', 'demo', 'wp-admin'
    );
    foreach ( $excluded_patterns as $pat ) {
        if ( stripos( $url['loc'], $pat ) !== false ) {
            return false;
        }
    }
    return $url;
}, 10, 3 );

// ── 5. Sanitize robots.txt & Expose AI Crawler Directives (/llms.txt) ─────────
add_filter( 'robots_txt', function( $output, $public ) {
    $custom = "User-agent: *\nDisallow: /wp-admin/\nAllow: /wp-admin/admin-ajax.php\nAllow: /wp-content/uploads/\nAllow: /wp-content/themes/\nAllow: /wp-includes/\n\n# AI Search Engine Crawlers\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: https://keystonepossibilities.ca/sitemap_index.xml\n";
    return $custom;
}, 99, 2 );
