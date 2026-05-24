'use client'

import { useState } from 'react'
import { toast } from 'sonner'

export function AssignTradeForm({ projectId }: { projectId: string }) {
  const [category, setCategory] = useState('')
  const [inviteLink, setInviteLink] = useState('')

  function handleGenerateLink(e: React.FormEvent) {
    e.preventDefault()
    if (!category.trim()) return

    const baseUrl = window.location.origin
    const link = `${baseUrl}/invite?project_id=${projectId}&role=trade&category=${encodeURIComponent(category.trim())}`
    setInviteLink(link)
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(inviteLink)
    toast.success('Invite link copied to clipboard!')
  }

  if (inviteLink) {
    return (
      <div className="mt-4 bg-[#10b981]/5 border border-[#10b981]/15 p-4 rounded-lg text-center kp-animate-in">
        <div className="flex justify-center mb-2">
          <div className="w-8 h-8 rounded-lg bg-[#10b981]/10 border border-[#10b981]/20 flex items-center justify-center">
            <svg className="w-4 h-4 text-[#10b981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
        </div>
        <h3 className="text-[#10b981] font-medium text-sm mb-1">Invite Generated</h3>
        <p className="text-[10px] text-[#666] mb-4">Send this link to your {category} subcontractor.</p>
        <div className="flex bg-black border border-[#1a1a1a] rounded-lg p-2 items-center gap-2 mb-4">
          <input 
            readOnly 
            value={inviteLink} 
            className="bg-transparent flex-1 text-[10px] text-[#a3a3a3] outline-none font-mono"
          />
        </div>
        <div className="flex gap-2">
          <button 
            onClick={copyToClipboard}
            className="kp-btn-emerald flex-1 py-2 text-[10px]"
          >
            Copy Link
          </button>
          <button 
            onClick={() => { setInviteLink(''); setCategory(''); }}
            className="flex-1 bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] text-[10px] py-2 rounded-lg transition-all duration-200 uppercase tracking-wider"
          >
            Generate Another
          </button>
        </div>
      </div>
    )
  }

  return (
    <form onSubmit={handleGenerateLink} className="mt-4 space-y-4">
      <div>
         <label className="block text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] font-medium mb-2">Trade Category</label>
         <input 
           type="text" 
           required 
           value={category}
           onChange={(e) => setCategory(e.target.value)}
           className="kp-input"
           placeholder="e.g. Electrical, Plumbing"
         />
      </div>

      <button 
        type="submit" 
        className="kp-btn-gold w-full py-2.5 text-center"
      >
        Generate Invite Link
      </button>
    </form>
  )
}
