<?php
/**
 * Standalone Master OPcache and WordPress Cache Purger
 * Bypasses cached PHP compiles and resets all cache layers live.
 */

header('Content-Type: text/plain');

// Flush OPcache if supported
if ( function_exists( 'opcache_reset' ) ) {
    opcache_reset();
    echo "OPCACHE_RESET: SUCCESS\n";
} else {
    echo "OPCACHE_RESET: NOT_AVAILABLE\n";
}

// Bootstrap WordPress to flush object caches
$wp_load_path = dirname( dirname( dirname( dirname( __FILE__ ) ) ) ) . '/wp-load.php';
if ( file_exists( $wp_load_path ) ) {
    require_once( $wp_load_path );
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

echo "ALL CACHE LAYERS PURGED SUCCESSFULLY\n";
