'use server'

import { createClient } from '@/utils/supabase/server'
import { revalidatePath } from 'next/cache'

/**
 * Trade action: Submit an invoice for completed work.
 */
export async function submitInvoice(formData: FormData) {
  const supabase = await createClient()
  const { data: { user }, error: authError } = await supabase.auth.getUser()

  if (authError || !user) {
    return { error: 'Not authenticated' }
  }

  const projectId = formData.get('project_id') as string
  const amountStr = formData.get('amount') as string
  const description = formData.get('description') as string
  const file = formData.get('file') as File | null

  if (!projectId || !amountStr) {
    return { error: 'Project ID and amount are required' }
  }

  const amount = parseFloat(amountStr)
  if (isNaN(amount) || amount <= 0) {
    return { error: 'Invalid invoice amount' }
  }

  // 1. Get the trade_id for this user on this project
  const { data: tradeData, error: tradeError } = await supabase
    .from('project_trades')
    .select('id, trade_category')
    .eq('project_id', projectId)
    .eq('user_id', user.id)
    .single()

  if (tradeError || !tradeData) {
    return { error: 'You are not assigned as a trade on this project' }
  }

  let fileUrl = ''
  let documentId = null

  // 2. If a file is uploaded, upload to Supabase Storage
  if (file && file.size > 0) {
    if (file.size > 10 * 1024 * 1024) {
      return { error: 'File size must be under 10MB' }
    }

    const ext = file.name.split('.').pop()
    const fileName = `${projectId}/${Date.now()}_invoice_${tradeData.trade_category.replace(/\s+/g, '_')}.${ext}`

    const { error: uploadError } = await supabase.storage
      .from('documents')
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: false,
      })

    if (uploadError) {
      console.error('Storage upload error:', uploadError)
      return { error: 'Failed to upload invoice document: ' + uploadError.message }
    }

    const { data: urlData } = supabase.storage.from('documents').getPublicUrl(fileName)
    fileUrl = urlData.publicUrl

    // Create record in documents table
    const { data: docData, error: docError } = await supabase
      .from('documents')
      .insert([{
        project_id: projectId,
        trade_id: tradeData.id,
        uploaded_by: user.id,
        document_type: 'invoice',
        title: `Invoice - ${tradeData.trade_category}`,
        file_url: fileUrl,
        status: 'pending_approval'
      }])
      .select('id')
      .single()

    if (docError) {
      console.error('Document insert error:', docError)
    } else if (docData) {
      documentId = docData.id
    }
  }

  // 3. Create entry in financial_ledger
  const { data: ledgerEntry, error: ledgerError } = await supabase
    .from('financial_ledger')
    .insert([{
      project_id: projectId,
      trade_id: tradeData.id,
      requested_by: user.id,
      type: 'invoice',
      amount,
      description: description + (fileUrl ? ` [Invoice Link: ${fileUrl}]` : ''),
      status: 'pending'
    }])
    .select('id')
    .single()

  if (ledgerError) {
    console.error('Financial ledger insert error:', ledgerError)
    return { error: 'Failed to record invoice: ' + ledgerError.message }
  }

  // 4. Write audit log to communications
  await supabase
    .from('communications')
    .insert([{
      project_id: projectId,
      trade_id: tradeData.id,
      sender_id: user.id,
      message: `AUDIT LOG: ${tradeData.trade_category} submitted Invoice (Amount: $${amount.toLocaleString(undefined, {minimumFractionDigits: 2})}).`
    }])

  revalidatePath('/dashboard/financials')
  revalidatePath('/dashboard')
  return { success: true }
}

/**
 * Trade action: Submit a change order request for out-of-scope work.
 */
export async function submitChangeOrder(formData: FormData) {
  const supabase = await createClient()
  const { data: { user }, error: authError } = await supabase.auth.getUser()

  if (authError || !user) {
    return { error: 'Not authenticated' }
  }

  const projectId = formData.get('project_id') as string
  const amountStr = formData.get('amount') as string
  const description = formData.get('description') as string
  const file = formData.get('file') as File | null

  if (!projectId || !amountStr || !description) {
    return { error: 'Project ID, amount, and justification are required' }
  }

  const amount = parseFloat(amountStr)
  if (isNaN(amount) || amount <= 0) {
    return { error: 'Invalid change order amount' }
  }

  // 1. Get the trade_id for this user on this project
  const { data: tradeData, error: tradeError } = await supabase
    .from('project_trades')
    .select('id, trade_category')
    .eq('project_id', projectId)
    .eq('user_id', user.id)
    .single()

  if (tradeError || !tradeData) {
    return { error: 'You are not assigned as a trade on this project' }
  }

  let fileUrl = ''
  let documentId = null

  // 2. If a photo/file is uploaded, upload to Supabase Storage
  if (file && file.size > 0) {
    if (file.size > 10 * 1024 * 1024) {
      return { error: 'File size must be under 10MB' }
    }

    const ext = file.name.split('.').pop()
    const fileName = `${projectId}/${Date.now()}_changeorder_${tradeData.trade_category.replace(/\s+/g, '_')}.${ext}`

    const { error: uploadError } = await supabase.storage
      .from('documents')
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: false,
      })

    if (uploadError) {
      console.error('Storage upload error:', uploadError)
      return { error: 'Failed to upload supporting document: ' + uploadError.message }
    }

    const { data: urlData } = supabase.storage.from('documents').getPublicUrl(fileName)
    fileUrl = urlData.publicUrl

    // Create record in documents table
    const { data: docData, error: docError } = await supabase
      .from('documents')
      .insert([{
        project_id: projectId,
        trade_id: tradeData.id,
        uploaded_by: user.id,
        document_type: 'change_order',
        title: `Change Order Proof - ${tradeData.trade_category}`,
        file_url: fileUrl,
        status: 'pending_approval'
      }])
      .select('id')
      .single()

    if (docError) {
      console.error('Document insert error:', docError)
    } else if (docData) {
      documentId = docData.id
    }
  }

  // 3. Create entry in financial_ledger
  const { error: ledgerError } = await supabase
    .from('financial_ledger')
    .insert([{
      project_id: projectId,
      trade_id: tradeData.id,
      requested_by: user.id,
      type: 'change_order',
      amount,
      description: description + (fileUrl ? ` [Proof Link: ${fileUrl}]` : ''),
      status: 'pending'
    }])

  if (ledgerError) {
    console.error('Financial ledger insert error:', ledgerError)
    return { error: 'Failed to record change order request: ' + ledgerError.message }
  }

  // 4. Write audit log to communications
  await supabase
    .from('communications')
    .insert([{
      project_id: projectId,
      trade_id: tradeData.id,
      sender_id: user.id,
      message: `AUDIT LOG: ${tradeData.trade_category} requested Change Order (Amount: $${amount.toLocaleString(undefined, {minimumFractionDigits: 2})}). Justification: ${description.substring(0, 100)}...`
    }])

  revalidatePath('/dashboard/financials')
  revalidatePath('/dashboard')
  return { success: true }
}

/**
 * PM action: Approve, Pay, or Deny a ledger item.
 */
export async function updateLedgerStatus(
  ledgerId: string,
  projectId: string,
  newStatus: 'approved' | 'paid' | 'denied',
  denyReason?: string
) {
  const supabase = await createClient()
  const { data: { user }, error: authError } = await supabase.auth.getUser()

  if (authError || !user) {
    return { error: 'Not authenticated' }
  }

  // 1. Verify that the user is the project's PM or Owner
  const { data: project, error: projError } = await supabase
    .from('projects')
    .select('owner_id, pm_id')
    .eq('id', projectId)
    .single()

  if (projError || !project) {
    return { error: 'Project not found' }
  }

  const isOwnerOrPM = project.owner_id === user.id || project.pm_id === user.id
  if (!isOwnerOrPM) {
    return { error: 'Unauthorized: Only the project Owner or PM can approve financials' }
  }

  // 2. Fetch the ledger item
  const { data: ledgerItem, error: itemError } = await supabase
    .from('financial_ledger')
    .select('*, project_trades(trade_category)')
    .eq('id', ledgerId)
    .single()

  if (itemError || !ledgerItem) {
    return { error: 'Ledger item not found' }
  }

  // 3. Update the status
  const updateData: any = {
    status: newStatus,
    approved_by: user.id,
    approved_at: new Date().toISOString()
  }

  if (newStatus === 'denied' && denyReason) {
    updateData.description = ledgerItem.description + ` [PM DENIAL REASON: ${denyReason}]`
  }

  const { error: updateError } = await supabase
    .from('financial_ledger')
    .update(updateData)
    .eq('id', ledgerId)

  if (updateError) {
    return { error: 'Failed to update ledger item: ' + updateError.message }
  }

  const tradeName = ledgerItem.project_trades?.trade_category || 'Contractor'
  const actionWord = newStatus === 'approved' ? 'APPROVED' : newStatus === 'paid' ? 'MARKED PAID' : 'DENIED'
  const details = newStatus === 'denied' && denyReason ? ` Reason: ${denyReason}` : ''

  // 4. Log the audit event in communications
  await supabase
    .from('communications')
    .insert([{
      project_id: projectId,
      trade_id: ledgerItem.trade_id,
      sender_id: user.id,
      message: `AUDIT LOG: PM ${actionWord} the ${ledgerItem.type.replace('_', ' ')} of $${Number(ledgerItem.amount).toLocaleString(undefined, {minimumFractionDigits: 2})} for ${tradeName}.${details}`
    }])

  revalidatePath('/dashboard/financials')
  revalidatePath('/dashboard')
  return { success: true }
}
