<?php
/**
 * Template Name: Industry Partners
 *
 * Verified BC Engineering, Architectural & Statutory Authority Directory:
 * BC Housing (#52603), Fast + Epp, Glotman Simpson, Thurber Engineering,
 * Lewkowich Engineering, Measured Architecture, VRBA, plus direct bridge to /realtor-architect-desk/.
 *
 * @package KeystonePossibilitiesChild
 * @version 3.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$kp_partners = array(
	array(
		'cat'   => 'STATUTORY LICENSING & WARRANTY AUTHORITY',
		'name'  => 'BC Housing — Licensing & Consumer Services (#52603)',
		'scope' => 'Statutory oversight for Licensed Residential Builder #52603, mandatory 2-5-10 Year New Home Warranty enrollment, and accredited Continuing Professional Development (CPD) compliance.',
	),
	array(
		'cat'   => 'STRUCTURAL ENGINEERING (MASS TIMBER, STEEL & SEISMIC)',
		'name'  => 'Fast + Epp Structural Engineers',
		'scope' => 'Complex cantilevered steel, architecturally exposed heavy timber, alpine snow-load framing (Sg = 6.2–8.1 kPa), and Part 4 ductile lateral shear assemblies.',
	),
	array(
		'cat'   => 'STRUCTURAL ENGINEERING (CONCRETE & HILLSIDE)',
		'name'  => 'Glotman Simpson Consulting Engineers',
		'scope' => 'Multi-tiered board-formed architectural concrete, deep seismic hold-downs, post-tensioned slabs, and multi-storey coastal residential structural Schedules B & C-B.',
	),
	array(
		'cat'   => 'GEOTECHNICAL, ROCK ANCHOR & SHORING ENGINEERING',
		'name'  => 'Thurber Engineering Ltd.',
		'scope' => 'Subgrade borehole profiling, granodiorite bedrock bearing verification, micropiles, post-tensioned rock anchors, slope stability covenants, and shotcrete shoring.',
	),
	array(
		'cat'   => 'VANCOUVER ISLAND & COASTAL GEOTECHNICAL',
		'name'  => 'Lewkowich Engineering Associates Ltd.',
		'scope' => 'Coastal bluff geotechnical hazard assessments, engineered structural fill compaction, perimeter drainage hydrology, and Vancouver Island seismic soil profiling.',
	),
	array(
		'cat'   => 'ARCHITECTURAL DESIGN & WEST COAST MODERNISM',
		'name'  => 'Measured Architecture Inc. & AIBC Studios',
		'scope' => 'Early-stage CCDC 5B pre-construction constructability, thermal-bridge mitigation, architectural concrete mockup standards, and value-engineering collaboration.',
	),
	array(
		'cat'   => 'REGIONAL INDUSTRY GOVERNANCE',
		'name'  => 'Victoria Residential Builders Association (VRBA) & CHBA BC',
		'scope' => 'Advancing residential building science, BC Energy Step Code 4/5 & Zero Carbon EL-4 execution, and ethical open-book contracting across coastal British Columbia.',
	),
);
?>

<main id="primary" class="kp-v3-page">
	<section style="padding:clamp(38px,5.5vw,72px) 0;background:radial-gradient(circle at 80% 15%,rgba(212,175,55,0.12),transparent 45%),#04070d;border-bottom:1px solid rgba(212,175,55,0.16);">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;">
			<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:700;color:#d4af37;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">
				LETTERS OF ASSURANCE (SCHEDULES A, B, C-A, C-B) &bull; COLLABORATIVE ROSTER
			</div>
			<h1 style="font-family:'Outfit',sans-serif;font-size:clamp(1.9rem,3.7vw,3rem);font-weight:800;line-height:1.11;color:#f8fafc;margin:0 0 14px;max-width:920px;">
				Verified BC Engineering, Architectural &amp; Regulatory Disciplines.
			</h1>
			<p style="font-size:1rem;line-height:1.65;color:#cbd5e1;max-width:840px;margin:0 0 22px;">
				Slope-critical estates and Bill 44 multiplexes demand seamless coordination between the Coordinating Registered Professional (CRP), geotechnical/structural P.Eng. authorities, and on-site superintendence. Below are the statutory bodies, engineering practices, and industry benchmarks our workflows align with across British Columbia.
			</p>
			<a href="<?php echo esc_url( home_url( '/realtor-architect-desk/' ) ); ?>" style="display:inline-flex;align-items:center;padding:12px 22px;border-radius:999px;background:linear-gradient(135deg,#f3e5ab,#d4af37 52%,#b89028);color:#04070d;font-family:'Outfit',sans-serif;font-weight:800;font-size:0.88rem;text-decoration:none;">
				Open Dedicated Realtor&reg; &amp; AIBC Architect Partner Desk &rarr;
			</a>
		</div>
	</section>

	<section style="padding:clamp(48px,6vw,84px) 0;background:#04070d;">
		<div style="width:min(1340px,calc(100% - 32px));margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:20px;">
			<?php foreach ( $kp_partners as $pt ) : ?>
				<article style="background:#0a101d;border:1px solid rgba(212,175,55,0.26);border-radius:18px;padding:24px;display:flex;flex-direction:column;gap:10px;">
					<span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;font-weight:700;color:#d4af37;"><?php echo esc_html( $pt['cat'] ); ?></span>
					<h2 style="font-family:'Outfit',sans-serif;font-size:1.15rem;font-weight:700;color:#f8fafc;margin:0;line-height:1.3;"><?php echo esc_html( $pt['name'] ); ?></h2>
					<p style="font-size:0.87rem;line-height:1.6;color:#cbd5e1;margin:0;"><?php echo esc_html( $pt['scope'] ); ?></p>
				</article>
			<?php endforeach; ?>
		</div>
	</section>

	<?php get_template_part( 'template-parts/realtor-rule511-card' ); ?>

	<?php
	get_template_part(
		'template-parts/lead-intake-form',
		null,
		array(
			'default_audience' => 'AIBC Architect / EGBC Engineer',
			'default_corridor' => 'west-vancouver',
		)
	);
	?>
</main>

<?php
get_footer();
