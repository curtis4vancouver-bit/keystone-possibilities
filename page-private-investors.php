<?php
/**
 * Template Name: Private Investors & JV
 *
 * British Columbia Bill 44 4–6 unit SSMUH multiplex & Coastal/Vancouver Island joint-venture
 * capital alignment desk: CCDC 5B open-book fiduciary governance, Builders Lien Act 10% holdback
 * trust, PQS draw audits, and cross-link to /bc-developer-portal/.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_jv_tiers = array(
	array(
		'tier'  => 'STRUCTURE 01 · SENIOR SECURED DEBT',
		'title' => '11.0% Fixed Preferred First-Mortgage Facility',
		'desc'  => 'Registered first-charge security on fee-simple British Columbia infill or coastal residential land, funded across verified Professional Quantity Surveyor (PQS) construction milestones.',
	),
	array(
		'tier'  => 'STRUCTURE 02 · HYBRID PREFERRED + EQUITY',
		'title' => '11.0% Preferred Return + 20% Net Project Equity',
		'desc'  => 'Designed for Bill 44 4–6 unit SSMUH and Vancouver R1-1 multiplex redevelopments—combining contractual preferred yield with strata exit participation.',
	),
	array(
		'tier'  => 'STRUCTURE 03 · LANDOWNER / GP-LP WATERFALL',
		'title' => '100% Capital Recovery -> 11.0% Cumulative -> 60/40 Profit Split',
		'desc'  => 'Institutional joint-venture waterfall for BC landowners contributing titled lots or accredited capital partners co-developing coastal estates and missing-middle multiplexes.',
	),
);

$kp_governance = array(
	array(
		'title' => 'Open-Book CCDC 5B Fiduciary Ledger',
		'desc'  => '24/7 digital access to signed sub-trade contracts, 3-bid tender comparisons, raw supplier invoices, and zero hidden GC sub-markup cascades.',
	),
	array(
		'title' => 'Statutory 10% Builders Lien Act Holdback Trust',
		'desc'  => 'Strict compliance with the BC Builders Lien Act—retaining 10% statutory holdback on every progress draw until verified substantial completion and lien-period expiry.',
	),
	array(
		'title' => 'Independent PQS & Schedule B Milestone Draws',
		'desc'  => 'Capital advances release strictly against P.Eng. Schedule B field reviews, municipal inspection passes, and Quantity Surveyor progress certifications.',
	),
	array(
		'title' => 'Self-Performed ES54 Civil & #52603 Execution',
		'desc'  => 'Controlled directly by Principal Superintendent Wayne Stevenson (#52603), removing utility energisation delays on multi-unit 400A–800A switchgear installations.',
	),
);
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(38px,5.5vw,74px) 0;background:radial-gradient(circle at 80% 14%,rgba(212,175,55,0.12),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">
				PRIVATE CAPITAL &amp; LANDOWNER JOINT VENTURES &bull; BRITISH COLUMBIA REAL ASSETS
			</div>
			<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.9rem,3.8vw,3.05rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;max-width:920px;">
				BC Bill 44 Multiplex &amp; Coastal Custom Estate Joint-Venture Partnerships.
			</h1>
			<p style="font-size:1rem;line-height:1.65;color:#cbd5e1;max-width:840px;margin:0 0 24px;">
				Keystone Possibilities Ltd. partners with British Columbia landowners, family offices, and accredited private investors to execute high-margin 4–6 unit Bill 44 SSMUH / Vancouver R1-1 multiplexes and signature Sea-to-Sky, North Shore, and Vancouver Island residences—governed by 100% Open-Book CCDC 5B accounting.
			</p>
			<div style="display:flex;flex-wrap:wrap;gap:12px;">
				<a href="#kp-lead-intake-form" style="display:inline-flex;align-items:center;padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
					Request Private JV Memorandum &rarr;
				</a>
				<a href="<?php echo esc_url( home_url( '/bc-developer-portal/' ) ); ?>" style="display:inline-flex;align-items:center;padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.44);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.85rem;text-decoration:none;">
					Open Institutional BC Developer Portal &rarr;
				</a>
			</div>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">
				CAPITAL ALIGNMENT FRAMEWORKS
			</div>
			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.55rem,2.9vw,2.25rem);font-weight:700;color:#f8fafc;margin:0 0 24px;">
				Three Structured Partnership Tiers Backed by Fee-Simple BC Title.
			</h2>

			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:20px;">
				<?php foreach ( $kp_jv_tiers as $jt ) : ?>
					<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.3);border-radius:18px;padding:24px;display:flex;flex-direction:column;gap:10px;">
						<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;color:#d4af37;"><?php echo esc_html( $jt['tier'] ); ?></span>
						<h3 style="font-family:'Outfit',sans-serif;font-size:1.15rem;font-weight:700;color:#f8fafc;margin:0;line-height:1.3;"><?php echo esc_html( $jt['title'] ); ?></h3>
						<p style="font-size:0.88rem;line-height:1.62;color:#cbd5e1;margin:0;"><?php echo esc_html( $jt['desc'] ); ?></p>
					</article>
				<?php endforeach; ?>
			</div>

			<div style="margin-top:40px;">
				<h3 style="font-family:'Outfit',sans-serif;font-size:1.4rem;font-weight:700;color:#f8fafc;margin:0 0 18px;">
					Fiduciary Draw &amp; Construction Risk Controls
				</h3>
				<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:18px;">
					<?php foreach ( $kp_governance as $gov ) : ?>
						<div style="background:#0a101d;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;">
							<div style="font-family:'Outfit',sans-serif;font-size:1.02rem;font-weight:700;color:#d4af37;margin-bottom:6px;"><?php echo esc_html( $gov['title'] ); ?></div>
							<p style="font-size:0.85rem;line-height:1.58;color:#cbd5e1;margin:0;"><?php echo esc_html( $gov['desc'] ); ?></p>
						</div>
					<?php endforeach; ?>
				</div>
			</div>
		</div>
	</section>

	<?php get_template_part( 'template-parts/bill44-calculator', null, array( 'default_corridor' => 'vancouver-r1-1' ) ); ?>

	<?php
	get_template_part(
		'template-parts/lead-intake-form',
		null,
		array(
			'default_corridor' => 'vancouver-r1-1',
			'default_audience' => 'Bill 44 Multiplex / JV Investor',
			'heading'          => 'Initiate a Confidential JV or Land-Contribution Review.',
			'subcopy'          => 'Connect directly with Principal Wayne Stevenson (#52603) regarding titled BC parcel joint ventures, Bill 44 multiplex underwriting, or senior construction capital alignment.',
		)
	);
	?>
</main>

<?php
get_footer();
