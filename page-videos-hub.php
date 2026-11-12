<?php
/**
 * Template Name: Videos Watch Hub
 * Template Post Type: page
 *
 * /videos/ Google Watch Hub index showcasing featured 4K @KeystonePossibilitiesLtd briefings
 * + full indexable grid of all 11 dedicated /videos/[slug]/ Watch Pages.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_watch_catalog = array(
	array(
		'slug'      => 'watch-west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide',
		'yt_id'     => 'kLsNyKvQswg',
		'duration'  => '08:42',
		'cat'       => 'STEP CODE 5 & CANTILEVERS',
		'title'     => 'West Vancouver & Whistler BCBC 2024 Step Code 5, Cantilevered Steel & ES54 Civil Guide',
		'post_slug' => 'west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide',
	),
	array(
		'slug'      => 'watch-why-4-storey-multiplexes-fail-lateral-shear',
		'yt_id'     => 'JwtaaZlrFeE',
		'duration'  => '07:19',
		'cat'       => 'PART 4 LATERAL SHEAR',
		'title'     => 'Why 4-Storey Bill 44 Multiplexes Fail Lateral Shear: BCBC 2024 Hold-Down Engineering',
		'post_slug' => 'why-4-storey-multiplexes-fail-lateral-shear',
	),
	array(
		'slug'      => 'watch-estate-microgrids-bc',
		'yt_id'     => 'HBy6NQQS3ks',
		'duration'  => '09:14',
		'cat'       => '800A MICROGRIDS & ES54',
		'title'     => 'Best 800A Estate Microgrids & Private BC Hydro ES54 PMT Vault Guide (CEC Rule 26-242)',
		'post_slug' => 'estate-microgrids-bc',
	),
	array(
		'slug'      => 'watch-sea-to-sky-luxury-compounds-bc-building-code',
		'yt_id'     => 'ERD0DiVkgYg',
		'duration'  => '08:15',
		'cat'       => 'BEDROCK & COMPOUNDS',
		'title'     => 'Sea-to-Sky Luxury Compounds: 2026 BC Building Code, FCL & Bedrock Anchoring',
		'post_slug' => 'sea-to-sky-luxury-compounds-bc-building-code',
	),
	array(
		'slug'      => 'watch-architectural-concrete-bc',
		'yt_id'     => 'qs7xlawF32k',
		'duration'  => '08:06',
		'cat'       => 'ARCHITECTURAL CONCRETE',
		'title'     => 'Architectural Board-Formed Concrete & Cantilevered Floating Stairs (Doka / Peri Specs)',
		'post_slug' => 'architectural-concrete-bc',
	),
	array(
		'slug'      => 'watch-net-zero-building-envelopes',
		'yt_id'     => 'sLXAtWGjeiA',
		'duration'  => '08:34',
		'cat'       => 'STEP CODE 5 ENVELOPES',
		'title'     => 'Net-Zero Building Envelopes: Proven BCBC 2024 Step Code 5 & <1.0 ACH50 Air-Barrier Guide',
		'post_slug' => 'net-zero-building-envelopes',
	),
	array(
		'slug'      => 'watch-inverted-roof-terraces-bc',
		'yt_id'     => 'W7eIvbv23Ew',
		'duration'  => '07:48',
		'cat'       => 'ROOFS & SNOW LOADS',
		'title'     => 'Inverted Roof Terraces & Whistler 8.1 kPa Alpine Cold Roofs: Waterproofing Engineering',
		'post_slug' => 'inverted-roof-terraces-bc',
	),
	array(
		'slug'      => 'watch-hydronic-radiant-floor-erv-engineering',
		'yt_id'     => 'v7r2uwF4eWU',
		'duration'  => '08:11',
		'cat'       => 'HYDRONIC & ZEHNDER ERV',
		'title'     => 'Hydronic Radiant Floor Manifolds, Air-to-Water Heat Pumps & ERV Balancing (BCBC 2024)',
		'post_slug' => 'hydronic-radiant-floor-erv-engineering',
	),
	array(
		'slug'      => 'watch-bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide',
		'yt_id'     => 'nPXnGzAEY6k',
		'duration'  => '08:29',
		'cat'       => 'HYDROSTATIC & RADON',
		'title'     => 'BCBC 2024 Luxury Basement Waterproofing, Hydrostatic Relief & Active Sub-Slab Radon Stacks',
		'post_slug' => 'bcbc-2024-luxury-basement-waterproofing-hydrostatic-radon-guide',
	),
	array(
		'slug'      => 'watch-vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide',
		'yt_id'     => 'SIHMOJ5AOyw',
		'duration'  => '07:55',
		'cat'       => 'R1-1 ADAPTABLE & MICROPILES',
		'title'     => 'Vancouver R1-1 Multiplex Adaptable Zero-Step Sills & Zero-Lot-Line Micropile Shoring',
		'post_slug' => 'vancouver-multiplex-bcbc-2024-adaptable-sill-micropile-guide',
	),
	array(
		'slug'      => 'watch-vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide',
		'yt_id'     => 'eV_Oo5ekaWc',
		'duration'  => '08:22',
		'cat'       => 'FIRE, STC 55+ & 2" WATER',
		'title'     => 'Vancouver Multiplex 1-Hr/2-Hr Fire Separations, STC 55+ Party Walls & 2-Inch Water Mains',
		'post_slug' => 'vancouver-multiplex-bcbc-2024-fire-acoustic-water-main-guide',
	),
);
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(34px,5vw,64px) 0 18px;background:#04070d;">
		<div style="width:min(1240px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">
				OFFICIAL 4K WATCH LIBRARY &bull; @KEYSTONEPOSSIBILITIESLTD &bull; VIDEOOBJECT INDEX
			</div>
			<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.9rem);font-weight:800;line-height:1.12;color:#f8fafc;margin:0 0 10px;">
				Superintendent Field Briefings &amp; BCBC 2024 Watch Pages.
			</h1>
			<p style="font-size:0.98rem;line-height:1.62;color:#cbd5e1;max-width:820px;margin:0;">
				Every video below resolves to a dedicated primary Watch Page featuring above-the-fold 4K playback, interactive chapter seek clips, direct engineering specifications, and its companion technical blueprint.
			</p>
		</div>
	</section>

	<?php get_template_part( 'template-parts/watch-player', null, array( 'heading' => 'Featured 4K Superintendent Briefings.' ) ); ?>

	<section style="padding:clamp(44px,6vw,84px) 0;background:#04070d;border-top:1px solid rgba(212,175,55,0.14);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.5rem,2.8vw,2.2rem);font-weight:700;color:#f8fafc;margin:0 0 24px;">
				All 11 Dedicated Engineering Watch Pages
			</h2>

			<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,350px),1fr));gap:22px;">
				<?php foreach ( $kp_watch_catalog as $vid ) :
					$watch_href = home_url( '/videos/' . $vid['slug'] . '/' );
					$post_href  = home_url( '/' . $vid['post_slug'] . '/' );
					$thumb      = 'https://i.ytimg.com/vi/' . rawurlencode( $vid['yt_id'] ) . '/hqdefault.jpg';
					?>
					<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.26);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;">
						<a href="<?php echo esc_url( $watch_href ); ?>" style="position:relative;aspect-ratio:16/9;display:block;background:#020408;overflow:hidden;text-decoration:none;">
							<img src="<?php echo esc_url( $thumb ); ?>" alt="<?php echo esc_attr( $vid['title'] ); ?>" style="width:100%;height:100%;object-fit:cover;display:block;" loading="lazy" />
							<span style="position:absolute;top:10px;left:10px;background:rgba(4,7,13,0.88);border:1px solid rgba(212,175,55,0.45);color:#d4af37;font-family:'JetBrains Mono',monospace;font-size:0.65rem;font-weight:700;padding:4px 9px;border-radius:999px;">
								<?php echo esc_html( $vid['cat'] ); ?>
							</span>
							<span style="position:absolute;bottom:10px;right:10px;background:rgba(4,7,13,0.9);border:1px solid rgba(56,189,248,0.4);color:#f8fafc;font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;padding:3px 8px;border-radius:6px;">
								&#9658; <?php echo esc_html( $vid['duration'] ); ?>
							</span>
						</a>
						<div style="padding:18px 20px;display:flex;flex-direction:column;gap:10px;flex:1;">
							<h3 style="font-family:'Outfit',sans-serif;font-size:1.06rem;font-weight:700;line-height:1.34;margin:0;">
								<a href="<?php echo esc_url( $watch_href ); ?>" style="color:#f8fafc;text-decoration:none;">
									<?php echo esc_html( $vid['title'] ); ?>
								</a>
							</h3>
							<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:auto;padding-top:10px;border-top:1px solid rgba(255,255,255,0.07);">
								<a href="<?php echo esc_url( $watch_href ); ?>" style="font-size:0.8rem;font-weight:700;color:#d4af37;text-decoration:none;">
									Open Watch Theater &rarr;
								</a>
								<a href="<?php echo esc_url( $post_href ); ?>" style="font-size:0.76rem;color:#cbd5e1;text-decoration:none;">
									Written Blueprint &nearr;
								</a>
							</div>
						</div>
					</article>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'squamish' ) ); ?>
</main>

<?php
get_footer();
