<?php
/**
 * Template Name: About Wayne & Credentials
 *
 * First-person Principal biography of Wayne Stevenson (20+ years Peter Kiewit & Sons heavy-civil
 * superintendence, CLAC Local 68, Doka/Peri formwork, BC Housing #52603, BC Hydro ES54, 2-5-10 Warranty)
 * + full 17-Certificate Museum Vault in grid mode with visually verified ground-truth captions.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_wayne_whistler = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/wayne_whistler_builder_avatar.jpg';
$kp_emblem_gold    = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_emblem_gold_transparent.png';

$kp_pillars = array(
	array(
		'code'  => '01 · HEAVY-CIVIL PEDIGREE',
		'title' => '20+ Years Peter Kiewit & Sons & CLAC Local 68 Superintendence',
		'desc'  => 'Trained on uncompromising civil infrastructure where rock anchors, Doka/Peri structural concrete formwork, hydro-vac utility corridors, and engineered shoring are executed to millimetre tolerances.',
	),
	array(
		'code'  => '02 · DIRECT SITE COMMAND',
		'title' => 'Principal On-Site—Never Handed Off to Junior Brokers',
		'desc'  => 'When you retain Keystone Possibilities Ltd., I personally chair pre-pour Schedule B rebar walks, mid-construction Step Code blower-door tests, and municipal inspections.',
	),
	array(
		'code'  => '03 · DUAL STATUTORY AUTHORITY',
		'title' => 'BC Housing Builder #52603 + BC Hydro ES54 Civil Registry',
		'desc'  => 'Combining licensed 2-5-10 Residential Builder authority with registered BC Hydro ES54 underground civil qualification eliminates the utility trenching bottleneck on 400A–800A estates and multiplexes.',
	),
	array(
		'code'  => '04 · FIDUCIARY TRANSPARENCY',
		'title' => '100% Open-Book CCDC 5B Ledger & 10% Lien Holdback Trust',
		'desc'  => 'Every sub-trade contract, 3-bid tender sheet, Dick’s Lumber #52603 takeoff, and Builders Lien Act 10% statutory holdback draw is open to the property owner 24/7 inside our Client Portal.',
	),
);
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(36px,5.5vw,72px) 0;background:radial-gradient(circle at 82% 16%,rgba(212,175,55,0.12),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:1.14fr 0.86fr;gap:clamp(24px,4vw,48px);align-items:center;" class="kp-about-hero-grid">
			<style>
				@media (max-width: 960px) { .kp-about-hero-grid { grid-template-columns: 1fr !important; } }
			</style>
			<div>
				<div style="display:inline-flex;align-items:center;gap:10px;background:#0a101d;border:1px solid rgba(212,175,55,0.36);border-radius:999px;padding:6px 14px;margin-bottom:14px;">
					<img src="<?php echo esc_url( $kp_emblem_gold ); ?>" alt="Keystone Possibilities Emblem" width="22" height="22" style="object-fit:contain;" />
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:700;color:#d4af37;letter-spacing:0.06em;">WAYNE STEVENSON · PRINCIPAL &amp; LICENSED BUILDER #52603</span>
				</div>

				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.9rem,3.7vw,3.05rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 16px;">
					Heavy-Civil Discipline Applied to Coastal Custom Estates &amp; Bill 44 Multiplexes.
				</h1>

				<div style="font-size:0.98rem;line-height:1.68;color:#e2e8f0;display:flex;flex-direction:column;gap:14px;">
					<p style="margin:0;">
						&ldquo;I founded Keystone Possibilities Ltd. in Squamish because BC’s steepest granite bluffs, highest alpine snow zones, and complex multi-unit infill lots punish residential ‘paper brokers’ who have never run heavy civil iron or structural formwork.&rdquo;
					</p>
					<p style="margin:0;color:#cbd5e1;">
						&ldquo;Before leading architectural custom builds under <strong>BC Housing Licence #52603</strong>, I spent <strong>20+ years on major infrastructure civil works including Peter Kiewit &amp; Sons</strong> and <strong>CLAC Local 68</strong>—directing rock excavation, Doka and Peri high-load concrete formwork, deep underground utilities, and zero-incident WorkSafeBC critical paths. Today, my team brings that exact engineering rigour, <strong>BC Hydro ES54 Registered Civil</strong> execution, mandatory <strong>2-5-10 Year New Home Warranty</strong> protection, and <strong>100% Open-Book CCDC 5B</strong> accounting directly to your property.&rdquo;
					</p>
					<div style="font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:700;color:#d4af37;">
						&mdash; Wayne Stevenson, Principal Superintendent · 1 Watts Point Rd, Squamish, BC
					</div>
				</div>
			</div>

			<div style="background:#0a101d;border:1px solid rgba(212,175,55,0.38);border-radius:22px;overflow:hidden;box-shadow:0 28px 64px rgba(0,0,0,0.7);">
				<img
					src="<?php echo esc_url( $kp_wayne_whistler ); ?>"
					alt="Wayne Stevenson — Principal & Heavy-Civil Superintendent holding structural blueprints"
					style="width:100%;aspect-ratio:4/4.2;object-fit:cover;object-position:center top;display:block;"
					fetchpriority="high"
				/>
				<div style="padding:16px 20px;border-top:1px solid rgba(212,175,55,0.24);display:grid;grid-template-columns:repeat(3,1fr);gap:10px;text-align:center;">
					<div>
						<div style="font-family:'Outfit',sans-serif;font-size:1.25rem;font-weight:800;color:#d4af37;">#52603</div>
						<div style="font-size:0.7rem;color:#cbd5e1;">BC Housing Licence</div>
					</div>
					<div>
						<div style="font-family:'Outfit',sans-serif;font-size:1.25rem;font-weight:800;color:#f8fafc;">ES54</div>
						<div style="font-size:0.7rem;color:#cbd5e1;">BC Hydro Civil Reg.</div>
					</div>
					<div>
						<div style="font-family:'Outfit',sans-serif;font-size:1.25rem;font-weight:800;color:#d4af37;">17</div>
						<div style="font-size:0.7rem;color:#cbd5e1;">Verified Certificates</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">
				THE KEYSTONE SUPERINTENDENT STANDARD
			</div>
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.55rem,2.9vw,2.25rem);font-weight:700;color:#f8fafc;margin:0 0 24px;">
				Four Non-Negotiable Governance Pillars on Every Build.
			</h2>
			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr));gap:20px;">
				<?php foreach ( $kp_pillars as $pil ) : ?>
					<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.25);border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:10px;">
						<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;font-weight:700;color:#d4af37;"><?php echo esc_html( $pil['code'] ); ?></span>
						<h3 style="font-family:'Outfit',sans-serif;font-size:1.12rem;font-weight:700;color:#f8fafc;margin:0;line-height:1.3;"><?php echo esc_html( $pil['title'] ); ?></h3>
						<p style="font-size:0.87rem;line-height:1.6;color:#cbd5e1;margin:0;"><?php echo esc_html( $pil['desc'] ); ?></p>
					</article>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<?php
	get_template_part(
		'template-parts/credential-vault',
		null,
		array(
			'mode'       => 'grid',
			'section_id' => 'credential-museum',
			'kicker'     => 'FULL 17-DOCUMENT STATUTORY & BUILDING CODE ARCHIVE',
			'heading'    => 'Inspect Every Original Licence, Registry Proof & Course Certificate.',
		)
	);
	?>

	<?php get_template_part( 'template-parts/portfolio-reel', null, array( 'mode' => 'reel' ) ); ?>
	<?php get_template_part( 'template-parts/lead-intake-form', null, array( 'default_corridor' => 'squamish' ) ); ?>
</main>

<?php
get_footer();
