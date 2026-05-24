import Link from 'next/link';

export default function WellnessBuilds() {
  return (
    <div className="min-h-screen bg-black text-neutral-100 flex flex-col selection:bg-amber-500/30 selection:text-white">
      {/* Premium Header */}
      <header className="sticky top-0 z-50 kp-glass border-b border-neutral-900 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <Link href="/dashboard" className="flex items-center gap-3">
            <span className="text-xl font-bold tracking-widest text-[#c5a55a]">KEYSTONE</span>
            <span className="text-xs bg-[#c5a55a]/10 text-[#c5a55a] border border-[#c5a55a]/20 px-2 py-0.5 rounded uppercase tracking-wider font-semibold">
              Wellness Builds
            </span>
          </Link>
          <Link href="/login" className="kp-btn-gold text-xs">
            Client Portal
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-24 px-6 overflow-hidden border-b border-neutral-900">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_var(--kp-gold-glow)_0%,_transparent_50%)]" />
        
        <div className="max-w-4xl mx-auto text-center relative z-10 space-y-6">
          <span className="text-[#c5a55a] text-xs font-semibold tracking-[0.2em] uppercase">
            Turnkey Contrast Therapy Circuits
          </span>
          <h1 className="text-4xl md:text-6xl font-light tracking-tight text-neutral-100 leading-tight">
            High-End Backyard <br />
            <span className="font-semibold text-transparent bg-clip-text bg-gradient-to-r from-[#c5a55a] via-amber-200 to-[#c5a55a]">
              Wellness Architecture
            </span>
          </h1>
          <p className="text-neutral-400 text-lg max-w-2xl mx-auto font-light leading-relaxed">
            We supervise complete outdoor thermal spa installations—custom cedar saunas, cold plunge surrounds, and luxury deck layouts—handled from excavation to electrical permit by the PNW's premier project managers.
          </p>
          <div className="pt-4">
            <div className="kp-keyline max-w-xs mx-auto mb-8" />
          </div>
        </div>
      </section>

      {/* Geographic Enclave Packages */}
      <section className="py-20 px-6 max-w-7xl mx-auto w-full space-y-12">
        <div className="text-center space-y-2">
          <h2 className="text-2xl md:text-3xl font-light tracking-wide text-neutral-100">
            Geographically Engineered Packages
          </h2>
          <p className="text-neutral-500 text-sm max-w-xl mx-auto font-light">
            Pacific Northwest terrain requires specialized engineering. Choose your enclave below to see our tailored approach.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-6">
          {/* Whistler Mountain Alpine Package */}
          <div className="kp-card-gold p-8 flex flex-col justify-between space-y-8 relative overflow-hidden group">
            <div className="absolute -right-16 -top-16 w-32 h-32 bg-[#c5a55a]/5 rounded-full blur-2xl group-hover:bg-[#c5a55a]/10 transition-all duration-500" />
            <div className="space-y-6">
              <div className="flex justify-between items-start">
                <span className="text-3xl">🏔️</span>
                <span className="text-xs border border-neutral-800 text-neutral-400 px-3 py-1 rounded-full uppercase tracking-wider font-semibold">
                  Whistler Chalet
                </span>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-medium text-neutral-100 tracking-wide">Après-Ski Thermal Circuit</h3>
                <p className="text-neutral-400 text-sm font-light leading-relaxed">
                  Engineered specifically for heavy sub-zero alpine climates. Rustic-luxury aesthetics meet heavy timber framing.
                </p>
              </div>
              <ul className="space-y-3 text-xs text-neutral-400 font-light border-t border-neutral-900 pt-6">
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Wood-Burning Custom Cedar Barrel Sauna (90°C+)
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Insulated Sub-Zero Cold Plunge Surround
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Structural Heavy-Timber Snow-Load Decking
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Frost-Free Utility Trenching & Hydrants
                </li>
              </ul>
            </div>
            <div className="pt-6">
              <div className="text-xs text-neutral-500 mb-2 font-mono">ESTIMATED PM TIMELINE: 4 WEEKS</div>
              <button className="w-full kp-btn-gold text-center py-2.5">Inquire Alpine Build</button>
            </div>
          </div>

          {/* West Vancouver Oceanfront Vista Package */}
          <div className="kp-card-gold p-8 flex flex-col justify-between space-y-8 relative overflow-hidden group">
            <div className="absolute -right-16 -top-16 w-32 h-32 bg-[#c5a55a]/5 rounded-full blur-2xl group-hover:bg-[#c5a55a]/10 transition-all duration-500" />
            <div className="space-y-6">
              <div className="flex justify-between items-start">
                <span className="text-3xl">🌊</span>
                <span className="text-xs border border-neutral-800 text-neutral-400 px-3 py-1 rounded-full uppercase tracking-wider font-semibold">
                  West Vancouver
                </span>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-medium text-neutral-100 tracking-wide">Oceanfront Cliffside Vista</h3>
                <p className="text-neutral-400 text-sm font-light leading-relaxed">
                  Clean-line modernist spa layout built to frame spectacular Howe Sound vistas from steep bedrock slopes.
                </p>
              </div>
              <ul className="space-y-3 text-xs text-neutral-400 font-light border-t border-neutral-900 pt-6">
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Full Glass-Front Custom Architectural Sauna
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Flush-Integrated Zero-Edge Cold Plunge
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Structural Steel slope brackets & concrete anchors
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> District of West Van Setback Permit Handling
                </li>
              </ul>
            </div>
            <div className="pt-6">
              <div className="text-xs text-neutral-500 mb-2 font-mono">ESTIMATED PM TIMELINE: 6 WEEKS</div>
              <button className="w-full kp-btn-gold text-center py-2.5">Inquire Ocean Build</button>
            </div>
          </div>

          {/* North Vancouver Deep Cove Package */}
          <div className="kp-card-gold p-8 flex flex-col justify-between space-y-8 relative overflow-hidden group">
            <div className="absolute -right-16 -top-16 w-32 h-32 bg-[#c5a55a]/5 rounded-full blur-2xl group-hover:bg-[#c5a55a]/10 transition-all duration-500" />
            <div className="space-y-6">
              <div className="flex justify-between items-start">
                <span className="text-3xl">🌲</span>
                <span className="text-xs border border-neutral-800 text-neutral-400 px-3 py-1 rounded-full uppercase tracking-wider font-semibold">
                  North Vancouver
                </span>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-medium text-neutral-100 tracking-wide">Deep Forest Bathing Sanctuary</h3>
                <p className="text-neutral-400 text-sm font-light leading-relaxed">
                  Lush, rustic rainforest spa integrations focusing on eco-sensitive footprints and advanced drainage.
                </p>
              </div>
              <ul className="space-y-3 text-xs text-neutral-400 font-light border-t border-neutral-900 pt-6">
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Western Red Cedar Barrel Sauna (Electric/WiFi)
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Custom Red Cedar Clad Hot Tub / plunge circuit
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Wet-Climate timber preservation & custom metal flashing
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-[#c5a55a]">✓</span> Root-Safe hand-digging & advanced surface drainage
                </li>
              </ul>
            </div>
            <div className="pt-6">
              <div className="text-xs text-neutral-500 mb-2 font-mono">ESTIMATED PM TIMELINE: 3 WEEKS</div>
              <button className="w-full kp-btn-gold text-center py-2.5">Inquire Forest Build</button>
            </div>
          </div>
        </div>
      </section>

      {/* The Trojan Horse: The Project Management Standard */}
      <section className="bg-neutral-950 border-t border-b border-neutral-900 py-20 px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <span className="text-[#c5a55a] text-xs font-semibold tracking-wider uppercase">
              The Keystone Advantage
            </span>
            <h2 className="text-3xl md:text-4xl font-light text-neutral-100 tracking-tight leading-tight">
              We Don't Just Drop a Box. <br />
              <span className="font-semibold text-transparent bg-clip-text bg-gradient-to-r from-[#c5a55a] to-amber-200">
                We Engineer Your Spa.
              </span>
            </h2>
            <p className="text-neutral-400 text-sm font-light leading-relaxed">
              Backyard wellness builds are major civil and structural projects disguised as simple landscaping. A standard cold plunge or hot tub filled with water weighs **over 2,500 lbs**—putting that on an un-engineered wood deck will result in severe structural failure. 
            </p>
            <p className="text-neutral-400 text-sm font-light leading-relaxed">
              As licensed B2B civil developers and high-end residential supervisors, we coordinate the entire sequence for you: civil earthworks, municipal setback permits, structural steel slope framing, and dedicated 220V trade connections. 
            </p>
            
            {/* Core Pillars */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
              <div className="kp-glass p-4 rounded-lg space-y-1">
                <div className="text-[#c5a55a] font-semibold text-sm">⚡ Dedicated Power Grids</div>
                <p className="text-xs text-neutral-500 font-light">Dedicated sub-panel layout and full electrical trade sign-off.</p>
              </div>
              <div className="kp-glass p-4 rounded-lg space-y-1">
                <div className="text-[#c5a55a] font-semibold text-sm">📐 Structural Verification</div>
                <p className="text-xs text-neutral-500 font-light">Structural calculations for deck loads, slopes, and bedrock anchoring.</p>
              </div>
              <div className="kp-glass p-4 rounded-lg space-y-1">
                <div className="text-[#c5a55a] font-semibold text-sm">🚜 Site Grade & Drainage</div>
                <p className="text-xs text-neutral-500 font-light">Precise site-grading to avoid stagnant pooling and timber decay.</p>
              </div>
              <div className="kp-glass p-4 rounded-lg space-y-1">
                <div className="text-[#c5a55a] font-semibold text-sm">📜 Municipal Permits</div>
                <p className="text-xs text-neutral-500 font-light">Navigating local setbacks, DPAs, and safety clearance rules.</p>
              </div>
            </div>
          </div>

          {/* Interactive PM Dashboard Preview Card */}
          <div className="kp-glass-gold p-8 rounded-2xl border border-[#c5a55a]/15 space-y-6 relative">
            <div className="flex justify-between items-center border-b border-neutral-900 pb-4">
              <div>
                <h4 className="text-sm font-semibold tracking-wide text-neutral-100">CLIENT LIVE TIMELINE PORTAL</h4>
                <p className="text-[10px] text-neutral-500 font-mono">PROJECT: HIGHLANDS LUXURY SPA CIRCUIT</p>
              </div>
              <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded">
                ACTIVE
              </span>
            </div>

            {/* Simulated Live Sequences */}
            <div className="space-y-4 font-mono text-xs">
              <div className="flex items-center justify-between border-b border-neutral-900/60 pb-3">
                <div className="space-y-1">
                  <div className="text-neutral-400">Phase 1: Bedrock Grading & Excavation</div>
                  <div className="text-[10px] text-neutral-600">Subcontractor: Sea-to-Sky Excavating Ltd</div>
                </div>
                <span className="text-emerald-400 text-[10px] font-semibold">PASSED ✓</span>
              </div>

              <div className="flex items-center justify-between border-b border-neutral-900/60 pb-3">
                <div className="space-y-1">
                  <div className="text-neutral-400">Phase 2: Heavy Timber Decks & Brackets</div>
                  <div className="text-[10px] text-neutral-600">Subcontractor: Keystone Heavy Timber Crew</div>
                </div>
                <span className="text-emerald-400 text-[10px] font-semibold">PASSED ✓</span>
              </div>

              <div className="flex items-center justify-between border-b border-neutral-900/60 pb-3">
                <div className="space-y-1 flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
                  <div className="text-neutral-200">Phase 3: 220V Dedicated Sub-Panel Hookup</div>
                </div>
                <span className="text-amber-400 text-[10px] font-semibold">IN PROGRESS</span>
              </div>

              <div className="flex items-center justify-between pb-1 opacity-50">
                <div className="space-y-1">
                  <div className="text-neutral-500">Phase 4: Barrel Sauna Installation</div>
                  <div className="text-[10px] text-neutral-600">Subcontractor: Authorized Redwood Dealer</div>
                </div>
                <span className="text-neutral-600 text-[10px]">PENDING</span>
              </div>
            </div>

            <div className="bg-neutral-950/70 p-4 rounded-lg border border-neutral-900 text-xs text-neutral-400 space-y-3 font-light leading-relaxed">
              <p>
                <strong>📱 Client Transparency Promise:</strong> Every phase is logged inside our custom client PWA. You see exactly which trades are on site, inspect structural engineer sign-offs, and track budget payouts live on your phone.
              </p>
              <p>
                <strong>Looking for a Full Custom Home PM?</strong> When you experience our level of professional management on a spa project, you will understand why developers trust Keystone to supervise multi-million dollar custom builds.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Sign-off & Footer */}
      <footer className="mt-auto bg-black border-t border-neutral-900 py-12 px-6 text-center text-xs text-neutral-500 space-y-4">
        <div className="max-w-md mx-auto space-y-1">
          <p className="tracking-widest font-semibold text-neutral-400">KEYSTONE POSSIBILITIES LTD.</p>
          <p className="font-light">BC Licensed Builder #52603 · Registered BC Hydro Civil Supplier</p>
        </div>
        <p className="font-light">© 2026 Keystone Possibilities. All rights reserved.</p>
      </footer>
    </div>
  );
}
