'use client'

import { useActionState, useState } from 'react'
import { createProject } from './actions'

const initialState = { error: '', success: false, projectId: '' }

export function CreateProjectForm() {
  const [state, formAction, isPending] = useActionState(async (prevState: any, formData: FormData) => {
    const result = await createProject(formData)
    if (result?.error) {
      return { error: result.error, success: false, projectId: '' }
    }
    return { error: '', success: true, projectId: result.projectId }
  }, initialState)

  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    if (state.projectId) {
      const inviteUrl = `${window.location.origin}/invite?project_id=${state.projectId}`
      navigator.clipboard.writeText(inviteUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  if (state.success && state.projectId) {
    const inviteUrl = typeof window !== 'undefined' ? `${window.location.origin}/invite?project_id=${state.projectId}` : ''
    return (
      <div className="kp-card-gold p-8 max-w-2xl mx-auto mt-8 text-center kp-animate-in">
        <div className="flex justify-center mb-4">
          <div className="w-12 h-12 rounded-xl bg-[#10b981]/10 border border-[#10b981]/20 flex items-center justify-center">
            <svg className="w-6 h-6 text-[#10b981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
        </div>
        <h2 className="text-2xl font-light text-[#10b981] mb-2">Project Initialized</h2>
        <p className="text-[#666] mb-6 text-xs leading-relaxed max-w-md mx-auto">
          Your project workspace has been created. Send this secure invite link to the Property Owner so they can connect their account.
        </p>
        <div className="flex items-center gap-2 bg-black border border-[#1a1a1a] rounded-lg p-3 mb-6">
          <input 
            type="text" 
            readOnly 
            value={inviteUrl} 
            className="flex-1 bg-transparent text-[#a3a3a3] text-xs focus:outline-none font-mono"
          />
          <button 
            onClick={handleCopy}
            className="kp-btn-emerald text-[10px] px-4 py-2 whitespace-nowrap"
          >
            {copied ? '✓ Copied' : 'Copy Link'}
          </button>
        </div>
        <button onClick={() => window.location.reload()} className="text-[#666] hover:text-[#c5a55a] text-xs transition-colors tracking-wider uppercase">
          Create Another Project
        </button>
      </div>
    )
  }

  return (
    <div className="kp-card-gold p-8 max-w-2xl mx-auto mt-8 kp-animate-in">
      <div className="flex items-center gap-3 mb-2">
        <svg className="w-5 h-5 text-[#c5a55a]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 4v16m8-8H4"></path>
        </svg>
        <h2 className="text-sm font-light text-[#f5f5f5] tracking-widest uppercase">Initialize New Project</h2>
      </div>
      <p className="text-[#666] mb-6 text-xs leading-relaxed">
        Set up the master configuration for a new build. Once created, you can upload contracts, invite trades, and unlock the financial ledger.
      </p>

      <form action={formAction} className="space-y-6">
        <div className="space-y-4">
          <div>
            <label htmlFor="title" className="block text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] font-medium mb-2">Project Name *</label>
            <input 
              type="text" 
              name="title" 
              id="title" 
              required
              className="kp-input"
              placeholder="e.g. 1234 Skyview Drive"
            />
          </div>

          <div>
            <label htmlFor="address" className="block text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] font-medium mb-2">Site Address</label>
            <input 
              type="text" 
              name="address" 
              id="address" 
              className="kp-input"
              placeholder="e.g. Vancouver, BC"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="total_budget" className="block text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] font-medium mb-2">Total Capital ($)</label>
              <input 
                type="number" 
                name="total_budget" 
                id="total_budget" 
                step="0.01"
                className="kp-input"
                placeholder="1500000"
              />
            </div>
            <div>
              <label htmlFor="pm_fee_percentage" className="block text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] font-medium mb-2">PM Fee (%)</label>
              <input 
                type="number" 
                name="pm_fee_percentage" 
                id="pm_fee_percentage" 
                step="0.01"
                defaultValue="12.00"
                className="kp-input"
              />
            </div>
          </div>
        </div>

        {state?.error && (
          <div className="kp-status-danger p-3 rounded-lg text-xs text-center">
            {state.error}
          </div>
        )}

        <button 
          type="submit" 
          disabled={isPending}
          className="kp-btn-gold w-full py-3 text-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPending ? 'Initializing...' : 'Initialize Project'}
        </button>
      </form>
    </div>
  )
}
