<?php
/**
 * Template Name: Regional Hub - Vancouver
 * Template Post Type: page
 *
 * Legacy regional template wrapper delegating cleanly to page-corridor.php.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_forced_corridor_slug = 'vancouver-r1-1';
require get_stylesheet_directory() . '/page-corridor.php';
