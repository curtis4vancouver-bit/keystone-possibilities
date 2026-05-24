import { createClient } from '@/utils/supabase/server';
import { cookies } from 'next/headers';
import Link from 'next/link';
import { CreateProjectForm } from './CreateProjectForm';
import { AssignTradeForm } from './AssignTradeForm';
import AssignOwnerForm from './AssignOwnerForm';
import { forceRefreshRole, fixProfile } from './actions';
import { redirect } from 'next/navigation';
import LandscaperDashboard from './LandscaperDashboard';
import ExcavatorDashboard from './ExcavatorDashboard';

export default async function DashboardPage() {
  const supabase = await createClient();
  
  // Get the current user to check their role
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return null;

  // Get user profile to check role explicitly
  const { data: profile } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single();

  const isPrivileged = profile?.role === 'owner' || profile?.role === 'pm';

  // Fetch all projects
  const { data: projects, error } = await supabase
    .from('projects')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Error fetching projects:', error);
  }

  // Determine active project from cookie
  const cookieStore = await cookies();
  const activeProjectCookie = cookieStore.get('active_project')?.value;
  
  // Check if user wants to create new project
  const showCreateForm = activeProjectCookie === '__new__';
  
  let project = null;
  if (!showCreateForm && projects && projects.length > 0) {
    if (activeProjectCookie && activeProjectCookie !== '__new__') {
      project = projects.find(p => p.id === activeProjectCookie) || projects[0];
    } else {
      project = projects[0];
    }
  }

  // Fetch active user's trade assignment if they are a trade user
  let activeTradeCategory: string | null = null;
  if (!isPrivileged && project && user) {
    const { data: tradeAssignment } = await supabase
      .from('project_trades')
      .select('trade_category')
      .eq('project_id', project.id)
      .eq('user_id', user.id)
      .maybeSingle();
    
    activeTradeCategory = tradeAssignment?.trade_category || null;
  }

  // Show create form if no projects exist or user clicked "New Project"
  if (!project || showCreateForm) {
    if (isPrivileged) {
      return (
        <div className="p-8 max-w-6xl mx-auto min-h-[60vh]">
          {/* Show existing projects count if any */}
          {projects && projects.length > 0 && (
            <div className="mb-6 flex items-center gap-3">
              <button 
                onClick={undefined}
                className="text-sm text-[#a3a3a3] hover:text-[#f5f5f5] transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" />
                </svg>
                You have {projects.length} existing project{projects.length > 1 ? 's' : ''} — use the sidebar switcher to go back
              </button>
            </div>
          )}
          <CreateProjectForm />
        </div>
      );
    } else {
      return (
        <div className="p-8 max-w-6xl mx-auto flex flex-col items-center justify-center min-h-[60vh] text-center">
          <div className="w-16 h-16 rounded-xl bg-[#111] border border-[#1a1a1a] flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-[#404040]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          </div>
          <h2 className="text-2xl font-light text-[#f5f5f5] mb-2">No Active Assignments</h2>
          <p className="text-[#666] max-w-md text-sm">
            You are approved for the platform, but you have not been assigned to any project workspaces yet. Please wait for the Project Manager to link your account.
          </p>
          <div className="mt-8 kp-card p-4 text-left font-mono text-sm max-w-md w-full">
            <p className="font-bold mb-2 text-[#a3a3a3] text-xs uppercase tracking-wider">Diagnostic Info</p>
            <div className="kp-keyline my-3" />
            <p className="text-[#666] text-xs">Database Role: <strong className="text-[#c5a55a]">{profile?.role || 'null/undefined'}</strong></p>
            <p className="text-[#666] text-xs mt-1">User ID: <span className="text-[#404040]">{user.id}</span></p>
            
            {(!profile || profile?.role === 'trade') && (
              <form action={async () => {
                'use server'
                const { fixProfile } = await import('./actions');
                await fixProfile();
                const { redirect } = await import('next/navigation');
                redirect('/dashboard');
              }} className="mt-4 pt-4 border-t border-[#1a1a1a]">
                <p className="text-xs text-[#f59e0b] mb-2">
                  {!profile 
                    ? "Your profile is missing from the database. Click here to auto-fix and claim the Owner role:"
                    : "If you just ran Admin Setup, click here to force-refresh the dashboard cache:"}
                </p>
                <button type="submit" className="kp-btn-emerald w-full py-3 text-center">
                  {!profile ? "Fix Profile & Claim Owner" : "Force Refresh Dashboard"}
                </button>
              </form>
            )}
          </div>
        </div>
      );
    }
  }

  // Count projects for multi-project indicator
  const projectCount = projects?.length || 0;

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex justify-between items-end border-b border-[#1a1a1a] pb-6 kp-animate-in">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <p className="text-[10px] uppercase tracking-[0.25em] text-[#666] font-medium">Command Center</p>
            {projectCount > 1 && (
              <span className="text-[9px] bg-[#111] text-[#c5a55a]/60 px-2 py-0.5 rounded-full border border-[#c5a55a]/10">
                {projectCount} projects
              </span>
            )}
          </div>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">{project.title}</h2>
          <p className="text-[#a3a3a3] text-sm">{project.address}</p>
        </div>
        <div className="text-right">
          <p className="text-[9px] tracking-[0.25em] uppercase text-[#666] mb-1">Status</p>
          <div className="kp-status-active inline-flex items-center px-3 py-1.5 rounded-lg text-xs capitalize tracking-wider">
            <span className="w-1.5 h-1.5 rounded-full bg-[#10b981] mr-2 animate-pulse"></span>
            {project.status.replace('_', ' ')}
          </div>
        </div>
      </header>

      {/* Financial Hub — Privileged View */}
      {isPrivileged ? (
        <div className="kp-card-gold p-6 relative overflow-hidden kp-animate-in" style={{ animationDelay: '100ms' }}>
          {/* Decorative keystone mark */}
          <div className="absolute top-4 right-4 opacity-[0.03]">
            <svg width="80" height="80" viewBox="0 0 56 56" fill="none">
              <path d="M28 4L8 18v20l20 14 20-14V18L28 4z" stroke="#c5a55a" strokeWidth="1.5" fill="none"/>
              <path d="M28 12L14 22v12l14 10 14-10V22L28 12z" stroke="#c5a55a" strokeWidth="1" fill="none"/>
              <path d="M28 20L20 26v6l8 6 8-6v-6L28 20z" fill="#c5a55a" opacity="0.3"/>
            </svg>
          </div>
          <h3 className="text-lg font-light text-[#c5a55a] mb-6 flex items-center gap-3">
            <svg className="w-5 h-5 text-[#c5a55a]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span className="tracking-widest uppercase text-xs">Keystone Financial Hub</span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="space-y-1">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] font-medium">Total Authorized Capital</p>
              <p className="text-3xl font-light text-[#f5f5f5]">{project.total_budget ? `$${project.total_budget.toLocaleString()}` : 'TBD'}</p>
            </div>
            <div className="space-y-1">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] font-medium">PM Fee ({project.pm_fee_percentage}%)</p>
              <p className="text-3xl font-light text-[#c5a55a]">
                {project.total_budget ? `$${(project.total_budget * (project.pm_fee_percentage / 100)).toLocaleString()}` : 'TBD'}
              </p>
            </div>
            <div className="space-y-1">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] font-medium">Invoices Pending</p>
              <p className="text-3xl font-light text-[#f59e0b]">0</p>
              <button className="text-[10px] text-[#c5a55a]/60 mt-1 hover:text-[#c5a55a] transition-colors tracking-wider uppercase">View Ledger →</button>
            </div>
            <div className="bg-black/30 p-4 rounded-lg border border-[#1a1a1a]">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] font-medium mb-2">Owner-PM Contract</p>
              <div className="flex items-center text-[#f59e0b] text-xs font-medium mb-3">
                <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                Signature Needed
              </div>
              <Link href="/dashboard/documents" className="kp-btn-gold w-full block text-center text-[10px] py-2">
                Upload & Send →
              </Link>
            </div>
          </div>
        </div>
      ) : activeTradeCategory?.toLowerCase().includes('landscap') ? (
        <LandscaperDashboard projectId={project.id} projectName={project.title} />
      ) : activeTradeCategory?.toLowerCase().includes('excavat') || activeTradeCategory?.toLowerCase().includes('demolition') || activeTradeCategory?.toLowerCase().includes('geotech') ? (
        <ExcavatorDashboard projectId={project.id} projectName={project.title} />
      ) : (
        <div className="kp-card p-6 kp-animate-in" style={{ animationDelay: '100ms' }}>
          <h3 className="text-xs font-light text-[#f5f5f5] mb-6 flex items-center gap-3 tracking-widest uppercase">
            <svg className="w-5 h-5 text-[#3b82f6]/60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            Trade Contract & Compliance
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-black rounded-lg border border-[#1a1a1a]">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-2">Locked Bid Amount</p>
              <p className="text-xl font-medium text-[#f5f5f5]">Pending Upload</p>
            </div>
            <div className="p-4 bg-black rounded-lg border border-[#1a1a1a]">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-2">WCB Status</p>
              <div className="flex items-center text-[#f59e0b] text-sm font-medium">
                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                Upload Required
              </div>
            </div>
            <div className="p-4 bg-black rounded-lg border border-[#1a1a1a]">
              <p className="text-[9px] uppercase tracking-[0.2em] text-[#666] mb-2">Subcontractor Agreement</p>
              <button className="kp-btn-gold w-full text-center text-[10px] py-2">
                Review & Sign
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-4">
        
        {/* Calendar / Timeline */}
        <div className="lg:col-span-2 space-y-6 kp-animate-in" style={{ animationDelay: '200ms' }}>
          <div className="flex justify-between items-center border-b border-[#1a1a1a] pb-4">
             <h3 className="text-sm font-medium tracking-[0.15em] uppercase text-[#a3a3a3]">Master Calendar</h3>
             <Link href="/dashboard/calendar" className="kp-btn-gold text-[10px] py-2 px-4 flex items-center gap-1.5">
               Open Calendar →
             </Link>
          </div>
          
          {/* Calendar Quick View */}
          <Link href="/dashboard/calendar" className="block kp-card-gold p-6 group">
            <div className="flex items-center justify-between mb-4">
              <p className="text-[#a3a3a3] font-medium group-hover:text-[#f5f5f5] transition-colors text-sm">
                📅 {new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
              </p>
              <svg className="w-5 h-5 text-[#404040] group-hover:text-[#c5a55a] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </div>
            <p className="text-[#666] text-xs leading-relaxed">Click to open the interactive calendar — add milestones, shift dates, and manage the project timeline.</p>
          </Link>
        </div>

        {/* Sidebar Widgets */}
        <div className="space-y-6 kp-animate-in" style={{ animationDelay: '300ms' }}>
          {/* Project Team */}
          <div className="kp-card p-6">
             <div className="flex justify-between items-start mb-4">
               <h3 className="text-sm font-medium tracking-[0.15em] uppercase text-[#a3a3a3]">Project Team</h3>
               {isPrivileged && <AssignOwnerForm projectId={project.id} currentOwnerId={project.owner_id} />}
             </div>
             <ul className="space-y-4">
                {project.pm_id ? (
                  <li className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-linear-to-br from-[#c5a55a]/15 to-[#c5a55a]/5 flex items-center justify-center text-[10px] font-bold text-[#c5a55a] border border-[#c5a55a]/15">PM</div>
                    <div>
                      <p className="text-sm text-[#a3a3a3]">Assigned PM</p>
                      <p className="text-[9px] text-[#666] uppercase tracking-wider">Project Manager</p>
                    </div>
                  </li>
                ) : null}
                {project.owner_id ? (
                  <li className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-linear-to-br from-[#10b981]/15 to-[#10b981]/5 flex items-center justify-center text-[10px] font-bold text-[#10b981] border border-[#10b981]/15">OW</div>
                    <div>
                      <p className="text-sm text-[#a3a3a3]">Property Owner</p>
                      <p className="text-[9px] text-[#666] uppercase tracking-wider">Client</p>
                    </div>
                  </li>
                ) : null}
             </ul>
             {!project.pm_id && !project.owner_id && (
               <p className="text-xs text-[#666]">Team members will be assigned during planning phase.</p>
             )}
             <button className="w-full mt-6 py-2.5 bg-[#111] hover:bg-[#1a1a1a] border border-[#1a1a1a] hover:border-[#c5a55a]/20 transition-all duration-200 text-xs rounded-lg text-[#a3a3a3] hover:text-[#c5a55a] uppercase tracking-wider">
               Message Team
             </button>
          </div>

          {/* Trade Assignment Widget for Privileged users */}
          {isPrivileged && (
            <div className="kp-card p-6">
               <h3 className="text-sm font-medium tracking-[0.15em] uppercase text-[#a3a3a3] mb-2">Assign Trades</h3>
               <p className="text-[10px] text-[#666] mb-4 leading-relaxed">Invite registered subcontractors to this workspace to unlock their portals.</p>
               <AssignTradeForm projectId={project.id} />
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
