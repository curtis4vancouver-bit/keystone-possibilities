import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'
import { InspectionReportModal } from './InspectionReportModal'
import { DeficiencyList } from './DeficiencyList'

export default async function InspectionsPage() {
  const supabase = await createClient()
  
  // 1. Get user profile and roles
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return (
      <div className="p-8 text-center text-[#666]">
        Please log in to view the Inspections Vault.
      </div>
    )
  }

  const { data: userData } = await supabase
    .from('users')
    .select('role')
    .eq('id', user.id)
    .single()
  
  const role = userData?.role || 'owner'
  const isAuthorized = ['pm', 'owner', 'city_inspector'].includes(role)
  const isPM = role === 'pm' || role === 'owner'

  // 2. Fetch projects and active project context
  const cookieStore = await cookies()
  const activeProjectCookie = cookieStore.get('active_project')?.value

  const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .order('created_at', { ascending: false })
    
  let project = null
  if (projects && projects.length > 0) {
    if (activeProjectCookie && activeProjectCookie !== '__new__') {
      project = projects.find(p => p.id === activeProjectCookie) || projects[0]
    } else {
      project = projects[0]
    }
  }

  if (!project) {
    return (
      <div className="p-8 max-w-6xl mx-auto text-center text-[#666]">
        No active project found. Please select or create a project in the Overview first.
      </div>
    )
  }

  // 3. Fetch milestones for THIS project to link in modal
  const { data: milestones } = await supabase
    .from('milestones')
    .select('id, title')
    .eq('project_id', project.id)
    .order('sequence_order', { ascending: true })

  // 4. Fetch inspection report documents for this project
  const { data: documents } = await supabase
    .from('documents')
    .select(`
      id,
      title,
      created_at,
      file_url,
      status,
      uploaded_by,
      users (
        full_name
      )
    `)
    .eq('project_id', project.id)
    .eq('document_type', 'inspection_report')
    .order('created_at', { ascending: false })

  const allDocuments = (documents || []) as any[]
  
  // Active deficiencies (action needed)
  const deficiencies = allDocuments.filter(doc => doc.status === 'action_needed')
  
  // Passed inspection reports
  const passedReports = allDocuments.filter(doc => doc.status === 'active')

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex flex-col sm:flex-row sm:justify-between sm:items-end border-b border-[#1a1a1a] pb-6 gap-4 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#3b82f6] font-semibold mb-2">Quality Assurance</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">
            {project.title} - Inspections Vault
          </h2>
          <p className="text-[#a3a3a3] text-sm font-light">Log site conditions, safety audits, and city inspection results.</p>
        </div>
        {isAuthorized && (
          <div className="flex gap-3">
            <InspectionReportModal projectId={project.id} milestones={milestones || []} />
          </div>
        )}
      </header>

      {/* Deficiency Alerts Banner at the top if any exist */}
      {deficiencies.length > 0 && (
        <DeficiencyList
          initialDeficiencies={deficiencies}
          isPM={isPM}
          projectId={project.id}
        />
      )}

      {/* Passed / Active Inspection Logs Grid */}
      <div className="space-y-4 kp-animate-in" style={{ animationDelay: '100ms' }}>
        <h3 className="text-sm font-semibold tracking-[0.15em] uppercase text-[#a3a3a3]">Passed Reports & Audits</h3>
        
        {passedReports.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {passedReports.map((item) => (
              <div 
                key={item.id} 
                className="kp-card p-6 relative overflow-hidden group hover:border-[#c5a55a]/30 transition-all duration-300"
              >
                <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                  <svg className="w-12 h-12 text-[#10b981]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <span className="inline-block text-[10px] text-[#10b981] bg-[#10b981]/10 border border-[#10b981]/25 px-2 py-0.5 rounded uppercase font-mono font-bold tracking-wider mb-2">
                      PASSED
                    </span>
                    <h4 className="text-lg font-light text-[#f5f5f5] group-hover:text-[#c5a55a] transition-colors">
                      {item.title.replace(' - PASSED', '')}
                    </h4>
                    <p className="text-xs text-[#666] font-mono mt-1">
                      Logged {new Date(item.created_at).toLocaleDateString()} by {item.users?.full_name || 'System'}
                    </p>
                  </div>
                </div>
                
                {item.file_url && item.file_url !== '#' && (
                  <div className="mt-4 pt-4 border-t border-[#1a1a1a] flex justify-between items-center">
                    <span className="text-xs text-[#404040]">Inspection document signed</span>
                    <a 
                      href={item.file_url} 
                      target="_blank" 
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 text-xs text-[#c5a55a] hover:underline"
                    >
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Download Report
                    </a>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="kp-card p-12 text-center bg-[#020202]">
            <div className="w-16 h-16 rounded-xl bg-[#0a0a0a] border border-[#1a1a1a] flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-[#404040]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-[#a3a3a3] mb-2">No Reports Found</h3>
            <p className="text-[#666] text-sm max-w-md mx-auto">
              City inspection documents and site photos will appear here once reports are logged by the PM or City Inspectors.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

