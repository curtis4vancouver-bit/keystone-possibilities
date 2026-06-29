import React from 'react';
import { Mic, PlusCircle, ChevronLeft, RefreshCw, BarChart2, MessageSquare, Settings, User, Shield, Palette, Cpu, Globe, Monitor, Info } from 'lucide-react';
import VoiceOrb from './VoiceOrb';

const CircularProgress = ({ percent, color = '#10b981' }) => {
  const radius = 16;
  const strokeWidth = 3;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percent / 100) * circumference;
  
  return (
    <div style={{ position: 'relative', width: '38px', height: '38px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg width="38" height="38" style={{ transform: 'rotate(-90deg)' }}>
        <circle
          cx="19"
          cy="19"
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.06)"
          strokeWidth={strokeWidth}
        />
        <circle
          cx="19"
          cy="19"
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
      <span style={{ position: 'absolute', fontSize: '9px', fontWeight: 'bold', color: '#fff', fontFamily: 'monospace' }}>
        {percent}%
      </span>
    </div>
  );
};

const SettingsPanel = () => {
  const [activeTab, setActiveTab] = React.useState('models');
  const [creditOverage, setCreditOverage] = React.useState(true);
  const [quotaData, setQuotaData] = React.useState({
    gemini_weekly: 86,
    gemini_weekly_text: "You have used some of your weekly limit, it will fully refresh in 3 days, 2 hours.",
    gemini_5hour: 91,
    gemini_5hour_text: "You have used some of your 5-hour limit, it will fully refresh in 4 hours, 32 minutes.",
    claude_weekly: 14,
    claude_weekly_text: "You have used some of your weekly limit, it will fully refresh in 13 hours, 20 minutes.",
    claude_5hour: 100,
    claude_5hour_text: "You have not used any of your 5-hour limit."
  });
  const [isLoading, setIsLoading] = React.useState(false);

  const fetchQuota = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/models/quota');
      if (res.ok) {
        const data = await res.json();
        setQuotaData(data);
        if (data.credit_overage !== undefined) {
          setCreditOverage(data.credit_overage);
        }
      }
    } catch (err) {
      console.error("Failed to fetch quota:", err);
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    if (activeTab === 'models') {
      fetchQuota();
    }
  }, [activeTab]);

  const tabs = [
    { id: 'general', label: 'General', icon: Settings },
    { id: 'account', label: 'Account', icon: User },
    { id: 'permissions', label: 'Permissions', icon: Shield },
    { id: 'appearance', label: 'Appearance', icon: Palette },
    { id: 'models', label: 'Models', icon: Cpu },
    { id: 'customizations', label: 'Customizations', icon: Monitor },
    { id: 'browser', label: 'Browser', icon: Globe },
    { id: 'app', label: 'App', icon: Monitor },
  ];

  return (
    <div style={{
      display: 'flex',
      height: '480px',
      backgroundColor: '#0c0c0e',
      color: '#e4e4e7',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      margin: '-16px'
    }}>
      {/* Left Sidebar */}
      <div style={{
        width: '180px',
        borderRight: '1px solid #27272a',
        backgroundColor: '#0e0e11',
        display: 'flex',
        flexDirection: 'column',
        padding: '12px 6px',
        overflowY: 'auto'
      }}>
        {tabs.map(tab => {
          const Icon = tab.icon;
          const isActive = tab.id === activeTab;
          return (
            <div
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '6px 12px',
                borderRadius: '4px',
                fontSize: '12.5px',
                cursor: 'pointer',
                color: isActive ? '#fff' : '#a1a1aa',
                backgroundColor: isActive ? '#27272a' : 'transparent',
                fontWeight: isActive ? 500 : 400,
                transition: 'all 0.15s ease',
                marginBottom: '2px'
              }}
            >
              <Icon size={14} color={isActive ? '#00d4ff' : '#71717a'} />
              <span style={{ whiteSpace: 'nowrap' }}>{tab.label}</span>
            </div>
          );
        })}
      </div>

      {/* Right Content */}
      <div style={{
        flex: 1,
        padding: '20px 24px',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        backgroundColor: '#0c0c0e'
      }}>
        {activeTab === 'models' ? (
          <>
            {/* Header Row */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '-4px' }}>
              <h2 style={{ fontSize: '15px', fontWeight: 600, color: '#fff', margin: 0 }}>Models</h2>
              <button 
                onClick={fetchQuota}
                disabled={isLoading}
                style={{
                  backgroundColor: '#27272a',
                  border: '1px solid #3f3f46',
                  color: '#e4e4e7',
                  padding: '4px 10px',
                  borderRadius: '4px',
                  fontSize: '11px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  transition: 'all 0.15s ease'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#3f3f46'; }}
                onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#27272a'; }}
              >
                <RefreshCw size={11} className={isLoading ? "spin-animation" : ""} />
                <span>{isLoading ? 'Updating...' : 'Refresh'}</span>
              </button>
            </div>

            {/* Model Credits Section */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <h3 style={{ fontSize: '13px', fontWeight: 600, color: '#fff', margin: 0 }}>Model Credits</h3>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'space-between',
                backgroundColor: '#131316',
                border: '1px solid #27272a',
                borderRadius: '6px',
                padding: '10px 14px'
              }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2px', paddingRight: '12px' }}>
                  <span style={{ fontSize: '12px', fontWeight: 500, color: '#fff' }}>Enable AI Credit Overages</span>
                  <span style={{ fontSize: '10.5px', color: '#71717a', lineHeight: '1.4' }}>
                    When toggled on, Antigravity will use your AI credits to fulfill model requests once you're out of model quota.
                  </span>
                </div>
                {/* Custom Toggle Switch */}
                <div 
                  onClick={() => setCreditOverage(!creditOverage)}
                  style={{
                    width: '32px',
                    height: '18px',
                    borderRadius: '9px',
                    backgroundColor: creditOverage ? '#10b981' : '#27272a',
                    position: 'relative',
                    cursor: 'pointer',
                    transition: 'background-color 0.2s ease',
                    flexShrink: 0
                  }}
                >
                  <div style={{
                    width: '14px',
                    height: '14px',
                    borderRadius: '50%',
                    backgroundColor: '#fff',
                    position: 'absolute',
                    top: '2px',
                    left: creditOverage ? '16px' : '2px',
                    transition: 'left 0.2s ease',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.4)'
                  }}></div>
                </div>
              </div>
            </div>

            {/* Model Quota Section */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <h3 style={{ fontSize: '13px', fontWeight: 600, color: '#fff', margin: 0 }}>Model Quota</h3>
              <span style={{ fontSize: '10.5px', color: '#71717a', lineHeight: '1.4' }}>
                Within each group, models share a weekly limit and a 5-hour limit. Quota is consumed proportionally to the cost of the tokens. Thus, limits will last longer with shorter tasks or using more cost-effective models.
              </span>

              {/* Gemini Models Card */}
              <div style={{
                backgroundColor: '#131316',
                border: '1px solid #27272a',
                borderRadius: '6px',
                padding: '12px 14px',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 600, color: '#fff' }}>
                  <span>Gemini Models</span>
                  <Info size={12} color="#71717a" style={{ cursor: 'pointer' }} />
                </div>
                
                {/* Gemini Weekly Limit Row */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px' }}>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 500, color: '#e4e4e7' }}>Weekly Limit</span>
                    <span style={{ fontSize: '10px', color: '#71717a' }}>{quotaData.gemini_weekly_text}</span>
                  </div>
                  <CircularProgress percent={quotaData.gemini_weekly} color="#10b981" />
                </div>

                {/* Gemini 5-Hour Limit Row */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', borderTop: '1px solid rgba(255,255,255,0.03)', paddingTop: '8px' }}>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 500, color: '#e4e4e7' }}>Five Hour Limit</span>
                    <span style={{ fontSize: '10px', color: '#71717a' }}>{quotaData.gemini_5hour_text}</span>
                  </div>
                  <CircularProgress percent={quotaData.gemini_5hour} color="#10b981" />
                </div>
              </div>

              {/* Claude/GPT Models Card */}
              <div style={{
                backgroundColor: '#131316',
                border: '1px solid #27272a',
                borderRadius: '6px',
                padding: '12px 14px',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontWeight: 600, color: '#fff' }}>
                  <span>Claude and GPT models</span>
                  <Info size={12} color="#71717a" style={{ cursor: 'pointer' }} />
                </div>

                {/* Claude Weekly Limit Row */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px' }}>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 500, color: '#e4e4e7' }}>Weekly Limit</span>
                    <span style={{ fontSize: '10px', color: '#71717a' }}>{quotaData.claude_weekly_text}</span>
                  </div>
                  <CircularProgress percent={quotaData.claude_weekly} color="#eab308" />
                </div>

                {/* Claude 5-Hour Limit Row */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', borderTop: '1px solid rgba(255,255,255,0.03)', paddingTop: '8px' }}>
                  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 500, color: '#e4e4e7' }}>Five Hour Limit</span>
                    <span style={{ fontSize: '10px', color: '#71717a' }}>{quotaData.claude_5hour_text}</span>
                  </div>
                  <CircularProgress percent={quotaData.claude_5hour} color="#10b981" />
                </div>
              </div>
            </div>
          </>
        ) : (
          <div style={{ display: 'flex', flex: 1, alignItems: 'center', justifyContent: 'center', height: '100%', color: '#71717a', fontSize: '12.5px' }}>
            <span>This setting is currently configured to inherit from your global system profile.</span>
          </div>
        )}
      </div>
    </div>
  );
};

const Sidebar = ({ width, onClose, onOpenWindow, voiceState = 'idle', voiceBridgeStatus = 'disconnected', onToggleVoice, selectedModel, onSelectModel, activeModule, onSelectModule, onNewChat }) => {
  const triggerMcpRefresh = () => {
    onOpenWindow('mcp', 'MCP Server Registry', (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px', fontFamily: 'monospace' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
          <span>SERVER NAME</span>
          <span>STATUS</span>
        </div>
        {[
          { name: 'brave-search', status: 'Connected' },
          { name: 'chrome-devtools-mcp', status: 'Connected' },
          { name: 'content-engine', status: 'Connected' },
          { name: 'keystone-brain', status: 'Connected' },
          { name: 'context7', status: 'Connected' }
        ].map(mcp => (
          <div key={mcp.name} style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-main)' }}>{mcp.name}</span>
            <span style={{ color: 'var(--accent-green)' }}>● {mcp.status}</span>
          </div>
        ))}
        <button style={{
          marginTop: '12px',
          backgroundColor: 'transparent',
          border: '1px solid var(--accent-blue)',
          color: 'var(--accent-blue)',
          padding: '6px',
          borderRadius: '4px',
          cursor: 'pointer',
          textAlign: 'center',
          transition: 'all 0.2s ease'
        }}
        onClick={async (e) => {
          const btn = e.currentTarget;
          btn.disabled = true;
          btn.innerText = 'Refreshing...';
          btn.style.borderColor = 'var(--accent-blue)';
          btn.style.color = 'var(--accent-blue)';
          
          try {
            const res = await fetch('/api/mcp/refresh', { method: 'POST' });
            if (res.ok) {
              btn.innerText = 'M C P Refreshed';
              btn.style.borderColor = 'var(--accent-green)';
              btn.style.color = 'var(--accent-green)';
            } else {
              btn.innerText = 'Refresh Failed';
              btn.style.borderColor = 'var(--accent-red)';
              btn.style.color = 'var(--accent-red)';
            }
          } catch (err) {
            console.error(err);
            btn.innerText = 'Refresh Error';
            btn.style.borderColor = 'var(--accent-red)';
            btn.style.color = 'var(--accent-red)';
          } finally {
            setTimeout(() => {
              btn.disabled = false;
              btn.innerText = 'Force Reset Registry';
              btn.style.borderColor = 'var(--accent-blue)';
              btn.style.color = 'var(--accent-blue)';
            }, 3000);
          }
        }}
        >
          Force Reset Registry
        </button>
      </div>
    ));
  };

  const triggerModelUsage = () => {
    onOpenWindow('models', 'Settings', <SettingsPanel />, '650px');
  };

  const [isModelDropdownOpen, setIsModelDropdownOpen] = React.useState(false);
  const [showUpdated, setShowUpdated] = React.useState(false);
  const firstRender = React.useRef(true);

  React.useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    setShowUpdated(true);
    const timer = setTimeout(() => setShowUpdated(false), 3000);
    return () => clearTimeout(timer);
  }, [selectedModel]);

  const modelsList = [
    { name: 'Gemini 3.5 Flash (Medium)', badge: 'Fast ⓘ' },
    { name: 'Gemini 3.5 Flash (High)', badge: 'Fast ⓘ' },
    { name: 'Gemini 3.5 Flash (Low)', badge: 'Fast ⓘ' },
    { name: 'Gemini 3.1 Pro (Low)', badge: null },
    { name: 'Gemini 3.1 Pro (High)', badge: null },
    { name: 'Claude Sonnet 4.6 (Thinking)', badge: null },
    { name: 'Claude Opus 4.6 (Thinking)', badge: null },
    { name: 'GPT-OSS 120B (Medium)', badge: null }
  ];


  return (
    <div className="panel" style={{ width: `${width}px`, flexShrink: 0, height: '100%', borderRight: '1px solid var(--border-color)', position: 'relative' }}>
      <div style={{ position: 'absolute', top: '8px', right: '8px', cursor: 'pointer', zIndex: 10 }} onClick={onClose}>
        <ChevronLeft size={16} color="var(--text-muted)" />
      </div>

      {/* Voice Visual Avatar */}
      <div style={{ 
        padding: '24px 16px 12px 16px', 
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        width: '100%'
      }}>
        {/* Donut visual centered and sized to fit sidebar width */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContainer: 'center', width: '100%' }}>
          <VoiceOrb state={voiceState} size={width - 32} />
        </div>
        
        {/* AIDA name underneath */}
        <h1 className="aida-sidebar-title" style={{
          width: '100%',
          textAlign: 'center',
          fontFamily: 'var(--font-mono)',
          fontSize: '36px',
          fontWeight: 700,
          letterSpacing: '6px',
          color: '#00d4ff',
          textShadow: '0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(0, 212, 255, 0.2)',
          textTransform: 'uppercase',
          margin: '12px 0 0 0'
        }}>
          A.I.D.A.
        </h1>
      </div>

      {/* Voice Toggle */}
      <div 
        onClick={onToggleVoice}
        style={{
          padding: '12px 16px',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexShrink: 0,
          cursor: 'pointer'
        }}
      >
        <div style={{display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px'}}>
          <Mic size={14} color={
            voiceBridgeStatus === 'connected' ? 'var(--accent-green)' : 
            voiceBridgeStatus === 'reconnecting' ? 'var(--accent-gold)' : 
            'var(--accent-red)'
          } />
          <span>VOICE BRIDGE [{voiceBridgeStatus.toUpperCase()}]</span>
        </div>
        <span style={{fontSize: '10px', color: 'var(--text-muted)'}}>[F9]</span>
      </div>

      {/* Active Modules list */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto', 
        padding: '12px 0',
        scrollbarWidth: 'thin'
      }}>
        <h3 style={{ fontSize: '10px', color: 'var(--text-muted)', padding: '0 16px', marginBottom: '8px', letterSpacing: '1px' }}>ACTIVE MODULES</h3>
        
        {[
          { id: 'chronos', name: 'Chronos (Master Brain)', desc: 'Vector Brain, self-healing, fixes' },
          { id: 'recomposition', name: 'Keystone Recomposition (Music)', desc: 'Music creation, publishing, Spotify' },
          { id: 'protocols', name: 'Keystone Protocols (Wellness)', desc: 'Peptide research, video production' },
          { id: 'possibilities', name: 'Keystone Possibilities (PM)', desc: 'Construction scripts, social uploads' },
          { id: 'webmaster', name: 'Websites, SEO & GEO', desc: 'WordPress, search engine domination' },
          { id: 'wayne_health', name: 'Wayne Stevenson (Health)', desc: 'Weight logs, peptides, bio-tracking' },
          { id: 'site_super', name: 'Site Superintendent (Work)', desc: 'Blueprints, STEP code compliance' },
          { id: 'tax_finance', name: 'Tax Strategist & Finance', desc: 'Deductions, structuring, corporate tax' },
          { id: 'market_analyst', name: 'Market Analyst (Wealth)', desc: 'Stocks, market research, trends' },
          { id: 'self_evolution', name: 'Self-Evolution & Learning', desc: 'Correction journal, compound learnings' }
        ].map((agent) => {
          const isActive = agent.id === activeModule;
          return (
            <div 
              key={agent.id} 
              className={`active-module-item ${isActive ? 'active' : ''}`}
              onClick={() => onSelectModule(agent.id)}
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '2px', minWidth: 0, flex: 1 }}>
                <span className="module-name" style={{ fontSize: '13px', color: 'var(--text-main)', transition: 'color 0.2s' }}>
                  {agent.name}
                </span>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {agent.desc}
                </span>
              </div>
              <div 
                className="new-chat-btn-box"
                title="New Chat (Flush & Archive)"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: '6px',
                  borderRadius: '4px',
                  border: '1px solid rgba(255,255,255,0.08)',
                  backgroundColor: 'rgba(255,255,255,0.02)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  marginLeft: '8px',
                  flexShrink: 0
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--accent-blue)';
                  e.currentTarget.style.backgroundColor = 'rgba(0, 212, 255, 0.08)';
                  e.currentTarget.style.boxShadow = '0 0 8px rgba(0, 212, 255, 0.2)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)';
                  e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.02)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  onNewChat(agent.id);
                }}
              >
                <PlusCircle size={14} color="var(--text-muted)" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Model Selector Dropdown (Dropup style) */}
      <div style={{
        padding: '10px 16px',
        borderTop: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        backgroundColor: 'rgba(0,0,0,0.1)',
        flexShrink: 0
      }}>
        <div 
          onClick={() => setIsModelDropdownOpen(!isModelDropdownOpen)}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '8px 12px',
            borderRadius: '6px',
            backgroundColor: 'var(--bg-panel-hover)',
            border: '1px solid var(--border-color)',
            cursor: 'pointer',
            fontSize: '12px',
            fontWeight: 500,
            transition: 'all 0.2s ease',
            color: 'var(--text-main)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = 'var(--accent-blue)';
            e.currentTarget.style.boxShadow = '0 0 10px rgba(59, 130, 246, 0.2)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'var(--border-color)';
            e.currentTarget.style.boxShadow = 'none';
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              backgroundColor: 'var(--accent-blue)',
              boxShadow: '0 0 8px var(--accent-blue)' 
            }}></span>
             <span style={{ fontFamily: 'monospace', letterSpacing: '0.5px' }}>{selectedModel}</span>
            {showUpdated && (
              <span style={{ 
                fontSize: '9px', 
                color: '#10b981', 
                backgroundColor: 'rgba(16, 185, 129, 0.1)', 
                border: '1px solid rgba(16, 185, 129, 0.2)',
                borderRadius: '3px',
                padding: '1px 4px',
                marginLeft: '8px',
                fontWeight: 'bold',
                fontFamily: 'monospace'
              }}>
                UPDATED
              </span>
            )}
          </div>
          <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>▲</span>
        </div>

        {/* Dropup list */}
        {isModelDropdownOpen && (
          <div style={{
            position: 'absolute',
            bottom: '100%',
            left: '16px',
            right: '16px',
            backgroundColor: '#131316',
            border: '1px solid var(--border-color)',
            borderRadius: '6px',
            marginBottom: '6px',
            zIndex: 1000,
            boxShadow: '0 -8px 24px rgba(0, 0, 0, 0.6)',
            maxHeight: '220px',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            padding: '4px 0',
            scrollbarWidth: 'thin'
          }}>
            <div style={{
              padding: '8px 12px 6px 12px',
              fontSize: '9px',
              fontWeight: 'bold',
              color: 'var(--text-muted)',
              letterSpacing: '1.2px',
              borderBottom: '1px solid rgba(255,255,255,0.05)',
              marginBottom: '4px'
            }}>
              MODEL
            </div>
            
            {modelsList.map((model) => {
              const isSelected = model.name === selectedModel;
              return (
                <div
                  key={model.name}
                  onClick={() => {
                    onSelectModel(model.name);
                    setIsModelDropdownOpen(false);
                  }}
                  className={`model-dropdown-item ${isSelected ? 'selected' : ''}`}
                  style={{
                    padding: '8px 12px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    fontSize: '12px',
                    color: isSelected ? 'var(--accent-green)' : 'var(--text-main)',
                    fontWeight: isSelected ? 600 : 400,
                    transition: 'all 0.2s ease',
                    fontFamily: 'monospace'
                  }}
                >
                  <span style={{
                    fontSize: '11px',
                    color: isSelected ? 'var(--accent-green)' : 'var(--text-main)',
                    transition: 'color 0.2s ease'
                  }}>{model.name}</span>
                  {model.badge && (
                    <span style={{
                      fontSize: '9px',
                      padding: '1px 5px',
                      borderRadius: '4px',
                      backgroundColor: 'rgba(255,255,255,0.05)',
                      color: 'var(--text-muted)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      marginLeft: '6px'
                    }}>
                      {model.badge}
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Tiny Status / Utility Row at Sidebar Bottom */}
      <div style={{
        display: 'flex',
        borderTop: '1px solid var(--border-color)',
        padding: '8px 16px',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.15)',
        flexShrink: 0
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          fontSize: '11px',
          color: 'var(--text-muted)',
          cursor: 'pointer'
        }}
        onClick={triggerMcpRefresh}
        onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-blue)'}
        onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
        >
          <RefreshCw size={11} />
          <span>Refresh MCPs</span>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          fontSize: '11px',
          color: 'var(--text-muted)',
          cursor: 'pointer'
        }}
        onClick={triggerModelUsage}
        onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-green)'}
        onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
        >
          <BarChart2 size={11} />
          <span>Model Limits</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
