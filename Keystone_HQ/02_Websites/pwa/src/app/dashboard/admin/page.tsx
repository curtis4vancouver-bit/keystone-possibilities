import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { ApproveUserButton } from './ApproveUserButton'
import { ResetProjectButton } from './ResetProjectButton'
import { PrintReport } from './PrintReport'
import { CreateAccountForm } from './CreateAccountForm'

export default async function AdminPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const { data: profile } = await supabase.from('users').select('role').eq('id', user.id).single()

  if (profile?.role !== 'pm') {
    return (
      <div className="p-8 text-center">
        <h2 className="text-xl text-[#ef4444]">Access Denied</h2>
        <p className="text-[#666] mt-2">Only Project Managers can access the admin panel.</p>
      </div>
    )
  }

  const cookieStore = await cookies()
  const activeProjectCookie = cookieStore.get('active_project')?.value
  const { data: projects } = await supabase.from('projects').select('*').order('created_at', { ascending: false })

  let activeProject = null
  if (projects && projects.length > 0) {
    if (activeProjectCookie && activeProjectCookie !== '__new__') {
      activeProject = projects.find(p => p.id === activeProjectCookie) || projects[0]
    } else {
      activeProject = projects[0]
    }
  }

  let milestones: any[] = [], documents: any[] = [], trades: any[] = []
  if (activeProject) {
    const [msRes, docRes, tradeRes] = await Promise.all([
      supabase.from('milestones').select('*').eq('project_id', activeProject.id).order('sequence_order', { ascending: true }),
      supabase.from('documents').select('*').eq('project_id', activeProject.id).order('created_at', { ascending: false }),
      supabase.from('project_trades').select('*').eq('project_id', activeProject.id).order('created_at', { ascending: false }),
    ])
    milestones = msRes.data || []; documents = docRes.data || []; trades = tradeRes.data || []
  }

  const { data: allUsers } = await supabase.from('users').select('id, email, full_name, role, is_approved, created_at').order('created_at', { ascending: false })
  const pendingUsers = (allUsers || []).filter(u => !u.is_approved)
  const approvedUsers = (allUsers || []).filter(u => u.is_approved)

  return (
    <div className="p-4 sm:p-8 max-w-5xl mx-auto space-y-8">
      <header className="flex flex-col sm:flex-row sm:justify-between sm:items-end gap-4 border-b border-[#1a1a1a] pb-6 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#f59e0b] font-medium mb-2">Administration</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">Admin Panel</h2>
          <p className="text-[#a3a3a3] text-sm">User management, project tools, and report generation.</p>
        </div>
        <CreateAccountForm />
      </header>

      {/* Pending Approvals */}
      <div className="space-y-4">
        <h3 className="text-[10px] font-medium text-[#f59e0b] flex items-center gap-2 tracking-[0.15em] uppercase">
          <span className="w-2 h-2 rounded-full bg-[#f59e0b] animate-pulse"></span>
          Pending Approval ({pendingUsers.length})
        </h3>
        {pendingUsers.length === 0 ? (
          <div className="kp-card p-8 text-center"><p className="text-[#666] text-sm">No users waiting for approval.</p></div>
        ) : (
          <div className="space-y-3">
            {pendingUsers.map(u => (
              <div key={u.id} className="kp-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <p className="text-[#f5f5f5] font-medium text-sm">{u.full_name || u.email}</p>
                  <p className="text-[10px] text-[#666]">{u.email} &bull; Role: <span className="text-[#a3a3a3]">{u.role || 'pending'}</span></p>
                </div>
                <ApproveUserButton userId={u.id} userName={u.full_name || u.email} />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Active Users */}
      <div className="space-y-4">
        <h3 className="text-[10px] font-medium text-[#10b981] flex items-center gap-2 tracking-[0.15em] uppercase">
          <span className="w-2 h-2 rounded-full bg-[#10b981]"></span>
          Active Users ({approvedUsers.length})
        </h3>
        <div className="kp-card overflow-hidden">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#0a0a0a] border-b border-[#1a1a1a] text-[#666]">
              <tr>
                <th className="px-4 py-3 font-medium uppercase text-[9px] tracking-[0.2em]">Name</th>
                <th className="px-4 py-3 font-medium uppercase text-[9px] tracking-[0.2em]">Email</th>
                <th className="px-4 py-3 font-medium uppercase text-[9px] tracking-[0.2em]">Role</th>
                <th className="px-4 py-3 font-medium uppercase text-[9px] tracking-[0.2em]">Since</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1a1a1a]">
              {approvedUsers.map(u => (
                <tr key={u.id} className="hover:bg-[#0a0a0a] transition-colors">
                  <td className="px-4 py-3 text-[#a3a3a3]">{u.full_name || '—'}</td>
                  <td className="px-4 py-3 text-[#666]">{u.email}</td>
                  <td className="px-4 py-3">
                    <span className={`text-[10px] px-2 py-1 rounded-lg border capitalize ${
                      u.role === 'pm' ? 'bg-[#c5a55a]/8 text-[#c5a55a] border-[#c5a55a]/15' :
                      u.role === 'owner' ? 'bg-[#10b981]/8 text-[#10b981] border-[#10b981]/15' :
                      'bg-[#f59e0b]/8 text-[#f59e0b] border-[#f59e0b]/15'
                    }`}>{u.role}</span>
                  </td>
                  <td className="px-4 py-3 text-[#404040] text-xs">{new Date(u.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Project Tools */}
      {activeProject && (
        <div className="space-y-4 border-t border-[#1a1a1a] pt-8">
          <h3 className="text-[10px] font-medium text-[#a3a3a3] flex items-center gap-2 tracking-[0.15em] uppercase">
            Project Tools — {activeProject.title}
          </h3>
          <div className="kp-card-gold p-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
              <div className="bg-black rounded-lg p-4 border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase tracking-[0.2em] mb-1">Milestones</p>
                <p className="text-2xl font-light text-[#f5f5f5]">{milestones.length}</p>
              </div>
              <div className="bg-black rounded-lg p-4 border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase tracking-[0.2em] mb-1">Documents</p>
                <p className="text-2xl font-light text-[#f5f5f5]">{documents.length}</p>
              </div>
              <div className="bg-black rounded-lg p-4 border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase tracking-[0.2em] mb-1">Trades</p>
                <p className="text-2xl font-light text-[#f5f5f5]">{trades.length}</p>
              </div>
            </div>
            <PrintReport project={activeProject} milestones={milestones} documents={documents} trades={trades} />
            <details className="group">
              <summary className="cursor-pointer text-[10px] text-[#404040] hover:text-[#ef4444] transition-colors flex items-center gap-2 py-2 select-none uppercase tracking-wider">
                <svg className="w-3 h-3 transition-transform group-open:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" /></svg>
                Danger Zone
              </summary>
              <div className="mt-3 pt-3 border-t border-[#ef4444]/10">
                <ResetProjectButton projectId={activeProject.id} projectTitle={activeProject.title} />
              </div>
            </details>
          </div>
        </div>
      )}
    </div>
  )
}
