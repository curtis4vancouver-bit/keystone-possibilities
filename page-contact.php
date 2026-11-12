<?php
/**
 * Template Name: Direct Contact Desk
 *
 * 2-column Principal dispatch: (604) 848-9688, 1 Watts Point Road, Squamish, BC V8B 0B1,
 * Sea-to-Sky & Greater Vancouver service-corridor map card, and WCAG lead-intake-form.php.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_badge_logo = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(36px,5.5vw,74px) 0;background:radial-gradient(circle at 80% 12%,rgba(212,175,55,0.12),transparent 46%),#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:0.92fr 1.08fr;gap:clamp(24px,4vw,44px);align-items:start;" class="kp-contact-grid">
			<style>
				@media (max-width: 960px) { .kp-contact-grid { grid-template-columns: 1fr !important; } }
			</style>

			<div style="display:flex;flex-direction:column;gap:18px;">
				<div style="display:inline-flex;align-items:center;gap:10px;align-self:flex-start;background:#0a101d;border:1px solid rgba(212,175,55,0.36);border-radius:999px;padding:6px 14px 6px 8px;">
					<img src="<?php echo esc_url( $kp_badge_logo ); ?>" alt="Keystone Possibilities Shield" width="26" height="26" style="border-radius:6px;object-fit:contain;" />
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:700;color:#d4af37;">DIRECT PRINCIPAL DISPATCH · SQUAMISH HQ</span>
				</div>

				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.85rem);font-weight:800;line-height:1.12;color:#f8fafc;margin:0;">
					Speak Directly With Superintendent Wayne Stevenson.
				</h1>

				<p style="font-size:0.96rem;line-height:1.64;color:#cbd5e1;margin:0;">
					Every custom estate, Bill 44 multiplex, and BC Hydro ES54 civil inquiry is reviewed personally by Wayne Stevenson—never routed through call centres or junior estimators.
				</p>

				<div style="background:#0a101d;border:1px solid rgba(212,175,55,0.34);border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:12px;">
					<div>
						<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#94a3b8;text-transform:uppercase;">Direct Principal Line</div>
						<a href="tel:+16048489688" style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:800;color:#d4af37;text-decoration:none;">(604) 848-9688</a>
					</div>
					<div>
						<div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#94a3b8;text-transform:uppercase;">Operations Headquarters</div>
						<div style="font-size:0.95rem;font-weight:700;color:#f8fafc;">1 Watts Point Road, Squamish, BC V8B 0B1</div>
					</div>
					<div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:10px;font-size:0.82rem;color:#cbd5e1;line-height:1.55;">
						<strong>Statutory Standing:</strong> BC Housing Licensed Builder #52603 &bull; BC Hydro ES54 Registered Civil Contractor &bull; WorkSafeBC #201703481 &bull; Mandatory 2-5-10 Warranty
					</div>
				</div>

				<div style="background:#0a101d;border:1px solid rgba(212,175,55,0.28);border-radius:18px;overflow:hidden;">
					<iframe
						title="Keystone Possibilities Ltd. — 1 Watts Point Road, Squamish, BC Service Corridor Map"
						src="https://www.google.com/maps?q=1+Watts+Point+Road,+Squamish,+BC+V8B+0B1&output=embed"
						width="100%"
						height="250"
						style="border:0;display:block;filter:invert(90%) hue-rotate(180deg) contrast(92%);"
						loading="lazy"
						referrerpolicy="no-referrer-when-downgrade"
					></iframe>
					<div style="padding:12px 16px;font-size:0.78rem;color:#cbd5e1;">
						Active Build Corridors: West Vancouver &bull; Whistler &bull; Squamish HQ &bull; North Vancouver &bull; Vancouver R1-1 &bull; Coquitlam &bull; Sunshine Coast &bull; Pemberton &bull; Vancouver Island
					</div>
				</div>
			</div>

			<div>
				<?php
				get_template_part(
					'template-parts/lead-intake-form',
					null,
					array(
						'embed_only'       => true,
						'default_corridor' => 'squamish',
					)
				);
				?>
			</div>
		</div>
	</section>
</main>

<?php
get_footer();
