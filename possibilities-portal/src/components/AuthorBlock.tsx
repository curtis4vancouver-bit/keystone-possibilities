import React from 'react';

export default function AuthorBlock() {
  return (
    <div className="bg-[#0a0a0a] border-l-4 border-[#c4a265] p-6 mt-12 mb-8 rounded shadow-lg">
      <div className="flex items-center gap-5">
        <img 
          src="/assets/wayne-stevenson-founder.jpeg" 
          alt="Wayne Stevenson" 
          className="w-20 h-20 rounded-full object-cover border-2 border-white/10"
        />
        <div>
          <h3 className="text-white font-geist-sans text-xl m-0 mb-1">Wayne Stevenson</h3>
          <p className="text-[#c4a265] font-geist-sans text-sm uppercase tracking-wider m-0 mb-2 font-semibold">
            Certified BC Builder (Lic #52603)
          </p>
          <p className="text-[#a3a3a3] font-geist-mono text-sm leading-relaxed m-0 max-w-2xl">
            Wayne oversees all high-end residential project management in the Sea-to-Sky corridor, operating under strict structural guidelines and E-E-A-T principles for high-quality construction information.
          </p>
        </div>
      </div>
    </div>
  );
}
