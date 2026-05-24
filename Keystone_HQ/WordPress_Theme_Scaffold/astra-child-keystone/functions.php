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

/**
 * 1. Enqueue Parent Stylesheet and Google Fonts
 */
function astra_child_keystone_enqueue_styles() {
    // Enqueue parent Astra style
    wp_enqueue_style( 'astra-parent-theme-css', get_template_directory_uri() . '/style.css' );
    
    // Enqueue Child customized style
    wp_enqueue_style( 'astra-child-keystone-css', get_stylesheet_directory_uri() . '/style.css', array( 'astra-parent-theme-css' ), '1.0.0' );
    
    // Load typography fonts (Montserrat & Inter)
    wp_enqueue_style( 'keystone-google-fonts', 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@700&display=swap', array(), null );
}
add_action( 'wp_enqueue_scripts', 'astra_child_keystone_enqueue_styles' );

/**
 * 2. Preconnecting Web Fonts (Performance GSC optimization)
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
 * 5. Load the rich SEO VideoObject Schema Injector and Shortcodes
 */
require_once get_stylesheet_directory() . '/inc/seo-video-injector.php';

/**
 * 6. Programmatically Inject TikTok into Rank Math PRO's structured metadata Graph
 */
add_filter( 'rank_math/json_ld', function( $data, $jsonld ) {
    // Loop through all graph nodes to find Person and Organization types
    if ( isset( $data['@graph'] ) && is_array( $data['@graph'] ) ) {
        foreach ( $data['@graph'] as &$node ) {
            if ( isset( $node['@type'] ) ) {
                $types = (array) $node['@type'];
                if ( in_array( 'Person', $types ) || in_array( 'Organization', $types ) ) {
                    if ( ! isset( $node['sameAs'] ) ) {
                        $node['sameAs'] = array();
                    }
                    // Clean and append TikTok securely if missing
                    if ( ! in_array( 'https://www.tiktok.com/@keystonerecomposition', $node['sameAs'] ) ) {
                        $node['sameAs'][] = 'https://www.tiktok.com/@keystonerecomposition';
                    }
                }
            }
        }
    }
    return $data;
}, 99, 2 );

/**
 * 7. Hook our custom lazy media metadata into Rank Math PRO's Video Sitemap Generator
 */
add_filter( 'rank_math/sitemap/video/post', function( $video, $post_id ) {
    // Attempt to pull the custom YouTube ID from post meta
    $youtube_id = get_post_meta( $post_id, 'keystone_youtube_id', true );
    
    // Fallback: search for [keystone_video id="..."] shortcode in content
    if ( empty( $youtube_id ) ) {
        $post = get_post( $post_id );
        if ( $post && preg_match( '/\[keystone_video\s+id=["\']([a-zA-Z0-9_-]+)["\']/', $post->post_content, $matches ) ) {
            $youtube_id = $matches[1];
        }
    }
    
    if ( ! empty( $youtube_id ) ) {
        $video['thumbnail_loc'] = "https://img.youtube.com/vi/{$youtube_id}/maxresdefault.jpg";
        $video['title']         = get_the_title( $post_id );
        $video['description']   = get_the_excerpt( $post_id );
        $video['player_loc']    = "https://www.youtube-nocookie.com/embed/{$youtube_id}";
        $video['uploader']      = "Wayne Stevenson";
        $video['uploader_info'] = "https://keystonerecomposition.com/";
    }
    
    return $video;
}, 10, 2 );
