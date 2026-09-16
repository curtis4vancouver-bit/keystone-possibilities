<?php
/**
 * Master Portfolio Residences 9-Carousel Component & Hero Banner System
 *
 * Provides [portfolio_residences_carousels] shortcode for Astra Child Theme.
 *
 * @package Astra Child for Keystone Possibilities
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function kp_portfolio_residences_carousels_shortcode() {
    ob_start();
    ?>
    <style>
        @keyframes floatReel {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }
        .portfolio-hero-banner-wrapper {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto 2.5rem auto;
            overflow: hidden;
            max-height: 400px;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(196, 162, 101, 0.4);
            position: relative;
        }
        .portfolio-hero-banner-img {
            width: 100%;
            height: 500px;
            object-fit: cover;
            object-position: center 20%;
            margin-top: -50px;
            display: block;
        }
        .residences-master-wrapper {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        .residence-section {
            position: relative;
            padding: 3.5rem 1.5rem;
            background: #04070d;
            border-top: 1px solid #1e293b;
            border-bottom: 1px solid #1e293b;
            margin: 3rem 0;
            overflow: hidden;
            border-radius: 8px;
        }
        .residence-glowing-aura {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 85%; height: 65%;
            background: radial-gradient(circle, rgba(196, 162, 101, 0.25) 0%, rgba(56, 189, 248, 0.12) 50%, transparent 80%);
            filter: blur(55px);
            z-index: 0; pointer-events: none;
        }
        .residence-title-heading {
            font-family: 'Outfit', sans-serif;
            font-size: clamp(1.6rem, 3.5vw, 2.4rem);
            font-weight: 700;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
            position: relative; z-index: 2;
        }
        .gold-glow-end {
            color: #C4A265;
            background: linear-gradient(135deg, #ffffff 20%, #C4A265 80%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 14px rgba(196, 162, 101, 0.75));
            font-weight: 800;
        }
        .residence-carousel-track {
            display: flex;
            gap: 1.5rem;
            overflow-x: auto;
            scroll-behavior: smooth;
            padding: 1.5rem 0.5rem;
            position: relative; z-index: 2;
        }
        .residence-carousel-track::-webkit-scrollbar { height: 6px; }
        .residence-carousel-track::-webkit-scrollbar-thumb {
            background: #C4A265;
            border-radius: 3px;
        }
        .residence-card {
            flex: 0 0 340px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(196, 162, 101, 0.3);
            border-radius: 8px;
            overflow: hidden;
            transition: all 0.4s ease;
            animation: floatReel 5s ease-in-out infinite;
        }
        .residence-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: #C4A265;
            box-shadow: 0 15px 35px rgba(196, 162, 101, 0.4), 0 0 25px rgba(56, 189, 248, 0.25);
        }
        .residence-img {
            width: 100%;
            height: 230px;
            object-fit: cover;
            cursor: zoom-in;
            transition: transform 0.4s ease;
        }
        .residence-img:hover { transform: scale(1.05); }
        .residence-breakdown-box {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(196, 162, 101, 0.25);
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            text-align: left;
            position: relative; z-index: 2;
        }
        .residence-breakdown-box h5 {
            color: #C4A265;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            text-transform: uppercase;
            margin: 0 0 0.4rem 0;
            letter-spacing: 0.05em;
        }
        .residence-breakdown-box p {
            color: #cbd5e1;
            font-size: 0.88rem;
            line-height: 1.6;
            margin: 0 0 0.8rem 0;
        }
        .code-badge-pill {
            display: inline-block;
            background: rgba(196, 162, 101, 0.15);
            border: 1px solid #C4A265;
            color: #ffffff;
            font-size: 0.75rem;
            padding: 3px 8px;
            border-radius: 4px;
            margin-right: 6px; margin-bottom: 6px;
        }
        /* LIGHTBOX MODAL */
        #residence-lightbox-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.94);
            backdrop-filter: blur(15px);
            z-index: 99999;
            justify-content: center; align-items: center;
            padding: 2rem;
        }
        #residence-lightbox-modal.active { display: flex; }
        .lightbox-modal-content {
            max-width: 90vw; max-height: 85vh;
            text-align: center; position: relative;
        }
        .lightbox-modal-content img {
            max-width: 100%; max-height: 75vh;
            border: 2px solid #C4A265;
            box-shadow: 0 0 45px rgba(196, 162, 101, 0.55);
            border-radius: 6px;
        }
        .lightbox-caption-text {
            color: #ffffff;
            font-family: 'Outfit', sans-serif;
            font-size: 1.2rem; margin-top: 1rem;
        }
        .lightbox-close-icon {
            position: absolute;
            top: -45px; right: 0;
            color: #C4A265; font-size: 2.8rem;
            cursor: pointer; line-height: 1;
        }
    </style>

    <!-- CENTERED CROPPED HERO BANNER -->
    <div class="portfolio-hero-banner-wrapper">
        <img src="https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2026/05/Modern_luxury_home_forest8_202605011201.jpeg?ssl=1" alt="Keystone Possibilities Master Luxury Home Build" class="portfolio-hero-banner-img">
    </div>

    <div class="residences-master-wrapper">
        <div style="text-align:center; padding: 1.5rem 0 2.5rem;">
            <h2 style="color:#ffffff; font-size: 2.4rem; text-transform:uppercase; letter-spacing:0.08em; margin:0;">
                MASTER PORTFOLIO &bull; <span class="gold-glow-end">9 RESIDENCES</span>
            </h2>
        </div>

        <!-- 1. WEST RIDGE PROPERTY - VANCOUVER (5 Photos) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                WEST RIDGE PROPERTY - <span class="gold-glow-end">VANCOUVER</span>
            </h3>
            <div class="residence-carousel-track">
                <?php
                $west_ridge_imgs = [
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.32-pm.png?resize=1580%2C1274&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.40-pm.png?resize=994%2C892&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.48-pm.png?resize=982%2C824&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.54.53-pm.png?resize=824%2C728&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.55.02-pm.png?resize=796%2C1298&ssl=1"
                ];
                foreach ($west_ridge_imgs as $idx => $img_url) : ?>
                    <div class="residence-card">
                        <img src="<?php echo esc_url($img_url); ?>" alt="West Ridge Property Vancouver <?php echo $idx + 1; ?>" class="residence-img" onclick="openResidenceLightbox('<?php echo esc_url($img_url); ?>', 'WEST RIDGE PROPERTY &bull; VANCOUVER, BC (Photo <?php echo $idx+1; ?> of 5)')">
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>West Ridge Road / Dunbar-Southlands Corridor, Vancouver, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Constructed under <strong>Vancouver Building By-law (VBBL 2014 / BCBC 2012)</strong>. Integrated continuous R-22 effective exterior wall insulation (VBBL Part 10), Simpson HTT/HDU cast-in-place seismic hold-down assemblies to withstand peak ground acceleration (Sa=0.94g), and engineered hydronic in-floor radiant heating loops.</p>
                <div>
                    <span class="code-badge-pill">VBBL 2014 Part 10</span>
                    <span class="code-badge-pill">R-22 Effective Insulation</span>
                    <span class="code-badge-pill">Seismic Hold-Downs (Sa=0.94g)</span>
                </div>
            </div>
        </section>

        <!-- 2. BALLANTREE RESIDENCE - VANCOUVER (5 Photos) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                BALLANTREE RESIDENCE - <span class="gold-glow-end">VANCOUVER</span>
            </h3>
            <div class="residence-carousel-track">
                <?php
                $ballantree_imgs = [
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.57.48-pm.png?resize=1870%2C1086&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.58.07-pm.png?resize=2592%2C1410&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-3.58.16-pm.png?resize=1292%2C1304&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.29-pm.png?resize=1558%2C616&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.23-pm.png?resize=1498%2C700&ssl=1"
                ];
                foreach ($ballantree_imgs as $idx => $img_url) : ?>
                    <div class="residence-card">
                        <img src="<?php echo esc_url($img_url); ?>" alt="Ballantree Residence West Vancouver <?php echo $idx + 1; ?>" class="residence-img" onclick="openResidenceLightbox('<?php echo esc_url($img_url); ?>', 'BALLANTREE RESIDENCE &bull; WEST VANCOUVER, BC (Photo <?php echo $idx+1; ?> of 5)')">
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>5610 Ballantree Road, British Properties, West Vancouver, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Navigated <strong>District of West Vancouver Watercourse Protection Bylaw No. 4364</strong> (15m top-of-bank setback) &amp; steep slope geotechnical stabilization. Deep concrete micropiles socketed directly into granite bedrock, post-tensioned rock anchors, and cantilevered architectural structural steel support frames.</p>
                <div>
                    <span class="code-badge-pill">Geotechnical Micropiles</span>
                    <span class="code-badge-pill">Granite Bedrock Anchors</span>
                    <span class="code-badge-pill">Bylaw 4364 15m Setback</span>
                </div>
            </div>
        </section>

        <!-- 3. DICKINSON RESIDENCE - VANCOUVER (8 Photos) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                DICKINSON RESIDENCE - <span class="gold-glow-end">VANCOUVER</span>
            </h3>
            <div class="residence-carousel-track">
                <?php
                $dickinson_imgs = [
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.02.40-pm.png?resize=1892%2C1460&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.38-pm.png?resize=1616%2C738&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.31-pm.png?resize=1464%2C704&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.02.54-pm.png?resize=2600%2C1174&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.39-pm.png?resize=2630%2C1356&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.05-pm.png?resize=1318%2C760&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.03.12-pm.png?resize=1348%2C622&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.04.56-pm.png?resize=2574%2C1332&ssl=1"
                ];
                foreach ($dickinson_imgs as $idx => $img_url) : ?>
                    <div class="residence-card">
                        <img src="<?php echo esc_url($img_url); ?>" alt="Dickinson Residence Vancouver <?php echo $idx + 1; ?>" class="residence-img" onclick="openResidenceLightbox('<?php echo esc_url($img_url); ?>', 'DICKINSON RESIDENCE &bull; VANCOUVER, BC (Photo <?php echo $idx+1; ?> of 8)')">
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>Dickinson Road / Point Grey Coastal Ridge, Vancouver, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Proactive winter weather excavation &amp; moisture management under <strong>BCBC 2012 Part 9.27 (Rainscreen Standard)</strong>. Integrated dual-membrane foundation damp-proofing, heavy timber ceiling joist ties, and high-performance low-E structural argon glazing.</p>
                <div>
                    <span class="code-badge-pill">BCBC Part 9.27 Rainscreen</span>
                    <span class="code-badge-pill">Foundation Damp-Proofing</span>
                    <span class="code-badge-pill">Argon Structural Glazing</span>
                </div>
            </div>
        </section>

        <!-- 4. ST ANDREWS RESIDENCE - VANCOUVER (10 Photos) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                ST ANDREWS RESIDENCE - <span class="gold-glow-end">VANCOUVER</span>
            </h3>
            <div class="residence-carousel-track">
                <?php
                $st_andrews_imgs = [
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.07.36-pm.png?resize=1938%2C1064&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.11-pm.png?resize=854%2C622&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.16-pm.png?resize=842%2C722&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.21-pm.png?resize=844%2C678&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.27-pm.png?resize=828%2C664&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.33-pm.png?resize=1256%2C890&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.38-pm.png?resize=1242%2C950&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.46-pm.png?resize=1162%2C956&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.08.54-pm.png?resize=1146%2C948&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.09.00-pm.png?resize=1160%2C882&ssl=1"
                ];
                foreach ($st_andrews_imgs as $idx => $img_url) : ?>
                    <div class="residence-card">
                        <img src="<?php echo esc_url($img_url); ?>" alt="St Andrews Residence Vancouver <?php echo $idx + 1; ?>" class="residence-img" onclick="openResidenceLightbox('<?php echo esc_url($img_url); ?>', 'ST ANDREWS RESIDENCE &bull; VANCOUVER, BC (Photo <?php echo $idx+1; ?> of 10)')">
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>St. Andrews Avenue / Lower Lonsdale-Vancouver Border, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Ultra-modern luxury build featuring full smart home system integration, 400A electrical service entrance, continuous acoustic ceiling baffles, and compliance with <strong>BCBC 2012 Section 9.36 Energy Efficiency Code</strong>.</p>
                <div>
                    <span class="code-badge-pill">BCBC 9.36 Energy Code</span>
                    <span class="code-badge-pill">400A Smart Electrical</span>
                    <span class="code-badge-pill">Acoustic Ceiling Assemblies</span>
                </div>
            </div>
        </section>

        <!-- 5. PRIMA RESIDENCE - VANCOUVER (3 Photos) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                PRIMA RESIDENCE - <span class="gold-glow-end">VANCOUVER</span>
            </h3>
            <div class="residence-carousel-track">
                <?php
                $prima_imgs = [
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.12.46-pm.png?resize=1818%2C984&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.12.55-pm.png?resize=1516%2C722&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.13.00-pm.png?resize=1178%2C1200&ssl=1"
                ];
                foreach ($prima_imgs as $idx => $img_url) : ?>
                    <div class="residence-card">
                        <img src="<?php echo esc_url($img_url); ?>" alt="Prima Residence Vancouver <?php echo $idx + 1; ?>" class="residence-img" onclick="openResidenceLightbox('<?php echo esc_url($img_url); ?>', 'PRIMA RESIDENCE &bull; VANCOUVER, BC (Photo <?php echo $idx+1; ?> of 3)')">
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>Prima Street / Vancouver Westside Infill Zone, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>High-density custom urban home. Built to <strong>VBBL 2014 Part 9 Architectural Fire Separations</strong> (1-hour fire-resistance rated party walls), zero-lot-line perimeter shoring, and high-efficiency heat recovery ventilator (HRV) mechanicals.</p>
                <div>
                    <span class="code-badge-pill">1-Hour Fire Separation</span>
                    <span class="code-badge-pill">Zero Lot Line Shoring</span>
                    <span class="code-badge-pill">HRV Mechanical System</span>
                </div>
            </div>
        </section>

        <!-- 6. SUNRIDGE RESIDENCE - WHISTLER (8 Photos) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                SUNRIDGE RESIDENCE - <span class="gold-glow-end">WHISTLER</span>
            </h3>
            <div class="residence-carousel-track">
                <?php
                $sunridge_imgs = [
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.07-pm.png?resize=2288%2C1172&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.14-pm.png?resize=2592%2C1252&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.22-pm.png?resize=2492%2C1246&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.30-pm.png?resize=2540%2C1244&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.38-pm.png?resize=2530%2C1224&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.45-pm.png?resize=2318%2C1174&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.51-pm.png?resize=2318%2C1154&ssl=1",
                    "https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.14.56-pm.png?resize=2412%2C1174&ssl=1"
                ];
                foreach ($sunridge_imgs as $idx => $img_url) : ?>
                    <div class="residence-card">
                        <img src="<?php echo esc_url($img_url); ?>" alt="Sunridge Residence Whistler <?php echo $idx + 1; ?>" class="residence-img" onclick="openResidenceLightbox('<?php echo esc_url($img_url); ?>', 'SUNRIDGE RESIDENCE &bull; WHISTLER, BC (Photo <?php echo $idx+1; ?> of 8)')">
                    </div>
                <?php endforeach; ?>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>Sunridge Plateau Drive, Whistler, BC (Ski-In / Ski-Out Zone)</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Engineered under <strong>BCBC 2012 Part 4 Structural Design</strong> for extreme high-altitude ground snow loads (S_g = 6.2 to 8.1 kPa). Heavy timber structural posts, bedrock-anchored concrete foundation, and RMOW OCP Wildfire Protection DPA Class A non-combustible metal roofing.</p>
                <div>
                    <span class="code-badge-pill">BCBC Part 4 Snow Load 8.1 kPa</span>
                    <span class="code-badge-pill">RMOW FireSmart DPA</span>
                    <span class="code-badge-pill">Granite Bedrock Tie-Backs</span>
                </div>
            </div>
        </section>

        <!-- 7. PIPER RESIDENCE - SECHELT (1 Photo) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                PIPER RESIDENCE - <span class="gold-glow-end">SECHELT</span>
            </h3>
            <div class="residence-carousel-track">
                <div class="residence-card">
                    <img src="https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.43-pm.png?resize=1812%2C940&ssl=1" alt="Piper Residence Sechelt" class="residence-img" onclick="openResidenceLightbox('https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.43-pm.png?resize=1812%2C940&ssl=1', 'PIPER RESIDENCE &bull; SECHELT, BC')">
                </div>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>Piper Lane, Davis Bay, Sechelt, Sunshine Coast, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Coastal custom residence complying with <strong>BCBC 2012 1/100 Hourly Wind Pressures (q100 = 0.55 kPa)</strong> and District of Sechelt Coastal Setback By-laws. Features BC Hydro ES54 underground electrical DB2 PVC conduit and continuous weeping tile in 150mm clear drain rock.</p>
                <div>
                    <span class="code-badge-pill">Wind Pressure q100 = 0.55 kPa</span>
                    <span class="code-badge-pill">BC Hydro ES54 Underground</span>
                    <span class="code-badge-pill">Geotextile Weeping Tile</span>
                </div>
            </div>
        </section>

        <!-- 8. COMPASS RESIDENCE - SECHELT (1 Photo) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                COMPASS RESIDENCE - <span class="gold-glow-end">SECHELT</span>
            </h3>
            <div class="residence-carousel-track">
                <div class="residence-card">
                    <img src="https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.52-pm.png?resize=1724%2C1130&ssl=1" alt="Compass Residence Sechelt" class="residence-img" onclick="openResidenceLightbox('https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.19.52-pm.png?resize=1724%2C1130&ssl=1', 'COMPASS RESIDENCE &bull; SECHELT, BC')">
                </div>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>Compass Lane, Trail Bay, Sechelt, Sunshine Coast, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Built under <strong>BCBC 2018 Moisture Management &amp; Section 9.14 Drainage Guidelines</strong>. Features high coastal water-table elastomeric waterproofing membrane, rainscreen cavity framing, and hurricane tie-down roof strapping.</p>
                <div>
                    <span class="code-badge-pill">BCBC 9.14 Foundation Drainage</span>
                    <span class="code-badge-pill">Coastal Water Table Barrier</span>
                    <span class="code-badge-pill">Hurricane Strapping</span>
                </div>
            </div>
        </section>

        <!-- 9. SULLIVAN RESIDENCE - SECHELT (1 Photo) -->
        <section class="residence-section">
            <div class="residence-glowing-aura"></div>
            <h3 class="residence-title-heading">
                SULLIVAN RESIDENCE - <span class="gold-glow-end">SECHELT</span>
            </h3>
            <div class="residence-carousel-track">
                <div class="residence-card">
                    <img src="https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.20.00-pm.png?resize=1802%2C872&ssl=1" alt="Sullivan Residence Sechelt" class="residence-img" onclick="openResidenceLightbox('https://i0.wp.com/keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-04-at-4.20.00-pm.png?resize=1802%2C872&ssl=1', 'SULLIVAN RESIDENCE &bull; SECHELT, BC')">
                </div>
            </div>
            <div class="residence-breakdown-box">
                <h5>📍 Location &amp; Neighborhood</h5>
                <p><strong>Sullivan Road, Sandy Hook, Sechelt, Sunshine Coast, BC</strong></p>
                <h5>🛠️ Historic BC Building Code &amp; Municipal Compliance</h5>
                <p>Heavy custom structural framing complying with <strong>BCBC 2012 Coastal High-Wind Provisions (q100 = 0.55 kPa)</strong>. Foundation footings poured directly onto cleared granite bedrock, engineered floor I-joist spans, and high-load structural steel support columns.</p>
                <div>
                    <span class="code-badge-pill">Granite Bedrock Footings</span>
                    <span class="code-badge-pill">Engineered Floor I-Joists</span>
                    <span class="code-badge-pill">High Load Steel Columns</span>
                </div>
            </div>
        </section>

    </div>

    <!-- LIGHTBOX MODAL DIALOG -->
    <div id="residence-lightbox-modal" onclick="closeResidenceLightbox(event)">
        <div class="lightbox-modal-content" onclick="event.stopPropagation()">
            <span class="lightbox-close-icon" onclick="closeResidenceLightbox(event)">&times;</span>
            <img id="residence-lightbox-target-img" src="" alt="Residence Full View">
            <div id="residence-lightbox-target-caption" class="lightbox-caption-text"></div>
        </div>
    </div>

    <script>
        function openResidenceLightbox(imgSrc, caption) {
            const modal = document.getElementById('residence-lightbox-modal');
            const img = document.getElementById('residence-lightbox-target-img');
            const cap = document.getElementById('residence-lightbox-target-caption');
            img.src = imgSrc;
            cap.innerHTML = caption;
            modal.classList.add('active');
        }
        function closeResidenceLightbox(event) {
            const modal = document.getElementById('residence-lightbox-modal');
            modal.classList.remove('active');
        }
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode( 'portfolio_residences_carousels', 'kp_portfolio_residences_carousels_shortcode' );
