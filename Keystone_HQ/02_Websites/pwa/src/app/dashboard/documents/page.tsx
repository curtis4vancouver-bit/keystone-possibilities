import { createClient } from '@/utils/supabase/server';
import { cookies } from 'next/headers';
import { SignContractButton } from './SignContractButton';
import { UploadDocumentForm } from './UploadDocumentForm';

export default async function DocumentVaultPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  const { data: userData } = await supabase.from('users').select('role').eq('id', user?.id).single();
  const isOwner = userData?.role === 'owner';
  const isPM = userData?.role === 'pm';

  const cookieStore = await cookies();
  const activeProjectCookie = cookieStore.get('active_project')?.value;
  const { data: projects } = await supabase.from('projects').select('id, title').order('created_at', { ascending: false });

  let project = null;
  if (projects && projects.length > 0) {
    if (activeProjectCookie && activeProjectCookie !== '__new__') {
      project = projects.find(p => p.id === activeProjectCookie) || projects[0];
    } else {
      project = projects[0];
    }
  }

  const { data: documents } = project 
    ? await supabase.from('documents').select('*').eq('project_id', project.id).order('created_at', { ascending: false })
    : { data: [] };

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto space-y-8">
      <header className="flex flex-col sm:flex-row sm:justify-between sm:items-end gap-4 border-b border-[#1a1a1a] pb-6 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#c5a55a] font-medium mb-2">Compliance & Storage</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">Document Vault</h2>
          <p className="text-[#a3a3a3] text-sm">Manage WCB, Liability Insurance, and Subcontractor Agreements.</p>
        </div>
        {project && <UploadDocumentForm projectId={project.id} />}
      </header>

      {documents && documents.length > 0 ? (
        <div className="kp-card overflow-hidden kp-animate-in" style={{ animationDelay: '100ms' }}>
          <table className="w-full text-left text-sm text-[#666]">
            <thead className="bg-[#0a0a0a] text-[9px] uppercase text-[#666] border-b border-[#1a1a1a] tracking-[0.2em]">
              <tr>
                <th className="px-6 py-4 font-medium">Document Title</th>
                <th className="px-6 py-4 font-medium">Type</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1a1a1a]">
              {documents.map((doc: any) => (
                <tr key={doc.id} className="hover:bg-[#0a0a0a] transition-colors">
                  <td className="px-6 py-4 text-[#a3a3a3]">{doc.title}</td>
                  <td className="px-6 py-4 capitalize">{doc.document_type.replace('_', ' ')}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-lg text-[10px] border ${
                      doc.status === 'active' 
                        ? 'bg-[#10b981]/8 text-[#10b981] border-[#10b981]/15' 
                        : 'bg-[#f59e0b]/8 text-[#f59e0b] border-[#f59e0b]/15'
                    }`}>
                      {doc.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right flex items-center justify-end gap-4">
                    <a href={doc.file_url} target="_blank" rel="noreferrer" className="text-[#666] hover:text-[#c5a55a] transition-colors text-xs uppercase tracking-wider">View</a>
                    {doc.document_type === 'pm_contract' && doc.status === 'pending_approval' && (isOwner || isPM) && (
                      <SignContractButton documentId={doc.id} />
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="kp-card p-12 text-center kp-animate-in" style={{ animationDelay: '100ms' }}>
          <div className="w-16 h-16 rounded-xl bg-[#111] border border-[#1a1a1a] flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-[#404040]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          </div>
          <h3 className="text-lg font-medium text-[#a3a3a3] mb-2">Vault is Empty</h3>
          <p className="text-[#666] text-sm">No documents have been uploaded to this workspace yet.</p>
        </div>
      )}
    </div>
  );
}
