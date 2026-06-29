import React, { useState, useEffect } from 'react';
import { Settings, Globe, Music, Shield, Box, Layout, AudioLines, Sparkles, Disc, BrainCircuit, Mic2, Video } from 'lucide-react';

const Footer = ({ isAgentWorking = false }) => {
  const [cpu, setCpu] = useState(0);
  const [ram, setRam] = useState(0);
  const [vram, setVram] = useState(0);
  const [ramUsed, setRamUsed] = useState(0);
  const [ramTotal, setRamTotal] = useState(16);
  const [vramUsed, setVramUsed] = useState(0);
  const [vramTotal, setVramTotal] = useState(16);
  
  const [appStatuses, setAppStatuses] = useState({
    vpn: false,
    docker: false,
    obsidian: false,
    davinci: false,
    facebook: false,
    antigravity: false
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/system');
        if (res.ok) {
          const data = await res.json();
          setCpu(data.cpu_percent || 0);
          setRam(data.ram_percent || 0);
          setVram(data.vram_percent || 0);
          setRamUsed(data.ram_used_gb || 0);
          setRamTotal(data.ram_total_gb || 16);
          setVramUsed(data.vram_used_gb || 0);
          setVramTotal(data.vram_total_gb || 16);
        }
      } catch (err) {
        console.error('Failed to fetch system stats:', err);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchAppStatuses = async () => {
      const statuses = {};
      const appNames = ['vpn', 'docker', 'obsidian', 'davinci', 'antigravity'];
      for (const name of appNames) {
        try {
          const res = await fetch(`/api/status/${name}`);
          if (res.ok) {
            const data = await res.json();
            statuses[name] = data.running;
          }
        } catch (err) {
          statuses[name] = false;
        }
      }
      setAppStatuses(prev => {
        const isChanged = Object.keys(statuses).some(k => statuses[k] !== prev[k]);
        return isChanged ? { ...prev, ...statuses } : prev;
      });
    };

    fetchAppStatuses();
    const interval = setInterval(fetchAppStatuses, 3000);
    return () => clearInterval(interval);
  }, []);

  const apps = [
    {
      name: 'Antigravity',
      title: 'Antigravity IDE',
      icon: (
        <svg viewBox="0 0 128 128" fill="none" style={{ width: '20px', height: '20px' }}>
          <defs>
            <linearGradient id="footerAgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#00d4ff"/>
              <stop offset="100%" stopColor="#0055ff"/>
            </linearGradient>
          </defs>
          <circle cx="64" cy="64" r="56" fill="url(#footerAgGrad)"/>
          <path d="M64 24L32 72h64L64 24z" fill="#ffffff"/>
        </svg>
      )
    },
    {
      name: 'VPN',
      title: 'Proton VPN',
      icon: (
        <svg viewBox="0 0 128 128" fill="none" style={{ width: '20px', height: '20px' }}>
          <defs>
            <linearGradient id="protonGrad" x1="15%" y1="15%" x2="85%" y2="85%">
              <stop offset="0%" stopColor="#aa7dfd"/>
              <stop offset="60%" stopColor="#6d4aff"/>
              <stop offset="100%" stopColor="#4c2bb3"/>
            </linearGradient>
          </defs>
          <path d="M64 8C43.5 14.5 24 16 16 28v42c0 28.5 29 44.5 48 50c19-5.5 48-21.5 48-50V28c-8-12-27.5-13.5-48-20z" fill="url(#protonGrad)"/>
          <path d="M64 24L32 38v30c0 19.5 19 32.5 32 36.5 13-4 32-17 32-36.5V38L64 24z" fill="#ffffff" fillOpacity="0.12"/>
          <path d="M64 42L48 50v14c0 10.5 10 17 16 19.5 6-2.5 16-9 16-19.5V50L64 42z" fill="#00ffff" fillOpacity="0.85"/>
        </svg>
      )
    },
    {
      name: 'Docker',
      title: 'Docker Desktop',
      icon: (
        <svg viewBox="0 0 128 128" fill="none" style={{ width: '20px', height: '20px' }}>
          <g fill="#0db7ed">
            <rect x="36" y="24" width="14" height="10" rx="1.5"/>
            <rect x="54" y="24" width="14" height="10" rx="1.5"/>
            <rect x="72" y="24" width="14" height="10" rx="1.5"/>
            <rect x="27" y="38" width="14" height="10" rx="1.5"/>
            <rect x="45" y="38" width="14" height="10" rx="1.5"/>
            <rect x="63" y="38" width="14" height="10" rx="1.5"/>
            <rect x="81" y="38" width="14" height="10" rx="1.5"/>
          </g>
          <path d="M120 62c-2-1.5-6.5-2-10-1c-1.5-6.5-6-11.5-12-14c-1 3.5-.5 7 .5 9.5c-4-.5-8-.5-12 0c-4-4.5-9.5-7.5-16-7.5c-11.5 0-21 9-22 20H12c-5.5 0-9.5 4-9.5 9.5c0 16 15 28 35.5 28c31.5 0 54-15 64-28.5c6 .5 13-1.5 18-9.5c1.5-2.5 1.5-5.5 0-7z" fill="#0db7ed"/>
        </svg>
      )
    },
    {
      name: 'Obsidian',
      title: 'Obsidian Vault',
      icon: (
        <svg viewBox="0 0 128 128" fill="none" style={{ width: '20px', height: '20px' }}>
          <defs>
            <linearGradient id="obsidianGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#4a37a0"/>
              <stop offset="100%" stopColor="#24145c"/>
            </linearGradient>
            <linearGradient id="obsidianGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#935df8"/>
              <stop offset="100%" stopColor="#562bb0"/>
            </linearGradient>
          </defs>
          <polygon points="64,8 108,44 88,96 64,120 40,96 20,44" fill="url(#obsidianGrad1)"/>
          <polygon points="64,8 108,44 64,68" fill="url(#obsidianGrad2)" opacity="0.8"/>
          <polygon points="64,8 64,68 20,44" fill="#a472ff" opacity="0.4"/>
          <polygon points="20,44 64,68 40,96" fill="#582cb5" opacity="0.9"/>
          <polygon points="108,44 88,96 64,68" fill="#884df0" opacity="0.75"/>
          <polygon points="40,96 64,68 88,96 64,120" fill="#321875" opacity="0.95"/>
        </svg>
      )
    },
    {
      name: 'DaVinci',
      title: 'DaVinci Resolve',
      icon: (
        <svg viewBox="0 0 128 128" fill="none" style={{ width: '20px', height: '20px' }}>
          <defs>
            <radialGradient id="redPetal" cx="35%" cy="65%" r="60%">
              <stop offset="0%" stopColor="#ff6688"/>
              <stop offset="60%" stopColor="#ff1a4a"/>
              <stop offset="100%" stopColor="#80001a"/>
            </radialGradient>
            <radialGradient id="bluePetal" cx="65%" cy="35%" r="60%">
              <stop offset="0%" stopColor="#66e6ff"/>
              <stop offset="60%" stopColor="#00aacc"/>
              <stop offset="100%" stopColor="#005566"/>
            </radialGradient>
            <radialGradient id="greenPetal" cx="65%" cy="65%" r="60%">
              <stop offset="0%" stopColor="#a3ff66"/>
              <stop offset="60%" stopColor="#66cc00"/>
              <stop offset="100%" stopColor="#336600"/>
            </radialGradient>
          </defs>
          <path d="M64 64c0-18.5 15-33.5 33.5-33.5c18.5 0 20.5 23.5 3.5 30.5c-12 5-23.5 12-37 3z" fill="url(#bluePetal)"/>
          <path d="M64 64c-16 9.2-31.8-4.3-41-20.2c-9.2-16 11.2-30 20.4-14.1c6.5 11.2 13.8 21.6 20.6 34.3z" fill="url(#redPetal)"/>
          <path d="M64 64c16.1 9.2 1.3 32.1-14.6 41.3c-15.9 9.2-31.7-10.4-15.8-19.6c11.2-6.5 21.6-13.8 30.4-21.7z" fill="url(#greenPetal)"/>
          <circle cx="64" cy="64" r="8" fill="#ffffff" opacity="0.95"/>
        </svg>
      )
    },
    {
      name: 'Facebook',
      title: 'Facebook Creator Portal',
      icon: (
        <svg viewBox="0 0 24 24" fill="#1877F2" style={{ width: '20px', height: '20px' }}>
          <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
        </svg>
      )
    },
    {
      name: 'Settings',
      title: 'System Settings',
      icon: <Settings size={20} color="var(--text-main)" />
    }
  ];

  const websites = [
    { name: 'Possibilities', title: 'Keystone Possibilities Website', icon: <Layout size={18} color="#00ffff" /> },
    { name: 'Recomposition', title: 'Keystone Recomposition Website', icon: <Music size={18} color="#00ffaa" /> },
    { name: 'Flow', title: 'Google Flow Studio', icon: <Sparkles size={18} color="#aa7dfd" /> },
    { name: 'SEO', title: 'Google Search Console', icon: <Globe size={18} color="#ffaa00" /> },
    { name: '11 Labs', title: 'ElevenLabs Voice Generator', icon: <AudioLines size={18} color="#ff3366" /> },
    { name: '2 Lost', title: '2Lost Music Distribution', icon: <Disc size={18} color="#a259ff" /> },
    { name: 'MusicBrains', title: 'MusicBrainz Database', icon: <BrainCircuit size={18} color="#3b82f6" /> },
    { name: 'MusicMatch', title: 'Musixmatch Lyrics Portal', icon: <Mic2 size={18} color="#ff44aa" /> },
    { name: 'YT Studio', title: 'YouTube Studio Portal', icon: <Video size={18} color="#ff0000" /> },
    { name: 'TikTok', title: 'TikTok Creator Studio', icon: <Video size={18} color="#ee1d52" /> },
    { name: 'Gmail', title: 'Google Gmail Portal', icon: (
      <svg viewBox="0 0 24 24" style={{ width: '18px', height: '18px', flexShrink: 0 }}>
        <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="#ea4335" />
      </svg>
    )},
    { name: 'Gemini', title: 'Google Gemini AI Studio', icon: (
      <svg viewBox="0 0 24 24" fill="none" style={{ width: '18px', height: '18px', flexShrink: 0 }}>
        <path d="M12 2L14.85 9.15L22 12L14.85 14.85L12 22L9.15 14.85L2 12L9.15 9.15L12 2Z" fill="url(#footerGeminiGradient)" />
        <defs>
          <linearGradient id="footerGeminiGradient" x1="2" y1="12" x2="22" y2="12" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="50%" stopColor="#8b5cf6" />
            <stop offset="100%" stopColor="#ec4899" />
          </linearGradient>
        </defs>
      </svg>
    )}
  ];

  const handleAppClick = async (appName) => {
    try {
      const endpointName = appName.toLowerCase();
      if (endpointName === 'settings') {
        console.log('Settings clicked');
        return;
      }
      if (endpointName === 'facebook') {
        await fetch(`/api/launch/facebook`, { method: 'POST' });
        return;
      }
      
      const isRunning = appStatuses[endpointName] || false;
      const endpoint = isRunning ? `/api/stop/${endpointName}` : `/api/launch/${endpointName}`;
      const res = await fetch(endpoint, { method: 'POST' });
      if (res.ok) {
        setAppStatuses(prev => ({ ...prev, [endpointName]: !isRunning }));
      } else {
        console.error(`Failed to toggle ${appName}`);
      }
    } catch (err) {
      console.error(`Error toggling app ${appName}:`, err);
    }
  };

  const websiteUrls = {
    'Possibilities': 'https://keystonepossibilities.ca/wp-admin/',
    'Recomposition': 'https://keystonerecomposition.com/wp-admin/',
    'Flow': 'https://labs.google/fx/tools/flow',
    'SEO': 'https://search.google.com/search-console',
    '11 Labs': 'https://elevenlabs.io/sign-in',
    '2 Lost': 'https://toolost.com/login',
    'MusicBrains': 'https://musicbrainz.org/login',
    'MusicMatch': 'https://www.musixmatch.com/sign-in',
    'YT Studio': 'https://studio.youtube.com',
    'TikTok': 'https://www.tiktok.com/login',
    'Gmail': 'https://mail.google.com',
    'Gemini': 'https://aistudio.google.com'
  };

  const handleWebClick = (webName) => {
    const url = websiteUrls[webName];
    if (url) {
      window.open(url, '_blank');
    }
  };

  return (
    <div style={{
      height: '96px',
      backgroundColor: 'var(--bg-panel)',
      borderTop: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      gap: '24px',
      overflow: 'visible',
      zIndex: 100,
      position: 'relative'
    }}>
      
      {/* Local Apps (Left Side Squircles) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {apps.map(app => {
          const lowerName = app.name.toLowerCase();
          const isRunning = appStatuses[lowerName] || false;
          return (
            <div 
              key={app.name} 
              className="tool-btn" 
              title={app.title} 
              onClick={() => handleAppClick(app.name)}
              style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', cursor: 'pointer', position: 'relative' }}
            >
              <div className="tool-icon" style={{
                width: '38px', height: '38px',
                borderRadius: '10px',
                border: isRunning ? '1px solid rgba(16, 185, 129, 0.5)' : '1px solid rgba(0, 212, 255, 0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                boxShadow: isRunning ? '0 0 10px rgba(16, 185, 129, 0.3), 0 4px 10px rgba(0, 0, 0, 0.4)' : '0 4px 10px rgba(0, 0, 0, 0.4)',
                backgroundColor: isRunning ? 'rgba(16, 185, 129, 0.1)' : 'rgba(10, 15, 30, 0.4)',
                transition: 'all 0.3s ease'
              }}>
                {app.icon}
              </div>
              
              {/* Green indicator dot if app is running */}
              {isRunning && (
                <span style={{
                  position: 'absolute',
                  top: '-2px',
                  right: '4px',
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  backgroundColor: '#10b981',
                  boxShadow: '0 0 6px #10b981',
                  border: '1.5px solid var(--bg-panel)'
                }} />
              )}
              
              <span style={{ fontSize: '9px', color: 'var(--text-muted)', marginTop: '3px' }}>{app.name}</span>
            </div>
          );
        })}
      </div>

      {/* Telemetry (Center Stack with Moving Bars) */}
      <div style={{
        position: 'absolute',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '360px',
        display: 'flex',
        flexDirection: 'column',
        gap: '6px'
      }}>
        {/* RAM */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '48px', fontFamily: 'monospace', fontSize: '10px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            RAM
            <svg 
              className={`telemetry-processing-indicator ${isAgentWorking ? 'working' : 'idle'}`} 
              viewBox="0 0 24 24" 
              style={{ 
                width: '12px', 
                height: '12px', 
                flexShrink: 0, 
                overflow: 'visible',
                opacity: isAgentWorking ? 1 : 0.45,
                transition: 'all 0.3s ease'
              }}
            >
              <style dangerouslySetInnerHTML={{__html: `
                @keyframes spin-cw {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
                @keyframes spin-ccw {
                  0% { transform: rotate(360deg); }
                  100% { transform: rotate(0deg); }
                }
                @keyframes pulse-glow {
                  0% { opacity: 0.4; filter: drop-shadow(0 0 1px #00d4ff); }
                  50% { opacity: 1; filter: drop-shadow(0 0 4px #00d4ff); }
                  100% { opacity: 0.4; filter: drop-shadow(0 0 1px #00d4ff); }
                }
                .telemetry-circle-outer {
                  transform-origin: center;
                  transition: stroke-dasharray 0.3s ease;
                }
                .telemetry-circle-inner {
                  transform-origin: center;
                  transition: stroke-dasharray 0.3s ease;
                }
                .telemetry-core {
                  transition: all 0.3s ease;
                }
                .working .telemetry-circle-outer {
                  animation: spin-cw 3.5s linear infinite;
                }
                .working .telemetry-circle-inner {
                  animation: spin-ccw 2.2s linear infinite;
                }
                .working .telemetry-core {
                  animation: pulse-glow 1.5s ease-in-out infinite;
                }
              `}} />
              <circle 
                cx="12" 
                cy="12" 
                r="10" 
                stroke="#00d4ff" 
                strokeWidth="1.5" 
                fill="none" 
                strokeDasharray={isAgentWorking ? "4 3" : "none"} 
                className="telemetry-circle-outer" 
              />
              <circle 
                cx="12" 
                cy="12" 
                r="6" 
                stroke="#ff8800" 
                strokeWidth="1.2" 
                fill="none" 
                strokeDasharray={isAgentWorking ? "3 2" : "none"} 
                className="telemetry-circle-inner" 
              />
              <circle 
                cx="12" 
                cy="12" 
                r="2.5" 
                fill="#00d4ff" 
                className="telemetry-core" 
              />
            </svg>
          </span>
          <div className="monitor-bar-container" style={{ flex: 1, height: '6px' }}>
            <div className="monitor-bar-fill ram-fill" style={{ width: `${ram}%` }}></div>
          </div>
          <span style={{ width: '60px', fontFamily: 'monospace', fontSize: '10px', textAlign: 'right', color: 'var(--accent-blue)' }}>
            {ramUsed.toFixed(1)} GB
          </span>
        </div>

        {/* VRAM */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '48px', fontFamily: 'monospace', fontSize: '10px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            VRAM
            <span style={{ fontSize: '7px', color: 'rgba(255,255,255,0.15)' }}>●</span>
          </span>
          <div className="monitor-bar-container" style={{ flex: 1, height: '6px' }}>
            <div className="monitor-bar-fill vram-fill" style={{ width: `${vram}%` }}></div>
          </div>
          <span style={{ width: '60px', fontFamily: 'monospace', fontSize: '10px', textAlign: 'right', color: 'var(--accent-green)' }}>
            {vramUsed.toFixed(1)} GB
          </span>
        </div>

        {/* CPU */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '48px', fontFamily: 'monospace', fontSize: '10px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            CPU
            <span style={{ fontSize: '7px', color: 'rgba(255,255,255,0.15)' }}>●</span>
          </span>
          <div className="monitor-bar-container" style={{ flex: 1, height: '6px' }}>
            <div className="monitor-bar-fill cpu-fill" style={{ width: `${cpu}%` }}></div>
          </div>
          <span style={{ width: '60px', fontFamily: 'monospace', fontSize: '10px', textAlign: 'right', color: 'var(--accent-red)' }}>
            {cpu}%
          </span>
        </div>
      </div>

      {/* Websites (Right Side Squircles) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {websites.map(web => (
          <div 
            key={web.name} 
            className="tool-btn" 
            title={web.title} 
            onClick={() => handleWebClick(web.name)}
            style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', cursor: 'pointer' }}
          >
            <div className="tool-icon" style={{
              width: '38px', height: '38px',
              borderRadius: '10px',
              border: '1px solid rgba(0, 212, 255, 0.12)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: '0 4px 10px rgba(0, 0, 0, 0.4)',
              backgroundColor: 'rgba(10, 15, 30, 0.4)'
            }}>
              {web.icon}
            </div>
            <span style={{ fontSize: '9px', color: 'var(--text-muted)', marginTop: '3px', maxWidth: '56px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {web.name}
            </span>
          </div>
        ))}
      </div>

    </div>
  );
};

export default Footer;
