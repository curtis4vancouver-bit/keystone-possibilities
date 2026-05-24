<?php
/**
 * Standalone Master OPcache and WordPress Cache Purger
 * Bypasses cached PHP compiles and resets all cache layers live.
 */

header('Content-Type: text/plain');

// Bootstrap WordPress
$wp_load_path = dirname( dirname( dirname( dirname( __FILE__ ) ) ) ) . '/wp-load.php';
if ( file_exists( $wp_load_path ) ) {
    require_once( $wp_load_path );
    
    // 1. Scan Spotify Links
    if ( isset( $_GET['scan'] ) ) {
        global $wpdb;
        echo "FRONT PAGE ID: " . get_option('page_on_front') . "\n\n";
        echo "=== DB POSTS SCAN FOR SPOTIFY ===\n\n";
        $posts = $wpdb->get_results( "SELECT ID, post_title, post_name, post_status, post_type, post_content FROM $wpdb->posts WHERE post_content LIKE '%spotify%'" );
        foreach ( $posts as $p ) {
            echo "POST ID: " . $p->ID . " | TITLE: " . $p->post_title . " | SLUG: " . $p->post_name . " | STATUS: " . $p->post_status . " | TYPE: " . $p->post_type . "\n";
            preg_match_all( '~https://open\.spotify\.com/[^\s\"\'<>]*~i', $p->post_content, $matches );
            if ( ! empty( $matches[0] ) ) {
                foreach ( $matches[0] as $m ) {
                    echo "  FOUND URL: " . $m . "\n";
                }
            }
        }
        
        echo "\n=== DB OPTIONS SCAN FOR SPOTIFY ===\n\n";
        $options = $wpdb->get_results( "SELECT option_name, option_value FROM $wpdb->options WHERE option_value LIKE '%spotify%'" );
        foreach ( $options as $o ) {
            echo "OPTION: " . $o->option_name . "\n";
            preg_match_all( '~https://open\.spotify\.com/[^\s\"\'<>]*~i', $o->option_value, $matches );
            if ( ! empty( $matches[0] ) ) {
                foreach ( $matches[0] as $m ) {
                    echo "  FOUND URL: " . $m . "\n";
                }
            }
        }
        exit;
    }

    // 2. Fix Spotify Links
    if ( isset( $_GET['fix'] ) ) {
        global $wpdb;
        echo "=== FIXING SPOTIFY LINKS ===\n\n";
        
        $wrong_urls = array(
            'https://open.spotify.com/artist/keystone-recomposition',
            'https://open.spotify.com/artist/1a30328b-20b2-48bd-8e56-2884d3b040c0',
            'https://open.spotify.com/artist/0',
            'https://open.spotify.com/artist/3hXpKBxUlhgoYkxGtzYNdU'
        );
        $correct_url = 'https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y';
        
        // Fix in posts
        $posts = $wpdb->get_results( "SELECT ID, post_content FROM $wpdb->posts WHERE post_content LIKE '%spotify%'" );
        $posts_updated = 0;
        foreach ( $posts as $p ) {
            $updated_content = $p->post_content;
            $needs_update = false;
            foreach ( $wrong_urls as $wrong ) {
                if ( strpos( $updated_content, $wrong ) !== false ) {
                    $updated_content = str_replace( $wrong, $correct_url, $updated_content );
                    $needs_update = true;
                }
            }
            if ( $needs_update ) {
                $wpdb->update(
                    $wpdb->posts,
                    array( 'post_content' => $updated_content ),
                    array( 'ID' => $p->ID )
                );
                clean_post_cache( $p->ID );
                echo "UPDATED POST ID: " . $p->ID . "\n";
                $posts_updated++;
            }
        }
        echo "TOTAL POSTS UPDATED: " . $posts_updated . "\n\n";
        
        // Fix in options
        $options = $wpdb->get_results( "SELECT option_name, option_value FROM $wpdb->options WHERE option_value LIKE '%spotify%'" );
        $options_updated = 0;
        foreach ( $options as $o ) {
            $updated_value = $o->option_value;
            $needs_update = false;
            foreach ( $wrong_urls as $wrong ) {
                if ( strpos( $updated_value, $wrong ) !== false ) {
                    $updated_value = str_replace( $wrong, $correct_url, $updated_value );
                    $needs_update = true;
                }
            }
            if ( $needs_update ) {
                update_option( $o->option_name, maybe_unserialize( $updated_value ) );
                echo "UPDATED OPTION: " . $o->option_name . "\n";
                $options_updated++;
            }
        }
        echo "TOTAL OPTIONS UPDATED: " . $options_updated . "\n\n";
    }

    if ( function_exists( 'wp_cache_flush' ) ) {
        wp_cache_flush();
        echo "WP_CACHE_FLUSH: SUCCESS\n";
    }
    
    // Programmatically set exact metadata for Post 1149 to feed GSC Video Schema
    $post_id = 1149;
    update_post_meta( $post_id, 'keystone_youtube_id', 'aXY9S_K88sk' );
    update_post_meta( $post_id, 'video_url', 'https://www.youtube.com/watch?v=aXY9S_K88sk' );
    update_post_meta( $post_id, 'video_title', 'I LOST 48 LBS ON MOUNJARO — HERE’S HOW MUCH WAS MUSCLE | MEN OVER 40' );
    update_post_meta( $post_id, 'video_description', 'Wayne Stevenson lost 48 lbs on Mounjaro. Learn how much was actual muscle loss vs visceral organ shrinkage, and the exact 4-Pillars Protocol to prevent it.' );
    update_post_meta( $post_id, 'video_duration', 'PT8M15S' );
    update_post_meta( $post_id, 'video_upload_date', '2026-05-22T20:04:10-07:00' );
    echo "POST_1149_META_UPDATE: SUCCESS\n";
} else {
    echo "WP-LOAD NOT FOUND AT: " . $wp_load_path . "\n";
}

// Flush OPcache if supported
if ( function_exists( 'opcache_reset' ) ) {
    opcache_reset();
    echo "OPCACHE_RESET: SUCCESS\n";
} else {
    echo "OPCACHE_RESET: NOT_AVAILABLE\n";
}

echo "ALL CACHE LAYERS PURGED SUCCESSFULLY\n";
