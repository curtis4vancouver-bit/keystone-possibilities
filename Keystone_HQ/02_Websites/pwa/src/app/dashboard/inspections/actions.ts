'use server'

import { createClient } from '@/utils/supabase/server'
import { revalidatePath } from 'next/cache'

/**
 * PM/Inspector Action: Log a site inspection or structural audit report.
 */
export async function logInspection(formData: FormData) {
  const supabase = await createClient()
  const { data: { user }, error: authError } = await supabase.auth.getUser()

  if (authError || !user) {
    return { error: 'Not authenticated' }
  }

  const projectId = formData.get('project_id') as string
  const milestoneId = formData.get('milestone_id') as string | null
  const title = formData.get('title') as string
  const status = formData.get('status') as 'passed' | 'failed'
  const notes = formData.get('notes') as string
  const file = formData.get('file') as File | null

  if (!projectId || !title || !status) {
    return { error: 'Project ID, title, and status are required' }
  }

  // 1. Verify user is authorized (PM, Owner, or City Inspector)
  const { data: userData, error: userError } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()

  if (userError || !userData) {
    return { error: 'User profile not found' }
  }

  const isAuthorized = ['pm', 'owner', 'city_inspector'].includes(userData.role)
  if (!isAuthorized) {
    return { error: 'Unauthorized: Only GCs, Owners, or Inspectors can log quality reports' }
  }

  let fileUrl = ''
  let fileName = ''

  // 2. Upload file to Supabase Storage if present
  if (file && file.size > 0) {
    if (file.size > 10 * 1024 * 1024) {
      return { error: 'File size must be under 10MB' }
    }

    const ext = file.name.split('.').pop()
    fileName = `${projectId}/${Date.now()}_inspection_${title.replace(/\s+/g, '_')}.${ext}`

    const { error: uploadError } = await supabase.storage
      .from('documents')
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: false,
      })

    if (uploadError) {
      console.error('Storage upload error:', uploadError)
      return { error: 'Failed to upload report file: ' + uploadError.message }
    }

    const { data: urlData } = supabase.storage.from('documents').getPublicUrl(fileName)
    fileUrl = urlData.publicUrl
  }

  // 3. Map milestone to trade category if milestone is linked
  let tradeId = null
  if (milestoneId) {
    // Find the trade category assigned to this project that fits the milestone name (approximate)
    const { data: milestone } = await supabase
      .from('milestones')
      .select('title')
      .eq('id', milestoneId)
      .single()

    if (milestone) {
      const { data: trade } = await supabase
        .from('project_trades')
        .select('id')
        .eq('project_id', projectId)
        .ilike('trade_category', `%${milestone.title.substring(0, 15)}%`)
        .limit(1)
        .maybeSingle()
      
      if (trade) {
        tradeId = trade.id
      }
    }
  }

  // 4. Create document entry
  const { data: docData, error: docError } = await supabase
    .from('documents')
    .insert([{
      project_id: projectId,
      trade_id: tradeId,
      uploaded_by: user.id,
      document_type: 'inspection_report',
      title: `${title} - ${status.toUpperCase()}`,
      file_url: fileUrl || '#', // Placeholder if no file
      status: status === 'passed' ? 'active' : 'action_needed'
    }])
    .select('id')
    .single()

  if (docError) {
    console.error('Document insert error:', docError)
    return { error: 'Failed to save report record: ' + docError.message }
  }

  // 5. Update milestone state if linked
  if (milestoneId) {
    const nextStatus = status === 'passed' ? 'completed' : 'failed_action_needed'
    const { error: msError } = await supabase
      .from('milestones')
      .update({ status: nextStatus })
      .eq('id', milestoneId)

    if (msError) {
      console.error('Failed to update milestone status:', msError)
    }
  }

  // 6. Add communications audit log
  const statusLabel = status === 'passed' ? 'PASSED ✅' : 'FAILED ❌ (ACTION REQUIRED)'
  const notesText = notes ? ` Notes: ${notes}` : ''
  const docLinkText = fileUrl ? ` [View Report: ${fileUrl}]` : ''

  await supabase
    .from('communications')
    .insert([{
      project_id: projectId,
      sender_id: user.id,
      message: `AUDIT LOG: Quality report "${title}" logged as ${statusLabel}.${notesText}${docLinkText}`
    }])

  revalidatePath('/dashboard/inspections')
  revalidatePath('/dashboard/calendar')
  revalidatePath('/dashboard')
  return { success: true }
}

/**
 * PM/Inspector Action: Resolve an active deficiency, clearing the action_needed status.
 */
export async function resolveDeficiency(documentId: string, projectId: string, milestoneId?: string) {
  const supabase = await createClient()
  const { data: { user }, error: authError } = await supabase.auth.getUser()

  if (authError || !user) {
    return { error: 'Not authenticated' }
  }

  // Update document status to active
  const { data: doc, error: updateError } = await supabase
    .from('documents')
    .update({ status: 'active' })
    .eq('id', documentId)
    .select('title')
    .single()

  if (updateError || !doc) {
    return { error: 'Failed to resolve deficiency: ' + (updateError?.message || 'Document not found') }
  }

  // If milestone is provided, restore status
  if (milestoneId) {
    await supabase
      .from('milestones')
      .update({ status: 'completed' })
      .eq('id', milestoneId)
  }

  // Log in communications
  await supabase
    .from('communications')
    .insert([{
      project_id: projectId,
      sender_id: user.id,
      message: `AUDIT LOG: Deficiency for "${doc.title.replace(' - FAILED', '')}" marked as RESOLVED by Project Manager.`
    }])

  revalidatePath('/dashboard/inspections')
  revalidatePath('/dashboard/calendar')
  revalidatePath('/dashboard')
  return { success: true }
}
