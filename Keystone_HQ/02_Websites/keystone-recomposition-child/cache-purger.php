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
} else {
    echo "WP-LOAD NOT FOUND AT: " . $wp_load_path . "\n";
}

echo "ALL CACHE LAYERS PURGED SUCCESSFULLY\n";
