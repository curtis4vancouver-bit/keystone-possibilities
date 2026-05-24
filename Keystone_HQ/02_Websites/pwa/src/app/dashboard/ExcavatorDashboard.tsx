'use client';

import React, { useState } from 'react';

interface ExcavatorDashboardProps {
  projectId: string;
  projectName: string;
}

export default function ExcavatorDashboard({ projectId, projectName }: ExcavatorDashboardProps) {
  const [seismicCertSigned, setSeismicCertSigned] = useState(false);
  const [machineryCleared, setMachineryCleared] = useState(false);
  
  // Custom states for rock anchoring log
  const [anchors, setAnchors] = useState([
    { id: 'RA-01', location: 'Sauna Base Rock-Face (North)', depth: '4.2m', tension: '180 kN', status: 'verified' },
    { id: 'RA-02', location: 'Sauna Base Rock-Face (South)', depth: '4.0m', tension: '175 kN', status: 'verified' },
    { id: 'RA-03', location: 'Bridge Deck Footing (East)', depth: '5.5m', tension: '210 kN', status: 'pending_test' },
    { id: 'RA-04', location: 'Retaining Wall Tieback', depth: '3.8m', tension: '150 kN', status: 'active' },
  ]);

  const [geotechIncidents, setGeotechIncidents] = useState([
    { id: 1, type: 'Fractured Granite Intercept', action: 'Grout injected (M30 Structural)', date: 'May 18, 2026' },
    { id: 2, type: 'Seep Water Extraction', action: 'High-pressure drains installed', date: 'May 15, 2026' },
  ]);

  return (
    <div className="space-y-8 kp-animate-in">
      {/* Geotechnical & Excavation Header */}
      <div className="kp-card p-6 relative overflow-hidden bg-gradient-to-r from-[#111] via-[#141414] to-black border border-[#1a1a1a]">
        <div className="absolute top-4 right-4 opacity-[0.05] text-[#3b82f6]">
          <svg width="100" height="100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <div className="space-y-2">
          <span className="text-[9px] bg-blue-500/10 text-blue-400 px-2 py-0.5 rounded-full border border-blue-500/20 font-mono uppercase tracking-widest">
            Structural & Heavy Civil Portal
          </span>
          <h2 className="text-2xl font-light text-[#f5f5f5] tracking-wide">Excavation & Geotechnical Engineering</h2>
          <p className="text-[#a3a3a3] text-sm max-w-xl">
            Managing solid granite sub-excavation, heavy plant machinery, and rock-anchor load distributions for <span className="text-[#c5a55a] font-medium">{projectName}</span>.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Rock Anchor Log */}
        <div className="lg:col-span-2 space-y-6">
          <div className="kp-card p-6 space-y-6">
            <div className="flex justify-between items-center border-b border-[#1a1a1a] pb-4">
              <div>
                <h3 className="text-sm font-medium tracking-wider uppercase text-[#f5f5f5]">Granite Rock-Anchor Ledger</h3>
                <p className="text-xs text-[#666] mt-0.5">Tension testing and drill verification registers (Squamish Granite)</p>
              </div>
              <button className="kp-btn-gold text-[10px] py-1.5 px-3">
                Log Rock Anchor
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-[#1a1a1a] text-[#666] uppercase tracking-wider text-[10px]">
                    <th className="pb-3 font-medium">Anchor ID</th>
                    <th className="pb-3 font-medium">Drill Depth</th>
                    <th className="pb-3 font-medium text-right">Lock Tension</th>
                    <th className="pb-3 font-medium text-right pl-4">Safety Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#1a1a1a]/50">
                  {anchors.map((anchor) => (
                    <tr key={anchor.id} className="group hover:bg-[#111]/30 transition-colors">
                      <td className="py-3 font-mono font-medium text-[#c5a55a] group-hover:text-[#d4b46a] transition-colors">
                        {anchor.id} <span className="text-[10px] text-[#666] font-sans">({anchor.location})</span>
                      </td>
                      <td className="py-3 text-[#a3a3a3] font-mono">{anchor.depth}</td>
                      <td className="py-3 text-right font-mono text-[#f5f5f5]">{anchor.tension}</td>
                      <td className="py-3 text-right pl-4">
                        <span className={`inline-block px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-wider ${
                          anchor.status === 'verified' ? 'bg-[#10b981]/10 text-[#10b981] border border-[#10b981]/20' : 
                          anchor.status === 'pending_test' ? 'bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20' :
                          'bg-[#3b82f6]/10 text-[#3b82f6] border border-[#3b82f6]/20'
                        }`}>
                          {anchor.status.replace('_', ' ')}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Interactive Seismic & Machinery Workspaces */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="kp-card p-6 space-y-4">
              <h4 className="text-xs font-semibold uppercase tracking-widest text-blue-400">Slope stability & Seismic anchor</h4>
              <p className="text-xs text-[#666] leading-relaxed">
                Confirm all deep-rock shear key plates are tensioned and locked. Verify structural epoxy curing temperatures on cliffside granite beds.
              </p>
              <div className="flex items-center gap-3 pt-2">
                <input 
                  type="checkbox" 
                  id="seismicCert" 
                  checked={seismicCertSigned}
                  onChange={(e) => setSeismicCertSigned(e.target.checked)}
                  className="w-4 h-4 rounded border-[#1a1a1a] bg-black text-[#c5a55a] focus:ring-0"
                />
                <label htmlFor="seismicCert" className="text-xs text-[#a3a3a3] cursor-pointer selection:bg-transparent">
                  Sign-off epoxy cure & structural lock
                </label>
              </div>
            </div>

            <div className="kp-card p-6 space-y-4">
              <h4 className="text-xs font-semibold uppercase tracking-widest text-[#f59e0b]">Heavy machinery safety check</h4>
              <p className="text-xs text-[#666] leading-relaxed">
                Verify steep-slope excavator rigging certificates, high-pressure hydraulic lines, and fluid containment packs (prevent riparian zoning spill).
              </p>
              <div className="flex items-center gap-3 pt-2">
                <input 
                  type="checkbox" 
                  id="machineryCheck" 
                  checked={machineryCleared}
                  onChange={(e) => setMachineryCleared(e.target.checked)}
                  className="w-4 h-4 rounded border-[#1a1a1a] bg-black text-[#f59e0b] focus:ring-0"
                />
                <label htmlFor="machineryCheck" className="text-xs text-[#a3a3a3] cursor-pointer selection:bg-transparent">
                  Sign-off daily plant inspections
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Geotech Incidents & Plant Logs Sidepanel */}
        <div className="space-y-6">
          <div className="kp-card p-6 space-y-6">
            <div>
              <h3 className="text-sm font-medium tracking-wider uppercase text-[#f5f5f5]">Geotech Intercept Log</h3>
              <p className="text-xs text-[#666] mt-0.5">Real-time geotechnical structural incidents</p>
            </div>
            
            <div className="space-y-4">
              {geotechIncidents.map((inc) => (
                <div key={inc.id} className="p-3 bg-[#050505] border border-[#1a1a1a] rounded-lg space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="text-[9px] text-[#ef4444] uppercase font-mono tracking-wider font-semibold">Incident Registered</span>
                    <span className="text-[9px] text-[#666]">{inc.date}</span>
                  </div>
                  <p className="text-xs font-semibold text-[#f5f5f5]">{inc.type}</p>
                  <p className="text-xs text-[#a3a3a3]">{inc.action}</p>
                </div>
              ))}
            </div>

            <button className="w-full py-2 bg-[#111] hover:bg-[#161616] text-[#a3a3a3] hover:text-[#f5f5f5] transition-all border border-[#1a1a1a] rounded-lg text-xs font-semibold uppercase tracking-wider">
              Request Emergency Shear Key Review
            </button>
          </div>

          {/* Quick Stats widget */}
          <div className="kp-card-gold p-6 space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-widest text-[#c5a55a] mb-2 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
              Stability Metrics
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/35 p-3 rounded-lg border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase">Shear Resistance</p>
                <p className="text-lg font-light text-[#f5f5f5] mt-1">450 MPa</p>
              </div>
              <div className="bg-black/35 p-3 rounded-lg border border-[#1a1a1a]">
                <p className="text-[9px] text-[#666] uppercase">Slope Gradient</p>
                <p className="text-lg font-light text-[#f5f5f5] mt-1">42 deg</p>
              </div>
            </div>
            <p className="text-[10px] text-[#666] leading-relaxed text-center italic">
              "We anchor architectural masterpieces deep into BC's ancient bedrock."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
