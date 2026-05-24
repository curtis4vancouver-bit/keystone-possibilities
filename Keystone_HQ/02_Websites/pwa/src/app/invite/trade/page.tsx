import { createClient } from '@/utils/supabase/server'
import { acceptTradeInvite } from './actions'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function TradeInvitePage({ searchParams }: { searchParams: Promise<{ project_id?: string, category?: string }> }) {
  const params = await searchParams
  const projectId = params.project_id
  const category = params.category

  if (!projectId || !category) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="kp-card-gold p-8 max-w-md w-full text-center space-y-4">
          <h1 className="text-xl font-medium text-[#f5f5f5]">Invalid Invitation</h1>
          <p className="text-[#a3a3a3]">This link is missing required parameters. Please ask your Project Manager for a new link.</p>
        </div>
      </div>
    )
  }

  const supabase = await createClient()
  
  // 1. Verify Project
  const { data: project } = await supabase
    .from('projects')
    .select('title')
    .eq('id', projectId)
    .single()

  if (!project) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4">
        <div className="kp-card-gold p-8 max-w-md w-full text-center space-y-4">
          <h1 className="text-xl font-medium text-[#f5f5f5]">Project Not Found</h1>
          <p className="text-[#a3a3a3]">The project for this invitation could not be found.</p>
        </div>
      </div>
    )
  }

  // 2. Check Auth Status
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-amber-900/20 via-black to-black"></div>
      
      <div className="kp-card-gold p-8 max-w-md w-full relative z-10 shadow-2xl">
        <div className="mb-8">
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#c5a55a] font-medium mb-2">Trade Partner Invitation</p>
          <h1 className="text-3xl font-light text-[#f5f5f5] mb-2">Join {project.title}</h1>
          <p className="text-[#a3a3a3] text-sm">
            You have been invited as the <strong className="text-[#10b981] font-medium">{category}</strong> partner for this project.
          </p>
        </div>

        {!user ? (
          <div className="space-y-4">
            <div className="bg-[#c5a55a]/5 border border-[#c5a55a]/20 p-4 rounded-lg">
              <p className="text-sm text-[#c5a55a]">You must sign in or create an account to accept this invitation and access your schedule.</p>
            </div>
            <Link 
              href={`/login?redirect=${encodeURIComponent(`/invite/trade?project_id=${projectId}&category=${category}`)}`}
              className="block w-full py-3 text-center bg-white text-black font-medium rounded-lg hover:bg-[#e5e5e5] transition-colors"
            >
              Log In / Sign Up
            </Link>
          </div>
        ) : (
          <form action={async () => {
            'use server'
            const result = await acceptTradeInvite(projectId, category)
            if (result.success) {
              redirect('/dashboard')
            } else {
              // Note: using redirect to show error is tricky, but in a real app we'd use a client component form here.
              // For simplicity of this MVP, we'll let it error out or redirect to dashboard.
              redirect('/dashboard?error=' + encodeURIComponent(result.error || 'Unknown error'))
            }
          }}>
            <button 
              type="submit" 
              className="kp-btn-emerald w-full py-3 font-medium"
            >
              Accept Invitation
            </button>
            <p className="text-center text-[10px] text-[#666] mt-4">
              Signed in as {user.email}
            </p>
          </form>
        )}
      </div>
    </div>
  )
}
