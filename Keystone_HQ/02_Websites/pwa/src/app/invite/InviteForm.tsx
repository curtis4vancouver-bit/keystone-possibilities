'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/utils/supabase/client'

export function InviteForm({ 
  projectId, 
  role, 
  category 
}: { 
  projectId: string
  role: string
  category: string 
}) {
  const [isPending, setIsPending] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsPending(true)
    setError('')

    const formData = new FormData(e.currentTarget)
    const full_name = formData.get('full_name') as string
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    const supabase = createClient()

    // Sign up
    const { data, error: signupError } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { full_name }
      }
    })

    if (signupError) {
      setError(signupError.message)
      setIsPending(false)
      return
    }

    if (!data.user) {
      setError('Failed to create account. Please try again.')
      setIsPending(false)
      return
    }

    // If project ID provided, link to project via API
    if (projectId) {
      try {
        const res = await fetch('/api/invite/accept', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId: data.user.id,
            projectId,
            role,
            category,
          })
        })
        if (!res.ok) {
          console.error('Failed to link to project')
        }
      } catch {
        console.error('Failed to link to project')
      }
    }

    setSuccess(true)
    setIsPending(false)

    // Redirect to dashboard after a short delay
    setTimeout(() => {
      router.push('/dashboard')
    }, 2000)
  }

  if (success) {
    return (
      <div className="rounded-xl border border-[#10b981]/20 bg-[#0a0a0a] p-8 text-center space-y-4">
        <div className="w-14 h-14 rounded-full bg-[#10b981]/10 flex items-center justify-center mx-auto">
          <svg className="w-7 h-7 text-[#10b981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-xl font-light text-[#f5f5f5]">Account Created</h2>
        <p className="text-[#666] text-sm">
          Your account is set up. The Project Manager will review and approve your access shortly.
        </p>
        <p className="text-[#c5a55a] text-xs animate-pulse">Redirecting to dashboard...</p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-xl border border-[#1a1a1a] bg-[#0a0a0a] p-6 space-y-5">
      {error && (
        <div className="bg-[#ef4444]/10 border border-[#ef4444]/20 rounded-lg p-3">
          <p className="text-[#ef4444] text-sm">{error}</p>
        </div>
      )}

      <div>
        <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em] font-medium">
          Full Name
        </label>
        <input
          type="text"
          name="full_name"
          required
          placeholder="Your full name"
          className="w-full px-4 py-3 bg-black border border-[#1a1a1a] rounded-lg text-[#f5f5f5] text-sm placeholder-[#333] focus:border-[#c5a55a]/40 focus:outline-none transition-colors"
        />
      </div>

      <div>
        <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em] font-medium">
          Email
        </label>
        <input
          type="email"
          name="email"
          required
          placeholder="your@email.com"
          className="w-full px-4 py-3 bg-black border border-[#1a1a1a] rounded-lg text-[#f5f5f5] text-sm placeholder-[#333] focus:border-[#c5a55a]/40 focus:outline-none transition-colors"
        />
      </div>

      <div>
        <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em] font-medium">
          Create Password
        </label>
        <input
          type="password"
          name="password"
          required
          minLength={6}
          placeholder="Min 6 characters"
          className="w-full px-4 py-3 bg-black border border-[#1a1a1a] rounded-lg text-[#f5f5f5] text-sm placeholder-[#333] focus:border-[#c5a55a]/40 focus:outline-none transition-colors"
        />
      </div>

      <button
        type="submit"
        disabled={isPending}
        className="w-full py-3 bg-[#10b981] hover:bg-[#0d9668] text-white font-medium text-sm rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed uppercase tracking-wider"
      >
        {isPending ? 'Creating Account...' : 'Join Project'}
      </button>

      <p className="text-[10px] text-[#333] text-center leading-relaxed">
        Already have an account?{' '}
        <a href="/login" className="text-[#c5a55a] hover:text-[#c5a55a]/80 transition-colors">
          Sign in here
        </a>
      </p>
    </form>
  )
}
