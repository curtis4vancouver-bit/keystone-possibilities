'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { logInspection } from './actions'

interface InspectionReportModalProps {
  projectId: string
  milestones: { id: string; title: string }[]
  onSuccess?: () => void
}

export function InspectionReportModal({ projectId, milestones, onSuccess }: InspectionReportModalProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [title, setTitle] = useState('')
  const [milestoneId, setMilestoneId] = useState('')
  const [status, setStatus] = useState<'passed' | 'failed'>('passed')
  const [notes, setNotes] = useState('')
  const [file, setFile] = useState<File | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (!title.trim()) {
      toast.error('Inspection title is required')
      return
    }

    setIsPending(true)
    const formData = new FormData()
    formData.append('project_id', projectId)
    formData.append('title', title)
    formData.append('status', status)
    formData.append('notes', notes)
    if (milestoneId) {
      formData.append('milestone_id', milestoneId)
    }
    if (file) {
      formData.append('file', file)
    }

    try {
      const result = await logInspection(formData)
      if (result.error) {
        toast.error(result.error)
      } else {
        toast.success(`Inspection report logged as ${status.toUpperCase()}!`)
        setIsOpen(false)
        setTitle('')
        setMilestoneId('')
        setStatus('passed')
        setNotes('')
        setFile(null)
        if (onSuccess) onSuccess()
      }
    } catch (err) {
      console.error(err)
      toast.error('An unexpected error occurred')
    } finally {
      setIsPending(false)
    }
  }

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="bg-[#3b82f6] hover:bg-[#2563eb] text-white px-4 py-2 rounded-lg text-sm font-semibold tracking-wider uppercase transition-all flex items-center gap-2 shadow-lg shadow-[#3b82f6]/15 cursor-pointer"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        Log QA Inspection
      </button>
    )
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4 overflow-y-auto"
      onClick={() => setIsOpen(false)}
    >
      <div
        className="bg-[#050505] border border-[#1a1a1a] rounded-2xl w-full max-w-md my-8 shadow-2xl relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-[#1a1a1a]">
          <div>
            <h3 className="text-xl font-light text-[#f5f5f5]">Log Quality Inspection</h3>
            <p className="text-[#666] text-xs mt-1">Submit official municipal reviews or structural sign-offs.</p>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="text-[#666] hover:text-[#f5f5f5] text-2xl leading-none transition-colors cursor-pointer"
          >
            &times;
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Inspection Title / Name
            </label>
            <input
              type="text"
              required
              placeholder="e.g. framing inspection, plumbing rough-in"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="kp-input text-sm"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Link to Project Milestone (Optional)
            </label>
            <select
              value={milestoneId}
              onChange={(e) => setMilestoneId(e.target.value)}
              className="kp-input text-sm [color-scheme:dark] bg-[#050505]"
            >
              <option value="">-- Unlinked --</option>
              {milestones.map((ms) => (
                <option key={ms.id} value={ms.id}>
                  {ms.title}
                </option>
              ))}
            </select>
          </div>

          {/* Status selector */}
          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Inspection Outcome
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setStatus('passed')}
                className={`py-2.5 rounded-lg border text-xs font-semibold tracking-wider uppercase transition-all cursor-pointer ${
                  status === 'passed'
                    ? 'bg-[#10b981]/15 text-[#10b981] border-[#10b981]'
                    : 'bg-black border-[#1a1a1a] text-[#666] hover:text-[#a3a3a3]'
                }`}
              >
                Passed
              </button>
              <button
                type="button"
                onClick={() => setStatus('failed')}
                className={`py-2.5 rounded-lg border text-xs font-semibold tracking-wider uppercase transition-all cursor-pointer ${
                  status === 'failed'
                    ? 'bg-red-500/15 text-red-500 border-red-500'
                    : 'bg-black border-[#1a1a1a] text-[#666] hover:text-[#a3a3a3]'
                }`}
              >
                Action Needed
              </button>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Inspection Details / Notes
            </label>
            <textarea
              rows={3}
              placeholder="Record inspector names, items checked, or remediation instructions if failed..."
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="kp-input text-sm resize-none"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Attachment (Signed PDF Report or Site Photo)
            </label>
            <div className="relative group border border-dashed border-[#1a1a1a] hover:border-[#c5a55a]/40 rounded-xl p-4 transition-all text-center bg-[#020202]">
              <input
                type="file"
                accept="image/*,application/pdf"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <div className="space-y-1">
                <svg className="w-8 h-8 text-[#404040] mx-auto group-hover:text-[#c5a55a] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p className="text-xs text-[#a3a3a3] font-medium">
                  {file ? file.name : 'Tap to select PDF or image file'}
                </p>
                <p className="text-[9px] text-[#404040]">Maximum upload size: 10MB</p>
              </div>
            </div>
          </div>

          {/* Action Footer */}
          <div className="pt-4 border-t border-[#1a1a1a] flex items-center justify-between">
            <button
              type="button"
              onClick={() => setIsOpen(false)}
              className="text-[#666] hover:text-[#f5f5f5] text-sm transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isPending}
              className="bg-gradient-to-r from-[#3b82f6] to-[#1d4ed8] hover:from-[#60a5fa] hover:to-[#2563eb] text-white px-6 py-2.5 rounded-lg text-sm font-semibold tracking-wider uppercase transition-all disabled:opacity-50 cursor-pointer"
            >
              {isPending ? 'Logging...' : 'Log Report'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
