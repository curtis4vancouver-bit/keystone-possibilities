<?php
/**
 * Astra Child Theme functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Astra Child for Keystone
 * @since 1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

if ( isset( $_GET['purge_all_caches'] ) ) {
    global $wpdb;
    $wpdb->query( "DELETE FROM $wpdb->options WHERE option_name LIKE '_transient_rank_math_sitemap_%' OR option_name LIKE '_transient_timeout_rank_math_sitemap_%'" );
    
    if ( function_exists( 'opcache_reset' ) ) {
        opcache_reset();
    }
    if ( function_exists( 'wp_cache_flush' ) ) {
        wp_cache_flush();
    }
    echo "CACHES PURGED SUCCESSFULLY";
    exit;
}

if ( isset( $_GET['get_post_inventory'] ) && $_GET['get_post_inventory'] === 'sovereign_view' ) {
    global $wpdb;
    $posts = $wpdb->get_results( 
        "SELECT ID, post_title, post_name, post_date, post_content 
         FROM $wpdb->posts 
         WHERE post_type = 'post' AND post_status = 'publish' 
         ORDER BY post_date DESC" 
    );
    
    $report = array();
    foreach ( $posts as $p ) {
        $youtube_id = '';
        // Check shortcode first (migration converted embeds to shortcodes)
        if ( preg_match( '~\[keystone_video\s+id=["\']([a-zA-Z0-9_-]+)["\']\]~', $p->post_content, $matches ) ) {
            $youtube_id = $matches[1];
        } elseif ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $p->post_content, $matches ) ) {
            $youtube_id = $matches[1];
        }
        // Also check post meta
        if ( empty( $youtube_id ) ) {
            $youtube_id = get_post_meta( $p->ID, 'keystone_youtube_id', true );
        }
        
        $report[] = array(
            'id' => $p->ID,
            'title' => $p->post_title,
            'slug' => $p->post_name,
            'date' => $p->post_date,
            'youtube_id' => $youtube_id,
            'has_meta' => ! empty( get_post_meta( $p->ID, 'keystone_youtube_id', true ) ),
            'length' => strlen( $p->post_content )
        );
    }
    
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( $report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
    exit;
}

if ( isset( $_GET['run_keystone_migration'] ) && $_GET['run_keystone_migration'] === 'sovereign_execute' ) {
    global $wpdb;
    
    // Fetch all published posts
    $posts = $wpdb->get_results( 
        "SELECT ID, post_title, post_name, post_date, post_content 
         FROM $wpdb->posts 
         WHERE post_type = 'post' AND post_status = 'publish' 
         ORDER BY post_date DESC" 
    );
    
    $migrated = array();
    $skipped = array();
    
    foreach ( $posts as $p ) {
        $post_id = intval( $p->ID );
        
        // Skip Post 1149 (the flagship blueprint)
        if ( $post_id === 1149 ) {
            $skipped[] = array(
                'id' => $post_id,
                'title' => $p->post_title,
                'reason' => 'Flagship blueprint skipped'
            );
            continue;
        }
        
        $post_content = $p->post_content;
        
        // 1. Identify YouTube Video ID using the robust regex
        $youtube_id = '';
        if ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $post_content, $matches ) ) {
            $youtube_id = $matches[1];
        }
        
        if ( empty( $youtube_id ) ) {
            $skipped[] = array(
                'id' => $post_id,
                'title' => $p->post_title,
                'reason' => 'No YouTube video detected'
            );
            continue;
        }
        
        // 2. Perform safe, clean, and idempotent content restructuring
        $cleaned_content = $post_content;
        
        // Remove existing custom sovereign disclaimers if any exist
        $cleaned_content = preg_replace( '/<!-- KEYSTONE_SOVEREIGN_MEDICAL_DISCLAIMER_START -->.*?<!-- KEYSTONE_SOVEREIGN_MEDICAL_DISCLAIMER_END -->/is', '', $cleaned_content );
        
        // Remove any legacy dual-column disclosures or generic medical disclaimers matching key superintendent keywords
        $cleaned_content = preg_replace( '/<div class="[^"]*wp-block-columns[^"]*".*?Medical Disclaimer.*?<\/div>\s*<\/div>\s*<\/div>/is', '', $cleaned_content );
        $cleaned_content = preg_replace( '/<div[^>]*class="[^"]*disclosure-card[^"]*".*?<\/div>/is', '', $cleaned_content );
        
        // Remove any existing play button shortcodes to prevent duplication
        $cleaned_content = preg_replace( '/\[keystone_video[^\]]*\]/i', '', $cleaned_content );
        
        // Remove Gutenberg Core Embed / YouTube blocks
        $cleaned_content = preg_replace( '/<!--\s+wp:embed\s+({.*?})?\s*-->.*?<!--\s+\/wp:embed\s*-->/is', '', $cleaned_content );
        $cleaned_content = preg_replace( '/<!--\s+wp:core-embed\/youtube\s+({.*?})?\s*-->.*?<!--\s+\/wp:core-embed\/youtube\s*-->/is', '', $cleaned_content );
        
        // Remove figure blocks containing youtube
        $cleaned_content = preg_replace( '/<figure class="[^"]*wp-block-embed-youtube[^"]*">.*?<\/figure>/is', '', $cleaned_content );
        $cleaned_content = preg_replace( '/<figure class="[^"]*wp-block-embed[^"]*is-provider-youtube[^"]*">.*?<\/figure>/is', '', $cleaned_content );
        
        // Remove raw YouTube iframe elements
        $cleaned_content = preg_replace( '/<iframe[^>]*youtube\.com\/embed\/[^>]*>.*?<\/iframe>/is', '', $cleaned_content );
        $cleaned_content = preg_replace( '/<iframe[^>]*youtube\.com\/[^>]*>.*?<\/iframe>/is', '', $cleaned_content );
        $cleaned_content = preg_replace( '/<iframe[^>]*youtu\.be\/[^>]*>.*?<\/iframe>/is', '', $cleaned_content );
        
        // Clean up any empty paragraphs or leftover markup around embeds
        $cleaned_content = preg_replace( '/<p>\s*(https?:\/\/(?:www\.)?(?:youtube\.com|youtu\.be)\/[^\s<>\'\"]*)\s*<\/p>/i', '', $cleaned_content );
        $cleaned_content = preg_replace( '/<p>\s*<!--\s*-->\s*<\/p>/i', '', $cleaned_content );
        
        // 3. Prepend the [keystone_video id="YOUTUBE_ID"] facade shortcode at the absolute top fold
        $cleaned_content = '[keystone_video id="' . esc_attr( $youtube_id ) . '"]' . "\n\n" . trim( $cleaned_content );
        
        // 4. Correct outbound Spotify links to the verified artist ID
        $cleaned_content = preg_replace(
            '~https://open\.spotify\.com/artist/(?!52v3Qe6Jo0hg764driOl5Y)[a-zA-Z0-9_-]+~i',
            'https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y',
            $cleaned_content
        );
        
        // 5. Append the clean centered Real Wayne Medical Disclaimer card at the bottom
        $disclaimer_card = "\n\n" . '<!-- KEYSTONE_SOVEREIGN_MEDICAL_DISCLAIMER_START -->' . "\n" .
                           '<div class="kr-medical-disclaimer-card" style="background-color: rgba(245, 158, 11, 0.03); border: 1px solid rgba(245, 158, 11, 0.15); padding: 25px; border-radius: 4px; margin-top: 50px; margin-bottom: 30px; text-align: center; max-width: 900px; margin-left: auto; margin-right: auto;">' . "\n" .
                           '    <h3 style="font-family: \'Outfit\', sans-serif; font-size: 0.95rem; color: #f59e0b; margin-top: 0; margin-bottom: 12px; letter-spacing: 0.08em; text-transform: uppercase;">⚠️ Medical Disclaimer</h3>' . "\n" .
                           '    <p style="font-family: \'Inter\', sans-serif; font-size: 0.85rem; color: #a3a3a3; line-height: 1.6; margin: 0; font-weight: 300; max-width: 750px; margin-left: auto; margin-right: auto;">' . "\n" .
                           '        This article is a personal case study for educational purposes only. Wayne Stevenson is a construction superintendent and metabolic researcher, not a doctor. Nothing here constitutes medical advice. GLP-1 / GIP therapies are powerful prescription drugs—always consult your licensed physician before starting or modifying any protocol.' . "\n" .
                           '    </p>' . "\n" .
                           '</div>' . "\n" .
                           '<!-- KEYSTONE_SOVEREIGN_MEDICAL_DISCLAIMER_END -->';
        
        $cleaned_content .= $disclaimer_card;
        
        // 6. Update wp_posts table with restructured content
        $wpdb->update(
            $wpdb->posts,
            array( 'post_content' => $cleaned_content ),
            array( 'ID' => $post_id )
        );
        
        // Clear post cache to force WordPress to load fresh DB rows
        clean_post_cache( $post_id );
        
        // 7. Inject GSC Video Object Metadata using WordPress Custom Fields
        $video_desc = wp_html_excerpt( wp_strip_all_tags( strip_shortcodes( $cleaned_content ) ), 150, '...' );
        if ( empty( $video_desc ) ) {
            $video_desc = esc_attr( $p->post_title ) . ' - High-performance health and longevity protocol details.';
        }
        
        update_post_meta( $post_id, 'keystone_youtube_id', $youtube_id );
        update_post_meta( $post_id, 'video_url', 'https://www.youtube.com/watch?v=' . $youtube_id );
        update_post_meta( $post_id, 'video_title', $p->post_title );
        update_post_meta( $post_id, 'video_description', $video_desc );
        update_post_meta( $post_id, 'video_duration', 'PT5M0S' ); // Standard ISO duration for historical posts
        update_post_meta( $post_id, 'video_upload_date', $p->post_date );
        
        $migrated[] = array(
            'id' => $post_id,
            'title' => $p->post_title,
            'youtube_id' => $youtube_id,
            'spotify_fixed' => true,
            'disclaimer_appended' => 'Real Wayne centered card',
            'facade_prepend' => 'Success'
        );
    }
    
    // Clear Object and OpCache layers
    if ( function_exists( 'wp_cache_flush' ) ) {
        wp_cache_flush();
    }
    if ( function_exists( 'opcache_reset' ) ) {
        opcache_reset();
    }
    
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( array(
        'status' => 'success',
        'message' => 'Keystone Sovereign Post-by-Post Migration Complete',
        'migrated_count' => count( $migrated ),
        'skipped_count' => count( $skipped ),
        'migrated_posts' => $migrated,
        'skipped_posts' => $skipped
    ), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
    exit;
}

if ( isset( $_GET['restore_mounjaro_post'] ) ) {
    $file_path = __DIR__ . '/mounjaro_backup.txt';
    if ( file_exists( $file_path ) ) {
        $content = file_get_contents( $file_path );
        $post_data = array(
            'ID'           => 1149,
            'post_content' => $content,
        );
        $res = wp_update_post( $post_data );
        if ( is_wp_error( $res ) ) {
            echo "ERROR RESTORING POST: " . $res->get_error_message();
        } else {
            echo "POST RESTORED SUCCESSFULLY: ID " . $res;
        }
    } else {
        echo "BACKUP FILE NOT FOUND AT: " . $file_path;
    }
    exit;
}

if ( isset( $_GET['list_revisions'] ) ) {
    $revisions = wp_get_post_revisions( 1149 );
    echo "=== REVISIONS FOR POST 1149 ===\n\n";
    foreach ( $revisions as $rev ) {
        echo "REVISION ID: " . $rev->ID . " | DATE: " . $rev->post_date . " | TITLE: " . $rev->post_title . "\n";
        echo "  CONTENT LENGTH: " . strlen( $rev->post_content ) . "\n";
        echo "  SNIPPET: " . substr( wp_strip_all_tags( $rev->post_content ), 0, 150) . "\n\n";
    }
    exit;
}

if ( isset( $_GET['restore_revision_id'] ) ) {
    $rev_id = intval( $_GET['restore_revision_id'] );
    $rev = wp_get_post_revision( $rev_id );
    if ( $rev ) {
        $content = $rev->post_content;
        
        $old_url = "https://open.spotify.com/artist/keystone-recomposition";
        $new_url = "https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y";
        $updated_content = str_replace( $old_url, $new_url, $content );
        
        $post_data = array(
            'ID'           => 1149,
            'post_content' => $updated_content,
        );
        $res = wp_update_post( $post_data );
        if ( is_wp_error( $res ) ) {
            echo "ERROR RESTORING REVISION: " . $res->get_error_message();
        } else {
            echo "REVISION " . $rev_id . " RESTORED & LINK UPDATED SUCCESSFULLY FOR POST 1149";
        }
    } else {
        echo "REVISION ID " . $rev_id . " NOT FOUND";
    }
    exit;
}

if ( isset( $_GET['check_rm_options'] ) ) {
    global $wpdb;
    $results = $wpdb->get_results( "SELECT option_name, option_value FROM $wpdb->options WHERE option_name LIKE '%rank-math%' OR option_name LIKE '%rank_math%' OR option_name LIKE '%schema%'" );
    echo "=== DB RANK MATH OPTIONS SCAN ===\n\n";
    foreach ( $results as $row ) {
        $val = maybe_unserialize( $row->option_value );
        $type = gettype( $val );
        echo "OPTION: " . $row->option_name . " | TYPE: " . $type . "\n";
        if ( $type === 'string' ) {
            echo "  VALUE: " . substr($val, 0, 150) . "\n";
        }
    }
    
    echo "\n=== RANK MATH SCHEMA POSTS SCAN ===\n\n";
    $schemas = get_posts( array(
        'post_type'   => 'rank_math_schema',
        'post_status' => 'any',
        'posts_per_page' => -1
    ) );
    echo "SCHEMAS COUNT: " . count($schemas) . "\n";
    foreach ( $schemas as $s ) {
        echo "SCHEMA ID: " . $s->ID . " | TITLE: " . $s->post_title . "\n";
        $meta = get_post_meta( $s->ID );
        foreach ( $meta as $key => $values ) {
            foreach ( $values as $val_raw ) {
                $val = maybe_unserialize( $val_raw );
                $type = gettype( $val );
                echo "  META KEY: " . $key . " | TYPE: " . $type . "\n";
                if ( $type === 'string' ) {
                    echo "    VALUE: " . substr($val, 0, 100) . "\n";
                }
            }
        }
    }
    
    echo "\n=== POST 1149 METADATA SCAN ===\n\n";
    $meta1149 = get_post_meta( 1149 );
    foreach ( $meta1149 as $key => $values ) {
        foreach ( $values as $val_raw ) {
            $val = maybe_unserialize( $val_raw );
            $type = gettype( $val );
            echo "META KEY: " . $key . " | TYPE: " . $type . "\n";
            if ( $type === 'string' ) {
                echo "  VALUE: " . substr($val, 0, 100) . "\n";
            }
        }
    }
    
    echo "\n=== POST 1149 SCHEMA META DETAIL ===\n\n";
    $val = get_post_meta( 1149, 'rank_math_schema_BlogPosting', true );
    echo "TYPE: " . gettype($val) . "\n";
    echo "VALUE:\n";
    print_r( $val );
    echo "\n";
    
    echo "\n=== SIMULATING RANK MATH ADMIN DATA ===\n\n";
    // Check if the class exists and what options it accesses
    if ( class_exists( 'RankMathPro\Schema\Admin' ) ) {
        echo "RankMathPro\\Schema\\Admin exists!\n";
    } else {
        echo "RankMathPro\\Schema\\Admin does NOT exist on frontend context.\n";
    }
    exit;
}

if ( isset( $_GET['delete_corrupt_post'] ) ) {
    $res = wp_delete_post( 807, true );
    echo "DELETE POST 807 RESULT: " . ($res ? "SUCCESS" : "FAILED") . "\n";
    exit;
}

/**
 * 1. Enqueue Parent Stylesheet and Google Fonts
 */
function astra_child_keystone_enqueue_styles() {
    // Enqueue parent Astra style
    wp_enqueue_style( 'astra-parent-theme-css', get_template_directory_uri() . '/style.css' );
    
    // Enqueue Child customized style
    wp_enqueue_style( 'astra-child-keystone-css', get_stylesheet_directory_uri() . '/style.css', array( 'astra-parent-theme-css' ), '1.0.3' );
    
    // Load typography fonts (Montserrat, Inter, Outfit)
    wp_enqueue_style( 'keystone-google-fonts', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@700&family=Outfit:wght@400;600;700;800&display=swap', array(), null );
}
add_action( 'wp_enqueue_scripts', 'astra_child_keystone_enqueue_styles' );

/**
 * 3. Preconnecting Web Fonts (Performance GSC optimization)
 */
function astra_child_keystone_resource_hints( $urls, $relation_type ) {
    if ( 'dns-prefetch' === $relation_type || 'preconnect' === $relation_type ) {
        $urls[] = 'https://fonts.googleapis.com';
        $urls[] = 'https://fonts.gstatic.com';
    }
    return $urls;
}
add_filter( 'wp_resource_hints', 'astra_child_keystone_resource_hints', 10, 2 );

/**
 * 3. Decharge Redundant Header Scripts (Optimizing PageSpeed score to 95+)
 */
function astra_child_keystone_clean_header() {
    // Remove emoji scripts
    remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
    remove_action( 'wp_print_styles', 'print_emoji_styles' );
    remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
    remove_action( 'admin_print_styles', 'print_emoji_styles' );
    
    // Remove shortlink tag
    remove_action( 'wp_head', 'wp_shortlink_wp_head', 10, 0 );
    
    // Remove XML-RPC RSD link
    remove_action( 'wp_head', 'rsd_link' );
    
    // Remove Windows Live Writer manifest
    remove_action( 'wp_head', 'wlwmanifest_link' );
}
add_action( 'init', 'astra_child_keystone_clean_header' );

/**
 * 4. Filter script loading tags to apply modern defer attribute flags to custom scripts
 */
function astra_child_keystone_add_defer_attribute( $tag, $handle ) {
    if ( 'keystone-lazy-player' !== $handle ) {
        return $tag;
    }
    return str_replace( ' src', ' defer="defer" src', $tag );
}
add_filter( 'script_loader_tag', 'astra_child_keystone_add_defer_attribute', 10, 2 );

/**
 * 5. Filter the single post title wrapper to ensure it's strictly an H1.
 */
add_filter( 'astra_the_title_before', 'keystone_recomposition_child_title_before', 10, 1 );
function keystone_recomposition_child_title_before( $before ) {
    if ( is_singular() ) {
        return preg_replace('~^<h[1-6]~i', '<h1', $before);
    }
    return $before;
}

add_filter( 'astra_the_title_after', 'keystone_recomposition_child_title_after', 10, 1 );
function keystone_recomposition_child_title_after( $after ) {
    if ( is_singular() ) {
        return preg_replace('~</h[1-6]>~i', '</h1>', $after);
    }
    return $after;
}

/**
 * 6. Filter the archive post title wrapper to ensure it's strictly an H2, preventing multiple H1s.
 */
add_filter( 'astra_the_post_title_before', 'keystone_recomposition_child_post_title_before', 10, 1 );
function keystone_recomposition_child_post_title_before( $before ) {
    if ( ! is_singular() ) {
        return preg_replace('~^<h[1-6]~i', '<h2', $before);
    }
    return $before;
}

add_filter( 'astra_the_post_title_after', 'keystone_recomposition_child_post_title_after', 10, 1 );
function keystone_recomposition_child_post_title_after( $after ) {
    if ( ! is_singular() ) {
        return preg_replace('~</h[1-6]>~i', '</h2>', $after);
    }
    return $after;
}

/**
 * 7. Inject Premium Organization & Person JSON-LD Schema (Knowledge Panel Anchor)
 */
function keystone_recomposition_child_inject_schema() {
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
            'https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y',
            'https://musicbrainz.org/label/30027d0e-6aeb-4704-8792-a031c936c62a',
            'https://audiomack.com/keystone-recomposition',
            'https://toolost.com',
            'https://www.tiktok.com/@keystonerecomposition'
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
            'https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y',
            'https://musicbrainz.org/label/30027d0e-6aeb-4704-8792-a031c936c62a',
            'https://audiomack.com/keystone-recomposition',
            'https://www.facebook.com/profile.php?id=61554185128555',
            'https://www.instagram.com/p/DO9FsCKj5Cb/',
            'https://www.tiktok.com/@keystonerecomposition'
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
 * 8. Dynamic, Robust, GSC-Compliant Standalone VideoObject Schema (Stored XSS Secure)
 * Extracts the primary article video and outputs exactly ONE premium schema object.
 */
function keystone_recomposition_child_youtube_schema() {
    if ( ! is_singular( 'post' ) ) {
        return;
    }

    global $post;
    if ( ! $post ) {
        return;
    }
    $post_id = $post->ID;

    // Try to get video URL or ID from post meta
    $video_url = get_post_meta( $post_id, 'video_url', true );
    $youtube_id = get_post_meta( $post_id, 'keystone_youtube_id', true );
    
    if ( empty( $video_url ) && ! empty( $youtube_id ) ) {
        $video_url = 'https://www.youtube.com/watch?v=' . $youtube_id;
    }

    // Fallback: search for [keystone_video id="..."] or plain youtube URL in content
    if ( empty( $video_url ) ) {
        $content = $post->post_content;
        if ( preg_match( '~\[keystone_video\s+id=["\']([a-zA-Z0-9_-]+)["\']]~', $content, $matches ) ) {
            $youtube_id = $matches[1];
            $video_url = 'https://www.youtube.com/watch?v=' . $youtube_id;
        } elseif ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $content, $matches ) ) {
            $youtube_id = $matches[1];
            $video_url = 'https://www.youtube.com/watch?v=' . $youtube_id;
        }
    }

    if ( empty( $youtube_id ) && ! empty( $video_url ) ) {
        if ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $video_url, $matches ) ) {
            $youtube_id = $matches[1];
        }
    }

    // If no video was detected at all, do not output schema
    if ( empty( $youtube_id ) ) {
        return;
    }

    // Determine high-resolution maxresdefault thumbnail
    $video_thumbnail = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
    
    // Get custom video details or fall back gracefully
    $video_name = get_post_meta( $post_id, 'video_title', true );
    if ( empty( $video_name ) ) {
        $video_name = get_the_title( $post_id ) . ' Video';
    }

    $video_description = get_post_meta( $post_id, 'video_description', true );
    if ( empty( $video_description ) ) {
        $excerpt_source = get_the_excerpt( $post_id );
        if ( empty( $excerpt_source ) ) {
            $excerpt_source = $post->post_content;
        }
        $clean_excerpt = wp_strip_all_tags( strip_shortcodes( $excerpt_source ) );
        $video_description = wp_html_excerpt( $clean_excerpt, 150, '...' );
    }
    if ( empty( $video_description ) ) {
        $video_description = esc_attr( get_the_title( $post_id ) ) . ' - High-performance health and longevity protocol details.';
    }

    $video_duration = get_post_meta( $post_id, 'video_duration', true );
    if ( empty( $video_duration ) ) {
        $video_duration = get_post_meta( $post_id, 'keystone_video_duration', true );
    }
    $duration_iso = 'PT5M0S'; // Default fallback 5 minutes
    if ( ! empty( $video_duration ) ) {
        // Parse time to ISO 8601
        $video_duration = trim( $video_duration );
        if ( stripos( $video_duration, 'PT' ) === 0 ) {
            $duration_iso = $video_duration;
        } else {
            $hours = 0; $minutes = 0; $seconds = 0;
            if ( is_numeric( $video_duration ) ) {
                $total_seconds = intval( $video_duration );
                $hours = floor( $total_seconds / 3600 );
                $minutes = floor( ( $total_seconds / 60 ) % 60 );
                $seconds = $total_seconds % 60;
            } elseif ( preg_match( '~^(?:(\d+):)?(\d+):(\d+)$~', $video_duration, $matches ) ) {
                if ( count( $matches ) === 4 && $matches[1] !== '' ) {
                    $hours = intval( $matches[1] );
                    $minutes = intval( $matches[2] );
                    $seconds = intval( $matches[3] );
                } else {
                    $minutes = intval( $matches[2] );
                    $seconds = intval( $matches[3] );
                }
            }
            $duration_iso = 'PT';
            if ( $hours > 0 ) $duration_iso .= $hours . 'H';
            if ( $minutes > 0 ) $duration_iso .= $minutes . 'M';
            if ( $seconds > 0 || ( $hours === 0 && $minutes === 0 ) ) $duration_iso .= $seconds . 'S';
        }
    }

    $video_upload_date = get_post_meta( $post_id, 'video_upload_date', true );
    if ( empty( $video_upload_date ) ) {
        $video_upload_date = get_the_date( 'c', $post_id );
    } else {
        $converted_time = strtotime( $video_upload_date );
        $video_upload_date = ( $converted_time !== false ) ? date( 'c', $converted_time ) : get_the_date( 'c', $post_id );
    }

    $video_schema = array(
        '@context' => 'https://schema.org',
        '@type' => 'VideoObject',
        'name' => esc_attr( $video_name ),
        'description' => esc_attr( $video_description ),
        'thumbnailUrl' => esc_url( $video_thumbnail ),
        'uploadDate' => esc_attr( $video_upload_date ),
        'embedUrl' => "https://www.youtube.com/embed/{$youtube_id}",
        'contentUrl' => "https://www.youtube.com/watch?v={$youtube_id}",
        'duration' => esc_attr( $duration_iso ),
        'publisher' => array(
            '@type' => 'Organization',
            'name' => 'Keystone Protocols',
            'logo' => array(
                '@type' => 'ImageObject',
                'url' => 'https://keystonerecomposition.com/wp-content/uploads/logo.png'
            )
        )
    );

    $json_video_schema = wp_json_encode( $video_schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT );

    echo "\n<!-- Keystone Digital VideoObject Schema for YouTube -->\n";
    echo "<script type=\"application/ld+json\">\n";
    echo $json_video_schema . "\n";
    echo "</script>\n";
    echo "<!-- End VideoObject Schema -->\n\n";
}
add_action( 'wp_head', 'keystone_recomposition_child_youtube_schema', 20 );

/**
 * 9. Hook custom media metadata into Rank Math PRO's Video Sitemap Generator
 */
add_filter( 'rank_math/sitemap/video/post', function( $video, $post_id ) {
    if ( ! is_array( $video ) ) {
        return $video;
    }
    $youtube_id = get_post_meta( $post_id, 'keystone_youtube_id', true );
    
    // Fallback: search for [keystone_video id="..."] or youtube embed in content
    if ( empty( $youtube_id ) ) {
        $post = get_post( $post_id );
        if ( $post ) {
            if ( preg_match( '~\[keystone_video\s+id=["\']([a-zA-Z0-9_-]+)["\']]~', $post->post_content, $matches ) ) {
                $youtube_id = $matches[1];
            } elseif ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $post->post_content, $matches ) ) {
                $youtube_id = $matches[1];
            }
        }
    }
    
    if ( ! empty( $youtube_id ) ) {
        $video['thumbnail_loc'] = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
        $video['title']         = get_the_title( $post_id );
        
        $excerpt = get_the_excerpt( $post_id );
        if ( empty( $excerpt ) ) {
            $post = get_post( $post_id );
            if ( $post ) {
                $excerpt = wp_trim_words( wp_strip_all_tags( strip_shortcodes( $post->post_content ) ), 40, '...' );
            }
        }
        $video['description']   = $excerpt;
        $video['player_loc']    = "https://www.youtube-nocookie.com/embed/{$youtube_id}";
        $video['uploader']      = "Wayne Stevenson";
        $video['uploader_info'] = "https://keystonerecomposition.com/";
    }
    
    return $video;
}, 10, 2 );

/**
 * 10. Deduplicate Rank Math JSON-LD Schema Graph & Auto-detected Videos
 */
add_filter( 'rank_math/json_ld', function( $data, $jsonld ) {
    if ( ! is_array( $data ) ) {
        return $data;
    }
    foreach ( $data as $key => $val ) {
        if ( in_array( strtolower( $key ), array( 'video', 'videoobject' ) ) ) {
            unset( $data[$key] );
        }
    }
    if ( isset( $data['@graph'] ) && is_array( $data['@graph'] ) ) {
        $other_nodes = array();
        foreach ( $data['@graph'] as $node ) {
            if ( isset( $node['@type'] ) ) {
                $types = (array) $node['@type'];
                $has_video = false;
                foreach ( $types as $t ) {
                    if ( strtolower( $t ) === 'videoobject' ) {
                        $has_video = true;
                        break;
                    }
                }
                if ( ! $has_video ) {
                    $other_nodes[] = $node;
                }
            } else {
                $other_nodes[] = $node;
            }
        }
        $data['@graph'] = $other_nodes;
    }
    return $data;
}, 999, 2 );

/**
 * 10.5 Nuclear Standalone Video Schema Deduplicator
 */
add_action( 'template_redirect', function() {
    if ( is_singular( 'post' ) ) {
        ob_start( function( $html ) {
            $html = preg_replace(
                '~<script type=["\']application/ld\+json["\']>[^\n]*?"@type"\s*:\s*"VideoObject"[^\n]*?</script>~i',
                '',
                $html
            );
            return $html;
        } );
    }
} );

/**
 * 11. General SEO Fixes: output noindex for tag, date, author archives and query parameters
 */
function keystone_recomposition_child_seo_noindex() {
    $should_noindex = false;

    // Only noindex archive types that create duplicate content
    if ( is_date() || is_author() || is_tag() || is_search() ) {
        $should_noindex = true;
    }

    // Only noindex pages with truly junk query params — NOT internal WP or tracking params
    if ( ! empty( $_GET ) && ! is_singular() ) {
        $allowed_params = array(
            'page', 'paged', 'p', 'page_id', 'cat', 'tag',
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
            'gclid', 'fbclid', 'ref', 'mc_cid', 'mc_eid',
            // Internal Keystone endpoints
            'get_post_inventory', 'purge_all_caches', 'run_instant_indexing',
            'run_keystone_migration', 'heal_video_meta', 'check_rm_options',
            'keystone_video_sitemap',
            // Rank Math / WP internals
            'replytocom', 'preview', 'preview_id', 'preview_nonce'
        );
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
 * 12. Patch Structural Site Leaks (404/Redirect Errors)
 */
function keystone_recomposition_child_404_redirect() {
    if ( is_404() ) {
        wp_redirect( home_url(), 301 );
        exit;
    }
}
add_action( 'template_redirect', 'keystone_recomposition_child_404_redirect' );

/**
 * 13. Shortcode to render our fast, PageSpeed-optimized lazy YouTube/Spotify media facade
 */
function keystone_lazy_video_shortcode( $atts ) {
    $args = shortcode_atts( array(
        'id'   => '',
        'type' => 'youtube',
        'placeholder_img' => '',
    ), $atts );

    if ( empty( $args['id'] ) ) {
        return '<p style="color: #FC8181; font-family: monospace;">[Error] Media Asset ID is missing.</p>';
    }

    $media_id   = esc_attr( $args['id'] );
    $media_type = esc_attr( strtolower( $args['type'] ) );
    
    $bg_img = '';
    if ( ! empty( $args['placeholder_img'] ) ) {
        $bg_img = esc_url( $args['placeholder_img'] );
    } elseif ( $media_type === 'youtube' ) {
        $bg_img = 'https://img.youtube.com/vi/' . $media_id . '/maxresdefault.jpg';
    } else {
        $bg_img = 'https://keystonerecomposition.com/wp-content/uploads/video-placeholder.jpg';
    }

    wp_enqueue_script( 'keystone-lazy-player', get_stylesheet_directory_uri() . '/js/lazy-player.js', array(), '1.0.0', true );

    ob_start();
    ?>
    <div class="luxury-video-facade" 
         data-video-id="<?php echo $media_id; ?>" 
         data-video-type="<?php echo $media_type; ?>" 
         role="region" 
         aria-label="Video Player Placeholder">
        
        <div class="facade-background" style="background-image: url('<?php echo $bg_img; ?>');"></div>
        <div class="facade-overlay"></div>
        
        <button class="play-button" aria-label="Play Embedded Video">
            <svg class="play-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
            </svg>
        </button>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode( 'keystone_video', 'keystone_lazy_video_shortcode' );

/**
 * 14. Inject Premium Grid Alignment Custom CSS directly in wp_head
 */
function keystone_recomposition_child_inject_custom_css() {
    ?>
    <style id="keystone-protocols-premium-grid">
    .ast-blog-layout-4-grid .ast-row,
    .ast-blog-layout-4-grid .infinite-wrap {
      display: grid !important;
      grid-template-columns: repeat(2, 1fr) !important;
      column-gap: 45px !important;
      row-gap: 55px !important;
    }
    @media (max-width: 768px) {
      .ast-blog-layout-4-grid .ast-row,
      .ast-blog-layout-4-grid .infinite-wrap {
        grid-template-columns: 1fr !important;
        row-gap: 45px !important;
      }
    }
    .ast-blog-layout-4-grid .ast-row article,
    .ast-blog-layout-4-grid .infinite-wrap article {
      width: 100% !important;
      min-width: 0 !important;
      float: none !important;
      margin: 0px !important;
      display: flex !important;
      flex-direction: column !important;
      height: 100% !important;
      background: #080808 !important;
      border: 1px solid rgba(196, 162, 101, 0.1) !important;
      padding: 0px !important;
      transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    .ast-blog-layout-4-grid .ast-row article:hover,
    .ast-blog-layout-4-grid .infinite-wrap article:hover {
      border-color: rgba(196, 162, 101, 0.3) !important;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
    .ast-blog-layout-4-grid .ast-row article .ast-article-inner,
    .ast-blog-layout-4-grid .infinite-wrap article .ast-article-inner {
      flex: 1 1 0% !important;
      display: flex !important;
      flex-direction: column !important;
      height: 100% !important;
      padding: 0px !important;
      margin: 0px !important;
    }
    .ast-blog-layout-4-grid .ast-row article .post-thumb,
    .ast-blog-layout-4-grid .infinite-wrap article .post-thumb {
      overflow: hidden !important;
      margin: 0px !important;
      padding: 0px !important;
      border-bottom: 2px solid rgba(196, 162, 101, 0.15) !important;
    }
    .ast-blog-layout-4-grid .ast-row article .post-thumb img,
    .ast-blog-layout-4-grid .infinite-wrap article .post-thumb img {
      height: 320px !important;
      width: 100% !important;
      object-fit: cover !important;
      border-radius: 0px !important;
      transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1) !important;
    }
    .ast-blog-layout-4-grid .ast-row article:hover .post-thumb img,
    .ast-blog-layout-4-grid .infinite-wrap article:hover .post-thumb img {
      transform: scale(1.04) !important;
    }
    .ast-blog-layout-4-grid .ast-row article .post-content,
    .ast-blog-layout-4-grid .infinite-wrap article .post-content {
      flex: 1 1 0% !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: flex-start !important;
      padding: 30px 25px 25px 25px !important;
      background: #080808 !important;
    }
    .ast-blog-layout-4-grid h2.entry-title {
      font-size: 20px !important;
      line-height: 1.35 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      margin: 10px 0 15px 0 !important;
      font-family: 'Outfit', sans-serif !important;
      font-weight: 700 !important;
    }
    .ast-blog-layout-4-grid h2.entry-title a {
      color: #c4a265 !important;
      text-decoration: none !important;
      font-size: 20px !important;
      line-height: 1.35 !important;
      letter-spacing: 1.5px !important;
      transition: color 0.3s ease !important;
    }
    .ast-blog-layout-4-grid h2.entry-title a:hover {
      color: #ffffff !important;
    }
    .ast-blog-layout-4-grid .entry-meta, 
    .ast-blog-layout-4-grid .entry-meta a {
      color: #737373 !important;
      font-size: 11px !important;
      text-transform: uppercase !important;
      letter-spacing: 1px !important;
      text-decoration: none !important;
    }
    .ast-blog-layout-4-grid .entry-meta a:hover {
      color: #c4a265 !important;
    }
    .ast-blog-layout-4-grid .ast-blog-single-element {
      margin-bottom: 12px !important;
    }
    .ast-blog-layout-4-grid .entry-content,
    .ast-blog-layout-4-grid .entry-content p {
      color: #a3a3a3 !important;
      font-size: 13px !important;
      line-height: 1.7 !important;
      font-weight: 300 !important;
      letter-spacing: 0.5px !important;
      margin-bottom: 20px !important;
    }
    
    /* Single Post Header Refinements (Quiet Luxury) */
    .single-post .entry-header {
      text-align: center !important;
      margin-top: 15px !important;
      margin-bottom: 35px !important;
      max-width: 850px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      padding: 0 10px !important;
    }
    .single-post h1.entry-title {
      font-family: 'Outfit', sans-serif !important;
      font-size: clamp(24px, 3.8vw, 36px) !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.025em !important;
      color: #ffffff !important;
      line-height: 1.25 !important;
      margin-bottom: 15px !important;
    }
    .single-post .entry-meta,
    .single-post .entry-meta a {
      font-family: 'Outfit', sans-serif !important;
      font-size: 11px !important;
      text-transform: uppercase !important;
      letter-spacing: 0.15em !important;
      color: #c4a265 !important;
      text-decoration: none !important;
    }
    .single-post .entry-meta .posted-on {
      color: #a3a3a3 !important;
    }
    .single-post .entry-meta .author-name {
      color: #00ced1 !important;
      font-weight: 600 !important;
    }
    </style>
    <?php
}
add_action( 'wp_head', 'keystone_recomposition_child_inject_custom_css', 150 );

/**
 * 15. Automatically Append YouTube Subscribe Buttons to All Pages and Posts
 */
function keystone_recomposition_child_append_subscribe_buttons( $content ) {
    if ( is_singular() && is_main_query() ) {
        if ( strpos( $content, 'sub_confirmation=1' ) === false ) {
            $subscribe_html = '
            <div class="keystone-global-subscribe-buttons" style="display:flex; flex-wrap:wrap; gap:15px; margin-top:40px; margin-bottom: 40px; justify-content: center; align-items: center;">
                <a href="https://www.youtube.com/@keystonerecomposition?sub_confirmation=1" target="_blank" rel="noopener" style="background-color:#cc0000; color:#fff; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 700; font-family: Outfit, sans-serif; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.3s ease;">&#9654; Subscribe: Keystone Recomposition</a>
                <a href="https://www.youtube.com/@keystoneprotocols?sub_confirmation=1" target="_blank" rel="noopener" style="background-color:#cc0000; color:#fff; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 700; font-family: Outfit, sans-serif; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.3s ease;">&#9654; Subscribe: Keystone Protocols</a>
            </div>';
            $content .= $subscribe_html;
        }
    }
    return $content;
}
add_filter( 'the_content', 'keystone_recomposition_child_append_subscribe_buttons', 99 );

/**
 * 16. Fallback Post Thumbnail to YouTube Video Thumbnail
 */
add_filter( 'get_post_metadata', 'keystone_fallback_thumbnail_id', 10, 4 );
function keystone_fallback_thumbnail_id( $value, $object_id, $meta_key, $single ) {
    if ( '_thumbnail_id' === $meta_key ) {
        remove_filter( 'get_post_metadata', 'keystone_fallback_thumbnail_id', 10 );
        $real_id = get_post_meta( $object_id, '_thumbnail_id', true );
        add_filter( 'get_post_metadata', 'keystone_fallback_thumbnail_id', 10, 4 );
        
        if ( ! empty( $real_id ) ) {
            return $value;
        }
        
        $youtube_id = get_post_meta( $object_id, 'keystone_youtube_id', true );
        if ( empty( $youtube_id ) ) {
            $post_obj = get_post( $object_id );
            if ( $post_obj && ! empty( $post_obj->post_content ) ) {
                if ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=|embed/)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $post_obj->post_content, $matches ) ) {
                    $youtube_id = $matches[1];
                }
            }
        }
        
        if ( ! empty( $youtube_id ) ) {
            global $keystone_fake_thumbnails;
            if ( ! isset( $keystone_fake_thumbnails ) ) {
                $keystone_fake_thumbnails = array();
            }
            $fake_id = - (int) $object_id;
            $keystone_fake_thumbnails[ $fake_id ] = $youtube_id;
            return $fake_id;
        }
    }
    return $value;
}

add_filter( 'wp_get_attachment_image_src', 'keystone_fake_thumbnail_src', 10, 4 );
function keystone_fake_thumbnail_src( $image, $attachment_id, $size, $icon ) {
    global $keystone_fake_thumbnails;
    if ( $attachment_id < 0 && isset( $keystone_fake_thumbnails[ $attachment_id ] ) ) {
        $youtube_id = $keystone_fake_thumbnails[ $attachment_id ];
        $url = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
        return array( $url, 1280, 720, false );
    }
    return $image;
}

add_filter( 'wp_get_attachment_image', 'keystone_fake_thumbnail_image', 10, 5 );
function keystone_fake_thumbnail_image( $html, $attachment_id, $size, $icon, $attr ) {
    global $keystone_fake_thumbnails;
    if ( $attachment_id < 0 && isset( $keystone_fake_thumbnails[ $attachment_id ] ) ) {
        $youtube_id = $keystone_fake_thumbnails[ $attachment_id ];
        $url = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
        $alt = isset($attr['alt']) ? $attr['alt'] : '';
        $class = isset($attr['class']) ? $attr['class'] : 'attachment-post-thumbnail size-post-thumbnail wp-post-image';
        return '<img src="' . esc_url( $url ) . '" alt="' . esc_attr( $alt ) . '" class="' . esc_attr( $class ) . '" decoding="async" loading="lazy" style="width:100%; height:100%; object-fit:cover;" />';
    }
    return $html;
}

/**
 * 17. Custom Video Sitemap Generator (Bypasses Rank Math)
 * Generates a Google-compliant video sitemap XML at /keystone-video-sitemap.xml
 * Bypasses Rank Math's broken default modules while perfectly integrating into the Rank Math Sitemap Index.
 */

// Register the custom rewrite rule for clean URL
add_action( 'init', 'keystone_video_sitemap_rewrite' );
function keystone_video_sitemap_rewrite() {
    add_rewrite_rule( '^keystone-video-sitemap\.xml$', 'index.php?keystone_video_sitemap=1', 'top' );
    // Check if flushed already, if not, flush once dynamically
    if ( ! get_option( 'keystone_vsm_flushed_v2_final' ) ) {
        flush_rewrite_rules();
        update_option( 'keystone_vsm_flushed_v2_final', true );
    }
}

// Register the query variable so WordPress recognizes it
add_filter( 'query_vars', 'keystone_video_sitemap_query_vars' );
function keystone_video_sitemap_query_vars( $vars ) {
    $vars[] = 'keystone_video_sitemap';
    return $vars;
}

// Serve the video sitemap XML
add_action( 'template_redirect', 'keystone_serve_video_sitemap' );
function keystone_serve_video_sitemap() {
    $is_sitemap = get_query_var( 'keystone_video_sitemap' );
    if ( ! $is_sitemap && isset( $_GET['keystone_video_sitemap'] ) ) {
        $is_sitemap = true;
    }
    if ( ! $is_sitemap ) {
        return;
    }

    header( 'Content-Type: application/xml; charset=UTF-8' );
    header( 'X-Robots-Tag: noindex, follow' );

    $posts = get_posts( array(
        'post_type'      => 'post',
        'post_status'    => 'publish',
        'posts_per_page' => -1,
        'orderby'        => 'date',
        'order'          => 'DESC',
    ) );

    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' . "\n";
    echo '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">' . "\n";

    $video_count = 0;
    foreach ( $posts as $p ) {
        $post_id = $p->ID;
        
        // Skip specific page/posts if needed
        $youtube_id = get_post_meta( $post_id, 'keystone_youtube_id', true );
        if ( empty( $youtube_id ) ) {
            if ( preg_match( '~\[keystone_video\s+id=["\']([a-zA-Z0-9_-]+)["\']]~', $p->post_content, $matches ) ) {
                $youtube_id = $matches[1];
            } elseif ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $p->post_content, $matches ) ) {
                $youtube_id = $matches[1];
            }
        }
        if ( empty( $youtube_id ) ) { 
            continue; 
        }

        $permalink = get_permalink( $post_id );
        
        // Symmetrical metadata extraction
        $title = get_post_meta( $post_id, 'video_title', true );
        if ( empty( $title ) ) { 
            $title = get_the_title( $post_id ); 
        }
        $title = mb_substr( wp_strip_all_tags( $title ), 0, 100 );

        $description = get_post_meta( $post_id, 'video_description', true );
        if ( empty( $description ) ) {
            $excerpt = get_the_excerpt( $post_id );
            if ( empty( $excerpt ) ) {
                $excerpt = wp_trim_words( wp_strip_all_tags( strip_shortcodes( $p->post_content ) ), 40, '...' );
            }
            $description = $excerpt;
        }
        $description = mb_substr( wp_strip_all_tags( $description ), 0, 2048 );
        if ( empty( $description ) ) {
            $description = $title . ' - High-performance health and longevity protocol details.';
        }

        $thumbnail_url = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
        $player_url    = "https://www.youtube.com/embed/{$youtube_id}";
        $content_url   = "https://www.youtube.com/watch?v={$youtube_id}";
        $upload_date   = get_the_date( 'c', $post_id );

        echo "  <url>\n";
        echo "    <loc>" . esc_url( $permalink ) . "</loc>\n";
        echo "    <video:video>\n";
        echo "      <video:thumbnail_loc>" . esc_url( $thumbnail_url ) . "</video:thumbnail_loc>\n";
        echo "      <video:title><![CDATA[" . $title . "]]></video:title>\n";
        echo "      <video:description><![CDATA[" . $description . "]]></video:description>\n";
        echo "      <video:content_loc>" . esc_url( $content_url ) . "</video:content_loc>\n";
        echo "      <video:player_loc>" . esc_url( $player_url ) . "</video:player_loc>\n";
        echo "      <video:publication_date>" . esc_attr( $upload_date ) . "</video:publication_date>\n";
        echo "      <video:family_friendly>yes</video:family_friendly>\n";
        echo "      <video:uploader info=\"https://keystonerecomposition.com/\">Wayne Stevenson</video:uploader>\n";
        echo "      <video:live>no</video:live>\n";
        echo "    </video:video>\n";
        echo "  </url>\n";
        $video_count++;
    }

    echo "</urlset>\n";
    echo "<!-- Keystone Sovereign Video Sitemap - " . $video_count . " videos found -->\n";
    exit;
}

// Register the video sitemap in Rank Math's main sitemap index dynamically
add_filter( 'rank_math/sitemap/index', 'keystone_add_video_sitemap_to_index' );
function keystone_add_video_sitemap_to_index( $index ) {
    $sitemap_url = home_url( '/keystone-video-sitemap.xml' );
    $index .= "\t<sitemap>\n";
    $index .= "\t\t<loc>" . esc_url( $sitemap_url ) . "</loc>\n";
    $index .= "\t\t<lastmod>" . date( 'c' ) . "</lastmod>\n";
    $index .= "\t</sitemap>\n";
    return $index;
}

// Disable Rank Math sitemap caching completely to ensure dynamic updates reflect immediately
add_filter( 'rank_math/sitemap/enable_caching', '__return_false' );

// Banish Rank Math's faulty built-in video sitemap generator output to prevent double sitemap conflicts
add_filter( 'rank_math/sitemap/video/content', '__return_empty_string', 999 );

// Add custom video sitemap link directly to the virtual robots.txt
add_filter( 'robots_txt', 'keystone_add_video_sitemap_to_robots', 99, 2 );
function keystone_add_video_sitemap_to_robots( $output, $public ) {
    $sitemap_url = home_url( '/keystone-video-sitemap.xml' );
    $output .= PHP_EOL . 'Sitemap: ' . $sitemap_url . PHP_EOL;
    return $output;
}

/**
 * 18. Auto-Heal Video Meta — Backfills keystone_youtube_id for ALL posts
 * Trigger: https://keystonerecomposition.com/?heal_video_meta=sovereign_execute
 * Scans every published post, extracts YouTube ID from [keystone_video] shortcode
 * or raw embed, and writes post meta if missing. This fixes the VideoObject schema
 * and video sitemap for posts that were missed during migration.
 */
if ( isset( $_GET['heal_video_meta'] ) && $_GET['heal_video_meta'] === 'sovereign_execute' ) {
    global $wpdb;
    
    $posts = $wpdb->get_results(
        "SELECT ID, post_title, post_content 
         FROM $wpdb->posts 
         WHERE post_type = 'post' AND post_status = 'publish' 
         ORDER BY post_date DESC"
    );
    
    $healed = array();
    $already_ok = array();
    $no_video = array();
    
    foreach ( $posts as $p ) {
        $post_id = intval( $p->ID );
        $existing_yt = get_post_meta( $post_id, 'keystone_youtube_id', true );
        
        // Extract YouTube ID from content
        $youtube_id = '';
        if ( preg_match( '~\[keystone_video\s+id=["\']([a-zA-Z0-9_-]+)["\']\]~', $p->post_content, $matches ) ) {
            $youtube_id = $matches[1];
        } elseif ( preg_match( '~(?:youtube\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/|youtube\.com/shorts/)([^"&?/ ]{11})~i', $p->post_content, $matches ) ) {
            $youtube_id = $matches[1];
        }
        
        if ( empty( $youtube_id ) ) {
            $no_video[] = array( 'id' => $post_id, 'title' => $p->post_title );
            continue;
        }
        
        if ( ! empty( $existing_yt ) && $existing_yt === $youtube_id ) {
            $already_ok[] = array( 'id' => $post_id, 'yt' => $youtube_id );
            continue;
        }
        
        // Backfill all video meta
        $video_desc = wp_html_excerpt( wp_strip_all_tags( strip_shortcodes( $p->post_content ) ), 150, '...' );
        if ( empty( $video_desc ) ) {
            $video_desc = esc_attr( $p->post_title ) . ' - High-performance health and longevity protocol details.';
        }
        
        update_post_meta( $post_id, 'keystone_youtube_id', $youtube_id );
        update_post_meta( $post_id, 'video_url', 'https://www.youtube.com/watch?v=' . $youtube_id );
        update_post_meta( $post_id, 'video_title', $p->post_title );
        update_post_meta( $post_id, 'video_description', $video_desc );
        
        // Preserve existing duration if set, otherwise default
        $existing_dur = get_post_meta( $post_id, 'video_duration', true );
        if ( empty( $existing_dur ) ) {
            update_post_meta( $post_id, 'video_duration', 'PT5M0S' );
        }
        
        $existing_date = get_post_meta( $post_id, 'video_upload_date', true );
        if ( empty( $existing_date ) ) {
            $post_obj = get_post( $post_id );
            update_post_meta( $post_id, 'video_upload_date', $post_obj->post_date );
        }
        
        $healed[] = array(
            'id' => $post_id,
            'title' => $p->post_title,
            'youtube_id' => $youtube_id,
            'had_existing' => ! empty( $existing_yt ),
            'old_yt' => $existing_yt
        );
    }
    
    // Clear caches
    if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }
    if ( function_exists( 'opcache_reset' ) ) { opcache_reset(); }
    
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( array(
        'status' => 'success',
        'message' => 'Video Meta Auto-Heal Complete',
        'healed_count' => count( $healed ),
        'already_ok_count' => count( $already_ok ),
        'no_video_count' => count( $no_video ),
        'healed_posts' => $healed,
        'no_video_posts' => $no_video
    ), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
    exit;
}

/**
 * 19. Read Single Post — Full content + meta for agent processing
 * Trigger: https://keystonerecomposition.com/?read_post_full=POST_ID
 */
if ( isset( $_GET['read_post_full'] ) ) {
    $post_id = intval( $_GET['read_post_full'] );
    $p = get_post( $post_id );
    if ( ! $p || $p->post_status !== 'publish' ) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode( array( 'error' => 'Post not found or not published', 'id' => $post_id ) );
        exit;
    }
    
    $meta = get_post_meta( $post_id );
    $flat_meta = array();
    foreach ( $meta as $key => $values ) {
        $flat_meta[ $key ] = ( count( $values ) === 1 ) ? $values[0] : $values;
    }
    
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( array(
        'id'             => $p->ID,
        'title'          => $p->post_title,
        'slug'           => $p->post_name,
        'date'           => $p->post_date,
        'content'        => $p->post_content,
        'excerpt'        => $p->post_excerpt,
        'permalink'      => get_permalink( $post_id ),
        'content_length' => strlen( $p->post_content ),
        'meta'           => $flat_meta
    ), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
    exit;
}

/**
 * 20. Update Single Post — Sovereign one-by-one blog enhancement
 * Trigger: POST to https://keystonerecomposition.com/?update_post_sovereign=1
 * Body: JSON with post_id, content, excerpt, meta_description, focus_keyword,
 *       video_duration, video_description, og_image
 */
if ( isset( $_GET['update_post_sovereign'] ) && $_SERVER['REQUEST_METHOD'] === 'POST' ) {
    $raw = file_get_contents('php://input');
    $data = json_decode( $raw, true );
    
    if ( ! $data || empty( $data['post_id'] ) ) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode( array( 'error' => 'Invalid JSON or missing post_id' ) );
        exit;
    }
    
    $post_id = intval( $data['post_id'] );
    $p = get_post( $post_id );
    if ( ! $p || $p->post_status !== 'publish' ) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode( array( 'error' => 'Post not found', 'id' => $post_id ) );
        exit;
    }
    
    $updated = array();
    
    // Update post content if provided
    if ( ! empty( $data['content'] ) ) {
        wp_update_post( array( 'ID' => $post_id, 'post_content' => $data['content'] ) );
        $updated[] = 'content';
    }
    
    // Update excerpt if provided
    if ( ! empty( $data['excerpt'] ) ) {
        wp_update_post( array( 'ID' => $post_id, 'post_excerpt' => $data['excerpt'] ) );
        $updated[] = 'excerpt';
    }
    
    // Update video duration
    if ( ! empty( $data['video_duration'] ) ) {
        update_post_meta( $post_id, 'video_duration', sanitize_text_field( $data['video_duration'] ) );
        $updated[] = 'video_duration';
    }
    
    // Update video description
    if ( ! empty( $data['video_description'] ) ) {
        update_post_meta( $post_id, 'video_description', sanitize_text_field( $data['video_description'] ) );
        $updated[] = 'video_description';
    }
    
    // Update Rank Math meta description
    if ( ! empty( $data['meta_description'] ) ) {
        update_post_meta( $post_id, 'rank_math_description', sanitize_text_field( $data['meta_description'] ) );
        $updated[] = 'rank_math_description';
    }
    
    // Update Rank Math focus keyword
    if ( ! empty( $data['focus_keyword'] ) ) {
        update_post_meta( $post_id, 'rank_math_focus_keyword', sanitize_text_field( $data['focus_keyword'] ) );
        $updated[] = 'rank_math_focus_keyword';
    }
    
    // Update OG image
    if ( ! empty( $data['og_image'] ) ) {
        update_post_meta( $post_id, 'rank_math_facebook_image', esc_url_raw( $data['og_image'] ) );
        update_post_meta( $post_id, 'rank_math_twitter_cardType', 'summary_large_image' );
        update_post_meta( $post_id, 'rank_math_twitter_image', esc_url_raw( $data['og_image'] ) );
        $updated[] = 'og_image';
    }
    
    // Update any custom meta fields
    if ( ! empty( $data['custom_meta'] ) && is_array( $data['custom_meta'] ) ) {
        foreach ( $data['custom_meta'] as $key => $value ) {
            update_post_meta( $post_id, sanitize_key( $key ), $value );
            $updated[] = 'custom:' . $key;
        }
    }
    
    clean_post_cache( $post_id );
    
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( array(
        'status'  => 'success',
        'post_id' => $post_id,
        'title'   => $p->post_title,
        'updated_fields' => $updated
    ), JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
    exit;
}

