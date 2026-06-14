<?php
/**
 * Standalone WordPress Watch Pages Auditor
 */

$wp_load_path = dirname( dirname( dirname( dirname( __FILE__ ) ) ) ) . '/wp-load.php';
if ( file_exists( $wp_load_path ) ) {
    require_once( $wp_load_path );
    
    global $wpdb;
    $watch_pages = $wpdb->get_results( 
        "SELECT ID, post_title, post_name, post_date, post_content, post_status 
         FROM $wpdb->posts 
         WHERE post_type = 'page' AND (post_name LIKE 'watch-%' OR post_title LIKE 'Watch%')
         ORDER BY post_date DESC" 
    );
    
    $report = array();
    foreach ( $watch_pages as $p ) {
        $report[] = array(
            'id' => $p->ID,
            'title' => $p->post_title,
            'slug' => $p->post_name,
            'date' => $p->post_date,
            'status' => $p->post_status,
            'length' => strlen( $p->post_content )
        );
    }
    
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( $report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
    exit;
} else {
    echo "wp-load not found";
    exit;
}
