<?php
/**
 * Template Name: BC Developer Portal
 * Template Post Type: page
 *
 * Institutional Landowner, Family-Office & Land-Assembly Desk in v3.0 Quiet-Luxury tokens:
 * Bill 44 4–6 unit SSMUH & Vancouver R1-1 multiplex underwriting, 4+ unit multi-residential
 * development rules, 9-corridor $/SF benchmark matrix, 5-stage portal reporting, and JV intake.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_dev_matrix = array(
	array( 'corridor' => 'West Vancouver',          'estate' => '$690–$980 / SF',  'multi' => '$510–$675 / SF', 'driver' => 'Granite micropiles, Bylaw 4364 creek setback & Step Code 5' ),
	array( 'corridor' => 'Whistler Alpine',         'estate' => '$720–$1,050 / SF','multi' => '$545–$710 / SF', 'driver' => 'Part 4 snow load Sg = 6.2–8.1 kPa & RMOW Class A FireSmart' ),
	array( 'corridor' => 'Squamish HQ',             'estate' => '$540–$760 / SF',  'multi' => '$425–$560 / SF', 'driver' => 'FCL structural fill, 3.4 kPa snow load & local HQ supervision' ),
	array( 'corridor' => 'North Vancouver',         'estate' => '$595–$840 / SF',  'multi' => '$455–$595 / SF', 'driver' => 'Glacial-till shoring, SPEA ravine buffers & 9.27 rainscreen' ),
	array( 'corridor' => 'Vancouver R1-1',          'estate' => '$640–$920 / SF',  'multi' => '$465–$615 / SF', 'driver' => '1.0 FSR up to 6–8 units, 2" water main, NFPA 13R & ES54 PMT' ),
	array( 'corridor' => 'Coquitlam (SSMUH / TOA)', 'estate' => '$530–$735 / SF',  'multi' => '$420–$545 / SF', 'driver' => 'Burke Mountain slope benching & storm detention chambers' ),
	array( 'corridor' => 'Sunshine Coast',          'estate' => '$560–$795 / SF',  'multi' => '$440–$575 / SF', 'driver' => 'q100 = 0.55 kPa wind uplift, granite footings & staged freight' ),
	array( 'corridor' => 'Pemberton Compounds',     'estate' => '$575–$825 / SF',  'multi' => '$450–$590 / SF', 'driver' => 'Long-run ES54 primary duct banks & 800A microgrid vaults' ),
	array( 'corridor' => 'Vancouver Island',        'estate' => '$565–$815 / SF',  'multi' => '$435–$575 / SF', 'driver' => 'High-seismic PGA > 0.58g ductile shear walls & coastal basalt' ),
);
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(38px,5.5vw,74px) 0;background:radial-gradient(circle at 80% 14%,rgba(212,175,55,0.12),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">
				INSTITUTIONAL LANDOWNER, FAMILY-OFFICE &amp; ASSEMBLY DESK &bull; BC #52603
			</div>
			<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.9rem,3.8vw,3.05rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;max-width:940px;">
				BC Multiplex Redevelopment, Landowner Assemblies &amp; Fiduciary Build Execution.
			</h1>
			<p style="font-size:1rem;line-height:1.65;color:#cbd5e1;max-width:860px;margin:0 0 24px;">
				Engineered for domestic and international family offices, titled BC landowners, and multi-unit infill developers executing 4–6 unit Bill 44 SSMUH redevelopments, Vancouver R1-1 multiplexes, and coastal estates under 100% Open-Book CCDC 5B governance.
			</p>
			<div style="display:flex;flex-wrap:wrap;gap:12px;">
				<a href="#kp-lead-intake-form" style="display:inline-flex;align-items:center;padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
					Submit Assembly or Parcel for Underwriting &rarr;
				</a>
				<a href="<?php echo esc_url( home_url( '/client-login/' ) ); ?>" style="display:inline-flex;align-items:center;padding:12px 20px;border-radius:999px;border:1px solid rgba(212,175,55,0.44);color:#f8fafc;font-family:'Outfit',sans-serif;font-weight:700;font-size:0.85rem;text-decoration:none;">
					Inspect Live CCDC 5B Client Portal &rarr;
				</a>
			</div>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:20px;margin-bottom:38px;">
				<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.28);border-radius:18px;padding:24px;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#d4af37;font-weight:700;">PILLAR 01 · BILL 44 &amp; R1-1 UPZONING</span>
					<h2 style="font-family:'Outfit',sans-serif;font-size:1.18rem;color:#f8fafc;margin:8px 0;">4–6 Unit Multi-Residential Redevelopment</h2>
					<p style="font-size:0.87rem;line-height:1.6;color:#cbd5e1;margin:0;">
						Transforming single-detached parcels into 4-to-6 strata dwelling units under provincial SSMUH legislation and municipal schedules, unlocking ground-up multi-unit residential development pathways across Metro Vancouver, Sea-to-Sky, and Vancouver Island.
					</p>
				</article>
				<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.28);border-radius:18px;padding:24px;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#d4af37;font-weight:700;">PILLAR 02 · AUDIT-READY FIDUCIARY LEDGER</span>
					<h2 style="font-family:'Outfit',sans-serif;font-size:1.18rem;color:#f8fafc;margin:8px 0;">LOTA, PTT &amp; Construction Lender Governance</h2>
					<p style="font-size:0.87rem;line-height:1.6;color:#cbd5e1;margin:0;">
						Clean division-by-division CCDC 5B accounting formatted for Canadian construction lenders, Quantity Surveyors (PQS), CPA tax counsel, and statutory 10% BC Builders Lien Act holdback trust verification.
					</p>
				</article>
				<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.28);border-radius:18px;padding:24px;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#d4af37;font-weight:700;">PILLAR 03 · 5-STAGE REMOTE COMMAND</span>
					<h2 style="font-family:'Outfit',sans-serif;font-size:1.18rem;color:#f8fafc;margin:8px 0;">24/7 Digital Milestone &amp; Schedule B Vault</h2>
					<p style="font-size:0.87rem;line-height:1.6;color:#cbd5e1;margin:0;">
						Monitor Rock/Shoring, ES54 Civil &amp; Slab, Structural Framing &amp; ATS Shear, Step Code Envelope Lockup, and Occupancy Commissioning remotely with dated P.Eng. inspection PDFs and signed trade contracts.
					</p>
				</article>
			</div>

			<h2 style="font-family:'Outfit',sans-serif;font-size:clamp(1.45rem,2.6vw,2.05rem);font-weight:700;color:#f8fafc;margin:0 0 16px;">
				2026 9-Corridor Open-Book Hard-Cost Benchmark Matrix
			</h2>
			<div style="overflow-x:auto;background:#0a101d;border:1px solid rgba(212,175,55,0.3);border-radius:18px;">
				<table style="width:100%;border-collapse:collapse;min-width:680px;font-size:0.86rem;">
					<thead>
						<tr style="background:#060a14;border-bottom:1px solid rgba(212,175,55,0.32);text-align:left;">
							<th style="padding:14px 18px;color:#d4af37;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">BC CORRIDOR</th>
							<th style="padding:14px 18px;color:#d4af37;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">CUSTOM ESTATE ($/SF)</th>
							<th style="padding:14px 18px;color:#d4af37;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">4–6 UNIT MULTIPLEX ($/SF)</th>
							<th style="padding:14px 18px;color:#d4af37;font-family:'JetBrains Mono',monospace;font-size:0.72rem;">PRIMARY STRUCTURAL &amp; CIVIL DRIVER</th>
						</tr>
					</thead>
					<tbody>
						<?php foreach ( $kp_dev_matrix as $row ) : ?>
							<tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
								<td style="padding:13px 18px;font-weight:700;color:#f8fafc;"><?php echo esc_html( $row['corridor'] ); ?></td>
								<td style="padding:13px 18px;font-family:'JetBrains Mono',monospace;color:#e2e8f0;"><?php echo esc_html( $row['estate'] ); ?></td>
								<td style="padding:13px 18px;font-family:'JetBrains Mono',monospace;color:#d4af37;font-weight:700;"><?php echo esc_html( $row['multi'] ); ?></td>
								<td style="padding:13px 18px;color:#cbd5e1;"><?php echo esc_html( $row['driver'] ); ?></td>
							</tr>
						<?php endforeach; ?>
					</tbody>
				</table>
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
			'heading'          => 'Request an Institutional Parcel Assembly or Multiplex Pro-Forma.',
		)
	);
	?>
</main>

<?php
get_footer();
