<?php
/**
 * Default Page Template (page.php) — Quiet-Luxury v3.0 Shell
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<main id="primary" class="kp-v3-page" style="background:#04070d;color:#f8fafc;min-height:70vh;">
	<section style="padding:clamp(40px,6vw,78px) 0;">
		<div style="width:min(1040px,calc(100% - 32px));margin:0 auto;">
			<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
				<header style="margin-bottom:28px;border-bottom:1px solid rgba(212,175,55,0.2);padding-bottom:18px;">
					<div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#d4af37;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">
						KEYSTONE POSSIBILITIES LTD. &bull; BC BUILDER #52603
					</div>
					<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.85rem);font-weight:800;line-height:1.13;color:#f8fafc;margin:0;">
						<?php the_title(); ?>
					</h1>
				</header>

				<div style="font-size:1rem;line-height:1.74;color:#e2e8f0;">
					<?php the_content(); ?>
				</div>
			<?php endwhile; endif; ?>
		</div>
	</section>
</main>

<?php
get_footer();
