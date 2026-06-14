import DiagnosticForm from '../../components/DiagnosticForm';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-zinc-800 selection:text-white font-sans overflow-x-hidden">
      {/* Navigation */}
      <nav className="w-full border-b border-white/10 bg-black/50 backdrop-blur-md fixed top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-xl font-light tracking-[0.2em] uppercase">Keystone</div>
          <div className="hidden md:flex gap-8 text-xs tracking-widest text-zinc-400 uppercase">
            <a href="#" className="hover:text-white transition-colors duration-500">Portfolio</a>
            <a href="#" className="hover:text-white transition-colors duration-500">Capabilities</a>
            <a href="#" className="hover:text-white transition-colors duration-500">Process</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-40 pb-20 px-6 max-w-7xl mx-auto flex flex-col md:flex-row items-center gap-16">
        <div className="flex-1 space-y-8 z-10">
          <div className="inline-block border border-white/20 rounded-full px-4 py-1 text-xs tracking-widest text-zinc-300 uppercase bg-white/5 backdrop-blur-sm">
            Exclusive Intake Portal
          </div>
          <h1 className="text-5xl md:text-7xl font-extralight tracking-tight leading-[1.1]">
            Engineering <br />
            <span className="font-semibold text-transparent bg-clip-text bg-gradient-to-r from-zinc-100 to-zinc-500">
              Possibilities.
            </span>
          </h1>
          <p className="text-lg text-zinc-400 font-light max-w-md leading-relaxed">
            We do not accept every project. Submit your vision, architectural files, and timeline for a comprehensive diagnostic evaluation by our executive team.
          </p>
        </div>
        
        {/* Abstract Aesthetic Element */}
        <div className="flex-1 relative w-full h-[400px] hidden md:block">
          <div className="absolute inset-0 bg-gradient-to-tr from-zinc-800/20 to-zinc-500/10 rounded-3xl border border-white/5 backdrop-blur-3xl overflow-hidden flex items-center justify-center">
             <div className="w-[300px] h-[300px] rounded-full border border-white/10 animate-[spin_60s_linear_infinite]" />
             <div className="absolute w-[200px] h-[200px] rounded-full border border-white/20 animate-[spin_40s_linear_infinite_reverse]" />
          </div>
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white/5 blur-[100px] rounded-full pointer-events-none" />
        </div>
      </section>

      {/* Diagnostic Form Section */}
      <section className="py-24 px-6 relative bg-zinc-950 border-t border-white/5">
        <div className="max-w-4xl mx-auto space-y-12">
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-light tracking-wide">Project Diagnostic & Intake</h2>
            <p className="text-zinc-500 text-sm tracking-widest uppercase">Secure File Transmission Protocol</p>
          </div>
          
          <div className="p-1 rounded-2xl bg-gradient-to-b from-white/10 to-transparent">
            <div className="bg-black rounded-xl p-4 sm:p-8 border border-white/5 shadow-2xl">
              <DiagnosticForm />
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full py-12 text-center text-zinc-600 text-xs tracking-widest uppercase border-t border-white/5 bg-black space-y-4">
        <div>
          © {new Date().getFullYear()} Keystone Possibilities. All Rights Reserved.
        </div>
        <div className="text-[10px] text-zinc-500 normal-case tracking-normal">
          Partner Brand:{' '}
          <a
            href="https://keystonerecomposition.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-zinc-400 hover:text-white transition-colors duration-300"
          >
            Keystone Recomposition (Health & Music)
          </a>
        </div>
      </footer>
    </div>
  );
}
