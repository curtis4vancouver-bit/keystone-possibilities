import { claimAdmin } from './actions'

export default async function AdminSetupPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>
}) {
  const params = await searchParams;

  return (
    <div className="min-h-screen bg-black flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-light tracking-tight text-[#f5f5f5] uppercase">
          Keystone <span className="font-bold text-[#c5a55a]">Master</span>
        </h2>
        <p className="mt-2 text-center text-sm text-[#666] tracking-widest uppercase">
          Administrator Access
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-[#0a0a0a]/50 border border-[#1a1a1a] py-8 px-4 shadow sm:rounded-xl sm:px-10">
          <form action={claimAdmin} className="space-y-6">
            <div>
              <label className="block text-[9px] font-medium text-[#c5a55a] uppercase tracking-[0.2em] mb-1.5">
                Administrating Key
              </label>
              <input
                id="secretKey"
                name="secretKey"
                type="password"
                required
                className="kp-input"
                placeholder="Enter the master key..."
              />
            </div>

            {params?.error && (
              <div className="bg-red-900/20 border border-red-900/50 text-red-400 p-3 rounded-lg text-sm text-center">
                {params.error}
              </div>
            )}

            <button
              type="submit"
              className="kp-btn-gold w-full py-3 text-sm font-medium"
            >
              Elevate to Owner
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
