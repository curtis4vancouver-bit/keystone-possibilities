'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { submitInvoice } from './actions'

interface InvoiceModalProps {
  projectId: string
  onSuccess?: () => void
}

export function InvoiceModal({ projectId, onSuccess }: InvoiceModalProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')
  const [file, setFile] = useState<File | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (!amount || parseFloat(amount) <= 0) {
      toast.error('Please enter a valid invoice amount')
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
      const result = await submitInvoice(formData)
      if (result.error) {
        toast.error(result.error)
      } else {
        toast.success('Invoice submitted successfully!')
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
        className="bg-[#10b981] hover:bg-[#059669] text-white px-4 py-2 rounded-lg text-sm font-semibold tracking-wider uppercase transition-all flex items-center gap-2 shadow-lg shadow-[#10b981]/15 cursor-pointer"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4"></path>
        </svg>
        Submit Invoice
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
            <h3 className="text-xl font-light text-[#f5f5f5]">Submit Trade Invoice</h3>
            <p className="text-[#666] text-xs mt-1">Upload invoice details to request capital release.</p>
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
              Invoice Amount ($)
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
              Work Description / Items
            </label>
            <textarea
              required
              rows={3}
              placeholder="Detail what tasks were completed or materials purchased..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="kp-input text-sm resize-none"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] uppercase text-[#c5a55a] tracking-[0.2em] font-medium block">
              Attachment (Receipt / PDF Invoice)
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
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
              className="kp-btn-emerald disabled:opacity-50 cursor-pointer"
            >
              {isPending ? 'Submitting...' : 'Submit Request'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
