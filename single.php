<?php
/**
 * Single Technical Blueprint & Engineering Post Template (single.php)
 *
 * Wraps all blog posts in:
 * - BreadcrumbList UI
 * - Principal Superintendent Wayne Stevenson (#52603) verified author byline
 * - Companion /videos/[slug]/ 4K Watch Page bridge card
 * - Crisp Quiet-Luxury Gutenberg block typography
 * - End-of-article Realtor® Rule 5-11 Desk + 48-Hr Lot Constructability Desk
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_watch_bridge_map = array(
	'estate-microgrids-bc'                                                    => 'watch-estate-microgrids-bc',
	'architectural-concrete-bc'                                               => 'watch-architectural-concrete-bc',
	'net-zero-building-envelopes'                                             => 'watch-net-zero-building-envelopes',
	'net-zero-envelopes-bc'                                                   => 'watch-net-zero-building-envelopes',
	'inverted-roof-terraces-bc'                                               => 'watch-inverted-roof-terraces-bc',
	'hydronic-radiant-floor-erv-engineering'                                  => 'watch-hydronic-radiant-floor-erv-engineering',
	'bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide'         => 'watch-bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide',
	'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide'            => 'watch-vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide',
	'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide'            => 'watch-vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide',
	'west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide'  => 'watch-west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide',
	'why-4-storey-multiplexes-fail-lateral-shear'                             => 'watch-why-4-storey-multiplexes-fail-lateral-shear',
	'sea-to-sky-luxury-compounds-bc-building-code'                            => 'watch-sea-to-sky-luxury-compounds-bc-building-code',
);

$kp_wayne_avatar = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/wayne_whistler_builder_avatar.jpg';
?>

<main id="primary" class="kp-v3-page">
	<style id="kp-v3-single-post-styles">
		.kp-single-shell {
			padding: clamp(30px, 4.5vw, 62px) 0 clamp(44px, 6vw, 76px);
			background: #04070d;
			color: #f8fafc;
		}
		.kp-single-wrap {
			width: min(920px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-single-crumbs {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			color: #94a3b8;
			margin-bottom: 14px;
			display: flex;
			flex-wrap: wrap;
			gap: 6px;
		}
		.kp-single-crumbs a {
			color: #d4af37;
			text-decoration: none;
		}
		.kp-single-h1 {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.75rem, 3.5vw, 2.75rem);
			font-weight: 800;
			line-height: 1.14;
			letter-spacing: -0.02em;
			color: #f8fafc;
			margin: 0 0 18px;
			text-wrap: balance;
		}
		.kp-single-byline {
			display: flex;
			align-items: center;
			justify-content: space-between;
			flex-wrap: wrap;
			gap: 14px;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.3);
			border-radius: 16px;
			padding: 14px 18px;
			margin-bottom: 24px;
		}
		.kp-single-author {
			display: flex;
			align-items: center;
			gap: 12px;
		}
		.kp-single-author img {
			width: 48px;
			height: 48px;
			border-radius: 50%;
			object-fit: cover;
			border: 1.5px solid #d4af37;
			flex-shrink: 0;
		}
		.kp-single-watch-banner {
			background: linear-gradient(135deg, rgba(212, 175, 55, 0.14), rgba(56, 189, 248, 0.08));
			border: 1px solid rgba(212, 175, 55, 0.45);
			border-radius: 16px;
			padding: 16px 20px;
			margin-bottom: 28px;
			display: flex;
			justify-content: space-between;
			align-items: center;
			flex-wrap: wrap;
			gap: 14px;
		}
		.kp-single-prose {
			font-size: 1.02rem;
			line-height: 1.78;
			color: #e2e8f0;
		}
		.kp-single-prose h2,
		.kp-single-prose h3,
		.kp-single-prose h4 {
			font-family: 'Outfit', sans-serif;
			color: #f8fafc;
			line-height: 1.24;
			margin: 1.85em 0 0.65em;
		}
		.kp-single-prose h2 {
			font-size: clamp(1.38rem, 2.4vw, 1.85rem);
			border-bottom: 1px solid rgba(212, 175, 55, 0.2);
			padding-bottom: 8px;
		}
		.kp-single-prose p,
		.kp-single-prose ul,
		.kp-single-prose ol {
			margin: 0 0 1.25em;
		}
		.kp-single-prose a {
			color: #d4af37;
			text-decoration: underline;
			text-underline-offset: 3px;
		}
		.kp-single-prose blockquote {
			margin: 1.6em 0;
			padding: 16px 20px;
			background: #0a101d;
			border-left: 4px solid #d4af37;
			border-radius: 0 14px 14px 0;
			color: #f8fafc;
		}
		.kp-single-prose img,
		.kp-single-prose figure {
			max-width: 100%;
			height: auto;
			border-radius: 14px;
		}
		.kp-single-prose table {
			width: 100%;
			border-collapse: collapse;
			margin: 1.6em 0;
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.28);
			display: block;
			overflow-x: auto;
		}
		.kp-single-prose th,
		.kp-single-prose td {
			padding: 11px 14px;
			border-bottom: 1px solid rgba(255, 255, 255, 0.08);
			text-align: left;
			font-size: 0.9rem;
		}
		.kp-single-prose th {
			color: #d4af37;
			background: #060a14;
		}
	</style>

	<?php if ( have_posts() ) : while ( have_posts() ) : the_post();
		$kp_slug       = get_post_field( 'post_name', get_the_ID() );
		$kp_watch_slug = isset( $kp_watch_bridge_map[ $kp_slug ] ) ? $kp_watch_bridge_map[ $kp_slug ] : trim( (string) get_post_meta( get_the_ID(), '_kp_watch_slug', true ) );
		?>
		<article id="post-<?php the_ID(); ?>" <?php post_class( 'kp-single-shell' ); ?>>
			<div class="kp-single-wrap">
				<nav class="kp-single-crumbs" aria-label="Breadcrumb">
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>">Home</a>
					<span>/</span>
					<a href="<?php echo esc_url( home_url( '/keystone-possibilities-custom-homes/' ) ); ?>">Master Builder Series</a>
					<span>/</span>
					<span><?php the_title(); ?></span>
				</nav>

				<h1 class="kp-single-h1"><?php the_title(); ?></h1>

				<div class="kp-single-byline">
					<div class="kp-single-author">
						<img src="<?php echo esc_url( $kp_wayne_avatar ); ?>" alt="Wayne Stevenson — Principal & Licensed Builder #52603" />
						<div>
							<div style="font-family:'Outfit',sans-serif;font-size:0.96rem;font-weight:700;color:#f8fafc;">
								By Wayne Stevenson &mdash; Principal &amp; Heavy-Civil Superintendent
							</div>
							<div style="font-size:0.78rem;color:#cbd5e1;">
								BC Housing Licensed Builder #52603 &bull; BC Hydro ES54 Civil &bull; 20+ Yrs Kiewit Heavy-Civil Pedigree
							</div>
						</div>
					</div>
					<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#d4af37;">
						Updated <?php echo esc_html( get_the_modified_date( 'M j, Y' ) ); ?>
					</div>
				</div>

				<?php if ( '' !== $kp_watch_slug ) : ?>
					<div class="kp-single-watch-banner">
						<div>
							<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;color:#d4af37;">COMPANION 4K SUPERINTENDENT BRIEFING</div>
							<div style="font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:700;color:#f8fafc;">Watch the 4K Video Briefing &amp; Chapter Seek Breakdown</div>
						</div>
						<a href="<?php echo esc_url( home_url( '/videos/' . trim( $kp_watch_slug, '/' ) . '/' ) ); ?>" style="display:inline-flex;align-items:center;padding:10px 18px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.84rem;text-decoration:none;">
							&#9658; Open Dedicated Watch Page &rarr;
						</a>
					</div>
				<?php endif; ?>

				<div class="kp-single-prose">
					<?php the_content(); ?>
				</div>
			</div>
		</article>
	<?php endwhile; endif; ?>

	<?php get_template_part( 'template-parts/realtor-rule511-card' ); ?>
	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'west-vancouver' ) ); ?>
</main>

<?php
get_footer();
