<?php
/**
 * Standalone script to create missing watch pages for:
 * 1. retatrutide-phase-3-data (ov51ES_PcKk)
 * 2. klow-vs-glow-peptide-stacks-science (9mO2IbOnT-4)
 * 3. fda-peptide-ban-ending-2026 (7qwDTfqVDKs)
 */

$wp_load_path = dirname( dirname( dirname( dirname( __FILE__ ) ) ) ) . '/wp-load.php';
if ( file_exists( $wp_load_path ) ) {
    require_once( $wp_load_path );
    
    $targets = array(
        array(
            'slug' => 'retatrutide-phase-3-data',
            'youtube_id' => 'ov51ES_PcKk',
            'title' => 'Watch: Retatrutide Phase 3 Data: The Most Powerful GLP-1 Ever'
        ),
        array(
            'slug' => 'klow-vs-glow-peptide-stacks-science',
            'youtube_id' => '9mO2IbOnT-4',
            'title' => 'Watch: KLOW vs GLOW Peptide Stacks: The Science Nobody Explains'
        ),
        array(
            'slug' => 'fda-peptide-ban-ending-2026',
            'youtube_id' => '7qwDTfqVDKs',
            'title' => 'Watch: The FDA Peptide Ban is Ending — 11 Compounds Under Review (2026)'
        )
    );

    $results = array();

    foreach ( $targets as $t ) {
        $watch_slug = 'watch-' . $t['slug'];
        
        // Check if watch page already exists
        $existing = get_page_by_path( $watch_slug, OBJECT, 'page' );
        if ( $existing && 'publish' === $existing->post_status ) {
            $results[] = array(
                'slug' => $watch_slug,
                'status' => 'exists',
                'id' => $existing->ID
            );
            continue;
        }

        // Get the original blog post to copy its content
        $orig_post = get_page_by_path( $t['slug'], OBJECT, 'post' );
        if ( ! $orig_post ) {
            $results[] = array(
                'slug' => $watch_slug,
                'status' => 'error',
                'message' => 'Original post not found'
            );
            continue;
        }

        // Prepare the content for the watch page
        $blog_permalink = get_permalink( $orig_post->ID );
        
        // Strip any existing [keystone_video ...] shortcodes from copied content to avoid duplicates
        $clean_content = preg_replace( '~\[keystone_video[^\]]*\]~i', '', $orig_post->post_content );
        
        // Build the watch page content
        $content = '';
        $content .= '[keystone_video id="' . $t['youtube_id'] . '" type="youtube"]' . "\n\n";
        $content .= $clean_content . "\n\n";
        $content .= '<p class="wp-block-paragraph" style="text-align:center; margin-top:45px; margin-bottom:45px;">';
        $content .= '<a href="' . esc_url( $blog_permalink ) . '" style="background-color: #c4a265; color: #000; padding: 15px 30px; border-radius: 4px; text-decoration: none; font-weight: bold; font-family: \'Outfit\', sans-serif; display: inline-block; text-transform: uppercase; letter-spacing: 1px;">Read the Full Protocol →</a>';
        $content .= '</p>';

        // Insert the page
        $page_id = wp_insert_post( array(
            'post_title'    => $t['title'],
            'post_name'     => $watch_slug,
            'post_content'  => $content,
            'post_status'   => 'publish',
            'post_type'     => 'page',
            'post_author'   => $orig_post->post_author
        ) );

        if ( is_wp_error( $page_id ) ) {
            $results[] = array(
                'slug' => $watch_slug,
                'status' => 'error',
                'message' => $page_id->get_error_message()
            );
        } else {
            // Set post meta to match original video data
            update_post_meta( $page_id, 'keystone_youtube_id', $t['youtube_id'] );
            
            $results[] = array(
                'slug' => $watch_slug,
                'status' => 'created',
                'id' => $page_id
            );
        }
    }

    header('Content-Type: application/json; charset=utf-8');
    echo json_encode( $results, JSON_PRETTY_PRINT );
    exit;
} else {
    echo "wp-load not found";
    exit;
}
