<?php
/**
 * Template Name: BC Hydro ES54 Civil
 *
 * Dedicated engineering hub for Keystone Possibilities Ltd.'s official BC Hydro Registered
 * Civil Contractor qualification: DB2 PVC duct banks (>=900mm/1050mm), 400A–800A switchgear,
 * PMT 3.0m hot-stick clearances (CEC Rule 26-242), 1,500–2,200 PSI hydro-vac daylighting,
 * official BC Hydro directory proof (WP ID 1668), and real John Deere 60G & rebar field photos.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_bchydro_proof_1668 = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/bc-hydro-civil-contractor-verified-proof.png';
$kp_bchydro_full_1665  = 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/bc-hydro-registered-civil-contractor-registry-proof.png';
$kp_deere_excavator    = 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/john-deere3.jpeg';
$kp_rebar_crush_photo  = 'https://keystonepossibilities.ca/wp-content/uploads/2023/12/whatsapp-image-2023-10-10-at-4.53.58-pm-1.jpeg';

$kp_es54_rules = array(
	array(
		'code'  => 'RULE 01 · ES54 TRENCH GEOMETRY',
		'title' => 'Primary & Secondary DB2 PVC Duct Depth (>=900mm / >=1050mm)',
		'desc'  => 'Minimum 900mm cover in non-vehicular boulevards and >=1050mm beneath driveways/roadways, bedded in screened thermal sand with red underground electrical warning tape and concrete encasement where crossings dictate.',
	),
	array(
		'code'  => 'RULE 02 · CEC RULE 26-242 CLEARANCE',
		'title' => 'Pad-Mounted Transformer (PMT) 3.0m Hot-Stick & Oil Containment',
		'desc'  => 'Pre-formed or cast-in-place BC Hydro vault/pad placement maintaining mandatory 3.0m unobstructed hot-stick operational front clearance, 1.0m side/rear clearances, and window/combustible wall offsets.',
	),
	array(
		'code'  => 'RULE 03 · 400A–800A SWITCHGEAR & EVEMS',
		'title' => 'Estate Microgrids & Bill 44 Multi-Meter Service Entrances',
		'desc'  => 'Coordinating 400A, 600A, and 800A single- or three-phase underground service entrances for heat-pump cascades, hydronic snow-melt, EVEMS charging banks, and 4–6 unit SSMUH multi-gang meter bases.',
	),
	array(
		'code'  => 'RULE 04 · NON-DESTRUCTIVE DAYLIGHTING',
		'title' => '1,500–2,200 PSI Hydro-Vac Daylighting Inside 1.0m Tolerance Zone',
		'desc'  => 'Strict BC 1 Call utility locates paired with controlled 1,500–2,200 PSI hydro-vac potholing whenever excavating within 1.0m of live energized primary cables, FortisBC gas mains, or municipal fibre.',
	),
	array(
		'code'  => 'RULE 05 · ENERGISATION QA GATE',
		'title' => 'Mandrel Proofing, Long-Radius Sweeps & Pull-String Sign-Off',
		'desc'  => 'Every conduit run is mandrel-tested for ovality/debris, fitted with approved long-radius fibreglass/bell-end sweeps, and strung with continuous rated pull rope prior to BC Hydro civil inspector sign-off.',
	),
);
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(36px,5.5vw,72px) 0;background:radial-gradient(circle at 80% 15%,rgba(56,189,248,0.09),transparent 42%),radial-gradient(circle at 15% 10%,rgba(212,175,55,0.11),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:1.1fr 0.9fr;gap:clamp(24px,4vw,44px);align-items:center;" class="kp-es54-hero-grid">
			<style>
				@media (max-width: 960px) { .kp-es54-hero-grid { grid-template-columns: 1fr !important; } }
			</style>
			<div>
				<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.07em;text-transform:uppercase;margin-bottom:10px;">
					OFFICIAL BC HYDRO REGISTERED CIVIL CONTRACTOR &bull; ES54 UNDERGROUND STANDARDS
				</div>
				<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.85rem,3.6vw,2.95rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;">
					Self-Performed BC Hydro ES54 Duct Banks, 400A–800A Services &amp; PMT Vaults.
				</h1>
				<p style="font-size:0.98rem;line-height:1.65;color:#cbd5e1;margin:0 0 20px;">
					Following BC Hydro’s mandatory Registered Civil Contractor qualification regime, uncertified general contractors cannot construct primary/secondary utility civil works on public/utility corridors. Keystone Possibilities Ltd. (Wayne Stevenson, 1 Watts Point Rd, Squamish) is officially listed on the BC Hydro Civil Contractor Directory—compressing months off your custom home or Bill 44 multiplex energisation critical path.
				</p>
				<div style="display:flex;flex-wrap:wrap;gap:12px;">
					<a href="#kp-lead-intake-form" style="display:inline-flex;align-items:center;padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
						Request ES54 Civil &amp; PMT Quote &rarr;
					</a>
					<a href="<?php echo esc_url( $kp_bchydro_full_1665 ); ?>" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.44);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.85rem;text-decoration:none;">
						View Full BC Hydro Registry Sheet &nearr;
					</a>
				</div>
			</div>

			<div style="background:#0a101d;border:1px solid rgba(212,175,55,0.42);border-radius:20px;padding:16px;box-shadow:0 26px 60px rgba(0,0,0,0.7);">
				<div style="background:#f6f2e9;border-radius:12px;padding:12px;">
					<img
						src="<?php echo esc_url( $kp_bchydro_proof_1668 ); ?>"
						alt="Official BC Hydro Registered Civil Contractor Directory Listing — Keystone Possibilities Ltd. / Wayne Stevenson (WP ID 1668)"
						style="width:100%;height:auto;display:block;border-radius:6px;"
						fetchpriority="high"
					/>
				</div>
				<div style="padding:12px 4px 2px;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#d4af37;font-weight:700;">VERIFIED REGISTRY RECORD · WP ID 1668</span>
					<span style="font-size:0.78rem;color:#cbd5e1;">1 Watts Point Rd, Squamish · (604) 848-9688</span>
				</div>
			</div>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">
				5 NON-NEGOTIABLE ES54 &amp; CEC ENGINEERING STANDARDS
			</div>
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.55rem,2.9vw,2.25rem);font-weight:700;color:#f8fafc;margin:0 0 24px;">
				Built Once to Pass First-Time BC Hydro &amp; Technical Safety BC Inspection.
			</h2>

			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:20px;">
				<?php foreach ( $kp_es54_rules as $rule ) : ?>
					<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.24);border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:10px;">
						<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;color:#38bdf8;"><?php echo esc_html( $rule['code'] ); ?></span>
						<h3 style="font-family:'Outfit',sans-serif;font-size:1.1rem;font-weight:700;color:#f8fafc;margin:0;line-height:1.32;"><?php echo esc_html( $rule['title'] ); ?></h3>
						<p style="font-size:0.86rem;line-height:1.6;color:#cbd5e1;margin:0;"><?php echo esc_html( $rule['desc'] ); ?></p>
					</article>
				<?php endforeach; ?>
			</div>

			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:22px;margin-top:34px;">
				<figure style="margin:0;background:#0a101d;border:1px solid rgba(212,175,55,0.3);border-radius:18px;overflow:hidden;">
					<img src="<?php echo esc_url( $kp_deere_excavator ); ?>" alt="Keystone Possibilities John Deere 60G Excavator on active BC civil trenching site" style="width:100%;aspect-ratio:16/10;object-fit:cover;display:block;" loading="lazy" />
					<figcaption style="padding:14px 18px;font-size:0.84rem;color:#cbd5e1;line-height:1.5;">
						<strong style="color:#f8fafc;display:block;margin-bottom:3px;">In-House John Deere 60G Civil Fleet</strong>
						Direct rock stripping, utility benching, and ES54 DB2 PVC duct trenching across Sea-to-Sky and North Shore parcels.
					</figcaption>
				</figure>
				<figure style="margin:0;background:#0a101d;border:1px solid rgba(212,175,55,0.3);border-radius:18px;overflow:hidden;">
					<img src="<?php echo esc_url( $kp_rebar_crush_photo ); ?>" alt="Compacted clear crush gravel base and welded wire rebar slab preparation" style="width:100%;aspect-ratio:16/10;object-fit:cover;display:block;" loading="lazy" />
					<figcaption style="padding:14px 18px;font-size:0.84rem;color:#cbd5e1;line-height:1.5;">
						<strong style="color:#f8fafc;display:block;margin-bottom:3px;">Compacted Clear-Crush &amp; Structural Rebar Preparation</strong>
						Integrated foundation drainage, sub-slab radon rock bed, and structural steel tie-ins supervised prior to Schedule B sign-off.
					</figcaption>
				</figure>
			</div>
		</div>
	</section>

	<?php
	get_template_part(
		'template-parts/watch-player',
		null,
		array(
			'video_id'  => 'HBy6NQQS3ks',
			'pill'      => '800A Microgrids & ES54 Vaults',
			'title'     => '800A Estate Microgrids & Private BC Hydro ES54 PMT Vault Clearances (CEC Rule 26-242)',
			'duration'  => '09:14',
			'watch_url' => home_url( '/videos/estate-microgrids-bc/' ),
		)
	);
	?>

	<?php
	get_template_part(
		'template-parts/lead-intake-form',
		null,
		array(
			'default_corridor' => 'squamish',
			'heading'          => 'Request a Direct BC Hydro ES54 Civil & PMT Engineering Quote.',
			'subcopy'          => 'Submit your BC Hydro design sketch, civic address, or 400A–800A service upgrade scope for direct review by Wayne Stevenson.',
		)
	);
	?>
</main>

<?php
get_footer();
