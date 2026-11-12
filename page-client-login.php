<?php
/**
 * Template Name: Client Login Portal
 * Template Post Type: page
 *
 * Keystone Possibilities Ltd. (#52603) — Multi-Job Open-Book CCDC 5B Client & Builder Portal (v10/v15)
 * Phase-1 Quiet-Luxury Cleanup: Externalized browser-cached portal-v10.css + portal-v10.js,
 * Official Interlocking Gold Keyhole Crest (WP Media IDs 1637 & 1639), <390px mobile overflow fix,
 * and hardened /wp-json/keystone/v1/portal-auth session support.
 *
 * @package Keystone_Possibilities_Child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Defensive enqueue guard: loads portal-v10.css & portal-v10.js strictly once if not already queued by inc/enqueue.php.
add_action(
	'wp_enqueue_scripts',
	function () {
		global $wp_styles, $wp_scripts;

		$css_rel  = '/assets/css/portal-v10.css';
		$js_rel   = '/assets/js/portal-v10.js';
		$css_path = get_stylesheet_directory() . $css_rel;
		$js_path  = get_stylesheet_directory() . $js_rel;
		$css_uri  = get_stylesheet_directory_uri() . $css_rel;
		$js_uri   = get_stylesheet_directory_uri() . $js_rel;

		$css_already = false;
		if ( isset( $wp_styles->registered ) && is_array( $wp_styles->registered ) ) {
			foreach ( $wp_styles->registered as $handle => $obj ) {
				if ( ! empty( $obj->src ) && false !== strpos( $obj->src, 'portal-v10.css' ) ) {
					if ( wp_style_is( $handle, 'enqueued' ) || wp_style_is( $handle, 'to_do' ) || wp_style_is( $handle, 'done' ) ) {
						$css_already = true;
						break;
					}
				}
			}
		}
		if ( ! $css_already && file_exists( $css_path ) ) {
			wp_enqueue_style(
				'kp-portal-v10',
				$css_uri,
				array(),
				(string) filemtime( $css_path )
			);
		}

		$js_already = false;
		if ( isset( $wp_scripts->registered ) && is_array( $wp_scripts->registered ) ) {
			foreach ( $wp_scripts->registered as $handle => $obj ) {
				if ( ! empty( $obj->src ) && false !== strpos( $obj->src, 'portal-v10.js' ) ) {
					if ( wp_script_is( $handle, 'enqueued' ) || wp_script_is( $handle, 'to_do' ) || wp_script_is( $handle, 'done' ) ) {
						$js_already = true;
						break;
					}
				}
			}
		}
		if ( ! $js_already && file_exists( $js_path ) ) {
			wp_enqueue_script(
				'kp-portal-v10',
				$js_uri,
				array(),
				(string) filemtime( $js_path ),
				true
			);
		}
	},
	99
);

$kp_logos      = function_exists( 'kp_get_official_logos' ) ? kp_get_official_logos() : array();
$kp_emblem_url = ! empty( $kp_logos['emblem_gold_transparent'] )
	? $kp_logos['emblem_gold_transparent']
	: 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_emblem_gold_transparent.png';
$kp_badge_url  = ! empty( $kp_logos['header_badge_bold'] )
	? $kp_logos['header_badge_bold']
	: 'https://keystonepossibilities.ca/wp-content/uploads/2026/09/keystone_real_logo_badge_bold.png';

get_header();
?>

<main id="main-content" class="kp-client-login-shell" role="main">
	<span id="kp-portal-v10-css-loaded" hidden></span>
<!-- KEYSTONE POSSIBILITIES LTD - MULTI-JOB SOVEREIGN CLIENT & BUILDER PORTAL (v10) -->
<div id="keystone-portal-wrapper">

      <!-- =========================================================================
       1. MULTI-JOB LOGIN GATE CARD (#ks-login-card) — PAGE 1 CANONICAL STANDARD
       ========================================================================= -->
  <div id="ks-login-card" style="width:100%; max-width:660px; background:#04070d; border:1.5px solid rgba(212,175,55,0.58); border-radius:22px; padding:clamp(1.35rem, 4.5vw, 2.6rem) clamp(1.15rem, 4vw, 2.5rem); backdrop-filter:blur(28px); -webkit-backdrop-filter:blur(28px); box-shadow:0 28px 68px rgba(0,0,0,0.94), 0 0 34px rgba(212,175,55,0.14); text-align:center; box-sizing:border-box; position:relative; margin:2.2rem auto;">
    
    <!-- Top Licensed Builder Pill (Pure #04070d Black + Gold Border + Pure White Wave Letters) -->
    <div class="kp-login-kicker-pill" style="display:inline-flex; align-items:center; justify-content:center; gap:0.55rem; background:#04070d; border:1.5px solid rgba(212,175,55,0.78); padding:0 1.25rem; height:42px; border-radius:9999px; font-size:0.75rem; font-weight:800; color:#ffffff; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:1.35rem; box-shadow:0 10px 24px rgba(0,0,0,0.85), inset 0 0 12px rgba(212,175,55,0.08);">
      <span style="width:8px; height:8px; border-radius:50%; background:#d4af37; box-shadow:0 0 10px rgba(212,175,55,0.9); display:inline-block; flex-shrink:0;"></span>
      <span class="ks-wave-text">BC Housing Licensed Builder #52603 &bull; 2-5-10 Warranty</span>
    </div>

    <!-- Official Interlocking Gold Keyhole Crest (WP Media ID 1637) -->
    <div class="kp-login-emblem-wrap">
      <img
        src="<?php echo esc_url( $kp_emblem_url ); ?>"
        alt="Keystone Possibilities Ltd. Official Keyhole Crest"
        width="52"
        height="52"
        class="kp-login-emblem-img"
        decoding="async"
      />
    </div>

    <!-- Brand Header: Strictly 2-Line Title Case (Line 1 Pure White, Line 2 White-to-Gold Gradient) -->
    <h1 class="kp-login-hero-h1" style="font-family:'Plus Jakarta Sans','Inter',-apple-system,sans-serif !important; font-size:clamp(1.45rem, 2.1vw, 1.82rem) !important; font-weight:800 !important; line-height:1.22 !important; margin:0 0 0.65rem 0 !important; text-transform:none !important; letter-spacing:-0.02em !important; color:#FFFFFF !important;">
      <span class="kp-login-h1-white" style="display:block; white-space:normal; color:#FFFFFF !important; -webkit-text-fill-color:#FFFFFF !important;">Keystone Possibilities Ltd.</span>
      <span class="kp-login-h1-gold" style="display:block; white-space:normal; background:linear-gradient(90deg, #f8fafc 0%, #fef3c7 14%, #f6d365 36%, #d4af37 72%, #c59b27 100%) !important; -webkit-background-clip:text !important; background-clip:text !important; -webkit-text-fill-color:transparent !important; color:transparent !important;">Private Owner &amp; Builder Project Portal</span>
    </h1>
    <p style="color:#cbd5e1 !important; font-size:0.94rem !important; margin:0 0 1.65rem 0 !important; line-height:1.55 !important;">
      Direct 24/7 <strong style="color:#ffffff !important; font-weight:700 !important;">Open-Book CCDC 5B Command</strong> for Active Project Owners, Architects &amp; Trade Partners
    </p>

    <!-- Error / Status Banner (Zero Passcodes Exposed) -->
    <div id="ks-auth-error" style="display:none; background:rgba(239,68,68,0.15); border:1px solid #ef4444; color:#fca5a5; padding:0.75rem 1rem; border-radius:12px; font-size:0.84rem; margin-bottom:1.15rem; text-align:left;">
      Invalid access passcode. Please enter the private Passcode issued for your Job Address by Keystone Possibilities Ltd.
    </div>

    <!-- Job Address Selector (Strictly 1 Active Project Address) -->
    <div style="text-align:left; margin-bottom:1.2rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.45rem;">
        <label for="ks-job-select" style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#ffffff !important;">
          <svg class="kp-login-svg-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-5.686-7-11a7 7 0 1 1 14 0c0 5.314-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg> Select Job Address
        </label>
        <span style="font-size:0.72rem; font-weight:700; color:#d4af37 !important;">Active Build &bull; KP-2026-001</span>
      </div>
      <select id="ks-job-select" onchange="onLoginJobSelectChange(this.value)" style="width:100%; height:50px; background:#04070d !important; border:1.5px solid rgba(212,175,55,0.58) !important; border-radius:14px !important; padding:0 1rem; font-size:0.92rem; font-weight:700; color:#ffffff !important; box-sizing:border-box; outline:none; margin-bottom:0; cursor:pointer; box-shadow:inset 0 0 12px rgba(0,0,0,0.85);">
        <option value="KP-2026-001" selected>40484 Tantalus Rd, Squamish, BC (KP-2026-001)</option>
      </select>
      <input type="hidden" id="ks-client-id" value="40484 Tantalus Rd, Squamish, BC" />
    </div>

    <!-- Passcode Input (Zero Public Passcode Hints) -->
    <div style="text-align:left; margin-bottom:1.55rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.45rem;">
        <label for="ks-passcode" style="font-size:0.78rem; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#ffffff !important;">
          <svg class="kp-login-svg-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L21 2m-3 3l3 3m-6 1l2.5 2.5"/></svg> Private Access Passcode
        </label>
        <span style="font-size:0.72rem; font-weight:600; color:#cbd5e1 !important;">Owner or Builder Login</span>
      </div>
      <input
        type="password"
        id="ks-passcode"
        placeholder="Enter Private Passcode"
        autocomplete="current-password"
        style="width:100%; height:50px; background:#04070d !important; border:1.5px solid rgba(212,175,55,0.58) !important; border-radius:14px !important; padding:0 1rem; font-size:0.94rem; color:#ffffff !important; box-sizing:border-box; outline:none; box-shadow:inset 0 0 12px rgba(0,0,0,0.85);"
        onkeydown="if(event.key==='Enter') handlePortalLogin()"
      />
    </div>

    <!-- Primary Action: Pure #04070d Black Pill Button + Gold Border + Pure White Letters + Gold Hover Wave -->
    <button
      type="button"
      id="btn-submit-login"
      onclick="handlePortalLogin()"
      class="kp-btn-sovereign-gold"
      style="width:100%; height:52px !important; border-radius:9999px !important; font-size:0.96rem !important; font-weight:800 !important; justify-content:center !important;"
    >
      <span class="ks-wave-text"><svg class="kp-login-svg-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.6-1.7"/></svg> Unlock Selected Job Portal &rarr;</span>
    </button>

    <!-- Prospective Landowner / Realtor Pre-Construction Bridge -->
    <div class="kp-login-feasibility-cta">
      Evaluating a new BC lot, slope parcel, or Bill 44 multiplex?
      <a href="<?php echo esc_url( home_url( '/feasibility-plan/' ) ); ?>">Request a 48-Hr Constructability Review &rarr;</a>
    </div>

    <!-- Trust Footer (Zero Blue) -->
    <div style="margin-top:1.45rem; border-top:1px solid rgba(212,175,55,0.22); padding-top:1.15rem; font-size:0.76rem; color:#cbd5e1 !important; line-height:1.55; text-align:center;">
      Authorized Property Owner &amp; Builder Access Only &bull; Need your job passcode? Contact <strong style="color:#ffffff !important;">Wayne Stevenson</strong> at <a href="tel:6048489688" style="color:#f6d365 !important; font-weight:800 !important; text-decoration:none !important;">(604) 848-9688</a>
      <div style="margin-top:0.38rem; font-size:0.7rem; color:#94a3b8 !important;">
        Keystone Possibilities Ltd. (BC Licensed Builder #52603) &bull; Statutory BC Builders Lien Act 10% Trust &bull; 2-5-10 National Home Warranty
      </div>
    </div>
  </div>


  <!-- =========================================================================
       2. AUTHENTICATED 6-TAB MULTI-JOB PORTAL (#ks-authenticated-portal)
       ========================================================================= -->
  <div id="ks-authenticated-portal" style="display:none !important;">
    
        <!-- Single-Line Sleek Executive Header (Locked to Active Job, Zero Extra Buttons, Fits 100% Inside) -->
    <header class="kp-app-header">
      <div class="kp-header-left">
        <div class="kp-brand-pill">
          <img src="<?php echo esc_url( $kp_badge_url ); ?>" alt="Keystone Possibilities Ltd." width="28" height="28" class="kp-brand-pill-logo" decoding="async" />
          <div>
            <div class="kp-brand-main">KEYSTONE POSSIBILITIES LTD.</div>
            <div class="kp-brand-sub">BC Licensed Builder #52603 &bull; Wayne Stevenson</div>
          </div>
        </div>
      </div>

      <!-- Center: Static Active Job Title & Address (Fits cleanly, no job switcher) -->
      <div class="kp-header-center-job">
        <span id="kp-header-static-job-title" class="kp-header-job-addr">
          40484 Tantalus Rd, Squamish, BC
        </span>
        <span class="kp-header-job-sep">&mdash;</span>
        <span id="kp-header-static-job-sub" class="kp-header-job-code">
          4-Unit Bill 44 Multiplex
        </span>
        <!-- Hidden select preserved for legacy JS compatibility -->
        <select id="kp-header-job-select" class="kp-header-job-select" onchange="switchActiveJob(this.value)" style="display:none !important; display:none !important; display:none !important; margin-left:8px; background:rgba(4,8,16,0.92); border:1px solid rgba(212,175,55,0.45); border-radius:9999px; padding:4px 10px; color:#f3e5ab; font-size:0.75rem; font-weight:800; cursor:pointer;"></select>
      </div>

      <!-- Right: ONLY Wayne Stevenson & Property Owner Name -->
      <div class="kp-header-right">
        <div class="kp-parties-badge" id="kp-header-parties-badge" title="Contracting Parties">
          <span style="color:#d4af37; font-weight:800;">Wayne Stevenson</span>
          <span style="color:rgba(255,255,255,0.35); margin:0 6px;">&times;</span>
          <span id="kp-header-owner-name" style="color:#ffffff; font-weight:800;">David &amp; Sarah Kensington</span>
        </div>
      </div>
    </header>

    <!-- Main Portal Body -->
    <main class="kp-portal-main">

      <!-- Slimmer Top 6 Master Navigation Tabs (Gold fill with Black text when active/clicked) -->
      <nav class="kp-nav-bar" id="kp-master-nav" style="grid-template-columns: repeat(6, minmax(0, 1fr)) !important;">
        <button type="button" class="kp-nav-tab active" data-tab="1" onclick="switchPortalPage(1, this)">
          1. Owner &amp; Contract
        </button>
        <button type="button" class="kp-nav-tab" data-tab="2" onclick="switchPortalPage(2, this)">
          2. Live Calendar Updates
        </button>
        <button type="button" class="kp-nav-tab" data-tab="4" onclick="switchPortalPage(4, this)">
          3. Master Trade Breakdown
        </button>
        <button type="button" class="kp-nav-tab" data-tab="6" onclick="switchPortalPage(6, this)">
          4. Master Financials &amp; PDFs
        </button>
        <button type="button" class="kp-nav-tab" data-tab="5" onclick="switchPortalPage(5, this)">
          5. Material &amp; Framing Breakdown
        </button>
        <button type="button" class="kp-nav-tab" data-tab="3" onclick="switchPortalPage(3, this)">
          6. Warranty &amp; Inspections
        </button>
      </nav>


      <!-- =====================================================================
           TAB 1: 1. OWNER & CONTRACT
           Strictly Gold, White & Black Palette — 3 Clean Executive Sections:
           1) Project Amount & Backtracked Running Capital Spent
           2) Where We Are Sitting (Daily Write-Up Preview) + Interactive Current-Month Calendar
           3) Master Project PDFs (Signed Contract, Architect Plans, Engineering Plans + City Permit #)
           ===================================================================== -->
      <section id="kp-page-1" class="kp-pane active">
        
        <!-- SECTION 1: PROJECT AMOUNT & BACKTRACKED RUNNING CAPITAL SPENT -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-section-top-row">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; min-width:0;">
              <span class="kp-badge-pill kp-badge-gold" id="p1-job-id-badge">KP-2026-001</span>
              <h2 id="p1-job-address-title" class="kp-section-h2">
                40484 Tantalus Rd, Squamish, BC &mdash; Project Amount &amp; Running Capital
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-white" id="p1-municipality-badge" onclick="promptEditMunicipalityAndPermit()" style="cursor:pointer;" title="Click to update Municipal Jurisdiction or Building Permit Number">
                District of Squamish &bull; Permit #BP2026-0419
              </span>
              <span class="kp-badge-pill kp-badge-gold" id="p1-contract-status-badge">&#10003; Contract Active</span>
            </div>
          </div>

          <!-- 4 Clean Financial KPI Cards (Strictly Gold, White & Black) -->
          <div class="kp-metric-grid">
            <div class="kp-metric-box kp-metric-box-gold" onclick="promptEditContractPrice()" style="cursor:pointer;" title="Click to adjust Baseline Project Amount">
              <div class="kp-metric-label">Total Project Amount</div>
              <div class="kp-metric-val" id="p1-kpi-revised-total" style="color:#d4af37;">$1,850,000</div>
              <div id="p1-kpi-base-sub" class="kp-metric-sub">Baseline <span id="p1-kpi-base-price" style="color:#ffffff;">$1,850,000</span> + Revisions <span id="p1-kpi-revisions-sum" style="color:#f3e5ab;">+$0</span></div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">Running Capital Spent to Date</div>
              <div class="kp-metric-val" id="p1-kpi-running-spent" style="color:#ffffff;">$846,500</div>
              <div id="p1-kpi-running-spent-sub" class="kp-metric-sub">44.9% of Project Spent &bull; Backtracked Stages 01&ndash;09</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">Remaining Capital Balance</div>
              <div class="kp-metric-val" id="p1-kpi-remaining-capital" style="color:#ffffff;">$1,038,000</div>
              <div id="p1-kpi-remaining-sub" class="kp-metric-sub">55.1% Remaining Capital to Completion</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">10% Statutory Lien Holdback</div>
              <div class="kp-metric-val" id="p1-kpi-holdback" style="color:#f3e5ab;">$84,650</div>
              <div id="p1-kpi-holdback-sub" class="kp-metric-sub">Retained on Spend ($188,450 Total Contract Holdback)</div>
            </div>
          </div>

          <!-- Hidden legacy IDs to prevent any null reference in helper functions -->
          <div style="display:none;">
            <span id="p1-job-subtitle"></span>
            <span id="p1-owner-name"></span>
            <span id="p1-owner-contact"></span>
            <span id="p1-owner-pass-hint"></span>
            <span id="p1-scope-summary-text"></span>
            <span id="p1-kpi-revisions-sub"></span>
            <span id="p1-builder-sig-display"></span>
            <span id="p1-builder-sig-meta"></span>
            <span id="p1-owner-sig-status-pill"></span>
            <div id="p1-owner-sig-preview-box"></div>
          </div>
        </div>


        <!-- SECTION 2: WHERE WE ARE SITTING (DAILY WRITE-UP PREVIEW) + INTERACTIVE CURRENT-MONTH CALENDAR -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-section-top-row" style="margin-bottom:0.85rem;">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-gold">WHERE WE ARE SITTING</span>
              <span class="kp-badge-pill kp-badge-white" id="p1-timeline-date-badge">October 2026 &bull; Click Any Date on Calendar to Preview Daily Write-Up</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <button type="button" onclick="switchPortalPage(2)" class="kp-secondary-btn kp-pill-sm">
                Full Schedule &amp; Calendar &rarr;
              </button>
              <button type="button" onclick="switchPortalPage(4)" class="kp-secondary-btn kp-pill-sm">
                All 30 Trades &rarr;
              </button>
            </div>
          </div>

          <!-- 2-Column Executive Layout: Left = Stage Completion + Selected Day Write-Up Preview | Right = Interactive Current-Month Calendar -->
          <div class="kp-where-we-sit-layout">
            <!-- Left: Active Stage Progress + Selected Calendar Day Write-Up Preview -->
            <div id="p1-active-stage-summary-panel" class="kp-active-stage-box">
              <!-- Populated dynamically by renderTab1Contract() & selectMiniCalDay() -->
            </div>

            <!-- Right: Interactive Current-Month Calendar (October 2026) -->
            <div id="p1-mini-month-calendar-panel" class="kp-mini-cal-box">
              <!-- Populated dynamically by renderTab1Contract() -->
            </div>
          </div>
        </div>


        <!-- SECTION 3: MASTER PROJECT PDF DOCUMENTS + CITY SUBMISSION & BUILDING PERMIT NUMBER -->
        <div class="kp-card kp-exec-section">
          <div class="kp-section-top-row" style="margin-bottom:0.9rem;">
            <div>
              <div class="kp-section-h2" style="font-size:1.05rem;">
                Master Project PDF Documents &amp; Municipal Permit Package
              </div>
              <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">
                Click any document below to open the full PDF on screen for inspection, printing, or download.
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-white" id="p1-pdf-district-badge" onclick="promptEditMunicipalityAndPermit()" style="cursor:pointer;" title="Click to edit Jurisdiction / Permit #">
                Submitted to: District of Squamish
              </span>
              <span class="kp-badge-pill kp-badge-gold" id="p1-pdf-permit-badge" onclick="openMasterPdfOnScreen('permit')" style="cursor:pointer;" title="Click to view Municipal Building Permit on screen">
                &#10003; City Building Permit #BP2026-0419
              </span>
            </div>
          </div>

          <!-- 3-Column Master PDF Cards Grid (100% contained, zero overflow) -->
          <div id="p1-master-pdfs-grid" class="kp-master-pdfs-grid">
            <!-- Rendered dynamically by JS:
                 1. Signed Prime Contract PDF
                 2. Architect Plans PDF (with District & Building Permit #)
                 3. Engineering Plans PDF (with District & Building Permit #) -->
          </div>
        </div>

      </section>


            <!-- =====================================================================
           TAB 2: 2. LIVE CALENDAR & TRADES
           Strictly White on Black — Top Full-Width Calendar + Active Date in Top Right
           + Underneath Box Listing Active Trades This Month & Percentage Done
           ===================================================================== -->
      <section id="kp-page-2" class="kp-pane">

        <!-- TOP BOX: FULL-WIDTH MONTHLY CALENDAR (White on Black, Active Date in Top-Right, No Prev/Next Buttons) -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-cal-header-bar">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <select id="cal-month-select" class="kp-cal-select" onchange="onCalendarSelectChange()">
                <option value="0">January</option>
                <option value="1">February</option>
                <option value="2">March</option>
                <option value="3">April</option>
                <option value="4">May</option>
                <option value="5">June</option>
                <option value="6">July</option>
                <option value="7">August</option>
                <option value="8">September</option>
                <option value="9" selected>October</option>
                <option value="10">November</option>
                <option value="11">December</option>
              </select>
              <select id="cal-year-select" class="kp-cal-select" onchange="onCalendarSelectChange()">
                <option value="2026" selected>2026</option>
                <option value="2027">2027</option>
              </select>
              <span style="font-size:0.76rem; color:#cbd5e1; font-weight:600;">
                Click any date to open daily write-up inputs, QA checkpoints, active trades &amp; file storage
              </span>
            </div>

            <!-- Top Right-Hand Corner: Active Date -->
            <div class="kp-cal-active-date-box" title="Active Build Date">
              <span class="kp-cal-active-date-label">Active Date:</span>
              <input
                type="date"
                id="p2-where-we-are-date"
                value="2026-10-15"
                onchange="updateWhereWeAreDate(this.value)"
                class="kp-cal-active-date-input"
              />
            </div>
          </div>

          <!-- 7-Day Calendar Grid (Strictly White on Black) -->
          <div class="kp-cal-grid">
            <div class="kp-cal-weekday">Sun</div>
            <div class="kp-cal-weekday">Mon</div>
            <div class="kp-cal-weekday">Tue</div>
            <div class="kp-cal-weekday">Wed</div>
            <div class="kp-cal-weekday">Thu</div>
            <div class="kp-cal-weekday">Fri</div>
            <div class="kp-cal-weekday">Sat</div>
          </div>
          <div class="kp-cal-grid" id="kp-calendar-days" style="margin-top:6px;">
            <!-- Populated dynamically by renderCalendar() -->
          </div>
        </div>

        <!-- UNDERNEATH BOX: ACTIVE TRADES THIS MONTH & PERCENTAGE DONE (Listed Out in White on Black) -->
        <div class="kp-card kp-exec-section" id="p2-monthly-active-trades-card">
          <div class="kp-section-top-row" style="margin-bottom:0.85rem;">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-white" id="p2-active-trades-month-badge">OCTOBER 2026</span>
              <h2 class="kp-section-h2" style="font-size:1.04rem;" id="p2-active-trades-heading">
                Active Trades This Month &amp; Completion Percentage
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="kp-badge-pill kp-badge-white" id="p2-active-trades-count">3 Active Trades</span>
            </div>
          </div>

          <div id="p2-active-trades-list" style="display:flex; flex-direction:column; gap:8px;">
            <!-- Populated dynamically by renderActiveTradeRadar() in crisp White on Black -->
          </div>

          <!-- Hidden legacy IDs to prevent any null errors in helper functions -->
          <div style="display:none;">
            <span id="p2-current-date-pill"></span>
            <span id="p2-current-stage-headline"></span>
            <div id="p2-progress-bar-fill"></div>
            <span id="p2-radar-date-label"></span>
            <div id="p2-stage-stepper-pills"></div>
            <div id="p2-upcoming-trades-list"></div>
          </div>
        </div>

      </section>


            <!-- =====================================================================
           TAB 3: 3. WARRANTY & INSPECTIONS
           Strictly Gold, White & Black — 3 Clean Executive Sections:
           1) 2-5-10 Year National Home Warranty (with PDF Download Inside Each Box)
           2) Architect • Engineer • City Approved Plans & Past Municipal Inspections
              (3 Clickable Box Sections -> Opens Categorized White-on-Black PDF Vault)
           3) Pre-Occupancy Final Walkthrough PDF Upload + Dual 2-5-10 Sign-Off & PDF at Bottom
           ===================================================================== -->
      <section id="kp-page-3" class="kp-pane">

        <!-- SECTION 1: 2-5-10 YEAR NATIONAL HOME WARRANTY (WITH PDF DOWNLOAD IN EACH BOX) -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-section-top-row" style="margin-bottom:0.9rem;">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-gold">BC HOUSING LICENSED BUILDER #52603</span>
              <span class="kp-badge-pill kp-badge-white" id="p3-warranty-policy-badge" onclick="promptEditWarrantyDetails()" style="cursor:pointer;" title="Click to edit Policy #">
                POLICY #NHW-2026-88421
              </span>
              <h2 class="kp-section-h2" style="font-size:1.06rem;">
                2&ndash;5&ndash;10 Year National Home Warranty Certificate Vault
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer;">
                Upload Warranty PDF
                <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleWarrantyPdfUpload(event)" />
              </label>
              <button type="button" onclick="openWarrantyTierPdfOnScreen('master')" class="kp-secondary-btn kp-pill-sm">
                Open Master 2-5-10 PDF
              </button>
              <button type="button" onclick="downloadWarrantyCertificatePdf()" class="kp-secondary-btn kp-pill-sm">
                Download 2-5-10 PDF
              </button>
            </div>
          </div>

          <!-- 3 Warranty Tier Boxes (Each Box Has Its Own PDF Open & Download Inside) -->
          <div class="kp-master-pdfs-grid" id="p3-warranty-tiers-grid" style="margin-bottom:0.85rem;">
            <!-- Populated dynamically by renderWarrantyAndPlansTab() -->
          </div>

          <!-- Clean Bottom Meta Bar for Warranty Provider & Active Policy -->
          <div id="p3-warranty-meta-bar" style="background:#0b0f17; border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:9px 14px; font-size:0.76rem; color:#cbd5e1; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <!-- Populated by JS -->
          </div>
        </div>


        <!-- SECTION 2: ARCHITECT • ENGINEER • CITY APPROVED PLANS & PAST MUNICIPAL INSPECTIONS -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-section-top-row" style="margin-bottom:0.9rem;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">ARCHITECT &bull; ENGINEER &bull; CITY PLANS &amp; INSPECTIONS</span>
                <span class="kp-badge-pill kp-badge-white" id="p3-plans-permit-badge">Permit #BP2026-0419</span>
              </div>
              <h2 class="kp-section-h2" style="font-size:1.05rem; margin-top:5px !important;">
                Master Plans &amp; Municipal Inspections Breakdown
              </h2>
            </div>
            <div style="font-size:0.75rem; color:#cbd5e1; font-weight:600;">
              Click any of the 3 boxes below to open its categorized PDF files &amp; past inspection reports
            </div>
          </div>

          <!-- 3 Clickable Box Sections: 1) Architect, 2) Engineer, 3) City Approved Plans & Past Inspections -->
          <div class="kp-master-pdfs-grid" id="p3-plan-disciplines-grid" style="margin-bottom:0.95rem;">
            <!-- Rendered by JS -->
          </div>

          <!-- Full-Width White-on-Black Overlay Box Showing Categorized PDFs for the Clicked Section -->
          <div id="p3-discipline-files-drawer" style="background:#05070b; border:1px solid rgba(255,255,255,0.22); border-radius:12px; padding:14px 16px;">
            <!-- Rendered dynamically by renderDisciplineFilesVault() in crisp White on Black -->
          </div>
        </div>


        <!-- SECTION 3: PRE-OCCUPANCY FINAL WALKTHROUGH CERTIFICATE & DUAL 2-5-10 SIGN-OFF -->
        <div class="kp-card kp-exec-section">
          <div class="kp-section-top-row" style="margin-bottom:0.9rem;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">PRE-OCCUPANCY STATION</span>
                <span class="kp-badge-pill kp-badge-white" id="p3-walkthrough-status-pill">Certificate &amp; Dual Sign-Off</span>
              </div>
              <h2 class="kp-section-h2" style="font-size:1.05rem; margin-top:5px !important;">
                Final Walkthrough Certificate &amp; 2&ndash;5&ndash;10 Warranty Dual Sign-Off
              </h2>
            </div>

            <!-- Single Clean Upload Button for Final Walkthrough PDF -->
            <div>
              <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer;">
                Upload Final Walkthrough PDF
                <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleWalkthroughPdfUpload(event)" />
              </label>
            </div>
          </div>

          <!-- Dual Sign-Off Row (Builder + Property Owner Sign-Off for 2-5-10 & Final Walkthrough) -->
          <div style="display:grid; grid-template-columns:minmax(0, 1fr) minmax(0, 1fr) auto; gap:12px; align-items:center; background:#0b0f17; border:1px solid rgba(255,255,255,0.16); border-radius:12px; padding:13px 16px; margin-bottom:0.85rem;">
            <div style="min-width:0;">
              <div style="font-size:0.66rem; font-weight:800; color:#d4af37; text-transform:uppercase; letter-spacing:0.06em;">1. Licensed Builder Sign-Off (2-5-10 Warranty)</div>
              <div style="font-size:0.86rem; font-weight:900; color:#ffffff; margin-top:2px;">Wayne Stevenson &mdash; BC Builder #52603</div>
              <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">Keystone Possibilities Ltd. &bull; Signed &amp; Certified</div>
            </div>

            <div style="min-width:0;">
              <div style="font-size:0.66rem; font-weight:800; color:#d4af37; text-transform:uppercase; letter-spacing:0.06em;">2. Property Owner Co-Sign-Off (2-5-10 Warranty)</div>
              <div id="p3-owner-signoff-name" style="font-size:0.86rem; font-weight:900; color:#ffffff; margin-top:2px;">David &amp; Sarah Kensington</div>
              <div id="p3-walkthrough-signoff-status" style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">Ready for Final Walkthrough &amp; 2-5-10 Co-Sign-Off</div>
            </div>

            <div>
              <button type="button" onclick="signOffFinalWalkthrough()" class="kp-gold-btn" id="p3-btn-dual-signoff">
                Sign Off 2-5-10 &amp; Final Walkthrough (Both Parties)
              </button>
            </div>
          </div>

          <!-- Bottom PDF File Bar: Final Walkthrough & Signed 2-5-10 Certificate PDF -->
          <div id="p3-bottom-walkthrough-pdf-bar" style="background:#05070b; border:1px solid rgba(212,175,55,0.38); border-radius:10px; padding:11px 15px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <!-- Populated dynamically by renderWarrantyAndPlansTab() -->
          </div>

          <!-- Hidden legacy IDs to prevent any null reference in helper functions -->
          <div style="display:none;">
            <div id="p3-cad-viewer-wrapper"></div>
            <tbody id="p3-inspections-tbody"></tbody>
            <div id="p3-walkthrough-grid"></div>
          </div>
        </div>

      </section>


            <!-- =====================================================================
           TAB 4: 4. MASTER TRADES BREAKDOWN
           Strictly Gold, White & Black —
           - Top: + Add Custom Trade + Export Trade Schedule (Updated CSV & PDF)
           - Money Breakdown of Where We Are Sitting (4 Cards in Gold, White & Black)
           - Clean Master List of All 22 Start-to-Finish Trades (From Architect to Final Occupancy):
             Just Trade Name + Date Active From When to When
           - Click Any Trade -> Opens Dedicated 3-Section Trade Page:
             1) Trade Contract, Date & Owner Signature (Open, Print, Download, Upload, Sign)
             2) Trade Timeline & Where They Are Sitting (Dates, % Complete, Billed, Status)
             3) Trade Change Orders (Made, Accepted & Put In)
           ===================================================================== -->
      <section id="kp-page-4" class="kp-pane">

        <div class="kp-card kp-exec-section">
          <!-- Top Header & Action Buttons (+ Add Custom Trade & Updated Export Trade Schedule) -->
          <div class="kp-section-top-row" style="margin-bottom:0.95rem;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">ARCHITECT TO FINAL OCCUPANCY &bull; 30 STAGES</span>
                <span class="kp-badge-pill kp-badge-white" id="p4-trades-count-badge">30 Start-to-Finish Scopes</span>
              </div>
              <h2 class="kp-section-h2" style="font-size:1.06rem; margin-top:5px !important;">
                Master Start-to-Finish BC Trades Breakdown
              </h2>
            </div>

            <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
              <button type="button" onclick="toggleAddCustomTradeDrawer()" class="kp-gold-btn kp-pill-sm">
                + Add Custom Trade
              </button>
              <button type="button" onclick="exportTradesSummary()" class="kp-secondary-btn kp-pill-sm">
                Export Trade Schedule (CSV)
              </button>
              <button type="button" onclick="exportTradesSchedulePdf()" class="kp-secondary-btn kp-pill-sm">
                Export Trade Schedule (PDF)
              </button>
            </div>
          </div>

          <!-- Inline Add Custom Trade Drawer (Hidden Until + Add Custom Trade Clicked) -->
          <div id="p4-add-custom-trade-drawer" style="display:none; background:#0b0f17; border:1px solid #d4af37; border-radius:12px; padding:14px 16px; margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span class="kp-badge-pill kp-badge-gold">+ ADD NEW CUSTOM TRADE SCOPE</span>
              <button type="button" onclick="toggleAddCustomTradeDrawer(false)" class="kp-secondary-btn kp-pill-sm">Cancel</button>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(175px, 1fr)); gap:10px; align-items:end;">
              <div>
                <label class="kp-form-label" style="color:#ffffff;">Trade Discipline &amp; Name</label>
                <input type="text" id="p4-new-trade-name" class="kp-form-input" placeholder="e.g. Custom Timber Pergola &amp; Decking" />
              </div>
              <div>
                <label class="kp-form-label" style="color:#ffffff;">Subcontractor Company</label>
                <input type="text" id="p4-new-trade-sub" class="kp-form-input" placeholder="e.g. Squamish Timber Craft Ltd." />
              </div>
              <div>
                <label class="kp-form-label" style="color:#ffffff;">Date Active From</label>
                <input type="date" id="p4-new-trade-start" class="kp-form-input" value="2026-10-19" style="color-scheme:dark;" />
              </div>
              <div>
                <label class="kp-form-label" style="color:#ffffff;">Date Active To</label>
                <input type="date" id="p4-new-trade-end" class="kp-form-input" value="2026-11-02" style="color-scheme:dark;" />
              </div>
              <div>
                <label class="kp-form-label" style="color:#ffffff;">Contract Amount ($ CAD)</label>
                <input type="number" id="p4-new-trade-amount" class="kp-form-input" value="0" />
              </div>
              <div>
                <button type="button" onclick="saveNewCustomTradeInline()" class="kp-gold-btn" style="width:100%; justify-content:center;">
                  Save &amp; Add Trade
                </button>
              </div>
            </div>
          </div>

          <!-- 4-Card Money Breakdown ("Where We Are Sitting" — Strictly Gold, White & Black) -->
          <div class="kp-metric-grid" style="margin-bottom:1.1rem;">
            <div class="kp-metric-box">
              <div class="kp-metric-label">Total Trade Subcontracts</div>
              <div class="kp-metric-val" id="p4-kpi-total-contracts" style="color:#ffffff;">$1,875,000</div>
              <div class="kp-metric-sub" id="p4-kpi-contracts-sub">30 Architect-to-Finish BC Scopes</div>
            </div>
            <div class="kp-metric-box kp-metric-box-gold">
              <div class="kp-metric-label" style="color:#f3e5ab;">Invoiced &amp; Certified To Date</div>
              <div class="kp-metric-val" id="p4-kpi-total-billed" style="color:#d4af37;">$830,500</div>
              <div class="kp-metric-sub" style="color:#f3e5ab;">Verified Trade Progress Draws</div>
            </div>
            <div class="kp-metric-box">
              <div class="kp-metric-label">10% Lien Holdback Retained</div>
              <div class="kp-metric-val" id="p4-kpi-total-holdback" style="color:#ffffff;">$83,050</div>
              <div class="kp-metric-sub">Sec. 5 Builders Lien Act Escrow</div>
            </div>
            <div class="kp-metric-box">
              <div class="kp-metric-label">Accepted Change Orders</div>
              <div class="kp-metric-val" id="p4-kpi-revisions" style="color:#d4af37;">$0</div>
              <div class="kp-metric-sub" id="p4-kpi-revisions-sub">Synced with Owner Contract</div>
            </div>
          </div>

          <!-- VIEW 1: CLEAN MASTER LIST OF ALL 22+ TRADES (Trade Name + Date Active From -> To) -->
          <div id="p4-master-trades-list-view">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:9px; padding:0 4px;">
              <div style="font-size:0.74rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">
                Click any of the 30 stages below to open its <span style="color:#ffffff;">1. Trades &amp; Contracts</span> &bull; <span style="color:#ffffff;">2. Invoices &amp; Paid Invoices</span> &bull; <span style="color:#ffffff;">3. Change Orders</span> &bull; <span style="color:#ffffff;">4. Geotagged Permits</span>
              </div>
              <div style="font-size:0.72rem; color:#d4af37; font-weight:800;">
                Scoped from Stage 01 (Architect &amp; Permits) to Stage 30 (Final Occupancy)
              </div>
            </div>

            <div id="p4-master-trades-list" style="display:flex; flex-direction:column; gap:7px;">
              <!-- Populated dynamically by renderTradesList() -->
            </div>
          </div>

          <!-- VIEW 2: CLICKED TRADE DEDICATED 3-SECTION PAGE (1. Contract & Sign-Off, 2. Timeline & Where Sitting, 3. Change Orders) -->
          <div id="p4-trade-detail-view" style="display:none;">
            <!-- Populated dynamically by renderSelectedTrade3SectionPage() -->
          </div>

          <!-- Hidden legacy tbody so old helpers never throw null errors -->
          <table style="display:none;"><tbody id="kp-trades-tbody"></tbody></table>
        </div>

      </section>


            <!-- =====================================================================
           TAB 5: 5. MATERIAL & FRAMING
           Strictly Gold, White & Black —
           - Small Active Plans Bar at the Top
           - One Clean Box for Each of the 7 Material Sections:
             1. Civil | 2. Excavation | 3. Concrete | 4. Framing | 5. Roofing | 6. Siding | 7. Finishing
           - Scrollable Single-Line List Inside Each Box (Newest at the Top):
             * Click the Material List -> Opens the PDF of JUST the List of Materials Needed
             * Click Paid / Not Paid beside it -> Opens the Invoice PDF (Paid Status, Date Paid & Cost + 10%)
           ===================================================================== -->
      <section id="kp-page-5" class="kp-pane">

        <div class="kp-card kp-exec-section">

          <!-- SMALL ACTIVE PLANS BAR AT THE TOP -->
          <div id="p5-active-plans-small-bar" style="background:#0b0f17; border:1px solid rgba(212,175,55,0.42); border-radius:12px; padding:9px 14px; margin-bottom:0.95rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div style="display:flex; align-items:center; gap:9px; min-width:0; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-gold">ACTIVE PLANS</span>
              <span id="p5-plan-pdf-badge" style="font-size:0.84rem; font-weight:800; color:#ffffff;">
                KP-2026-001_Framing_Takeoff_Blueprint_Set.pdf
              </span>
              <span id="p5-plan-pdf-meta" style="font-size:0.73rem; color:#cbd5e1;">
                &bull; Permit #BP2026-0419
              </span>
            </div>

            <div style="display:flex; gap:7px; align-items:center; flex-wrap:wrap;">
              <button type="button" onclick="openActivePlanTakeoffPdfOnScreen()" class="kp-gold-btn kp-pill-sm">
                Open Active Plans PDF
              </button>
              <label class="kp-secondary-btn kp-pill-sm" style="cursor:pointer; margin:0;">
                Upload Plan PDF
                <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleTakeoffPlanPdfUpload(event)" />
              </label>
              <button type="button" id="p5-btn-cost-plus-toggle" onclick="toggleP5CostPlusMode()" class="kp-secondary-btn kp-pill-sm" title="Toggle Builder 10% Plus Cost on Invoices">
                10% Plus Cost: ON &#10003;
              </button>
              <button type="button" onclick="promptAddCustomMaterialSection()" class="kp-secondary-btn kp-pill-sm">
                + Add Section
              </button>
            </div>
          </div>

          <!-- 7 SECTION BOXES (CIVIL, EXCAVATION, CONCRETE, FRAMING, ROOFING, SIDING, FINISHING) -->
          <div id="kp-material-accordions" style="display:flex; flex-direction:column; gap:11px;">
            <!-- Populated dynamically by renderMaterialsList() -->
          </div>

          <!-- Hidden legacy IDs to prevent any null errors -->
          <div style="display:none;">
            <div id="mat-total-budget"></div>
            <div id="mat-total-actual"></div>
            <div id="mat-total-var"></div>
            <div id="p5-uploaded-plan-bar"></div>
            <tbody id="p5-suggested-takeoff-tbody"></tbody>
          </div>

        </div>

      </section>


            <!-- =====================================================================
           TAB 6: 6. MASTER FINANCIALS & PDFS (HIGHLAND MULTIPLEX MASTER LEDGER)
           Strictly Gold, White & Black —
           - Top 2 Job/Passcode Portals Removed
           - Top: Keystone Master Money Breakdown (4-Card Executive Summary)
           - Middle: 5 Live-Updated PDF & Financial Sections:
             1. Trades | 2. Materials | 3. City | 4. Architect | 5. Engineer
           - Bottom: Highland Master Tally (Total Paid, Total Unpaid & How Much We Are At)
           ===================================================================== -->
      <section id="kp-page-6" class="kp-pane">

        <div class="kp-card kp-exec-section">

          <!-- TOP HEADER: HIGHLAND MULTIPLEX MASTER FINANCIALS & LIVE PDF ROLLUP -->
          <div class="kp-section-top-row" style="margin-bottom:0.95rem;">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; min-width:0;">
              <span class="kp-badge-pill kp-badge-gold" id="p6-highland-badge">HIGHLAND MULTIPLEX &bull; KP-2026-001</span>
              <h2 class="kp-section-h2" id="p6-master-title">
                40484 Tantalus Rd, Squamish, BC &mdash; Keystone Master Financial &amp; PDF Breakdown
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap;">
              <button type="button" onclick="promptAddMasterFinancialEntry()" class="kp-gold-btn kp-pill-sm">
                + Add Financial / PDF Entry
              </button>
              <button type="button" onclick="exportPortalBankDrawHoldbackPdf()" class="kp-gold-btn kp-pill-sm" id="btn-p6-export-holdback-pdf" style="display:none !important;">
                📄 Export 10% Lien Holdback &amp; Bank Draw PDF
              </button>
              <button type="button" onclick="exportHighlandMasterFinancialPdf()" class="kp-secondary-btn kp-pill-sm">
                Download Master Financial PDF
              </button>
            </div>
          </div>

          <!-- TOP 4-CARD KEYSTONE MASTER BREAKDOWN (WHERE WE ARE WITH MONEY) -->
          <div class="kp-metric-grid" style="margin-bottom:1.15rem;">
            <div class="kp-metric-box">
              <div class="kp-metric-label">Revised Project Contract</div>
              <div class="kp-metric-val" id="p6-kpi-contract-total" style="color:#ffffff;">$1,850,000</div>
              <div class="kp-metric-sub" id="p6-kpi-contract-sub">Baseline $1,850,000 + Revisions +$0</div>
            </div>

            <div class="kp-metric-box kp-metric-box-gold">
              <div class="kp-metric-label" style="color:#f3e5ab;">Total Paid to Date (All PDFs)</div>
              <div class="kp-metric-val" id="p6-kpi-paid-total" style="color:#d4af37;">$1,039,550</div>
              <div class="kp-metric-sub" id="p6-kpi-paid-sub" style="color:#f3e5ab;">Verified Paid Across All 5 Sections</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">Total Unpaid / Pending PDFs</div>
              <div class="kp-metric-val" id="p6-kpi-unpaid-total" style="color:#ffffff;">$141,660</div>
              <div class="kp-metric-sub" id="p6-kpi-unpaid-sub">Active &amp; Upcoming Unpaid Invoices</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">Where We Are Sitting &amp; Remaining</div>
              <div class="kp-metric-val" id="p6-kpi-where-we-sit" style="color:#f3e5ab;">$1,181,210</div>
              <div class="kp-metric-sub" id="p6-kpi-remaining-sub">$703,290 Remaining Unspent Contract Float</div>
            </div>
          </div>

          <!-- 10% STATUTORY BUILDERS LIEN HOLDBACK TRUST & CCDC 5B SUMMARY BAR -->
          <div id="p6-statutory-holdback-bar" style="display:none !important; display:none !important; display:none !important; background:linear-gradient(180deg, rgba(212,175,55,0.10) 0%, #0b0f17 100%); border:1px solid rgba(212,175,55,0.48); border-radius:14px; padding:13px 16px; margin-bottom:1.15rem; display:flex; flex-direction:column; gap:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px;">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">BC BUILDERS LIEN ACT (SBC 1997 c.45 SEC. 5)</span>
                <span class="kp-badge-pill kp-badge-white">CCDC 5B CONSTRUCTION MANAGEMENT</span>
                <span style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:0.94rem; font-weight:900; color:#ffffff;">
                  10% Statutory Lien Holdback Trust &amp; Bank Draw Certification
                </span>
              </div>
              <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap;">
                <button type="button" onclick="exportPortalBankDrawHoldbackPdf()" class="kp-gold-btn kp-pill-sm">
                  📄 Open &amp; Print 10% Lien Holdback Certificate
                </button>
                <button type="button" onclick="switchPortalPage(4)" class="kp-secondary-btn kp-pill-sm">
                  3. Master Trade Breakdown (30 Stages) &rarr;
                </button>
              </div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:10px;">
              <div style="background:#05070b; border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:9px 12px;">
                <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">Gross Certified Invoiced</div>
                <div id="p6-holdback-gross-val" style="font-size:1.16rem; font-weight:900; color:#ffffff; margin-top:2px;">$1,039,550</div>
                <div style="font-size:0.68rem; color:#94a3b8;">100% Verified Progress Draws</div>
              </div>
              <div style="background:#05070b; border:1px solid rgba(212,175,55,0.45); border-radius:10px; padding:9px 12px;">
                <div style="font-size:0.65rem; font-weight:800; color:#f3e5ab; text-transform:uppercase; letter-spacing:0.06em;">10% Statutory Holdback Retained</div>
                <div id="p6-holdback-10pct-val" style="font-size:1.16rem; font-weight:900; color:#d4af37; margin-top:2px;">$103,955</div>
                <div style="font-size:0.68rem; color:#f3e5ab;">Held in Statutory Lien Trust Account</div>
              </div>
              <div style="background:#05070b; border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:9px 12px;">
                <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">90% Net Payable Disbursed</div>
                <div id="p6-holdback-net90-val" style="font-size:1.16rem; font-weight:900; color:#ffffff; margin-top:2px;">$935,595</div>
                <div style="font-size:0.68rem; color:#94a3b8;">Invariant: 90% Net + 10% Holdback = 100%</div>
              </div>
              <div style="background:#05070b; border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:9px 12px;">
                <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">CCDC 5B CM Fee &amp; Release Gate</div>
                <div id="p6-holdback-cmfee-val" style="font-size:1.16rem; font-weight:900; color:#f3e5ab; margin-top:2px;">$129,944 (12.5%)</div>
                <div style="font-size:0.68rem; color:#94a3b8;">55-Day Post-Completion Lien Release</div>
              </div>
            </div>
          </div>

          <!-- 5 LIVE-SYNCED PDF & FINANCIAL SECTIONS:
               1. TRADES | 2. MATERIALS | 3. CITY | 4. ARCHITECT | 5. ENGINEER -->
          <div id="p6-five-sections-container" style="display:flex; flex-direction:column; gap:12px; margin-bottom:1.25rem;">
            <!-- Populated dynamically by renderTab6JobManager() -->
          </div>

          <!-- BOTTOM: HIGHLAND MASTER TALLY (PAID, UNPAID & HOW MUCH WE ARE AT) -->
          <div id="p6-bottom-master-tally-box" style="background:#05070b; border:1.5px solid #d4af37; border-radius:14px; padding:16px 18px; box-shadow:0 12px 32px rgba(0,0,0,0.85);">
            <!-- Populated dynamically by renderTab6JobManager() -->
          </div>

          <!-- Hidden legacy IDs to prevent any null errors in legacy helpers -->
          <div style="display:none;">
            <div id="p6-jobs-registry-list"></div>
            <div id="p6-sync-status-text"></div>
            <input type="text" id="p6-edit-address" />
            <input type="text" id="p6-edit-job-id" />
            <input type="text" id="p6-edit-municipality" />
            <input type="text" id="p6-edit-owner-name" />
            <input type="text" id="p6-edit-owner-phone" />
            <input type="text" id="p6-edit-owner-email" />
            <input type="number" id="p6-edit-contract-price" />
            <input type="text" id="p6-edit-owner-passcode" />
            <table><tbody id="kp-ledger-tbody"></tbody></table>
          </div>

        </div>

      </section>

      <!-- =====================================================================
           TAB 7: 7. 30-STAGE, GEOTECH & ENG
           Strictly Gold, White & Black Luxury Executive Theme —
           - Top 4-Card Executive Summary (30-Stage Progress, 6-Discipline P.Eng & Geotech, BCBC Letters of Assurance, 10% Lien Holdback Trust)
           - Section 1: 6-Discipline P.Eng (Geotechnical, Structural, Civil ES54, Mechanical Step Code 4, Electrical 400A/EVEMS, Building Envelope)
                        + BCBC 2024 Letters of Assurance (Schedule A, Schedule B, Schedule C-A, Schedule C-B)
                        + Interactive Side-by-Side Blueprint Revision Diff (Permit Rev 2 vs IFC Rev 4)
           - Section 2: Complete 30-Stage Start-to-Finish House & Multiplex Checklist (STAGE 01 to STAGE 30 across Phases I–VI)
                        with Phase Filter Pills, Status Toggles, Auto-Notify Next Trade (DAG Mobilization) & 10% Lien Bank Draw PDF
           ===================================================================== -->
      <section id="kp-page-7" class="kp-pane" style="display:none !important;">

        <!-- TOP EXECUTIVE SUMMARY CARD -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-section-top-row">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; min-width:0;">
              <span class="kp-badge-pill kp-badge-gold" id="p7-job-id-badge">KP-2026-001 &bull; BC BUILDER #52603</span>
              <h2 class="kp-section-h2" id="p7-master-title">
                40484 Tantalus Rd, Squamish, BC &mdash; 30-Stage Construction, Geotech &amp; 6-Discipline Engineering
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap;">
              <button type="button" onclick="triggerPortalNextTradeNotification()" class="kp-gold-btn kp-pill-sm" id="btn-p7-notify-next-trade">
                📨 Auto-Notify Next Trade (DAG Mobilization)
              </button>
              <button type="button" onclick="exportPortalBankDrawHoldbackPdf()" class="kp-gold-btn kp-pill-sm" id="btn-p7-export-draw-pdf">
                📄 Export 10% Lien &amp; Bank Draw PDF
              </button>
              <button type="button" onclick="syncPortalFromDaemonV10Jobs(false)" class="kp-secondary-btn kp-pill-sm" id="btn-p7-live-sync">
                Sync Cloud Vault
              </button>
            </div>
          </div>

          <!-- Top 4-Card Executive Summary -->
          <div class="kp-metric-grid">
            <div class="kp-metric-box kp-metric-box-gold">
              <div class="kp-metric-label" style="color:#f3e5ab;">30-Stage Master Progress</div>
              <div class="kp-metric-val" id="p7-kpi-stages-progress" style="color:#d4af37;">12 / 30 Completed</div>
              <div class="kp-metric-sub" id="p7-kpi-stages-sub" style="color:#f3e5ab;">Stage 13 Active &bull; Rough Framing &amp; Dick's Lumber #52603 Trusses</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">6-Discipline P.Eng &amp; Geotech</div>
              <div class="kp-metric-val" id="p7-kpi-peng-val" style="color:#ffffff;">6 / 6 Sealed</div>
              <div class="kp-metric-sub" id="p7-kpi-peng-sub">Geotech, Struct, Civil ES54, Mech, Elec, Envelope Sealed</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">BCBC 2024 Letters of Assurance</div>
              <div class="kp-metric-val" id="p7-kpi-loa-val" style="color:#ffffff;">Schedules A &amp; B Filed</div>
              <div class="kp-metric-sub" id="p7-kpi-loa-sub">Schedules A &amp; B Active &bull; C-A / C-B Pre-Occupancy</div>
            </div>

            <div class="kp-metric-box">
              <div class="kp-metric-label">10% Builders Lien Holdback Trust</div>
              <div class="kp-metric-val" id="p7-kpi-holdback-val" style="color:#f3e5ab;">$103,955 Retained</div>
              <div class="kp-metric-sub" id="p7-kpi-holdback-sub">SBC 1997 c.45 Statutory Escrow Active (10.0% Holdback)</div>
            </div>
          </div>
        </div>


        <!-- SECTION 1: 6-DISCIPLINE P.ENG, GEOTECHNICAL & BCBC LETTERS OF ASSURANCE + PLAN REVISION DIFF -->
        <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem;">
          <div class="kp-section-top-row" style="margin-bottom:0.9rem;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">6-DISCIPLINE P.ENG &amp; GEOTECHNICAL VAULT</span>
                <span class="kp-badge-pill kp-badge-white">BCBC 2024 SCHEDULES A &bull; B &bull; C-A &bull; C-B</span>
              </div>
              <h2 class="kp-section-h2" style="font-size:1.06rem; margin-top:5px !important;">
                Geotechnical P.Eng, 6-Discipline Sealed Engineering &amp; BCBC Letters of Assurance
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <button type="button" onclick="togglePortalPlanRevisionDiff()" class="kp-gold-btn kp-pill-sm" id="btn-p7-compare-revs">
                🔍 Compare Plan Revisions (Permit Rev 2 vs IFC Rev 4)
              </button>
              <button type="button" onclick="openGeotechAndLoaSummaryPdf()" class="kp-secondary-btn kp-pill-sm">
                📄 Open Geotech &amp; LOA Package PDF
              </button>
            </div>
          </div>

          <!-- 6-Discipline P.Eng Grid (Geotechnical, Structural, Civil ES54, Mechanical, Electrical, Building Envelope) -->
          <div id="p7-peng-disciplines-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(295px, 1fr)); gap:11px; margin-bottom:1rem;">
            <div style="background:#0b0f17; border:1px solid #d4af37; border-radius:12px; padding:13px 15px;">
              <span class="kp-badge-pill kp-badge-gold">1. GEOTECHNICAL P.ENG</span>
              <div style="font-weight:900; color:#ffffff; margin-top:4px;">Geotechnical Engineering — Bedrock Anchors, Shoring, Subgrade &amp; Bearing Capacity (Thurber Geotechnical P.Eng.)</div>
            </div>
            <div style="background:#0b0f17; border:1px solid rgba(212,175,55,0.34); border-radius:12px; padding:13px 15px;">
              <span class="kp-badge-pill kp-badge-gold">2. STRUCTURAL P.ENG</span>
              <div style="font-weight:900; color:#ffffff; margin-top:4px;">Structural P.Eng — 35 MPa Concrete, Simpson ATS Tie-Downs &amp; #52603 Roof Trusses (Apex Structural P.Eng.)</div>
            </div>
            <div style="background:#0b0f17; border:1px solid rgba(212,175,55,0.34); border-radius:12px; padding:13px 15px;">
              <span class="kp-badge-pill kp-badge-gold">3. CIVIL &amp; ES54 P.ENG</span>
              <div style="font-weight:900; color:#ffffff; margin-top:4px;">Civil &amp; BC Hydro ES54 Underground P.Eng — Stormwater Detention &amp; Municipal Mains</div>
            </div>
            <div style="background:#0b0f17; border:1px solid rgba(212,175,55,0.34); border-radius:12px; padding:13px 15px;">
              <span class="kp-badge-pill kp-badge-gold">4. MECHANICAL P.ENG</span>
              <div style="font-weight:900; color:#ffffff; margin-top:4px;">Mechanical / HVAC Step Code 4 P.Eng — Cold-Climate Heat Pumps, Zehnder HRV &amp; Hydronics</div>
            </div>
            <div style="background:#0b0f17; border:1px solid rgba(212,175,55,0.34); border-radius:12px; padding:13px 15px;">
              <span class="kp-badge-pill kp-badge-gold">5. ELECTRICAL P.ENG</span>
              <div style="font-weight:900; color:#ffffff; margin-top:4px;">Electrical 400A / EVEMS P.Eng — Primary Underground Service &amp; Multi-Unit Metering</div>
            </div>
            <div style="background:#0b0f17; border:1px solid rgba(212,175,55,0.34); border-radius:12px; padding:13px 15px;">
              <span class="kp-badge-pill kp-badge-gold">6. BUILDING ENVELOPE P.ENG</span>
              <div style="font-weight:900; color:#ffffff; margin-top:4px;">Building Envelope P.Eng — Rainscreen WRB, Exterior Rockwool, Mid-Blower Door &amp; NFPA 13D</div>
            </div>
          </div>

          <!-- BCBC 2024 Letters of Assurance (Schedule A, Schedule B, Schedule C-A, Schedule C-B) -->
          <div id="p7-loa-schedules-bar" style="background:#0b0f17; border:1px solid rgba(212,175,55,0.42); border-radius:12px; padding:12px 15px; margin-bottom:0.95rem;">
            <span class="kp-badge-pill kp-badge-gold">Schedule A</span>
            <span class="kp-badge-pill kp-badge-gold">Schedule B</span>
            <span class="kp-badge-pill kp-badge-white">Schedule C-A</span>
            <span class="kp-badge-pill kp-badge-white">Schedule C-B</span>
          </div>

          <!-- Side-by-Side Blueprint Revision Diff Drawer (Permit Rev 2 vs IFC Rev 4) -->
          <div id="p7-plan-revision-diff-drawer" style="display:block; background:#05070b; border:1px solid rgba(212,175,55,0.45); border-radius:12px; padding:14px 16px;">
            <span class="kp-badge-pill kp-badge-gold">Permit Rev 2 vs IFC Rev 4</span>
            <span style="font-size:0.78rem; color:#cbd5e1; margin-left:8px;">Sheets A-101, A-201, S-101, S-202, C-101, M-101, E-101 Side-by-Side Blueprint Revision Comparison</span>
          </div>
        </div>


        <!-- SECTION 2: COMPLETE 30-STAGE START-TO-FINISH HOUSE & MULTIPLEX CHECKLIST (ST-01 TO ST-30 ACROSS PHASES I–VI) -->
        <div class="kp-card kp-exec-section">
          <div class="kp-section-top-row" style="margin-bottom:0.85rem;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">PHASES I&ndash;VI &bull; 30 CANONICAL STAGES (ST-01 TO ST-30)</span>
                <span class="kp-badge-pill kp-badge-white" id="p7-stages-filter-count-badge">Showing All 30 Start-to-Finish Stages</span>
              </div>
              <h2 class="kp-section-h2" style="font-size:1.06rem; margin-top:5px !important;">
                Complete 30-Stage Start-to-Finish House &amp; Multiplex Execution Checklist
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap;">
              <button type="button" onclick="triggerPortalNextTradeNotification()" class="kp-gold-btn kp-pill-sm">
                📨 Auto-Notify Next Trade (DAG Mobilization)
              </button>
              <button type="button" onclick="exportPortalBankDrawHoldbackPdf()" class="kp-secondary-btn kp-pill-sm">
                📄 Export 10% Lien &amp; Bank Draw PDF
              </button>
            </div>
          </div>

          <!-- Phase Filter Pills (Phases I to VI) -->
          <div id="p7-phase-filter-bar" style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:0.95rem; background:#0b0f17; border:1px solid rgba(255,255,255,0.12); border-radius:12px; padding:8px 12px;">
            <button type="button" onclick="filterTab7StagesByPhase(0)" class="kp-gold-btn kp-pill-sm p7-phase-pill" data-phase="0">
              All 30 Stages (01&ndash;30)
            </button>
            <button type="button" onclick="filterTab7StagesByPhase(1)" class="kp-secondary-btn kp-pill-sm p7-phase-pill" data-phase="1">
              Phase I: Survey, Arch, Geotech &amp; Permits (01&ndash;05)
            </button>
            <button type="button" onclick="filterTab7StagesByPhase(2)" class="kp-secondary-btn kp-pill-sm p7-phase-pill" data-phase="2">
              Phase II: Excavation, Geotech Shoring, Civil &amp; Concrete (06&ndash;11)
            </button>
            <button type="button" onclick="filterTab7StagesByPhase(3)" class="kp-secondary-btn kp-pill-sm p7-phase-pill" data-phase="3">
              Phase III: Steel, Framing #52603, Roof &amp; Envelope (12&ndash;16)
            </button>
            <button type="button" onclick="filterTab7StagesByPhase(4)" class="kp-secondary-btn kp-pill-sm p7-phase-pill" data-phase="4">
              Phase IV: MEP, Fire Sprinklers, Acoustic &amp; Drywall (17&ndash;22)
            </button>
            <button type="button" onclick="filterTab7StagesByPhase(5)" class="kp-secondary-btn kp-pill-sm p7-phase-pill" data-phase="5">
              Phase V: Cladding, Millwork, Tile &amp; Commissioning (23&ndash;28)
            </button>
            <button type="button" onclick="filterTab7StagesByPhase(6)" class="kp-secondary-btn kp-pill-sm p7-phase-pill" data-phase="6">
              Phase VI: Civil Hardscape, C-A/C-B &amp; Occupancy (29&ndash;30)
            </button>
          </div>

          <!-- Active DAG Predecessor & Mobilization Status Banner -->
          <div id="p7-dag-mobilization-banner" style="background:linear-gradient(90deg, rgba(212,175,55,0.12) 0%, #0b0f17 100%); border:1px solid rgba(212,175,55,0.45); border-radius:12px; padding:11px 15px; margin-bottom:0.95rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
              <div style="font-size:0.68rem; font-weight:800; color:#d4af37; text-transform:uppercase; letter-spacing:0.06em;">
                ACTIVE DAG STAGE &amp; PREDECESSOR GATE
              </div>
              <div id="p7-dag-banner-headline" style="font-size:0.86rem; font-weight:900; color:#ffffff; margin-top:2px;">
                Stage 13 Active: Rough Framing &amp; Dick's Lumber #52603 Trusses &mdash; Predecessors ST-01..ST-12 Verified Complete &#10003;
              </div>
              <div id="p7-dag-banner-sub" style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
                Click any stage status pill below to advance or toggle completion. Completing a stage unlocks its DAG successor trade for instant mobilization.
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-gold" id="p7-live-hub-sync-pill">CCDC 5B Cloud Sync Ready</span>
            </div>
          </div>

          <!-- 30-Stage Master Checklist List -->
          <div id="p7-thirty-stages-list" style="display:flex; flex-direction:column; gap:8px;">
            <div style="font-size:0.75rem; color:#cbd5e1;">
              ST-01 BCLS Survey &bull; ST-02 Architect AIBC &bull; ST-03 Geotechnical &amp; 6-Discipline P.Eng &bull; ST-04 Energy Step Code &bull; ST-05 Municipal Permits &amp; #52603 Warranty &bull;
              ST-06 Abatement/Demo &bull; ST-07 Bulk Excavation, Rock Blasting &amp; Geotech Shoring &bull; ST-08 Civil Utilities &amp; BC Hydro ES54 &bull; ST-09 Doka Formwork, Rebar &amp; 35 MPa Concrete &bull;
              ST-10 Waterproofing, Drain Tile &amp; Geotech Backfill Compaction &bull; ST-11 Under-Slab Plumbing, Radon &amp; Slab Pour &bull; ST-12 Structural Steel &bull;
              ST-13 Rough Framing &amp; Dick's Lumber #52603 Trusses &bull; ST-14 Roofing &bull; ST-15 NAFS Triple-Glazed Windows &bull; ST-16 Rainscreen WRB &amp; Mid-Blower Door Test &bull;
              ST-17 Plumbing/Gas/Hydronic Rough-In &bull; ST-18 Heat Pumps &amp; HRV &bull; ST-19 NFPA 13D Fire Sprinklers &bull; ST-20 Electrical 400A &amp; EVEMS &bull;
              ST-21 Mineral Wool &amp; STC 55+ Acoustic Insulation &bull; ST-22 Type X Drywall &amp; Level 5 Finish &bull; ST-23 Exterior Cladding &bull; ST-24 Interior Doors, Trim &amp; Stairs &bull;
              ST-25 Cabinetry &amp; Quartz &bull; ST-26 Schluter Waterproofing, Tile &amp; Flooring &bull; ST-27 Glass Railings &amp; Appliances &bull; ST-28 MEP Final Trims &amp; Commissioning &bull;
              ST-29 Civil Hardscaping &amp; Permeable Pavers &bull; ST-30 Final Blower Door, Schedules C-A/C-B &amp; Occupancy
            </div>
          </div>
        </div>

      </section>

    </main>


    <!-- =======================================================================
         MODALS (Trade Command Modal, Day Planner Modal, New Job Modal, PDF Reader Modal, Contacts Modal)
         ======================================================================= -->

    <!-- MODAL A: Full Trade Command Modal (Dates -> Calendar, Signed Contract PDF, Owner Revisions) -->
    <div id="modal-trade" class="kp-modal-backdrop">
      <div class="kp-modal-container" style="max-width:1020px;">
        <div class="kp-modal-header">
          <div class="kp-modal-title" id="trade-modal-title">
            <span>🛠️</span> Trade Subcontract, Schedule &amp; Revision Command
          </div>
          <button type="button" onclick="closeModal('modal-trade')" class="kp-close-btn">&times;</button>
        </div>

        <div class="kp-modal-body">
          <!-- Subcontractor Details & Schedule Dates (Auto-Syncs with Tab 2 Calendar) -->
          <div style="background:rgba(4,8,16,0.85); border:1px solid rgba(56,189,248,0.38); border-radius:14px; padding:16px; margin-bottom:1.25rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
              <div style="font-size:0.8rem; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">
                1. Subcontractor Identity, Contract Sum &amp; Live Calendar Dates
              </div>
              <span style="font-size:0.74rem; color:#d4af37;">⚡ Saving dates immediately updates Tab 2 Calendar &amp; Active Trade Radar</span>
            </div>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px;">
              <div>
                <label class="kp-form-label">Trade Discipline / Stage Name</label>
                <input type="text" id="tm-name" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label">Subcontractor Company Name</label>
                <input type="text" id="tm-sub" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label">Site Foreman / Contact Person</label>
                <input type="text" id="tm-contact" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label">Direct Phone / SMS</label>
                <input type="text" id="tm-phone" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label" style="color:#38bdf8;">📅 Mobilization / Start Date</label>
                <input type="date" id="tm-start-date" class="kp-form-input" style="border-color:rgba(56,189,248,0.5);" />
              </div>
              <div>
                <label class="kp-form-label" style="color:#38bdf8;">🏁 Completion / Finish Date</label>
                <input type="date" id="tm-end-date" class="kp-form-input" style="border-color:rgba(56,189,248,0.5);" />
              </div>
              <div>
                <label class="kp-form-label">Subcontract Baseline ($ CAD)</label>
                <input type="number" id="tm-contract" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label">Invoiced / Billed to Date ($ CAD)</label>
                <input type="number" id="tm-billed" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label">QA Inspection Gate</label>
                <input type="text" id="tm-gate" class="kp-form-input" />
              </div>
              <div>
                <label class="kp-form-label">On-Site Status</label>
                <select id="tm-status" class="kp-form-input">
                  <option value="Completed">Completed</option>
                  <option value="Active On-Site">Active On-Site</option>
                  <option value="Scheduled">Scheduled</option>
                  <option value="Not Started">Not Started</option>
                </select>
              </div>
            </div>

            <div style="margin-top:12px; display:flex; justify-content:flex-end;">
              <button type="button" onclick="saveTradeModalChanges()" class="kp-gold-btn kp-pill-sm">
                💾 Save Trade Details &amp; Sync Calendar Dates
              </button>
            </div>
          </div>

          <!-- Signed Trade Contract PDF Vault -->
          <div style="background:rgba(4,8,16,0.85); border:1px solid rgba(212,175,55,0.38); border-radius:14px; padding:16px; margin-bottom:1.25rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
              <div>
                <div style="font-size:0.8rem; font-weight:800; color:#d4af37; text-transform:uppercase; letter-spacing:0.05em;">
                  2. Executed Trade Subcontract PDF &amp; Scope Documents
                </div>
                <div style="font-size:0.75rem; color:#94a3b8;">Upload the signed trade contract PDF, WCB clearance letter, or shop drawings for instant download.</div>
              </div>
              <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer;">
                📤 Upload Signed Trade Contract PDF
                <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleTradeContractPdfUpload(event)" />
              </label>
            </div>
            <div id="tm-docs-list" style="display:flex; flex-direction:column; gap:8px;">
              <!-- Rendered by JS -->
            </div>
          </div>

          <!-- Trade Revisions / Change Orders Requiring Owner Signature -->
          <div style="background:rgba(4,8,16,0.85); border:1px solid rgba(56,189,248,0.42); border-radius:14px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
              <div>
                <div style="font-size:0.8rem; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">
                  3. Trade Revisions &amp; Change Orders (Synced to Tab 1 for Owner Signature)
                </div>
                <div style="font-size:0.75rem; color:#94a3b8;">
                  Add any scope revision or extra below. The Property Owner can sign &amp; approve it right here or on Tab 1.
                </div>
              </div>
            </div>

            <!-- Add New Revision Inline Form -->
            <div style="display:grid; grid-template-columns:2fr 2fr 1fr 1fr auto; gap:8px; align-items:end; margin-bottom:12px; background:rgba(0,0,0,0.45); padding:10px; border-radius:10px;">
              <div>
                <label class="kp-form-label">Revision Title</label>
                <input type="text" id="tm-rev-title" class="kp-form-input" placeholder="e.g. Extra Bedrock Anchors" />
              </div>
              <div>
                <label class="kp-form-label">Scope / Reason</label>
                <input type="text" id="tm-rev-desc" class="kp-form-input" placeholder="Detailed scope change..." />
              </div>
              <div>
                <label class="kp-form-label">Cost Impact ($)</label>
                <input type="number" id="tm-rev-amount" class="kp-form-input" placeholder="4500" />
              </div>
              <div>
                <label class="kp-form-label">Days Impact</label>
                <input type="number" id="tm-rev-days" class="kp-form-input" placeholder="2" value="0" />
              </div>
              <button type="button" onclick="addRevisionToActiveTrade()" class="kp-cyan-btn kp-pill-sm" style="height:40px;">
                + Add Revision
              </button>
            </div>

            <div id="tm-revisions-list" style="display:flex; flex-direction:column; gap:8px;">
              <!-- Rendered by JS -->
            </div>
          </div>
        </div>

        <div class="kp-modal-footer">
          <button type="button" onclick="closeModal('modal-trade')" class="kp-secondary-btn">Close</button>
          <button type="button" onclick="saveTradeModalChanges(true)" class="kp-gold-btn">💾 Save Trade &amp; Close</button>
        </div>
      </div>
    </div>

        <!-- MODAL B: Day Command, Multi-Field Write-Up & File Storage Modal (White, Gold & Black) -->
    <div id="modal-day" class="kp-modal-backdrop">
      <div class="kp-modal-container" style="max-width:920px; background:#070a10; border:1px solid rgba(255,255,255,0.28);">
        <div class="kp-modal-header" style="background:#05070b; border-bottom:1px solid rgba(255,255,255,0.12);">
          <div class="kp-modal-title" id="day-modal-title" style="color:#ffffff;">
            Daily Field Log, Checkpoints &amp; File Storage
          </div>
          <button type="button" onclick="closeModal('modal-day')" class="kp-close-btn">&times;</button>
        </div>

        <div class="kp-modal-body" style="background:#070a10;">
          <!-- Set This Date as Active Date Banner -->
          <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.2); border-radius:12px; padding:12px 16px; margin-bottom:1.1rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
              <div style="font-size:0.68rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">Active Build Date Control</div>
              <div style="font-size:0.84rem; color:#ffffff; font-weight:700; margin-top:2px;">Set this selected calendar date as the Active Date in the top-right corner</div>
            </div>
            <button type="button" onclick="setModalDateAsWhereWeAre()" class="kp-secondary-btn kp-pill-sm">
              Set as Active Date
            </button>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.15rem;">
            <div style="display:flex; flex-direction:column; gap:1rem;">
              <div>
                <label class="kp-form-label" style="color:#ffffff;">1. Daily Superintendent Field Log &amp; Site Notes</label>
                <textarea id="day-notes-input" class="kp-form-input" style="height:140px; resize:vertical; background:#0b0f17; border-color:rgba(255,255,255,0.22); color:#ffffff;" placeholder="Enter daily field progress, weather, concrete pour tickets, inspection results..."></textarea>
              </div>
              <div>
                <label class="kp-form-label" style="color:#ffffff;">2. Daily QA &amp; Milestone Checkpoints</label>
                <div style="display:flex; gap:6px; margin-bottom:8px;">
                  <input type="text" id="new-checkpoint-input" class="kp-form-input" style="background:#0b0f17; border-color:rgba(255,255,255,0.22); color:#ffffff;" placeholder="Add daily QA checkpoint..." onkeydown="if(event.key==='Enter') addDayCheckpointInline()" />
                  <button type="button" onclick="addDayCheckpointInline()" class="kp-secondary-btn kp-pill-sm">+ Add</button>
                </div>
                <div id="day-checkpoints-list" style="display:flex; flex-direction:column; gap:6px;"></div>
              </div>
            </div>

            <div style="display:flex; flex-direction:column; gap:1rem;">
              <div>
                <label class="kp-form-label" style="color:#ffffff;">3. Trades Active on This Date</label>
                <div id="day-trades-tags" style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:8px;"></div>
                <div style="display:flex; gap:6px;">
                  <input type="text" id="new-day-trade-input" class="kp-form-input" style="background:#0b0f17; border-color:rgba(255,255,255,0.22); color:#ffffff;" placeholder="Write in or tag trade on site..." onkeydown="if(event.key==='Enter') addDayTradeInline()" />
                  <button type="button" onclick="addDayTradeInline()" class="kp-secondary-btn kp-pill-sm">+ Add Trade</button>
                </div>
              </div>

              <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.18); border-radius:12px; padding:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <div>
                    <label class="kp-form-label" style="color:#ffffff; margin:0;">4. Daily File &amp; Photo Storage Vault</label>
                    <div style="font-size:0.7rem; color:#94a3b8; margin-top:2px;">Store site photos, delivery tickets &amp; inspection PDFs for this date</div>
                  </div>
                  <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer;">
                    Upload File
                    <input type="file" style="display:none;" onchange="handleDayFileUpload(event)" />
                  </label>
                </div>
                <div id="day-photos-list" style="display:flex; flex-direction:column; gap:6px;"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="kp-modal-footer" style="background:#05070b; border-top:1px solid rgba(255,255,255,0.12);">
          <button type="button" onclick="closeModal('modal-day')" class="kp-secondary-btn">Cancel</button>
          <button type="button" onclick="saveDayLogModal()" class="kp-gold-btn">Save Daily Log</button>
        </div>
      </div>
    </div>

    <!-- MODAL C: Create New Upcoming Job Portal Modal -->
    <div id="modal-new-job" class="kp-modal-backdrop">
      <div class="kp-modal-container" style="max-width:680px;">
        <div class="kp-modal-header">
          <div class="kp-modal-title">
            <span>🏛️</span> Create New Job Portal (Unique Address &amp; Owner Passcode)
          </div>
          <button type="button" onclick="closeModal('modal-new-job')" class="kp-close-btn">&times;</button>
        </div>
        <div class="kp-modal-body">
          <div style="font-size:0.84rem; color:#cbd5e1; margin-bottom:1rem;">
            Create a complete, dedicated portal for an upcoming project. It will automatically pre-load the 22 BC Construction Trades, 12 Municipal Inspections, 2-5-10 National Home Warranty vault, and 8 Builder Material Takeoff stages ready for customization.
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
            <div style="grid-column:span 2;">
              <label class="kp-form-label" style="color:#38bdf8;">📍 Job Civic Address (Required)</label>
              <input type="text" id="nj-address" class="kp-form-input" placeholder="e.g. 38120 Westway Ave, Squamish, BC" />
            </div>
            <div>
              <label class="kp-form-label">Project Title / Description</label>
              <input type="text" id="nj-title" class="kp-form-input" placeholder="e.g. Westway Custom Mountain Residence" />
            </div>
            <div>
              <label class="kp-form-label">Municipal Jurisdiction</label>
              <input type="text" id="nj-municipality" class="kp-form-input" placeholder="e.g. District of Squamish" value="District of Squamish" />
            </div>
            <div>
              <label class="kp-form-label">Property Owner Full Name(s)</label>
              <input type="text" id="nj-owner-name" class="kp-form-input" placeholder="e.g. Robert &amp; Claire Sterling" />
            </div>
            <div>
              <label class="kp-form-label">Owner Phone (SMS / Call)</label>
              <input type="text" id="nj-owner-phone" class="kp-form-input" placeholder="(604) 555-0144" />
            </div>
            <div>
              <label class="kp-form-label">Original Contract Price ($ CAD)</label>
              <input type="number" id="nj-contract-price" class="kp-form-input" placeholder="2150000" value="2150000" />
            </div>
            <div>
              <label class="kp-form-label" style="color:#d4af37;">🔑 Assign Owner Passcode</label>
              <input type="text" id="nj-passcode" class="kp-form-input" placeholder="e.g. westway2026" />
            </div>
            <div>
              <label class="kp-form-label">Scheduled Start Date</label>
              <input type="date" id="nj-start-date" class="kp-form-input" value="2026-11-02" />
            </div>
            <div>
              <label class="kp-form-label">Building Footprint Per Floor (SF)</label>
              <input type="number" id="nj-footprint" class="kp-form-input" value="1650" />
            </div>
          </div>
        </div>
        <div class="kp-modal-footer">
          <button type="button" onclick="closeModal('modal-new-job')" class="kp-secondary-btn">Cancel</button>
          <button type="button" onclick="createNewJobPortalFromModal()" class="kp-gold-btn">✨ Create &amp; Launch New Job Portal</button>
        </div>
      </div>
    </div>

    <!-- MODAL D: Inline Document & PDF Reader Modal -->
    <div id="modal-pdf-viewer" class="kp-modal-backdrop">
      <div class="kp-modal-container" style="max-width:960px;">
        <div class="kp-modal-header">
          <div class="kp-modal-title" id="pdf-modal-title">
            <span>📄</span> Verified Project Document Viewer
          </div>
          <button type="button" onclick="closeModal('modal-pdf-viewer')" class="kp-close-btn">&times;</button>
        </div>
        <div class="kp-modal-body" id="pdf-modal-body" style="max-height:72vh; overflow-y:auto;"></div>
        <div class="kp-modal-footer">
          <button type="button" onclick="closeModal('modal-pdf-viewer')" class="kp-secondary-btn">Close Viewer</button>
          <button type="button" id="pdf-modal-download-btn" class="kp-gold-btn">📥 Download PDF Copy</button>
        </div>
      </div>
    </div>

    <!-- MODAL E: Executive Contact Directory Modal -->
    <div id="modal-binder" class="kp-modal-backdrop">
      <div class="kp-modal-container" style="max-width:960px;">
        <div class="kp-modal-header">
          <div class="kp-modal-title">
            <span>🏛️</span> Executive Project Authority &amp; Engineering Directory
          </div>
          <button type="button" onclick="closeModal('modal-binder')" class="kp-close-btn">&times;</button>
        </div>
        <div class="kp-modal-body">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:8px;">
            <span style="font-size:0.84rem; color:#cbd5e1;">Key project contacts for Builder, Owner, Architect, Structural/Geotech Engineers &amp; City Inspectors.</span>
            <button type="button" onclick="openAddContactPrompt()" class="kp-cyan-btn kp-pill-sm">+ Add Project Authority</button>
          </div>
          <div id="contacts-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:12px;"></div>
        </div>
        <div class="kp-modal-footer">
          <button type="button" onclick="closeModal('modal-binder')" class="kp-secondary-btn">Close Directory</button>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div id="kp-toast">Action saved!</div>

  </div>
</div>
</main>

<?php
get_footer();
