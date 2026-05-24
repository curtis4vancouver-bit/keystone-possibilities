import { createClient } from '@/utils/supabase/server';
import { GenerateTradeLink } from './GenerateTradeLink';

export default async function TradesPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  const { data: profile } = await supabase.from('users').select('role').eq('id', user?.id).single();
  const isPM = profile?.role === 'pm';

  const { data: projects } = await supabase.from('projects').select('id').order('created_at', { ascending: false });
  const project = projects && projects.length > 0 ? projects[0] : null;

  const { data: trades } = await supabase
    .from('project_trades')
    .select(`id, trade_category, status, locked_bid, user_id, users ( full_name, company_name, email )`)
    .order('created_at', { ascending: false });

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto space-y-8">
      <header className="flex flex-col sm:flex-row sm:justify-between sm:items-end gap-4 border-b border-[#1a1a1a] pb-6 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#c5a55a] font-medium mb-2">Team Management</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">Trades & Teams</h2>
          <p className="text-[#a3a3a3] text-sm">Manage subcontractors, assign tasks, and review bids.</p>
        </div>
      </header>

      {isPM && project && <GenerateTradeLink projectId={project.id} />}

      {trades && trades.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trades.map((trade: any) => (
            <div key={trade.id} className="kp-card p-6 hover:border-[#c5a55a]/20 transition-colors">
              <div className="flex justify-between items-start mb-4">
                <span className="px-2 py-1 bg-[#111] text-[#a3a3a3] text-[10px] rounded-lg border border-[#1a1a1a] uppercase tracking-wider">
                  {trade.trade_category}
                </span>
                <span className={`w-2 h-2 rounded-full ${trade.status === 'active' ? 'bg-[#10b981]' : 'bg-[#f59e0b]'}`}></span>
              </div>
              <h3 className="text-base font-medium text-[#f5f5f5] mb-1">
                {trade.users?.company_name || trade.users?.full_name || 'Unknown User'}
              </h3>
              <p className="text-xs text-[#666] mb-4">{trade.users?.email}</p>
              <div className="pt-4 border-t border-[#1a1a1a] flex justify-between items-center">
                <div>
                  <p className="text-[9px] text-[#666] uppercase tracking-[0.2em]">Locked Bid</p>
                  <p className="text-sm font-mono text-[#c5a55a]">
                    {trade.locked_bid ? `$${trade.locked_bid.toLocaleString()}` : 'Pending'}
                  </p>
                </div>
                <button className="text-[10px] text-[#c5a55a] hover:text-[#d4b46a] transition-colors uppercase tracking-wider">
                  View Workspace &rarr;
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="kp-card p-12 text-center kp-animate-in" style={{ animationDelay: '100ms' }}>
          <div className="w-16 h-16 rounded-xl bg-[#111] border border-[#1a1a1a] flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-[#404040]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          </div>
          <h3 className="text-lg font-medium text-[#a3a3a3] mb-2">No Trades Assigned</h3>
          <p className="text-[#666] text-sm">
            {isPM 
              ? 'Use the invite link generator above to bring subcontractors into this project.' 
              : 'Use the Assign Trades widget on the overview page to invite subcontractors.'}
          </p>
        </div>
      )}
    </div>
  );
}
