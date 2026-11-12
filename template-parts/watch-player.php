<?php
/**
 * Template Part: 4K Watch Superintendent Briefing Theater (youtube-nocookie.com)
 *
 * Click-to-play 16:9 theater with @KeystonePossibilitiesLtd verified badge, Official Keyhole
 * shield mark (ID 1639), 4K UHD · VIDEOOBJECT pill, optional multi-briefing switcher pills,
 * and interactive chapter-seek pills.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$kp_logos = function_exists( 'kp_get_official_logos' ) ? kp_get_official_logos() : array();
$kp_badge_logo = ! empty( $kp_logos['header_badge'] ) ? $kp_logos['header_badge'] : 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';

$kp_default_videos = array(
	array(
		'id'         => 'kLsNyKvQswg',
		'pill'       => '01 · Step Code 5, Cantilevers & ES54 Civil',
		'title'      => 'West Vancouver & Whistler Step Code 5 / EL-4, Cantilevered Steel & ES54 Civil Engineering',
		'duration'   => '08:42',
		'watch_url'  => home_url( '/videos/west-vancouver-whistler-step-code-5-cantilever-seismic/' ),
		'chapters'   => array(
			array( 'sec' => 0,   'label' => '00:00 · Granite Micropile & Slope Hold-Points' ),
			array( 'sec' => 118, 'label' => '01:58 · Thermal-Broken Cantilever Steel' ),
			array( 'sec' => 264, 'label' => '04:24 · Step Code 5 / EL-4 Air-Barrier (<1.0 ACH)' ),
			array( 'sec' => 395, 'label' => '06:35 · Self-Performed BC Hydro ES54 Ducts' ),
		),
	),
	array(
		'id'         => 'JwtaaZlrFeE',
		'pill'       => '02 · Why 4-Storey Multiplexes Fail Shear',
		'title'      => 'Why 4-Storey Bill 44 Multiplexes Fail Lateral Shear: BCBC 2024 Part 4 Hold-Downs',
		'duration'   => '07:19',
		'watch_url'  => home_url( '/videos/why-4-storey-multiplexes-fail-lateral-shear/' ),
		'chapters'   => array(
			array( 'sec' => 0,   'label' => '00:00 · Open Ground-Floor Glazing Drift Traps' ),
			array( 'sec' => 105, 'label' => '01:45 · Simpson ATS Continuous Rod Tie-Downs' ),
			array( 'sec' => 240, 'label' => '04:00 · STC 55+ Fire & Acoustic Party Walls' ),
			array( 'sec' => 350, 'label' => '05:50 · Pre-Offer Structural Grid Audit' ),
		),
	),
	array(
		'id'         => 'HBy6NQQS3ks',
		'pill'       => '03 · 800A Estate Microgrids & PMT Vaults',
		'title'      => '800A Estate Microgrids & Private BC Hydro ES54 PMT Vault Clearances (CEC Rule 26-242)',
		'duration'   => '09:14',
		'watch_url'  => home_url( '/videos/estate-microgrids-bc/' ),
		'chapters'   => array(
			array( 'sec' => 0,   'label' => '00:00 · When 400A Fails Heat-Pump + EV Loads' ),
			array( 'sec' => 132, 'label' => '02:12 · CEC Rule 26-242 3.0m Hot-Stick Clearance' ),
			array( 'sec' => 290, 'label' => '04:50 · DB2 PVC Duct Bank Depth (>=900mm/1050mm)' ),
			array( 'sec' => 430, 'label' => '07:10 · Battery/Generator Automatic Transfer' ),
		),
	),
);

$kp_videos = ! empty( $args['videos'] ) && is_array( $args['videos'] ) ? $args['videos'] : $kp_default_videos;

// Allow single-video shorthand via $args['video_id'].
if ( ! empty( $args['video_id'] ) && empty( $args['videos'] ) ) {
	$vid_clean = preg_replace( '/[^A-Za-z0-9_-]/', '', (string) $args['video_id'] );
	// Never allow legacy non-Possibilities video IDs starting with y67f-.
	if ( '' === $vid_clean || 0 === strpos( $vid_clean, 'y67f-' ) ) {
		$vid_clean = 'ERD0DiVkgYg';
	}
	$kp_videos = array(
		array(
			'id'        => $vid_clean,
			'pill'      => isset( $args['pill'] ) ? (string) $args['pill'] : 'Superintendent Briefing',
			'title'     => isset( $args['title'] ) ? (string) $args['title'] : 'Keystone Possibilities Field Engineering Briefing',
			'duration'  => isset( $args['duration'] ) ? (string) $args['duration'] : '08:20',
			'watch_url' => isset( $args['watch_url'] ) ? (string) $args['watch_url'] : home_url( '/videos/' ),
			'chapters'  => isset( $args['chapters'] ) && is_array( $args['chapters'] ) ? $args['chapters'] : array(
				array( 'sec' => 0,   'label' => '00:00 · Site Geotechnical & Civil Scope' ),
				array( 'sec' => 120, 'label' => '02:00 · BCBC 2024 Structural & Step Code Gates' ),
				array( 'sec' => 255, 'label' => '04:15 · Open-Book CCDC 5B Cost Governance' ),
			),
		),
	);
}

$kp_compact    = ! empty( $args['compact'] );
$kp_section_id = isset( $args['section_id'] ) ? sanitize_html_class( (string) $args['section_id'] ) : 'watch-briefing';
$kp_kicker     = isset( $args['kicker'] ) ? (string) $args['kicker'] : '4K SUPERINTENDENT BRIEFING THEATER · @KEYSTONEPOSSIBILITIESLTD';
$kp_heading    = isset( $args['heading'] ) ? (string) $args['heading'] : 'Verify How We Engineer Rock, Shear Walls & Underground ES54 Civil.';
$kp_watch_uid  = wp_unique_id( 'kp-watch-' );
$kp_first      = $kp_videos[0];
$kp_thumb_url  = ! empty( $kp_first['poster'] ) ? $kp_first['poster'] : 'https://i.ytimg.com/vi/' . rawurlencode( $kp_first['id'] ) . '/maxresdefault.jpg';

if ( empty( $GLOBALS['kp_v3_watch_player_css'] ) ) :
	$GLOBALS['kp_v3_watch_player_css'] = true;
	?>
	<style id="kp-v3-watch-player-styles">
		.kp-watch-section {
			padding: clamp(48px, 6vw, 84px) 0;
			background: #04070d;
			color: #f8fafc;
			border-top: 1px solid rgba(212, 175, 55, 0.14);
		}
		.kp-watch-wrap {
			width: min(1240px, calc(100% - 32px));
			margin: 0 auto;
		}
		.kp-watch-compact {
			width: 100%;
		}
		.kp-watch-head {
			display: flex;
			flex-wrap: wrap;
			justify-content: space-between;
			align-items: flex-end;
			gap: 16px;
			margin-bottom: 20px;
		}
		.kp-watch-kicker {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.72rem;
			font-weight: 600;
			letter-spacing: 0.08em;
			text-transform: uppercase;
			color: #d4af37;
			margin-bottom: 6px;
		}
		.kp-watch-h2 {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1.5rem, 2.8vw, 2.15rem);
			font-weight: 700;
			line-height: 1.16;
			color: #f8fafc;
			margin: 0;
			max-width: 780px;
		}
		.kp-watch-switchers {
			display: flex;
			flex-wrap: wrap;
			gap: 8px;
			margin-bottom: 16px;
		}
		.kp-watch-sw-btn {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.28);
			color: #cbd5e1;
			border-radius: 999px;
			padding: 8px 15px;
			min-height: 38px;
			font-size: 0.78rem;
			font-weight: 600;
			cursor: pointer;
			transition: all 0.2s ease;
		}
		.kp-watch-sw-btn:hover,
		.kp-watch-sw-btn.is-active {
			background: rgba(212, 175, 55, 0.18);
			border-color: #d4af37;
			color: #f8fafc;
		}
		.kp-watch-frame-card {
			background: #0a101d;
			border: 1px solid rgba(212, 175, 55, 0.36);
			border-radius: 20px;
			overflow: hidden;
			box-shadow: 0 26px 64px rgba(0, 0, 0, 0.72);
		}
		.kp-watch-stage {
			position: relative;
			aspect-ratio: 16 / 9;
			background: #020409;
			overflow: hidden;
		}
		.kp-watch-stage iframe,
		.kp-watch-poster {
			position: absolute;
			inset: 0;
			width: 100%;
			height: 100%;
			border: 0;
		}
		.kp-watch-poster {
			cursor: pointer;
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			padding: clamp(12px, 2.4vw, 22px);
			background-size: cover;
			background-position: center;
		}
		.kp-watch-poster::before {
			content: '';
			position: absolute;
			inset: 0;
			background: linear-gradient(180deg, rgba(4, 7, 13, 0.68) 0%, rgba(4, 7, 13, 0.32) 48%, rgba(4, 7, 13, 0.88) 100%);
		}
		.kp-watch-top-bar,
		.kp-watch-bottom-bar,
		.kp-watch-play-center {
			position: relative;
			z-index: 2;
		}
		.kp-watch-top-bar {
			display: flex;
			justify-content: space-between;
			align-items: center;
			flex-wrap: wrap;
			gap: 8px;
		}
		.kp-watch-chan-pill {
			display: inline-flex;
			align-items: center;
			gap: 8px;
			background: rgba(4, 7, 13, 0.86);
			backdrop-filter: blur(10px);
			border: 1px solid rgba(212, 175, 55, 0.45);
			border-radius: 999px;
			padding: 5px 12px 5px 6px;
			font-size: 0.74rem;
			font-weight: 700;
			color: #f8fafc;
		}
		.kp-watch-chan-pill img {
			width: 24px;
			height: 24px;
			border-radius: 6px;
			object-fit: contain;
		}
		.kp-watch-uhd-pill {
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.68rem;
			font-weight: 700;
			color: #38bdf8;
			background: rgba(4, 7, 13, 0.86);
			border: 1px solid rgba(56, 189, 248, 0.38);
			border-radius: 999px;
			padding: 5px 11px;
		}
		.kp-watch-play-center {
			align-self: center;
			width: clamp(64px, 8vw, 84px);
			height: clamp(64px, 8vw, 84px);
			border-radius: 50%;
			background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 55%, #b89028 100%);
			color: #04070d;
			border: 3px solid rgba(255, 255, 255, 0.85);
			display: flex;
			align-items: center;
			justify-content: center;
			box-shadow: 0 16px 42px rgba(0, 0, 0, 0.8), 0 0 28px rgba(212, 175, 55, 0.45);
			transition: transform 0.22s ease;
		}
		.kp-watch-poster:hover .kp-watch-play-center {
			transform: scale(1.07);
		}
		.kp-watch-bottom-bar {
			display: flex;
			justify-content: space-between;
			align-items: flex-end;
			gap: 12px;
			flex-wrap: wrap;
		}
		.kp-watch-vid-title {
			font-family: 'Outfit', sans-serif;
			font-size: clamp(1rem, 2vw, 1.32rem);
			font-weight: 700;
			color: #f8fafc;
			margin: 0;
			max-width: 780px;
			text-align: left;
		}
		.kp-watch-chapters {
			display: flex;
			flex-wrap: wrap;
			align-items: center;
			justify-content: space-between;
			gap: 10px;
			padding: 14px 18px;
			background: #070c17;
			border-top: 1px solid rgba(212, 175, 55, 0.2);
		}
		.kp-watch-chap-list {
			display: flex;
			flex-wrap: wrap;
			gap: 8px;
		}
		.kp-watch-chap-btn {
			background: rgba(255, 255, 255, 0.04);
			border: 1px solid rgba(212, 175, 55, 0.24);
			color: #e2e8f0;
			border-radius: 999px;
			padding: 6px 12px;
			font-family: 'JetBrains Mono', monospace;
			font-size: 0.7rem;
			cursor: pointer;
			transition: border-color 0.18s ease, color 0.18s ease;
		}
		.kp-watch-chap-btn:hover {
			border-color: #d4af37;
			color: #d4af37;
		}
		.kp-watch-hub-link {
			font-size: 0.78rem;
			font-weight: 700;
			color: #d4af37;
			text-decoration: none;
			white-space: nowrap;
		}
	</style>
<?php endif; ?>

<?php if ( ! $kp_compact ) : ?>
<section id="<?php echo esc_attr( $kp_section_id ); ?>" class="kp-watch-section">
	<div class="kp-watch-wrap" data-kp-watch="<?php echo esc_attr( $kp_watch_uid ); ?>">
		<div class="kp-watch-head">
			<div>
				<div class="kp-watch-kicker"><?php echo esc_html( $kp_kicker ); ?></div>
				<h2 class="kp-watch-h2"><?php echo esc_html( $kp_heading ); ?></h2>
			</div>
			<a href="<?php echo esc_url( home_url( '/videos/' ) ); ?>" class="kp-watch-hub-link">All 4K Engineering Briefings &rarr;</a>
		</div>
<?php else : ?>
	<div class="kp-watch-compact" data-kp-watch="<?php echo esc_attr( $kp_watch_uid ); ?>">
<?php endif; ?>

		<?php if ( count( $kp_videos ) > 1 ) : ?>
			<div class="kp-watch-switchers" role="tablist" aria-label="Select Superintendent Video Briefing">
				<?php foreach ( $kp_videos as $v_idx => $v_item ) : ?>
					<button
						type="button"
						class="kp-watch-sw-btn<?php echo 0 === $v_idx ? ' is-active' : ''; ?>"
						data-watch-select="<?php echo esc_attr( (string) $v_idx ); ?>"
					>
						<?php echo esc_html( $v_item['pill'] ); ?>
					</button>
				<?php endforeach; ?>
			</div>
		<?php endif; ?>

		<div class="kp-watch-frame-card">
			<div class="kp-watch-stage" data-watch-stage>
				<div
					class="kp-watch-poster"
					role="button"
					tabindex="0"
					aria-label="<?php echo esc_attr( 'Play 4K Briefing: ' . $kp_first['title'] ); ?>"
					style="background-image:url('<?php echo esc_url( $kp_thumb_url ); ?>');"
					data-watch-poster
				>
					<div class="kp-watch-top-bar">
						<span class="kp-watch-chan-pill">
							<img src="<?php echo esc_url( $kp_badge_logo ); ?>" alt="Keystone Possibilities Shield" width="24" height="24" />
							<span>@KeystonePossibilitiesLtd &bull; Verified Principal</span>
						</span>
						<span class="kp-watch-uhd-pill" data-watch-dur>4K UHD &bull; VIDEOOBJECT &bull; <?php echo esc_html( $kp_first['duration'] ?? '08:42' ); ?></span>
					</div>

					<div class="kp-watch-play-center" aria-hidden="true">
						<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
					</div>

					<div class="kp-watch-bottom-bar">
						<h3 class="kp-watch-vid-title" data-watch-title><?php echo esc_html( $kp_first['title'] ); ?></h3>
					</div>
				</div>
			</div>

			<div class="kp-watch-chapters">
				<div class="kp-watch-chap-list" data-watch-chapters>
					<?php foreach ( ( $kp_first['chapters'] ?? array() ) as $ch ) : ?>
						<button type="button" class="kp-watch-chap-btn" data-seek="<?php echo esc_attr( (string) intval( $ch['sec'] ) ); ?>">
							<?php echo esc_html( $ch['label'] ); ?>
						</button>
					<?php endforeach; ?>
				</div>
				<a href="<?php echo esc_url( $kp_first['watch_url'] ?? home_url( '/videos/' ) ); ?>" class="kp-watch-hub-link" data-watch-dedicated-link>
					Dedicated Watch Page &amp; Transcript &rarr;
				</a>
			</div>
		</div>

		<script>
		(function() {
			var root = document.querySelector('[data-kp-watch="<?php echo esc_js( $kp_watch_uid ); ?>"]');
			if (!root) return;
			var videos = <?php echo wp_json_encode( array_values( $kp_videos ) ); ?>;
			var stage = root.querySelector('[data-watch-stage]');
			var poster = root.querySelector('[data-watch-poster]');
			var titleEl = root.querySelector('[data-watch-title]');
			var durEl = root.querySelector('[data-watch-dur]');
			var chapWrap = root.querySelector('[data-watch-chapters]');
			var dedLink = root.querySelector('[data-watch-dedicated-link]');
			var swBtns = Array.prototype.slice.call(root.querySelectorAll('[data-watch-select]'));
			var currentIdx = 0;

			function mountIframe(videoId, startSec) {
				var oldIframe = stage.querySelector('iframe');
				if (oldIframe) oldIframe.remove();
				var ifr = document.createElement('iframe');
				var startParam = startSec > 0 ? '&start=' + encodeURIComponent(String(startSec)) : '';
				ifr.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(videoId) + '?autoplay=1&rel=0&modestbranding=1' + startParam;
				ifr.title = videos[currentIdx] ? videos[currentIdx].title : 'Keystone Superintendent Briefing';
				ifr.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
				ifr.allowFullscreen = true;
				poster.style.display = 'none';
				stage.appendChild(ifr);
			}

			function bindChapterButtons() {
				Array.prototype.forEach.call(chapWrap.querySelectorAll('[data-seek]'), function(btn) {
					btn.addEventListener('click', function() {
						var sec = parseInt(btn.getAttribute('data-seek'), 10) || 0;
						mountIframe(videos[currentIdx].id, sec);
					});
				});
			}

			function selectVideo(idx, autoPlay) {
				currentIdx = idx;
				var v = videos[idx];
				if (!v) return;
				var oldIframe = stage.querySelector('iframe');
				if (oldIframe) oldIframe.remove();
				poster.style.display = 'flex';
				poster.style.backgroundImage = "url('" + (v.poster || ('https://i.ytimg.com/vi/' + encodeURIComponent(v.id) + '/maxresdefault.jpg')) + "')";
				titleEl.textContent = v.title;
				if (durEl) durEl.textContent = '4K UHD · VIDEOOBJECT · ' + (v.duration || '08:30');
				if (dedLink && v.watch_url) dedLink.href = v.watch_url;

				chapWrap.innerHTML = '';
				(v.chapters || []).forEach(function(ch) {
					var b = document.createElement('button');
					b.type = 'button';
					b.className = 'kp-watch-chap-btn';
					b.setAttribute('data-seek', String(ch.sec || 0));
					b.textContent = ch.label;
					chapWrap.appendChild(b);
				});
				bindChapterButtons();
				if (autoPlay) mountIframe(v.id, 0);
			}

			poster.addEventListener('click', function() { mountIframe(videos[currentIdx].id, 0); });
			poster.addEventListener('keydown', function(e) {
				if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); mountIframe(videos[currentIdx].id, 0); }
			});

			swBtns.forEach(function(btn) {
				btn.addEventListener('click', function() {
					var idx = parseInt(btn.getAttribute('data-watch-select'), 10) || 0;
					swBtns.forEach(function(b) { b.classList.toggle('is-active', b === btn); });
					selectVideo(idx, false);
				});
			});

			bindChapterButtons();
		})();
		</script>

<?php if ( ! $kp_compact ) : ?>
	</div>
</section>
<?php else : ?>
	</div>
<?php endif; ?>
