'use client'

import { useState } from 'react'
import { toast } from 'sonner'
import { applyTradeChecklist } from './actions'

// Master construction trade sequence - correct build order
const MASTER_TRADE_SEQUENCE = [
  { id: 1, trade: 'Site Survey & Geotechnical', category: 'Pre-Construction', defaultDays: 3, icon: '📐' },
  { id: 2, trade: 'Permits & Approvals', category: 'Pre-Construction', defaultDays: 14, icon: '📋' },
  { id: 3, trade: 'Demolition', category: 'Site Work', defaultDays: 5, icon: '🔨' },
  { id: 4, trade: 'Excavation & Grading', category: 'Site Work', defaultDays: 5, icon: '🚜' },
  { id: 5, trade: 'Shoring & Underpinning', category: 'Site Work', defaultDays: 7, icon: '🏗️' },
  { id: 6, trade: 'Foundation & Footings', category: 'Structure', defaultDays: 10, icon: '🧱' },
  { id: 7, trade: 'Waterproofing (Below Grade)', category: 'Structure', defaultDays: 3, icon: '💧' },
  { id: 8, trade: 'Concrete / Slab-on-Grade', category: 'Structure', defaultDays: 7, icon: '🏛️' },
  { id: 9, trade: 'Structural Steel / Framing', category: 'Structure', defaultDays: 14, icon: '🔩' },
  { id: 10, trade: 'Rough Plumbing', category: 'Rough-In', defaultDays: 7, icon: '🔧' },
  { id: 11, trade: 'Rough Electrical', category: 'Rough-In', defaultDays: 7, icon: '⚡' },
  { id: 12, trade: 'Rough HVAC / Mechanical', category: 'Rough-In', defaultDays: 7, icon: '🌡️' },
  { id: 13, trade: 'Fire Suppression / Sprinklers', category: 'Rough-In', defaultDays: 5, icon: '🧯' },
  { id: 14, trade: 'Framing Inspection', category: 'Inspections', defaultDays: 1, icon: '✅' },
  { id: 15, trade: 'Insulation', category: 'Envelope', defaultDays: 5, icon: '🧤' },
  { id: 16, trade: 'Vapour Barrier / Air Barrier', category: 'Envelope', defaultDays: 3, icon: '🛡️' },
  { id: 17, trade: 'Windows & Exterior Doors', category: 'Envelope', defaultDays: 5, icon: '🪟' },
  { id: 18, trade: 'Roofing', category: 'Envelope', defaultDays: 7, icon: '🏠' },
  { id: 19, trade: 'Exterior Cladding / Siding', category: 'Envelope', defaultDays: 10, icon: '🧱' },
  { id: 20, trade: 'Drywall & Taping', category: 'Interior', defaultDays: 10, icon: '🪧' },
  { id: 21, trade: 'Interior Painting', category: 'Interior', defaultDays: 7, icon: '🎨' },
  { id: 22, trade: 'Cabinetry & Millwork', category: 'Interior', defaultDays: 7, icon: '🪚' },
  { id: 23, trade: 'Countertops', category: 'Interior', defaultDays: 3, icon: '🪨' },
  { id: 24, trade: 'Tile & Flooring', category: 'Interior', defaultDays: 7, icon: '🔲' },
  { id: 25, trade: 'Finish Plumbing', category: 'Finish', defaultDays: 5, icon: '🚿' },
  { id: 26, trade: 'Finish Electrical', category: 'Finish', defaultDays: 5, icon: '💡' },
  { id: 27, trade: 'Finish HVAC', category: 'Finish', defaultDays: 3, icon: '❄️' },
  { id: 28, trade: 'Appliance Installation', category: 'Finish', defaultDays: 2, icon: '🍳' },
  { id: 29, trade: 'Interior Doors & Hardware', category: 'Finish', defaultDays: 3, icon: '🚪' },
  { id: 30, trade: 'Final Painting & Touch-Up', category: 'Finish', defaultDays: 3, icon: '🖌️' },
  { id: 31, trade: 'Landscaping & Hardscaping', category: 'Exterior', defaultDays: 7, icon: '🌿' },
  { id: 32, trade: 'Driveway & Paving', category: 'Exterior', defaultDays: 5, icon: '🛣️' },
  { id: 33, trade: 'Fencing & Gates', category: 'Exterior', defaultDays: 3, icon: '🏡' },
  { id: 34, trade: 'Final Clean', category: 'Closeout', defaultDays: 2, icon: '🧹' },
  { id: 35, trade: 'Final Inspection', category: 'Closeout', defaultDays: 1, icon: '🏆' },
  { id: 36, trade: 'Occupancy Permit', category: 'Closeout', defaultDays: 3, icon: '📜' },
  { id: 37, trade: 'Owner Walkthrough / Deficiency', category: 'Closeout', defaultDays: 2, icon: '👁️' },
  { id: 38, trade: 'Project Handover', category: 'Closeout', defaultDays: 1, icon: '🔑' },
]

const CATEGORIES = [...new Set(MASTER_TRADE_SEQUENCE.map(t => t.category))]

const CATEGORY_COLORS: Record<string, string> = {
  'Pre-Construction': 'border-violet-500/30 bg-violet-500/5',
  'Site Work': 'border-amber-500/30 bg-amber-500/5',
  'Structure': 'border-red-500/30 bg-red-500/5',
  'Rough-In': 'border-orange-500/30 bg-orange-500/5',
  'Inspections': 'border-cyan-500/30 bg-cyan-500/5',
  'Envelope': 'border-blue-500/30 bg-blue-500/5',
  'Interior': 'border-pink-500/30 bg-pink-500/5',
  'Finish': 'border-emerald-500/30 bg-emerald-500/5',
  'Exterior': 'border-green-500/30 bg-green-500/5',
  'Closeout': 'border-yellow-500/30 bg-yellow-500/5',
}

const CATEGORY_TEXT: Record<string, string> = {
  'Pre-Construction': 'text-violet-400',
  'Site Work': 'text-amber-400',
  'Structure': 'text-red-400',
  'Rough-In': 'text-orange-400',
  'Inspections': 'text-cyan-400',
  'Envelope': 'text-blue-400',
  'Interior': 'text-pink-400',
  'Finish': 'text-emerald-400',
  'Exterior': 'text-green-400',
  'Closeout': 'text-yellow-400',
}

export function TradeChecklistModal({ projectId }: { projectId: string }) {
  const [isOpen, setIsOpen] = useState(false)
  const [selected, setSelected] = useState<Set<number>>(new Set())
  const [startDate, setStartDate] = useState(() => new Date().toISOString().split('T')[0])
  const [isPending, setIsPending] = useState(false)

  const toggle = (id: number) => {
    setSelected(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const selectCategory = (category: string) => {
    const ids = MASTER_TRADE_SEQUENCE.filter(t => t.category === category).map(t => t.id)
    setSelected(prev => {
      const next = new Set(prev)
      const allSelected = ids.every(id => next.has(id))
      if (allSelected) {
        ids.forEach(id => next.delete(id))
      } else {
        ids.forEach(id => next.add(id))
      }
      return next
    })
  }

  const selectAll = () => {
    if (selected.size === MASTER_TRADE_SEQUENCE.length) {
      setSelected(new Set())
    } else {
      setSelected(new Set(MASTER_TRADE_SEQUENCE.map(t => t.id)))
    }
  }

  const selectedTrades = MASTER_TRADE_SEQUENCE
    .filter(t => selected.has(t.id))
    .map((t, i) => ({ ...t, sequence: i + 1 }))

  const totalDays = selectedTrades.reduce((sum, t) => sum + t.defaultDays, 0)

  async function handleApply() {
    if (selected.size === 0) {
      toast.error('Select at least one trade')
      return
    }
    setIsPending(true)
    const trades = selectedTrades.map(t => ({
      title: t.trade,
      sequence_order: t.sequence,
      duration_days: t.defaultDays,
    }))
    const result = await applyTradeChecklist(projectId, trades, startDate)
    if (result?.error) {
      toast.error(result.error)
    } else {
      toast.success(`${trades.length} milestones added to calendar!`)
      setIsOpen(false)
      setSelected(new Set())
    }
    setIsPending(false)
  }

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="bg-[#c5a55a] hover:bg-[#d4b46a] text-black px-4 py-2 rounded-lg text-sm transition-all flex items-center gap-2 shadow-lg shadow-[#c5a55a]/10"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
        Trade Checklist
      </button>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center bg-black/90 p-4 overflow-y-auto" onClick={() => setIsOpen(false)}>
      <div className="bg-[#050505] border border-[#1a1a1a] rounded-2xl w-full max-w-2xl my-8 shadow-2xl" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-[#1a1a1a]">
          <div>
            <h3 className="text-xl font-light text-[#f5f5f5]">Trade Sequence Checklist</h3>
            <p className="text-[#666] text-xs mt-1">Select the trades needed — they auto-order to the correct build sequence</p>
          </div>
          <button onClick={() => setIsOpen(false)} className="text-[#666] hover:text-[#f5f5f5] text-2xl leading-none transition-colors">&times;</button>
        </div>

        {/* Start Date + Summary Bar */}
        <div className="px-6 py-4 border-b border-[#1a1a1a] flex flex-col sm:flex-row gap-4 sm:items-center sm:justify-between bg-[#0a0a0a]/50">
          <div className="flex items-center gap-3">
            <label className="text-[9px] uppercase text-[#c5a55a] tracking-[0.2em]">Project Start</label>
            <input
              type="date"
              value={startDate}
              onChange={e => setStartDate(e.target.value)}
              className="kp-input text-sm [color-scheme:dark]"
            />
          </div>
          <div className="flex items-center gap-4 text-sm">
            <span className="text-[#a3a3a3]">{selected.size} trades selected</span>
            <span className="text-[#404040]">|</span>
            <span className="text-[#c5a55a] font-mono">~{totalDays} days</span>
            <button onClick={selectAll} className="text-[10px] text-[#666] hover:text-[#f5f5f5] underline underline-offset-2 transition-colors">
              {selected.size === MASTER_TRADE_SEQUENCE.length ? 'Deselect All' : 'Select All'}
            </button>
          </div>
        </div>

        {/* Trade List by Category */}
        <div className="max-h-[50vh] overflow-y-auto p-4 space-y-4">
          {CATEGORIES.map(category => {
            const trades = MASTER_TRADE_SEQUENCE.filter(t => t.category === category)
            const catSelected = trades.filter(t => selected.has(t.id)).length
            const allSelected = catSelected === trades.length
            
            return (
              <div key={category} className={`border rounded-xl p-3 transition-all ${CATEGORY_COLORS[category] || 'border-[#1a1a1a]'}`}>
                {/* Category Header */}
                <button
                  onClick={() => selectCategory(category)}
                  className="w-full flex items-center justify-between px-2 py-1 mb-2"
                >
                  <span className={`text-xs font-semibold uppercase tracking-wider ${CATEGORY_TEXT[category] || 'text-[#a3a3a3]'}`}>
                    {category}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-[#666]">{catSelected}/{trades.length}</span>
                    <div className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-all ${
                      allSelected ? 'bg-[#c5a55a] border-[#c5a55a]' : catSelected > 0 ? 'border-[#c5a55a]/50 bg-[#c5a55a]/20' : 'border-[#404040]'
                    }`}>
                      {allSelected && <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>}
                      {catSelected > 0 && !allSelected && <div className="w-1.5 h-1.5 bg-[#c5a55a] rounded-sm"></div>}
                    </div>
                  </div>
                </button>
                
                {/* Trade Items */}
                <div className="space-y-1">
                  {trades.map(trade => (
                    <button
                      key={trade.id}
                      onClick={() => toggle(trade.id)}
                      className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-all ${
                        selected.has(trade.id) 
                          ? 'bg-[#111]/80 text-[#f5f5f5]' 
                          : 'text-[#666] hover:bg-[#0a0a0a]/50 hover:text-[#a3a3a3]'
                      }`}
                    >
                      <div className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 transition-all ${
                        selected.has(trade.id) ? 'bg-[#c5a55a] border-[#c5a55a]' : 'border-[#404040]'
                      }`}>
                        {selected.has(trade.id) && (
                          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>
                        )}
                      </div>
                      <span className="text-base">{trade.icon}</span>
                      <span className="flex-1 text-sm">{trade.trade}</span>
                      <span className="text-[10px] text-[#404040] font-mono">{trade.defaultDays}d</span>
                    </button>
                  ))}
                </div>
              </div>
            )
          })}
        </div>

        {/* Selected Preview */}
        {selected.size > 0 && (
          <div className="px-6 py-3 border-t border-[#1a1a1a] bg-[#0a0a0a]/30">
            <p className="text-[10px] uppercase text-[#666] mb-2 tracking-[0.2em]">Build Sequence Preview</p>
            <div className="flex flex-wrap gap-1.5">
              {selectedTrades.map(t => (
                <span key={t.id} className="text-[10px] px-2 py-1 rounded-full bg-[#111] text-[#a3a3a3] border border-[#1a1a1a]">
                  {t.sequence}. {t.trade}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Action Footer */}
        <div className="px-6 py-4 border-t border-[#1a1a1a] flex items-center justify-between">
          <button onClick={() => setIsOpen(false)} className="text-[#666] hover:text-[#f5f5f5] text-sm transition-colors">
            Cancel
          </button>
          <button
            onClick={handleApply}
            disabled={isPending || selected.size === 0}
            className="kp-btn-gold px-6 py-2.5 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isPending ? 'Applying...' : `Apply ${selected.size} Trades to Calendar`}
          </button>
        </div>
      </div>
    </div>
  )
}
