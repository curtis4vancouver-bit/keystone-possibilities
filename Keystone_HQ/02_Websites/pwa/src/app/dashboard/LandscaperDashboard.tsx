'use client';

import React, { useState } from 'react';

interface LandscaperDashboardProps {
  projectId: string;
  projectName: string;
}

export default function LandscaperDashboard({ projectId, projectName }: LandscaperDashboardProps) {
  const [mossWallSignoff, setMossWallSignoff] = useState(false);
  const [cedarOrderReady, setCedarOrderReady] = useState(false);
  
  // Custom states for interactive checklist items
  const [materials, setMaterials] = useState([
    { id: 1, name: 'Premium Clear-Grade Western Red Cedar (Sauna Exterior)', qty: '1,200 LFT', status: 'delivered' },
    { id: 2, name: 'Structural Granite Footing Stone (Watts Point Sourcing)', qty: '8 Tons', status: 'pending' },
    { id: 3, name: 'Water-Permeable Sub-base Fabrics (Steep-Slope Stabilizer)', qty: '4 Rolls', status: 'delivered' },
    { id: 4, name: 'Native Salal & Emerald Forest Groundcovers (Biophilic Blends)', qty: '350 Pots', status: 'ordered' },
  ]);

  const [complianceLogs, setComplianceLogs] = useState([
    { id: 'env-1', label: 'Riparian Zone Border Assessment (Squamish Code)', status: 'Approved', auditor: 'C. Vance' },
    { id: 'env-2', label: 'Biophilic Micro-Climate Air Flow Model (EMF Shielding)', status: 'Pending Review', auditor: 'Keystone Architect' },
    { id: 'env-3', label: 'Rock-Anchor Drainage Path Approval', status: 'Approved', auditor: 'M. Geotech' },
  ]);

  return (
    <div className="space-y-8 kp-animate-in">
      {/* Biophilic Landscaping Header */}
      <div className="kp-card-gold p-6 relative overflow-hidden">
        <div className="absolute top-4 right-4 opacity-[0.05] text-[#c5a55a]">
          <svg width="100" height="100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707.707M12 7a5 5 0 100 10 5 5 0 000-10z" />
          </svg>
        </div>
        <div className="space-y-2">
          <span className="text-[9px] bg-[#c5a55a]/10 text-[#c5a55a] px-2 py-0.5 rounded-full border border-[#c5a55a]/15 font-mono uppercase tracking-widest">
            Specialized Portal
          </span>
          <h2 className="text-2xl font-light text-[#f5f5f5] tracking-wide">Landscaping & Exterior Living Workspace</h2>
          <p className="text-[#a3a3a3] text-sm max-w-xl">
            Coordinating natural stone integration, structural cedar decks, and micro-climate biophilic zoning for <span className="text-[#c5a55a] font-medium">{projectName}</span>.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Material Logs & Material Ordering */}
        <div className="lg:col-span-2 space-y-6">
          <div className="kp-card p-6 space-y-6">
            <div className="flex justify-between items-center border-b border-[#1a1a1a] pb-4">
              <div>
                <h3 className="text-sm font-medium tracking-wider uppercase text-[#f5f5f5]">Biophilic Material Register</h3>
                <p className="text-xs text-[#666] mt-0.5">Track specialized wood, stone, and plant supplies</p>
              </div>
              <button className="kp-btn-gold text-[10px] py-1.5 px-3">
                Log New Batch
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-[#1a1a1a] text-[#666] uppercase tracking-wider text-[10px]">
                    <th className="pb-3 font-medium">Material Description</th>
                    <th className="pb-3 font-medium text-right">Quantity Required</th>
                    <th className="pb-3 font-medium text-right pl-4">Delivery Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1a1a1a]/50">
                  {materials.map((mat) => (
                    <tr key={mat.id} className="group hover:bg-[#111]/30 transition-colors">
                      <td className="py-3 font-medium text-[#a3a3a3] group-hover:text-[#f5f5f5] transition-colors">
                        {mat.name}
                      </td>
                      <td className="py-3 text-right font-mono text-[#f5f5f5]">{mat.qty}</td>
                      <td className="py-3 text-right pl-4">
                        <span className={`inline-block px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-wider ${
                          mat.status === 'delivered' ? 'bg-[#10b981]/10 text-[#10b981] border border-[#10b981]/20' : 
                          mat.status === 'ordered' ? 'bg-[#3b82f6]/10 text-[#3b82f6] border border-[#3b82f6]/20' :
                          'bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20'
                        }`}>
                          {mat.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Interactive Moss Wall & Cedar Shield Cabin Workspaces */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="kp-card p-6 space-y-4">
              <h4 className="text-xs font-semibold uppercase tracking-widest text-[#c5a55a]">Suna Spa Cantilever Deck</h4>
              <p className="text-xs text-[#666] leading-relaxed">
                Confirm structural load limits on rock-anchored brackets. Grade clear cedar structural supports to coordinate alignment.
              </p>
              <div className="flex items-center gap-3 pt-2">
                <input 
                  type="checkbox" 
                  id="cedarReady" 
                  checked={cedarOrderReady}
                  onChange={(e) => setCedarOrderReady(e.target.checked)}
                  className="w-4 h-4 rounded border-[#1a1a1a] bg-black text-[#c5a55a] focus:ring-0"
                />
                <label htmlFor="cedarReady" className="text-xs text-[#a3a3a3] cursor-pointer selection:bg-transparent">
                  Sign-off clear cedar structural checks
                </label>
              </div>
            </div>

            <div className="kp-card p-6 space-y-4">
              <h4 className="text-xs font-semibold uppercase tracking-widest text-[#10b981]">Biophilic Living Moss Wall</h4>
              <p className="text-xs text-[#666] leading-relaxed">
                Check misting nozzles, water barrier backings, and automated mineral-dosing tubes. Coordinate with the electrical team for LED grow lamps.
              </p>
              <div className="flex items-center gap-3 pt-2">
                <input 
                  type="checkbox" 
                  id="mossReady" 
                  checked={mossWallSignoff}
                  onChange={(e) => setMossWallSignoff(e.target.checked)}
                  className="w-4 h-4 rounded border-[#1a1a1a] bg-black text-[#10b981] focus:ring-0"
                />
                <label htmlFor="mossReady" className="text-xs text-[#a3a3a3] cursor-pointer selection:bg-transparent">
                  Sign-off misting flow & moisture seal
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Environmental & Geotechnical Compliance Sidepanel */}
        <div className="space-y-6">
          <div className="kp-card p-6 space-y-6">
            <div>
              <h3 className="text-sm font-medium tracking-wider uppercase text-[#f5f5f5]">Eco Compliance Logs</h3>
              <p className="text-xs text-[#666] mt-0.5">BC Municipal & biophilic building compliance checks</p>
            </div>
            
            <div className="space-y-4">
              {complianceLogs.map((log) => (
                <div key={log.id} className="p-3 bg-[#050505] border border-[#1a1a1a] rounded-lg space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="text-[9px] text-[#666] uppercase font-mono">{log.id}</span>
                    <span className={`inline-block px-1.5 py-0.5 rounded-sm text-[8px] uppercase tracking-wider font-semibold ${
                      log.status === 'Approved' ? 'bg-[#10b981]/15 text-[#10b981]' : 'bg-[#f59e0b]/15 text-[#f59e0b]'
                    }`}>
                      {log.status}
                    </span>
                  </div>
                  <p className="text-xs font-medium text-[#a3a3a3]">{log.label}</p>
                  <p className="text-[9px] text-[#404040]">Auditor: {log.auditor}</p>
                </div>
              ))}
            </div>

            <button className="w-full py-2 bg-[#111] hover:bg-[#161616] text-[#a3a3a3] hover:text-[#f5f5f5] transition-all border border-[#1a1a1a] rounded-lg text-xs font-semibold uppercase tracking-wider">
              Request Geotechnical Audit
            </button>
          </div>

          {/* Quick Stats widget */}
          <div className="kp-card-gold p-6 space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-widest text-[#c5a55a] mb-2 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-[#c5a55a]"></span>
              Biophilic Index
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/35 p-3 rounded-lg border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase">Native Biomass</p>
                <p className="text-lg font-light text-[#f5f5f5] mt-1">84%</p>
              </div>
              <div className="bg-black/35 p-3 rounded-lg border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase">EMF Attenuation</p>
                <p className="text-lg font-light text-[#f5f5f5] mt-1">-32 dB</p>
              </div>
            </div>
            <p className="text-[10px] text-[#666] leading-relaxed text-center italic">
              "We construct spaces that respect and integrate with the coastal topography."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
