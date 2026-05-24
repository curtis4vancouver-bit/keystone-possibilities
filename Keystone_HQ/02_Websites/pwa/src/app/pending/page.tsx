import { createClient } from '@/utils/supabase/server';
import { redirect } from 'next/navigation';
import { logout } from '@/app/login/actions';

export default async function PendingPage() {
  const supabase = await createClient();
  const { data: { user }, error: authError } = await supabase.auth.getUser();

  if (!user || authError) {
    redirect('/login');
  }

  const { data: profile } = await supabase
    .from('users')
    .select('is_approved, full_name')
    .eq('id', user.id)
    .single();

  if (profile?.is_approved) {
    redirect('/dashboard');
  }

  return (
    <div className="min-h-screen bg-black flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-light tracking-tight text-[#f5f5f5] uppercase">
          Keystone <span className="font-bold text-[#10b981]">Possibilities</span>
        </h2>
        <p className="mt-2 text-center text-sm text-[#666] tracking-widest uppercase">
          Authorization Pending
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-[#0a0a0a]/50 border border-[#1a1a1a] py-8 px-8 shadow sm:rounded-xl text-center">
          <svg className="mx-auto h-12 w-12 text-[#c5a55a] mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
          </svg>
          
          <h3 className="text-xl font-medium text-[#f5f5f5] mb-2">Account Restricted</h3>
          <p className="text-sm text-[#a3a3a3] mb-6 leading-relaxed">
            Your account ({user.email}) has been created, but it requires authorization to access the Command Center. 
            <br /><br />
            If you need to pay the entrance fee or establish a contract, please contact your project manager or use the payment portal. Once authorized, your access will be automatically granted.
          </p>

          <form action={logout}>
            <button className="w-full flex justify-center py-3 px-4 border border-[#1a1a1a] rounded-lg shadow-sm text-sm font-medium text-[#a3a3a3] bg-[#111] hover:bg-[#1a1a1a] transition-colors">
              Sign Out
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
