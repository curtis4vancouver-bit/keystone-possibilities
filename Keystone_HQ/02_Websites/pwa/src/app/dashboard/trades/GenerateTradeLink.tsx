'use client'

import { useState } from 'react'
import { toast } from 'sonner'

const TRADE_CATEGORIES = [
  'Site Preparation','Excavation','Foundation / Concrete','Framing','Roofing',
  'Plumbing','Electrical','HVAC','Insulation','Drywall','Painting','Flooring',
  'Tiling','Cabinetry & Millwork','Landscaping','General Contractor','Demolition',
  'Masonry','Windows & Doors','Siding / Exterior','Fencing','Paving / Asphalt',
  'Fire Protection','Security Systems','Elevator','Other',
]

export function GenerateTradeLink({ projectId }: { projectId: string }) {
  const [category, setCategory] = useState('')
  const [customCategory, setCustomCategory] = useState('')
  const [inviteLink, setInviteLink] = useState('')

  function handleGenerate(e: React.FormEvent) {
    e.preventDefault()
    const selectedCategory = category === 'Other' ? customCategory.trim() : category
    if (!selectedCategory) return
    const baseUrl = window.location.origin
    setInviteLink(`${baseUrl}/invite/trade?project_id=${projectId}&category=${encodeURIComponent(selectedCategory)}`)
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(inviteLink)
    toast.success('Trade invite link copied!')
  }

  return (
    <div className="kp-card p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-lg bg-[#10b981]/8 border border-[#10b981]/15 flex items-center justify-center">
          <svg className="w-5 h-5 text-[#10b981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
          </svg>
        </div>
        <div>
          <h3 className="text-base font-medium text-[#f5f5f5]">Invite Trade Partner</h3>
          <p className="text-[10px] text-[#666]">Generate a unique link to send to your subcontractor.</p>
        </div>
      </div>

      {inviteLink ? (
        <div className="space-y-4">
          <div className="bg-[#10b981]/5 border border-[#10b981]/15 p-4 rounded-lg">
            <p className="text-[10px] text-[#10b981] font-medium mb-2 uppercase tracking-wider">
              ✓ Link Generated for: <span className="text-[#f5f5f5]">{category === 'Other' ? customCategory : category}</span>
            </p>
            <div className="flex items-center gap-2 bg-black border border-[#1a1a1a] rounded p-2">
              <input readOnly value={inviteLink} className="bg-transparent flex-1 text-xs text-[#a3a3a3] outline-none font-mono" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button onClick={copyToClipboard} className="kp-btn-emerald text-sm py-2.5">📋 Copy Link</button>
            <button onClick={() => { setInviteLink(''); setCategory(''); setCustomCategory(''); }} className="bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] text-sm py-2.5 rounded-lg transition-colors">+ New Link</button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label className="block text-[9px] uppercase tracking-[0.2em] text-[#c5a55a] mb-1.5">Trade Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)} required className="kp-input scheme-dark">
              <option value="">Select a trade...</option>
              {TRADE_CATEGORIES.map(cat => (<option key={cat} value={cat}>{cat}</option>))}
            </select>
          </div>
          {category === 'Other' && (
            <div>
              <label className="block text-[9px] uppercase tracking-[0.2em] text-[#c5a55a] mb-1.5">Custom Category</label>
              <input type="text" value={customCategory} onChange={(e) => setCustomCategory(e.target.value)} required className="kp-input" placeholder="Enter trade name..." />
            </div>
          )}
          <button type="submit" className="kp-btn-emerald w-full py-2.5 text-sm">Generate Invite Link</button>
        </form>
      )}
    </div>
  )
}
