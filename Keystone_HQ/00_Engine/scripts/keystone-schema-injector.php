<?php
/**
 * Plugin Name: Keystone Schema Injector
 * Description: Injects LocalBusiness, FAQPage, and BreadcrumbList schema for GEO/AI optimization
 * Version: 1.0.0
 * Author: Keystone Master Brain
 */

// Prevent direct access
if (!defined('ABSPATH')) exit;

/**
 * Inject LocalBusiness schema on the homepage
 */
add_action('wp_head', 'keystone_inject_localbusiness_schema');
function keystone_inject_localbusiness_schema() {
    if (!is_front_page()) return;
    
    $schema = [
        "@context" => "https://schema.org",
        "@type" => "LocalBusiness",
        "@id" => "https://keystonepossibilities.ca/#localbusiness",
        "name" => "Keystone Possibilities LTD",
        "legalName" => "Keystone Possibilities Ltd.",
        "description" => "Licensed residential builder and fiduciary construction project manager serving Squamish, Whistler, West Vancouver, and the Sea-to-Sky corridor in British Columbia, Canada. BC Builder License #52603.",
        "url" => "https://keystonepossibilities.ca",
        "logo" => [
            "@type" => "ImageObject",
            "url" => "https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-03-at-2.30.29-pm-1.png",
            "width" => 600,
            "height" => 60
        ],
        "image" => "https://keystonepossibilities.ca/wp-content/uploads/2026/05/Home_under_construction_mountain1_202605011201.jpeg",
        "telephone" => "+1-604-815-8534",
        "email" => "wayne@keystonepossibilities.com",
        "founder" => [
            "@type" => "Person",
            "@id" => "https://keystonepossibilities.ca/#person",
            "name" => "Wayne Stevenson",
            "jobTitle" => "Founder & Licensed BC Builder",
            "hasCredential" => [
                "@type" => "EducationalOccupationalCredential",
                "credentialCategory" => "Licensed Residential Builder",
                "recognizedBy" => [
                    "@type" => "Organization",
                    "name" => "BC Housing"
                ],
                "identifier" => "52603"
            ]
        ],
        "address" => [
            "@type" => "PostalAddress",
            "streetAddress" => "Watts Point Road",
            "addressLocality" => "Squamish",
            "addressRegion" => "BC",
            "postalCode" => "V8B 0B1",
            "addressCountry" => "CA"
        ],
        "geo" => [
            "@type" => "GeoCoordinates",
            "latitude" => "49.6580",
            "longitude" => "-123.2140"
        ],
        "priceRange" => "$$$$",
        "currenciesAccepted" => "CAD",
        "paymentAccepted" => "Cash, Credit Card, E-Transfer, Wire Transfer",
        "openingHoursSpecification" => [
            [
                "@type" => "OpeningHoursSpecification",
                "dayOfWeek" => ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens" => "07:00",
                "closes" => "18:00"
            ],
            [
                "@type" => "OpeningHoursSpecification",
                "dayOfWeek" => "Saturday",
                "opens" => "08:00",
                "closes" => "14:00"
            ]
        ],
        "areaServed" => [
            ["@type" => "City", "name" => "Squamish", "sameAs" => "https://en.wikipedia.org/wiki/Squamish,_British_Columbia"],
            ["@type" => "City", "name" => "Whistler", "sameAs" => "https://en.wikipedia.org/wiki/Whistler,_British_Columbia"],
            ["@type" => "City", "name" => "West Vancouver", "sameAs" => "https://en.wikipedia.org/wiki/West_Vancouver"],
            ["@type" => "City", "name" => "North Vancouver"],
            ["@type" => "City", "name" => "Pemberton"],
            ["@type" => "AdministrativeArea", "name" => "Sunshine Coast"]
        ],
        "hasOfferCatalog" => [
            "@type" => "OfferCatalog",
            "name" => "Construction Services",
            "itemListElement" => [
                [
                    "@type" => "Offer",
                    "itemOffered" => [
                        "@type" => "Service",
                        "name" => "Fiduciary Construction Project Management",
                        "description" => "100% transparent, open-book construction PM at a flat fee of 10-15%. No markup on trades or materials.",
                        "serviceType" => "Construction Management"
                    ]
                ],
                [
                    "@type" => "Offer",
                    "itemOffered" => [
                        "@type" => "Service",
                        "name" => "Custom Luxury Home Building",
                        "description" => "Start-to-finish custom luxury home construction in the Sea-to-Sky corridor.",
                        "serviceType" => "Residential Construction"
                    ]
                ],
                [
                    "@type" => "Offer",
                    "itemOffered" => [
                        "@type" => "Service",
                        "name" => "BC Hydro Civil Utility Connections",
                        "description" => "Registered BC Hydro civil contractor for electrical service upgrades and utility connections.",
                        "serviceType" => "Civil Contracting"
                    ]
                ],
                [
                    "@type" => "Offer",
                    "itemOffered" => [
                        "@type" => "Service",
                        "name" => "BC Bill 44 Multiplex Conversions",
                        "description" => "Feasibility analysis and construction for fourplex and multiplex conversions under BC Bill 44.",
                        "serviceType" => "Multiplex Construction"
                    ]
                ]
            ]
        ],
        "sameAs" => [
            "https://www.youtube.com/@KeyStoneRecomposition",
            "https://www.youtube.com/@KeystoneProtocols",
            "https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y",
            "https://keystonerecomposition.com",
            "https://www.facebook.com/profile.php?id=61554185128555",
            "https://www.instagram.com/keystonerecomposition"
        ],
        "memberOf" => [
            ["@type" => "Organization", "name" => "Squamish Chamber of Commerce"],
            ["@type" => "Organization", "name" => "Canadian Home Builders' Association Sea-to-Sky"]
        ],
        "hasCredential" => [
            [
                "@type" => "EducationalOccupationalCredential",
                "credentialCategory" => "Licensed Residential Builder",
                "recognizedBy" => ["@type" => "Organization", "name" => "BC Housing"],
                "identifier" => "52603"
            ],
            [
                "@type" => "EducationalOccupationalCredential",
                "credentialCategory" => "National Home Warranty Provider",
                "description" => "2-5-10 Year New Home Warranty Coverage"
            ]
        ]
    ];
    
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
}

/**
 * Inject BreadcrumbList schema on all pages
 */
add_action('wp_head', 'keystone_inject_breadcrumb_schema');
function keystone_inject_breadcrumb_schema() {
    if (is_front_page()) return;
    
    $breadcrumbs = [
        "@context" => "https://schema.org",
        "@type" => "BreadcrumbList",
        "itemListElement" => []
    ];
    
    // Home is always first
    $breadcrumbs["itemListElement"][] = [
        "@type" => "ListItem",
        "position" => 1,
        "name" => "Home",
        "item" => "https://keystonepossibilities.ca/"
    ];
    
    // Add current page
    $position = 2;
    
    // If it's a category page, add category
    if (is_category()) {
        $cat = get_queried_object();
        $breadcrumbs["itemListElement"][] = [
            "@type" => "ListItem",
            "position" => $position,
            "name" => $cat->name,
            "item" => get_category_link($cat->term_id)
        ];
    }
    // If it's a single post
    elseif (is_single()) {
        $categories = get_the_category();
        if (!empty($categories)) {
            $breadcrumbs["itemListElement"][] = [
                "@type" => "ListItem",
                "position" => $position,
                "name" => $categories[0]->name,
                "item" => get_category_link($categories[0]->term_id)
            ];
            $position++;
        }
        $breadcrumbs["itemListElement"][] = [
            "@type" => "ListItem",
            "position" => $position,
            "name" => get_the_title(),
            "item" => get_permalink()
        ];
    }
    // If it's a page
    elseif (is_page()) {
        // Check for parent pages
        $ancestors = get_post_ancestors(get_the_ID());
        if (!empty($ancestors)) {
            $ancestors = array_reverse($ancestors);
            foreach ($ancestors as $ancestor_id) {
                $breadcrumbs["itemListElement"][] = [
                    "@type" => "ListItem",
                    "position" => $position,
                    "name" => get_the_title($ancestor_id),
                    "item" => get_permalink($ancestor_id)
                ];
                $position++;
            }
        }
        $breadcrumbs["itemListElement"][] = [
            "@type" => "ListItem",
            "position" => $position,
            "name" => get_the_title(),
            "item" => get_permalink()
        ];
    }
    
    echo '<script type="application/ld+json">' . wp_json_encode($breadcrumbs, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
}

/**
 * Inject FAQPage schema on the services page and FAQ page
 */
add_action('wp_head', 'keystone_inject_faq_schema');
function keystone_inject_faq_schema() {
    // Only inject on services page or FAQ page
    $services_slugs = ['services-general-contractor-squamish', 'faq'];
    
    if (!is_page($services_slugs)) return;
    
    if (is_page('services-general-contractor-squamish')) {
        $faqs = [
            [
                "question" => "What is fiduciary construction project management?",
                "answer" => "Fiduciary construction project management means we legally represent YOUR interests, not ours. Unlike traditional general contractors who mark up every subcontractor invoice by 15-25%, we operate on a flat fee of 10-15% with 100% open-book accounting. You see every invoice, every trade contract, and every material cost in real time through our secure client portal. This model saves Sea-to-Sky homeowners an average of $80,000-$150,000 on a typical custom home build."
            ],
            [
                "question" => "What areas does Keystone Possibilities serve?",
                "answer" => "We serve the entire Sea-to-Sky corridor in British Columbia: Squamish, Whistler, Pemberton, West Vancouver, North Vancouver, and the Sunshine Coast. Our head office is in Squamish, BC, giving us strategic access to all Sea-to-Sky communities. We hold BC Builder License #52603 and are registered with WorkSafeBC for all service areas."
            ],
            [
                "question" => "How much does it cost to build a custom home in the Sea-to-Sky corridor?",
                "answer" => "Custom home construction costs in the Sea-to-Sky corridor range from $450 to $900+ per square foot depending on location, terrain, and finishes. Whistler alpine builds typically cost $600-$900/sqft due to extreme snow load engineering requirements. Squamish valley builds range $450-$650/sqft. West Vancouver cliffside estates can exceed $900/sqft due to structural steel and geotechnical requirements. Our fiduciary PM model ensures you pay true trade pricing with zero markup on materials or labor."
            ],
            [
                "question" => "Are you a registered BC Hydro civil contractor?",
                "answer" => "Yes, Keystone Possibilities is officially listed as a registered BC Hydro civil contractor. We handle all electrical utility connections, service upgrades, transformer pad installations, and overhead-to-underground conversions throughout the Sea-to-Sky corridor. We are compliant with 30M33 Electrical Distribution Safety Standards and hold all required WorkSafeBC certifications."
            ],
            [
                "question" => "What warranty coverage do you provide?",
                "answer" => "All new Keystone Possibilities homes are covered by the National Home Warranty Program, providing comprehensive 2-5-10 year protection: 2 years on materials and labor defects, 5 years on building envelope (water penetration), and 10 years on structural defects. This warranty is backed by a national insurance program and transfers with the property if you sell."
            ]
        ];
    } else {
        return; // FAQ page schema will be generated by the FAQ page itself
    }
    
    $schema = [
        "@context" => "https://schema.org",
        "@type" => "FAQPage",
        "mainEntity" => []
    ];
    
    foreach ($faqs as $faq) {
        $schema["mainEntity"][] = [
            "@type" => "Question",
            "name" => $faq["question"],
            "acceptedAnswer" => [
                "@type" => "Answer",
                "text" => $faq["answer"]
            ]
        ];
    }
    
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
}

/**
 * Fix the Organization schema - override Rank Math's incorrect description
 * This filters Rank Math's JSON-LD output to fix the entity confusion
 */
add_filter('rank_math/json_ld', 'keystone_fix_rankmath_schema', 99, 2);
function keystone_fix_rankmath_schema($data, $jsonld) {
    // Fix Organization description
    if (isset($data['Organization'])) {
        $data['Organization']['description'] = 'Licensed residential builder and fiduciary construction project manager serving Squamish, Whistler, West Vancouver, and the Sea-to-Sky corridor in British Columbia, Canada. BC Builder License #52603.';
        
        // Fix logo URL if it points to staging
        if (isset($data['Organization']['logo']['url']) && strpos($data['Organization']['logo']['url'], 'wpcomstaging.com') !== false) {
            $data['Organization']['logo']['url'] = str_replace(
                'staging-a826-keystonepossibilities.wpcomstaging.com',
                'keystonepossibilities.ca',
                $data['Organization']['logo']['url']
            );
        }
        
        // Ensure Organization is NOT also typed as Person
        if (is_array($data['Organization']['@type'])) {
            $data['Organization']['@type'] = 'Organization';
        }
        
        // Remove duplicate sameAs entries
        if (isset($data['Organization']['sameAs']) && is_array($data['Organization']['sameAs'])) {
            $data['Organization']['sameAs'] = array_values(array_unique($data['Organization']['sameAs']));
        }
    }
    
    // Fix Person entity - ensure it's separate from Organization
    if (isset($data['Person'])) {
        if (is_array($data['Person']['@type'])) {
            $data['Person']['@type'] = 'Person';
        }
    }
    
    // Fix any remaining staging URLs throughout all schema
    $json_string = wp_json_encode($data);
    $json_string = str_replace(
        'staging-a826-keystonepossibilities.wpcomstaging.com',
        'keystonepossibilities.ca',
        $json_string
    );
    $data = json_decode($json_string, true);
    
    return $data;
}

/**
 * ═══════════════════════════════════════════════════════════════
 * FIX #1: Remove NOCACHE meta tags that block AI grounding
 * Bing says: "NOCACHE tag restricts text available to Copilot"
 * This also helps Google AI Overviews cite our content.
 * ═══════════════════════════════════════════════════════════════
 */
add_action('wp_head', 'keystone_remove_nocache', 1);
function keystone_remove_nocache() {
    // Remove any nocache headers WordPress or plugins might set
    if (!is_admin()) {
        header_remove('X-Robots-Tag');
        // We'll use output buffering to strip nocache metas
        ob_start('keystone_strip_nocache_meta');
    }
}

add_action('wp_footer', 'keystone_flush_nocache_buffer', 999);
function keystone_flush_nocache_buffer() {
    if (ob_get_level() > 0) {
        ob_end_flush();
    }
}

function keystone_strip_nocache_meta($html) {
    // Remove <meta name="robots" content="...nocache..."> or noarchive tags
    $html = preg_replace(
        '/<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*(?:nocache|noarchive|nosnippet)[^"\']*["\']\s*\/?>/i',
        '',
        $html
    );
    return $html;
}

// Override Rank Math's robots to ensure no NOCACHE
add_filter('rank_math/frontend/robots', 'keystone_force_cache_robots');
function keystone_force_cache_robots($robots) {
    // Remove nocache, noarchive, nosnippet directives
    unset($robots['nocache']);
    unset($robots['noarchive']);
    unset($robots['nosnippet']);
    
    // Ensure max-snippet is unlimited for AI grounding
    $robots['max-snippet'] = 'max-snippet:-1';
    $robots['max-video-preview'] = 'max-video-preview:-1';
    $robots['max-image-preview'] = 'max-image-preview:large';
    
    return $robots;
}

/**
 * ═══════════════════════════════════════════════════════════════
 * FIX #2: Optimize meta descriptions for ALL pages
 * Bing says: "Meta descriptions on many pages are too short"
 * Target: 150-160 characters, keyword-rich, compelling
 * ═══════════════════════════════════════════════════════════════
 */
add_filter('rank_math/frontend/description', 'keystone_override_meta_descriptions');
function keystone_override_meta_descriptions($description) {
    global $post;
    if (!$post) return $description;
    
    $slug = $post->post_name;
    
    $descriptions = [
        // Location pages
        'squamish-custom-homes' => 'Custom home builder in Squamish, BC. Fiduciary project management, BC Builder License #52603. Save 12-18% vs traditional builders. Free consultation.',
        'whistler-custom-homes' => 'Whistler custom home builder specializing in alpine construction. Engineered for 11m+ annual snowfall. Fiduciary PM, BC License #52603. Free consultation.',
        'west-vancouver-custom-homes' => 'West Vancouver custom home builder for cliffside & waterfront estates. Rock-anchored foundations, marine-grade construction. BC License #52603.',
        'north-vancouver-custom-homes' => 'North Vancouver custom home builder with biophilic design expertise. Forest-sensitive construction, Lynn Valley to Deep Cove. BC License #52603.',
        'sunshine-coast-custom-homes' => 'Sunshine Coast custom home builder for remote coastal & island properties. Barge logistics, off-grid systems expert. BC License #52603.',
        
        // Service pages
        'services-general-contractor-squamish' => 'Keystone Possibilities: fiduciary construction project management in Squamish, BC. 100% transparent pricing, open-book accounting. BC Builder License #52603.',
        'squamish-custom-home-builder' => 'Wayne Stevenson, licensed BC custom home builder (#52603) in Squamish. 20+ years experience, fiduciary PM model saves homeowners 12-18% on builds.',
        'squamish-accessory-dwelling-unit-adu-builder' => 'ADU & laneway home builder in Squamish, BC. BC Bill 44 multiplex conversions, secondary suites. Licensed builder #52603. Free feasibility assessment.',
        'project-management' => 'Fiduciary construction project management for custom homes in BC Sea-to-Sky corridor. Open-book accounting, flat PM fee. BC License #52603.',
        'bc-hydro-registered-civil-contractor' => 'BC Hydro registered civil contractor in Squamish. Electrical service upgrades, transformer pads, overhead-to-underground conversions. Licensed & insured.',
        
        // Blog posts — ensure they have good descriptions
        'bc-building-code-updates-2025-2026' => 'Complete guide to BC Building Code updates for 2025-2026. Energy Step Code changes, structural requirements, and what Squamish builders need to know.',
    ];
    
    // Check by slug
    if (isset($descriptions[$slug])) {
        return $descriptions[$slug];
    }
    
    // If current description is too short (under 120 chars), auto-generate one
    if (strlen($description) < 120 && !empty($post->post_content)) {
        $excerpt = wp_strip_all_tags($post->post_content);
        $excerpt = substr($excerpt, 0, 155);
        $excerpt = substr($excerpt, 0, strrpos($excerpt, ' '));
        if (strlen($excerpt) > 120) {
            return $excerpt . '...';
        }
    }
    
    return $description;
}

/**
 * ═══════════════════════════════════════════════════════════════
 * FIX #3: Fix multiple <h1> tags on the homepage
 * Bing says: "There are multiple <h1> tags on the page" (HIGH)
 * The theme outputs h1.Home + the page title as h1. Fix to single h1.
 * ═══════════════════════════════════════════════════════════════
 */
add_filter('the_title', 'keystone_fix_homepage_h1', 10, 2);
function keystone_fix_homepage_h1($title, $id = null) {
    // Only modify on front page, main query
    if (is_front_page() && is_main_query() && in_the_loop()) {
        // Return empty to prevent duplicate h1 from page title
        // The theme's hero section should provide the single h1
        return '';
    }
    return $title;
}

// Use output buffer to enforce single h1 on homepage
add_action('wp_head', 'keystone_start_h1_fix', 2);
function keystone_start_h1_fix() {
    if (is_front_page()) {
        ob_start('keystone_enforce_single_h1');
    }
}

function keystone_enforce_single_h1($html) {
    // Count h1 tags
    preg_match_all('/<h1[^>]*>(.*?)<\/h1>/is', $html, $matches);
    
    if (count($matches[0]) > 1) {
        $first = true;
        $html = preg_replace_callback('/<h1([^>]*)>(.*?)<\/h1>/is', function($m) use (&$first) {
            if ($first) {
                $first = false;
                // Keep the first h1 but make it keyword-rich
                $text = strip_tags($m[2]);
                if (strtolower(trim($text)) === 'home' || strlen(trim($text)) < 5) {
                    return '<h1' . $m[1] . '>Custom Home Builder Squamish BC | Keystone Possibilities</h1>';
                }
                return $m[0]; // Keep first h1 as-is if it's already good
            }
            // Convert subsequent h1s to h2
            return '<h2' . $m[1] . '>' . $m[2] . '</h2>';
        }, $html);
    } elseif (count($matches[0]) === 1) {
        // If there's only one h1 but it just says "Home", fix it
        $text = strip_tags($matches[1][0]);
        if (strtolower(trim($text)) === 'home') {
            $html = preg_replace(
                '/<h1([^>]*)>\s*Home\s*<\/h1>/i',
                '<h1$1>Custom Home Builder Squamish BC | Keystone Possibilities</h1>',
                $html
            );
        }
    }
    
    return $html;
}

/**
 * ═══════════════════════════════════════════════════════════════
 * FIX #4: Add ALT attributes to images missing them
 * Bing says: "<img> tag does not have an ALT attribute" (3 pages)
 * Also critical for Google Image search and accessibility
 * ═══════════════════════════════════════════════════════════════
 */
add_filter('the_content', 'keystone_auto_alt_attributes', 20);
function keystone_auto_alt_attributes($content) {
    // Find all img tags without alt attributes or with empty alt
    $content = preg_replace_callback(
        '/<img(?![^>]*\balt\s*=)[^>]*>/i',
        function($match) {
            $img = $match[0];
            // Try to extract a meaningful alt from the filename
            if (preg_match('/src=["\']([^"\']+)["\']/i', $img, $src)) {
                $filename = pathinfo(parse_url($src[1], PHP_URL_PATH), PATHINFO_FILENAME);
                // Clean up the filename to make a readable alt
                $alt = str_replace(['-', '_'], ' ', $filename);
                $alt = ucwords(trim($alt));
                // Add context
                $alt .= ' - Keystone Possibilities Custom Home Builder Squamish BC';
                // Insert alt attribute before the closing >
                $img = str_replace('/>', ' alt="' . esc_attr($alt) . '" />', $img);
                $img = str_replace('>', ' alt="' . esc_attr($alt) . '">', $img);
            } else {
                // Fallback generic alt
                $img = str_replace('/>', ' alt="Keystone Possibilities custom home construction in Squamish BC" />', $img);
                $img = str_replace('>', ' alt="Keystone Possibilities custom home construction in Squamish BC">', $img);
            }
            return $img;
        },
        $content
    );
    
    // Also fix empty alt="" tags with meaningful content
    $content = preg_replace_callback(
        '/<img([^>]*)\balt\s*=\s*["\']["\']([^>]*)>/i',
        function($match) {
            $before = $match[1];
            $after = $match[2];
            // Extract filename for alt
            $full = $match[0];
            if (preg_match('/src=["\']([^"\']+)["\']/i', $full, $src)) {
                $filename = pathinfo(parse_url($src[1], PHP_URL_PATH), PATHINFO_FILENAME);
                $alt = str_replace(['-', '_'], ' ', $filename);
                $alt = ucwords(trim($alt));
                return '<img' . $before . 'alt="' . esc_attr($alt) . '"' . $after . '>';
            }
            return $full;
        },
        $content
    );
    
    return $content;
}

// Also fix images in the header/footer/widgets
add_action('wp_head', 'keystone_start_global_alt_fix', 3);
function keystone_start_global_alt_fix() {
    if (!is_admin()) {
        ob_start('keystone_global_img_alt_fix');
    }
}

function keystone_global_img_alt_fix($html) {
    // Add alt to any img without it across the entire page
    return preg_replace_callback(
        '/<img(?![^>]*\balt\s*=)[^>]*>/i',
        function($match) {
            $img = $match[0];
            if (preg_match('/src=["\']([^"\']+)["\']/i', $img, $src)) {
                $filename = pathinfo(parse_url($src[1], PHP_URL_PATH), PATHINFO_FILENAME);
                $alt = str_replace(['-', '_'], ' ', $filename);
                $alt = ucwords(trim($alt));
                return str_replace('>', ' alt="' . esc_attr($alt) . '">', $img);
            }
            return str_replace('>', ' alt="Keystone Possibilities">', $img);
        },
        $html
    );
}

/**
 * ═══════════════════════════════════════════════════════════════
 * FIX #5: BC Hydro Contractor credential in schema (for backlinks)
 * Adds the BC Hydro registration as a credential on all pages
 * ═══════════════════════════════════════════════════════════════
 */
add_action('wp_head', 'keystone_inject_contractor_schema');
function keystone_inject_contractor_schema() {
    if (!is_page('bc-hydro-registered-civil-contractor')) return;
    
    $schema = [
        "@context" => "https://schema.org",
        "@type" => "Service",
        "@id" => "https://keystonepossibilities.ca/bc-hydro-registered-civil-contractor/#service",
        "name" => "BC Hydro Registered Civil Contractor Services",
        "description" => "Keystone Possibilities is a registered BC Hydro civil contractor providing electrical service upgrades, transformer pad installations, overhead-to-underground conversions, and utility connections throughout the Sea-to-Sky corridor.",
        "provider" => [
            "@type" => "LocalBusiness",
            "@id" => "https://keystonepossibilities.ca/#localbusiness",
            "name" => "Keystone Possibilities LTD"
        ],
        "serviceType" => "BC Hydro Civil Contracting",
        "areaServed" => [
            ["@type" => "City", "name" => "Squamish, BC"],
            ["@type" => "City", "name" => "Whistler, BC"],
            ["@type" => "City", "name" => "West Vancouver, BC"],
            ["@type" => "City", "name" => "North Vancouver, BC"],
            ["@type" => "AdministrativeArea", "name" => "Sea-to-Sky Corridor, BC"]
        ],
        "hasCredential" => [
            "@type" => "EducationalOccupationalCredential",
            "credentialCategory" => "Registered BC Hydro Civil Contractor",
            "recognizedBy" => [
                "@type" => "Organization",
                "name" => "BC Hydro",
                "url" => "https://www.bchydro.com"
            ]
        ],
        "offers" => [
            [
                "@type" => "Offer",
                "itemOffered" => [
                    "@type" => "Service",
                    "name" => "Electrical Service Upgrades",
                    "description" => "Residential and commercial electrical service upgrades from 100A to 400A+"
                ]
            ],
            [
                "@type" => "Offer",
                "itemOffered" => [
                    "@type" => "Service",
                    "name" => "Transformer Pad Installation",
                    "description" => "Ground-mount and pad-mount transformer installations for new developments"
                ]
            ],
            [
                "@type" => "Offer",
                "itemOffered" => [
                    "@type" => "Service",
                    "name" => "Overhead to Underground Conversion",
                    "description" => "Converting overhead electrical lines to underground distribution"
                ]
            ]
        ]
    ];
    
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
}

/**
 * Add IndexNow support - enables instant indexing with Bing/Yandex
 */
add_action('save_post', 'keystone_indexnow_ping', 10, 3);
function keystone_indexnow_ping($post_id, $post, $update) {
    // Only ping for published posts/pages
    if ($post->post_status !== 'publish') return;
    if (wp_is_post_revision($post_id)) return;
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;
    
    $url = get_permalink($post_id);
    $key = 'keystone-indexnow-2026';
    
    // Ping IndexNow (Bing + Yandex)
    $endpoints = [
        'https://api.indexnow.org/indexnow',
        'https://www.bing.com/indexnow',
    ];
    
    foreach ($endpoints as $endpoint) {
        wp_remote_get(add_query_arg([
            'url' => $url,
            'key' => $key,
        ], $endpoint), [
            'timeout' => 5,
            'blocking' => false,
        ]);
    }
}
