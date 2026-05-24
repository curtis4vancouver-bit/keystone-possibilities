import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'
import { InvoiceModal } from './InvoiceModal'
import { ChangeOrderModal } from './ChangeOrderModal'
import { LedgerTable } from './LedgerTable'

export default async function FinancialsPage() {
  const supabase = await createClient()
  const cookieStore = await cookies()
  const activeProjectCookie = cookieStore.get('active_project')?.value

  // 1. Get user profile and roles
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return (
      <div className="p-8 text-center text-[#666]">
        Please log in to view the Financial Hub.
      </div>
    )
  }

  const { data: profile } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()
  
  const isPM = profile?.role === 'pm' || profile?.role === 'owner'

  // 2. Fetch projects and active project context
  const { data: projects } = await supabase
    .from('projects')
    .select('id, title, total_budget')
  
  let activeProject = projects?.[0]
  if (activeProjectCookie && activeProjectCookie !== '__new__') {
    const found = projects?.find(p => p.id === activeProjectCookie)
    if (found) activeProject = found
  }

  const projectId = activeProject?.id

  // 3. Fetch financial ledger data
  const { data: ledger } = projectId 
    ? await supabase
        .from('financial_ledger')
        .select(`
          id,
          project_id,
          trade_id,
          requested_by,
          type,
          amount,
          description,
          status,
          created_at,
          users:users!financial_ledger_requested_by_fkey (
            full_name
          ),
          project_trades (
            trade_category
          )
        `)
        .eq('project_id', projectId)
        .order('created_at', { ascending: false })
    : { data: [] }

  // 4. Budget calculations
  const totalBudget = activeProject?.total_budget ? Number(activeProject.total_budget) : 0
  
  const approvedTotal = ledger
    ? ledger
        .filter((item: any) => (item.type === 'invoice' || item.type === 'payment') && (item.status === 'approved' || item.status === 'paid'))
        .reduce((sum: number, item: any) => sum + Number(item.amount), 0)
    : 0

  const pendingTotal = ledger
    ? ledger
        .filter((item: any) => item.status === 'pending')
        .reduce((sum: number, item: any) => sum + Number(item.amount), 0)
    : 0

  const remainingBudget = Math.max(0, totalBudget - approvedTotal)

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex flex-col sm:flex-row sm:justify-between sm:items-end border-b border-[#1a1a1a] pb-6 gap-4 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#10b981] font-semibold mb-2">Accounting</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">
            {activeProject ? `${activeProject.title} Ledger` : 'Financial Hub'}
          </h2>
          <p className="text-[#a3a3a3] text-sm font-light">Track invoices, change orders, and active project budget deployment.</p>
        </div>
        
        {projectId && (
          <div className="flex gap-3">
            {!isPM && (
              <>
                <InvoiceModal projectId={projectId} />
                <ChangeOrderModal projectId={projectId} />
              </>
            )}
          </div>
        )}
      </header>

      {projectId ? (
        <>
          {/* Stats Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 kp-animate-in" style={{ animationDelay: '100ms' }}>
            <div className="kp-card-gold p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity">
                <svg className="w-12 h-12 text-[#c5a55a]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
              </div>
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-1 font-semibold">Total Budget</p>
              <p className="text-2xl font-light text-[#f5f5f5] font-mono">
                {totalBudget > 0 ? `$${totalBudget.toLocaleString(undefined, {minimumFractionDigits: 2})}` : 'TBD'}
              </p>
            </div>
            
            <div className="kp-card p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-3 opacity-5">
                <svg className="w-12 h-12 text-[#10b981]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-1 font-semibold">Approved to Date</p>
              <p className="text-2xl font-light text-[#10b981] font-mono">
                ${approvedTotal.toLocaleString(undefined, {minimumFractionDigits: 2})}
              </p>
            </div>
            
            <div className="kp-card p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-3 opacity-5">
                <svg className="w-12 h-12 text-[#f59e0b]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-1 font-semibold">Pending Approval</p>
              <p className="text-2xl font-light text-[#f59e0b] font-mono">
                ${pendingTotal.toLocaleString(undefined, {minimumFractionDigits: 2})}
              </p>
            </div>
            
            <div className="kp-card p-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-3 opacity-5">
                <svg className="w-12 h-12 text-[#a3a3a3]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              </div>
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-1 font-semibold">Remaining Budget</p>
              <p className="text-2xl font-light text-[#a3a3a3] font-mono">
                {totalBudget > 0 ? `$${remainingBudget.toLocaleString(undefined, {minimumFractionDigits: 2})}` : 'TBD'}
              </p>
            </div>
          </div>

          {/* Ledger Table */}
          <div className="space-y-4 kp-animate-in" style={{ animationDelay: '200ms' }}>
            <h3 className="text-sm font-semibold tracking-[0.15em] uppercase text-[#a3a3a3] pt-4">Ledger Activity</h3>
            {ledger && ledger.length > 0 ? (
              <LedgerTable ledger={ledger} isPM={isPM} projectId={projectId} />
            ) : (
              <div className="kp-card p-12 text-center bg-[#020202]">
                <div className="w-16 h-16 rounded-xl bg-[#0a0a0a] border border-[#1a1a1a] flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-[#404040]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-[#a3a3a3] mb-2">No Ledger Activity</h3>
                <p className="text-[#666] text-sm max-w-sm mx-auto">
                  {isPM 
                    ? 'No invoices or change orders have been submitted for this project yet.' 
                    : 'Submit an invoice or request a change order above to start tracking financials.'}
                </p>
              </div>
            )}
          </div>
        </>
      ) : (
        <div className="kp-card p-12 text-center bg-[#020202]">
          <h3 className="text-lg font-medium text-[#a3a3a3] mb-2">No Active Project Selected</h3>
          <p className="text-[#666] text-sm">Please select or create a project in the sidebar to view financials.</p>
        </div>
      )}
    </div>
  )
}
