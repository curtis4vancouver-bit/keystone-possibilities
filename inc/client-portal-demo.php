<?php
/**
 * Keystone Possibilities - Public "Client Portal Demo" (Virtual Jobsite Tour)
 *
 * Provides:
 * 1. [keystone_client_portal_demo] shortcode for rendering a public, interactive,
 *    anonymized project showcase with 360° pre-drywall MEP scans, daily supervisor logs,
 *    live line-item financial ledger with 10% lien holdback, and 2-5-10 warranty vault.
 * 2. Automatic template interception for /client-portal-demo/ route.
 *
 * @package KeystonePossibilitiesChild
 * @version 2.6.0
 */

if (!defined('ABSPATH')) {
    exit;
}

// ── 1. Intercept /client-portal-demo/ and inject virtual showcase if page not in DB ─
add_action('template_redirect', 'keystone_possibilities_handle_client_portal_demo_route', 5);
function keystone_possibilities_handle_client_portal_demo_route() {
    $uri = $_SERVER['REQUEST_URI'] ?? '';
    if (preg_match('#^/client-portal-demo/?$#i', parse_url($uri, PHP_URL_PATH) ?? '')) {
        // If a native page exists, let WordPress render it normally.
        // If not, render standalone high-converting luxury portal demo page.
        global $wp_query;
        if ($wp_query->is_404) {
            status_header(200);
            $wp_query->is_404 = false;
            nocache_headers();
            
            get_header();
            echo '<main id="primary" class="site-main" style="background:#04070d; min-height:80vh; padding: 2rem 1rem;">';
            echo do_shortcode('[keystone_client_portal_demo]');
            echo '</main>';
            get_footer();
            exit;
        }
    }
}

// Ensure the_content renders client portal demo if a native page is created
add_filter('the_content', 'keystone_possibilities_inject_portal_demo_content', 20);
function keystone_possibilities_inject_portal_demo_content($content) {
    if (is_page('client-portal-demo') || (is_singular() && preg_match('#client-portal-demo#i', $_SERVER['REQUEST_URI'] ?? ''))) {
        if (stripos($content, 'kp-client-portal-demo-wrapper') === false) {
            return $content . "\n\n" . do_shortcode('[keystone_client_portal_demo]');
        }
    }
    return $content;
}

// ── 2. Shortcode: [keystone_client_portal_demo] ──────────────────────────────
add_shortcode('keystone_client_portal_demo', 'keystone_possibilities_client_portal_demo_shortcode');
function keystone_possibilities_client_portal_demo_shortcode($atts) {
    ob_start();
    ?>
    <div id="kp-client-portal-demo-wrapper" style="max-width: 1200px; margin: 0 auto; font-family: 'Inter', -apple-system, sans-serif; color: #f8fafc;">
        
        <!-- Hero Header -->
        <div style="text-align: center; margin-bottom: 2.5rem; padding: 1rem;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.4); padding: 5px 16px; border-radius: 9999px; margin-bottom: 14px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #00f0ff; box-shadow: 0 0 10px #00f0ff;"></span>
                <span style="color: #00f0ff; font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">Radical Transparency • Client Portal Demo</span>
            </div>
            <h1 style="font-family: 'Outfit', sans-serif; font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; text-transform: uppercase; letter-spacing: 0.04em; margin: 0 0 0.75rem 0; background: linear-gradient(135deg, #ffffff 40%, #d4af37 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Live Virtual Jobsite &amp; Portal Tour
            </h1>
            <p style="color: #94a3b8; font-size: 1.1rem; max-width: 720px; margin: 0 auto; line-height: 1.6;">
                Experience the exact proprietary portal environment provided to our custom home and multiplex clients. Complete 360° pre-drywall digital scans, timestamped supervisor logs, and open-book trade ledgers.
            </p>
        </div>

        <!-- Project Meta Bar -->
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 12px; padding: 1.25rem 1.75rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">Demonstration Project:</span>
                <div style="color: #00f0ff; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.2rem;">The Highland Estate — Lot 42, Squamish, BC</div>
            </div>
            <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
                <div>
                    <span style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;">Milestone:</span>
                    <div style="color: #34d399; font-weight: 700; font-size: 0.95rem;">Pre-Drywall MEP Lock (94% Verified)</div>
                </div>
                <div>
                    <span style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;">BC Builder License:</span>
                    <div style="color: #d4af37; font-weight: 700; font-size: 0.95rem;">#52603 (Wayne Stevenson)</div>
                </div>
                <div>
                    <span style="color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;">Next Milestone:</span>
                    <div style="color: #f8fafc; font-weight: 700; font-size: 0.95rem;">Blow-in Cellulose &amp; Drywall Hang</div>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div style="display: flex; gap: 8px; margin-bottom: 1.5rem; overflow-x: auto; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px;">
            <button class="kp-portal-tab active" data-target="kp-tab-360" style="background: rgba(0, 240, 255, 0.15); border: 1px solid #00f0ff; color: #00f0ff; padding: 10px 20px; border-radius: 8px; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; cursor: pointer; transition: all 0.2s;">
                📸 360° Pre-Drywall Scan
            </button>
            <button class="kp-portal-tab" data-target="kp-tab-logs" style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; padding: 10px 20px; border-radius: 8px; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; cursor: pointer; transition: all 0.2s;">
                📋 Daily Site Logs &amp; QA
            </button>
            <button class="kp-portal-tab" data-target="kp-tab-ledger" style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; padding: 10px 20px; border-radius: 8px; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; cursor: pointer; transition: all 0.2s;">
                💲 Open-Book Trade Ledger
            </button>
            <button class="kp-portal-tab" data-target="kp-tab-vault" style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; padding: 10px 20px; border-radius: 8px; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; cursor: pointer; transition: all 0.2s;">
                🛡️ 2-5-10 Warranty &amp; Permits
            </button>
        </div>

        <!-- TAB 1: 360° PRE-DRYWALL DIGITAL SCAN VIEWER -->
        <div id="kp-tab-360" class="kp-portal-pane" style="display: block;">
            <div style="background: #000000; border: 1px solid rgba(0, 240, 255, 0.4); border-radius: 12px; overflow: hidden; position: relative; height: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
                
                <!-- Simulated 360 Pre-Drywall Canvas / Pan Container -->
                <div id="kp-360-viewport" style="width: 100%; height: 100%; background: radial-gradient(circle at center, #1e293b 0%, #020617 100%); position: relative; cursor: grab; display: flex; align-items: center; justify-content: center; overflow: hidden; user-select: none;">
                    
                    <!-- Structural Grid Background simulating framing cavity -->
                    <div style="position: absolute; inset: 0; background-image: linear-gradient(rgba(212,175,55,0.15) 1px, transparent 1px), linear-gradient(90deg, rgba(212,175,55,0.15) 1px, transparent 1px); background-size: 60px 60px; opacity: 0.7;"></div>

                    <!-- Framing & MEP Simulation Layers -->
                    <div id="kp-360-stage" style="position: absolute; width: 1400px; height: 800px; transition: transform 0.05s ease-out; display: flex; align-items: center; justify-content: space-around;">
                        
                        <!-- Stud Wall 1 -->
                        <div style="width: 280px; height: 600px; border: 2px dashed rgba(255,255,255,0.3); border-radius: 8px; padding: 1rem; position: relative; background: rgba(15,23,42,0.6);">
                            <span style="color:#d4af37; font-family:'Outfit'; font-weight:700; font-size:0.8rem;">FRAME GRID: WALL B-4</span>
                            <div style="position: absolute; top: 120px; left: 40px; background: rgba(239,68,68,0.25); border: 1px solid #ef4444; border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; color: #fca5a5;">
                                🔴 PEX-A Hot Water Trunk (1")
                            </div>
                            <div style="position: absolute; top: 200px; left: 30px; background: rgba(59,130,246,0.25); border: 1px solid #3b82f6; border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; color: #93c5fd;">
                                🔵 PEX-A Cold Water Line (3/4")
                            </div>
                            <div style="position: absolute; top: 320px; left: 20px; background: rgba(234,179,8,0.25); border: 1px solid #eab308; border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; color: #fef08a;">
                                ⚡ 200A Sub-Panel Feed Conduits
                            </div>
                        </div>

                        <!-- Central Mechanical Room / HVAC -->
                        <div style="width: 320px; height: 600px; border: 2px dashed rgba(0,240,255,0.4); border-radius: 8px; padding: 1rem; position: relative; background: rgba(15,23,42,0.8);">
                            <span style="color:#00f0ff; font-family:'Outfit'; font-weight:700; font-size:0.8rem;">MEP HUB: HRV &amp; HEAT PUMP</span>
                            <div style="position: absolute; top: 140px; left: 30px; background: rgba(16,185,129,0.25); border: 1.5px solid #10b981; border-radius: 6px; padding: 6px 12px; font-size: 0.8rem; color: #6ee7b7;">
                                🌿 Zehnder ComfoAir Q350 HRV (84% SRE)
                            </div>
                            <div style="position: absolute; top: 240px; left: 20px; background: rgba(168,85,247,0.25); border: 1px solid #a855f7; border-radius: 6px; padding: 4px 10px; font-size: 0.75rem; color: #d8b4fe;">
                                📡 Cat6A Shielded Home Automation Runs
                            </div>
                            <div style="position: absolute; top: 360px; left: 40px; background: rgba(212,175,55,0.25); border: 1px solid #d4af37; border-radius: 6px; padding: 4px 10px; font-size: 0.75rem; color: #f6d365;">
                                🛡️ Acoustic Resilient Channel (RC-1 Deluxe)
                            </div>
                        </div>

                        <!-- Stud Wall 2 -->
                        <div style="width: 280px; height: 600px; border: 2px dashed rgba(255,255,255,0.3); border-radius: 8px; padding: 1rem; position: relative; background: rgba(15,23,42,0.6);">
                            <span style="color:#d4af37; font-family:'Outfit'; font-weight:700; font-size:0.8rem;">EXTERIOR WALL: STEP CODE 5</span>
                            <div style="position: absolute; top: 180px; left: 20px; background: rgba(16,185,129,0.25); border: 1px solid #10b981; border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; color: #6ee7b7;">
                                🧱 4" Continuous Exterior Rockwool (R-16.8)
                            </div>
                            <div style="position: absolute; top: 280px; left: 30px; background: rgba(0,240,255,0.25); border: 1px solid #00f0ff; border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; color: #67e8f9;">
                                🪟 Innotech Triple-Glazed Argon Rough-In
                            </div>
                        </div>

                    </div>

                    <!-- Overlay Controls -->
                    <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(4,7,13,0.85); border: 1px solid rgba(212,175,55,0.4); border-radius: 30px; padding: 6px 18px; display: flex; gap: 12px; align-items: center; z-index: 10;">
                        <span style="font-size: 0.8rem; color: #94a3b8;">Click &amp; Drag to Pan 360° Scan</span>
                        <button id="kp-360-left" style="background: none; border: none; color: #00f0ff; font-size: 1.2rem; cursor: pointer;">◀</button>
                        <button id="kp-360-reset" style="background: none; border: none; color: #d4af37; font-size: 0.8rem; cursor: pointer; text-transform: uppercase; font-weight: 700;">Reset</button>
                        <button id="kp-360-right" style="background: none; border: none; color: #00f0ff; font-size: 1.2rem; cursor: pointer;">▶</button>
                    </div>

                    <!-- Scan Stamp Badge -->
                    <div style="position: absolute; top: 16px; left: 16px; background: rgba(4,7,13,0.85); border: 1px solid rgba(0,240,255,0.5); border-radius: 6px; padding: 6px 12px; font-size: 0.78rem; color: #00f0ff; z-index: 10;">
                        ● LIDAR / Matterport Scan ID: KP-360-PRE-202609
                    </div>
                </div>
            </div>
            <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 10px; text-align: center;">
                Every Keystone client receives complete sub-millimeter 360° spatial documentation of every conduit, pipe, and framing member permanently archived before insulation and drywall closure.
            </p>
        </div>

        <!-- TAB 2: DAILY SITE SUPERVISOR LOGS & FIELD QA -->
        <div id="kp-tab-logs" class="kp-portal-pane" style="display: none;">
            <div style="background: #0a0f19; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 8px;">
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; text-transform: uppercase; color: #d4af37; margin: 0;">
                        Field Supervisor Inspection Stream
                    </h3>
                    <span style="font-size: 0.85rem; color: #34d399; font-weight: 600;">● Live Onsite Stream Active</span>
                </div>

                <!-- Log Entry 1 -->
                <div style="border-left: 2px solid #00f0ff; padding-left: 1.25rem; margin-bottom: 1.5rem; position: relative;">
                    <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; border-radius: 50%; background: #00f0ff;"></div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 0.82rem; color: #94a3b8;">
                        <span>September 18, 2026 • 15:45 PST</span>
                        <span style="color: #00f0ff; font-weight: 700;">Supervisor: Wayne Stevenson (#52603)</span>
                    </div>
                    <h4 style="font-size: 1rem; color: #ffffff; margin: 0 0 6px 0; font-family: 'Outfit', sans-serif;">Pre-Drywall Rough-In Municipality Sign-Off</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin: 0 0 8px 0;">
                        District building inspector completed plumbing rough-in and electrical branch inspection. 100% clean pass with zero deficiencies. Acoustic RC-1 channel separation verified on party walls. 360° LiDAR capture completed and synced to client portal vault.
                    </p>
                    <div style="display: inline-block; background: rgba(16,185,129,0.15); border: 1px solid #10b981; border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; color: #34d399;">
                        ✓ Municipal Permit Stage #04 APPROVED
                    </div>
                </div>

                <!-- Log Entry 2 -->
                <div style="border-left: 2px solid rgba(255,255,255,0.2); padding-left: 1.25rem; margin-bottom: 1.5rem; position: relative;">
                    <div style="position: absolute; left: -6px; top: 0; width: 10px; height: 10px; border-radius: 50%; background: #64748b;"></div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 0.82rem; color: #94a3b8;">
                        <span>September 14, 2026 • 11:20 PST</span>
                        <span style="color: #d4af37; font-weight: 700;">Trade Lead: Coastal GeoTech</span>
                    </div>
                    <h4 style="font-size: 1rem; color: #ffffff; margin: 0 0 6px 0; font-family: 'Outfit', sans-serif;">Foundation 28-Day Concrete Core Compression Test</h4>
                    <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin: 0 0 8px 0;">
                        Independent lab break tests for 35 MPa foundation wall pour returned 39.2 MPa at 28 days, exceeding structural engineer specifications by 12%. Sub-slab radon membrane inspection signed off.
                    </p>
                    <div style="display: inline-block; background: rgba(0,240,255,0.15); border: 1px solid #00f0ff; border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; color: #00f0ff;">
                        ✓ GeoTechnical Lab Certificate #CG-4912 Archived
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: OPEN-BOOK TRADE LEDGER & LIEN HOLDBACK -->
        <div id="kp-tab-ledger" class="kp-portal-pane" style="display: none;">
            <div style="background: #0a0f19; border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 12px; padding: 1.5rem; overflow-x: auto;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; text-transform: uppercase; color: #d4af37; margin: 0;">
                            Live Construction Draw &amp; Trade Pass-Through
                        </h3>
                        <span style="color: #94a3b8; font-size: 0.82rem;">BC Builders Lien Act: Strict 10% Statutory Holdback Maintained on all lines</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;">Total Hard Costs to Date:</span>
                        <div style="color: #10b981; font-family: 'Outfit', sans-serif; font-weight: 900; font-size: 1.4rem;">$642,850.00</div>
                    </div>
                </div>

                <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 1.5px solid rgba(212,175,55,0.4); color: #d4af37; font-family: 'Outfit', sans-serif; text-transform: uppercase; font-size: 0.78rem;">
                            <th style="padding: 10px;">Line Item / Trade</th>
                            <th style="padding: 10px;">Invoice #</th>
                            <th style="padding: 10px;">Gross Trade Cost</th>
                            <th style="padding: 10px;">10% Lien Holdback</th>
                            <th style="padding: 10px;">Keystone Markup</th>
                            <th style="padding: 10px;">Net Paid</th>
                            <th style="padding: 10px;">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                            <td style="padding: 12px 10px; font-weight: 600; color: #f8fafc;">Civil Bedrock Pin Piling</td>
                            <td style="padding: 12px 10px; color: #94a3b8;">INV-8821</td>
                            <td style="padding: 12px 10px;">$84,200.00</td>
                            <td style="padding: 12px 10px; color: #f6d365;">-$8,420.00</td>
                            <td style="padding: 12px 10px; color: #34d399; font-weight: 700;">$0.00 (Pass-through)</td>
                            <td style="padding: 12px 10px; font-weight: 700;">$75,780.00</td>
                            <td style="padding: 12px 10px;"><span style="color: #34d399;">● Approved</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                            <td style="padding: 12px 10px; font-weight: 600; color: #f8fafc;">35 MPa Concrete Forming &amp; Pour</td>
                            <td style="padding: 12px 10px; color: #94a3b8;">INV-4019</td>
                            <td style="padding: 12px 10px;">$148,500.00</td>
                            <td style="padding: 12px 10px; color: #f6d365;">-$14,850.00</td>
                            <td style="padding: 12px 10px; color: #34d399; font-weight: 700;">$0.00 (Pass-through)</td>
                            <td style="padding: 12px 10px; font-weight: 700;">$133,650.00</td>
                            <td style="padding: 12px 10px;"><span style="color: #34d399;">● Approved</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                            <td style="padding: 12px 10px; font-weight: 600; color: #f8fafc;">Structural SPF Framing &amp; Engineered Trusses</td>
                            <td style="padding: 12px 10px; color: #94a3b8;">INV-7732</td>
                            <td style="padding: 12px 10px;">$215,000.00</td>
                            <td style="padding: 12px 10px; color: #f6d365;">-$21,500.00</td>
                            <td style="padding: 12px 10px; color: #34d399; font-weight: 700;">$0.00 (Pass-through)</td>
                            <td style="padding: 12px 10px; font-weight: 700;">$193,500.00</td>
                            <td style="padding: 12px 10px;"><span style="color: #34d399;">● Approved</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                            <td style="padding: 12px 10px; font-weight: 600; color: #f8fafc;">BC Hydro ES54 Underground Civil Duct Bank</td>
                            <td style="padding: 12px 10px; color: #94a3b8;">INV-9021</td>
                            <td style="padding: 12px 10px;">$68,400.00</td>
                            <td style="padding: 12px 10px; color: #f6d365;">-$6,840.00</td>
                            <td style="padding: 12px 10px; color: #34d399; font-weight: 700;">$0.00 (Pass-through)</td>
                            <td style="padding: 12px 10px; font-weight: 700;">$61,560.00</td>
                            <td style="padding: 12px 10px;"><span style="color: #34d399;">● Approved</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 4: 2-5-10 WARRANTY & COMPLIANCE VAULT -->
        <div id="kp-tab-vault" class="kp-portal-pane" style="display: none;">
            <div style="background: #0a0f19; border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 12px; padding: 1.5rem;">
                <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; text-transform: uppercase; color: #00f0ff; margin: 0 0 1.25rem 0;">
                    Certified Builder Credentials &amp; Warranty Vault
                </h3>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem;">
                    
                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(212,175,55,0.3); border-radius: 8px; padding: 1.25rem;">
                        <div style="font-size: 1.8rem; margin-bottom: 6px;">🏛️</div>
                        <h4 style="font-size: 1rem; color: #d4af37; margin: 0 0 4px 0; font-family: 'Outfit', sans-serif;">BC Housing Builder License</h4>
                        <p style="font-size: 0.85rem; color: #94a3b8; margin: 0 0 8px 0;">License Number: <strong>#52603</strong><br>General Contractor: Wayne Stevenson</p>
                        <span style="color: #34d399; font-size: 0.78rem; font-weight: 700;">✓ Active &amp; In Good Standing</span>
                    </div>

                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(0,240,255,0.3); border-radius: 8px; padding: 1.25rem;">
                        <div style="font-size: 1.8rem; margin-bottom: 6px;">🛡️</div>
                        <h4 style="font-size: 1rem; color: #00f0ff; margin: 0 0 4px 0; font-family: 'Outfit', sans-serif;">2-5-10 Home Warranty</h4>
                        <p style="font-size: 0.85rem; color: #94a3b8; margin: 0 0 8px 0;">Pacific Home Warranty #PHW-52603<br>2 Yr Labour/Material | 5 Yr Envelope | 10 Yr Structure</p>
                        <span style="color: #34d399; font-size: 0.78rem; font-weight: 700;">✓ Bound &amp; Registered</span>
                    </div>

                    <div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; padding: 1.25rem;">
                        <div style="font-size: 1.8rem; margin-bottom: 6px;">⚡</div>
                        <h4 style="font-size: 1rem; color: #f8fafc; margin: 0 0 4px 0; font-family: 'Outfit', sans-serif;">BC Hydro ES54 Civil</h4>
                        <p style="font-size: 0.85rem; color: #94a3b8; margin: 0 0 8px 0;">Registered Underground Civil Contractor<br>Authorized for 400A–600A primary duct conversions</p>
                        <span style="color: #34d399; font-size: 0.78rem; font-weight: 700;">✓ ES54 Certified</span>
                    </div>

                </div>
            </div>
        </div>

        <!-- CTA Action Footer -->
        <div style="margin-top: 2.5rem; background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(0, 240, 255, 0.15) 100%); border: 1.5px solid #d4af37; border-radius: 12px; padding: 2rem; text-align: center;">
            <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 800; text-transform: uppercase; color: #f8fafc; margin: 0 0 0.5rem 0;">
                Ready for Radical Transparency on Your Build?
            </h3>
            <p style="color: #94a3b8; font-size: 0.95rem; max-width: 600px; margin: 0 auto 1.25rem auto;">
                Every custom home and multiplex client receives their own private portal credentials with 24/7 access to live financial ledgers, 360° LiDAR captures, and trade invoices.
            </p>
            <a href="/feasibility-plan/" style="display: inline-block; background: linear-gradient(135deg, #d4af37 0%, #aa820a 100%); color: #04070d; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.06em; box-shadow: 0 4px 20px rgba(212, 175, 55, 0.35);">
                Book a Pre-Construction Feasibility Review With Wayne
            </a>
        </div>

    </div>

    <!-- Interactive Tabs & 360 Panning Script -->
    <script>
    document.addEventListener('DOMContentLoaded', function () {
        // Tab switcher
        const tabs = document.querySelectorAll('.kp-portal-tab');
        const panes = document.querySelectorAll('.kp-portal-pane');

        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                tabs.forEach(function (t) {
                    t.style.background = 'rgba(15, 23, 42, 0.8)';
                    t.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                    t.style.color = '#94a3b8';
                });
                panes.forEach(function (p) { p.style.display = 'none'; });

                this.style.background = 'rgba(0, 240, 255, 0.15)';
                this.style.borderColor = '#00f0ff';
                this.style.color = '#00f0ff';

                const target = document.getElementById(this.getAttribute('data-target'));
                if (target) target.style.display = 'block';
            });
        });

        // 360 Panning simulation
        const stage = document.getElementById('kp-360-stage');
        const viewport = document.getElementById('kp-360-viewport');
        let isDown = false;
        let startX;
        let currentTranslate = 0;

        if (viewport && stage) {
            viewport.addEventListener('mousedown', function (e) {
                isDown = true;
                viewport.style.cursor = 'grabbing';
                startX = e.pageX - currentTranslate;
            });

            window.addEventListener('mouseup', function () {
                isDown = false;
                if (viewport) viewport.style.cursor = 'grab';
            });

            viewport.addEventListener('mousemove', function (e) {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - startX;
                currentTranslate = Math.max(-400, Math.min(400, x));
                stage.style.transform = 'translateX(' + currentTranslate + 'px)';
            });

            document.getElementById('kp-360-left').addEventListener('click', function () {
                currentTranslate = Math.min(400, currentTranslate + 120);
                stage.style.transform = 'translateX(' + currentTranslate + 'px)';
            });
            document.getElementById('kp-360-right').addEventListener('click', function () {
                currentTranslate = Math.max(-400, currentTranslate - 120);
                stage.style.transform = 'translateX(' + currentTranslate + 'px)';
            });
            document.getElementById('kp-360-reset').addEventListener('click', function () {
                currentTranslate = 0;
                stage.style.transform = 'translateX(0px)';
            });
        }
    });
    </script>
    <?php
    return ob_get_clean();
}
