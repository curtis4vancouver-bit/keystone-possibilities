<?php
/**
 * Template Name: AI Construction Engineering Case Study
 * Template Post Type: page
 *
 * Description: Editorial case study detailing multi-agent AI systems, FastMCP swarms, and autonomous engineering in residential construction.
 * Contains editorial link to https://keystonerecomposition.com/ai-protocols/.
 *
 * @package KeystonePossibilitiesChild
 * @version 2.8.0
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

get_header();
$theme_uri = get_stylesheet_directory_uri();
?>

<div id="primary" class="content-area primary keystone-case-study-page" style="background-color: #04070d; color: #f8fafc; min-height: 100vh;">
    <main id="main" class="site-main">

        <!-- Top Credentials Ribbon -->
        <div style="background: rgba(10, 15, 25, 0.95); border-bottom: 1px solid rgba(212, 175, 55, 0.3); padding: 12px 20px; text-align: center; font-size: 0.80rem; font-family: 'Outfit', sans-serif; letter-spacing: 0.08em; text-transform: uppercase;">
            <span style="color: #d4af37; font-weight: 700;">PROPTEL &amp; AI CASE STUDY</span> 
            <span style="color: rgba(255, 255, 255, 0.3); margin: 0 8px;">|</span>
            <span style="color: #38bdf8;">BC HOUSING BUILDER #52603 &bull; FASTMCP AUTONOMOUS AGENT FLEET</span>
        </div>

        <!-- Hero Section -->
        <section style="max-width: 1100px; margin: 0 auto; padding: 60px 24px 40px; text-align: center;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid #38bdf8; padding: 6px 18px; border-radius: 9999px; margin-bottom: 24px; font-size: 0.82rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
                <span>⚡ TECHNICAL BRIEFING // 2026 FIELD DEPLOYMENT</span>
            </div>

            <h1 style="font-family: 'Outfit', sans-serif; font-size: clamp(2.2rem, 5vw, 3.5rem); font-weight: 900; line-height: 1.15; color: #ffffff; margin-bottom: 24px; letter-spacing: -0.02em;">
                Multi-Agent AI in Residential Construction &amp;<br>
                <span style="background: linear-gradient(135deg, #d4af37 0%, #f6d365 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Autonomous Civil Engineering</span>
            </h1>

            <p style="font-size: 1.15rem; line-height: 1.7; color: #94a3b8; max-width: 860px; margin: 0 auto 36px;">
                How Keystone Possibilities deploys 28 FastMCP autonomous software agents to eliminate schedule drift, automate CCDC 5B open-book trade audits, and streamline structural engineering across complex West Vancouver, Whistler, and Sea-to-Sky custom home sites.
            </p>

            <div style="display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;">
                <a href="#case-study-content" style="background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; font-weight: 800; font-family: 'Outfit', sans-serif; padding: 14px 32px; border-radius: 9999px; text-decoration: none; font-size: 0.90rem; text-transform: uppercase; letter-spacing: 0.04em; box-shadow: 0 4px 20px rgba(212, 175, 55, 0.35);">
                    Read Field Case Study &darr;
                </a>
                <a href="https://keystonerecomposition.com/ai-protocols/" target="_blank" rel="noopener noreferrer" style="background: rgba(56, 189, 248, 0.1); border: 1.5px solid #38bdf8; color: #38bdf8; font-weight: 700; font-family: 'Outfit', sans-serif; padding: 14px 28px; border-radius: 9999px; text-decoration: none; font-size: 0.90rem; text-transform: uppercase; letter-spacing: 0.04em; transition: all 0.25s ease;">
                    Explore Keystone AI Protocols &rarr;
                </a>
            </div>
        </section>

        <!-- KPI Grid -->
        <section style="max-width: 1100px; margin: 0 auto 60px; padding: 0 24px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px;">
                <div style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; padding: 24px; text-align: center;">
                    <div style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 900; color: #f6d365;">22%</div>
                    <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 6px;">Schedule Compression</div>
                    <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 8px;">Autonomous sub-trade sequencing and material delivery critical-path locks.</p>
                </div>
                <div style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; padding: 24px; text-align: center;">
                    <div style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 900; color: #38bdf8;">$180K+</div>
                    <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 6px;">Average Trade Savings</div>
                    <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 8px;">Automated 3-bid leveling and wholesale material pass-through auditing.</p>
                </div>
                <div style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 18px; padding: 24px; text-align: center;">
                    <div style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 900; color: #f6d365;">100%</div>
                    <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 6px;">Photographic Verification</div>
                    <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 8px;">Computer vision QA for rebar spacing, thermal envelope, and MEP rough-ins.</p>
                </div>
                <div style="background: rgba(10, 15, 25, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 18px; padding: 24px; text-align: center;">
                    <div style="font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 900; color: #38bdf8;">0.6 ACH</div>
                    <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 6px;">Step Code 5 Airtightness</div>
                    <p style="font-size: 0.82rem; color: #cbd5e1; margin-top: 8px;">Predictive thermal modeling eliminating cold-climate building envelope leaks.</p>
                </div>
            </div>
        </section>

        <!-- Main Editorial Content -->
        <article id="case-study-content" style="max-width: 900px; margin: 0 auto; padding: 0 24px 80px; line-height: 1.8; font-size: 1.05rem;">
            
            <section style="background: rgba(10, 15, 25, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 18px; padding: 36px; margin-bottom: 40px;">
                <h2 style="font-family: 'Outfit', sans-serif; color: #ffffff; font-size: 1.8rem; margin-top: 0; margin-bottom: 16px;">
                    1. The Structural Challenge in Sea-to-Sky Custom Building
                </h2>
                <p>
                    Building luxury residential estates and high-density infill multiplexes along the Sea-to-Sky corridor (West Vancouver, Whistler, Squamish, North Vancouver) represents one of North America's most demanding physical environments. Builders navigate steep granite bedrock slopes, high-seismic shear dynamics (Sa = 0.94g), rigorous District of West Vancouver Watercourse Protection Bylaws (15m riparian buffers), and sub-zero alpine snow loads (8.5+ kPa in Whistler).
                </p>
                <p>
                    Conventional custom home contracting relies on fragmented communication: superintendents on paper clipboards, sub-trade markup inflation, delayed change-order approvals, and lagging municipal inspections. Under the leadership of <strong>Wayne Stevenson (Licensed BC Housing Residential Builder #52603)</strong>, Keystone Possibilities engineered a proprietary operational leap: integrating <em>autonomous multi-agent AI swarms</em> directly into daily on-site superintendence.
                </p>
            </section>

            <section style="background: rgba(10, 15, 25, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 18px; padding: 36px; margin-bottom: 40px;">
                <h2 style="font-family: 'Outfit', sans-serif; color: #ffffff; font-size: 1.8rem; margin-top: 0; margin-bottom: 16px;">
                    2. The FastMCP Multi-Agent Construction Fleet
                </h2>
                <p>
                    Rather than relying on generic consumer chatbots, Keystone Possibilities coordinates a dedicated fleet of specialized agents running on local daemon architecture and typed FastMCP protocol contracts:
                </p>
                <ul style="color: #cbd5e1; padding-left: 20px; margin-bottom: 24px;">
                    <li style="margin-bottom: 12px;"><strong>Geotechnical &amp; Bedrock Invariant Scanners:</strong> Ingest 3D LiDAR point clouds and borehole geotechnical reports to calculate rock anchor depths, stepped footing elevations, and blasting volumes before mobilization.</li>
                    <li style="margin-bottom: 12px;"><strong>BC Hydro Civil Utility (ES54) Pipeline Managers:</strong> Track primary duct banks, secondary underground conduits, and pad-mounted transformer (PMT) vault specifications to bypass the standard 6-month utility backlog.</li>
                    <li style="margin-bottom: 12px;"><strong>CCDC 5B Open-Book Ledger Auditors:</strong> Automatically reconcile supplier invoices and sub-trade draw applications against master contract trade allowances, guaranteeing zero hidden percentage markups.</li>
                    <li style="margin-bottom: 12px;"><strong>Computer Vision Inspection Observers:</strong> Analyze high-resolution on-site progress imagery to verify structural framing clips, Simpson Strong-Tie ATS rod tension, and continuous thermal envelope R-values prior to drywall closure.</li>
                </ul>

                <!-- Editorial Contextual Link Callout -->
                <div style="background: rgba(56, 189, 248, 0.08); border-left: 4px solid #38bdf8; padding: 24px; border-radius: 8px; margin: 30px 0;">
                    <span style="display: block; font-family: 'Outfit', sans-serif; color: #38bdf8; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;">
                        🔗 Technical Architecture Reference
                    </span>
                    <p style="margin: 0; color: #e2e8f0; font-size: 0.98rem; line-height: 1.6;">
                        For full technical specifications on the 28-agent daemon cluster, FastMCP tool servers, and Chrome DevTools Protocol automation runtime powering our operations, review the official documentation at the 
                        <a href="https://keystonerecomposition.com/ai-protocols/" target="_blank" rel="noopener noreferrer" style="color: #38bdf8; font-weight: 700; text-decoration: underline; transition: color 0.2s ease;">
                            Keystone AI Protocols Workstation Architecture &rarr;
                        </a>
                    </p>
                </div>
            </section>

            <section style="background: rgba(10, 15, 25, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 18px; padding: 36px; margin-bottom: 40px;">
                <h2 style="font-family: 'Outfit', sans-serif; color: #ffffff; font-size: 1.8rem; margin-top: 0; margin-bottom: 16px;">
                    3. Case Study: High-Snow-Load Alpine Estate in Whistler
                </h2>
                <p>
                    On a 6,200 sq ft custom mountain estate located in Whistler's Sunridge Plateau, snow loads demanded an engineered 12.8 kPa roof assembly with cold-roof thermal ventilation to eliminate attic condensation. The project involved:
                </p>
                <div style="background: rgba(4, 7, 13, 0.8); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; padding: 20px; margin: 20px 0;">
                    <h4 style="color: #f6d365; margin: 0 0 10px 0; font-family: 'Outfit', sans-serif;">Key Project Milestones Achieved:</h4>
                    <p style="margin: 0 0 8px 0; color: #cbd5e1;">&bull; <strong>Airtightness Test Result:</strong> Certified 0.58 ACH50 on final blower door test (exceeding BC Energy Step Code Level 5 requirements).</p>
                    <p style="margin: 0 0 8px 0; color: #cbd5e1;">&bull; <strong>Zero Structural Rework:</strong> 3D collision detection between heavy timber structural bents and ERV mechanical ducting prevented 14 field change orders.</p>
                    <p style="margin: 0; color: #cbd5e1;">&bull; <strong>Fiduciary Client Oversight:</strong> Complete open-book visibility into all $3.4M in hard trade costs via real-time client portal reporting.</p>
                </div>
                <p>
                    By coupling physical on-site builder superintendence with autonomous multi-agent intelligence, Keystone Possibilities delivers institutional execution speed to private custom estate owners and developers across British Columbia.
                </p>
            </section>

            <!-- Estimator Embed -->
            <section style="margin: 3.5rem 0;">
                <div style="text-align: center; margin-bottom: 24px;">
                    <span style="color: #38bdf8; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 6px;">
                        INSTANT INFILL MODELLING
                    </span>
                    <h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 0;">
                        Bill 44 Multiplex &amp; Construction Estimator
                    </h2>
                </div>
                <?php echo do_shortcode( '[keystone_bill44_estimator]' ); ?>
            </section>

            <!-- Embedded Lead Intake Form -->
            <section style="background: linear-gradient(135deg, rgba(10, 15, 25, 0.95), rgba(4, 7, 13, 0.98)); border: 1.5px solid #d4af37; border-radius: 18px; padding: 40px 32px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(212, 175, 55, 0.15);">
                <div style="text-align: center; margin-bottom: 28px;">
                    <span style="color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.80rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; display: block; margin-bottom: 8px;">
                        DIRECT SUPERINTENDENT INTAKE
                    </span>
                    <h3 style="color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; margin: 0 0 10px 0;">
                        Discuss Your Custom Build or Infill Project
                    </h3>
                    <p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto;">
                        Connect directly with Wayne Stevenson (BC Builder #52603) to evaluate site feasibility, geotechnical constraints, and CCDC 5B fiduciary cost structures.
                    </p>
                </div>

                <form method="POST" action="/wp-json/keystone/v1/lead" data-project-type="AI Construction Engineering Inquiry" style="max-width: 640px; margin: 0 auto;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                        <div>
                            <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">First Name *</label>
                            <input type="text" name="first_name" required placeholder="John" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
                        </div>
                        <div>
                            <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Surname *</label>
                            <input type="text" name="surname" required placeholder="Doe" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                        <div>
                            <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Email Address *</label>
                            <input type="email" name="client_email" required placeholder="client@example.com" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
                        </div>
                        <div>
                            <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Phone Number *</label>
                            <input type="tel" name="client_phone" required placeholder="(604) 000-0000" style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
                        </div>
                    </div>

                    <div style="margin-bottom: 16px;">
                        <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Project Location &amp; Municipality *</label>
                        <select name="project_location" required style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box;">
                            <option value="">Select Municipality...</option>
                            <option value="West Vancouver">West Vancouver</option>
                            <option value="Whistler">Whistler</option>
                            <option value="Squamish">Squamish</option>
                            <option value="North Vancouver">North Vancouver</option>
                            <option value="Vancouver">City of Vancouver</option>
                            <option value="Pemberton">Pemberton / Other</option>
                        </select>
                    </div>

                    <div style="margin-bottom: 24px;">
                        <label style="display: block; font-size: 0.78rem; font-weight: 700; color: #cbd5e1; margin-bottom: 6px; text-transform: uppercase;">Project Details &amp; Lot Address</label>
                        <textarea name="project_scope" rows="3" placeholder="Provide property address, planned square footage, or specific engineering requirements..." style="width: 100%; padding: 12px; background: rgba(5, 8, 14, 0.9); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 6px; color: #ffffff; font-size: 0.92rem; box-sizing: border-box; resize: vertical;"></textarea>
                    </div>

                    <button type="submit" style="width: 100%; background: linear-gradient(135deg, #d4af37, #f6d365); color: #04070d; border: none; padding: 14px 24px; border-radius: 9999px; font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; box-shadow: 0 4px 18px rgba(212, 175, 55, 0.4);">
                        Submit Direct Inquiry to Master Builder #52603 &rarr;
                    </button>
                </form>
            </section>

        </article>

    </main>
</div>

<?php
get_footer();
