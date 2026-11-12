<?php
/**
 * 404 Not Found Template (404.php) — Quiet-Luxury Navigation Command
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>

<main id="primary" style="background:#04070d;color:#f8fafc;min-height:74vh;display:flex;align-items:center;padding:64px 0;">
	<div style="width:min(860px,calc(100% - 32px));margin:0 auto;background:#0a101d;border:1px solid rgba(212,175,55,0.36);border-radius:22px;padding:clamp(26px,5vw,48px);text-align:center;">
		<div style="font-family:'JetBrains Mono',monospace;font-size:0.74rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;margin-bottom:10px;">
			HTTP 404 &bull; BLUEPRINT COORDINATE NOT FOUND
		</div>
		<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.75rem);font-weight:800;color:#f8fafc;margin:0 0 12px;line-height:1.14;">
			This Parcel or Page Has Moved Within Our v3.0 Engineering Hub.
		</h1>
		<p style="font-size:0.98rem;line-height:1.65;color:#cbd5e1;max-width:640px;margin:0 auto 28px;">
			Select an active engineering desk below or speak directly with Principal Superintendent Wayne Stevenson (#52603) at <a href="tel:+16048489688" style="color:#d4af37;font-weight:700;text-decoration:none;">(604) 848-9688</a>.
		</p>
		<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:12px;">
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>" style="padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
				Return to Flagship Home &rarr;
			</a>
			<a href="<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>" style="padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.42);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.86rem;text-decoration:none;">
				48-Hr Feasibility &amp; Cost Plan
			</a>
			<a href="<?php echo esc_url( home_url( '/portfolio-general-contractor-squamish/' ) ); ?>" style="padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.42);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.86rem;text-decoration:none;">
				9 Built Residences
			</a>
			<a href="<?php echo esc_url( home_url( '/videos/' ) ); ?>" style="padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.42);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.86rem;text-decoration:none;">
				4K Watch Briefings
			</a>
		</div>
	</div>
</main>

<?php
get_footer();
