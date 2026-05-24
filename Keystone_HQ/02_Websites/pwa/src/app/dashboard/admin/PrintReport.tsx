'use client'

import { useState } from 'react'

interface ProjectReportProps {
  project: {
    id: string
    title: string
    address: string
    status: string
    total_budget: number | null
    pm_fee_percentage: number
    created_at: string
  }
  milestones: any[]
  documents: any[]
  trades: any[]
}

export function PrintReport({ project, milestones, documents, trades }: ProjectReportProps) {
  const [isGenerating, setIsGenerating] = useState(false)

  function handlePrint() {
    setIsGenerating(true)

    const completedMilestones = milestones.filter(m => m.status === 'completed').length
    const pendingMilestones = milestones.filter(m => m.status === 'pending').length
    const inProgressMilestones = milestones.filter(m => m.status === 'in_progress').length

    const reportHTML = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>${project.title} — Project Report</title>
        <style>
          * { margin: 0; padding: 0; box-sizing: border-box; }
          body { font-family: 'Segoe UI', Tahoma, sans-serif; color: #1a1a1a; padding: 40px; max-width: 900px; margin: 0 auto; }
          .header { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #10b981; padding-bottom: 20px; margin-bottom: 30px; }
          .header h1 { font-size: 28px; font-weight: 300; letter-spacing: 3px; text-transform: uppercase; }
          .header .subtitle { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }
          .header .date { text-align: right; font-size: 12px; color: #666; }
          .section { margin-bottom: 30px; }
          .section h2 { font-size: 14px; text-transform: uppercase; letter-spacing: 2px; color: #10b981; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid #e5e5e5; }
          .info-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 20px; }
          .info-card { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px; }
          .info-card label { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #6b7280; display: block; margin-bottom: 4px; }
          .info-card .value { font-size: 18px; font-weight: 600; }
          table { width: 100%; border-collapse: collapse; font-size: 12px; }
          th { background: #f3f4f6; text-align: left; padding: 10px 12px; text-transform: uppercase; font-size: 10px; letter-spacing: 1px; color: #6b7280; border-bottom: 2px solid #e5e7eb; }
          td { padding: 10px 12px; border-bottom: 1px solid #f3f4f6; }
          tr:hover { background: #fafafa; }
          .status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; text-transform: uppercase; font-weight: 600; }
          .status-completed { background: #d1fae5; color: #065f46; }
          .status-in_progress { background: #dbeafe; color: #1e40af; }
          .status-pending { background: #fef3c7; color: #92400e; }
          .status-planning { background: #fef3c7; color: #92400e; }
          .status-active_construction { background: #d1fae5; color: #065f46; }
          .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; font-size: 10px; color: #9ca3af; }
          .summary-row { display: flex; gap: 24px; margin-top: 12px; }
          .summary-item { font-size: 12px; color: #666; }
          .summary-item strong { color: #1a1a1a; }
          @media print { body { padding: 20px; } .no-print { display: none; } }
        </style>
      </head>
      <body>
        <div class="header">
          <div>
            <h1>Keystone Possibilities</h1>
            <p class="subtitle">Project Status Report</p>
          </div>
          <div class="date">
            <p><strong>Generated:</strong> ${new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
            <p>${new Date().toLocaleTimeString()}</p>
          </div>
        </div>

        <div class="section">
          <h2>Project Overview</h2>
          <div class="info-grid">
            <div class="info-card">
              <label>Project Name</label>
              <div class="value" style="font-size:14px">${project.title}</div>
            </div>
            <div class="info-card">
              <label>Address</label>
              <div class="value" style="font-size:14px">${project.address || 'N/A'}</div>
            </div>
            <div class="info-card">
              <label>Status</label>
              <div class="value"><span class="status-badge status-${project.status}">${project.status.replace('_', ' ')}</span></div>
            </div>
            <div class="info-card">
              <label>Total Budget</label>
              <div class="value">${project.total_budget ? '$' + project.total_budget.toLocaleString() : 'TBD'}</div>
            </div>
            <div class="info-card">
              <label>PM Fee (${project.pm_fee_percentage}%)</label>
              <div class="value">${project.total_budget ? '$' + (project.total_budget * (project.pm_fee_percentage / 100)).toLocaleString() : 'TBD'}</div>
            </div>
            <div class="info-card">
              <label>Project Created</label>
              <div class="value" style="font-size:14px">${new Date(project.created_at).toLocaleDateString()}</div>
            </div>
          </div>
        </div>

        <div class="section">
          <h2>Schedule / Milestones (${milestones.length})</h2>
          <div class="summary-row">
            <div class="summary-item">Completed: <strong>${completedMilestones}</strong></div>
            <div class="summary-item">In Progress: <strong>${inProgressMilestones}</strong></div>
            <div class="summary-item">Pending: <strong>${pendingMilestones}</strong></div>
          </div>
          ${milestones.length > 0 ? `
          <table style="margin-top:12px">
            <thead>
              <tr><th>#</th><th>Milestone</th><th>Start</th><th>End</th><th>Duration</th><th>Status</th></tr>
            </thead>
            <tbody>
              ${milestones.map(m => `
              <tr>
                <td>${m.sequence_order}</td>
                <td>${m.title}</td>
                <td>${new Date(m.start_date).toLocaleDateString()}</td>
                <td>${new Date(m.end_date).toLocaleDateString()}</td>
                <td>${m.duration_days} day${m.duration_days !== 1 ? 's' : ''}</td>
                <td><span class="status-badge status-${m.status}">${m.status}</span></td>
              </tr>`).join('')}
            </tbody>
          </table>` : '<p style="color:#999;margin-top:12px">No milestones created yet.</p>'}
        </div>

        <div class="section">
          <h2>Documents (${documents.length})</h2>
          ${documents.length > 0 ? `
          <table>
            <thead>
              <tr><th>Title</th><th>Type</th><th>Status</th><th>Uploaded</th></tr>
            </thead>
            <tbody>
              ${documents.map(d => `
              <tr>
                <td>${d.title}</td>
                <td>${d.document_type.replace('_', ' ')}</td>
                <td><span class="status-badge status-${d.status === 'active' ? 'completed' : 'pending'}">${d.status}</span></td>
                <td>${new Date(d.created_at).toLocaleDateString()}</td>
              </tr>`).join('')}
            </tbody>
          </table>` : '<p style="color:#999">No documents uploaded yet.</p>'}
        </div>

        <div class="section">
          <h2>Assigned Trades (${trades.length})</h2>
          ${trades.length > 0 ? `
          <table>
            <thead>
              <tr><th>Category</th><th>Status</th><th>Assigned</th></tr>
            </thead>
            <tbody>
              ${trades.map(t => `
              <tr>
                <td>${t.trade_category}</td>
                <td><span class="status-badge status-${t.status === 'active' ? 'completed' : 'pending'}">${t.status}</span></td>
                <td>${new Date(t.created_at).toLocaleDateString()}</td>
              </tr>`).join('')}
            </tbody>
          </table>` : '<p style="color:#999">No trades assigned yet.</p>'}
        </div>

        <div class="footer">
          <p>Keystone Possibilities Ltd. &bull; Confidential Project Report &bull; Generated by Command Center PWA</p>
          <p style="margin-top:4px">This report is a snapshot at the time of generation. Data may have changed since.</p>
        </div>
      </body>
      </html>
    `

    const printWindow = window.open('', '_blank')
    if (printWindow) {
      printWindow.document.write(reportHTML)
      printWindow.document.close()
      printWindow.onload = () => {
        printWindow.print()
      }
    }

    setIsGenerating(false)
  }

  return (
    <button
      onClick={handlePrint}
      disabled={isGenerating}
      className="w-full bg-[#111] hover:bg-[#1a1a1a] text-[#a3a3a3] border border-[#1a1a1a] hover:border-[#c5a55a]/30 py-3 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
    >
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
      </svg>
      {isGenerating ? 'Generating...' : 'Print Project Report'}
    </button>
  )
}
