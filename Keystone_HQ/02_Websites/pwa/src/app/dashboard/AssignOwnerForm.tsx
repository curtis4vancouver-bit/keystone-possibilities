'use client'

import { useState } from 'react'
import { assignOwner } from './assignOwnerAction'

export default function AssignOwnerForm({ projectId, currentOwnerId }: { projectId: string, currentOwnerId: string | null }) {
  const [isOpen, setIsOpen] = useState(false)
  const [message, setMessage] = useState('')

  if (currentOwnerId) {
    return (
      <div className="text-[10px] bg-[#10b981]/8 text-[#10b981] px-3 py-1.5 rounded-lg border border-[#10b981]/15 uppercase tracking-wider font-medium">
        ✓ Owner Assigned
      </div>
    )
  }

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="text-[10px] bg-[#f59e0b]/8 text-[#f59e0b] hover:bg-[#f59e0b]/12 px-3 py-1.5 rounded-lg transition-all duration-200 border border-[#f59e0b]/15 uppercase tracking-wider font-medium"
      >
        Assign Owner
      </button>
    )
  }

  async function action(formData: FormData) {
    setMessage('Assigning...')
    const result = await assignOwner(projectId, formData)
    if (result.error) {
      setMessage(result.error)
    } else {
      setMessage('Owner assigned successfully!')
      setIsOpen(false)
    }
  }

  return (
    <div className="kp-card p-4 text-left w-64 kp-animate-in">
      <div className="flex justify-between items-center mb-3">
        <span className="text-[9px] uppercase tracking-[0.2em] text-[#c5a55a] font-medium">Link Owner</span>
        <button onClick={() => setIsOpen(false)} className="text-[#404040] hover:text-[#f5f5f5] transition-colors text-sm">&times;</button>
      </div>
      <form action={action} className="space-y-3">
        <input 
          type="email" 
          name="email" 
          required 
          placeholder="owner@email.com" 
          className="kp-input text-xs"
        />
        <button type="submit" className="kp-btn-emerald w-full py-2 text-center text-[10px]">
          Save
        </button>
      </form>
      {message && <p className="text-xs text-[#f59e0b] mt-2">{message}</p>}
    </div>
  )
}
