<?php
/**
 * Legacy Multi-Job Portal Shim — Delegates 100% cleanly to inc/portal-api-v10.php
 * Prevents duplicate REST route registration and eliminates legacy unauthenticated write routes.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

require_once __DIR__ . '/portal-api-v10.php';
