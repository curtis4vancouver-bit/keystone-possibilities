'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { createUserAccount } from './actions'

export function CreateAccountForm() {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [result, setResult] = useState<{ email?: string; password?: string } | null>(null)

  async function handleSubmit(formData: FormData) {
    setIsPending(true)
    const res = await createUserAccount(formData)
    if (res?.error) {
      toast.error(res.error)
    } else if (res?.success) {
      toast.success('Account created!')
      setResult({ email: res.email, password: res.password })
    }
    setIsPending(false)
  }

  if (!isOpen) {
    return (
      <button
        onClick={() => { setIsOpen(true); setResult(null) }}
        className="kp-btn-emerald px-4 py-2 text-sm flex items-center gap-2"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
        </svg>
        Create Account
      </button>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setIsOpen(false)}>
      <div className="p-6 w-full max-w-md rounded-xl border border-[#c5a55a]/20 bg-[#0a0a0a] shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-center mb-6 border-b border-[#1a1a1a] pb-3">
          <h3 className="text-lg font-light text-[#f5f5f5]">Create Account</h3>
          <button onClick={() => setIsOpen(false)} className="text-[#666] hover:text-[#f5f5f5] text-xl transition-colors">&times;</button>
        </div>

        {result ? (
          <div className="space-y-4">
            <div className="bg-[#10b981]/10 border border-[#10b981]/20 rounded-lg p-4">
              <p className="text-[#10b981] text-sm font-medium mb-3">✅ Account Created — Send these credentials:</p>
              <div className="space-y-2 font-mono text-sm">
                <p className="text-[#a3a3a3]">
                  <span className="text-[#666]">Email:</span> <span className="text-[#f5f5f5] select-all">{result.email}</span>
                </p>
                <p className="text-[#a3a3a3]">
                  <span className="text-[#666]">Password:</span> <span className="text-[#f5f5f5] select-all">{result.password}</span>
                </p>
                <p className="text-[#a3a3a3]">
                  <span className="text-[#666]">URL:</span> <span className="text-[#f5f5f5] select-all">app.keystonepossibilities.ca</span>
                </p>
              </div>
            </div>
            <button
              onClick={() => { setResult(null); setIsOpen(false) }}
              className="kp-btn-gold w-full py-2.5 text-sm"
            >
              Done
            </button>
          </div>
        ) : (
          <form action={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Full Name</label>
              <input type="text" name="full_name" required className="kp-input" placeholder="e.g. John Smith" />
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Email</label>
              <input type="email" name="email" required className="kp-input" placeholder="e.g. john@gmail.com" />
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Role</label>
              <select name="role" required className="kp-input [color-scheme:dark]">
                <option value="owner">Owner (Property Client)</option>
                <option value="trade">Trade (Subcontractor)</option>
              </select>
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Temporary Password</label>
              <input type="text" name="password" defaultValue="Welcome2026!" required className="kp-input" />
              <p className="text-[10px] text-[#404040] mt-1">They can change this after first login.</p>
            </div>
            <button type="submit" disabled={isPending} className="kp-btn-emerald w-full py-2.5 font-medium text-sm disabled:opacity-50">
              {isPending ? 'Creating...' : 'Create & Auto-Approve'}
            </button>
          </form>
        )}
      </div>
    </div>
  )
}
