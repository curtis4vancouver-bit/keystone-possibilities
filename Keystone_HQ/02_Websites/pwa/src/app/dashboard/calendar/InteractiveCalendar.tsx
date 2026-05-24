'use client'

import { useState, useCallback } from 'react'
import { createMilestone } from './actions'
import { useRouter } from 'next/navigation'

interface Milestone {
  id: string
  title: string
  start_date: string
  end_date: string
  duration_days: number
  sequence_order: number
  status: string
}

interface InteractiveCalendarProps {
  milestones: Milestone[]
  projectId: string
  isPM: boolean
  projectStartDate?: string
}

export default function InteractiveCalendar({ milestones, projectId, isPM, projectStartDate }: InteractiveCalendarProps) {
  const router = useRouter()
  
  // Default to project start date or earliest milestone or today
  const getInitialDate = () => {
    if (projectStartDate) return new Date(projectStartDate + 'T00:00:00')
    if (milestones.length > 0) {
      const earliest = milestones.reduce((min, m) => m.start_date < min ? m.start_date : min, milestones[0].start_date)
      return new Date(earliest + 'T00:00:00')
    }
    return new Date()
  }

  const [currentDate, setCurrentDate] = useState(getInitialDate())
  const [selectedDate, setSelectedDate] = useState<string | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)
  const [isPending, setIsPending] = useState(false)
  const [selectedMilestone, setSelectedMilestone] = useState<Milestone | null>(null)

  const year = currentDate.getFullYear()
  const month = currentDate.getMonth()

  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const firstDayOfWeek = new Date(year, month, 1).getDay()
  const monthName = currentDate.toLocaleString('default', { month: 'long' })

  // Previous month days for leading cells
  const prevMonthDays = new Date(year, month, 0).getDate()

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1))
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1))
  const goToToday = () => setCurrentDate(new Date())

  // Get milestones that fall on a specific date
  const getMilestonesForDate = useCallback((dateStr: string) => {
    return milestones.filter(m => {
      const start = new Date(m.start_date + 'T00:00:00')
      const end = new Date(m.end_date + 'T00:00:00')
      const check = new Date(dateStr + 'T00:00:00')
      return check >= start && check <= end
    })
  }, [milestones])

  // Check if a date is the start of a milestone
  const isStartDate = (dateStr: string) => milestones.some(m => m.start_date === dateStr)
  const isEndDate = (dateStr: string) => milestones.some(m => m.end_date === dateStr)

  const todayStr = new Date().toISOString().split('T')[0]

  // Handle date click — opens the add form for that date
  const handleDateClick = (dateStr: string) => {
    const dayMilestones = getMilestonesForDate(dateStr)
    if (dayMilestones.length > 0) {
      setSelectedMilestone(dayMilestones[0])
      setSelectedDate(dateStr)
      setShowAddForm(false)
    } else if (isPM) {
      setSelectedDate(dateStr)
      setSelectedMilestone(null)
      setShowAddForm(true)
    }
  }

  // Handle "+ Add Schedule Item" button
  const handleAddScheduleItem = () => {
    setSelectedDate(todayStr)
    setSelectedMilestone(null)
    setShowAddForm(true)
  }

  // Handle form submit
  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (!selectedDate) return
    setIsPending(true)

    const form = e.currentTarget
    const formData = new FormData(form)
    const title = formData.get('title') as string
    const startDate = formData.get('startDate') as string || selectedDate
    const duration = parseInt(formData.get('durationDays') as string, 10)
    const sequence = parseInt(formData.get('sequenceOrder') as string, 10)

    const result = await createMilestone(projectId, title, startDate, duration, sequence)
    
    if (result?.error) {
      alert(result.error)
    }
    
    setIsPending(false)
    setShowAddForm(false)
    setSelectedDate(null)
    setSelectedMilestone(null)
    router.refresh()
  }

  // Status color map
  const statusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-emerald-500/20 border-emerald-500/40 text-emerald-400'
      case 'in_progress': return 'bg-blue-500/20 border-blue-500/40 text-blue-400'
      default: return 'bg-amber-500/15 border-amber-500/30 text-amber-400'
    }
  }

  const statusDot = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-emerald-500'
      case 'in_progress': return 'bg-blue-500'
      default: return 'bg-amber-500'
    }
  }

  // Build calendar grid — 6 rows always for consistency
  const days: { day: number; isCurrentMonth: boolean; dateStr: string }[] = []
  
  // Previous month trailing days
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const d = prevMonthDays - i
    const m = month === 0 ? 12 : month
    const y = month === 0 ? year - 1 : year
    days.push({ day: d, isCurrentMonth: false, dateStr: `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}` })
  }
  
  // Current month days
  for (let d = 1; d <= daysInMonth; d++) {
    days.push({ day: d, isCurrentMonth: true, dateStr: `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}` })
  }
  
  // Next month leading days
  let nextDay = 1
  while (days.length < 42) {
    const m = month + 2 > 12 ? 1 : month + 2
    const y = month + 2 > 12 ? year + 1 : year
    days.push({ day: nextDay, isCurrentMonth: false, dateStr: `${y}-${String(m).padStart(2, '0')}-${String(nextDay).padStart(2, '0')}` })
    nextDay++
  }

  // Count milestones this month
  const monthMilestoneCount = milestones.filter(m => {
    const start = new Date(m.start_date + 'T00:00:00')
    const end = new Date(m.end_date + 'T00:00:00')
    const monthStart = new Date(year, month, 1)
    const monthEnd = new Date(year, month + 1, 0)
    return start <= monthEnd && end >= monthStart
  }).length

  return (
    <div className="space-y-4">
      {/* Calendar Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <button onClick={prevMonth} className="p-2 hover:bg-[#111] rounded-lg transition-colors text-[#666] hover:text-[#f5f5f5]">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" /></svg>
            </button>
            <h3 className="text-2xl font-light text-[#f5f5f5] min-w-[200px] text-center">{monthName} {year}</h3>
            <button onClick={nextMonth} className="p-2 hover:bg-[#111] rounded-lg transition-colors text-[#666] hover:text-[#f5f5f5]">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" /></svg>
            </button>
          </div>
          <button onClick={goToToday} className="text-[10px] uppercase tracking-wider bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] text-[#a3a3a3] px-3 py-1.5 rounded-lg transition-colors">
            Today
          </button>
          <span className="text-[11px] text-[#666]">{monthMilestoneCount} event{monthMilestoneCount !== 1 ? 's' : ''} this month</span>
        </div>
        {isPM && (
          <button 
            onClick={handleAddScheduleItem}
            className="kp-btn-emerald flex items-center gap-2 text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" /></svg>
            Add Schedule Item
          </button>
        )}
      </div>

      {/* Day Labels */}
      <div className="grid grid-cols-7 border border-[#1a1a1a] rounded-t-xl overflow-hidden">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="bg-[#0d0d0d] py-3 text-center text-[10px] uppercase tracking-[0.2em] text-[#555] font-medium border-r border-[#1a1a1a] last:border-r-0">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 border-l border-b border-[#1a1a1a] rounded-b-xl overflow-hidden -mt-4">
        {days.map((cell, i) => {
          const dayMilestones = getMilestonesForDate(cell.dateStr)
          const isToday = cell.dateStr === todayStr
          const isStart = isStartDate(cell.dateStr)
          const isEnd = isEndDate(cell.dateStr)
          const isSelected = cell.dateStr === selectedDate
          const isWeekend = i % 7 === 0 || i % 7 === 6

          return (
            <div
              key={`${cell.dateStr}-${i}`}
              onClick={() => cell.isCurrentMonth && handleDateClick(cell.dateStr)}
              className={`
                min-h-[110px] p-2 transition-all duration-150 relative group border-r border-t border-[#1a1a1a]
                ${cell.isCurrentMonth ? (isPM ? 'cursor-pointer hover:bg-[#111]' : 'cursor-default') : 'opacity-30 cursor-default'}
                ${isSelected ? 'ring-2 ring-inset ring-[#c5a55a] bg-[#111]' : ''}
                ${isToday && cell.isCurrentMonth ? 'bg-[#0a0f0a]' : 'bg-[#050505]'}
                ${isWeekend && cell.isCurrentMonth ? 'bg-[#040404]' : ''}
              `}
            >
              {/* Date Number */}
              <div className="flex items-center justify-between mb-1.5">
                <span className={`
                  text-sm font-medium w-7 h-7 flex items-center justify-center rounded-full transition-colors
                  ${isToday && cell.isCurrentMonth ? 'bg-[#c5a55a] text-black font-bold' : ''}
                  ${!isToday && cell.isCurrentMonth ? (isWeekend ? 'text-[#404040]' : 'text-[#a3a3a3]') : 'text-[#333]'}
                `}>
                  {cell.day}
                </span>
                <div className="flex gap-0.5">
                  {isStart && cell.isCurrentMonth && (
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" title="Milestone starts" />
                  )}
                  {isEnd && cell.isCurrentMonth && (
                    <span className="w-1.5 h-1.5 rounded-full bg-red-400" title="Milestone ends" />
                  )}
                </div>
              </div>

              {/* Milestones on this date */}
              {cell.isCurrentMonth && (
                <div className="space-y-0.5">
                  {dayMilestones.slice(0, 3).map(m => (
                    <div
                      key={m.id}
                      className={`text-[10px] px-1.5 py-0.5 rounded border truncate ${statusColor(m.status)}`}
                      title={`${m.title} — ${m.status} (${m.duration_days} day${m.duration_days !== 1 ? 's' : ''})`}
                    >
                      {isStartDate(m.start_date) && cell.dateStr === m.start_date ? '● ' : ''}{m.title}
                    </div>
                  ))}
                  {dayMilestones.length > 3 && (
                    <div className="text-[9px] text-[#555] pl-1">+{dayMilestones.length - 3} more</div>
                  )}
                </div>
              )}

              {/* PM hover indicator — show + on empty cells */}
              {isPM && cell.isCurrentMonth && dayMilestones.length === 0 && (
                <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                  <svg className="w-6 h-6 text-[#222]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                  </svg>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-5 pt-1 text-[11px] text-[#555]">
        <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Completed</div>
        <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blue-500" /> In Progress</div>
        <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> Pending</div>
        <div className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Start</div>
        <div className="flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-red-400" /> End</div>
        {isPM && <div className="flex items-center gap-1.5 text-[#333]">Click any date to add</div>}
      </div>

      {/* Detail Panel — when clicking a milestone on the calendar */}
      {selectedMilestone && !showAddForm && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => { setSelectedMilestone(null); setSelectedDate(null) }}>
          <div className="bg-[#0d0d0d] border border-[#1a1a1a] rounded-xl p-6 w-full max-w-md shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-5">
              <div>
                <p className="text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] mb-1">Milestone Detail</p>
                <h3 className="text-lg font-light text-[#f5f5f5]">{selectedMilestone.title}</h3>
              </div>
              <button onClick={() => { setSelectedMilestone(null); setSelectedDate(null) }} className="text-[#666] hover:text-[#f5f5f5] text-xl transition-colors">&times;</button>
            </div>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-2 border-b border-[#1a1a1a]">
                <span className="text-[#666]">Status</span>
                <span className={`text-[10px] px-2 py-0.5 rounded-lg border capitalize ${statusColor(selectedMilestone.status)}`}>{selectedMilestone.status}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-[#1a1a1a]">
                <span className="text-[#666]">Start Date</span>
                <span className="text-[#a3a3a3]">{new Date(selectedMilestone.start_date + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-[#1a1a1a]">
                <span className="text-[#666]">End Date</span>
                <span className="text-[#a3a3a3]">{new Date(selectedMilestone.end_date + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-[#1a1a1a]">
                <span className="text-[#666]">Duration</span>
                <span className="text-[#a3a3a3]">{selectedMilestone.duration_days} Day{selectedMilestone.duration_days !== 1 ? 's' : ''}</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-[#666]">Sequence</span>
                <span className="text-[#a3a3a3]">#{selectedMilestone.sequence_order}</span>
              </div>
            </div>
            {isPM && (
              <button
                onClick={() => { setShowAddForm(true); setSelectedMilestone(null) }}
                className="kp-btn-emerald w-full mt-5 py-2.5 text-sm"
              >
                + Add Another Item on This Date
              </button>
            )}
          </div>
        </div>
      )}

      {/* Add Schedule Item Modal */}
      {showAddForm && isPM && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => { setShowAddForm(false); setSelectedDate(null) }}>
          <div className="bg-[#0d0d0d] border border-[#1a1a1a] rounded-xl p-6 w-full max-w-md shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-5">
              <div>
                <p className="text-[10px] uppercase tracking-[0.2em] text-[#c5a55a] mb-1">New Schedule Item</p>
                <h3 className="text-lg font-light text-[#f5f5f5]">Add to Calendar</h3>
              </div>
              <button onClick={() => { setShowAddForm(false); setSelectedDate(null) }} className="text-[#666] hover:text-[#f5f5f5] text-xl transition-colors">&times;</button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Event Title</label>
                <input
                  type="text"
                  name="title"
                  required
                  placeholder="e.g. Framing Inspection, Plumbing Rough-In"
                  className="kp-input"
                  autoFocus
                />
              </div>
              <div>
                <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Start Date</label>
                <input
                  type="date"
                  name="startDate"
                  required
                  defaultValue={selectedDate || todayStr}
                  className="kp-input scheme-dark"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Duration (Days)</label>
                  <input type="number" name="durationDays" required min="1" defaultValue="1" className="kp-input" />
                </div>
                <div>
                  <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Sequence #</label>
                  <input type="number" name="sequenceOrder" required min="0" defaultValue={milestones.length + 1} className="kp-input" />
                </div>
              </div>
              <button type="submit" disabled={isPending} className="kp-btn-emerald w-full py-3 font-medium disabled:opacity-50 text-sm">
                {isPending ? 'Adding...' : '✓ Save to Calendar'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
