import re

local_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites\keystone-recomposition-child\functions.php"
remote_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\remote_functions.php"

# Let's read both
with open(local_path, "r", encoding="utf-8") as f:
    local_code = f.read()

with open(remote_path, "r", encoding="utf-8") as f:
    remote_code = f.read()

# We know the remote code has missing backslashes in some places!
# Let's see: the remote code has a few unescaped backslashes in strings like:
# echo "<script type="application/ld+json">
# Let's make sure the merge is based on the local file (which is perfectly correct and has all backslashes escaped) 
# and we append the extra clean blocks from the remote file (cleanly written).

extra_subscribe = """
/**
 * 15. Automatically Append YouTube Subscribe Buttons to All Pages and Posts
 * Skips appending if the content already contains a sub_confirmation link.
 */
function keystone_recomposition_child_append_subscribe_buttons( $content ) {
    if ( is_singular() && is_main_query() ) {
        // Prevent duplication if the user manually embedded them
        if ( strpos( $content, 'sub_confirmation=1' ) === false ) {
            $subscribe_html = '
            <div class="keystone-global-subscribe-buttons" style="display:flex; flex-wrap:wrap; gap:15px; margin-top:40px; margin-bottom: 40px; justify-content: center; align-items: center;">
                <a href="https://www.youtube.com/@keystonerecomposition?sub_confirmation=1" target="_blank" rel="noopener" style="background-color:#cc0000; color:#fff; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 700; font-family: \\'Outfit\\', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.3s ease;">▶ Subscribe: Keystone Recomposition</a>
                <a href="https://www.youtube.com/@keystoneprotocols?sub_confirmation=1" target="_blank" rel="noopener" style="background-color:#cc0000; color:#fff; padding: 12px 24px; border-radius: 4px; text-decoration: none; font-weight: 700; font-family: \\'Outfit\\', sans-serif; text-transform: uppercase; letter-spacing: 0.05em; transition: opacity 0.3s ease;">▶ Subscribe: Keystone Protocols</a>
            </div>';
            $content .= $subscribe_html;
        }
    }
    return $content;
}
add_filter( 'the_content', 'keystone_recomposition_child_append_subscribe_buttons', 99 );
"""

extra_fallback = """
/**
 * 16. Fallback Post Thumbnail to YouTube Video Thumbnail
 * Provides a fake _thumbnail_id so all themes (including Astra) and plugins think there's a thumbnail.
 */
add_filter( 'get_post_metadata', 'keystone_fallback_thumbnail_id', 10, 4 );
function keystone_fallback_thumbnail_id( $value, $object_id, $meta_key, $single ) {
    if ( '_thumbnail_id' === $meta_key ) {
        // Prevent infinite recursion by temporarily removing the filter
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
                if ( preg_match( '~(?:youtube\\\\.com/(?:[^/]+/.+/(?:v|e(?:mbed)?)/|.*[?&]v=|embed/)|youtu\\\\.be/|youtube\\\\.com/shorts/)([^\"&?/ ]{11})~i', $post_obj->post_content, $matches ) ) {
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
"""

# Let's combine the local_code with these extra blocks at the end
# But let's first check if they are already in the local_code (just in case)
if "keystone_recomposition_child_append_subscribe_buttons" not in local_code:
    # Append them beautifully!
    # Strip any ending PHP tag if present
    merged_code = local_code.strip()
    if merged_code.endswith("?>"):
        merged_code = merged_code[:-2].strip()
        
    merged_code += "\n\n" + extra_subscribe.strip() + "\n\n" + extra_fallback.strip()
    
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(merged_code)
    print("Successfully merged and saved perfectly clean functions.php!")
else:
    print("Extra functions are already present in local code.")
