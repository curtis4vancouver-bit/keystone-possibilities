import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'
import AddMilestoneForm from './AddMilestoneForm'
import { ShiftMilestoneModal } from './ShiftMilestoneModal'
import { TradeDateProposalModal } from './TradeDateProposalModal'
import { ProposalApprovalCard } from './ProposalApprovalCard'
import { TradeChecklistModal } from './TradeChecklistModal'
import InteractiveCalendar from './InteractiveCalendar'

export default async function CalendarPage() {
  const supabase = await createClient()
  
  // Get user role
  const { data: { user } } = await supabase.auth.getUser()
  const { data: userData } = await supabase.from('users').select('role').eq('id', user?.id).single()
  const role = userData?.role || 'owner'

  // Get the active project from cookie (scoped correctly)
  const cookieStore = await cookies()
  const activeProjectCookie = cookieStore.get('active_project')?.value

  const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .order('created_at', { ascending: false })
    
  let project = null
  if (projects && projects.length > 0) {
    if (activeProjectCookie && activeProjectCookie !== '__new__') {
      project = projects.find(p => p.id === activeProjectCookie) || projects[0]
    } else {
      project = projects[0]
    }
  }

  if (!project) {
    return <div className="p-8 text-[#666]">No active project found. Create a project in the Overview first.</div>
  }

  // Fetch milestones for THIS project
  const { data: milestones } = await supabase
    .from('milestones')
    .select('*')
    .eq('project_id', project.id)
    .order('sequence_order', { ascending: true })

  // Fetch pending proposals (for PM only)
  let proposals: any[] = []
  if (role === 'pm') {
    const { data: rawProposals } = await supabase
      .from('date_proposals')
      .select('*, milestones(title, project_id), users:trade_id(email)')
      .eq('status', 'pending')
      .order('created_at', { ascending: false })

    // Flatten the joined data
    proposals = (rawProposals || [])
      .filter((p: any) => p.milestones?.project_id === project.id)
      .map((p: any) => ({
        ...p,
        milestone_title: p.milestones?.title,
        trade_email: p.users?.email,
      }))
  }

  // Get project start date (from project record or earliest milestone)
  const projectStartDate = project.created_at 
    ? new Date(project.created_at).toISOString().split('T')[0]
    : undefined

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <header className="flex flex-col sm:flex-row sm:justify-between sm:items-end gap-4 border-b border-[#1a1a1a] pb-6 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#c5a55a] font-medium mb-2">Scheduling</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-1">{project.title}</h2>
          <p className="text-[#a3a3a3] text-sm">Master Calendar — Click dates to add items. I can update this for you anytime.</p>
        </div>
        {role === 'pm' && (
          <div className="flex items-center gap-3">
            <TradeChecklistModal projectId={project.id} />
            <AddMilestoneForm projectId={project.id} />
          </div>
        )}
      </header>

      {/* PM: Pending Date Proposals */}
      {role === 'pm' && proposals.length > 0 && (
        <div className="space-y-3 kp-animate-in" style={{ animationDelay: '100ms' }}>
          <h3 className="text-sm font-medium text-[#c5a55a] flex items-center gap-2 tracking-widest uppercase text-[10px]">
            <span className="w-2 h-2 rounded-full bg-[#c5a55a] animate-pulse"></span>
            Pending Date Proposals ({proposals.length})
          </h3>
          {proposals.map((p: any) => (
            <ProposalApprovalCard key={p.id} proposal={p} />
          ))}
        </div>
      )}

      {/* ========== CALENDAR — ALWAYS VISIBLE ========== */}
      <div className="kp-animate-in" style={{ animationDelay: '150ms' }}>
        <InteractiveCalendar
          milestones={milestones || []}
          projectId={project.id}
          isPM={role === 'pm'}
          projectStartDate={projectStartDate}
        />
      </div>

      {/* ========== MILESTONE TABLE — Below Calendar ========== */}
      {milestones && milestones.length > 0 && (
        <>
          <div className="border-t border-[#1a1a1a] pt-6 kp-animate-in" style={{ animationDelay: '200ms' }}>
            <h3 className="text-sm font-medium tracking-[0.15em] uppercase text-[#a3a3a3] mb-4">Milestone Details</h3>
          </div>

          {/* Mobile: card layout */}
          <div className="block sm:hidden space-y-3">
            {milestones.map((m: any) => (
              <div key={m.id} className="kp-card p-4 space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-[10px] text-[#404040] font-mono mb-1">#{m.sequence_order}</p>
                    <p className="text-[#a3a3a3] font-medium text-sm">{m.title}</p>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded-lg border capitalize ${
                    m.status === 'completed' ? 'bg-[#10b981]/8 text-[#10b981] border-[#10b981]/15' :
                    m.status === 'in_progress' ? 'bg-[#3b82f6]/8 text-[#3b82f6] border-[#3b82f6]/15' :
                    'bg-[#111] text-[#666] border-[#1a1a1a]'
                  }`}>{m.status}</span>
                </div>
                <div className="flex justify-between text-xs text-[#666]">
                  <span>{new Date(m.start_date).toLocaleDateString()}</span>
                  <span>{m.duration_days} Day{m.duration_days !== 1 ? 's' : ''}</span>
                </div>
                <div className="pt-2 border-t border-[#1a1a1a]">
                  {role === 'pm' ? (
                    <ShiftMilestoneModal milestone={m} />
                  ) : role === 'trade' ? (
                    <TradeDateProposalModal milestone={m} />
                  ) : (
                    <span className="text-[#404040] text-xs">View Only</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Desktop: table layout */}
          <div className="hidden sm:block kp-card overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-[#0a0a0a] border-b border-[#1a1a1a] text-[#666]">
                <tr>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em]">Seq</th>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em]">Milestone</th>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em]">Start Date</th>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em]">End Date</th>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em]">Duration</th>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em]">Status</th>
                  <th className="px-6 py-4 font-medium uppercase text-[9px] tracking-[0.2em] text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1a1a1a]">
                {milestones.map((m: any) => (
                  <tr key={m.id} className="hover:bg-[#0a0a0a] transition-colors">
                    <td className="px-6 py-4 text-[#404040] font-mono text-xs">{m.sequence_order}</td>
                    <td className="px-6 py-4 text-[#a3a3a3]">{m.title}</td>
                    <td className="px-6 py-4 text-[#666]">
                      {new Date(m.start_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-[#666]">
                      {new Date(m.end_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-[#666]">
                      {m.duration_days} Day{m.duration_days !== 1 ? 's' : ''}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`text-[10px] px-2 py-1 rounded-lg border capitalize ${
                        m.status === 'completed' ? 'bg-[#10b981]/8 text-[#10b981] border-[#10b981]/15' :
                        m.status === 'in_progress' ? 'bg-[#3b82f6]/8 text-[#3b82f6] border-[#3b82f6]/15' :
                        'bg-[#111] text-[#666] border-[#1a1a1a]'
                      }`}>{m.status}</span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      {role === 'pm' ? (
                        <ShiftMilestoneModal milestone={m} />
                      ) : role === 'trade' ? (
                        <TradeDateProposalModal milestone={m} />
                      ) : (
                        <span className="text-[#404040] text-xs">View Only</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
