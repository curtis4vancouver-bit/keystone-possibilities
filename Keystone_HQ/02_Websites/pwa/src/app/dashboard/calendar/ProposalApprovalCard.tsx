'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { approveProposal, denyProposal } from './actions'

export function ProposalApprovalCard({ proposal }: { proposal: any }) {
  const [isPending, setIsPending] = useState(false)
  const [resolved, setResolved] = useState(proposal.status !== 'pending')

  const handleApprove = async () => {
    setIsPending(true)
    const result = await approveProposal(proposal.id)
    if ('error' in result) {
      toast.error(result.error)
    } else {
      toast.success(`Proposal approved. ${result.shifted} milestone(s) shifted.`)
      setResolved(true)
    }
    setIsPending(false)
  }

  const handleDeny = async () => {
    setIsPending(true)
    const result = await denyProposal(proposal.id)
    if ('error' in result) {
      toast.error(result.error)
    } else {
      toast.info('Proposal denied.')
      setResolved(true)
    }
    setIsPending(false)
  }

  if (resolved) {
    return (
      <div className="flex items-center gap-2 text-xs text-[#666]">
        <span className={`px-2 py-1 rounded-lg border text-[10px] ${
          proposal.status === 'approved' 
            ? 'bg-[#10b981]/8 text-[#10b981] border-[#10b981]/15' 
            : 'bg-red-500/10 text-red-400 border-red-500/20'
        }`}>
          {proposal.status}
        </span>
      </div>
    )
  }

  return (
    <div className="kp-card p-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <p className="text-sm text-[#f5f5f5] font-medium">{proposal.milestone_title || 'Milestone'}</p>
          <p className="text-[10px] text-[#666] mt-1">
            Proposed: <span className="text-[#3b82f6]">{new Date(proposal.proposed_start_date).toLocaleDateString()}</span>
            <span className="text-[#404040] mx-2">&bull;</span>
            By: <span className="text-[#a3a3a3]">{proposal.trade_email || 'Trade Partner'}</span>
          </p>
        </div>
        <div className="flex gap-2 shrink-0">
          <button onClick={handleApprove} disabled={isPending} className="kp-btn-emerald px-3 py-1.5 text-[10px] disabled:opacity-50">
            {isPending ? '...' : 'Approve & Shift'}
          </button>
          <button onClick={handleDeny} disabled={isPending} className="px-3 py-1.5 text-[10px] bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] rounded-lg transition-colors disabled:opacity-50">
            Deny
          </button>
        </div>
      </div>
    </div>
  )
}
