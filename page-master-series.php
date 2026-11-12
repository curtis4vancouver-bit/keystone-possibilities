<?php
/**
 * Template Name: Master Builder Series Hub
 *
 * Dynamic WP_Query of all published technical blog blueprints + category filter pills +
 * Featured Long-Form 16:9 (HBy6NQQS3ks) + Companion 9:16 Vertical Short (SCzsJmJH_2M) +
 * direct links to companion /videos/[slug]/ Watch Pages.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

// Map published blog post slugs to their dedicated /videos/[watch-slug]/ Watch Pages.
$kp_companion_watch_map = array(
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

$kp_series_query = new WP_Query(
	array(
		'post_type'           => 'post',
		'post_status'         => 'publish',
		'posts_per_page'      => 36,
		'ignore_sticky_posts' => true,
	)
);
?>

<main id="primary" class="kp-v3-page">
	<style id="kp-v3-master-series-styles">
		.kp-ms-showcase {
			display: grid;
			grid-template-columns: 1.55fr 0.65fr;
			gap: 22px;
			align-items: stretch;
			margin-top: 24px;
		}
		@media (max-width: 960px) {
			.kp-ms-showcase {
				grid-template-columns: 1fr;
			}
		}
		.kp-ms-short-card {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.36);
			border-radius: 20px;
			padding: 16px;
			display: flex;
			flex-direction: column;
			gap: 12px;
		}
		.kp-ms-short-stage {
			position: relative;
			aspect-ratio: 9 / 16;
			max-height: 440px;
			margin: 0 auto;
			width: 100%;
			border-radius: 14px;
			overflow: hidden;
			background: #020409;
			cursor: pointer;
			background-size: cover;
			background-position: center;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		.kp-ms-short-stage iframe {
			position: absolute;
			inset: 0;
			width: 100%;
			height: 100%;
			border: 0;
		}
		.kp-ms-filter-bar {
			display: flex;
			flex-wrap: wrap;
			gap: 8px;
			margin: 20px 0 26px;
		}
		.kp-ms-pill {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.28);
			color: #cbd5e1;
			border-radius: 999px;
			padding: 8px 16px;
			font-size: 0.8rem;
			font-weight: 600;
			cursor: pointer;
		}
		.kp-ms-pill.is-active,
		.kp-ms-pill:hover {
			background: rgba(212, 175, 55, 0.18);
			border-color: #d4af37;
			color: #f8fafc;
		}
		.kp-ms-post-card[hidden] {
			display: none !important;
		}
	</style>

	<section class="kp-v3-hero" style="padding:clamp(34px,5vw,64px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">
				ARCHITECTURAL MASTER BUILDER SERIES &bull; BCBC 2024 TECHNICAL BLUEPRINTS
			</div>
			<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.95rem);font-weight:800;line-height:1.12;color:#f8fafc;margin:0 0 12px;max-width:900px;">
				Field-Tested Structural, Step Code 5, Multiplex &amp; ES54 Engineering Guides.
			</h1>
			<p style="font-size:1rem;line-height:1.62;color:#cbd5e1;max-width:820px;margin:0;">
				Authored by Principal &amp; Heavy-Civil Superintendent Wayne Stevenson (BC Housing #52603). Pair full-length 4K technical briefings with written BC Building Code 2024 construction specifications.
			</p>

			<div class="kp-ms-showcase">
				<div>
					<?php
					get_template_part(
						'template-parts/watch-player',
						null,
						array(
							'compact'   => true,
							'video_id'  => 'HBy6NQQS3ks',
							'pill'      => 'Featured Masterclass',
							'title'     => 'Best 800A Estate Microgrids & Private BC Hydro ES54 PMT Vault Clearances (BCBC 2024)',
							'duration'  => '09:14',
							'watch_url' => home_url( '/videos/estate-microgrids-bc/' ),
						)
					);
					?>
				</div>

				<aside class="kp-ms-short-card" aria-label="Companion 9:16 Field Briefing Short">
					<div style="display:flex;justify-content:space-between;align-items:center;">
						<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#d4af37;font-weight:700;">COMPANION 9:16 FIELD SHORT</span>
						<span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:#38bdf8;">60s BRIEF</span>
					</div>
					<div
						class="kp-ms-short-stage"
						style="background-image:linear-gradient(180deg,rgba(4,7,13,0.45),rgba(4,7,13,0.85)),url('https://i.ytimg.com/vi/SCzsJmJH_2M/hqdefault.jpg');"
						role="button"
						tabindex="0"
						aria-label="Play 9:16 Vertical Companion Short"
						data-ms-short="SCzsJmJH_2M"
					>
						<div style="width:58px;height:58px;border-radius:50%;background:#d4af37;color:#04070d;display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 12px 28px rgba(0,0,0,0.75);">
							&#9658;
						</div>
					</div>
					<div style="font-family:'Outfit',sans-serif;font-size:0.96rem;font-weight:700;color:#f8fafc;">
						Rapid Field Check: 800A Vault &amp; CEC Rule 26-242 3.0m Hot-Stick Clearance
					</div>
					<a href="<?php echo esc_url( home_url( '/videos/' ) ); ?>" style="font-size:0.8rem;font-weight:700;color:#d4af37;text-decoration:none;margin-top:auto;">
						Browse All 11 Dedicated Watch Pages &rarr;
					</a>
				</aside>
			</div>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;border-top:1px solid rgba(212,175,55,0.14);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.5rem,2.8vw,2.2rem);font-weight:700;color:#f8fafc;margin:0 0 8px;">
				Published Engineering Blueprints &amp; Code Guides
			</h2>

			<div class="kp-ms-filter-bar" role="tablist" aria-label="Filter Technical Blueprints">
				<button type="button" class="kp-ms-pill is-active" data-ms-filter="all">All Blueprints</button>
				<button type="button" class="kp-ms-pill" data-ms-filter="multiplex">Bill 44 &amp; R1-1 Multiplex</button>
				<button type="button" class="kp-ms-pill" data-ms-filter="structural">Structural, Concrete &amp; Slope</button>
				<button type="button" class="kp-ms-pill" data-ms-filter="envelope">Step Code 5, Roofs &amp; Mechanical</button>
				<button type="button" class="kp-ms-pill" data-ms-filter="fiduciary">Fiduciary PM, Permits &amp; Microgrids</button>
			</div>

			<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:20px;">
				<?php
				if ( $kp_series_query->have_posts() ) :
					while ( $kp_series_query->have_posts() ) :
						$kp_series_query->the_post();
						$p_slug = get_post_field( 'post_name', get_the_ID() );
						$p_lc   = strtolower( $p_slug . ' ' . get_the_title() );

						if ( false !== strpos( $p_lc, 'multiplex' ) || false !== strpos( $p_lc, 'bill-44' ) || false !== strpos( $p_lc, 'shear' ) ) {
							$topic = 'multiplex';
							$badge = 'MULTIPLEX & PART 4';
						} elseif ( false !== strpos( $p_lc, 'concrete' ) || false !== strpos( $p_lc, 'cantilever' ) || false !== strpos( $p_lc, 'snow' ) || false !== strpos( $p_lc, 'bedrock' ) || false !== strpos( $p_lc, 'foundation' ) || false !== strpos( $p_lc, 'creek' ) ) {
							$topic = 'structural';
							$badge = 'STRUCTURAL & GEOTECH';
						} elseif ( false !== strpos( $p_lc, 'envelope' ) || false !== strpos( $p_lc, 'step-code' ) || false !== strpos( $p_lc, 'roof' ) || false !== strpos( $p_lc, 'hydronic' ) || false !== strpos( $p_lc, 'waterproof' ) ) {
							$topic = 'envelope';
							$badge = 'ENVELOPE & MEP';
						} else {
							$topic = 'fiduciary';
							$badge = 'FIDUCIARY & CIVIL';
						}

						$watch_slug = isset( $kp_companion_watch_map[ $p_slug ] ) ? $kp_companion_watch_map[ $p_slug ] : (string) get_post_meta( get_the_ID(), '_kp_watch_slug', true );
						?>
						<article class="kp-v3-card kp-ms-post-card" data-ms-topic="<?php echo esc_attr( $topic ); ?>" style="background:#0a101d;border:1px solid rgba(212,175,55,0.24);border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:10px;">
							<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
								<span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:#d4af37;font-weight:700;"><?php echo esc_html( $badge ); ?></span>
								<span style="font-size:0.74rem;color:#94a3b8;"><?php echo esc_html( get_the_date( 'M Y' ) ); ?></span>
							</div>
							<h3 style="font-family:'Outfit',sans-serif;font-size:1.12rem;font-weight:700;line-height:1.32;margin:0;">
								<a href="<?php echo esc_url( get_permalink() ); ?>" style="color:#f8fafc;text-decoration:none;">
									<?php the_title(); ?>
								</a>
							</h3>
							<p style="font-size:0.85rem;line-height:1.58;color:#cbd5e1;margin:0;">
								<?php echo esc_html( wp_trim_words( get_the_excerpt(), 24 ) ); ?>
							</p>
							<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-top:auto;padding-top:12px;border-top:1px solid rgba(255,255,255,0.07);">
								<a href="<?php echo esc_url( get_permalink() ); ?>" style="font-size:0.8rem;font-weight:700;color:#d4af37;text-decoration:none;">
									Read Blueprint &rarr;
								</a>
								<?php if ( '' !== $watch_slug ) : ?>
									<a href="<?php echo esc_url( home_url( '/videos/' . trim( $watch_slug, '/' ) . '/' ) ); ?>" style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#38bdf8;text-decoration:none;font-weight:600;">
										&#9658; 4K Watch Page
									</a>
								<?php endif; ?>
							</div>
						</article>
						<?php
					endwhile;
					wp_reset_postdata();
				else :
					?>
					<div style="grid-column:1/-1;background:#0a101d;border:1px solid rgba(212,175,55,0.28);border-radius:16px;padding:26px;color:#cbd5e1;">
						Technical blueprints are syncing—explore our <a href="<?php echo esc_url( home_url( '/videos/' ) ); ?>" style="color:#d4af37;font-weight:700;">4K Video Briefing Library</a> or request a direct 48-hour parcel review below.
					</div>
				<?php endif; ?>
			</div>
		</div>
	</section>

	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'squamish' ) ); ?>

	<script>
	(function() {
		var shortBox = document.querySelector('[data-ms-short]');
		if (shortBox) {
			function playShort() {
				var id = shortBox.getAttribute('data-ms-short');
				if (!id || shortBox.querySelector('iframe')) return;
				var ifr = document.createElement('iframe');
				ifr.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&modestbranding=1';
				ifr.title = 'Keystone Possibilities Field Short';
				ifr.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
				ifr.allowFullscreen = true;
				shortBox.innerHTML = '';
				shortBox.appendChild(ifr);
			}
			shortBox.addEventListener('click', playShort);
			shortBox.addEventListener('keydown', function(e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); playShort(); } });
		}

		var pills = Array.prototype.slice.call(document.querySelectorAll('[data-ms-filter]'));
		var cards = Array.prototype.slice.call(document.querySelectorAll('[data-ms-topic]'));
		pills.forEach(function(pill) {
			pill.addEventListener('click', function() {
				var f = pill.getAttribute('data-ms-filter');
				pills.forEach(function(p) { p.classList.toggle('is-active', p === pill); });
				cards.forEach(function(c) {
					var show = (f === 'all' || c.getAttribute('data-ms-topic') === f);
					if (show) c.removeAttribute('hidden');
					else c.setAttribute('hidden', 'hidden');
				});
			});
		});
	})();
	</script>
</main>

<?php
get_footer();
