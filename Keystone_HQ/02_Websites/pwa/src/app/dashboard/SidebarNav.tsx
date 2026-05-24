'use client'

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { 
    href: '/dashboard', 
    label: 'Overview', 
    exact: true,
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
      </svg>
    )
  },
  { 
    href: '/dashboard/calendar', 
    label: 'Master Calendar',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
      </svg>
    )
  },
  { 
    href: '/dashboard/documents', 
    label: 'Document Vault',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"></path>
      </svg>
    )
  },
  { 
    href: '/dashboard/inspections', 
    label: 'Inspections', 
    badge: true,
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
      </svg>
    )
  },
  { 
    href: '/dashboard/financials', 
    label: 'Financial Hub',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
    )
  },
  { 
    href: '/dashboard/trades', 
    label: 'Trades & Teams',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
      </svg>
    )
  },
  { 
    href: '/dashboard/calculator', 
    label: 'Site Calculator',
    icon: (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
      </svg>
    )
  },
];

export function SidebarNav({ role }: { role: string }) {
  const pathname = usePathname();

  function isActive(href: string, exact?: boolean) {
    if (exact) return pathname === href;
    return pathname.startsWith(href);
  }

  return (
    <nav className="flex-1 p-4 space-y-1">
      <p className="px-4 py-2 text-[9px] uppercase tracking-[0.25em] text-[#666] font-medium">Navigation</p>
      {navItems.map((item) => {
        const active = isActive(item.href, item.exact);
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-4 py-2.5 text-sm rounded-lg transition-all duration-200 group ${
              active
                ? 'bg-[#c5a55a]/8 text-[#c5a55a] font-medium border border-[#c5a55a]/15'
                : 'text-[#a3a3a3] hover:bg-[#111] hover:text-[#f5f5f5]'
            }`}
          >
            <span className={`transition-colors duration-200 ${active ? 'text-[#c5a55a]' : 'text-[#404040] group-hover:text-[#666]'}`}>
              {item.icon}
            </span>
            <span className="flex-1">{item.label}</span>
            {item.badge && (
              <span className={`w-2 h-2 rounded-full ${active ? 'bg-[#c5a55a]' : 'bg-[#c5a55a]/40'}`}></span>
            )}
          </Link>
        );
      })}

      {role === 'pm' && (
        <>
          <div className="kp-keyline my-4" />
          <p className="px-4 py-2 text-[9px] uppercase tracking-[0.25em] text-[#666] font-medium">System</p>
          <Link
            href="/dashboard/admin"
            className={`flex items-center gap-3 px-4 py-2.5 text-sm rounded-lg transition-all duration-200 group ${
              isActive('/dashboard/admin')
                ? 'bg-[#f59e0b]/8 text-[#f59e0b] font-medium border border-[#f59e0b]/15'
                : 'text-[#f59e0b]/50 hover:bg-[#f59e0b]/5 hover:text-[#f59e0b]'
            }`}
          >
            <svg className={`w-4 h-4 transition-colors ${isActive('/dashboard/admin') ? 'text-[#f59e0b]' : 'text-[#f59e0b]/30 group-hover:text-[#f59e0b]/60'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
            <span>Admin Panel</span>
          </Link>
        </>
      )}
    </nav>
  );
}
