'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { createMilestone } from './actions'

export default function AddMilestoneForm({ projectId }: { projectId: string }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="kp-btn-emerald flex items-center gap-2"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path></svg>
        Add Milestone
      </button>
    )
  }

  async function action(formData: FormData) {
    setIsPending(true)
    const result = await createMilestone(
      projectId, 
      formData.get('title') as string, 
      formData.get('startDate') as string, 
      parseInt(formData.get('durationDays') as string, 10),
      parseInt(formData.get('sequenceOrder') as string, 10)
    )
    if (result?.error) {
      toast.error(result.error)
    } else {
      toast.success('Milestone added to calendar.')
    }
    setIsPending(false)
    setIsOpen(false)
  }

  return (
    <div className="kp-card p-6 mt-4 w-full">
      <div className="flex justify-between items-center mb-4 border-b border-[#1a1a1a] pb-3">
        <h3 className="text-sm text-[#10b981] font-medium uppercase tracking-wider">Add Manual Schedule Item</h3>
        <button onClick={() => setIsOpen(false)} className="text-[#666] hover:text-[#f5f5f5] transition-colors">&times;</button>
      </div>
      <form action={action} className="space-y-4">
        <div>
          <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Title</label>
          <input type="text" name="title" required className="kp-input" placeholder="e.g. Framing Start" />
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Start Date</label>
            <input type="date" name="startDate" required className="kp-input scheme-dark" />
          </div>
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Duration (Days)</label>
            <input type="number" name="durationDays" required min="1" defaultValue="1" className="kp-input" />
          </div>
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Sequence Order</label>
            <input type="number" name="sequenceOrder" required min="0" defaultValue="1" className="kp-input" />
          </div>
        </div>
        <button type="submit" disabled={isPending} className="kp-btn-emerald w-full py-2.5 font-medium disabled:opacity-50">
          {isPending ? 'Adding...' : 'Save to Master Calendar'}
        </button>
      </form>
    </div>
  )
}
