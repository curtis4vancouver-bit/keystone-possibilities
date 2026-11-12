<?php
/**
 * Keystone Possibilities v3.0 — Master Portfolio Residences Shortcode Bridge
 *
 * Provides `[portfolio_residences_carousels]` backed directly by `kp_get_portfolio_residences()`
 * (9 genuine BC Signature Residences, 42 live gallery URLs, tactile `.kp-lux-reel-track` horizontal
 * reels, and accessible `#kpLightboxModal` inspection — zero watermarked stock images or vertical bounce).
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Renders the 9 Signature Portfolio Residences using the v3.0 tactile horizontal reel system.
 *
 * @return string
 */
function kp_portfolio_residences_carousels_shortcode(): string
{
    $residences = function_exists('kp_get_portfolio_residences') ? kp_get_portfolio_residences() : array();
    if (empty($residences)) {
        return '';
    }

    ob_start();
    ?>
    <div class="kp-container" data-kp-filter-group="portfolio-shortcode">
        <div class="kp-lux-reel-header">
            <div>
                <span class="kp-eyebrow">Built Architectural Record · 9 Signature BC Residences</span>
                <h2 class="kp-section-title">Master Portfolio Galleries</h2>
            </div>
            <div class="kp-filter-bar" role="tablist" aria-label="Filter Portfolio by Corridor">
                <button type="button" class="kp-filter-pill is-active" data-kp-filter="all">All Residences (9)</button>
                <button type="button" class="kp-filter-pill" data-kp-filter="west-van-north-shore">West &amp; North Shore</button>
                <button type="button" class="kp-filter-pill" data-kp-filter="whistler-squamish">Whistler &amp; Sea-to-Sky</button>
                <button type="button" class="kp-filter-pill" data-kp-filter="vancouver">Vancouver Westside</button>
                <button type="button" class="kp-filter-pill" data-kp-filter="sunshine-coast">Sunshine Coast</button>
            </div>
        </div>

        <div class="kp-lux-reel-wrap" data-kp-reel>
            <div class="kp-lux-reel-track">
                <?php foreach ($residences as $project) : ?>
                    <?php
                    $gallery      = !empty($project['gallery']) && is_array($project['gallery']) ? $project['gallery'] : array($project['hero_image']);
                    $gallery_json = wp_json_encode($gallery);
                    $photo_count  = count($gallery);
                    ?>
                    <article class="kp-portfolio-card" data-kp-category="<?php echo esc_attr((string) $project['filter_group']); ?>">
                        <div class="kp-portfolio-card__media">
                            <img src="<?php echo esc_url((string) $project['hero_image']); ?>"
                                 alt="<?php echo esc_attr((string) $project['title'] . ' — ' . $project['location']); ?>"
                                 loading="lazy"
                                 decoding="async">
                            <span class="kp-portfolio-card__count"><?php echo (int) $photo_count; ?> <?php echo $photo_count === 1 ? 'Photo' : 'Photos'; ?></span>
                        </div>
                        <div class="kp-portfolio-card__body">
                            <div class="kp-portfolio-card__loc"><?php echo esc_html((string) $project['location']); ?></div>
                            <h3 class="kp-portfolio-card__title"><?php echo esc_html((string) $project['title']); ?></h3>
                            <p class="kp-portfolio-card__desc"><?php echo esc_html((string) $project['summary']); ?></p>
                            <div class="kp-portfolio-card__tags">
                                <?php foreach ((array) $project['tags'] as $tag) : ?>
                                    <span class="kp-tag"><?php echo esc_html((string) $tag); ?></span>
                                <?php endforeach; ?>
                            </div>
                            <div style="margin-top: 16px;">
                                <button type="button"
                                        class="kp-btn kp-btn-outline"
                                        style="width: 100%;"
                                        data-kp-lightbox="<?php echo esc_url((string) $project['hero_image']); ?>"
                                        data-kp-gallery="<?php echo esc_attr((string) $gallery_json); ?>"
                                        data-kp-title="<?php echo esc_attr((string) $project['title']); ?>"
                                        data-kp-meta="<?php echo esc_attr((string) $project['location'] . ' · ' . $photo_count . ' Verified Photos'); ?>">
                                    Inspect Full Gallery (<?php echo (int) $photo_count; ?>) &rarr;
                                </button>
                            </div>
                        </div>
                    </article>
                <?php endforeach; ?>
            </div>
            <div style="display: flex; justify-content: flex-end; margin-top: 12px;">
                <div class="kp-reel-controls">
                    <button type="button" class="kp-reel-btn" data-kp-reel-prev aria-label="Previous residence">&lsaquo;</button>
                    <button type="button" class="kp-reel-btn" data-kp-reel-next aria-label="Next residence">&rsaquo;</button>
                </div>
            </div>
        </div>
    </div>
    <?php
    return (string) ob_get_clean();
}
add_shortcode('portfolio_residences_carousels', 'kp_portfolio_residences_carousels_shortcode');
