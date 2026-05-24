'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { submitChangeOrder } from './actions'

interface ChangeOrderModalProps {
  projectId: string
  onSuccess?: () => void
}

export function ChangeOrderModal({ projectId, onSuccess }: ChangeOrderModalProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')
  const [file, setFile] = useState<File | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (!amount || parseFloat(amount) <= 0) {
      toast.error('Please enter a valid change order amount')
      return
    }
    if (!description.trim()) {
      toast.error('Justification is required for change orders')
      return
    }

    setIsPending(true)
    const formData = new FormData()
    formData.append('project_id', projectId)
    formData.append('amount', amount)
    formData.append('description', description)
    if (file) {
      formData.append('file', file)
    }

    try {
      const result = await submitChangeOrder(formData)
      if (result.error) {
        toast.error(result.error)
      } else {
        toast.success('Change order requested successfully!')
        setIsOpen(false)
        setAmount('')
        setDescription('')
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
        className="bg-gradient-to-r from-[#c5a55a] to-[#9a7e3f] text-black px-4 py-2 rounded-lg text-sm font-semibold tracking-wider uppercase transition-all flex items-center gap-2 shadow-lg shadow-[#c5a55a]/10 cursor-pointer"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Request Change Order
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
            <h3 className="text-xl font-light text-[#f5f5f5]">Request Change Order</h3>
            <p className="text-[#666] text-xs mt-1">Submit out-of-scope variations for PM review.</p>
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
              Estimated Amount ($)
            </label>
            <input
              type="number"
              step="0.01"
              required
              min="0.01"
              placeholder="0.00"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="kp-input text-sm font-mono [color-scheme:dark]"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Change Request Justification
            </label>
            <textarea
              required
              rows={3}
              placeholder="Explain why this change is necessary (e.g. bedrock encountered, structural plan discrepancy)..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="kp-input text-sm resize-none"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Supporting Photo / Proof-of-Condition
            </label>
            <div className="relative group border border-dashed border-[#1a1a1a] hover:border-[#c5a55a]/40 rounded-xl p-4 transition-all text-center bg-[#020202]">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <div className="space-y-1">
                <svg className="w-8 h-8 text-[#404040] mx-auto group-hover:text-[#c5a55a] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <p className="text-xs text-[#a3a3a3] font-medium">
                  {file ? file.name : 'Tap to capture or upload photo'}
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
              className="bg-gradient-to-r from-[#c5a55a] to-[#9a7e3f] hover:from-[#d4b46a] hover:to-[#a38545] text-black px-6 py-2.5 rounded-lg text-sm font-semibold tracking-wider uppercase transition-all disabled:opacity-50 cursor-pointer"
            >
              {isPending ? 'Requesting...' : 'Request Change'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
