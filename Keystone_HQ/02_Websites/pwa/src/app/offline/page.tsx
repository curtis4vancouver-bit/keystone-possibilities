'use client'

export default function OfflinePage() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="text-center max-w-md">
        <div className="w-20 h-20 rounded-full bg-[#0a0a0a] border border-[#1a1a1a] flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-[#666]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M18.364 5.636a9 9 0 010 12.728M5.636 18.364a9 9 0 010-12.728m12.728 0L5.636 18.364M12 9v4m0 4h.01" />
          </svg>
        </div>
        <h1 className="text-2xl font-light text-[#f5f5f5] mb-3">You&apos;re Offline</h1>
        <p className="text-[#a3a3a3] text-sm mb-8">
          Keystone Command Center requires an internet connection to sync project data. 
          Please check your Wi-Fi or cell signal and try again.
        </p>
        <button 
          onClick={() => window.location.reload()} 
          className="kp-btn-emerald px-6 py-3 text-sm font-medium"
        >
          Retry Connection
        </button>
      </div>
    </div>
  );
}
