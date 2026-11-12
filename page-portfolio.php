<?php
/**
 * Template Name: Portfolio Showcase
 *
 * Full filterable showcase of all 9 real Signature Residences (42 gallery photos) +
 * 2 real 2023 ES54 Civil Fleet items via portfolio-reel.php in grid mode.
 * Zero watermarked magazine imagery; zero vertical bounce animation.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_ballantree_hero = 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.57.48-pm.png';
$kp_st_andrews_hero = 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.07.36-pm.png';
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(34px,5vw,68px) 0;background:radial-gradient(circle at 80% 15%,rgba(212,175,55,0.12),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:32px;align-items:center;">
			<div>
				<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">
					BUILT ARCHITECTURAL &amp; HEAVY-CIVIL RECORD &bull; BC BUILDER #52603
				</div>
				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.9rem,3.7vw,3rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;">
					9 Signature Coastal &amp; Alpine Residences (42 Photographs) + Self-Performed ES54 Civil.
				</h1>
				<p style="font-size:1rem;line-height:1.64;color:#cbd5e1;margin:0 0 22px;">
					From post-tensioned granite rock anchors at 5610 Ballantree Road in West Vancouver’s British Properties and 8.1 kPa alpine snow loads on Whistler’s Sunridge Plateau to multi-unit urban infill and Sunshine Coast foreshore estates—every project below is documented with real compliance specifications.
				</p>
				<div style="display:flex;flex-wrap:wrap;gap:12px;">
					<a href="#portfolio-grid" style="display:inline-flex;align-items:center;padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
						Explore All 42 Project Photos &darr;
					</a>
					<a href="#calculator" style="display:inline-flex;align-items:center;padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.44);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.86rem;text-decoration:none;">
						Model $/SF in Your Corridor &rarr;
					</a>
				</div>
			</div>

			<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
				<figure style="margin:0;border-radius:16px;overflow:hidden;border:1px solid rgba(212,175,55,0.38);background:#0a101d;">
					<img src="<?php echo esc_url( $kp_ballantree_hero ); ?>" alt="Ballantree Residence — British Properties, West Vancouver" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block;" fetchpriority="high" />
					<figcaption style="padding:10px 12px;font-size:0.76rem;color:#e2e8f0;">
						<strong style="color:#d4af37;display:block;">Ballantree Residence</strong>
						British Properties, West Vancouver
					</figcaption>
				</figure>
				<figure style="margin:0;border-radius:16px;overflow:hidden;border:1px solid rgba(212,175,55,0.38);background:#0a101d;">
					<img src="<?php echo esc_url( $kp_st_andrews_hero ); ?>" alt="St Andrews Residence — North Shore" style="width:100%;aspect-ratio:4/3;object-fit:cover;display:block;" loading="lazy" />
					<figcaption style="padding:10px 12px;font-size:0.76rem;color:#e2e8f0;">
						<strong style="color:#d4af37;display:block;">St Andrews Residence</strong>
						400A Cantilevered Luxury Build
					</figcaption>
				</figure>
			</div>
		</div>
	</section>

	<?php
	get_template_part(
		'template-parts/portfolio-reel',
		null,
		array(
			'mode'       => 'grid',
			'section_id' => 'portfolio-grid',
			'kicker'     => 'COMPLETE FILTERABLE GALLERY · CLICK ANY CARD FOR MULTI-PHOTO INSPECTION',
			'heading'    => 'Filter Residences & Civil Fleet by BC Corridor.',
		)
	);
	?>

	<?php get_template_part( 'template-parts/bill44-calculator', null, array( 'default_corridor' => 'west-vancouver' ) ); ?>
	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'west-vancouver' ) ); ?>
</main>

<?php
get_footer();
