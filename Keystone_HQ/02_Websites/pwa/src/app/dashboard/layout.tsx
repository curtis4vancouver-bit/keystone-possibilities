import { createClient } from '@/utils/supabase/server';
import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import { logout } from '@/app/login/actions';
import { SidebarNav } from './SidebarNav';
import { ProjectSwitcher } from './ProjectSwitcher';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = await createClient();
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (!user || authError) {
    redirect('/login');
  }

  // Fetch the user's profile from public.users
  const { data: profile } = await supabase
    .from('users')
    .select('full_name, role, is_approved')
    .eq('id', user.id)
    .single();

  // Auto-fix: Admin emails always get PM access (no payment needed)
  const ADMIN_EMAILS = ['curtis4vancouver@gmail.com'];
  if (user.email && ADMIN_EMAILS.includes(user.email)) {
    if (!profile) {
      // Profile missing — create it
      await supabase.from('users').upsert({
        id: user.id,
        email: user.email,
        full_name: user.user_metadata?.full_name || 'Curtis',
        role: 'pm',
        is_approved: true,
      });
    } else if (!profile.is_approved || profile.role !== 'pm') {
      // Profile exists but wrong state — fix it
      await supabase.from('users').update({ role: 'pm', is_approved: true }).eq('id', user.id);
    }
  }

  // Re-fetch if we just fixed it
  const { data: finalProfile } = (profile && profile.is_approved && user.email && ADMIN_EMAILS.includes(user.email))
    ? { data: { ...profile, role: 'pm' as const, is_approved: true, full_name: profile.full_name } }
    : (!profile && user.email && ADMIN_EMAILS.includes(user.email))
      ? await supabase.from('users').select('full_name, role, is_approved').eq('id', user.id).single()
      : { data: profile };

  if (finalProfile && !finalProfile.is_approved) {
    redirect('/pending');
  }

  const fullName = finalProfile?.full_name || 'User';
  const role = finalProfile?.role || 'trade';
  const initials = fullName.split(' ').map((n: string) => n[0]).join('').substring(0, 2).toUpperCase();
  const isPrivileged = role === 'owner' || role === 'pm';

  // Fetch all projects for this user
  const { data: projects } = await supabase
    .from('projects')
    .select('id, title, address, status')
    .order('created_at', { ascending: false });

  // Get active project from cookie
  const cookieStore = await cookies();
  const activeProjectCookie = cookieStore.get('active_project')?.value;
  
  // Determine active project ID
  let activeProjectId: string | null = null;
  if (activeProjectCookie && activeProjectCookie !== '__new__' && projects?.some(p => p.id === activeProjectCookie)) {
    activeProjectId = activeProjectCookie;
  } else if (projects && projects.length > 0 && activeProjectCookie !== '__new__') {
    activeProjectId = projects[0].id;
  }

  return (
    <div className="min-h-screen bg-black text-[#f5f5f5] flex flex-col md:flex-row">
      {/* ═══ Sidebar ═══ */}
      <aside className="w-full md:w-72 bg-black border-b md:border-b-0 md:border-r border-[#1a1a1a] flex flex-col shrink-0 relative">
        {/* Subtle side glow */}
        <div className="absolute top-0 right-0 w-px h-full bg-linear-to-b from-transparent via-[#c5a55a]/10 to-transparent hidden md:block" />
        
        {/* Brand Header */}
        <div className="p-6 border-b border-[#1a1a1a]">
          <div className="flex items-center gap-3">
            {/* Transparent SVG Logo Mark */}
            <svg width="32" height="32" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg" className="shrink-0">
              <path d="M28 4L8 18v20l20 14 20-14V18L28 4z" stroke="#c5a55a" strokeWidth="1.5" fill="none" opacity="0.8"/>
              <path d="M28 12L14 22v12l14 10 14-10V22L28 12z" stroke="#c5a55a" strokeWidth="1" fill="none" opacity="0.4"/>
              <path d="M28 20L20 26v6l8 6 8-6v-6L28 20z" fill="#c5a55a" opacity="0.2"/>
            </svg>
            <div>
              <h1 className="text-sm font-light tracking-[0.2em] uppercase text-white">Keystone</h1>
              <p className="text-[9px] tracking-[0.3em] text-[#c5a55a] uppercase font-medium">Command Center</p>
            </div>
          </div>
        </div>
        
        {/* Project Switcher — only for PM/Owner with projects */}
        {isPrivileged && projects && projects.length > 0 && (
          <ProjectSwitcher 
            projects={projects} 
            activeProjectId={activeProjectId} 
          />
        )}
        
        <SidebarNav role={role} />
        
        {/* User Profile Footer */}
        <div className="p-4 border-t border-[#1a1a1a] mt-auto">
          <div className="flex items-center gap-3 px-3 py-2">
            <div className="w-9 h-9 rounded-lg bg-linear-to-br from-[#c5a55a]/20 to-[#c5a55a]/5 flex items-center justify-center text-xs font-semibold text-[#c5a55a] border border-[#c5a55a]/15">
              {initials}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-[#a3a3a3] truncate">{fullName}</p>
              <p className="text-[9px] text-[#c5a55a]/60 tracking-wider uppercase">{role.replace('_', ' ')}</p>
            </div>
            <form action={logout}>
              <button 
                title="Sign Out" 
                className="p-2 text-[#404040] hover:text-red-400 hover:bg-[#111] rounded-lg transition-all duration-200"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
              </button>
            </form>
          </div>
        </div>
      </aside>

      {/* ═══ Main Content ═══ */}
      <main className="flex-1 overflow-y-auto bg-black">
        {children}
      </main>
    </div>
  );
}
