'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { updateLedgerStatus } from './actions'

interface LedgerTableProps {
  ledger: any[]
  isPM: boolean
  projectId: string
}

export function LedgerTable({ ledger: initialLedger, isPM, projectId }: LedgerTableProps) {
  const [ledger, setLedger] = useState(initialLedger)
  const [isPending, setIsPending] = useState<string | null>(null)

  async function handleStatusChange(ledgerId: string, newStatus: 'approved' | 'paid' | 'denied') {
    let denyReason = ''
    if (newStatus === 'denied') {
      const reason = prompt('Please enter a reason for denying this payment request:')
      if (reason === null) return // User cancelled
      if (!reason.trim()) {
        toast.error('Denial reason is required')
        return
      }
      denyReason = reason
    }

    setIsPending(ledgerId)
    try {
      const result = await updateLedgerStatus(ledgerId, projectId, newStatus, denyReason)
      if (result.error) {
        toast.error(result.error)
      } else {
        toast.success(`Request ${newStatus} successfully!`)
        // Optimistically update the UI status
        setLedger(prev =>
          prev.map(item =>
            item.id === ledgerId
              ? {
                  ...item,
                  status: newStatus,
                  description: newStatus === 'denied' 
                    ? item.description + ` [PM DENIAL REASON: ${denyReason}]`
                    : item.description
                }
              : item
          )
        )
      }
    } catch (err) {
      console.error(err)
      toast.error('Failed to update status')
    } finally {
      setIsPending(null)
    }
  }

  return (
    <div className="kp-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-[#a3a3a3]">
          <thead className="bg-[#050505] text-[9px] uppercase text-[#666] border-b border-[#1a1a1a] tracking-[0.2em]">
            <tr>
              <th className="px-6 py-4 font-semibold">Type</th>
              <th className="px-6 py-4 font-semibold">Contractor / Trade</th>
              <th className="px-6 py-4 font-semibold">Description</th>
              <th className="px-6 py-4 font-semibold">Amount</th>
              <th className="px-6 py-4 font-semibold">Status</th>
              <th className="px-6 py-4 font-semibold">Submitted</th>
              {isPM && <th className="px-6 py-4 font-semibold text-right">Actions</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1a1a1a] bg-[#020202]">
            {ledger.map((item: any) => {
              const tradeName = item.project_trades?.trade_category || 'General Contractor'
              const requestorName = item.users?.full_name || 'System'
              
              return (
                <tr key={item.id} className="hover:bg-[#050505]/50 transition-colors">
                  <td className="px-6 py-4 capitalize font-medium text-white">
                    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] uppercase font-mono tracking-wider border ${
                      item.type === 'invoice' ? 'bg-[#10b981]/5 text-[#10b981] border-[#10b981]/15' : 
                      item.type === 'change_order' ? 'bg-[#f59e0b]/5 text-[#f59e0b] border-[#f59e0b]/15' :
                      'bg-blue-500/5 text-blue-400 border-blue-500/15'
                    }`}>
                      {item.type.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <p className="text-white font-light text-sm">{tradeName}</p>
                    <p className="text-[10px] text-[#666]">{requestorName}</p>
                  </td>
                  <td className="px-6 py-4 max-w-xs md:max-w-md">
                    <span className="text-sm text-[#a3a3a3] block line-clamp-2">
                      {item.description}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-mono text-[#c5a55a] font-medium text-sm">
                    ${Number(item.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-0.5 rounded text-[10px] border tracking-wider uppercase font-semibold ${
                      item.status === 'approved' ? 'bg-[#10b981]/8 text-[#10b981] border-[#10b981]/15' : 
                      item.status === 'paid' ? 'bg-[#3b82f6]/8 text-[#3b82f6] border-[#3b82f6]/15' : 
                      item.status === 'denied' ? 'bg-red-500/8 text-red-500 border-red-500/15' :
                      'bg-[#f59e0b]/8 text-[#f59e0b] border-[#f59e0b]/15'
                    }`}>{item.status}</span>
                  </td>
                  <td className="px-6 py-4 text-xs text-[#666] font-mono">
                    {new Date(item.created_at).toLocaleDateString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      year: '2-digit'
                    })}
                  </td>
                  {isPM && (
                    <td className="px-6 py-4 text-right space-x-2 whitespace-nowrap">
                      {item.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handleStatusChange(item.id, 'approved')}
                            disabled={isPending !== null}
                            className="bg-[#10b981]/10 hover:bg-[#10b981] text-[#10b981] hover:text-white border border-[#10b981]/25 px-2.5 py-1 rounded text-xs transition-all font-semibold cursor-pointer disabled:opacity-50"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleStatusChange(item.id, 'denied')}
                            disabled={isPending !== null}
                            className="bg-red-500/10 hover:bg-red-500 text-red-500 hover:text-white border border-red-500/25 px-2.5 py-1 rounded text-xs transition-all font-semibold cursor-pointer disabled:opacity-50"
                          >
                            Deny
                          </button>
                        </>
                      )}
                      {item.status === 'approved' && (
                        <button
                          onClick={() => handleStatusChange(item.id, 'paid')}
                          disabled={isPending !== null}
                          className="bg-blue-500/10 hover:bg-blue-500 text-blue-400 hover:text-white border border-blue-500/25 px-2.5 py-1 rounded text-xs transition-all font-semibold cursor-pointer disabled:opacity-50"
                        >
                          Mark Paid
                        </button>
                      )}
                      {item.status !== 'pending' && item.status !== 'approved' && (
                        <span className="text-xs text-[#404040] italic font-mono">-</span>
                      )}
                    </td>
                  )}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
