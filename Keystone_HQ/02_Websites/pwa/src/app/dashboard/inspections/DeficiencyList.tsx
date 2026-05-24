'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { resolveDeficiency } from './actions'

interface DeficiencyListProps {
  initialDeficiencies: any[]
  isPM: boolean
  projectId: string
}

export function DeficiencyList({ initialDeficiencies, isPM, projectId }: DeficiencyListProps) {
  const [deficiencies, setDeficiencies] = useState(initialDeficiencies)
  const [isPending, setIsPending] = useState<string | null>(null)

  async function handleResolve(documentId: string) {
    setIsPending(documentId)
    try {
      const result = await resolveDeficiency(documentId, projectId)
      if (result.error) {
        toast.error(result.error)
      } else {
        toast.success('Deficiency marked as resolved!')
        // Remove from local list
        setDeficiencies(prev => prev.filter(d => d.id !== documentId))
      }
    } catch (err) {
      console.error(err)
      toast.error('An unexpected error occurred')
    } finally {
      setIsPending(null)
    }
  }

  if (deficiencies.length === 0) return null

  return (
    <div className="space-y-4 kp-animate-in">
      <div className="border border-red-500/30 bg-red-500/5 rounded-2xl p-4 flex items-center gap-3">
        <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse flex-shrink-0" />
        <h4 className="text-sm font-semibold tracking-wider uppercase text-red-400">
          Active Site Deficiencies ({deficiencies.length})
        </h4>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {deficiencies.map((item) => (
          <div
            key={item.id}
            className="bg-[#050505] border border-red-500/20 rounded-xl p-5 flex flex-col justify-between gap-4 shadow-lg shadow-red-500/2"
          >
            <div>
              <div className="flex justify-between items-start gap-2">
                <h5 className="text-sm font-semibold text-white uppercase tracking-wide">
                  {item.title.replace(' - FAILED', '')}
                </h5>
                <span className="bg-red-500/8 text-red-500 border border-red-500/15 rounded px-2 py-0.5 text-[9px] uppercase font-bold tracking-wider font-mono">
                  ACTION NEEDED
                </span>
              </div>
              <p className="text-xs text-[#666] font-mono mt-1">
                Logged: {new Date(item.created_at).toLocaleDateString()} by{' '}
                {item.users?.full_name || 'Inspector'}
              </p>
              {item.file_url && item.file_url !== '#' && (
                <a
                  href={item.file_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs text-[#c5a55a] hover:underline mt-3"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  View Attachment
                </a>
              )}
            </div>

            {isPM && (
              <div className="border-t border-[#1a1a1a] pt-3 text-right">
                <button
                  onClick={() => handleResolve(item.id)}
                  disabled={isPending !== null}
                  className="bg-[#10b981]/15 hover:bg-[#10b981] text-[#10b981] hover:text-white border border-[#10b981]/30 px-3 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all cursor-pointer disabled:opacity-50"
                >
                  {isPending === item.id ? 'Resolving...' : 'Mark Resolved'}
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
