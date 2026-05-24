import { createClient } from '@/utils/supabase/server'
import { InviteForm } from './InviteForm'

export default async function InvitePage({
  searchParams,
}: {
  searchParams: Promise<{ project_id?: string; role?: string; category?: string }>
}) {
  const params = await searchParams
  const projectId = params.project_id
  const role = params.role || 'trade'
  const category = params.category || ''

  let projectTitle = 'a Keystone Project'

  if (projectId) {
    const supabase = await createClient()
    const { data: project } = await supabase
      .from('projects')
      .select('title')
      .eq('id', projectId)
      .single()
    if (project) {
      projectTitle = project.title
    }
  }

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-4">
      {/* Background texture */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#0a0a0a] via-black to-black pointer-events-none" />

      <div className="relative z-10 w-full max-w-md space-y-8">
        {/* Logo & Branding */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[#0a0a0a] border border-[#c5a55a]/20 mx-auto">
            <svg width="32" height="32" viewBox="0 0 56 56" fill="none">
              <path d="M28 4L8 18v20l20 14 20-14V18L28 4z" stroke="#c5a55a" strokeWidth="1.5" fill="none"/>
              <path d="M28 12L14 22v12l14 10 14-10V22L28 12z" stroke="#c5a55a" strokeWidth="1" fill="none"/>
              <path d="M28 20L20 26v6l8 6 8-6v-6L28 20z" fill="#c5a55a" opacity="0.3"/>
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-light text-[#f5f5f5] tracking-tight">
              You&apos;ve Been Invited
            </h1>
            <p className="text-[#666] text-sm mt-2">
              {role === 'owner' 
                ? `You've been invited as the property owner on` 
                : `You've been invited to join as a ${category || 'trade'} on`}
            </p>
            <p className="text-[#c5a55a] font-medium mt-1">{projectTitle}</p>
          </div>
        </div>

        {/* Signup Form */}
        <InviteForm 
          projectId={projectId || ''} 
          role={role} 
          category={category} 
        />

        {/* Footer */}
        <p className="text-center text-[10px] text-[#333] uppercase tracking-[0.25em]">
          Keystone Possibilities &bull; Command Center
        </p>
      </div>
    </div>
  )
}
