<?php
/**
 * Keystone Possibilities v3.0 — Theme Sync & Manifest API Module
 * Delegates cleanly to the self-contained bootstrap engine in inc/project-sync-api.php.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

require_once __DIR__ . '/project-sync-api.php';
