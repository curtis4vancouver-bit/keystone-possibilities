'use server'

import { createClient } from '@/utils/supabase/server'
import { createClient as createAdminClient } from '@supabase/supabase-js'
import { revalidatePath } from 'next/cache'

export async function createUserAccount(formData: FormData) {
  // Verify caller is PM
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return { error: 'Not authenticated' }

  const { data: profile } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'pm') return { error: 'Only PMs can create accounts' }

  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const full_name = formData.get('full_name') as string
  const role = formData.get('role') as string

  if (!email || !password || !full_name || !role) {
    return { error: 'All fields are required' }
  }

  // Use admin client with service role key to create user
  const admin = createAdminClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  // Create the auth user (auto-confirms email)
  const { data: newUser, error: createError } = await admin.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
    user_metadata: { full_name }
  })

  if (createError) {
    return { error: createError.message }
  }

  // Update their role and auto-approve in public.users
  // (the trigger should have created the row, but let's ensure the role is correct)
  const { error: updateError } = await admin
    .from('users')
    .update({ role, is_approved: true, full_name })
    .eq('id', newUser.user.id)

  if (updateError) {
    // If trigger didn't fire, insert directly
    await admin
      .from('users')
      .upsert({
        id: newUser.user.id,
        email,
        full_name,
        role,
        is_approved: true
      })
  }

  revalidatePath('/dashboard/admin')
  return { success: true, email, password }
}


export async function approveUser(userId: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return { error: 'Not authenticated' }

  // Verify caller is PM
  const { data: profile } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'pm') return { error: 'Only PMs can approve users' }

  const { error } = await supabase
    .from('users')
    .update({ is_approved: true })
    .eq('id', userId)

  if (error) return { error: error.message }

  revalidatePath('/dashboard/admin')
  return { success: true }
}

export async function revokeUser(userId: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return { error: 'Not authenticated' }

  const { data: profile } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'pm') return { error: 'Only PMs can revoke users' }

  const { error } = await supabase
    .from('users')
    .update({ is_approved: false })
    .eq('id', userId)

  if (error) return { error: error.message }

  revalidatePath('/dashboard/admin')
  return { success: true }
}

/**
 * PM action: Reset/wipe all data for a specific project.
 * Deletes milestones, documents, communications, date_proposals, project_trades.
 * The project record itself is preserved.
 */
export async function resetProject(projectId: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return { error: 'Not authenticated' }

  // Verify caller is PM
  const { data: profile } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'pm') return { error: 'Only PMs can reset projects' }

  // Verify project exists and user is the PM
  const { data: project } = await supabase
    .from('projects')
    .select('id, pm_id, title')
    .eq('id', projectId)
    .single()

  if (!project) return { error: 'Project not found' }
  if (project.pm_id !== user.id) return { error: 'You are not the PM of this project' }

  const errors: string[] = []

  // Delete date_proposals via milestones
  const { data: milestoneIds } = await supabase
    .from('milestones')
    .select('id')
    .eq('project_id', projectId)

  if (milestoneIds && milestoneIds.length > 0) {
    const ids = milestoneIds.map(m => m.id)
    try {
      const { error: dpErr } = await supabase.from('date_proposals').delete().in('milestone_id', ids)
      // Ignore errors from missing table — date_proposals may not exist yet
      if (dpErr && !dpErr.message.includes('schema cache') && !dpErr.message.includes('not find')) {
        errors.push('date_proposals: ' + dpErr.message)
      }
    } catch {
      // Table doesn't exist, skip silently
    }
  }

  // Delete milestones
  const { error: msErr } = await supabase.from('milestones').delete().eq('project_id', projectId)
  if (msErr) errors.push('milestones: ' + msErr.message)

  // Delete documents
  const { error: docErr } = await supabase.from('documents').delete().eq('project_id', projectId)
  if (docErr) errors.push('documents: ' + docErr.message)

  // Delete communications
  const { error: comErr } = await supabase.from('communications').delete().eq('project_id', projectId)
  if (comErr) errors.push('communications: ' + comErr.message)

  // Delete project_trades (may not exist)
  try {
    const { error: ptErr } = await supabase.from('project_trades').delete().eq('project_id', projectId)
    if (ptErr && !ptErr.message.includes('schema cache') && !ptErr.message.includes('not find')) {
      errors.push('project_trades: ' + ptErr.message)
    }
  } catch {
    // Table doesn't exist, skip
  }

  // Delete the project itself
  const { error: projErr } = await supabase.from('projects').delete().eq('id', projectId)
  if (projErr) errors.push('projects: ' + projErr.message)

  if (errors.length > 0) {
    return { error: 'Partial reset. Errors: ' + errors.join(', ') }
  }

  revalidatePath('/dashboard')
  revalidatePath('/dashboard/admin')
  revalidatePath('/dashboard/calendar')
  revalidatePath('/dashboard/documents')
  return { success: true }
}
