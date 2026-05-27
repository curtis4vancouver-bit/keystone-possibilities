<?php
require_once( dirname(__FILE__) . '/../keystonerecomposition/wp-load.php' );
global $wpdb;

$post = $wpdb->get_row("SELECT ID, post_title, post_name, post_date, post_content FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish' ORDER BY post_date DESC LIMIT 1");
if($post) {
    echo "ID: " . $post->ID . "\n";
    echo "Title: " . $post->post_title . "\n";
    echo "Date: " . $post->post_date . "\n";
    echo "Content:\n" . $post->post_content . "\n";
} else {
    echo "No post found.\n";
}
