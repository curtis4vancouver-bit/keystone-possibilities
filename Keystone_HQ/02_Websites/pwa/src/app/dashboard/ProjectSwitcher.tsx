'use client'

import { useRouter } from 'next/navigation'
import { useState, useTransition } from 'react'

interface Project {
  id: string
  title: string
  address: string | null
  status: string
}

export function ProjectSwitcher({
  projects,
  activeProjectId,
}: {
  projects: Project[]
  activeProjectId: string | null
}) {
  const router = useRouter()
  const [isOpen, setIsOpen] = useState(false)
  const [isPending, startTransition] = useTransition()

  const activeProject = projects.find(p => p.id === activeProjectId)

  const statusColors: Record<string, string> = {
    planning: 'bg-[#3b82f6]',
    active: 'bg-[#10b981]',
    on_hold: 'bg-[#f59e0b]',
    completed: 'bg-[#666]',
    archived: 'bg-[#404040]',
  }

  const handleSelect = (projectId: string) => {
    document.cookie = `active_project=${projectId};path=/;max-age=31536000`
    setIsOpen(false)
    startTransition(() => {
      router.refresh()
    })
  }

  const handleNewProject = () => {
    document.cookie = `active_project=__new__;path=/;max-age=31536000`
    setIsOpen(false)
    startTransition(() => {
      router.refresh()
    })
  }

  return (
    <div className="relative px-4 py-3 border-b border-[#1a1a1a]">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-2 px-3 py-2.5 bg-[#0a0a0a] border border-[#1a1a1a] rounded-lg hover:border-[#c5a55a]/20 transition-all duration-200 text-left group"
      >
        <div className="flex-1 min-w-0">
          {activeProject ? (
            <>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${statusColors[activeProject.status] || 'bg-[#666]'}`} />
                <p className="text-sm font-medium text-[#a3a3a3] group-hover:text-[#f5f5f5] truncate transition-colors">
                  {activeProject.title}
                </p>
              </div>
              {activeProject.address && (
                <p className="text-[10px] text-[#404040] mt-0.5 pl-4 truncate">
                  {activeProject.address}
                </p>
              )}
            </>
          ) : (
            <p className="text-sm text-[#666]">Select Project</p>
          )}
        </div>
        <svg
          className={`w-4 h-4 text-[#404040] group-hover:text-[#c5a55a] transition-all duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
          
          {/* Dropdown */}
          <div className="absolute left-4 right-4 top-full mt-1 z-50 bg-[#0a0a0a] border border-[#222] rounded-lg shadow-2xl shadow-black/50 overflow-hidden kp-animate-in">
            <div className="max-h-64 overflow-y-auto">
              {projects.map(project => (
                <button
                  key={project.id}
                  onClick={() => handleSelect(project.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-[#111] transition-all duration-200 ${
                    project.id === activeProjectId ? 'bg-[#111] border-l-2 border-[#c5a55a]' : 'border-l-2 border-transparent'
                  }`}
                >
                  <span className={`w-2 h-2 rounded-full shrink-0 ${statusColors[project.status] || 'bg-[#666]'}`} />
                  <div className="min-w-0">
                    <p className={`text-sm truncate ${project.id === activeProjectId ? 'text-[#c5a55a]' : 'text-[#a3a3a3]'}`}>{project.title}</p>
                    {project.address && (
                      <p className="text-[10px] text-[#404040] truncate">{project.address}</p>
                    )}
                  </div>
                  <span className="ml-auto text-[9px] uppercase tracking-[0.2em] text-[#404040] shrink-0">
                    {project.status.replace('_', ' ')}
                  </span>
                </button>
              ))}
            </div>
            
            {/* Create New */}
            <div className="border-t border-[#1a1a1a]">
              <button
                onClick={handleNewProject}
                className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-[#10b981]/5 transition-all duration-200 text-[#10b981]"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                </svg>
                <span className="text-sm font-medium tracking-wider uppercase text-[10px]">New Project</span>
              </button>
            </div>
          </div>
        </>
      )}

      {isPending && (
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center rounded-lg">
          <div className="w-4 h-4 border-2 border-[#c5a55a] border-t-transparent rounded-full animate-spin" />
        </div>
      )}
    </div>
  )
}
