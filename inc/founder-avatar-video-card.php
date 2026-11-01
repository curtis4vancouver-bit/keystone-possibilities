<?php
/**
 * Founder Avatar 4K Video Card & Chapter Seek Component — Keystone Possibilities Ltd.
 *
 * Renders Quiet Luxury architectural video cards backed by wp_options:
 *   - 'feasibility' -> kp_video_id_feasibility
 *   - 'bill44'      -> kp_video_id_bill44_multiplex
 *   - 'stepcode5'   -> kp_video_id_stepcode5_custom
 *
 * Design Invariants (Rule 30 & Rule 33):
 *   - Obsidian (#04070d), Glassmorphic Card (rgba(10, 15, 25, 0.92)), Sovereign Gold (#d4af37),
 *     Luminous Baby Blue (#38bdf8), 18px card radius, 9999px pill buttons.
 *   - Enqueues CSS & JS in wp_head AND applies inline styles so WordPress/Jetpack content
 *     filters never strip widescreen 16:9 sizing or allow Astra blue button defaults.
 *   - Zero emerald green drift, zero hardcoded retainer prices,
 *     zero horizontal overflow, zero broken iframe when wp_option is empty.
 *
 * @package KeystonePossibilitiesChild
 * @version 2.9.1
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Return canonical metadata and chapter matrices for all 3 Founder Avatar video slots.
 *
 * @return array<string, array<string, mixed>>
 */
function kp_get_founder_avatar_video_slots(): array {
	return array(
		'feasibility' => array(
			'option'       => 'kp_video_id_feasibility',
			'badge'        => 'BUILDER #52603 • PRE-CONSTRUCTION FEASIBILITY BRIEFING',
			'title'        => 'Turnkey Land & Construction Feasibility Plans — Builder #52603 Breakdown (3:30)',
			'description'  => 'Wayne Stevenson (BC Housing Licensed Residential Builder #52603 & BC Hydro ES54 Registered Civil Contractor) breaks down pre-acquisition parcel due diligence, municipal zoning & OCP verification, civil water/sewer/ES54 capacity, geotechnical & 30m RAPR riparian setbacks, DCC/ACC pro-forma modeling, and DP/BP critical-path scheduling.',
			'duration_iso' => 'PT3M30S',
			'total_sec'    => 210,
			'chapters'     => array(
				array(
					'time'    => '0:00',
					'title'   => 'Due Diligence',
					'seconds' => 0,
				),
				array(
					'time'    => '0:30',
					'title'   => 'Zoning & OCP',
					'seconds' => 30,
				),
				array(
					'time'    => '0:50',
					'title'   => 'Civil Water/Sewer',
					'seconds' => 50,
				),
				array(
					'time'    => '1:30',
					'title'   => 'Geotech & 30m RAPR',
					'seconds' => 90,
				),
				array(
					'time'    => '2:10',
					'title'   => 'DCC/ACC Pro-Forma',
					'seconds' => 130,
				),
				array(
					'time'    => '2:40',
					'title'   => 'DP/BP Critical Path',
					'seconds' => 160,
				),
			),
		),
		'bill44'      => array(
			'option'       => 'kp_video_id_bill44_multiplex',
			'badge'        => 'BC BILL 44 SSMUH • STATUTORY & BCBC 2024 ENGINEERING BRIEFING',
			'title'        => 'BC Bill 44 Multiplex (3-to-6 Unit SSMUH) — Statutory, BCBC 2024 & Pro-Forma Breakdown (3:00)',
			'description'  => 'Executive engineering breakdown of BC Bill 44 Small-Scale Multi-Unit Housing (SSMUH) rules, 3/4/6-unit parcel size thresholds, Frequent Transit Development Area zero-parking rules, statutory exemptions, BC Building Code 2024 Section 9.10 fire & ASTC 47 acoustic separations, and civil servicing.',
			'duration_iso' => 'PT3M00S',
			'total_sec'    => 180,
			'chapters'     => array(
				array(
					'time'    => '0:00',
					'title'   => 'SSMUH Rules',
					'seconds' => 0,
				),
				array(
					'time'    => '0:20',
					'title'   => '3, 4 & 6-Unit Thresholds',
					'seconds' => 20,
				),
				array(
					'time'    => '0:50',
					'title'   => 'Frequent Transit 0-Parking',
					'seconds' => 50,
				),
				array(
					'time'    => '1:30',
					'title'   => 'Exemptions',
					'seconds' => 90,
				),
				array(
					'time'    => '2:00',
					'title'   => 'Fire 9.10 & ASTC 47',
					'seconds' => 120,
				),
				array(
					'time'    => '2:20',
					'title'   => 'Civil & Estimator',
					'seconds' => 140,
				),
			),
		),
		'stepcode5'   => array(
			'option'       => 'kp_video_id_stepcode5_custom',
			'badge'        => 'BC ENERGY STEP CODE 5 • COASTAL & ALPINE ENVELOPE BRIEFING',
			'title'        => 'Sea-to-Sky & Vancouver Island Custom Homes — BC Energy Step Code 5 Breakdown (2:30)',
			'description'  => 'Licensed BC Builder #52603 technical walkthrough of coastal and alpine custom home envelope engineering, BC Energy Step Code Level 5 & HOT2000 energy modeling, ≤ 1.0 ACH50 blower-door airtightness verification, continuous exterior mineral-wool insulation with triple-glazed fenestration, and 2-5-10 warranty milestones.',
			'duration_iso' => 'PT2M30S',
			'total_sec'    => 150,
			'chapters'     => array(
				array(
					'time'    => '0:00',
					'title'   => 'Coastal & Alpine Envelope',
					'seconds' => 0,
				),
				array(
					'time'    => '0:30',
					'title'   => 'Step 5 & HOT2000',
					'seconds' => 30,
				),
				array(
					'time'    => '1:00',
					'title'   => '≤ 1.0 ACH50 Blower-Door',
					'seconds' => 60,
				),
				array(
					'time'    => '1:20',
					'title'   => 'Exterior Mineral-Wool & Triple-Glaze',
					'seconds' => 80,
				),
				array(
					'time'    => '2:00',
					'title'   => 'Milestones & 2-5-10 Warranty',
					'seconds' => 120,
				),
			),
		),
	);
}

/**
 * Normalize slot aliases so shortcode or template callers always resolve cleanly.
 *
 * @param string $slot Raw slot identifier.
 * @return string Canonical slot key ('feasibility', 'bill44', 'stepcode5') or ''.
 */
function kp_normalize_founder_video_slot( string $slot ): string {
	$clean = strtolower( trim( $slot ) );
	$map   = array(
		'feasibility'           => 'feasibility',
		'feasibility_plan'      => 'feasibility',
		'retainer'              => 'feasibility',
		'bill44'                => 'bill44',
		'bill44_multiplex'      => 'bill44',
		'multiplex'             => 'bill44',
		'stepcode5'             => 'stepcode5',
		'stepcode5_custom'      => 'stepcode5',
		'step-code-5'           => 'stepcode5',
		'custom'                => 'stepcode5',
	);
	return $map[ $clean ] ?? '';
}

/**
 * Emit Quiet Luxury CSS & chapter-seek JS in <head> so WordPress content filters never strip them
 * and Astra theme button rules (#0274be) never override our Obsidian/Baby-Blue/Gold pills.
 */
function kp_print_founder_avatar_video_head_assets(): void {
	if ( ! empty( $GLOBALS['kp_founder_video_head_printed'] ) ) {
		return;
	}
	$GLOBALS['kp_founder_video_head_printed'] = true;
	?>
	<style id="kp-founder-avatar-video-card-css">
	.kp-founder-video-card {
		background: rgba(10, 15, 25, 0.92) !important;
		border: 1.5px solid rgba(212, 175, 55, 0.45) !important;
		border-radius: 18px !important;
		padding: 22px 24px !important;
		margin: 1.75rem auto 2.25rem auto !important;
		max-width: 1080px !important;
		width: 100% !important;
		box-sizing: border-box !important;
		overflow: hidden !important;
		box-shadow: 0 18px 46px rgba(0, 0, 0, 0.78) !important;
		color: #f8fafc !important;
	}
	.kp-founder-video-topbar {
		display: flex !important;
		align-items: center !important;
		justify-content: space-between !important;
		flex-wrap: wrap !important;
		gap: 10px !important;
		margin-bottom: 12px !important;
	}
	.kp-founder-video-badge {
		display: inline-flex !important;
		align-items: center !important;
		gap: 8px !important;
		background: #04070d !important;
		border: 1px solid rgba(212, 175, 55, 0.6) !important;
		border-radius: 9999px !important;
		padding: 5px 14px !important;
		color: #d4af37 !important;
		font-family: 'JetBrains Mono', monospace !important;
		font-size: 0.72rem !important;
		font-weight: 800 !important;
		letter-spacing: 0.04em !important;
		text-transform: uppercase !important;
		max-width: 100% !important;
		box-sizing: border-box !important;
	}
	a.kp-founder-video-cta-pill,
	.kp-founder-video-cta-pill {
		display: inline-flex !important;
		align-items: center !important;
		justify-content: center !important;
		gap: 6px !important;
		background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 55%, #aa8010 100%) !important;
		color: #04070d !important;
		-webkit-text-fill-color: #04070d !important;
		border: none !important;
		border-radius: 9999px !important;
		padding: 8px 18px !important;
		font-family: 'Outfit', 'Inter', sans-serif !important;
		font-size: 0.80rem !important;
		font-weight: 800 !important;
		letter-spacing: 0.02em !important;
		text-decoration: none !important;
		cursor: pointer !important;
		box-shadow: 0 6px 18px rgba(212, 175, 55, 0.34) !important;
		transition: transform 0.18s ease, box-shadow 0.18s ease !important;
		box-sizing: border-box !important;
	}
	.kp-founder-video-heading {
		font-family: 'Outfit', 'Inter', sans-serif !important;
		font-size: clamp(1.14rem, 2.05vw, 1.38rem) !important;
		font-weight: 800 !important;
		color: #ffffff !important;
		margin: 0 0 14px 0 !important;
		line-height: 1.32 !important;
	}
	.kp-founder-video-frame-wrap {
		position: relative !important;
		width: 100% !important;
		padding-bottom: 56.25% !important;
		height: 0 !important;
		background: #04070d !important;
		border: 1.5px solid rgba(56, 189, 248, 0.38) !important;
		border-radius: 14px !important;
		overflow: hidden !important;
		box-sizing: border-box !important;
	}
	.kp-founder-video-frame-wrap iframe {
		position: absolute !important;
		top: 0 !important;
		left: 0 !important;
		width: 100% !important;
		height: 100% !important;
		border: 0 !important;
		margin: 0 !important;
	}
	.kp-founder-chapter-bar {
		display: flex !important;
		flex-wrap: wrap !important;
		align-items: center !important;
		gap: 8px !important;
		margin-top: 14px !important;
		padding-top: 12px !important;
		border-top: 1px solid rgba(212, 175, 55, 0.25) !important;
		max-width: 100% !important;
		box-sizing: border-box !important;
	}
	button.kp-founder-chapter-pill,
	.kp-founder-chapter-pill {
		display: inline-flex !important;
		align-items: center !important;
		gap: 6px !important;
		background: #04070d !important;
		background-color: #04070d !important;
		border: 1px solid rgba(56, 189, 248, 0.48) !important;
		border-radius: 9999px !important;
		padding: 7px 14px !important;
		color: #f8fafc !important;
		font-family: 'Outfit', 'Inter', sans-serif !important;
		font-size: 0.78rem !important;
		font-weight: 700 !important;
		line-height: 1.2 !important;
		cursor: pointer !important;
		transition: all 0.18s ease !important;
		max-width: 100% !important;
		box-sizing: border-box !important;
		box-shadow: none !important;
		text-transform: none !important;
	}
	button.kp-founder-chapter-pill:hover,
	button.kp-founder-chapter-pill.is-active,
	.kp-founder-chapter-pill:hover,
	.kp-founder-chapter-pill.is-active {
		border-color: #d4af37 !important;
		background: rgba(212, 175, 55, 0.16) !important;
		background-color: rgba(212, 175, 55, 0.16) !important;
		color: #ffffff !important;
		box-shadow: 0 4px 14px rgba(212, 175, 55, 0.24) !important;
	}
	.kp-founder-chapter-ts {
		color: #38bdf8 !important;
		font-family: 'JetBrains Mono', monospace !important;
		font-size: 0.72rem !important;
		font-weight: 800 !important;
		white-space: nowrap !important;
	}
	button.kp-founder-chapter-pill.is-active .kp-founder-chapter-ts,
	button.kp-founder-chapter-pill:hover .kp-founder-chapter-ts {
		color: #d4af37 !important;
	}
	.kp-founder-video-card ~ section .luxury-video-facade,
	.kp-founder-video-card + section .luxury-video-facade {
		display: none !important;
	}
	.kp-founder-video-card + section[style*="-50px"] {
		margin-top: 0 !important;
	}
	@media (max-width: 640px) {
		.kp-founder-video-card {
			padding: 16px 14px !important;
		}
		button.kp-founder-chapter-pill {
			font-size: 0.73rem !important;
			padding: 6px 11px !important;
		}
	}
	</style>
	<script id="kp-founder-avatar-video-card-js">
	window.kpSeekFounderAvatarVideo = function(iframeId, videoId, startSec, btnEl) {
		var iframe = document.getElementById(iframeId);
		if (!iframe || !videoId) return;
		var sec = Math.max(0, parseInt(startSec, 10) || 0);
		iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(videoId) + '?start=' + sec + '&autoplay=1&rel=0&modestbranding=1';
		if (btnEl && btnEl.parentNode) {
			var pills = btnEl.parentNode.querySelectorAll('.kp-founder-chapter-pill');
			for (var i = 0; i < pills.length; i++) {
				pills[i].classList.remove('is-active');
			}
			btnEl.classList.add('is-active');
		}
	};
	window.kpScrollToParcelReview = function(evt) {
		var target = document.getElementById('kp-feasibility-intake')
			|| document.querySelector('form[action*="/keystone/v1/lead"]')
			|| document.getElementById('kp-b44-gate-form')
			|| document.getElementById('custom-build-planner');
		if (target) {
			if (evt && typeof evt.preventDefault === 'function') {
				evt.preventDefault();
			}
			target.scrollIntoView({ behavior: 'smooth', block: 'start' });
			return false;
		}
		return true;
	};
	</script>
	<?php
}
if ( function_exists( 'add_action' ) ) {
	add_action( 'wp_head', 'kp_print_founder_avatar_video_head_assets', 30 );
}

/**
 * Build the complete HTML + VideoObject JSON-LD for a Founder Avatar Video Card.
 * Returns an empty string when the backing wp_option is unset/empty so zero broken
 * iframes or empty wrappers ever render prior to Unlisted YouTube ID binding.
 *
 * @param string $slot   Slot identifier ('feasibility', 'bill44', 'stepcode5').
 * @param bool   $dedupe Prevent duplicate rendering of the same slot in one request.
 * @return string
 */
function kp_get_founder_avatar_video_card_html( string $slot, bool $dedupe = true ): string {
	$canonical_slot = kp_normalize_founder_video_slot( $slot );
	if ( '' === $canonical_slot ) {
		return '';
	}

	$slots = kp_get_founder_avatar_video_slots();
	if ( ! isset( $slots[ $canonical_slot ] ) ) {
		return '';
	}

	$cfg    = $slots[ $canonical_slot ];
	$raw_id = trim( (string) get_option( (string) $cfg['option'], '' ) );
	if ( '' === $raw_id || 1 !== preg_match( '/^[A-Za-z0-9_-]{11}$/', $raw_id ) ) {
		return '';
	}
	$video_id = $raw_id;

	if ( ! isset( $GLOBALS['kp_rendered_founder_video_slots'] ) || ! is_array( $GLOBALS['kp_rendered_founder_video_slots'] ) ) {
		$GLOBALS['kp_rendered_founder_video_slots'] = array();
	}
	if ( $dedupe && ! empty( $GLOBALS['kp_rendered_founder_video_slots'][ $canonical_slot ] ) ) {
		return '';
	}
	$GLOBALS['kp_rendered_founder_video_slots'][ $canonical_slot ] = true;

	$iframe_id = 'kpFounderAvatarIframe-' . $canonical_slot;
	$card_id   = 'kpFounderAvatarCard-' . $canonical_slot;
	$chapters  = (array) $cfg['chapters'];
	$total_sec = (int) $cfg['total_sec'];

	$clips    = array();
	$ch_count = count( $chapters );
	for ( $i = 0; $i < $ch_count; $i++ ) {
		$ch        = $chapters[ $i ];
		$start_sec = (int) $ch['seconds'];
		$end_sec   = ( $i + 1 < $ch_count ) ? (int) $chapters[ $i + 1 ]['seconds'] : $total_sec;
		$clips[]   = array(
			'@type'       => 'Clip',
			'name'        => (string) $ch['title'],
			'startOffset' => $start_sec,
			'endOffset'   => $end_sec,
			'url'         => 'https://www.youtube.com/watch?v=' . $video_id . '&t=' . $start_sec . 's',
		);
	}

	$site_home = function_exists( 'home_url' ) ? home_url( '/' ) : 'https://keystonepossibilities.ca/';
	$schema    = array(
		'@context'     => 'https://schema.org',
		'@type'        => 'VideoObject',
		'@id'          => rtrim( $site_home, '/' ) . '/#founder-video-' . $canonical_slot,
		'name'         => (string) $cfg['title'],
		'description'  => (string) $cfg['description'],
		'thumbnailUrl' => array(
			'https://i.ytimg.com/vi/' . $video_id . '/maxresdefault.jpg',
			'https://i.ytimg.com/vi/' . $video_id . '/hqdefault.jpg',
		),
		'uploadDate'   => '2026-11-01T08:00:00-07:00',
		'duration'     => (string) $cfg['duration_iso'],
		'contentUrl'   => 'https://www.youtube.com/watch?v=' . $video_id,
		'embedUrl'     => 'https://www.youtube-nocookie.com/embed/' . $video_id,
		'publisher'    => array(
			'@type' => 'Organization',
			'name'  => 'Keystone Possibilities Ltd.',
			'url'   => $site_home,
		),
		'hasPart'      => $clips,
	);

	$json_ld = function_exists( 'wp_json_encode' )
		? (string) wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
		: (string) json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );

	ob_start();
	?>
	<section id="<?php echo esc_attr( $card_id ); ?>" class="kp-founder-video-card" data-founder-slot="<?php echo esc_attr( $canonical_slot ); ?>" aria-label="<?php echo esc_attr( (string) $cfg['title'] ); ?>" style="background: rgba(10, 15, 25, 0.92); border: 1.5px solid rgba(212, 175, 55, 0.45); border-radius: 18px; padding: 22px 24px; margin: 1.75rem auto 2.25rem auto; max-width: 1080px; width: 100%; box-sizing: border-box; overflow: hidden; box-shadow: 0 18px 46px rgba(0, 0, 0, 0.78); color: #f8fafc;">
		<div class="kp-founder-video-topbar" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
			<span class="kp-founder-video-badge" style="display: inline-flex; align-items: center; gap: 8px; background: #04070d; border: 1px solid rgba(212, 175, 55, 0.6); border-radius: 9999px; padding: 5px 14px; color: #d4af37; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.04em; text-transform: uppercase;"><?php echo esc_html( (string) $cfg['badge'] ); ?></span>
			<a href="#kp-feasibility-intake" class="kp-founder-video-cta-pill" onclick="return window.kpScrollToParcelReview ? window.kpScrollToParcelReview(event) : true;" style="display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: linear-gradient(135deg, #f3e5ab 0%, #d4af37 55%, #aa8010 100%); color: #04070d; border-radius: 9999px; padding: 8px 18px; font-weight: 800; font-size: 0.80rem; text-decoration: none; box-shadow: 0 6px 18px rgba(212, 175, 55, 0.34);">
				Request Parcel Feasibility Review &darr;
			</a>
		</div>
		<h2 class="kp-founder-video-heading" style="font-size: clamp(1.14rem, 2.05vw, 1.38rem); font-weight: 800; color: #ffffff; margin: 0 0 14px 0; line-height: 1.32;"><?php echo esc_html( (string) $cfg['title'] ); ?></h2>
		<div class="kp-founder-video-frame-wrap" style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; background: #04070d; border: 1.5px solid rgba(56, 189, 248, 0.38); border-radius: 14px; overflow: hidden; box-sizing: border-box;">
			<iframe id="<?php echo esc_attr( $iframe_id ); ?>"
					src="https://www.youtube-nocookie.com/embed/<?php echo esc_attr( $video_id ); ?>?rel=0&amp;modestbranding=1"
					title="<?php echo esc_attr( (string) $cfg['title'] ); ?>"
					style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; margin: 0;"
					allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
					allowfullscreen
					loading="eager"></iframe>
		</div>
		<div class="kp-founder-chapter-bar" role="navigation" aria-label="Video Chapters" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 14px; padding-top: 12px; border-top: 1px solid rgba(212, 175, 55, 0.25);">
			<?php foreach ( $chapters as $idx => $ch ) : ?>
				<button type="button"
						class="kp-founder-chapter-pill<?php echo 0 === $idx ? ' is-active' : ''; ?>"
						data-start="<?php echo esc_attr( (string) $ch['seconds'] ); ?>"
						style="display: inline-flex; align-items: center; gap: 6px; background: <?php echo 0 === $idx ? 'rgba(212, 175, 55, 0.16)' : '#04070d'; ?>; border: 1px solid <?php echo 0 === $idx ? '#d4af37' : 'rgba(56, 189, 248, 0.48)'; ?>; border-radius: 9999px; padding: 7px 14px; color: #f8fafc; font-size: 0.78rem; font-weight: 700; line-height: 1.2; cursor: pointer;"
						onclick="kpSeekFounderAvatarVideo('<?php echo esc_js( $iframe_id ); ?>', '<?php echo esc_js( $video_id ); ?>', <?php echo (int) $ch['seconds']; ?>, this)">
					<span class="kp-founder-chapter-ts" style="color: <?php echo 0 === $idx ? '#d4af37' : '#38bdf8'; ?>; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 800;"><?php echo esc_html( (string) $ch['time'] ); ?></span>
					<span><?php echo esc_html( (string) $ch['title'] ); ?></span>
				</button>
			<?php endforeach; ?>
		</div>
		<script type="application/ld+json"><?php echo $json_ld; ?></script>
	</section>
	<?php
	return (string) ob_get_clean();
}

/**
 * Echo the Founder Avatar Video Card for the specified canonical slot.
 *
 * @param string $slot Slot identifier ('feasibility', 'bill44', 'stepcode5').
 * @return void
 */
function kp_render_founder_avatar_video_card( string $slot ): void {
	echo kp_get_founder_avatar_video_card_html( $slot, true );
}

/**
 * Shortcode handler: [kp_founder_video slot="feasibility"]
 *
 * @param array<string, mixed>|string $atts Shortcode attributes.
 * @return string
 */
function kp_founder_avatar_video_shortcode( $atts ): string {
	$args = function_exists( 'shortcode_atts' )
		? shortcode_atts( array( 'slot' => 'feasibility' ), is_array( $atts ) ? $atts : array(), 'kp_founder_video' )
		: array( 'slot' => is_array( $atts ) && isset( $atts['slot'] ) ? (string) $atts['slot'] : 'feasibility' );

	return kp_get_founder_avatar_video_card_html( (string) $args['slot'], true );
}
if ( function_exists( 'add_shortcode' ) ) {
	add_shortcode( 'kp_founder_video', 'kp_founder_avatar_video_shortcode' );
}

/**
 * Automatic slug-based fallback injector on `the_content` (priority 25) so pages using
 * the default WordPress/Gutenberg template (rather than custom page-*.php files) still
 * render their canonical Founder Avatar Video Card directly below `</header>` or hero `</section>`
 * with zero duplication when a custom PHP template has already rendered the slot.
 *
 * @param string $content Post content HTML.
 * @return string
 */
function kp_auto_inject_founder_avatar_video_on_slug_pages( string $content ): string {
	if ( ( function_exists( 'is_admin' ) && is_admin() ) || ( function_exists( 'is_feed' ) && is_feed() ) ) {
		return $content;
	}
	if ( function_exists( 'is_page' ) && ! is_page() ) {
		return $content;
	}

	$slug = '';
	if ( isset( $GLOBALS['post'] ) && is_object( $GLOBALS['post'] ) && ! empty( $GLOBALS['post']->post_name ) ) {
		$slug = strtolower( (string) $GLOBALS['post']->post_name );
	} elseif ( ! empty( $_SERVER['REQUEST_URI'] ) ) {
		$slug = strtolower( trim( (string) parse_url( (string) $_SERVER['REQUEST_URI'], PHP_URL_PATH ), '/' ) );
	}

	$slug_to_slot = array(
		'feasibility-plan'                       => 'feasibility',
		'feasibility-retainer'                   => 'feasibility',
		'vancouver-multiplex-development'        => 'bill44',
		'vancouver-multiplex'                    => 'bill44',
		'north-vancouver-multiplex-conversions'  => 'bill44',
		'squamish-custom-homes'                  => 'stepcode5',
		'squamish-custom-home-builder'           => 'stepcode5',
		'squamish'                               => 'stepcode5',
		'step-code-5-engineering'                => 'stepcode5',
		'west-vancouver-custom-homes'            => 'stepcode5',
		'whistler-custom-homes'                  => 'stepcode5',
		'whistler-luxury-builder'                => 'stepcode5',
		'pemberton-luxury-builder'               => 'stepcode5',
		'sunshine-coast-custom-homes'            => 'stepcode5',
		'north-vancouver-custom-homes'           => 'stepcode5',
		'vancouver-island-custom-homes'          => 'stepcode5',
	);

	if ( '' === $slug || ! isset( $slug_to_slot[ $slug ] ) ) {
		return $content;
	}

	$card_html = kp_get_founder_avatar_video_card_html( $slug_to_slot[ $slug ], true );
	if ( '' === $card_html ) {
		return $content;
	}

	// Remove legacy placeholder video-facade blocks (e.g. broken #0085ff play-button with -50px overlap) when real 4K Founder Avatar card is active.
	$content = (string) preg_replace( '/<div[^>]*class=["\'][^"\']*luxury-video-facade[^"\']*["\'][^>]*>[\s\S]*?<\/button>\s*<\/div>/i', '', $content );
	$content = (string) preg_replace( '/margin:\s*-\d+px\s+auto/i', 'margin: 0 auto', $content );

	if ( false !== stripos( $content, '</header>' ) ) {
		return (string) preg_replace( '/<\/header>/i', '</header>' . "\n" . $card_html, $content, 1 );
	}
	if ( false !== stripos( $content, '</section>' ) ) {
		return (string) preg_replace( '/<\/section>/i', '</section>' . "\n" . $card_html, $content, 1 );
	}

	return $card_html . "\n" . $content;
}
if ( function_exists( 'add_filter' ) ) {
	add_filter( 'the_content', 'kp_auto_inject_founder_avatar_video_on_slug_pages', 25 );
}
