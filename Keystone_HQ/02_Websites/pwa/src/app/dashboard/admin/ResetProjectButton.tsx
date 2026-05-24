'use client'

import { useState } from 'react'
import { resetProject } from './actions'
import { useRouter } from 'next/navigation'

export function ResetProjectButton({ projectId, projectTitle }: { projectId: string, projectTitle: string }) {
  const router = useRouter()
  const [step, setStep] = useState<'idle' | 'confirm1' | 'confirm2' | 'resetting' | 'done' | 'error'>('idle')
  const [errorMsg, setErrorMsg] = useState('')

  async function handleReset() {
    setStep('resetting')
    const result = await resetProject(projectId)
    if (result.error) {
      setErrorMsg(result.error)
      setStep('error')
    } else {
      setStep('done')
      setTimeout(() => {
        router.refresh()
        setStep('idle')
      }, 2000)
    }
  }

  if (step === 'idle') {
    return (
      <button
        onClick={() => setStep('confirm1')}
        className="w-full bg-red-900/20 hover:bg-red-900/40 text-red-400 border border-red-800/30 py-3 rounded-lg text-sm font-medium transition-colors"
      >
        ⚠️ Reset Project Data
      </button>
    )
  }

  if (step === 'confirm1') {
    return (
      <div className="bg-red-950/30 border border-red-800/50 rounded-xl p-4 space-y-3">
        <div className="flex items-start gap-3">
          <svg className="w-6 h-6 text-red-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h4 className="text-red-400 font-medium">Are you sure?</h4>
            <p className="text-sm text-[#a3a3a3] mt-1">
              This will permanently delete <strong className="text-[#f5f5f5]">all milestones, documents, communications, trade assignments, and date proposals</strong> for <strong className="text-[#f5f5f5]">&ldquo;{projectTitle}&rdquo;</strong>.
            </p>
            <p className="text-xs text-[#666] mt-1">The project itself will be preserved and reset to &ldquo;Planning&rdquo; status.</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setStep('confirm2')}
            className="flex-1 bg-red-600 hover:bg-red-500 text-white py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Yes, Continue to Final Confirmation
          </button>
          <button
            onClick={() => setStep('idle')}
            className="flex-1 bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] py-2 rounded-lg text-sm transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    )
  }

  if (step === 'confirm2') {
    return (
      <div className="bg-red-950/50 border-2 border-red-600/60 rounded-xl p-4 space-y-3 animate-pulse-once">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 mx-auto rounded-full bg-red-600/20 flex items-center justify-center">
            <svg className="w-7 h-7 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </div>
          <h4 className="text-lg text-red-400 font-bold">FINAL CONFIRMATION</h4>
          <p className="text-sm text-[#a3a3a3]">
            Type <strong className="text-red-400">RESET</strong> is not required — just click the button below. This action <strong className="text-red-400">CANNOT</strong> be undone.
          </p>
          <p className="text-xs text-[#666]">
            Project: <strong className="text-[#a3a3a3]">{projectTitle}</strong>
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleReset}
            className="flex-1 bg-red-600 hover:bg-red-500 text-white py-3 rounded-lg text-sm font-bold transition-colors border border-red-500"
          >
            🗑️ PERMANENTLY RESET ALL DATA
          </button>
          <button
            onClick={() => setStep('idle')}
            className="flex-1 bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] py-3 rounded-lg text-sm transition-colors"
          >
            Cancel — Keep Data
          </button>
        </div>
      </div>
    )
  }

  if (step === 'resetting') {
    return (
      <div className="bg-[#0a0a0a] border border-[#1a1a1a] rounded-xl p-6 text-center">
        <div className="animate-spin w-8 h-8 border-2 border-red-500 border-t-transparent rounded-full mx-auto mb-3" />
        <p className="text-[#a3a3a3] text-sm">Resetting project data...</p>
      </div>
    )
  }

  if (step === 'done') {
    return (
      <div className="bg-emerald-950/30 border border-emerald-800/50 rounded-xl p-6 text-center">
        <p className="text-emerald-400 font-medium">✓ Project data has been reset successfully.</p>
      </div>
    )
  }

  if (step === 'error') {
    return (
      <div className="bg-red-950/30 border border-red-800/50 rounded-xl p-4 space-y-2">
        <p className="text-red-400 text-sm font-medium">Reset failed: {errorMsg}</p>
        <button onClick={() => setStep('idle')} className="text-xs text-[#666] hover:text-[#f5f5f5]">Dismiss</button>
      </div>
    )
  }

  return null
}
