<?php
/**
 * 410 Gone Template (410.php) — Retired Legacy Resource Notice
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! headers_sent() ) {
	status_header( 410 );
	nocache_headers();
}

get_header();
?>

<main id="primary" style="background:#04070d;color:#f8fafc;min-height:74vh;display:flex;align-items:center;padding:64px 0;">
	<div style="width:min(860px,calc(100% - 32px));margin:0 auto;background:#0a101d;border:1px solid rgba(212,175,55,0.36);border-radius:22px;padding:clamp(26px,5vw,48px);text-align:center;">
		<div style="font-family:'JetBrains Mono',monospace;font-size:0.74rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;margin-bottom:10px;">
			HTTP 410 &bull; ARCHIVED LEGACY URL PERMANENTLY RETIRED
		</div>
		<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.8rem,3.4vw,2.6rem);font-weight:800;color:#f8fafc;margin:0 0 12px;line-height:1.15;">
			This Legacy Document Has Been Permanently Retired.
		</h1>
		<p style="font-size:0.96rem;line-height:1.65;color:#cbd5e1;max-width:640px;margin:0 auto 28px;">
			Keystone Possibilities Ltd. (BC Housing Licensed Builder #52603 &amp; BC Hydro ES54 Registered Civil Contractor) focuses exclusively on British Columbia slope-critical custom estates, Bill 44 4–6 unit multiplexes, and underground civil infrastructure.
		</p>
		<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:12px;">
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>" style="padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
				Explore Active BC Custom Estates &amp; Multiplexes &rarr;
			</a>
			<a href="<?php echo esc_url( home_url( '/realtor-architect-desk/' ) ); ?>" style="padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.42);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.86rem;text-decoration:none;">
				Realtor&reg; &amp; Architect Partner Desk
			</a>
		</div>
	</div>
</main>

<?php
get_footer();
