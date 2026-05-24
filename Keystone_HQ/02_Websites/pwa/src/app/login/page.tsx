import { login, signup } from './actions'

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ message: string; redirect: string }>
}) {
  const params = await searchParams;
  return (
    <div className="min-h-screen bg-black flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Ambient Background Effects */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-[#c5a55a] opacity-[0.015] rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#10b981] opacity-[0.01] rounded-full blur-[120px]" />
        {/* Grid overlay */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage: 'linear-gradient(rgba(197,165,90,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(197,165,90,0.3) 1px, transparent 1px)',
            backgroundSize: '60px 60px',
          }}
        />
      </div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        {/* Logo SVG — Transparent Keystone Mark */}
        <div className="flex justify-center mb-8">
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M28 4L8 18v20l20 14 20-14V18L28 4z" stroke="#c5a55a" strokeWidth="1.5" fill="none" opacity="0.8"/>
            <path d="M28 12L14 22v12l14 10 14-10V22L28 12z" stroke="#c5a55a" strokeWidth="1" fill="none" opacity="0.4"/>
            <path d="M28 20L20 26v6l8 6 8-6v-6L28 20z" fill="#c5a55a" opacity="0.15"/>
            <path d="M28 4v48M8 18l40 0M8 38l40 0" stroke="#c5a55a" strokeWidth="0.5" opacity="0.1"/>
          </svg>
        </div>

        <h2 className="text-center text-2xl font-light tracking-[0.15em] text-white uppercase">
          Keystone
        </h2>
        <p className="mt-1 text-center text-xs tracking-[0.3em] text-[#c5a55a] uppercase font-medium">
          Possibilities
        </p>
        <div className="kp-keyline mt-6 mx-auto w-32" />
        <p className="mt-4 text-center text-[10px] text-[#666] tracking-[0.25em] uppercase">
          Command Center Access
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="kp-card-gold py-10 px-6 sm:px-10 kp-animate-in">
          <form action={login} className="space-y-6">
            {params?.redirect && <input type="hidden" name="redirect" value={params.redirect} />}
            <div>
              <label className="block text-[10px] font-medium text-[#c5a55a] uppercase tracking-[0.2em] mb-2">
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="kp-input"
                placeholder="you@keystonepossibilities.ca"
              />
            </div>

            <div>
              <label className="block text-[10px] font-medium text-[#c5a55a] uppercase tracking-[0.2em] mb-2">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="kp-input"
                placeholder="••••••••••"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-3.5 w-3.5 accent-[#c5a55a] bg-black border-[#222] rounded cursor-pointer"
                />
                <label htmlFor="remember-me" className="ml-2 block text-xs text-[#666]">
                  Remember me
                </label>
              </div>

              <div className="text-xs">
                <a href="#" className="text-[#c5a55a] hover:text-[#d4b86a] transition-colors">
                  Forgot password?
                </a>
              </div>
            </div>

            {params?.message && (
              <div className="bg-red-900/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-xs text-center">
                {params.message}
              </div>
            )}

            <div className="flex flex-col gap-3 pt-2">
              <button
                formAction={login}
                className="kp-btn-gold w-full py-3 text-center"
              >
                Sign In
              </button>
              <button
                formAction={signup}
                className="w-full flex justify-center py-3 px-4 border border-[#1a1a1a] rounded-lg text-xs font-medium text-[#666] bg-transparent hover:border-[#c5a55a]/30 hover:text-[#a3a3a3] transition-all duration-200 uppercase tracking-wider"
              >
                Request Authorization
              </button>
            </div>
          </form>
        </div>

        {/* Footer watermark */}
        <p className="mt-8 text-center text-[9px] text-[#333] tracking-[0.3em] uppercase">
          Keystone Possibilities © {new Date().getFullYear()}
        </p>
      </div>
    </div>
  )
}
