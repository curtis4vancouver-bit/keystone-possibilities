'use client'

import { useState } from 'react'

export default function CalculatorPage() {
  const [length, setLength] = useState('')
  const [width, setWidth] = useState('')
  const [thickness, setThickness] = useState('')

  const cubicYards = (parseFloat(length || '0') * parseFloat(width || '0') * (parseFloat(thickness || '0') / 12)) / 27

  const [lbrLength, setLbrLength] = useState('')
  const [lbrSpacing, setLbrSpacing] = useState('16')
  const [lbrWallLength, setLbrWallLength] = useState('')

  const studsNeeded = lbrWallLength
    ? Math.ceil((parseFloat(lbrWallLength) * 12) / parseFloat(lbrSpacing || '16')) + 1
    : 0

  return (
    <div className="p-4 sm:p-8 max-w-6xl mx-auto space-y-8">
      <header className="flex justify-between items-end border-b border-[#1a1a1a] pb-6 kp-animate-in">
        <div>
          <p className="text-[10px] uppercase tracking-[0.25em] text-[#c5a55a] font-medium mb-2">Tools</p>
          <h2 className="text-3xl font-light text-[#f5f5f5] mb-2">Site Calculator</h2>
          <p className="text-[#a3a3a3] text-sm">Quick conversions, volume estimates, and material takeoffs.</p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 kp-animate-in" style={{ animationDelay: '100ms' }}>
        {/* Concrete Volume */}
        <div className="kp-card p-6">
          <h3 className="text-sm font-medium text-[#f5f5f5] mb-4 border-b border-[#1a1a1a] pb-3 uppercase tracking-wider">Concrete Volume (Slab)</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Length (ft)</label>
              <input type="number" value={length} onChange={e => setLength(e.target.value)} className="kp-input" placeholder="0" />
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Width (ft)</label>
              <input type="number" value={width} onChange={e => setWidth(e.target.value)} className="kp-input" placeholder="0" />
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Thickness (inches)</label>
              <input type="number" value={thickness} onChange={e => setThickness(e.target.value)} className="kp-input" placeholder="0" />
            </div>
            <div className="pt-4 border-t border-[#1a1a1a]">
              <div className="flex justify-between items-center mb-2">
                <span className="text-[#a3a3a3] text-sm">Total Cubic Yards:</span>
                <span className="text-2xl font-mono text-[#10b981] font-bold">{cubicYards.toFixed(2)}</span>
              </div>
              {cubicYards > 0 && (
                <div className="flex justify-between items-center text-sm">
                  <span className="text-[#666]">Bags (80lb) @ 0.6 cu ft each:</span>
                  <span className="text-[#a3a3a3] font-mono">{Math.ceil(cubicYards * 27 / 0.6)}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Stud Calculator */}
        <div className="kp-card p-6">
          <h3 className="text-sm font-medium text-[#f5f5f5] mb-4 border-b border-[#1a1a1a] pb-3 uppercase tracking-wider">Stud Calculator</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Wall Length (ft)</label>
              <input type="number" value={lbrWallLength} onChange={e => setLbrWallLength(e.target.value)} className="kp-input" placeholder="0" />
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Stud Spacing (inches)</label>
              <select value={lbrSpacing} onChange={e => setLbrSpacing(e.target.value)} className="kp-input scheme-dark">
                <option value="12">12" O.C.</option>
                <option value="16">16" O.C. (standard)</option>
                <option value="24">24" O.C.</option>
              </select>
            </div>
            <div>
              <label className="block text-[9px] uppercase text-[#c5a55a] mb-1.5 tracking-[0.2em]">Stud Length (ft)</label>
              <input type="number" value={lbrLength} onChange={e => setLbrLength(e.target.value)} className="kp-input" placeholder="8" />
            </div>
            <div className="pt-4 border-t border-[#1a1a1a]">
              <div className="flex justify-between items-center mb-2">
                <span className="text-[#a3a3a3] text-sm">Studs Needed:</span>
                <span className="text-2xl font-mono text-[#10b981] font-bold">{studsNeeded}</span>
              </div>
              {studsNeeded > 0 && lbrLength && (
                <div className="flex justify-between items-center text-sm">
                  <span className="text-[#666]">Total Linear Feet:</span>
                  <span className="text-[#a3a3a3] font-mono">{(studsNeeded * parseFloat(lbrLength)).toFixed(0)} ft</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Reference */}
      <div className="kp-card p-6 kp-animate-in" style={{ animationDelay: '200ms' }}>
        <h3 className="text-sm font-medium text-[#f5f5f5] mb-4 border-b border-[#1a1a1a] pb-3 uppercase tracking-wider">Quick Reference</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-sm">
          <div>
            <p className="text-[9px] uppercase text-[#c5a55a] mb-2 font-medium tracking-[0.2em]">Common Concrete Depths</p>
            <ul className="space-y-1 text-[#a3a3a3]">
              <li>• Walkway: 4"</li>
              <li>• Driveway: 5-6"</li>
              <li>• Garage slab: 6"</li>
              <li>• Foundation wall: 8-10"</li>
              <li>• Footing: 12-16"</li>
            </ul>
          </div>
          <div>
            <p className="text-[9px] uppercase text-[#c5a55a] mb-2 font-medium tracking-[0.2em]">Lumber Dimensions</p>
            <ul className="space-y-1 text-[#a3a3a3]">
              <li>• 2×4 actual: 1.5" × 3.5"</li>
              <li>• 2×6 actual: 1.5" × 5.5"</li>
              <li>• 2×8 actual: 1.5" × 7.25"</li>
              <li>• 2×10 actual: 1.5" × 9.25"</li>
              <li>• 2×12 actual: 1.5" × 11.25"</li>
            </ul>
          </div>
          <div>
            <p className="text-[9px] uppercase text-[#c5a55a] mb-2 font-medium tracking-[0.2em]">Unit Conversions</p>
            <ul className="space-y-1 text-[#a3a3a3]">
              <li>• 1 cu yd = 27 cu ft</li>
              <li>• 1 sq ft = 144 sq in</li>
              <li>• 1 meter = 3.281 ft</li>
              <li>• 1 acre = 43,560 sq ft</li>
              <li>• 1 board ft = 144 cu in</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
