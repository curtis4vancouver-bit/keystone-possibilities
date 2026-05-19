<?php
// Enqueue parent theme styles
add_action( 'wp_enqueue_scripts', 'keystone_recomposition_child_enqueue_styles' );
function keystone_recomposition_child_enqueue_styles() {
    wp_enqueue_style( 'astra-theme-css', get_template_directory_uri() . '/style.css' );
}

/**
 * Filter the single post title wrapper to ensure it's strictly an H1.
 */
add_filter( 'astra_the_title_before', 'keystone_recomposition_child_title_before', 10, 1 );
function keystone_recomposition_child_title_before( $before ) {
    if ( is_singular() ) {
        // Force the opening tag to be an h1 for single posts/pages.
        // Astra natively passes <h1 ...> for some places, but let's be sure.
        return preg_replace('/^<h[1-6]/i', '<h1', $before);
    }
    return $before;
}

add_filter( 'astra_the_title_after', 'keystone_recomposition_child_title_after', 10, 1 );
function keystone_recomposition_child_title_after( $after ) {
    if ( is_singular() ) {
        return preg_replace('/<\/h[1-6]>/i', '</h1>', $after);
    }
    return $after;
}

/**
 * Filter the archive post title wrapper to ensure it's strictly an H2, preventing multiple H1s.
 */
add_filter( 'astra_the_post_title_before', 'keystone_recomposition_child_post_title_before', 10, 1 );
function keystone_recomposition_child_post_title_before( $before ) {
    if ( ! is_singular() ) {
        // Change any h1-h6 opening tag to h2 for post loops in archives/index
        return preg_replace('/^<h[1-6]/i', '<h2', $before);
    }
    return $before;
}

add_filter( 'astra_the_post_title_after', 'keystone_recomposition_child_post_title_after', 10, 1 );
function keystone_recomposition_child_post_title_after( $after ) {
    if ( ! is_singular() ) {
        return preg_replace('/<\/h[1-6]>/i', '</h2>', $after);
    }
    return $after;
}

/**
 * Inject JSON-LD Schema into wp_head
 */
function keystone_recomposition_child_inject_schema() {
    // Attempt to get custom logo from theme mods, fallback to default URL
    $custom_logo_id = get_theme_mod( 'custom_logo' );
    $logo_url = wp_get_attachment_image_url( $custom_logo_id, 'full' );
    if ( ! $logo_url ) {
        $logo_url = 'https://keystonerecomposition.com/wp-content/uploads/logo.png';
    }

    // === Organization Schema ===
    $schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'Organization',
        'name' => 'Keystone Digital',
        'url' => 'https://keystonerecomposition.com',
        'description' => 'A multifaceted digital organization managing health, beauty, construction, and entertainment projects, including deep house music and record labels.',
        'keywords' => 'Keystone Digital, deep house music, music label, digital organization, entertainment, record label',
        'logo' => $logo_url,
        'sameAs' => array(
            'https://www.youtube.com/@KeystoneRecomposition',
            'https://www.youtube.com/@KeystoneProtocols',
            'https://musicbrainz.org/label/30027d0e-6aeb-4704-8792-a031c936c62a',
            'https://audiomack.com/keystone-recomposition',
            'https://toolost.com'
        ),
        'identifier' => array(
            '@type' => 'PropertyValue',
            'propertyID' => 'Too Lost Catalog Reference ID',
            'value' => 'TOOLOST3000939655'
        ),
        'subOrganization' => array(
            array(
                '@type' => 'HealthAndBeautyBusiness',
                'name' => 'Keystone Recomposition',
                'url' => 'https://keystonerecomposition.com',
                'description' => 'Specializing in health, wellness, and beauty recomposition. Explore GLP-1 weight loss solutions, fitness programs, and beauty enhancements.',
                'keywords' => 'Keystone Recomposition, GLP-1, health, beauty, wellness, weight loss, fitness',
                'founder' => array(
                    '@type' => 'Person',
                    'name' => 'Wayne Stevenson',
                    'jobTitle' => 'Biohacking & Metabolic Health Authority'
                )
            ),
            array(
                '@type' => 'GeneralContractor',
                'name' => 'Keystone Possibilities',
                'url' => 'https://keystonepossibilities.ca',
                'description' => 'Premium Construction Project Management and Civil Construction Services operating across the Sea-to-Sky and Greater Vancouver regions.',
                'founder' => array(
                    '@type' => 'Person',
                    'name' => 'Wayne Stevenson',
                    'jobTitle' => 'Certified BC Builder & Project Manager',
                    'sameAs' => 'https://keystonerecomposition.com/about/'
                ),
                'areaServed' => array(
                    array('@type' => 'City', 'name' => 'Whistler'),
                    array('@type' => 'City', 'name' => 'West Vancouver'),
                    array('@type' => 'City', 'name' => 'North Vancouver'),
                    array('@type' => 'City', 'name' => 'Squamish')
                ),
                'hasOfferCatalog' => array(
                    '@type' => 'OfferCatalog',
                    'name' => 'Construction Services',
                    'itemListElement' => array(
                        array('@type' => 'Offer', 'itemOffered' => array('@type' => 'Service', 'name' => 'Luxury Custom Home Project Management')),
                        array('@type' => 'Offer', 'itemOffered' => array('@type' => 'Service', 'name' => 'Civil Construction & Site Engineering'))
                    )
                ),
                'identifier' => array(
                    '@type' => 'PropertyValue',
                    'propertyID' => 'BC Builder License',
                    'value' => '52603'
                ),
                'memberOf' => array(
                    '@type' => 'Organization',
                    'name' => 'WBI Home Warranty',
                    'url' => 'https://wbihomewarranty.com/'
                )
            )
        )
    );

    $json_schema = wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );

    echo "<!-- Keystone Digital JSON-LD Schema -->\n";
    echo "<script type=\"application/ld+json\">\n";
    echo $json_schema . "\n";
    echo "</script>\n";
    echo "<!-- End Keystone Digital JSON-LD Schema -->\n";

    // === Person Schema (Knowledge Panel Anchor) ===
    $person_schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'Person',
        'name' => 'Wayne Stevenson',
        'alternateName' => array( 'Keystone Recomposition', 'Keystone Protocols' ),
        'url' => 'https://keystonerecomposition.com',
        'image' => $logo_url,
        'jobTitle' => 'Health Researcher, Music Producer & Construction Project Manager',
        'description' => 'Founder of Keystone Digital. Documents the intersection of GLP-1 metabolic health, peptide science, body recomposition, and longevity for men over 40. Also produces deep house music and manages luxury construction projects in the Sea-to-Sky corridor.',
        'knowsAbout' => array(
            'GLP-1 receptor agonists',
            'metabolic health',
            'body recomposition',
            'peptide protocols',
            'biohacking',
            'deep house music production',
            'construction project management'
        ),
        'sameAs' => array(
            'https://www.youtube.com/@KeystoneRecomposition',
            'https://www.youtube.com/@KeystoneProtocols',
            'https://www.youtube.com/channel/UCxURlqMNhAtxUTpdXmlOYaw',
            'https://keystonepossibilities.ca',
            'https://musicbrainz.org/label/30027d0e-6aeb-4704-8792-a031c936c62a',
            'https://audiomack.com/keystone-recomposition'
        ),
        'worksFor' => array(
            '@type' => 'Organization',
            'name' => 'Keystone Digital',
            'url' => 'https://keystonerecomposition.com'
        )
    );

    $json_person = wp_json_encode( $person_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );

    echo "<!-- Keystone Person Schema (Knowledge Panel) -->\n";
    echo "<script type=\"application/ld+json\">\n";
    echo $json_person . "\n";
    echo "</script>\n";
    echo "<!-- End Person Schema -->\n";
}
add_action( 'wp_head', 'keystone_recomposition_child_inject_schema' );

/**
 * General SEO Fixes: output noindex for specific archives and unrecognized query parameters.
 */
function keystone_recomposition_child_seo_noindex() {
    $should_noindex = false;

    // Check for specific archive types that should not be indexed
    if ( is_date() || is_author() || is_tag() || is_search() ) {
        $should_noindex = true;
    }

    // Check for unrecognized GET parameters
    if ( ! empty( $_GET ) ) {
        $allowed_params = array( 'page', 'paged', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'ref' );
        foreach ( $_GET as $key => $value ) {
            if ( ! in_array( $key, $allowed_params ) ) {
                $should_noindex = true;
                break;
            }
        }
    }

    if ( $should_noindex ) {
        echo "<meta name=\"robots\" content=\"noindex, follow\">\n";
    }
}
add_action( 'wp_head', 'keystone_recomposition_child_seo_noindex', 1 );

/**
 * Automatically inject VideoObject Schema for YouTube embeds in singular posts/pages
 */
function keystone_recomposition_child_youtube_schema() {
    if ( ! is_singular() ) {
        return;
    }

    global $post;
    $content = $post->post_content;

    // Regex to match youtube iframes or plain youtube links (often auto-embedded by WP)
    // Matches youtube.com/embed/ID, youtube.com/watch?v=ID, youtu.be/ID
    $pattern = '/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/i';

    if ( preg_match_all( $pattern, $content, $matches ) ) {
        $video_ids = array_unique( $matches[1] );

        foreach ( $video_ids as $video_id ) {
            $thumbnail_urls = array(
                'https://img.youtube.com/vi/' . $video_id . '/maxresdefault.jpg',
                'https://img.youtube.com/vi/' . $video_id . '/sddefault.jpg',
                'https://img.youtube.com/vi/' . $video_id . '/hqdefault.jpg',
                'https://img.youtube.com/vi/' . $video_id . '/default.jpg'
            );
            $embed_url = 'https://www.youtube.com/embed/' . $video_id;
            $content_url = 'https://www.youtube.com/watch?v=' . $video_id;

            $video_name = get_the_title();
            if ( empty( $video_name ) ) {
                $video_name = 'Video for ' . get_bloginfo( 'name' );
            }

            $video_description = wp_trim_words( wp_strip_all_tags( $content ), 40, '...' );
            if ( empty( $video_description ) ) {
                $video_description = $video_name;
            }

            $video_schema = array(
                '@context' => 'https://schema.org',
                '@type' => 'VideoObject',
                'name' => $video_name,
                'description' => $video_description,
                'thumbnailUrl' => $thumbnail_urls,
                'uploadDate' => get_the_date('c'),
                'embedUrl' => $embed_url,
                'contentUrl' => $content_url
            );

            $json_video_schema = wp_json_encode( $video_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );

            echo "<!-- Keystone Digital VideoObject Schema for YouTube -->\n";
            echo "<script type=\"application/ld+json\">\n";
            echo $json_video_schema . "\n";
            echo "</script>\n";
            echo "<!-- End VideoObject Schema -->\n";
        }
    }
}
add_action( 'wp_head', 'keystone_recomposition_child_youtube_schema' );

/**
 * Patch Structural Site Leaks (404/Redirect Errors)
 * Redirects 404 pages to the homepage with a 301 Moved Permanently status
 * to preserve link equity and resolve Google Search Console 404 indexing errors.
 * Skips sitemaps and XML requests to prevent Search Console crawl errors.
 */
function keystone_recomposition_child_404_redirect() {
    if ( is_404() ) {
        // Skip sitemap and XML requests to prevent indexing errors in GSC
        $request_uri = $_SERVER['REQUEST_URI'];
        if ( preg_match( '/sitemap.*\.xml$/i', $request_uri ) || preg_match( '/\.xml$/i', $request_uri ) ) {
            return;
        }
        wp_redirect( home_url(), 301 );
        exit;
    }
}
add_action( 'template_redirect', 'keystone_recomposition_child_404_redirect' );

/**
 * Programmatic SEO Filters: Fix Rank Math JSON-LD Typos, Duplications & Embeds on the fly
 */
add_filter( 'rank_math/json_ld', 'keystone_recomposition_clean_json_ld', 99, 2 );
function keystone_recomposition_clean_json_ld( $data, $jsonld ) {
    if ( empty( $data ) ) {
        return $data;
    }

    // 1. Serialize to JSON to safely perform replacements on both arrays and objects
    $is_object_mode = is_object( $data );
    $json = wp_json_encode( $data );
    if ( ! empty( $json ) ) {
        // Fix keystonepossibilities TLD typo
        $json = str_replace( 'keystonepossibilities.cao', 'keystonepossibilities.ca', $json );
        
        // Standardize Instagram post URLs
        $json = preg_replace( '/https?:\/\/(?:www\.)?instagram\.com\/p\/[a-zA-Z0-9_-]+/i', 'https://www.instagram.com/keystonerecomposition', $json );
        
        // Convert YouTube redirect/short URLs inside video schema to clean embed URLs
        $json = preg_replace( '/https?:\/\/youtu\.be\/([a-zA-Z0-9_-]{11})/i', 'https://www.youtube.com/embed/$1', $json );
        
        $decoded = json_decode( $json, !$is_object_mode );
        if ( ! empty( $decoded ) ) {
            $data = $decoded;
        }
    }

    // 2. Clean up duplicates in sameAs arrays/objects recursively
    keystone_recomposition_deduplicate_sameas( $data );

    return $data;
}

function keystone_recomposition_deduplicate_sameas( &$data ) {
    if ( is_array( $data ) ) {
        if ( isset( $data['sameAs'] ) && is_array( $data['sameAs'] ) ) {
            $data['sameAs'] = array_values( array_unique( $data['sameAs'] ) );
        }
        foreach ( $data as &$item ) {
            keystone_recomposition_deduplicate_sameas( $item );
        }
    } elseif ( is_object( $data ) ) {
        if ( isset( $data->sameAs ) && is_array( $data->sameAs ) ) {
            $data->sameAs = array_values( array_unique( $data->sameAs ) );
        }
        foreach ( get_object_vars( $data ) as $key => $val ) {
            keystone_recomposition_deduplicate_sameas( $data->$key );
        }
    }
}

/**
 * Programmatic Injection of Rank Math Metadata
 * Automates E-E-A-T optimization across project blog posts.
 */
add_filter( 'rank_math/frontend/description', 'keystone_recomposition_child_rankmath_description' );
function keystone_recomposition_child_rankmath_description( $description ) {
    if ( is_singular( 'post' ) ) {
        global $post;
        // If description is empty or default, generate a robust fallback
        if ( empty( $description ) ) {
            $excerpt = wp_trim_words( wp_strip_all_tags( $post->post_content ), 30, '...' );
            if ( ! empty( $excerpt ) ) {
                return $excerpt . ' - Expert metabolic health and structural engineering insights from Keystone Recomposition.';
            }
        }
    }
    return $description;
}

add_filter( 'rank_math/snippet/rich_snippet_article_entity', 'keystone_recomposition_child_rankmath_article_schema' );
function keystone_recomposition_child_rankmath_article_schema( $entity ) {
    if ( is_singular( 'post' ) ) {
        // Enhance Article Schema with E-E-A-T specifics
        $entity['author']['@type'] = 'Person';
        $entity['author']['name']  = 'Keystone Architect';
        $entity['author']['url']   = 'https://keystonerecomposition.com/about/';
        $entity['publisher']['@type'] = 'Organization';
        $entity['publisher']['name']  = 'Keystone Recomposition';
    }
    return $entity;
}
