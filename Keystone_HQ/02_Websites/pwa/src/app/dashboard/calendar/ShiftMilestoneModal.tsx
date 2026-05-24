'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { shiftMilestoneDates } from './actions'

export function ShiftMilestoneModal({ milestone }: { milestone: any }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [newDate, setNewDate] = useState(milestone.start_date)

  const handleShift = async () => {
    setIsPending(true)
    const result = await shiftMilestoneDates(milestone.id, newDate)
    if (result?.error) {
      toast.error(result.error)
    } else {
      toast.success(`Schedule shifted. ${result.shifted} milestone(s) updated.`)
    }
    setIsPending(false)
    setIsOpen(false)
  }

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="text-[#f59e0b] hover:text-[#fbbf24] text-[10px] px-2 py-1 rounded-lg border border-[#f59e0b]/15 bg-[#f59e0b]/8 transition-colors uppercase tracking-wider"
      >
        Shift Date
      </button>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setIsOpen(false)}>
      <div className="kp-card-gold p-6 w-full max-w-sm" onClick={e => e.stopPropagation()}>
        <h3 className="text-lg font-light text-[#f5f5f5] mb-2">Shift Schedule</h3>
        <p className="text-[#a3a3a3] text-sm mb-4">
          Changing the start date for <strong className="text-[#f5f5f5]">{milestone.title}</strong> will automatically shift all subsequent dependent milestones.
        </p>
        <div className="space-y-4">
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">New Start Date</label>
            <input type="date" value={newDate} onChange={(e) => setNewDate(e.target.value)} className="kp-input [color-scheme:dark]" />
          </div>
          <div className="flex gap-3 mt-6">
            <button onClick={() => setIsOpen(false)} className="flex-1 px-4 py-2 bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] rounded-lg text-sm transition-colors">Cancel</button>
            <button onClick={handleShift} disabled={isPending || newDate === milestone.start_date} className="kp-btn-emerald flex-1 px-4 py-2 text-sm disabled:opacity-50">
              {isPending ? 'Shifting...' : 'Apply Shift'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
