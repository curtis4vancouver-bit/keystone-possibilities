<?php
/**
 * The template for displaying the Keystone Possibilities Master Builder Homepage
 * Certified BC Housing Builder #52603 — Architectural Dark Quiet Luxury
 *
 * @package KeystonePossibilitiesChild
 * @version 4.6.0
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

get_header();
?>

<div id="primary" class="content-area primary keystone-master-builder-home">
    <main id="main" class="site-main">

<div class="kp-homepage-wrapper kp-v460-master">
  

  <!-- GOLD CREDENTIAL RIBBON SUBHEADER -->
  <div class="credential-ribbon">
    <p class="ribbon-text">
      CERTIFIED BC HOUSING BUILDER #52603 • BC HYDRO REGISTERED CIVIL CONTRACTOR (ES54) • STATUTORY 2-5-10 WARRANTY • CCDC 5B OPEN-BOOK FIDUCIARY
    </p>
  </div>

  <!-- =========================================================================
       1. HERO SECTION — CENTERED H1 + GEO CORRIDOR BAR + SINGLE VIDEO BRIEFING
       ========================================================================= -->
  <section class="hero-center-container" style="max-width: 1280px; margin: 0 auto; padding: 36px 20px 28px; text-align: center; display: flex; flex-direction: column; align-items: center;">
    
    <!-- Centered Entity Pill -->
    <div class="kp-kicker-pill-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(212, 175, 55, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; margin-bottom: 16px;">
      <span>🏛️ KEYSTONE POSSIBILITIES LTD • LICENSED BUILDER #52603</span>
    </div>

    <!-- Prominent Geo Corridor Pills Bar (Clearly Labeled Geo Locations) -->
    <div class="municipal-pills-row" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 24px;">
      <a href="/west-vancouver-custom-homes/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 West Vancouver →</span></a>
      <a href="/whistler-custom-homes/" class="kp-geo-pill kp-geo-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(56, 189, 248, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 Whistler Alpine →</span></a>
      <a href="/squamish-custom-homes/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 Squamish →</span></a>
      <a href="/north-vancouver-custom-homes/" class="kp-geo-pill kp-geo-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(56, 189, 248, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 North Vancouver →</span></a>
      <a href="/bc-hydro-registered-civil-contractor/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>⚡ BC Hydro Civil ES54 →</span></a>
    </div>

    <!-- Centered H1 Master Headline (White First -> Gold at the End) -->
    <h1 class="hero-master-title" style="font-size: clamp(1.75rem, 2.65vw, 2.55rem) !important; font-weight: 800 !important; line-height: 1.2 !important; letter-spacing: -0.01em !important; text-transform: uppercase !important; color: #FFFFFF !important; max-width: 1080px !important; margin: 0 auto 18px auto !important; text-align: center !important;">
      Luxury Custom Homes, Mountain Estates &amp; BC Hydro Civil —<br>
      <span style="color: #d4af37 !important; -webkit-text-fill-color: #d4af37 !important; text-shadow: 0 0 24px rgba(212, 175, 55, 0.35);">Built With Open-Book Cost Transparency</span>
    </h1>

    <!-- Centered Subtitle Paragraph -->
    <p class="hero-description-lead" style="font-size: clamp(0.98rem, 1.12vw, 1.1rem); line-height: 1.7; color: #cbd5e1; max-width: 880px; margin: 0 auto 28px auto; text-align: center;">
      Turnkey architectural custom homes, mountain &amp; oceanfront estates, and self-performed <strong style="color: #d4af37;">BC Hydro ES54 underground civil servicing</strong> across <strong style="color: #f8fafc;">West Vancouver, Whistler, Squamish, and North Vancouver</strong>. Directly supervised on-site by licensed Master Builder <strong style="color: #d4af37;">Wayne Stevenson (#52603)</strong> with statutory 2-5-10 Year Warranty protection and <strong style="color: #38bdf8;">100% open-book CCDC 5B accounting</strong>.
    </p>

    <!-- Centered Dual Pure-Black CTA Buttons -->
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; margin-bottom: 44px;">
      <a href="#sqft-calculator" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
        <span>📐 Calculate Your Square-Foot Build Cost →</span>
      </a>
      <a href="/client-login/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
        <span>🔐 24/7 Client Portal Login →</span>
      </a>
    </div>

    <!-- =======================================================================
         2. MASTER BUILDER VIDEO BRIEFING — SINGLE 16:9 YOUTUBE VIDEO (NO DUPLICATE LEFT IMAGE)
         ======================================================================= -->
    <div id="kp-poss009-featured-showcase" style="width: 100%; max-width: 1080px; text-align: center; margin: 0 auto 48px auto; padding: clamp(26px, 3.5vw, 40px); background: radial-gradient(circle at top center, rgba(212, 175, 55, 0.14) 0%, rgba(10, 16, 28, 0.98) 65%, #04070d 100%); border: 1.5px solid rgba(212, 175, 55, 0.72); border-radius: 20px; box-shadow: 0 24px 55px rgba(0,0,0,0.88), 0 0 28px rgba(212, 175, 55, 0.16); box-sizing: border-box;">
      <div class="kp-kicker-pill-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(56, 189, 248, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important;">
        <span>🎬 MASTER BUILDER VIDEO BRIEFING • 📍 WEST VANCOUVER &amp; WHISTLER</span>
      </div>
      <h2 style="margin: 0 auto 12px auto; font-size: clamp(1.45rem, 2.2vw, 1.95rem); font-weight: 800; line-height: 1.24; color: #ffffff; max-width: 920px; text-align: center; text-transform: uppercase;">
        West Vancouver &amp; Whistler Custom Homes:<br>
        <span style="color: #d4af37;">Step Code 5 &amp; Structural Cantilever Engineering</span>
      </h2>
      <p style="margin: 0 auto 24px auto; color: #cbd5e1; font-size: 0.98rem; line-height: 1.68; max-width: 820px; text-align: center;">
        Watch Wayne Stevenson (BC Housing Licensed Builder #52603) explain how we engineer oceanfront concrete cantilevers, Whistler 4.2 kPa snow-load timber frames, and Schöck Isokorb thermal breaks so your custom estate passes BC Building Code Step Code 5 without costly mid-build redesigns.
      </p>

      <!-- Single Centered 16:9 YouTube Video Frame -->
      <div style="max-width: 860px; margin: 0 auto 26px auto; border-radius: 16px; overflow: hidden; border: 1.5px solid rgba(212, 175, 55, 0.65); box-shadow: 0 18px 44px rgba(0,0,0,0.85); background: #000;">
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
          <iframe src="https://www.youtube.com/embed/kLsNyKvQswg" title="West Vancouver &amp; Whistler BCBC 2024 Step Code 5 Masterclass" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="" loading="lazy"></iframe>
        </div>
      </div>

      <!-- Centered Pure-Black Gold & Blue Video Action Buttons -->
      <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; align-items: center;">
        <a href="https://keystonepossibilities.ca/2026/10/16/west-vancouver-whistler-bcbc-2024-step-code-5-cantilever-seismic-guide/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
          <span>📖 Open Full Technical Briefing &amp; Blueprints →</span>
        </a>
        <a href="https://www.youtube.com/shorts/GFeD0LGGks8" target="_blank" rel="noopener" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
          <span>⚡ Watch 40s Companion Short →</span>
        </a>
      </div>
    </div>

    <!-- =======================================================================
         3. DIRECT MASTER BUILDER SUPERINTENDENCE CARD (WAYNE'S COASTAL ESTATE PORTRAIT)
         ======================================================================= -->
    <div class="superintendence-master-card" id="direct-superintendence" style="width: 100%; max-width: 1200px; margin: 0 auto; padding: clamp(28px, 3.5vw, 42px); background: linear-gradient(145deg, rgba(10, 16, 30, 0.96) 0%, rgba(4, 7, 13, 0.99) 100%); border: 1.5px solid rgba(212, 175, 55, 0.65); border-radius: 20px; box-shadow: 0 24px 60px rgba(0,0,0,0.88); box-sizing: border-box;">
      <div style="text-align: center; margin-bottom: 26px;">
        <div class="kp-kicker-pill-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(212, 175, 55, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important;">
          <span>🏛️ DIRECT MASTER BUILDER SUPERINTENDENCE • ZERO BROKER LAYERS</span>
        </div>
        <h2 style="margin: 0 auto 10px auto; font-size: clamp(1.38rem, 2.1vw, 1.92rem); font-weight: 800; line-height: 1.24; color: #ffffff; text-transform: uppercase; text-align: center;">
          Personal On-Site Command By <span style="color: #d4af37; white-space: nowrap;">Wayne Stevenson (#52603)</span>
        </h2>
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 12px;">
          <a href="/west-vancouver-custom-homes/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 WEST VANCOUVER</span></a>
          <a href="/whistler-custom-homes/" class="kp-geo-pill kp-geo-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(56, 189, 248, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 WHISTLER</span></a>
          <a href="/squamish-custom-homes/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 SQUAMISH HQ</span></a>
          <a href="/north-vancouver-custom-homes/" class="kp-geo-pill kp-geo-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(56, 189, 248, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 NORTH VANCOUVER</span></a>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 34px; align-items: center; text-align: left;">
        <!-- Left: Wayne Stevenson High-End Coastal & Mountain Estate Avatar Portrait -->
        <div style="position: relative; border-radius: 16px; overflow: hidden; border: 1.5px solid #d4af37; box-shadow: 0 18px 42px rgba(0,0,0,0.85);">
          <img decoding="async" src="https://keystonepossibilities.ca/wp-content/uploads/2026/10/wayne_possibilities_coastal_estate.jpg" alt="Wayne Stevenson — Licensed Master Builder #52603 on Coastal &amp; Mountain Estate Construction Site" loading="eager" style="width: 100%; height: auto; display: block; object-fit: cover;">
          <div style="position: absolute; bottom: 14px; left: 14px; right: 14px; background: rgba(4, 7, 13, 0.92); backdrop-filter: blur(10px); border: 1px solid rgba(212, 175, 55, 0.65); border-radius: 12px; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; gap: 10px;">
            <div>
              <div style="font-family: 'Outfit', sans-serif; font-size: 1rem; font-weight: 800; color: #ffffff;">Wayne Stevenson</div>
              <div style="font-size: 0.76rem; color: #d4af37; font-weight: 700;">BC Housing Licensed Builder #52603 • BC Hydro ES54 Civil Superintendent</div>
            </div>
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 10px #38bdf8; flex-shrink: 0;"></span>
          </div>
        </div>

        <!-- Right: Crisp Executive Builder Credentials -->
        <div style="display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <h3 style="font-size: 1.45rem; font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.25;">
              Your Estate Is Built By The Principal — Never Handed Off To Junior Brokers.
            </h3>
            <p style="color: #cbd5e1; font-size: 0.96rem; line-height: 1.68; margin: 0 0 20px 0;">
              Most custom home companies operate as sales brokerages that sign your contract and hand your multi-million-dollar build to rotating site coordinators. At Keystone Possibilities, Wayne Stevenson personally directs every rock excavation, structural concrete pour, and BC Hydro utility tie-in.
            </p>
            
            <div style="display: grid; gap: 12px; margin-bottom: 24px;">
              <div style="background: rgba(4, 7, 13, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 12px; padding: 12px 16px; font-size: 0.88rem; color: #e2e8f0; line-height: 1.55;">
                <strong style="color: #d4af37;">✦ BC Housing Licensed Builder #52603:</strong> Full statutory 2-5-10 Year National Home Warranty coverage and licensed structural compliance.
              </div>
              <div style="background: rgba(4, 7, 13, 0.85); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 12px 16px; font-size: 0.88rem; color: #e2e8f0; line-height: 1.55;">
                <strong style="color: #38bdf8;">✦ BC Hydro Registered Civil Contractor (ES54):</strong> In-house underground duct banks, transformer vaults, and 400A–1200A+ estate power without utility delays.
              </div>
              <div style="background: rgba(4, 7, 13, 0.85); border: 1px solid rgba(212, 175, 55, 0.35); border-radius: 12px; padding: 12px 16px; font-size: 0.88rem; color: #e2e8f0; line-height: 1.55;">
                <strong style="color: #d4af37;">✦ CCDC 5B Open-Book Cost Control:</strong> You see every original trade bid and supplier invoice in our 24/7 Portal—zero hidden markups.
              </div>
            </div>
          </div>

          <div style="display: flex; gap: 14px; flex-wrap: wrap;">
            <a href="/about-us-general-contractor-squamish/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; flex: 1 1 210px;">
              <span>🏛️ Meet Wayne Stevenson →</span>
            </a>
            <a href="/feasibility-plan/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; flex: 1 1 210px;">
              <span>📐 Start Your Build Plan →</span>
            </a>
          </div>
        </div>
      </div>
    </div>

  </section>

  <!-- =========================================================================
       4. INTERACTIVE SQUARE-FOOT ($/SQ FT) & TURNKEY BUILD COST CALCULATOR
       ========================================================================= -->
  <section id="sqft-calculator" style="max-width: 1280px; margin: 36px auto 80px auto; padding: 0 20px;">
    <div style="background: linear-gradient(145deg, rgba(12, 19, 36, 0.98) 0%, rgba(4, 7, 13, 0.99) 65%, rgba(15, 23, 42, 0.97) 100%); border: 1.5px solid #d4af37; border-radius: 22px; padding: clamp(28px, 4vw, 46px); box-shadow: 0 28px 65px rgba(0, 0, 0, 0.92), 0 0 36px rgba(212, 175, 55, 0.18);">
      
      <!-- Centered Calculator Header -->
      <div style="text-align: center; max-width: 900px; margin: 0 auto 34px auto;">
        <div class="kp-kicker-pill-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(56, 189, 248, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important;">
          <span>📐 2026 SEA-TO-SKY &amp; NORTH SHORE SQUARE-FOOT COST ESTIMATOR</span>
        </div>
        <h2 style="font-size: clamp(1.65rem, 2.5vw, 2.25rem); font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.22; text-transform: uppercase; text-align: center;">
          How Much Does It Cost Per Square Foot<br>
          <span style="color: #d4af37;">To Build Your Custom Home?</span>
        </h2>
        <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.68; margin: 0;">
          Select your target municipality, home square footage, and site servicing tier below to see real-world <strong style="color: #d4af37;">cost-per-square-foot ($/sq ft)</strong> ranges, where every dollar goes, and how our open-book management protects your budget.
        </p>
      </div>

      <!-- Two-Column Calculator Grid -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 32px; align-items: stretch;">
        
        <!-- LEFT COLUMN: Easy Step-by-Step Controls -->
        <div style="background: rgba(4, 7, 13, 0.85); border: 1px solid rgba(212, 175, 55, 0.38); border-radius: 18px; padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <!-- Step 1: Geo Location Buttons -->
            <div style="margin-bottom: 26px;">
              <label style="display: block; font-family: 'Outfit', sans-serif; font-size: 0.84rem; font-weight: 800; color: #f8fafc; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">
                1. Choose Your Geo Municipality
              </label>
              <div id="kpSimCorridorBtns" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <button type="button" data-corridor="westvan" class="kp-sim-corridor-btn active" style="padding: 13px 14px; border-radius: 14px; border: 1.5px solid #d4af37; background: #04070d; color: #ffffff; font-family: 'Outfit', sans-serif; text-align: left; cursor: pointer; box-shadow: inset 0 0 14px rgba(212,175,55,0.18);">
                  <div style="color: #d4af37; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;">📍 West Vancouver</div>
                  <div style="font-size: 0.9rem; font-weight: 800; margin-top: 2px;">$790 – $930 / sq ft</div>
                </button>
                <button type="button" data-corridor="whistler" class="kp-sim-corridor-btn" style="padding: 13px 14px; border-radius: 14px; border: 1px solid rgba(56, 189, 248, 0.35); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: left; cursor: pointer;">
                  <div style="color: #38bdf8; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;">📍 Whistler Alpine</div>
                  <div style="font-size: 0.9rem; font-weight: 800; margin-top: 2px;">$840 – $990 / sq ft</div>
                </button>
                <button type="button" data-corridor="squamish" class="kp-sim-corridor-btn" style="padding: 13px 14px; border-radius: 14px; border: 1px solid rgba(212, 175, 55, 0.35); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: left; cursor: pointer;">
                  <div style="color: #d4af37; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;">📍 Squamish</div>
                  <div style="font-size: 0.9rem; font-weight: 800; margin-top: 2px;">$680 – $820 / sq ft</div>
                </button>
                <button type="button" data-corridor="northvan" class="kp-sim-corridor-btn" style="padding: 13px 14px; border-radius: 14px; border: 1px solid rgba(56, 189, 248, 0.35); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: left; cursor: pointer;">
                  <div style="color: #38bdf8; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;">📍 North Vancouver</div>
                  <div style="font-size: 0.9rem; font-weight: 800; margin-top: 2px;">$740 – $880 / sq ft</div>
                </button>
              </div>
            </div>

            <!-- Step 2: Home Size Slider -->
            <div style="margin-bottom: 26px;">
              <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px;">
                <label for="kpSimSqft" style="font-family: 'Outfit', sans-serif; font-size: 0.84rem; font-weight: 800; color: #f8fafc; text-transform: uppercase; letter-spacing: 0.08em;">
                  2. Slide Home Square Footage
                </label>
                <span id="kpSimSqftDisplay" style="font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 900; color: #d4af37;">4,500 sq ft</span>
              </div>
              <input type="range" id="kpSimSqft" min="2500" max="10000" step="250" value="4500" style="width: 100%; accent-color: #d4af37; cursor: pointer; height: 8px; border-radius: 9999px;">
              <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #94a3b8; margin-top: 8px; font-weight: 700;">
                <span>2,500 sq ft (Custom Home)</span>
                <span>5,000 sq ft (Luxury Estate)</span>
                <span>10,000 sq ft (Compound)</span>
              </div>
            </div>

            <!-- Step 3: Site & Utility Scope -->
            <div style="margin-bottom: 20px;">
              <label style="display: block; font-family: 'Outfit', sans-serif; font-size: 0.84rem; font-weight: 800; color: #f8fafc; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px;">
                3. Select Lot &amp; Underground Power Scope
              </label>
              <div id="kpSimCivilBtns" style="display: grid; grid-template-columns: 1fr; gap: 10px;">
                <button type="button" data-civil="standard" class="kp-sim-civil-btn active" style="padding: 12px 16px; border-radius: 14px; border: 1.5px solid #38bdf8; background: #04070d; color: #ffffff; font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 800; text-align: left; cursor: pointer; box-shadow: inset 0 0 14px rgba(56,189,248,0.16);">
                  🏡 Standard Custom Lot + Underground 200A–400A Power Trenching
                </button>
                <button type="button" data-civil="pmt" class="kp-sim-civil-btn" style="padding: 12px 16px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.16); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; font-size: 0.82rem; font-weight: 700; text-align: left; cursor: pointer;">
                  ⚡ Steep Bedrock / Estate Lot + BC Hydro ES54 Transformer Vault (400A–800A+)
                </button>
              </div>
            </div>
          </div>

          <div style="padding: 14px 16px; background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.32); border-radius: 12px; font-size: 0.8rem; color: #e2e8f0; line-height: 1.55;">
            <strong style="color: #d4af37;">Open-Book Guarantee:</strong> Unlike fixed-price builders who hide 20%–30% markups inside lump-sum quotes, you pay exact audited trade invoices plus a transparent management fee.
          </div>
        </div>

        <!-- RIGHT COLUMN: Crystal-Clear $/sq ft Breakdown & Total Turnkey Readout -->
        <div style="background: rgba(4, 7, 13, 0.92); border: 1px solid rgba(56, 189, 248, 0.45); border-radius: 18px; padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <!-- Top 3 KPI Readout Boxes -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 22px;">
              <div style="background: #04070d; border: 1.5px solid #d4af37; border-radius: 14px; padding: 16px; text-align: center; box-shadow: inset 0 0 16px rgba(212, 175, 55, 0.14);">
                <div style="font-size: 0.68rem; font-weight: 800; color: #d4af37; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">Cost Per Square Foot</div>
                <div id="kpSimSqftRateBig" style="font-family: 'Outfit', sans-serif; font-size: 1.32rem; font-weight: 900; color: #ffffff;">$790 – $930 / sq ft</div>
                <div id="kpSimGeoBadge" style="font-size: 0.72rem; color: #d4af37; margin-top: 4px; font-weight: 700;">📍 West Vancouver</div>
              </div>
              <div style="background: #04070d; border: 1.5px solid #38bdf8; border-radius: 14px; padding: 16px; text-align: center; box-shadow: inset 0 0 16px rgba(56, 189, 248, 0.14);">
                <div style="font-size: 0.68rem; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">Est. Turnkey Build Total</div>
                <div id="kpSimBudgetBand" style="font-family: 'Outfit', sans-serif; font-size: 1.32rem; font-weight: 900; color: #ffffff;">$3.60M – $4.27M</div>
                <div id="kpSimCivilNote" style="font-size: 0.72rem; color: #cbd5e1; margin-top: 4px;">Includes Underground Hydro</div>
              </div>
              <div style="background: #04070d; border: 1px solid rgba(212, 175, 55, 0.55); border-radius: 14px; padding: 16px; text-align: center;">
                <div style="font-size: 0.68rem; font-weight: 800; color: #d4af37; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">Open-Book Client Savings</div>
                <div id="kpSimFiduciarySaved" style="font-family: 'Outfit', sans-serif; font-size: 1.32rem; font-weight: 900; color: #38bdf8;">$360,000 – $510,000</div>
                <div style="font-size: 0.72rem; color: #cbd5e1; margin-top: 4px;">Saved vs. Broker Markups</div>
              </div>
            </div>

            <!-- Clear 3-Line Square-Foot Cost Breakdown -->
            <div style="background: #04070d; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 18px 20px; margin-bottom: 22px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                <span id="kpSimSpecHeader" style="font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.08em;">📍 WEST VANCOUVER SQUARE-FOOT BREAKDOWN</span>
                <span style="font-size: 0.72rem; color: #d4af37; font-weight: 800;">CCDC 5B OPEN-BOOK</span>
              </div>

              <div style="display: grid; gap: 12px; font-size: 0.85rem; color: #e2e8f0;">
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; padding-bottom: 8px; border-bottom: 1px dashed rgba(255,255,255,0.08);">
                  <div>
                    <strong style="color: #d4af37;">1. Site Prep, Rock, Concrete &amp; Underground Hydro:</strong>
                    <div id="kpSimDesc1" style="font-size: 0.78rem; color: #94a3b8;">Excavation, rock anchors, waterproofed foundation &amp; BC Hydro ES54 trenching</div>
                  </div>
                  <span id="kpSimBreak1" style="font-family: 'Outfit', sans-serif; font-weight: 900; color: #d4af37; white-space: nowrap;">$175 – $210 / sq ft</span>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; padding-bottom: 8px; border-bottom: 1px dashed rgba(255,255,255,0.08);">
                  <div>
                    <strong style="color: #38bdf8;">2. Structural Framing, Roof &amp; Step Code 5 Glass:</strong>
                    <div id="kpSimDesc2" style="font-size: 0.78rem; color: #94a3b8;">Steel &amp; Douglas Fir timber structure, triple-pane windows &amp; exterior insulation</div>
                  </div>
                  <span id="kpSimBreak2" style="font-family: 'Outfit', sans-serif; font-weight: 900; color: #38bdf8; white-space: nowrap;">$315 – $370 / sq ft</span>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
                  <div>
                    <strong style="color: #d4af37;">3. Custom Interior Finishes, Millwork &amp; Mechanical:</strong>
                    <div id="kpSimDesc3" style="font-size: 0.78rem; color: #94a3b8;">Architectural millwork, stone, radiant floor heating, smart home &amp; 2-5-10 Warranty</div>
                  </div>
                  <span id="kpSimBreak3" style="font-family: 'Outfit', sans-serif; font-weight: 900; color: #d4af37; white-space: nowrap;">$300 – $350 / sq ft</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Centered Pure-Black Gold & Blue Calculator Action Buttons -->
          <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;">
            <a href="/feasibility-plan/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; flex: 1 1 240px;">
              <span>📐 Get Exact Lot &amp; Square-Foot Cost Plan →</span>
            </a>
            <a href="/contact-general-contractor-squamish/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; flex: 1 1 200px;">
              <span>📞 Discuss My Project With Wayne →</span>
            </a>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- =========================================================================
       5. THE 3 CORE KEYSTONE ADVANTAGES (EQUAL-HEIGHT 3-COLUMN GRID)
       ========================================================================= -->
  <section class="pillar-matrix-section" id="civil" style="max-width: 1280px; margin: 0 auto 80px auto; padding: 0 20px;">
    <div style="text-align: center; max-width: 900px; margin: 0 auto 40px auto;">
      <div class="kp-kicker-pill-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(212, 175, 55, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important;">
        <span>⚡ WHY ESTATE OWNERS &amp; ARCHITECTS CHOOSE KEYSTONE</span>
      </div>
      <h2 style="font-size: clamp(1.65rem, 2.5vw, 2.25rem); font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.22; text-transform: uppercase; text-align: center;">
        Three Unmatched <span style="color: #d4af37; white-space: nowrap;">Master Builder Advantages</span>
      </h2>
      <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.68; margin: 0;">
        We unite licensed residential construction (#52603), registered BC Hydro ES54 civil contracting, and 24/7 open-book accounting under one roof across <strong style="color: #f8fafc;">West Vancouver, Whistler, Squamish, and North Vancouver</strong>.
      </p>
    </div>

    <div class="kp-3col-equal-grid" style="display: grid !important; grid-template-columns: repeat(3, minmax(0, 1fr)) !important; gap: 26px !important; align-items: stretch !important;">
      <!-- Card 1 -->
      <article style="background: rgba(10, 16, 30, 0.95); border: 1.5px solid rgba(212, 175, 55, 0.55); border-radius: 18px; padding: 30px 26px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 18px 45px rgba(0,0,0,0.8);">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <span style="padding: 5px 14px; border-radius: 9999px; background: #04070d; border: 1px solid #d4af37; color: #d4af37; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em;">01 • LICENSE #52603</span>
            <span style="font-size: 0.72rem; font-weight: 800; color: #94a3b8;">📍 SEA-TO-SKY &amp; NORTH SHORE</span>
          </div>
          <h3 style="font-size: 1.32rem; font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.25;">Direct Master Builder Site Command</h3>
          <p style="color: #cbd5e1; font-size: 0.93rem; line-height: 1.68; margin: 0 0 18px 0;">
            Every foundation anchor, structural steel frame, and Step Code 5 airtight envelope detail is inspected on-site by Wayne Stevenson—backed by mandatory 2-5-10 Year National Home Warranty coverage.
          </p>
        </div>
        <a href="/about-us-general-contractor-squamish/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; width: 100%;">
          <span>🏛️ Verify Builder Credentials →</span>
        </a>
      </article>

      <!-- Card 2 -->
      <article style="background: rgba(10, 16, 30, 0.95); border: 1.5px solid rgba(56, 189, 248, 0.55); border-radius: 18px; padding: 30px 26px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 18px 45px rgba(0,0,0,0.8);">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <span style="padding: 5px 14px; border-radius: 9999px; background: #04070d; border: 1px solid #38bdf8; color: #38bdf8; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em;">02 • BC HYDRO ES54</span>
            <span style="font-size: 0.72rem; font-weight: 800; color: #94a3b8;">📍 IN-HOUSE CIVIL CREW</span>
          </div>
          <h3 style="font-size: 1.32rem; font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.25;">BC Hydro ES54 Underground Civil</h3>
          <p style="color: #cbd5e1; font-size: 0.93rem; line-height: 1.68; margin: 0 0 18px 0;">
            Instead of waiting 6 months on third-party utility contractors, our registered ES54 civil team self-performs rock trenching, high-voltage duct banks, and pad-mounted transformer vaults during foundation excavation.
          </p>
        </div>
        <a href="/bc-hydro-registered-civil-contractor/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; width: 100%;">
          <span>⚡ Explore ES54 Civil Scope →</span>
        </a>
      </article>

      <!-- Card 3 -->
      <article style="background: rgba(10, 16, 30, 0.95); border: 1.5px solid rgba(212, 175, 55, 0.55); border-radius: 18px; padding: 30px 26px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 18px 45px rgba(0,0,0,0.8);">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
            <span style="padding: 5px 14px; border-radius: 9999px; background: #04070d; border: 1px solid #d4af37; color: #d4af37; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em;">03 • CCDC 5B PORTAL</span>
            <span style="font-size: 0.72rem; font-weight: 800; color: #94a3b8;">📍 100% OPEN-BOOK AUDIT</span>
          </div>
          <h3 style="font-size: 1.32rem; font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.25;">24/7 Open-Book Fiduciary Portal</h3>
          <p style="color: #cbd5e1; font-size: 0.93rem; line-height: 1.68; margin: 0 0 18px 0;">
            Log in anytime to review 3-bid subcontractor tenders, original supplier invoices, daily job-site photos, and milestone draw certificates—with 100% of trade discounts credited directly to you.
          </p>
        </div>
        <a href="/client-login/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; width: 100%;">
          <span>📊 Open 24/7 Client Portal →</span>
        </a>
      </article>
    </div>
  </section>

  <!-- =========================================================================
       6. THE 5 PILLARS OF THE KEYSTONE TURNKEY BUILD PROTOCOL (#execution-roadmap)
       ========================================================================= -->
  <section id="execution-roadmap" style="max-width: 1280px; margin: 0 auto 80px auto; padding: 0 20px;">
    <div style="background: linear-gradient(145deg, rgba(10, 16, 30, 0.96) 0%, rgba(4, 7, 13, 0.99) 100%); border: 1.5px solid rgba(56, 189, 248, 0.55); border-radius: 22px; padding: clamp(28px, 3.8vw, 44px); box-shadow: 0 24px 60px rgba(0, 0, 0, 0.88);">
      
      <div style="text-align: center; max-width: 900px; margin: 0 auto 32px auto;">
        <div class="kp-kicker-pill-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(56, 189, 248, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important;">
          <span>🧭 FIVE PILLARS OF TURNKEY EXECUTION • START TO FINISH</span>
        </div>
        <h2 style="font-size: clamp(1.65rem, 2.45vw, 2.2rem); font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.22; text-transform: uppercase; text-align: center;">
          The 5-Pillar <span style="color: #d4af37; white-space: nowrap;">Keystone Protocol Build</span>
        </h2>
        <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.68; margin: 0;">
          Every custom estate across <strong style="color: #f8fafc;">West Vancouver, Whistler, Squamish, and North Vancouver</strong> follows our 5-pillar critical path—eliminating permit delays, rock excavation surprises, and budget overruns. Click any pillar below to inspect the deliverables.
        </p>
      </div>

      <!-- 5 Equal-Height Pillar Cards Grid -->
      <div id="kpRoadmapTabs" class="kp-5pillars-grid" style="display: grid !important; grid-template-columns: repeat(5, minmax(0, 1fr)) !important; gap: 14px !important; align-items: stretch !important; margin-bottom: 26px;">
        <button type="button" data-stage="0" class="kp-roadmap-tab active" style="padding: 18px 16px; border-radius: 16px; border: 1.5px solid #d4af37; background: #04070d; color: #ffffff; font-family: 'Outfit', sans-serif; text-align: center; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between; box-shadow: inset 0 0 16px rgba(212,175,55,0.18);">
          <div style="font-size: 0.7rem; font-weight: 800; color: #d4af37; letter-spacing: 0.1em; text-transform: uppercase;">PILLAR 01</div>
          <div style="font-size: 0.95rem; font-weight: 800; margin: 8px 0;">Lot, Zoning &amp; Cost Feasibility</div>
          <div style="font-size: 0.72rem; color: #94a3b8;">Weeks 1–4</div>
        </button>

        <button type="button" data-stage="1" class="kp-roadmap-tab" style="padding: 18px 16px; border-radius: 16px; border: 1px solid rgba(56, 189, 248, 0.4); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: center; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="font-size: 0.7rem; font-weight: 800; color: #38bdf8; letter-spacing: 0.1em; text-transform: uppercase;">PILLAR 02</div>
          <div style="font-size: 0.95rem; font-weight: 800; margin: 8px 0;">Engineering &amp; Permit Lock</div>
          <div style="font-size: 0.72rem; color: #94a3b8;">Months 2–4</div>
        </button>

        <button type="button" data-stage="2" class="kp-roadmap-tab" style="padding: 18px 16px; border-radius: 16px; border: 1px solid rgba(212, 175, 55, 0.4); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: center; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="font-size: 0.7rem; font-weight: 800; color: #d4af37; letter-spacing: 0.1em; text-transform: uppercase;">PILLAR 03</div>
          <div style="font-size: 0.95rem; font-weight: 800; margin: 8px 0;">Rock Excavation &amp; ES54 Hydro</div>
          <div style="font-size: 0.72rem; color: #94a3b8;">Months 5–8</div>
        </button>

        <button type="button" data-stage="3" class="kp-roadmap-tab" style="padding: 18px 16px; border-radius: 16px; border: 1px solid rgba(56, 189, 248, 0.4); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: center; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="font-size: 0.7rem; font-weight: 800; color: #38bdf8; letter-spacing: 0.1em; text-transform: uppercase;">PILLAR 04</div>
          <div style="font-size: 0.95rem; font-weight: 800; margin: 8px 0;">Seismic Frame &amp; Step 5 Shell</div>
          <div style="font-size: 0.72rem; color: #94a3b8;">Months 9–15</div>
        </button>

        <button type="button" data-stage="4" class="kp-roadmap-tab" style="padding: 18px 16px; border-radius: 16px; border: 1px solid rgba(212, 175, 55, 0.4); background: #04070d; color: #cbd5e1; font-family: 'Outfit', sans-serif; text-align: center; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="font-size: 0.7rem; font-weight: 800; color: #d4af37; letter-spacing: 0.1em; text-transform: uppercase;">PILLAR 05</div>
          <div style="font-size: 0.95rem; font-weight: 800; margin: 8px 0;">Custom Finish &amp; 2-5-10 Warranty</div>
          <div style="font-size: 0.72rem; color: #94a3b8;">Months 16–20</div>
        </button>
      </div>

      <!-- Active Pillar Detail Readout Box -->
      <div id="kpRoadmapDetailPanel" style="background: #04070d; border: 1.5px solid rgba(212, 175, 55, 0.55); border-radius: 18px; padding: clamp(22px, 3vw, 32px); display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 28px; align-items: center;">
        <div>
          <div id="kpRoadmapBadge" style="display: inline-block; padding: 5px 14px; border-radius: 9999px; background: #04070d; border: 1px solid #d4af37; color: #d4af37; font-family: 'Outfit', sans-serif; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px;">
            PILLAR 01 • LOT, ZONING &amp; COST FEASIBILITY
          </div>
          <h3 id="kpRoadmapTitle" style="font-size: 1.45rem; font-weight: 800; color: #ffffff; margin: 0 0 12px 0; line-height: 1.25;">
            Lot Feasibility, Rock Profile &amp; Square-Foot Budget Lock
          </h3>
          <p id="kpRoadmapDesc" style="color: #cbd5e1; font-size: 0.96rem; line-height: 1.7; margin: 0;">
            Before you spend $100,000+ on architectural plans that exceed your budget, we inspect your lot’s zoning setbacks, bedrock depth, and BC Hydro connection distance—delivering a clear 40-division open-book cost plan from Day 1.
          </p>
        </div>
        <div style="background: rgba(10, 16, 30, 0.9); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 14px; padding: 20px;">
          <div style="font-family: 'Outfit', sans-serif; font-size: 0.78rem; font-weight: 800; color: #38bdf8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px;">
            ✓ Key Deliverables Included In This Pillar
          </div>
          <ul id="kpRoadmapBullets" style="list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; font-size: 0.86rem; color: #f8fafc; line-height: 1.55;">
            <li><span style="color: #d4af37; font-weight: 900;">✦</span> <strong>Municipal Zoning &amp; Setback Check:</strong> Maximum buildable square footage &amp; view cones</li>
            <li><span style="color: #d4af37; font-weight: 900;">✦</span> <strong>Bedrock &amp; Slope Assessment:</strong> Excavation, rock anchoring &amp; retaining wall budget</li>
            <li><span style="color: #d4af37; font-weight: 900;">✦</span> <strong>BC Hydro ES54 Power Layout:</strong> Underground duct bank &amp; transformer siting</li>
            <li><span style="color: #d4af37; font-weight: 900;">✦</span> <strong>40-Division Open-Book Pro-Forma:</strong> Transparent line-item square-foot budget</li>
          </ul>
        </div>
      </div>

    </div>
  </section>

  <!-- =========================================================================
       7. 3-COLUMN REGIONAL ESTATE & CIVIL SHOWCASE (WITH WAYNE'S 3 PICTURES & GEO BADGES)
       ========================================================================= -->
  <section class="portfolio-showcase-section" id="portfolio" style="max-width: 1280px; margin: 0 auto 80px auto; padding: 0 20px;">
    <div style="text-align: center; max-width: 900px; margin: 0 auto 40px auto;">
      <div class="kp-kicker-pill-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(212, 175, 55, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important;">
        <span>🏔️ REGIONAL CUSTOM HOME &amp; ESTATE SHOWCASE • GEO CORRIDORS</span>
      </div>
      <h2 style="font-size: clamp(1.65rem, 2.5vw, 2.25rem); font-weight: 800; color: #ffffff; line-height: 1.22; margin: 0 0 12px 0; text-transform: uppercase; text-align: center;">
        Sea-to-Sky &amp; North Shore <span style="color: #d4af37; white-space: nowrap;">Signature Estate Builds</span>
      </h2>
      <p style="color: #cbd5e1; font-size: 1rem; line-height: 1.68; margin: 0;">
        Explore how we tailor structural engineering, Step Code 5 energy envelopes, and BC Hydro ES54 underground power to each specific municipality across <strong style="color: #f8fafc;">Whistler, West Vancouver, Squamish, and North Vancouver</strong>.
      </p>
    </div>

    <div class="kp-3col-equal-grid" style="display: grid !important; grid-template-columns: repeat(3, minmax(0, 1fr)) !important; gap: 26px !important; align-items: stretch !important; margin-bottom: 36px;">
      
      <!-- Column 01: Whistler Alpine (With Picture Kept) -->
      <article style="background: rgba(10, 16, 30, 0.94); border: 1.5px solid rgba(212, 175, 55, 0.55); border-radius: 18px; overflow: hidden; box-shadow: 0 20px 48px rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="height: 240px; position: relative; overflow: hidden;">
            <img decoding="async" src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/whistler_luxury_estate.jpg" alt="Whistler Alpine Custom Ski-In Estate" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
            <div style="position: absolute; top: 14px; left: 14px; background: #04070d; border: 1.5px solid #d4af37; color: #d4af37; padding: 6px 14px; border-radius: 9999px; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">
              📍 WHISTLER, BC • ALPINE ESTATES
            </div>
          </div>
          <div style="padding: 26px 24px 18px 24px;">
            <h3 style="font-size: 1.32rem; font-weight: 800; color: #ffffff; margin: 0 0 10px 0;">Whistler Alpine &amp; Ski-In Residences</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.65; margin: 0 0 16px 0;">
              Built for Whistler’s extreme 4.2 kPa snow loads and Zero Carbon Step Code 5 mandates—featuring heavy Douglas Fir glulam timber, triple-pane European glass walls, and heated snow-melt driveways.
            </p>
            <div style="background: #04070d; border: 1px solid rgba(212, 175, 55, 0.32); border-radius: 12px; padding: 12px 14px; font-size: 0.8rem; color: #e2e8f0; line-height: 1.65;">
              <div><strong style="color: #d4af37;">📍 Geo Areas:</strong> Kadenwood, Blueberry Hill &amp; Sunridge</div>
              <div><strong style="color: #38bdf8;">📐 Typical Build Rate:</strong> $840 – $990 / sq ft</div>
              <div><strong style="color: #d4af37;">⚡ Power &amp; Heat:</strong> 600A Underground + Hydronic Snow-Melt</div>
            </div>
          </div>
        </div>
        <div style="padding: 0 24px 26px 24px;">
          <a href="/whistler-custom-homes/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; width: 100%;">
            <span>📍 Explore Whistler Custom Homes →</span>
          </a>
        </div>
      </article>

      <!-- Column 02: West Vancouver Coastal Concrete (With Picture Kept) -->
      <article style="background: rgba(10, 16, 30, 0.94); border: 1.5px solid rgba(56, 189, 248, 0.55); border-radius: 18px; overflow: hidden; box-shadow: 0 20px 48px rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="height: 240px; position: relative; overflow: hidden;">
            <img decoding="async" src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/west_vancouver_concrete.jpg" alt="West Vancouver Coastal Bluff Architectural Concrete Estate" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
            <div style="position: absolute; top: 14px; left: 14px; background: #04070d; border: 1.5px solid #38bdf8; color: #38bdf8; padding: 6px 14px; border-radius: 9999px; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">
              📍 WEST VANCOUVER, BC • COASTAL BLUFF
            </div>
          </div>
          <div style="padding: 26px 24px 18px 24px;">
            <h3 style="font-size: 1.32rem; font-weight: 800; color: #ffffff; margin: 0 0 10px 0;">West Vancouver Oceanfront &amp; Bluff Estates</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.65; margin: 0 0 16px 0;">
              Architectural board-formed concrete and steel residences anchored directly into coastal granodiorite bedrock—engineered with cantilevered oceanfront terraces and marine-grade curtain wall glazing.
            </p>
            <div style="background: #04070d; border: 1px solid rgba(56, 189, 248, 0.32); border-radius: 12px; padding: 12px 14px; font-size: 0.8rem; color: #e2e8f0; line-height: 1.65;">
              <div><strong style="color: #38bdf8;">📍 Geo Areas:</strong> British Properties, Altamont &amp; Caulfeild</div>
              <div><strong style="color: #d4af37;">📐 Typical Build Rate:</strong> $790 – $930 / sq ft</div>
              <div><strong style="color: #38bdf8;">🏛️ Structure:</strong> Tensioned Rock Anchors &amp; Seismic Concrete</div>
            </div>
          </div>
        </div>
        <div style="padding: 0 24px 26px 24px;">
          <a href="/west-vancouver-custom-homes/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; width: 100%;">
            <span>📍 Explore West Vancouver Builds →</span>
          </a>
        </div>
      </article>

      <!-- Column 03: Squamish & North Vancouver (With Picture Kept) -->
      <article style="background: rgba(10, 16, 30, 0.94); border: 1.5px solid rgba(212, 175, 55, 0.55); border-radius: 18px; overflow: hidden; box-shadow: 0 20px 48px rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div style="height: 240px; position: relative; overflow: hidden;">
            <img decoding="async" src="https://keystonepossibilities.ca/wp-content/uploads/2026/09/luxury-home-construction-squamish-bc-aerial.jpeg" alt="Squamish &amp; North Shore Custom Estates and BC Hydro ES54 Civil" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
            <div style="position: absolute; top: 14px; left: 14px; background: #04070d; border: 1.5px solid #d4af37; color: #d4af37; padding: 6px 14px; border-radius: 9999px; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;">
              📍 SQUAMISH &amp; NORTH VANCOUVER, BC
            </div>
          </div>
          <div style="padding: 26px 24px 18px 24px;">
            <h3 style="font-size: 1.32rem; font-weight: 800; color: #ffffff; margin: 0 0 10px 0;">Squamish Acreages &amp; North Shore Estates</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.65; margin: 0 0 16px 0;">
              Multi-generational custom homes, carriage houses, and steep-canyon residences featuring full in-house BC Hydro ES54 underground power trenching, transformer vaults, and Step Code 5 insulation.
            </p>
            <div style="background: #04070d; border: 1px solid rgba(212, 175, 55, 0.32); border-radius: 12px; padding: 12px 14px; font-size: 0.8rem; color: #e2e8f0; line-height: 1.65;">
              <div><strong style="color: #d4af37;">📍 Geo Areas:</strong> Garibaldi Highlands, Crumpit &amp; Edgemont</div>
              <div><strong style="color: #38bdf8;">📐 Typical Build Rate:</strong> $680 – $880 / sq ft</div>
              <div><strong style="color: #d4af37;">⚡ Civil Advantage:</strong> In-House ES54 Underground Servicing</div>
            </div>
          </div>
        </div>
        <div style="padding: 0 24px 26px 24px;">
          <a href="/squamish-custom-homes/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important; width: 100%;">
            <span>📍 Explore Squamish &amp; North Shore →</span>
          </a>
        </div>
      </article>

    </div>

    <!-- Centered Full Portfolio Button -->
    <div style="text-align: center;">
      <a href="/portfolio-general-contractor-squamish/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
        <span>🏔️ View Full 9-Residence &amp; Civil Infrastructure Portfolio →</span>
      </a>
    </div>
  </section>

  <!-- =========================================================================
       8. CLEAN CENTERED EXECUTIVE GATEWAY BANNER (REPLACING CLUTTERED BOTTOM CONTACT LIST)
       ========================================================================= -->
  <section id="executive-gateway" style="max-width: 1280px; margin: 0 auto 76px auto; padding: 0 20px;">
    <div style="background: radial-gradient(circle at top center, rgba(212, 175, 55, 0.16) 0%, rgba(10, 16, 30, 0.98) 65%, #04070d 100%); border: 1.5px solid #d4af37; border-radius: 22px; padding: clamp(34px, 4.5vw, 56px); box-shadow: 0 28px 65px rgba(0,0,0,0.9), 0 0 32px rgba(212, 175, 55, 0.16); text-align: center;">
      <div class="kp-kicker-pill-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; padding: 6px 18px !important; border-radius: 9999px !important; background: #04070d !important; border: 1px solid rgba(212, 175, 55, 0.78) !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: 'Outfit', sans-serif !important; font-size: 0.74rem !important; font-weight: 800 !important; letter-spacing: 0.14em !important; text-transform: uppercase !important; margin-bottom: 14px !important; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important;">
        <span>🏛️ READY TO PLAN YOUR CUSTOM BUILD OR CIVIL PROJECT?</span>
      </div>
      <h2 style="font-size: clamp(1.65rem, 2.5vw, 2.25rem); font-weight: 800; color: #ffffff; line-height: 1.22; margin: 0 auto 14px auto; max-width: 920px; text-transform: uppercase; text-align: center;">
        Lock In Your Pre-Construction<br>
        <span style="color: #d4af37;">Cost &amp; Feasibility Plan Today</span>
      </h2>
      <p style="color: #cbd5e1; font-size: 1.02rem; line-height: 1.7; max-width: 820px; margin: 0 auto 24px auto;">
        Work directly with licensed Master Builder <strong style="color: #ffffff;">Wayne Stevenson (#52603)</strong> to audit your lot, verify BC Hydro ES54 underground power requirements, and establish a transparent CCDC 5B line-item budget—with 100% of your pre-construction retainer credited toward your build.
      </p>

      <!-- Geo Service Corridor Confirmation Row -->
      <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 28px;">
        <a href="/west-vancouver-custom-homes/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 West Vancouver</span></a>
        <a href="/whistler-custom-homes/" class="kp-geo-pill kp-geo-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(56, 189, 248, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 Whistler</span></a>
        <a href="/squamish-custom-homes/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 Squamish HQ</span></a>
        <a href="/north-vancouver-custom-homes/" class="kp-geo-pill kp-geo-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(56, 189, 248, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(56, 189, 248, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 North Vancouver</span></a>
        <a href="/north-vancouver-multiplex-conversions/" class="kp-geo-pill" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 6px !important; background: #04070d !important; background-color: #04070d !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid rgba(212, 175, 55, 0.78) !important; border-radius: 9999px !important; padding: 9px 18px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.75), inset 0 0 12px rgba(212, 175, 55, 0.12) !important; transition: all 0.25s ease !important;"><span>📍 Vancouver Multiplex</span></a>
      </div>

      <!-- Centered Dual Pure-Black CTA Buttons -->
      <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 16px;">
        <a href="/feasibility-plan/" class="kp-btn-sovereign-gold" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.85), 0 0 16px rgba(212, 175, 55, 0.22), inset 0 0 18px rgba(212, 175, 55, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
          <span>📐 Start Your Custom Home &amp; Cost Plan →</span>
        </a>
        <a href="/contact-general-contractor-squamish/" class="kp-btn-blue" style="display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 8px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; padding: 14px 28px !important; font-family: 'Outfit', sans-serif !important; font-size: 0.84rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0, 0, 0, 0.82), 0 0 16px rgba(56, 189, 248, 0.22), inset 0 0 18px rgba(56, 189, 248, 0.14) !important; cursor: pointer !important; transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important; box-sizing: border-box !important;">
          <span>📞 Direct Consultation Desk • (604) 848-9688 →</span>
        </a>
      </div>
    </div>
  </section>

  <!-- =========================================================================
       INTERACTIVE JAVASCRIPT ENGINE ($/SQ FT CALCULATOR + 5 PILLARS + WORD-WAVE)
       ========================================================================= -->
  <script id="kp-v460-master-script">(function() { function initKeystoneHomepageV460() { var oldSt = document.getElementById('kp-v460-head-styles'); if (oldSt) oldSt.remove(); var st = document.createElement('style'); st.id = 'kp-v460-head-styles'; st.textContent = [ '.kp-homepage-wrapper p:empty, .kp-homepage-wrapper br:empty, .superintendent-grid > p, .three-pillar-grid > p, .portfolio-grid > p, .kp-five-pillars-grid > p { display: none !important; }', '.kp-homepage-wrapper h1, .kp-homepage-wrapper h2, .kp-homepage-wrapper h3, .kp-homepage-wrapper h4 { border-bottom: none !important; font-family: "Outfit", -apple-system, BlinkMacSystemFont, sans-serif !important; }', '@keyframes kpWaveGold { 0%, 100% { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-shadow: 0 0 10px rgba(212,175,55,0.55); transform: translateY(0); } 50% { color: #f6d365 !important; -webkit-text-fill-color: #f6d365 !important; text-shadow: 0 0 18px rgba(212,175,55,0.98), 0 0 28px rgba(56,189,248,0.45); transform: translateY(-1px); } }', '@keyframes kpWaveBlue { 0%, 100% { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-shadow: 0 0 10px rgba(56,189,248,0.55); transform: translateY(0); } 50% { color: #7dd3fc !important; -webkit-text-fill-color: #7dd3fc !important; text-shadow: 0 0 18px rgba(56,189,248,0.98), 0 0 28px rgba(212,175,55,0.45); transform: translateY(-1px); } }', '@keyframes kpHaloPulseGold { 0%, 100% { box-shadow: 0 10px 26px rgba(0,0,0,0.85), 0 0 14px rgba(212,175,55,0.22), inset 0 0 16px rgba(212,175,55,0.14); border-color: rgba(212,175,55,0.85); } 50% { box-shadow: 0 10px 28px rgba(0,0,0,0.88), 0 0 24px rgba(212,175,55,0.48), inset 0 0 20px rgba(212,175,55,0.24); border-color: #f6d365; } }', '@keyframes kpHaloPulseBlue { 0%, 100% { box-shadow: 0 10px 26px rgba(0,0,0,0.85), 0 0 14px rgba(56,189,248,0.22), inset 0 0 16px rgba(56,189,248,0.14); border-color: rgba(56,189,248,0.82); } 50% { box-shadow: 0 10px 28px rgba(0,0,0,0.88), 0 0 24px rgba(56,189,248,0.48), inset 0 0 20px rgba(56,189,248,0.24); border-color: #7dd3fc; } }', '.kp-wave-word { display: inline-block; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-decoration: none !important; transition: color 0.22s ease, text-shadow 0.22s ease, transform 0.22s ease; }', 'html body .kp-btn-sovereign-gold, html body a.kp-btn-sovereign-gold, html body button.kp-btn-sovereign-gold, html body .kp-subscribe-direct-btn, html body a.kp-subscribe-direct-btn { background: #04070d !important; background-color: #04070d !important; background-image: none !important; border: 1.5px solid #d4af37 !important; border-radius: 9999px !important; text-decoration: none !important; animation: kpHaloPulseGold 3.2s ease-in-out infinite !important; }', 'html body .kp-btn-sovereign-gold, html body .kp-btn-sovereign-gold *, html body .kp-subscribe-direct-btn, html body .kp-subscribe-direct-btn *, html body .kp-kicker-pill-gold, html body .kp-kicker-pill-gold * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-decoration: none !important; }', 'html body .kp-btn-blue, html body a.kp-btn-blue, html body button.kp-btn-blue { background: #04070d !important; background-color: #04070d !important; background-image: none !important; border: 1.5px solid #38bdf8 !important; border-radius: 9999px !important; text-decoration: none !important; animation: kpHaloPulseBlue 3.2s ease-in-out infinite !important; }', 'html body .kp-btn-blue, html body .kp-btn-blue *, html body .kp-kicker-pill-blue, html body .kp-kicker-pill-blue * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-decoration: none !important; }', 'html body .kp-geo-pill, html body a.kp-geo-pill { background: #04070d !important; background-color: #04070d !important; background-image: none !important; border-radius: 9999px !important; text-decoration: none !important; }', 'html body .kp-geo-pill, html body .kp-geo-pill * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; text-decoration: none !important; }', 'html body .kp-btn-sovereign-gold .kp-wave-word, html body .kp-subscribe-direct-btn .kp-wave-word, html body .kp-geo-pill:not(.kp-geo-blue) .kp-wave-word, html body .kp-kicker-pill-gold .kp-wave-word { animation: kpWaveGold 2.6s ease-in-out infinite !important; animation-delay: calc(var(--w-idx, 0) * 0.14s) !important; }', 'html body .kp-btn-blue .kp-wave-word, html body .kp-geo-pill.kp-geo-blue .kp-wave-word, html body .kp-kicker-pill-blue .kp-wave-word { animation: kpWaveBlue 2.6s ease-in-out infinite !important; animation-delay: calc(var(--w-idx, 0) * 0.14s) !important; }', 'html body .kp-btn-sovereign-gold:hover, html body .kp-subscribe-direct-btn:hover, html body .kp-geo-pill:not(.kp-geo-blue):hover { background: #04070d !important; border-color: #f6d365 !important; box-shadow: 0 0 30px rgba(212,175,55,0.65), 0 0 16px rgba(56,189,248,0.32), inset 0 0 22px rgba(212,175,55,0.28) !important; transform: translateY(-2px) !important; }', 'html body .kp-btn-blue:hover, html body .kp-geo-pill.kp-geo-blue:hover { background: #04070d !important; border-color: #7dd3fc !important; box-shadow: 0 0 30px rgba(56,189,248,0.65), 0 0 16px rgba(212,175,55,0.32), inset 0 0 22px rgba(56,189,248,0.28) !important; transform: translateY(-2px) !important; }', 'html body .kp-btn-sovereign-gold:hover .kp-wave-word, html body .kp-subscribe-direct-btn:hover .kp-wave-word, html body .kp-geo-pill:not(.kp-geo-blue):hover .kp-wave-word, html body .kp-kicker-pill-gold:hover .kp-wave-word { animation: kpWaveGold 0.85s ease-in-out infinite !important; animation-delay: calc(var(--w-idx, 0) * 0.06s) !important; }', 'html body .kp-btn-blue:hover .kp-wave-word, html body .kp-geo-pill.kp-geo-blue:hover .kp-wave-word, html body .kp-kicker-pill-blue:hover .kp-wave-word { animation: kpWaveBlue 0.85s ease-in-out infinite !important; animation-delay: calc(var(--w-idx, 0) * 0.06s) !important; }', 'html body .kp-social-icon-btn { background: #04070d !important; border: 1.5px solid rgba(212,175,55,0.65) !important; color: #f6d365 !important; box-shadow: 0 6px 18px rgba(0,0,0,0.8), inset 0 0 12px rgba(212,175,55,0.14) !important; }', 'html body .kp-social-icon-btn:hover { border-color: #38bdf8 !important; color: #38bdf8 !important; box-shadow: 0 0 20px rgba(56,189,248,0.55) !important; transform: translateY(-2px) scale(1.06) !important; }', '.kp-3col-equal-grid { display: grid !important; grid-template-columns: repeat(3, minmax(0, 1fr)) !important; gap: 26px !important; align-items: stretch !important; }', '.kp-5pillars-grid { display: grid !important; grid-template-columns: repeat(5, minmax(0, 1fr)) !important; gap: 14px !important; align-items: stretch !important; }', '@media (max-width: 1100px) { .kp-3col-equal-grid { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)) !important; } .kp-5pillars-grid { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)) !important; } }' ].join('\n'); document.head.appendChild(st); document.querySelectorAll('.kp-subscribe-direct-btn, .kp-btn-sovereign-gold, .btn-gold-action, a[style*="linear-gradient"]').forEach(function(btn) { btn.classList.remove('kp-btn-sovereign-gold', 'btn-gold-action', 'kp-btn-primary'); btn.classList.add('kp-btn-sovereign-gold'); btn.setAttribute('style', 'display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 10px !important; min-height: 48px !important; padding: 12px 26px !important; border-radius: 9999px !important; background: #04070d !important; background-color: #04070d !important; background-image: none !important; border: 1.5px solid #d4af37 !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-family: Outfit, sans-serif !important; font-size: 0.82rem !important; font-weight: 800 !important; letter-spacing: 0.07em !important; text-transform: uppercase !important; text-decoration: none !important; box-shadow: 0 10px 26px rgba(0,0,0,0.85), 0 0 16px rgba(212,175,55,0.24), inset 0 0 16px rgba(212,175,55,0.14) !important; transition: all 0.25s ease !important;'); }); var waveSels = '.kp-btn-sovereign-gold, .kp-btn-sovereign-gold, .kp-btn-blue, .kp-geo-pill, .kp-kicker-pill-gold, .kp-kicker-pill-blue, .kp-subscribe-direct-btn, .btn-gold-action, .btn-portal-secondary'; document.querySelectorAll(waveSels).forEach(function(el) { if (el.dataset.kpWaveInit === '1') return; el.dataset.kpWaveInit = '1'; var target = el.querySelector('span:last-child') || el; if (target.children.length > 0) return; var txt = (target.textContent || '').trim(); if (!txt) return; var words = txt.split(' ').filter(Boolean); target.innerHTML = words.map(function(w, i) { return '<span class="kp-wave-word" style="color:#ffffff !important;-webkit-text-fill-color:#ffffff !important;--w-idx:' + i + '">' + w + '</span>'; }).join(' '); }); var corridorData = { westvan: { geo: "📍 West Vancouver", header: "📍 WEST VANCOUVER SQUARE-FOOT BREAKDOWN", rateLow: 790, rateHigh: 930, b1Low: 175, b1High: 210, b2Low: 315, b2High: 370, b3Low: 300, b3High: 350, desc1: "Coastal bedrock anchoring, waterproofed concrete foundation & BC Hydro ES54 trenching", desc2: "Seismic steel & timber framing, cantilevered slabs & Step Code 5 triple-pane glass", desc3: "Custom architectural millwork, natural stone, radiant floor heating & 2-5-10 Warranty" }, whistler: { geo: "📍 Whistler Alpine", header: "📍 WHISTLER ALPINE SQUARE-FOOT BREAKDOWN", rateLow: 840, rateHigh: 990, b1Low: 190, b1High: 230, b2Low: 340, b2High: 390, b3Low: 310, b3High: 370, desc1: "Alpine rock excavation, frost-protected footings, snow-melt apron & ES54 hydro ducting", desc2: "4.2 kPa snow-load glulam timber & steel frame, triple-sealed Step Code 5 envelope", desc3: "Mountain luxury stonework, custom white-oak millwork, air-to-water hydronics & warranty" }, squamish: { geo: "📍 Squamish", header: "📍 SQUAMISH SQUARE-FOOT BREAKDOWN", rateLow: 680, rateHigh: 820, b1Low: 145, b1High: 180, b2Low: 275, b2High: 330, b3Low: 260, b3High: 310, desc1: "Granite or flood-construction-level (FCL) foundations & in-house ES54 underground power", desc2: "Engineered Douglas Fir framing, exterior Rockwool insulation & triple-glazed windows", desc3: "Custom kitchen & millwork package, hydronic radiant heating, ERV & 2-5-10 Warranty" }, northvan: { geo: "📍 North Vancouver", header: "📍 NORTH VANCOUVER SQUARE-FOOT BREAKDOWN", rateLow: 740, rateHigh: 880, b1Low: 160, b1High: 195, b2Low: 295, b2High: 350, b3Low: 285, b3High: 335, desc1: "Ravine/slope shoring, micropiled footings, storm detention & underground hydro service", desc2: "Acoustic & thermal Step Code 5 shell, structural steel moment frames & European glazing", desc3: "Bespoke interior millwork, designer tile/stone, multi-zone radiant floors & warranty" } }; var state = { sqft: 4500, corridor: "westvan", civil: "standard" }; var sqftInput = document.getElementById("kpSimSqft"); var sqftDisplay = document.getElementById("kpSimSqftDisplay"); var sqftRateBig = document.getElementById("kpSimSqftRateBig"); var geoBadge = document.getElementById("kpSimGeoBadge"); var budgetBand = document.getElementById("kpSimBudgetBand"); var civilNote = document.getElementById("kpSimCivilNote"); var fiduciarySaved = document.getElementById("kpSimFiduciarySaved"); var specHeader = document.getElementById("kpSimSpecHeader"); var break1 = document.getElementById("kpSimBreak1"); var break2 = document.getElementById("kpSimBreak2"); var break3 = document.getElementById("kpSimBreak3"); var desc1 = document.getElementById("kpSimDesc1"); var desc2 = document.getElementById("kpSimDesc2"); var desc3 = document.getElementById("kpSimDesc3"); function formatM(v) { return "$" + (v / 1000000).toFixed(2) + "M"; } function formatK(v) { return "$" + (Math.round(v / 10000) * 10).toLocaleString() + ",000"; } function renderSqftCalc() { var c = corridorData[state.corridor] || corridorData.westvan; var civilSqftAdd = state.civil === "pmt" ? 35 : 0; var rLow = c.rateLow + civilSqftAdd; var rHigh = c.rateHigh + civilSqftAdd; var totalLow = state.sqft * rLow; var totalHigh = state.sqft * rHigh; var savedLow = totalLow * 0.10; var savedHigh = totalHigh * 0.13; if (sqftDisplay) sqftDisplay.textContent = state.sqft.toLocaleString() + " sq ft"; if (sqftRateBig) sqftRateBig.textContent = "$" + rLow + " – $" + rHigh + " / sq ft"; if (geoBadge) geoBadge.textContent = c.geo; if (budgetBand) budgetBand.textContent = formatM(totalLow) + " – " + formatM(totalHigh); if (civilNote) civilNote.textContent = state.civil === "pmt" ? "Includes ES54 Transformer Vault" : "Includes Underground 200A–400A Hydro"; if (fiduciarySaved) fiduciarySaved.textContent = formatK(savedLow) + " – " + formatK(savedHigh); if (specHeader) specHeader.textContent = c.header; if (break1) break1.textContent = "$" + (c.b1Low + civilSqftAdd) + " – $" + (c.b1High + civilSqftAdd) + " / sq ft"; if (break2) break2.textContent = "$" + c.b2Low + " – $" + c.b2High + " / sq ft"; if (break3) break3.textContent = "$" + c.b3Low + " – $" + c.b3High + " / sq ft"; if (desc1) desc1.textContent = c.desc1; if (desc2) desc2.textContent = c.desc2; if (desc3) desc3.textContent = c.desc3; } if (sqftInput) { sqftInput.addEventListener("input", function() { state.sqft = parseInt(this.value, 10) || 4500; renderSqftCalc(); }); } document.querySelectorAll(".kp-sim-corridor-btn").forEach(function(btn) { btn.addEventListener("click", function() { state.corridor = this.getAttribute("data-corridor") || "westvan"; document.querySelectorAll(".kp-sim-corridor-btn").forEach(function(b) { var active = b === btn; b.style.border = active ? "1.5px solid #d4af37" : "1px solid rgba(255,255,255,0.16)"; b.style.boxShadow = active ? "inset 0 0 14px rgba(212,175,55,0.18)" : "none"; b.style.color = active ? "#ffffff" : "#cbd5e1"; }); renderSqftCalc(); }); }); document.querySelectorAll(".kp-sim-civil-btn").forEach(function(btn) { btn.addEventListener("click", function() { state.civil = this.getAttribute("data-civil") || "standard"; document.querySelectorAll(".kp-sim-civil-btn").forEach(function(b) { var active = b === btn; b.style.border = active ? "1.5px solid #38bdf8" : "1px solid rgba(255,255,255,0.16)"; b.style.boxShadow = active ? "inset 0 0 14px rgba(56,189,248,0.18)" : "none"; b.style.color = active ? "#ffffff" : "#cbd5e1"; }); renderSqftCalc(); }); }); var pillars = [ { badge: "PILLAR 01 • LOT, ZONING & COST FEASIBILITY (WEEKS 1–4)", title: "Lot Feasibility, Rock Profile & Square-Foot Budget Lock", desc: "Before you spend $100,000+ on architectural plans that exceed your budget, we inspect your lot’s zoning setbacks, bedrock depth, and BC Hydro connection distance—delivering a clear 40-division open-book cost plan from Day 1.", bullets: [ "Municipal Zoning & Setback Check: Maximum buildable square footage & view cones", "Bedrock & Slope Assessment: Excavation, rock anchoring & retaining wall budget", "BC Hydro ES54 Power Layout: Underground duct bank & transformer siting", "40-Division Open-Book Pro-Forma: Transparent line-item square-foot budget" ] }, { badge: "PILLAR 02 • ENGINEERING & PERMIT LOCK (MONTHS 2–4)", title: "Architectural Coordination, Step Code 5 & Permit Approvals", desc: "We work directly alongside your architect, structural engineer, and energy advisor to eliminate costly thermal bridges and structural clashes before drawings enter municipal plan check across West Vancouver, Whistler, Squamish, or North Vancouver.", bullets: [ "3-Bid Subcontractor Tendering: Side-by-side open-book trade pricing across 40 divisions", "Step Code 5 & Zero Carbon Modeling: Triple-pane glazing & Schöck Isokorb thermal breaks", "Part 4 Seismic Engineering: Concealed steel frames for panoramic ocean & mountain glass", "Guaranteed Max Price (GMP) Option: Lock your build price once drawings are finalized" ] }, { badge: "PILLAR 03 • ROCK EXCAVATION & ES54 HYDRO (MONTHS 5–8)", title: "In-House Bedrock Excavation, Micropiles & Underground Power", desc: "While conventional builders stall for months waiting on utility contractors, our in-house civil crew executes bedrock splitting, tensioned rock anchors, and BC Hydro ES54 underground duct banks simultaneously.", bullets: [ "Controlled Rock Splitting & Shoring: Engineered foundation excavation & rock bolting", "BC Hydro ES54 Transformer Vaults: Precast pads & 400A–1200A+ primary estate power", "Underground Utility Trenching: Primary hydro, fiber optics, storm & sanitary tie-ins", "Architectural Concrete Foundations: Precision board-formed walls & seismic shear cores" ] }, { badge: "PILLAR 04 • SEISMIC FRAME & STEP 5 SHELL (MONTHS 9–15)", title: "Steel & Heavy Timber Framing + Airtight Step Code 5 Envelope", desc: "Precision erection of structural steel moment frames, CNC Douglas Fir glulam beams, and triple-pane European window walls—verified mid-build by certified blower-door airtightness testing.", bullets: [ "Seismic Steel & Mass Timber Erection: Engineered for coastal wind & 4.2 kPa alpine snow", "Continuous Exterior Rockwool Armor: Zero thermal bridging across concrete slabs", "Mid-Build Blower-Door Verification: Confirmed ≤ 1.0 ACH50 airtight energy performance", "Hydronic & Heat-Pump Rough-In: Electrified radiant floor heating & snow-melt driveways" ] }, { badge: "PILLAR 05 • CUSTOM FINISH & 2-5-10 WARRANTY (MONTHS 16–20)", title: "Bespoke Millwork, Commissioning & 2-5-10 Warranty Handover", desc: "Museum-grade custom cabinetry, architectural stonework, smart-home commissioning, final municipal occupancy sign-off, and full registration under our BC Housing #52603 2-5-10 Year National Home Warranty.", bullets: [ "Master Builder White-Glove QA: 250-point laser-level & thermal-camera envelope inspection", "Mechanical & Smart Home Commissioning: Full hydronic balancing & Lutron automation", "CCDC 5B Final Open-Book Accounting: Complete reconciliation of all trade invoices", "Statutory 2-5-10 Year Warranty: Protected under BC Housing Licensed Builder #52603" ] } ]; document.querySelectorAll(".kp-roadmap-tab").forEach(function(tab) { tab.addEventListener("click", function() { var idx = parseInt(this.getAttribute("data-stage"), 10) || 0; var p = pillars[idx] || pillars[0]; document.querySelectorAll(".kp-roadmap-tab").forEach(function(t) { var active = t === tab; t.style.border = active ? "1.5px solid #d4af37" : "1px solid rgba(255,255,255,0.18)"; t.style.boxShadow = active ? "inset 0 0 16px rgba(212,175,55,0.18)" : "none"; t.style.color = active ? "#ffffff" : "#cbd5e1"; }); var bEl = document.getElementById("kpRoadmapBadge"); var tEl = document.getElementById("kpRoadmapTitle"); var dEl = document.getElementById("kpRoadmapDesc"); var ulEl = document.getElementById("kpRoadmapBullets"); if (bEl) bEl.textContent = p.badge; if (tEl) tEl.textContent = p.title; if (dEl) dEl.textContent = p.desc; if (ulEl) { ulEl.innerHTML = p.bullets.map(function(item) { var parts = item.split(":"); return '<li><span style="color: #d4af37; font-weight: 900;">✦</span> <strong>' + parts[0] + ':</strong>' + (parts[1] || '') + '</li>'; }).join(""); } }); }); renderSqftCalc(); } if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", initKeystoneHomepageV460); } else { initKeystoneHomepageV460(); } })();</script>
</div>

    </main>
</div>

<?php
get_footer();
