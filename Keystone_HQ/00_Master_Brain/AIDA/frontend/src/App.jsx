import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { 
  Mic, RefreshCw, BarChart2, Folder, Cpu, HardDrive, Play, Square,
  Globe, Music, Shield, Box, Layout, AudioLines, Sparkles, Disc, 
  BrainCircuit, Mic2, Video
} from 'lucide-react';
import VoiceOrb from './components/VoiceOrb';
import { MarkdownRenderer } from './components/MarkdownRenderer';

const CircularProgress = ({ percent, color = '#10b981' }) => {
  const radius = 14;
  const strokeWidth = 2.5;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percent / 100) * circumference;
  
  return (
    <div style={{ position: 'relative', width: '34px', height: '34px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg width="34" height="34" style={{ transform: 'rotate(-90deg)' }}>
        <circle
          cx="17"
          cy="17"
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={strokeWidth}
        />
        <circle
          cx="17"
          cy="17"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 0.5s ease' }}
        />
      </svg>
      <span style={{ position: 'absolute', fontSize: '8px', fontWeight: 'bold', color: '#fff', fontFamily: 'monospace' }}>
        {percent}%
      </span>
    </div>
  );
};

function App() {
  // Voice Bridge & Agent Status
  const [voiceBridgeStatus, setVoiceBridgeStatus] = useState('disconnected');
  const [isF8Pressed, setIsF8Pressed] = useState(false);
  const [isAgentWorking, setIsAgentWorking] = useState(false);
  const [activeAgentsCount, setActiveAgentsCount] = useState(0);
  const [isPythonWorking, setIsPythonWorking] = useState(false);
  const [activePythonTasksCount, setActivePythonTasksCount] = useState(0);
  
  // Model & Chat Data
  const [selectedModel, setSelectedModel] = useState('Gemini 3.5 Flash (High)');
  const [chronosProjectId, setChronosProjectId] = useState('02ec213a-7c20-4ec1-8396-ea46c276b1b1');
  const [chronosChatId, setChronosChatId] = useState(null);
  const [messages, setMessages] = useState([]);
  
  // System Telemetry
  const [cpu, setCpu] = useState(0);
  const [ram, setRam] = useState(0);
  const [vram, setVram] = useState(0);
  const [ramUsed, setRamUsed] = useState(0);
  const [ramTotal, setRamTotal] = useState(16);
  const [vramUsed, setVramUsed] = useState(0);
  const [vramTotal, setVramTotal] = useState(16);
  
  // App Launcher Statuses
  const [appStatuses, setAppStatuses] = useState({
    vpn: false,
    docker: false,
    obsidian: false,
    davinci: false,
    facebook: false,
    antigravity: false
  });
  
  // Quota Data
  const [quotaData, setQuotaData] = useState({
    gemini_weekly: 86,
    gemini_weekly_text: "Weekly quota status loaded.",
    gemini_5hour: 91,
    gemini_5hour_text: "5-hour quota status loaded.",
    claude_weekly: 14,
    claude_weekly_text: "Weekly quota status loaded.",
    claude_5hour: 100,
    claude_5hour_text: "5-hour quota status loaded."
  });

  const chatEndRef = useRef(null);

  // Computed Voice State
  const voiceState = 
    voiceBridgeStatus === 'speaking' ? 'speaking' : 
    (voiceBridgeStatus === 'listening' || isF8Pressed) ? 'listening' : 
    isAgentWorking ? 'working' :
    'idle';

  // 1. Fetch Chronos Project and Chats on mount
  useEffect(() => {
    const initChronosChat = async () => {
      try {
        const projRes = await fetch('/api/projects');
        if (projRes.ok) {
          const projects = await projRes.json();
          const chronosProj = projects.find(p => p.name.includes('Chronos') || p.id === 'chronos');
          if (chronosProj) {
            setChronosProjectId(chronosProj.id);
            // Fetch chats for this project
            const chatsRes = await fetch(`/api/chats?project_id=${chronosProj.id}`);
            if (chatsRes.ok) {
              const chats = await chatsRes.json();
              if (chats.length > 0) {
                // Sort by last modified
                chats.sort((a, b) => b.mtime - a.mtime);
                setChronosChatId(chats[0].id);
                if (chats[0].model) {
                  setSelectedModel(chats[0].model);
                }
              }
            }
          }
        }
      } catch (err) {
        console.error('Failed to initialize Chronos chat:', err);
      }
    };
    initChronosChat();
  }, []);

  // 2. Poll active chat from backend config (handles switches/updates)
  useEffect(() => {
    const syncActiveChat = async () => {
      try {
        const activeRes = await fetch('/api/chats/active');
        if (activeRes.ok) {
          const activeData = await activeRes.json();
          const activeId = activeData.active_chat_id;
          if (activeId && activeId !== chronosChatId) {
            // Check if this chat belongs to the Chronos project
            const chatsRes = await fetch('/api/chats');
            if (chatsRes.ok) {
              const chats = await chatsRes.json();
              const foundChat = chats.find(c => c.id === activeId);
              if (foundChat && foundChat.project_id === chronosProjectId) {
                setChronosChatId(activeId);
                if (foundChat.model) {
                  setSelectedModel(foundChat.model);
                }
              }
            }
          }
        }
      } catch (err) {
        console.error('Error syncing active chat:', err);
      }
    };
    syncActiveChat();
    const interval = setInterval(syncActiveChat, 1000);
    return () => clearInterval(interval);
  }, [chronosChatId, chronosProjectId]);

  // 3. Poll messages for the active Chronos chat
  useEffect(() => {
    if (!chronosChatId) return;
    let isSubscribed = true;
    
    const fetchMessages = async () => {
      try {
        const res = await fetch(`/api/chats/${chronosChatId}/messages`);
        if (res.ok && isSubscribed) {
          const data = await res.json();
          const mapped = data.map(msg => ({
            sender: msg.sender,
            text: msg.content,
            timestamp: msg.timestamp,
            file_changes: msg.file_changes || []
          }));
          setMessages(prev => {
            if (prev.length !== mapped.length) return mapped;
            const isDifferent = prev.some((msg, idx) => 
              msg.sender !== mapped[idx].sender ||
              msg.text !== mapped[idx].text ||
              msg.timestamp !== mapped[idx].timestamp
            );
            return isDifferent ? mapped : prev;
          });
        }
      } catch (err) {
        console.error('Error fetching messages:', err);
      }
    };

    fetchMessages();
    const interval = setInterval(fetchMessages, 2000);
    return () => {
      isSubscribed = false;
      clearInterval(interval);
    };
  }, [chronosChatId]);

  // Scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 4. Poll system telemetry (CPU, RAM, VRAM)
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
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  // 5. Poll local apps running status
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
      setAppStatuses(prev => ({ ...prev, ...statuses }));
    };
    fetchAppStatuses();
    const interval = setInterval(fetchAppStatuses, 5000);
    return () => clearInterval(interval);
  }, []);

  // 6. Poll voice bridge status for live state sync (e.g. listening/speaking/disconnected)
  useEffect(() => {
    const fetchVoiceStatus = async () => {
      try {
        const res = await fetch('/api/voice/status');
        if (res.ok) {
          const data = await res.json();
          setVoiceBridgeStatus(prev => prev !== data.status ? data.status : prev);
        }
      } catch (err) {
        console.error("Failed to fetch voice status:", err);
      }
    };
    fetchVoiceStatus();
    const interval = setInterval(fetchVoiceStatus, 1000);
    return () => clearInterval(interval);
  }, []);

  // 7. Poll model quota data
  useEffect(() => {
    const fetchQuota = async () => {
      try {
        const res = await fetch('/api/models/quota');
        if (res.ok) {
          const data = await res.json();
          setQuotaData(data);
        }
      } catch (err) {
        console.error("Failed to fetch quota:", err);
      }
    };
    fetchQuota();
    const interval = setInterval(fetchQuota, 10000);
    return () => clearInterval(interval);
  }, []);

  // 8. Capture global F8/F9 keydown/keyup events inside the app screen
  useEffect(() => {
    const isKeyPressedRef = { current: false };

    const handleKeyDown = (e) => {
      if (e.key === 'F8' || e.key === 'F9') {
        e.preventDefault();
        if (!isKeyPressedRef.current) {
          isKeyPressedRef.current = true;
          setIsF8Pressed(true);
          fetch('/api/voice/press', { method: 'POST' }).catch(err => console.error('Failed to trigger press:', err));
        }
      }
    };

    const handleKeyUp = (e) => {
      if (e.key === 'F8' || e.key === 'F9') {
        e.preventDefault();
        if (isKeyPressedRef.current) {
          isKeyPressedRef.current = false;
          setIsF8Pressed(false);
          fetch('/api/voice/release', { method: 'POST' }).catch(err => console.error('Failed to trigger release:', err));
        }
      }
    };

    const handleBlur = () => {
      if (isKeyPressedRef.current) {
        isKeyPressedRef.current = false;
        setIsF8Pressed(false);
        fetch('/api/voice/release', { method: 'POST' }).catch(err => console.error('Failed to trigger release on blur:', err));
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    window.addEventListener('blur', handleBlur);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('blur', handleBlur);
    };
  }, []);

  // Voice Toggle Handler
  const toggleVoiceBridge = async () => {
    const isRunning = voiceBridgeStatus === 'connected' || voiceBridgeStatus === 'reconnecting';
    const endpoint = isRunning ? '/api/voice/stop' : '/api/voice/start';
    try {
      setVoiceBridgeStatus(isRunning ? 'disconnecting' : 'connecting');
      const res = await fetch(endpoint, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setVoiceBridgeStatus(data.status || 'disconnected');
      }
    } catch (err) {
      console.error('Failed to toggle voice bridge:', err);
    }
  };

  // Launch Local App Handler
  const handleAppClick = async (appName) => {
    try {
      const endpointName = appName.toLowerCase();
      if (endpointName === 'facebook') {
        await fetch(`/api/launch/facebook`, { method: 'POST' });
        return;
      }
      const isRunning = appStatuses[endpointName] || false;
      const endpoint = isRunning ? `/api/stop/${endpointName}` : `/api/launch/${endpointName}`;
      await fetch(endpoint, { method: 'POST' });
    } catch (err) {
      console.error(`Error toggling app ${appName}:`, err);
    }
  };

  // Force Refresh MCP Registry
  const handleMcpRefresh = async (e) => {
    const btn = e.currentTarget;
    btn.disabled = true;
    const oldText = btn.innerHTML;
    btn.innerHTML = 'Refreshing...';
    try {
      const res = await fetch('/api/mcp/refresh', { method: 'POST' });
      if (res.ok) {
        btn.innerHTML = 'MCP Refreshed';
        btn.style.color = 'var(--accent-green)';
      }
    } catch (err) {
      btn.innerHTML = 'Failed';
    } finally {
      setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = oldText;
        btn.style.color = '';
      }, 3000);
    }
  };

  // Open Local Folder Handler
  const handleOpenFolder = async (path) => {
    try {
      await fetch('/api/open-folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      });
    } catch (err) {
      console.error('Failed to open folder:', err);
    }
  };

  // Website Shortcut Config
  const websites = [
    { name: 'Possibilities', url: 'https://keystonepossibilities.ca/wp-admin/', icon: <Layout size={14} color="#00ffff" /> },
    { name: 'Recomposition', url: 'https://keystonerecomposition.com/wp-admin/', icon: <Music size={14} color="#00ffaa" /> },
    { name: 'Flow', url: 'https://labs.google/fx/tools/flow', icon: <Sparkles size={14} color="#aa7dfd" /> },
    { name: 'SEO', url: 'https://search.google.com/search-console', icon: <Globe size={14} color="#ffaa00" /> },
    { name: '11 Labs', url: 'https://elevenlabs.io/sign-in', icon: <AudioLines size={14} color="#ff3366" /> },
    { name: '2 Lost', url: 'https://toolost.com/login', icon: <Disc size={14} color="#a259ff" /> },
    { name: 'MusicBrains', url: 'https://musicbrainz.org/login', icon: <BrainCircuit size={14} color="#3b82f6" /> },
    { name: 'Musixmatch', url: 'https://www.musixmatch.com/sign-in', icon: <Mic2 size={14} color="#ff44aa" /> },
    { name: 'YT Studio', url: 'https://studio.youtube.com', icon: <Video size={14} color="#ff0000" /> },
    { name: 'TikTok', url: 'https://www.tiktok.com/login', icon: <Video size={14} color="#ee1d52" /> },
    { name: 'Suno', url: 'https://suno.com/', icon: <Music size={14} color="#fca5a5" /> },
    { name: 'Spotify', url: 'https://artists.spotify.com/', icon: <Disc size={14} color="#1ed760" /> },
    { name: 'Gmail', url: 'https://mail.google.com', icon: (
      <svg viewBox="0 0 24 24" style={{ width: '14px', height: '14px' }}>
        <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" fill="#ea4335" />
      </svg>
    )},
    { name: 'Gemini', url: 'https://aistudio.google.com', icon: (
      <svg viewBox="0 0 24 24" fill="none" style={{ width: '14px', height: '14px' }}>
        <path d="M12 2L14.85 9.15L22 12L14.85 14.85L12 22L9.15 14.85L2 12L9.15 9.15L12 2Z" fill="url(#hudGeminiGrad)" />
        <defs>
          <linearGradient id="hudGeminiGrad" x1="2" y1="12" x2="22" y2="12" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#3b82f6" /><stop offset="50%" stopColor="#8b5cf6" /><stop offset="100%" stopColor="#ec4899" />
          </linearGradient>
        </defs>
      </svg>
    )}
  ];

  const localApps = [
    { name: 'Antigravity', title: 'Antigravity IDE', color: '#00d4ff' },
    { name: 'VPN', title: 'Proton VPN', color: '#aa7dfd' },
    { name: 'Docker', title: 'Docker Desktop', color: '#0db7ed' },
    { name: 'Obsidian', title: 'Obsidian Vault', color: '#935df8' },
    { name: 'DaVinci', title: 'DaVinci Resolve', color: '#ff1a4a' },
    { name: 'Facebook', title: 'Facebook Portal', color: '#1877F2' }
  ];

  return (
    <div className="aida-v3-hud">
      {/* 1. Header with Orb */}
      <div className="hud-header">
        <div 
          onClick={toggleVoiceBridge} 
          style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%', padding: '10px 0', cursor: 'pointer' }}
          title="Toggle Voice Bridge"
        >
          <VoiceOrb state={voiceState} size={340} />
        </div>
        <h1 className="hud-title">A.I.D.A.</h1>
        <div className="hud-voice-status" onClick={toggleVoiceBridge} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}>
            <span className={`status-dot ${voiceBridgeStatus === 'connected' ? 'pulsing' : ''}`} style={{
              backgroundColor: voiceBridgeStatus === 'connected' ? 'var(--accent-green)' : 
                              voiceBridgeStatus === 'reconnecting' ? 'var(--accent-gold)' : 'var(--accent-red)'
            }} />
            <span>VOICE BRIDGE: {voiceBridgeStatus.toUpperCase()}</span>
          </div>
          {chronosChatId && (
            <span style={{ fontSize: '10px', color: 'rgba(255, 255, 255, 0.4)', fontFamily: 'monospace', letterSpacing: '0.5px', marginTop: '2px' }}>
              SESSION: {chronosChatId.slice(0, 8)}
            </span>
          )}
        </div>
      </div>

      {/* 4. App Launcher Grid */}
      <div className="hud-section">
        <div className="section-title">LOCAL APPLICATIONS</div>
        <div className="app-grid">
          {localApps.map(app => {
            const isRunning = appStatuses[app.name.toLowerCase()] || false;
            return (
              <div key={app.name} className={`app-card ${isRunning ? 'running' : ''}`} onClick={() => handleAppClick(app.name)} title={app.title}>
                <span className="app-indicator" style={{ backgroundColor: isRunning ? 'var(--accent-green)' : 'rgba(255,255,255,0.1)' }} />
                <span className="app-name">{app.name}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* 5. Website Shortcut Grid */}
      <div className="hud-section">
        <div className="section-title">WEB CHANNELS & PORTALS</div>
        <div className="web-grid">
          {websites.map(web => (
            <div key={web.name} className="web-card" onClick={() => window.open(web.url, '_blank')} title={web.name}>
              <span className="web-icon">{web.icon}</span>
              <span className="web-name">{web.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 6. Folder Shortcuts & Telemetry */}
      <div className="hud-footer">
        {/* Folders */}
        <div className="footer-folders">
          <button className="folder-btn" onClick={() => handleOpenFolder('C:\\Users\\Curtis\\Downloads')} title="Open Downloads Folder">
            <Folder size={12} /> Downloads
          </button>
          <button className="folder-btn" onClick={() => handleOpenFolder('C:\\Users\\Curtis\\Desktop\\Keystone Protocols')} title="Open Keystone Protocol Folder">
            <Folder size={12} /> Protocols
          </button>
          <button className="folder-btn" onClick={() => handleOpenFolder('C:\\Users\\Curtis\\Desktop\\Keystone Possibilities')} title="Open Possibilities Folder">
            <Folder size={12} /> Possibilities
          </button>
        </div>

        {/* Telemetry progress bars */}
        <div className="footer-telemetry">
          <div className="telem-row">
            <span className="telem-label">CPU</span>
            <div className="telem-bar"><div className="telem-fill cpu-fill" style={{ width: `${cpu}%` }} /></div>
            <span className="telem-val">{cpu}%</span>
          </div>
          <div className="telem-row">
            <span className="telem-label">RAM</span>
            <div className="telem-bar"><div className="telem-fill ram-fill" style={{ width: `${ram}%` }} /></div>
            <span className="telem-val">{ramUsed.toFixed(1)}GB</span>
          </div>
          <div className="telem-row">
            <span className="telem-label">VRAM</span>
            <div className="telem-bar"><div className="telem-fill vram-fill" style={{ width: `${vram}%` }} /></div>
            <span className="telem-val">{vramUsed.toFixed(1)}GB</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
