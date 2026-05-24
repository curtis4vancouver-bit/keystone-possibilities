import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { userId, projectId, role, category } = await req.json()

    if (!userId || !projectId) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 })
    }

    // Use admin client to update user role and link to project
    const admin = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    )

    // Update user role if it's 'owner'
    if (role === 'owner') {
      await admin
        .from('users')
        .update({ role: 'owner' })
        .eq('id', userId)

      // Link owner to project
      await admin
        .from('projects')
        .update({ owner_id: userId })
        .eq('id', projectId)
    }

    // If trade, add to project_trades
    if (role === 'trade' && category) {
      await admin
        .from('project_trades')
        .upsert({
          project_id: projectId,
          user_id: userId,
          trade_category: category,
          status: 'pending'
        })
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Invite accept error:', error)
    return NextResponse.json({ error: 'Internal error' }, { status: 500 })
  }
}
