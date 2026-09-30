<?php
/**
 * Keystone Possibilities Child Theme - Custom XML Video Sitemap Engine
 * Certified BC Residential Builder #52603 — Google Video 1.1 Specification
 * 
 * Generates dynamic, Google-compliant XML Video Sitemaps (/video-sitemap.xml)
 * and bridges directly into Rank Math's sitemap_index.xml without Rank Math Pro.
 * 
 * @package KeystonePossibilitiesChild
 * @version 2026.1.0
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// ── 1. Register Rewrite Rule & Query Var for /video-sitemap.xml ──────────────
add_action('init', 'keystone_register_video_sitemap_rewrite', 5);
function keystone_register_video_sitemap_rewrite() {
    add_rewrite_rule('^video-sitemap\.xml$', 'index.php?video_sitemap=1', 'top');
}

add_filter('query_vars', 'keystone_register_video_sitemap_query_vars');
function keystone_register_video_sitemap_query_vars($vars) {
    $vars[] = 'video_sitemap';
    return $vars;
}

// ── 2. Version-Guarded Soft Rewrite Flush (Zero-Overhead Immunity) ────────────
add_action('init', 'keystone_maybe_flush_video_sitemap_rewrites', 99);
function keystone_maybe_flush_video_sitemap_rewrites() {
    $engine_version = '2026.1.2';
    if (get_option('keystone_video_sitemap_ver') !== $engine_version) {
        flush_rewrite_rules(false);
        update_option('keystone_video_sitemap_ver', $engine_version);
    }
}
add_action('after_switch_theme', function() {
    flush_rewrite_rules(false);
});

// ── 3. Template Redirect & XML Output Handler ────────────────────────────────
add_action('template_redirect', 'keystone_render_video_sitemap_xml', 1);
function keystone_render_video_sitemap_xml() {
    if (!get_query_var('video_sitemap')) {
        return;
    }

    // Suppress caching and minification for real-time XML serving
    if (!defined('DONOTCACHEPAGE')) define('DONOTCACHEPAGE', true);
    if (!defined('DONOTCACHEDB'))   define('DONOTCACHEDB', true);
    if (!defined('DONOTMINIFY'))   define('DONOTMINIFY', true);

    status_header(200);
    header('Content-Type: text/xml; charset=utf-8');
    header('X-Robots-Tag: noindex, follow', true);
    nocache_headers();

    // Check transient cache (12-hour TTL to protect MySQL under aggressive bot crawls)
    $cached_xml = get_transient('keystone_video_sitemap_xml_cache');
    if (false !== $cached_xml && !empty($cached_xml) && !isset($_GET['fresh'])) {
        echo $cached_xml;
        exit;
    }

    $xml = keystone_generate_video_sitemap_markup();
    set_transient('keystone_video_sitemap_xml_cache', $xml, 12 * HOUR_IN_SECONDS);

    echo $xml;
    exit;
}

// ── 4. Cache Invalidation on Post Mutation ───────────────────────────────────
add_action('save_post', 'keystone_invalidate_video_sitemap_transient');
add_action('deleted_post', 'keystone_invalidate_video_sitemap_transient');
function keystone_invalidate_video_sitemap_transient($post_id) {
    if (wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
        return;
    }
    delete_transient('keystone_video_sitemap_xml_cache');
}

// ── 5. Inject /video-sitemap.xml into Rank Math's sitemap_index.xml ──────────
add_filter('rank_math/sitemap/index', 'keystone_inject_video_sitemap_into_rank_math', 11);
function keystone_inject_video_sitemap_into_rank_math($xml) {
    $sitemap_url = esc_url(home_url('/video-sitemap.xml'));

    $latest_post = get_posts(array(
        'numberposts' => 1,
        'post_status' => 'publish',
        'post_type'   => array('post', 'page'),
        'orderby'     => 'post_modified_gmt',
        'order'       => 'DESC',
    ));

    $lastmod = !empty($latest_post) ? mysql2date('Y-m-d\TH:i:s+00:00', $latest_post[0]->post_modified_gmt) : gmdate('c');

    $custom_node  = "\t<sitemap>\n";
    $custom_node .= "\t\t<loc>" . $sitemap_url . "</loc>\n";
    $custom_node .= "\t\t<lastmod>" . esc_html($lastmod) . "</lastmod>\n";
    $custom_node .= "\t</sitemap>\n";

    return $xml . $custom_node;
}

// ── 6. Universal YouTube ID Extractor ────────────────────────────────────────
function keystone_extract_youtube_id_core($post) {
    if (is_numeric($post)) {
        $post = get_post($post);
    }
    if (!$post) return false;

    $post_id = $post->ID;

    // 1. Explicit Post Meta Override
    $meta_id = get_post_meta($post_id, 'keystone_youtube_id', true);
    if (!empty($meta_id) && preg_match('/^[a-zA-Z0-9_-]{11}$/', trim($meta_id))) {
        return trim($meta_id);
    }

    $video_url = get_post_meta($post_id, 'video_url', true);
    if (!empty($video_url)) {
        $found = keystone_parse_youtube_url_core($video_url);
        if ($found) return $found;
    }

    $content = $post->post_content;
    if (empty($content)) return false;

    // 2. Custom Keystone Shortcode check
    if (preg_match('/\[keystone_video[^\]]*id=["\']([a-zA-Z0-9_-]{11})["\']/i', $content, $m)) {
        return $m[1];
    }

    // 3. Universal Regex
    return keystone_parse_youtube_url_core($content);
}

function keystone_parse_youtube_url_core($string) {
    $pattern = '%(?:youtube(?:-nocookie)?\.com/(?:[^/\s]+/.+/|(?:v|e(?:mbed)?|shorts)/|.*[?&]v=)|youtu\.be/)([\w-]{11})%i';
    if (preg_match($pattern, $string, $matches)) {
        return $matches[1];
    }
    return false;
}

// ── 7. XML Markup Builder (Google Video 1.1 Specification) ───────────────────
function keystone_generate_video_sitemap_markup() {
    $posts = get_posts(array(
        'numberposts'      => 100,
        'post_type'        => array('post', 'page'),
        'post_status'      => 'publish',
        'orderby'          => 'date',
        'order'            => 'DESC',
        'suppress_filters' => false,
        'no_found_rows'    => true,
    ));

    $entries = array();

    foreach ($posts as $p) {
        $video_id = keystone_extract_youtube_id_core($p);
        if (!$video_id) {
            continue;
        }

        $loc      = esc_url(get_permalink($p->ID));
        $pub_date = mysql2date('Y-m-d\TH:i:s+00:00', $p->post_date_gmt);

        // Thumbnail: Local featured image preferred, fallback to YouTube hqdefault.jpg
        if (has_post_thumbnail($p->ID)) {
            $thumb = get_the_post_thumbnail_url($p->ID, 'full');
        } else {
            $thumb = "https://i.ytimg.com/vi/{$video_id}/hqdefault.jpg";
        }

        $raw_title = get_post_meta($p->ID, 'video_title', true);
        $title     = !empty($raw_title) ? $raw_title : get_the_title($p->ID);
        $title     = htmlspecialchars(wp_strip_all_tags($title), ENT_XML1, 'UTF-8');
        if (mb_strlen($title) > 100) {
            $title = mb_substr($title, 0, 97) . '...';
        }

        $raw_desc = get_post_meta($p->ID, 'video_description', true);
        if (empty($raw_desc)) {
            $raw_desc = get_the_excerpt($p->ID);
        }
        if (empty($raw_desc)) {
            $raw_desc = wp_trim_words($p->post_content, 35);
        }
        $desc = htmlspecialchars(mb_strimwidth(wp_strip_all_tags($raw_desc), 0, 2040, '...'), ENT_XML1, 'UTF-8');

        $entries[] = array(
            'loc'        => $loc,
            'thumb'      => esc_url($thumb),
            'title'      => $title,
            'desc'       => $desc,
            'player_loc' => "https://www.youtube-nocookie.com/embed/{$video_id}",
            'pub_date'   => $pub_date,
            'video_id'   => $video_id,
        );
    }

    $out  = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    $out .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' . "\n";
    $out .= '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">' . "\n";

    foreach ($entries as $e) {
        $out .= "\t<url>\n";
        $out .= "\t\t<loc>{$e['loc']}</loc>\n";
        $out .= "\t\t<video:video>\n";
        $out .= "\t\t\t<video:thumbnail_loc>{$e['thumb']}</video:thumbnail_loc>\n";
        $out .= "\t\t\t<video:title>{$e['title']}</video:title>\n";
        $out .= "\t\t\t<video:description>{$e['desc']}</video:description>\n";
        $out .= "\t\t\t<video:player_loc allow_embed=\"yes\">{$e['player_loc']}</video:player_loc>\n";
        $out .= "\t\t\t<video:publication_date>{$e['pub_date']}</video:publication_date>\n";
        $out .= "\t\t\t<video:family_friendly>yes</video:family_friendly>\n";
        $out .= "\t\t\t<video:uploader info=\"https://keystonepossibilities.ca\">Keystone Possibilities Ltd.</video:uploader>\n";
        $out .= "\t\t</video:video>\n";
        $out .= "\t</url>\n";
    }

    $out .= '</urlset>';
    return $out;
}
