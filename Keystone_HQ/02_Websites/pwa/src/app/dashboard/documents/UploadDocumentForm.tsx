'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { uploadDocument } from './actions'

export function UploadDocumentForm({ projectId }: { projectId: string }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, setIsPending] = useState(false)

  async function handleSubmit(formData: FormData) {
    setIsPending(true)
    formData.append('project_id', projectId)
    const result = await uploadDocument(formData)
    if (result?.error) {
      toast.error(result.error)
    } else {
      toast.success('Document uploaded successfully.')
      setIsOpen(false)
    }
    setIsPending(false)
  }

  if (!isOpen) {
    return (
      <button 
        onClick={() => setIsOpen(true)}
        className="kp-btn-emerald px-4 py-2 text-sm flex items-center gap-2"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
        Upload Document
      </button>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setIsOpen(false)}>
      <div className="p-6 w-full max-w-md rounded-xl border border-[#c5a55a]/20 bg-[#0a0a0a] shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-center mb-6 border-b border-[#1a1a1a] pb-3">
          <h3 className="text-lg font-light text-[#f5f5f5]">Upload Document</h3>
          <button onClick={() => setIsOpen(false)} className="text-[#666] hover:text-[#f5f5f5] text-xl transition-colors">&times;</button>
        </div>
        <form action={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Document Title</label>
            <input type="text" name="title" required className="kp-input" placeholder="e.g. PM Contract - Smith Residence" />
          </div>
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Document Type</label>
            <select name="document_type" required className="kp-input [color-scheme:dark]">
              <option value="pm_contract">PM Contract</option>
              <option value="wcb">WCB Certificate</option>
              <option value="liability_insurance">Liability Insurance</option>
              <option value="subcontractor_agreement">Subcontractor Agreement</option>
              <option value="permit">Permit</option>
              <option value="invoice">Invoice</option>
              <option value="inspection_report">Inspection Report</option>
              <option value="change_order">Change Order</option>
              <option value="site_photo">Site Photo</option>
            </select>
          </div>
          <div>
            <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">File</label>
            <input type="file" name="file" required accept=".pdf,.png,.jpg,.jpeg,.doc,.docx" className="w-full text-sm text-[#a3a3a3] file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-[#10b981] file:text-white hover:file:bg-[#0d9668] file:cursor-pointer file:transition-colors" />
            <p className="text-[10px] text-[#404040] mt-1">Accepted: PDF, PNG, JPG, DOC/DOCX (max 10MB)</p>
          </div>
          <button type="submit" disabled={isPending} className="kp-btn-emerald w-full py-2.5 font-medium text-sm disabled:opacity-50">
            {isPending ? 'Uploading...' : 'Upload to Vault'}
          </button>
        </form>
      </div>
    </div>
  )
}
