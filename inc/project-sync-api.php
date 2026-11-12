<?php
/**
 * Keystone Possibilities v3.0 — Atomic Theme Asset, Root Static & Portal Project Sync Engine
 *
 * CRITICAL BOOTSTRAP MODULE:
 * - Bootstrapped onto live WP via legacy-allowlisted `inc/geo-cache-indexnow.php` (Step A0),
 *   synced to `inc/project-sync-api.php` (Step A1), and retained via `inc/geo-cache-indexnow.php`
 *   `require_once` bridge (Step A2) until v3.0 `functions.php` is uploaded last.
 * - Registers at rest_api_init priority 30 with $override = true so loading this module
 *   immediately upgrades /sync-theme-asset and unlocks /theme-manifest & /sync-root-static
 *   for the entire v3.0 child theme!
 * - Enforces SHA-256 verification, PHP token_get_all(..., TOKEN_PARSE) syntax validation,
 *   atomic tmp->rename writes, OPcache invalidation, and clean Batcache/object-cache flush
 *   (zero destructive 38-page wp_update_post loops).
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

if (!function_exists('kp_v3_verify_admin_or_sync_secret')) {
    /**
     * Permission check for theme/root/project sync endpoints.
     * Requires authenticated WP Administrator (Application Password / Cookie Nonce)
     * OR configured server-side sync secret in wp-config / wp_options.
     *
     * @param WP_REST_Request $request Incoming REST request.
     * @return bool|WP_Error
     */
    function kp_v3_verify_admin_or_sync_secret(WP_REST_Request $request)
    {
        if (function_exists('current_user_can') && current_user_can('manage_options')) {
            return true;
        }

        $configured_secret = defined('KP_PORTAL_SYNC_SECRET')
            ? (string) KP_PORTAL_SYNC_SECRET
            : (string) get_option('kp_portal_sync_secret', '');

        if ($configured_secret !== '') {
            $header_secret = (string) ($request->get_header('x-keystone-sync-secret') ?: $request->get_header('x-keystone-secret'));
            if ($header_secret !== '' && hash_equals($configured_secret, $header_secret)) {
                return true;
            }
        }

        return new WP_Error(
            'kp_sync_forbidden',
            'Administrator authentication required for Keystone v3.0 sync endpoints.',
            array('status' => 403)
        );
    }
}

if (!function_exists('kp_v3_is_allowed_theme_rel_path')) {
    /**
     * Strictly validates relative child-theme asset paths against traversal & arbitrary file writes.
     *
     * @param string $rel_path Relative path within child theme.
     * @return bool
     */
    function kp_v3_is_allowed_theme_rel_path(string $rel_path): bool
    {
        $rel = str_replace('\\', '/', trim($rel_path));
        if ($rel === '' || $rel[0] === '/' || strpos($rel, '..') !== false || strpos($rel, "\0") !== false) {
            return false;
        }

        $exact_root = array(
            'functions.php',
            'style.css',
            'header.php',
            'footer.php',
            'front-page.php',
            'single.php',
            'page.php',
            '404.php',
            '410.php',
            'llms.txt',
            'llms-full.txt',
        );
        if (in_array($rel, $exact_root, true)) {
            return true;
        }

        $patterns = array(
            '/^page-[a-z0-9_-]+\.php$/',
            '/^inc\/[a-z0-9_-]+\.php$/',
            '/^template-parts\/[a-z0-9_\/-]+\.php$/',
            '/^assets\/css\/[a-z0-9_-]+\.css$/',
            '/^assets\/js\/[a-z0-9_-]+\.js$/',
            '/^assets\/images\/[a-zA-Z0-9_.-]+\.(png|jpg|jpeg|webp|svg)$/',
            '/^js\/[a-z0-9_-]+\.js$/',
        );

        foreach ($patterns as $regex) {
            if (preg_match($regex, $rel) === 1) {
                return true;
            }
        }

        return false;
    }
}

if (!function_exists('kp_v3_validate_php_syntax')) {
    /**
     * Validates PHP source syntax in-memory using PHP's native lexer/parser (TOKEN_PARSE)
     * before writing to disk so a malformed upload can never brick the child theme.
     *
     * @param string $php_source Raw PHP file contents.
     * @return true|string True when valid, or error description string when invalid.
     */
    function kp_v3_validate_php_syntax(string $php_source)
    {
        if (strpos(ltrim($php_source), '<?php') !== 0) {
            return 'PHP file must start with <?php opening tag.';
        }

        try {
            if (defined('TOKEN_PARSE')) {
                $tokens = token_get_all($php_source, TOKEN_PARSE);
            } else {
                $tokens = token_get_all($php_source);
            }
        } catch (\ParseError $e) {
            return 'PHP ParseError on line ' . $e->getLine() . ': ' . $e->getMessage();
        } catch (\Throwable $t) {
            return 'PHP Tokenizer Error: ' . $t->getMessage();
        }

        // Secondary structural balance check across non-string/comment tokens
        $brace_depth = 0;
        foreach ($tokens as $tok) {
            if (is_array($tok)) {
                $id = $tok[0];
                if ($id === T_CURLY_OPEN || $id === T_DOLLAR_OPEN_CURLY_BRACES) {
                    $brace_depth += 1;
                }
            } elseif ($tok === '{') {
                $brace_depth += 1;
            } elseif ($tok === '}') {
                $brace_depth -= 1;
                if ($brace_depth < 0) {
                    return 'Unbalanced closing curly brace detected.';
                }
            }
        }

        if ($brace_depth !== 0) {
            return 'Unbalanced curly braces (net depth ' . $brace_depth . ').';
        }

        return true;
    }
}

if (!function_exists('kp_v3_flush_edge_cache')) {
    /**
     * Flushes WordPress object cache and Batcache URL keys cleanly without touching post_modified.
     *
     * @return array<string, mixed>
     */
    function kp_v3_flush_edge_cache(): array
    {
        $flushed = array(
            'wp_cache_flush' => false,
            'batcache_urls'  => 0,
        );

        if (function_exists('wp_cache_flush')) {
            $flushed['wp_cache_flush'] = (bool) wp_cache_flush();
        }

        if (function_exists('batcache_clear_url')) {
            $key_urls = array(
                home_url('/'),
                home_url('/feasibility-plan/'),
                home_url('/realtor-architect-desk/'),
                home_url('/portfolio-general-contractor-squamish/'),
                home_url('/about-us-general-contractor-squamish/'),
                home_url('/client-login/'),
                home_url('/videos/'),
                home_url('/west-vancouver-custom-homes/'),
                home_url('/whistler-custom-homes/'),
                home_url('/squamish-custom-homes/'),
                home_url('/north-vancouver-custom-homes/'),
                home_url('/vancouver-r1-1-multiplex-builder/'),
                home_url('/coquitlam-custom-homes-multiplex/'),
                home_url('/bc-developer-portal/'),
            );
            foreach ($key_urls as $u) {
                @batcache_clear_url($u);
                $flushed['batcache_urls'] += 1;
            }
        }

        return $flushed;
    }
}

if (!function_exists('kp_v3_write_root_static_file')) {
    /**
     * Writes an approved static discovery file (llms.txt, llms-full.txt, IndexNow key)
     * to WP Cloud Nginx document root (/srv/htdocs/) and ABSPATH.
     *
     * @param string $filename Allowed root filename.
     * @param string $content  Raw UTF-8 file content.
     * @return array<string, mixed>
     */
    function kp_v3_write_root_static_file(string $filename, string $content): array
    {
        $allowed_names = array(
            'llms.txt',
            'llms-full.txt',
            '567052ceffa24bb89513f2fd8cc7cfd5.txt',
        );
        if (!in_array($filename, $allowed_names, true)) {
            return array('ok' => false, 'error' => 'Disallowed root static filename: ' . $filename);
        }

        $roots = array();
        if (!empty($_SERVER['DOCUMENT_ROOT']) && is_dir((string) $_SERVER['DOCUMENT_ROOT'])) {
            $roots[] = rtrim((string) $_SERVER['DOCUMENT_ROOT'], '/\\');
        }
        if (is_dir('/srv/htdocs')) {
            $roots[] = '/srv/htdocs';
        }
        if (defined('ABSPATH') && is_dir(ABSPATH)) {
            $roots[] = rtrim(ABSPATH, '/\\');
        }
        $roots[] = rtrim(get_stylesheet_directory(), '/\\');
        $roots   = array_values(array_unique($roots));

        $written = array();
        foreach ($roots as $dir) {
            if (!is_writable($dir)) {
                continue;
            }
            $target = $dir . '/' . $filename;
            $tmp    = $target . '.tmp.' . getmypid();
            $bytes  = @file_put_contents($tmp, $content);
            if ($bytes !== false && @rename($tmp, $target)) {
                @chmod($target, 0644);
                $written[] = array('path' => $target, 'bytes' => $bytes);
            } else {
                @unlink($tmp);
            }
        }

        return array(
            'ok'      => !empty($written),
            'file'    => $filename,
            'written' => $written,
            'sha256'  => hash('sha256', $content),
        );
    }
}

if (!function_exists('kp_v3_handle_theme_manifest')) {
    /**
     * GET /wp-json/keystone/v1/theme-manifest
     * Returns SHA-256 + byte size inventory of all managed child-theme files on disk.
     *
     * @return WP_REST_Response
     */
    function kp_v3_handle_theme_manifest(): WP_REST_Response
    {
        $theme_dir = rtrim(get_stylesheet_directory(), '/\\');
        $files     = array();

        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($theme_dir, FilesystemIterator::SKIP_DOTS)
        );

        foreach ($iterator as $file_info) {
            if (!$file_info->isFile()) {
                continue;
            }
            $abs = str_replace('\\', '/', $file_info->getPathname());
            $rel = ltrim(substr($abs, strlen(str_replace('\\', '/', $theme_dir))), '/');
            if (!kp_v3_is_allowed_theme_rel_path($rel)) {
                continue;
            }
            $files[$rel] = array(
                'bytes'  => (int) $file_info->getSize(),
                'sha256' => (string) hash_file('sha256', $file_info->getPathname()),
                'mtime'  => (int) $file_info->getMTime(),
            );
        }

        ksort($files);

        return new WP_REST_Response(array(
            'ok'        => true,
            'version'   => '3.0.0',
            'theme_dir' => $theme_dir,
            'count'     => count($files),
            'files'     => $files,
        ), 200);
    }
}

if (!function_exists('kp_v3_handle_sync_theme_asset')) {
    /**
     * POST /wp-json/keystone/v1/sync-theme-asset
     * Atomically writes a validated child-theme file with SHA-256 & PHP syntax guards.
     *
     * @param WP_REST_Request $request Incoming request.
     * @return WP_REST_Response
     */
    function kp_v3_handle_sync_theme_asset(WP_REST_Request $request): WP_REST_Response
    {
        $params   = $request->get_json_params();
        $body     = is_array($params) ? $params : $request->get_params();
        $rel_file = trim(str_replace('\\', '/', (string) ($body['file'] ?? $body['rel_path'] ?? $body['path'] ?? '')));

        if (!kp_v3_is_allowed_theme_rel_path($rel_file)) {
            return new WP_REST_Response(array(
                'ok'    => false,
                'error' => 'Path not in v3.0 theme allowlist: ' . $rel_file,
            ), 400);
        }

        $raw_bytes = null;
        if (isset($body['content_b64']) && is_string($body['content_b64']) && $body['content_b64'] !== '') {
            $decoded = base64_decode($body['content_b64'], true);
            if ($decoded === false) {
                return new WP_REST_Response(array('ok' => false, 'error' => 'Invalid base64 payload.'), 400);
            }
            $raw_bytes = $decoded;
        } elseif (isset($body['content']) && is_string($body['content'])) {
            $raw_bytes = $body['content'];
        }

        if ($raw_bytes === null || strlen($raw_bytes) < 16) {
            return new WP_REST_Response(array('ok' => false, 'error' => 'Empty or undersized content payload.'), 400);
        }

        $actual_sha256   = hash('sha256', $raw_bytes);
        $expected_sha256 = strtolower(trim((string) ($body['sha256'] ?? '')));
        if ($expected_sha256 !== '' && !hash_equals($expected_sha256, $actual_sha256)) {
            return new WP_REST_Response(array(
                'ok'       => false,
                'error'    => 'SHA-256 checksum mismatch.',
                'expected' => $expected_sha256,
                'actual'   => $actual_sha256,
            ), 400);
        }

        if (substr($rel_file, -4) === '.php') {
            $syntax_ok = kp_v3_validate_php_syntax($raw_bytes);
            if ($syntax_ok !== true) {
                return new WP_REST_Response(array(
                    'ok'    => false,
                    'error' => 'PHP syntax validation failed: ' . $syntax_ok,
                    'file'  => $rel_file,
                ), 422);
            }
        }

        $dest = trailingslashit(get_stylesheet_directory()) . $rel_file;
        $dir  = dirname($dest);
        if (!is_dir($dir) && !wp_mkdir_p($dir)) {
            return new WP_REST_Response(array('ok' => false, 'error' => 'Failed to create directory: ' . $dir), 500);
        }

        $tmp   = $dest . '.tmp.' . getmypid();
        $bytes = @file_put_contents($tmp, $raw_bytes);
        if ($bytes === false || !@rename($tmp, $dest)) {
            @unlink($tmp);
            return new WP_REST_Response(array('ok' => false, 'error' => 'Atomic write failed for ' . $rel_file), 500);
        }
        @chmod($dest, 0644);

        if (substr($rel_file, -4) === '.php' && function_exists('opcache_invalidate')) {
            @opcache_invalidate($dest, true);
        }

        $root_mirror = null;
        if ($rel_file === 'llms.txt' || $rel_file === 'llms-full.txt') {
            $root_mirror = kp_v3_write_root_static_file($rel_file, $raw_bytes);
        }

        $flush_report = empty($body['skip_cache_flush']) ? kp_v3_flush_edge_cache() : array('skipped' => true);

        return new WP_REST_Response(array(
            'ok'               => true,
            'file'             => $rel_file,
            'bytes'            => $bytes,
            'sha256'           => $actual_sha256,
            'dest'             => $dest,
            'root_mirror'      => $root_mirror,
            'edge_cache_purge' => $flush_report,
        ), 200);
    }
}

if (!function_exists('kp_v3_handle_sync_root_static')) {
    /**
     * POST /wp-json/keystone/v1/sync-root-static
     * Syncs llms.txt, llms-full.txt, and 567052ceffa24bb89513f2fd8cc7cfd5.txt to /srv/htdocs/.
     *
     * @param WP_REST_Request $request Incoming request.
     * @return WP_REST_Response
     */
    function kp_v3_handle_sync_root_static(WP_REST_Request $request): WP_REST_Response
    {
        $params  = $request->get_json_params();
        $body    = is_array($params) ? $params : $request->get_params();
        $results = array();

        // Batch files map `{ "files": { "llms.txt": "...", ... } }` or single `{ "file": "llms.txt", "content": "..." }`
        if (isset($body['files']) && is_array($body['files'])) {
            foreach ($body['files'] as $fname => $fcontent) {
                if (is_string($fname) && is_string($fcontent)) {
                    $results[$fname] = kp_v3_write_root_static_file($fname, $fcontent);
                }
            }
        } elseif (!empty($body['file']) && isset($body['content'])) {
            $fname           = (string) $body['file'];
            $results[$fname] = kp_v3_write_root_static_file($fname, (string) $body['content']);
        } else {
            // Default: mirror existing theme llms.txt, llms-full.txt & IndexNow key to /srv/htdocs/
            $theme_dir = trailingslashit(get_stylesheet_directory());
            foreach (array('llms.txt', 'llms-full.txt') as $fn) {
                if (file_exists($theme_dir . $fn)) {
                    $results[$fn] = kp_v3_write_root_static_file($fn, (string) file_get_contents($theme_dir . $fn));
                }
            }
            $results['567052ceffa24bb89513f2fd8cc7cfd5.txt'] = kp_v3_write_root_static_file(
                '567052ceffa24bb89513f2fd8cc7cfd5.txt',
                '567052ceffa24bb89513f2fd8cc7cfd5'
            );
        }

        return new WP_REST_Response(array(
            'ok'      => !empty($results),
            'results' => $results,
        ), 200);
    }
}

if (!function_exists('kp_v3_handle_set_avatar_video_ids')) {
    /**
     * POST /wp-json/keystone/v1/set-avatar-video-ids
     *
     * @param WP_REST_Request $request Incoming request.
     * @return WP_REST_Response
     */
    function kp_v3_handle_set_avatar_video_ids(WP_REST_Request $request): WP_REST_Response
    {
        $params  = $request->get_json_params() ?: $request->get_params();
        $key_map = array(
            'feasibility'                  => 'kp_video_id_feasibility',
            'kp_video_id_feasibility'      => 'kp_video_id_feasibility',
            'bill44'                       => 'kp_video_id_bill44_multiplex',
            'kp_video_id_bill44_multiplex' => 'kp_video_id_bill44_multiplex',
            'stepcode5'                    => 'kp_video_id_stepcode5_custom',
            'kp_video_id_stepcode5_custom' => 'kp_video_id_stepcode5_custom',
        );

        $updated = array();
        foreach ($key_map as $input_key => $option_name) {
            if (!array_key_exists($input_key, $params)) {
                continue;
            }
            $raw_val = trim(sanitize_text_field((string) $params[$input_key]));
            if ($raw_val !== '' && preg_match('/^[A-Za-z0-9_-]{11}$/', $raw_val) !== 1) {
                return new WP_REST_Response(array(
                    'ok'    => false,
                    'error' => sprintf('Invalid 11-character YouTube video ID for %s.', $input_key),
                ), 400);
            }
            update_option($option_name, $raw_val, false);
            $updated[$option_name] = $raw_val;
        }

        if (empty($updated)) {
            return new WP_REST_Response(array(
                'ok'    => false,
                'error' => 'Provide at least one video ID key: feasibility, bill44, or stepcode5.',
            ), 400);
        }

        return new WP_REST_Response(array('ok' => true, 'updated' => $updated), 200);
    }
}

if (!function_exists('keystone_portal_sync_project_handler')) {
    /**
     * POST /wp-json/keystone/v1/sync-project
     * Synchronizes a builder project dossier into wp_options (`keystone_portal_jobs_v10`).
     *
     * @param WP_REST_Request $request Incoming request.
     * @return WP_REST_Response|WP_Error
     */
    function keystone_portal_sync_project_handler(WP_REST_Request $request)
    {
        $params = $request->get_json_params();
        if (empty($params) || !is_array($params)) {
            $params = $request->get_params();
        }

        $jobs_opt    = defined('KEYSTONE_PORTAL_JOBS_OPTION') ? KEYSTONE_PORTAL_JOBS_OPTION : 'keystone_portal_jobs_v10';
        $updated_opt = defined('KEYSTONE_PORTAL_JOBS_UPDATED_OPTION') ? KEYSTONE_PORTAL_JOBS_UPDATED_OPTION : 'keystone_portal_jobs_v10_updated_at';

        $job_id = sanitize_text_field((string) ($params['job_id'] ?? $params['jobId'] ?? 'KP-2026-001'));
        $jobs   = get_option($jobs_opt, array());
        if (!is_array($jobs)) {
            $jobs = array();
        }

        $existing = isset($jobs[$job_id]) && is_array($jobs[$job_id]) ? $jobs[$job_id] : array();
        $incoming = isset($params['job']) && is_array($params['job']) ? $params['job'] : $params;
        unset($incoming['secret']);

        $merged               = array_merge($existing, $incoming);
        $merged['id']         = $job_id;
        $merged['job_id']     = $job_id;
        $merged['updated_at'] = gmdate('c');

        $jobs[$job_id] = $merged;
        update_option($jobs_opt, $jobs, false);
        update_option($updated_opt, $merged['updated_at'], false);

        return new WP_REST_Response(array(
            'ok'         => true,
            'status'     => 'synced',
            'job_id'     => $job_id,
            'total_jobs' => count($jobs),
            'updated_at' => $merged['updated_at'],
        ), 200);
    }
}

if (!function_exists('kp_v3_register_theme_sync_routes')) {
    /**
     * Registers v3.0 sync & manifest routes at priority 30 with $override = true.
     */
    function kp_v3_register_theme_sync_routes(): void
    {
        register_rest_route('keystone/v1', '/theme-manifest', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => 'kp_v3_handle_theme_manifest',
            'permission_callback' => 'kp_v3_verify_admin_or_sync_secret',
        ), true);

        register_rest_route('keystone/v1', '/sync-theme-asset', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'kp_v3_handle_sync_theme_asset',
            'permission_callback' => 'kp_v3_verify_admin_or_sync_secret',
        ), true);

        register_rest_route('keystone/v1', '/sync-root-static', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'kp_v3_handle_sync_root_static',
            'permission_callback' => 'kp_v3_verify_admin_or_sync_secret',
        ), true);

        register_rest_route('keystone/v1', '/set-avatar-video-ids', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'kp_v3_handle_set_avatar_video_ids',
            'permission_callback' => 'kp_v3_verify_admin_or_sync_secret',
        ), true);

        register_rest_route('keystone/v1', '/sync-project', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'keystone_portal_sync_project_handler',
            'permission_callback' => 'kp_v3_verify_admin_or_sync_secret',
        ), true);
    }
    add_action('rest_api_init', 'kp_v3_register_theme_sync_routes', 30);
}
