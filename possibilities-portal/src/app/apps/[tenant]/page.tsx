import DiagnosticForm from "../../../components/DiagnosticForm";

interface TenantConfig {
  name: string;
  tagline: string;
  description: string;
  ctaText: string;
}

const verticalConfigs: Record<string, TenantConfig> = {
  landscaping: {
    name: "GreenScape Professional Operations",
    tagline: "Eco-Conscious Landscape & Outdoor Living Engineering",
    description: "Submit details on sod area, hardscape vision, and design assets for a comprehensive visual project estimate.",
    ctaText: "Request Outdoor Design Diagnostics",
  },
  roofing: {
    name: "Apex Roofing and Estimation",
    tagline: "High-Performance Protection & Leak Auditing Systems",
    description: "Submit storm damage photos, roof measurements, or structural blueprints for high-velocity industrial review.",
    ctaText: "Request Storm Damage Evaluation",
  },
  "custom-homes": {
    name: "Elysian Custom Home Builder",
    tagline: "Architectural Mastery & Luxury Custom Build Optimization",
    description: "Submit premium site surveys, zoning documentation, and custom architectural layouts for elite project auditing.",
    ctaText: "Begin Architectural Evaluation",
  },
};

export default async function TenantPage({
  params,
}: {
  params: Promise<{ tenant: string }>;
}) {
  const { tenant } = await params;
  
  // Resolve active industry configuration
  const config = verticalConfigs[tenant] || verticalConfigs.landscaping;

  return (
    <div className="min-h-screen text-zinc-900 selection:bg-brand-primary selection:text-white font-brand antialiased">
      {/* Dynamic Navigation */}
      <nav className="w-full border-b border-zinc-200 bg-white/80 backdrop-blur-md fixed top-0 z-50 transition-all duration-300">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-lg font-semibold tracking-wider text-brand-primary">
            {config.name.split(" ")[0]} <span className="font-light text-zinc-500">{config.name.split(" ").slice(1).join(" ")}</span>
          </div>
          <div className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
            Intake Protocol
          </div>
        </div>
      </nav>

      {/* Dynamic Hero Section */}
      <section className="relative pt-40 pb-20 px-6 max-w-5xl mx-auto text-center space-y-8">
        <div 
          style={{ borderRadius: "var(--brand-radius)" }} 
          className="inline-block border border-brand-primary/20 px-4 py-1 text-xs tracking-widest text-brand-primary uppercase bg-brand-primary/5"
        >
          {config.ctaText}
        </div>
        <h1 className="text-4xl md:text-6xl font-light tracking-tight leading-none">
          {config.tagline.split(" & ")[0]} <br />
          <span className="font-bold text-brand-primary">
            {config.tagline.split(" & ")[1] || ""}
          </span>
        </h1>
        <p className="text-zinc-600 font-light max-w-2xl mx-auto text-base md:text-lg leading-relaxed">
          {config.description}
        </p>
      </section>

      {/* Diagnostic Form Mount */}
      <section className="py-16 px-6 relative bg-zinc-50 border-t border-zinc-200">
        <div className="max-w-4xl mx-auto space-y-12">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-light tracking-tight text-zinc-800">Dynamic Evaluation System</h2>
            <p className="text-zinc-400 text-xs tracking-widest uppercase">Secure Portal // Direct Database Delivery</p>
          </div>
          
          <div 
            style={{ borderRadius: "var(--brand-radius)" }}
            className="p-[1px] bg-gradient-to-b from-brand-primary/20 to-transparent shadow-xl"
          >
            <div 
              style={{ borderRadius: "var(--brand-radius)" }}
              className="bg-white p-6 sm:p-10 border border-zinc-100"
            >
              {/* Mounted Lead Form - fully responsive to active vertical variables! */}
              <DiagnosticForm />
            </div>
          </div>
        </div>
      </section>

      {/* Dynamic Footer */}
      <footer className="w-full py-12 text-center text-zinc-400 text-xs tracking-widest uppercase border-t border-zinc-100 bg-white">
        © {new Date().getFullYear()} {config.name}. All Rights Reserved.
      </footer>
    </div>
  );
}
