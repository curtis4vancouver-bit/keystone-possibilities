<?php
/**
 * Enterprise SEO Architecture - Programmatic VideoObject Schema Generator
 * Customized for Astra Child Theme to inject secure, GSC-compliant JSON-LD markup.
 *
 * @package Astra Child for Keystone
 * @since 1.0.0
 */

// Prevent direct execution of this file outside of the WordPress core lifecycle.
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'wp_head', 'keystone_inject_video_seo_schema', 15 );

/**
 * Orchestrates page checking, fetches metadata, builds fallback trees, and injects schema.
 */
function keystone_inject_video_seo_schema() {
    // 1. Structural Verification: Limit execution exclusively to single post templates.
    if ( ! is_single() ) {
        return;
    }

    $post_id = get_the_ID();
    if ( ! $post_id ) {
        return;
    }

    // 2. Eligibility Checking: Verify if the post represents a video blog post.
    $is_video_blog_meta      = get_post_meta( $post_id, 'is_video_blog', true );
    $video_blog_field_exists = get_post_meta( $post_id, 'video_blog', true );
    $has_video_category      = has_category( array( 'video-blog', 'video_blog', 'video-posts', 'longevity-video' ), $post_id );
    
    // Support our legacy keystone_youtube_id custom field check as well for backward compatibility
    $youtube_id_meta         = get_post_meta( $post_id, 'keystone_youtube_id', true );

    // Terminate processing immediately if no video-specific flag, ID, or category is detected.
    if ( ! $is_video_blog_meta && ! $has_video_category && ! $video_blog_field_exists && empty( $youtube_id_meta ) ) {
        return;
    }

    // 3. Metadata Extraction
    // First, try standard video_url or legacy keystone_youtube_id custom fields
    $video_url = get_post_meta( $post_id, 'video_url', true );
    if ( empty( $video_url ) && ! empty( $youtube_id_meta ) ) {
        $video_url = 'https://www.youtube.com/watch?v=' . $youtube_id_meta;
    }

    $video_thumbnail    = get_post_meta( $post_id, 'video_thumbnail', true );
    $video_duration     = get_post_meta( $post_id, 'video_duration', true );
    if ( empty( $video_duration ) ) {
        $video_duration = get_post_meta( $post_id, 'keystone_video_duration', true );
    }

    $video_upload_date  = get_post_meta( $post_id, 'video_upload_date', true );
    $video_transcript   = get_post_meta( $post_id, 'video_transcript', true );

    // --- Core Fallback Routines ---

    // Title / Name Fallback Priority
    $video_name = get_post_meta( $post_id, 'video_title', true );
    if ( empty( $video_name ) ) {
        $video_name = get_post_meta( $post_id, 'keystone_video_title', true );
    }
    if ( empty( $video_name ) ) {
        $video_name = get_the_title( $post_id );
    }

    // Description Fallback Priority (Purifies markup and shortcodes to ensure clean GSC indexing)
    $video_description = get_post_meta( $post_id, 'video_description', true );
    if ( empty( $video_description ) ) {
        $video_description = get_post_meta( $post_id, 'keystone_video_description', true );
    }
    if ( empty( $video_description ) ) {
        $excerpt_source = get_the_excerpt( $post_id );
        if ( empty( $excerpt_source ) ) {
            $post_obj = get_post( $post_id );
            $excerpt_source = ! empty( $post_obj->post_content ) ? $post_obj->post_content : '';
        }
        // Normalize, strip macros, discard tags, and truncate excerpt for clean rendering.
        $clean_excerpt     = wp_strip_all_tags( strip_shortcodes( $excerpt_source ) );
        $video_description = wp_html_excerpt( $clean_excerpt, 150, '...' );
    }

    if ( empty( $video_description ) ) {
        $video_description = esc_attr( get_the_title() ) . ' - High-performance health and longevity protocol details.';
    }

    // Thumbnail Fallback Priority
    if ( empty( $video_thumbnail ) ) {
        if ( has_post_thumbnail( $post_id ) ) {
            $thumbnail_id       = get_post_thumbnail_id( $post_id );
            $thumbnail_src_data = wp_get_attachment_image_src( $thumbnail_id, 'full' );
            if ( $thumbnail_src_data ) {
                $video_thumbnail = $thumbnail_src_data[0];
            }
        } elseif ( ! empty( $video_url ) ) {
            // Attempt to derive thumbnail from YouTube identifiers
            $video_thumbnail = astra_child_extract_video_thumbnail_fallback( $video_url );
        }
    }

    // Upload Date Fallback Priority (Enforces strict ISO 8601 formatting)
    if ( empty( $video_upload_date ) ) {
        $video_upload_date = get_the_date( 'c', $post_id );
    } else {
        $converted_time = strtotime( $video_upload_date );
        $video_upload_date = ( $converted_time !== false ) ? date( 'c', $converted_time ) : get_the_date( 'c', $post_id );
    }

    // ISO 8601 Duration Conversion
    $duration_iso = '';
    if ( ! empty( $video_duration ) ) {
        $duration_iso = astra_child_parse_duration_to_iso8601( $video_duration );
    }

    // Content URL and Embed URL Parsing
    $content_url = '';
    $embed_url   = '';
    if ( ! empty( $video_url ) ) {
        if ( preg_match( '/\.(mp4|m3u8|webm|ogg)$/i', $video_url ) ) {
            $content_url = esc_url_raw( $video_url );
        } else {
            $embed_url   = astra_child_parse_video_embed_url( $video_url );
            $content_url = esc_url_raw( $video_url ); // Keep watch URL as content reference
        }
    }

    // If embedUrl was derived and thumbnailUrl is still empty, fetch the default maxres
    if ( empty( $video_thumbnail ) && ! empty( $embed_url ) ) {
        $video_thumbnail = astra_child_extract_video_thumbnail_fallback( $video_url );
    }

    // If thumbnail is still blank, write a generic site fallback thumbnail to satisfy GSC eligibility
    if ( empty( $video_thumbnail ) ) {
        $video_thumbnail = 'https://keystoneprotocols.com/wp-content/uploads/logo.png';
    }

    // 4. Schema Array Compilation with Escape Filters
    $schema = array(
        '@context'     => 'https://schema.org',
        '@type'        => 'VideoObject',
        'name'         => esc_attr( $video_name ),
        'description'  => esc_attr( $video_description ),
        'thumbnailUrl' => esc_url( $video_thumbnail ),
        'uploadDate'   => esc_attr( $video_upload_date ),
    );

    // Conditional inclusion of non-mandatory, highly recommended fields
    if ( ! empty( $content_url ) ) {
        $schema['contentUrl'] = esc_url( $content_url );
    }

    if ( ! empty( $embed_url ) ) {
        $schema['embedUrl'] = esc_url( $embed_url );
    }

    if ( ! empty( $duration_iso ) ) {
        $schema['duration'] = esc_attr( $duration_iso );
    }

    if ( ! empty( $video_transcript ) ) {
        $schema['transcript'] = esc_html( wp_strip_all_tags( strip_shortcodes( $video_transcript ) ) );
    }

    // Set Organization details
    $schema['publisher'] = array(
        '@type' => 'Organization',
        'name'  => 'Keystone Protocols',
        'logo'  => array(
            '@type' => 'ImageObject',
            'url'   => 'https://keystoneprotocols.com/wp-content/uploads/logo.png'
        )
    );

    // 5. Secure JSON Serialization and Hook Injection
    // Enforce strict bitwise hex masking parameters to block stored XSS injection vectors.
    $json_flags      = JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT;
    $secured_json_ld = wp_json_encode( $schema, $json_flags );

    if ( ! empty( $secured_json_ld ) ) {
        echo "\n<!-- 🧠 Keystone Protocols - GSC Structured Video Schema Injector (Stored XSS Secure) -->\n";
        echo '<script type="application/ld+json">' . $secured_json_ld . "</script>\n\n";
    }
}

/**
 * Programmatically parses standard durations into ISO 8601 interval format (PTnHnMnS).
 * Accepts integer seconds, "MM:SS", and "HH:MM:SS" time formats.
 *
 * @param string|int $duration Raw duration input.
 * @return string Formatted ISO 8601 duration string.
 */
function astra_child_parse_duration_to_iso8601( $duration ) {
    $duration = trim( $duration );
    if ( empty( $duration ) ) {
        return '';
    }

    // Check if the input is already structured in ISO 8601 layout.
    if ( stripos( $duration, 'PT' ) === 0 ) {
        return $duration;
    }

    $hours   = 0;
    $minutes = 0;
    $seconds = 0;

    if ( is_numeric( $duration ) ) {
        $total_seconds = intval( $duration );
        $hours         = floor( $total_seconds / 3600 );
        $minutes       = floor( ( $total_seconds / 60 ) % 60 );
        $seconds       = $total_seconds % 60;
    } elseif ( preg_match( '/^(?:(\d+):)?(\d+):(\d+)$/', $duration, $matches ) ) {
        // HH:MM:SS format matches
        if ( count( $matches ) === 4 && $matches[1] !== '' ) {
            $hours   = intval( $matches[1] );
            $minutes = intval( $matches[2] );
            $seconds = intval( $matches[3] );
        } else {
            // MM:SS format matches
            $minutes = intval( $matches[2] );
            $seconds = intval( $matches[3] );
        }
    } else {
        return '';
    }

    // Compile time structures, omitting unassigned structures to remain compliant.
    $iso_string = 'PT';
    if ( $hours > 0 ) {
        $iso_string .= $hours . 'H';
    }
    if ( $minutes > 0 ) {
        $iso_string .= $minutes . 'M';
    }
    if ( $seconds > 0 || ( $hours === 0 && $minutes === 0 ) ) {
        $iso_string .= $seconds . 'S';
    }

    return $iso_string;
}

/**
 * Normalizes video platform links to output clean player embed structures.
 * Supports YouTube, YouTube Shorts, and Vimeo formats.
 *
 * @param string $url Raw platform video address.
 * @return string Normalized embed player URL.
 */
function astra_child_parse_video_embed_url( $url ) {
    $url = trim( $url );

    // Extract identifiers from various YouTube and Shorts patterns.
    if ( preg_match( '/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/ ]{11})/i', $url, $matches ) ) {
        return 'https://www.youtube.com/embed/' . $matches[1];
    }

    // Extract identifiers from various Vimeo formats.
    if ( preg_match( '/(?:vimeo\.com\/)(?:channels\/(?:\w+\/)?|groups\/([^\/]*)\/videos\/|album\/(\d+)\/video\/|showcase\/\d+\/video\/|video\/)?(\d+)/i', $url, $matches ) ) {
        $vimeo_id = end( $matches );
        if ( is_numeric( $vimeo_id ) ) {
            return 'https://player.vimeo.com/video/' . $vimeo_id;
        }
    }

    return $url;
}

/**
 * Extracts high-resolution fallback YouTube thumbnail URLs from video platform paths.
 *
 * @param string $url Platform video address.
 * @return string Fallback thumbnail path or empty string.
 */
function astra_child_extract_video_thumbnail_fallback( $url ) {
    if ( preg_match( '/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/ ]{11})/i', $url, $matches ) ) {
        return 'https://img.youtube.com/vi/' . $matches[1] . '/maxresdefault.jpg';
    }
    return '';
}


/**
 * 2. Shortcode to render our fast, PageSpeed-optimized lazy YouTube/Spotify media facade
 * Usage: [keystone_video id="YOUTUBE_ID" type="youtube" placeholder_img="OPTIONAL_URL"]
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
    
    // Set custom background or grab YouTube's maxres cover dynamically
    $bg_img = '';
    if ( ! empty( $args['placeholder_img'] ) ) {
        $bg_img = esc_url( $args['placeholder_img'] );
    } elseif ( $media_type === 'youtube' ) {
        $bg_img = 'https://img.youtube.com/vi/' . $media_id . '/maxresdefault.jpg';
    } else {
        // Fallback placeholder image for other media formats
        $bg_img = 'https://keystoneprotocols.com/wp-content/uploads/video-placeholder.jpg';
    }

    // Enqueue the deferred high-performance lazy player script
    wp_enqueue_script( 'keystone-lazy-player', get_stylesheet_directory_uri() . '/js/lazy-player.js', array(), '1.0.0', true );

    // Output the structural Premium Facade Blueprint markup
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
