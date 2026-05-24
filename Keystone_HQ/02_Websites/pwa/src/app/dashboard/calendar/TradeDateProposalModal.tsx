'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { proposeDate } from './actions'

export function TradeDateProposalModal({ milestone }: { milestone: any }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [newDate, setNewDate] = useState(milestone.start_date)

  const handlePropose = async () => {
    setIsPending(true)
    const result = await proposeDate(milestone.id, newDate)
    if (result?.error) {
      toast.error(result.error)
    } else {
      toast.success('Date proposal sent to Project Manager for review.')
    }
    setIsPending(false)
    setIsOpen(false)
  }

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="text-[#3b82f6] hover:text-[#60a5fa] text-[10px] px-2 py-1 rounded-lg border border-[#3b82f6]/15 bg-[#3b82f6]/8 transition-colors uppercase tracking-wider"
      >
        Propose Date Change
      </button>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setIsOpen(false)}>
      <div className="kp-card-gold p-6 w-full max-w-sm text-left" onClick={e => e.stopPropagation()}>
        <h3 className="text-lg font-light text-[#f5f5f5] mb-2">Propose New Date</h3>
        <p className="text-[#a3a3a3] text-sm mb-4">
          If you have a scheduling conflict, propose an alternate start date for <strong className="text-[#f5f5f5]">{milestone.title}</strong>. The PM will review your request.
        </p>
        <div className="space-y-4">
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Proposed Start Date</label>
            <input type="date" value={newDate} onChange={(e) => setNewDate(e.target.value)} className="kp-input [color-scheme:dark]" />
          </div>
          <div className="flex gap-3 mt-6">
            <button onClick={() => setIsOpen(false)} className="flex-1 px-4 py-2 bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] rounded-lg text-sm transition-colors">Cancel</button>
            <button onClick={handlePropose} disabled={isPending || newDate === milestone.start_date} className="kp-btn-emerald flex-1 px-4 py-2 text-sm disabled:opacity-50">
              {isPending ? 'Sending...' : 'Send Proposal'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
