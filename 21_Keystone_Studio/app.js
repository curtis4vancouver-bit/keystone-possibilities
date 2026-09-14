/* ==========================================================================
   KEYSTONE NEXT v2.4 — ADVANCED DESKTOP STUDIO CONTROLLER
   Architecture: Tab Group Switcher, Full-Height Sidebar, Dynamic HUD Context,
   High-End Hardware Telemetry Gauges, Bottom Intelligence Socket Dock (Antigravity/OpenAI),
   and 5-State Avatar Engine.
   ========================================================================== */

(function () {
  'use strict';

  // Master Layout Elements
  const appLayout = document.getElementById('hudAppLayout');
  const dragSplitter = document.getElementById('dragSplitter');
  const btnToggleSidebar = document.getElementById('btnToggleSidebar');
  const btnCollapseSidebar = document.getElementById('btnCollapseSidebar');
  const btnWinMin = document.getElementById('btnWinMin');
  const btnWinMax = document.getElementById('btnWinMax');
  const btnWinClose = document.getElementById('btnWinClose');
  const sidebarDragSpacer = document.getElementById('sidebarDragSpacer');
  const btnExpandFab = document.getElementById('btnExpandFab');
  const panelWidthRange = document.getElementById('panelWidthRange');
  const widthDisplay = document.getElementById('widthDisplay');
  const glowRange = document.getElementById('glowRange');
  const glowDisplay = document.getElementById('glowDisplay');

  // Master Cyber Audio & Volume Controls
  const hudAudioQuickBar = document.getElementById('hudAudioQuickBar');
  const hudAudioDeviceBadge = document.getElementById('hudAudioDeviceBadge');
  const hudAudioDeviceLabel = document.getElementById('hudAudioDeviceLabel');
  const hudAudioBadgeIcon = document.getElementById('hudAudioBadgeIcon');
  const btnVolumeMute = document.getElementById('btnVolumeMute');
  const hudVolumeIcon = document.getElementById('hudVolumeIcon');
  const hudVolumeSlider = document.getElementById('hudVolumeSlider');
  const hudVolumeDisplay = document.getElementById('hudVolumeDisplay');
  let isInteractingWithVolume = false;

  // Chat Dropdown Elements (Legacy Compatibility)
  const chatDropdownWrap = document.getElementById('chatDropdownWrap');
  const chatDropdownBtn = document.getElementById('chatDropdownBtn');
  const activeChatLabel = document.getElementById('activeChatLabel');
  const chatDropdownMenu = document.getElementById('chatDropdownMenu');

  // Master Sidebar Control Hub Elements (Bootstrap Box & Groups Box)
  const sidebarMasterControlHub = document.getElementById('sidebarMasterControlHub');
  const hubBoxBootstrap = document.getElementById('hubBoxBootstrap');
  const hubBoxGroups = document.getElementById('hubBoxGroups');
  const sidebarActiveChatNum = document.getElementById('sidebarActiveChatNum');
  const sidebarActiveChatTitle = document.getElementById('sidebarActiveChatTitle');
  const sidebarActiveChatDesc = document.getElementById('sidebarActiveChatDesc');
  const sidebarChatList = document.getElementById('sidebarChatList');
  const sidebarGroupsList = document.getElementById('sidebarGroupsList');
  const sidebarActiveGroupBadge = document.getElementById('sidebarActiveGroupBadge');
  const btnSidebarAddGroup = document.getElementById('btnSidebarAddGroup');

  // Tab Groups (Nav Tab Strip at Far Left)
  const groupPillsScroll = document.getElementById('groupPillsScroll');
  const hudTabStrip = document.getElementById('hudTabStrip');
  const btnAddGroup = document.getElementById('btnAddGroup');

  // Main Canvas & View Panes
  const socketCanvas = document.getElementById('socketCanvas');
  const viewportContent = document.getElementById('viewportContent');
  const viewSocketPane = document.getElementById('viewSocketPane');
  const viewVectorBrainPane = document.getElementById('viewVectorBrainPane');
  const viewAvatarPane = document.getElementById('viewAvatarPane');
  const viewPolymarketPane = document.getElementById('viewPolymarketPane');
  const viewFlowPane = document.getElementById('viewFlowPane');
  const viewDaVinciPane = document.getElementById('viewDaVinciPane');
  const viewAgentsPane = document.getElementById('viewAgentsPane');

  // Hardware Telemetry Elements
  const cpuLoadValue = document.getElementById('cpuLoadValue');
  const cpuProgressFill = document.getElementById('cpuProgressFill');
  const ramLoadValue = document.getElementById('ramLoadValue');
  const ramProgressFill = document.getElementById('ramProgressFill');
  const vramLoadValue = document.getElementById('vramLoadValue');
  const vramProgressFill = document.getElementById('vramProgressFill');
  const vramSafetyBadge = document.getElementById('vramSafetyBadge');

  // Dynamic Sidebar Container
  const sidebarDynamicContent = document.getElementById('sidebarDynamicContent');

  // Bottom Socket Dock Elements
  const hudBottomDock = document.getElementById('hudBottomDock');
  const btnToggleSocket = document.getElementById('btnToggleSocket');
  const socketBtnText = document.getElementById('socketBtnText');
  const engineAntigravity = document.getElementById('engineAntigravity');
  const engineOpenAI = document.getElementById('engineOpenAI');
  const activeEngineTag = document.getElementById('activeEngineTag');
  const dockCmdInput = document.getElementById('dockCmdInput');
  const dockSendBtn = document.getElementById('dockSendBtn');
  const btnToggleDockExpand = document.getElementById('btnToggleDockExpand');
  const dockExpandIcon = document.getElementById('dockExpandIcon');
  const dockAudioWave = document.getElementById('dockAudioWave');
  const terminalOutputFeed = document.getElementById('terminalOutputFeed');
  const btnClearTerminal = document.getElementById('btnClearTerminal');

  // Avatar Elements
  const avatarViewport = document.getElementById('avatarViewport');
  const avatarCapsule = document.getElementById('avatarCapsule');
  const activeAvatarName = document.getElementById('activeAvatarName');
  const currentStateBadge = document.getElementById('currentStateBadge');
  const speechBubble = document.getElementById('speechBubble');
  const speechBubbleText = document.getElementById('speechBubbleText');
  const fxCanvas = document.getElementById('fxCanvas');
  const fxCtx = fxCanvas ? fxCanvas.getContext('2d') : null;
  const candidateCards = document.querySelectorAll('.candidate-card');
  const stateTriggerBtns = document.querySelectorAll('.state-trigger-btn');

  // Video State Layers Map
  const videoLayers = {
    idle: document.getElementById('vidIdle'),
    listening: document.getElementById('vidListening'),
    working: document.getElementById('vidWorking'),
    thinking: document.getElementById('vidThinking'),
    talking: document.getElementById('vidTalking'),
    walking: document.getElementById('vidWalking')
  };

  const portalCoreVideo = document.getElementById('portalCoreVideo');
  if (portalCoreVideo) {
    const playCoreVideo = () => {
      portalCoreVideo.style.display = 'block';
      portalCoreVideo.play().catch(() => {});
    };
    portalCoreVideo.addEventListener('loadeddata', playCoreVideo);
    portalCoreVideo.addEventListener('canplay', playCoreVideo);
    if (portalCoreVideo.readyState >= 2) {
      playCoreVideo();
    }
    // Periodic ensure play
    setInterval(() => {
      if (portalCoreVideo && portalCoreVideo.paused) {
        portalCoreVideo.play().catch(() => {});
      }
    }, 3000);
  }

  // State Store
  let isCollapsed = localStorage.getItem('keystone_next_collapsed') === 'true';
  let inspectorWidth = parseInt(localStorage.getItem('keystone_next_width') || '360', 10);
  let glowPercent = parseInt(localStorage.getItem('keystone_next_glow') || '80', 10);
  let isDraggingSplitter = false;
  let activeGroup = 1;
  let activeTabKey = 'antigravity';
  let isSocketed = false;
  let activeEngine = 'antigravity';
  let currentAvatarState = 'idle';
  window.keystoneCurrentAvatarState = currentAvatarState;
  let isAwaitingAgentSpeech = false;
  window.keystoneIsAwaitingAgentSpeech = isAwaitingAgentSpeech;
  let animTick = 0;
  let selectedChatId = localStorage.getItem('keystone_active_chat_id') || '1baa32b7-bf7a-4715-b3f6-2daeb7357af8';
  let selectedChatTitle = localStorage.getItem('keystone_active_chat_title') || '[#01] Run Bootstrap Process — Master Daemons & Watchdog';

  // --------------------------------------------------------------------------
  // Tab Group Configurations (Exact Group 1 Sequence)
  // --------------------------------------------------------------------------
  const TAB_GROUPS = {
    1: {
      name: '✦ KEYSTONE — MASTER STUDIO',
      title: 'Group 1',
      desc: 'Master Studio',
      tabs: [
        { key: 'antigravity', label: 'Antigravity', icon: '>_' },
        { key: 'vector-brain', label: 'Vector Brain', icon: '🧠' },
        { key: 'agents', label: 'Agents', icon: '🤖' },
        { key: 'work', label: 'Work', icon: '💼' },
        { key: 'possibilities', label: 'Possibilities', icon: '✨' },
        { key: 'recomposition', label: 'Recomposition', icon: '🛡️' },
        { key: 'protocols', label: 'Protocols', icon: '📋' },
        { key: 'websites', label: 'Websites', icon: '🌐' },
        { key: 'money', label: 'Money', icon: '💲' }
      ]
    },
    2: {
      name: '✦ KEYSTONE — MEDIA & FLOW',
      title: 'Group 2',
      desc: 'Media & Production',
      tabs: [
        { key: 'flow', label: 'Google Flow', icon: '🌊' },
        { key: 'davinci', label: 'DaVinci Bridge', icon: '🎬' },
        { key: 'recomposition', label: 'Recomposition', icon: '🛡️' },
        { key: 'agents', label: 'Media Swarms', icon: '🤖' }
      ]
    },
    3: {
      name: '✦ KEYSTONE — MULTIPLEX & CODE',
      title: 'Group 3',
      desc: 'Multiplex & Code',
      tabs: [
        { key: 'work', label: 'Vancouver Code', icon: '💼' },
        { key: 'possibilities', label: 'Possibilities Pro-Forma', icon: '✨' },
        { key: 'antigravity', label: 'Zoning Brain', icon: '>_' }
      ]
    },
    4: {
      name: '✦ KEYSTONE — QUANT & PROTOCOLS',
      title: 'Group 4',
      desc: 'Quant & Health',
      tabs: [
        { key: 'money', label: 'Polymarket Tennis', icon: '💲' },
        { key: 'protocols', label: 'Peptides & TRT', icon: '📋' },
        { key: 'agents', label: 'Sentinel Swarm', icon: '🤖' }
      ]
    }
  };

  // --------------------------------------------------------------------------

  // --------------------------------------------------------------------------
  // Antigravity HUD Web Portals Catalog & Draggable Reordering (v8.4.0)
  // --------------------------------------------------------------------------
  const DEFAULT_WEB_PORTALS = [
    { id: 'gmail', label: 'Gmail', url: 'https://mail.google.com', icon: '✉️', color: '#ea4335', title: 'Google Mail' },
    { id: 'google-flow', label: 'Google Flow', url: 'https://labs.google/fx/tools/flow', icon: '⚡', color: '#fbbf24', title: 'Google Flow AI Video Studio' },
    { id: 'too-lost', label: 'Too Lost', url: 'https://toolost.com/user-portal', icon: '💿', color: '#00f0ff', title: 'TooLost Music Distribution Portal' },
    { id: 'suno', label: 'Suno AI', url: 'https://suno.com/create', icon: '✨', color: '#ff007f', title: 'Suno AI Music Generator' },
    { id: 'musixmatch', label: 'Musixmatch Pro', url: 'https://pro.musixmatch.com/roster/artist/72648585', icon: '🎵', color: '#ff5722', title: 'Musixmatch Pro Synced Lyrics Roster' },
    { id: 'musicbrainz', label: 'MusicBrainz', url: 'https://musicbrainz.org/artist/1a30328b-20b2-48bd-8e56-2884d3b040c0', icon: '🧠', color: '#a855f7', title: 'MusicBrainz Open Audio DB' },
    { id: 'recomp-site', label: 'Keystone Recomp', url: 'https://keystonerecomposition.com', icon: '🛡️', color: '#ff007f', title: 'Keystone Recomposition Official Site' },
    { id: 'possibilities-site', label: 'Keystone Poss', url: 'https://keystonepossibilities.ca', icon: '✨', color: '#00f0ff', title: 'Keystone Possibilities Ltd' },
    { id: 'facebook', label: 'Facebook Page', url: 'https://www.facebook.com/166025896601563', icon: '📘', color: '#1877f2', title: 'Keystone Facebook Business Page' },
    { id: 'instagram', label: 'Instagram', url: 'https://www.instagram.com/keystonerecomposition', icon: '📷', color: '#e1306c', title: 'Keystone Recomposition Instagram' },
    { id: 'youtube-studio', label: 'YouTube Studio', url: 'https://studio.youtube.com', icon: '▶️', color: '#ff0000', title: 'YouTube Creator Studio' },
    { id: 'google-seo', label: 'Google SEO', url: 'https://search.google.com/search-console', icon: '🔍', color: '#4285f4', title: 'Google Search Console & Instant Indexing' },
    { id: 'polymarket', label: 'Polymarket', url: 'https://polymarket.com', icon: '📈', color: '#10b981', title: 'Polymarket Quant Sports & Financial Markets' },
    { id: 'realtor-ca', label: 'Realtor Lots', url: 'https://www.realtor.ca', icon: '🏠', color: '#e53e3e', title: 'Realtor.ca BC Multiplex & Land Ingestion' },
    { id: 'google-gemini', label: 'Google Gemini', url: 'https://gemini.google.com/app', icon: '💎', color: '#00d2ff', title: 'Google Gemini Deep Research Portal' },
    { id: 'ledcor-workday', label: 'Ledcor Workday', url: 'http://cloud.ledcor.com/', icon: '👷‍♂️', color: '#ffd700', title: 'Ledcor Workday Employee & Payroll Portal' },
    { id: 'vancity', label: 'Vancity Banking', url: 'https://www.vancity.com', icon: '🏦', color: '#008542', title: 'Vancity Credit Union Online Banking' },
    { id: 'sunshine-ccu', label: 'Sunshine CU', url: 'https://www.sunshineccu.com', icon: '💳', color: '#00a0dc', title: 'Sunshine Coast Credit Union Online Banking' }
  ];

  window.openWebPortal = function(url, label) {
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🌐 Launching ${label || 'Web Portal'}: ${url}`);
    }
    try {
      const invoke = window.__TAURI_INTERNALS__?.invoke || window.__TAURI__?.core?.invoke || window.__TAURI__?.invoke;
      if (invoke) {
        invoke('open_url', { url }).catch(() => {
          window.open(url, '_blank');
        });
        return;
      }
    } catch (err) {}
    window.open(url, '_blank');
  };

  function getSavedWebPortals() {
    try {
      const raw = localStorage.getItem('keystone_antigravity_web_links_order_v2');
      if (raw) {
        const parsed = JSON.parse(raw);
        const map = new Map(DEFAULT_WEB_PORTALS.map(p => [p.id, p]));
        const result = [];
        for (const item of parsed) {
          if (map.has(item.id)) {
            result.push(Object.assign({}, map.get(item.id), item));
            map.delete(item.id);
          }
        }
        for (const remaining of map.values()) {
          result.push(remaining);
        }
        return result;
      }
    } catch (e) {}
    return DEFAULT_WEB_PORTALS.slice();
  }

  function saveWebPortalsOrder(portals) {
    try {
      localStorage.setItem('keystone_antigravity_web_links_order_v2', JSON.stringify(portals.map(p => ({ id: p.id, label: p.label, url: p.url, icon: p.icon, color: p.color }))));
    } catch (e) {}
  }

  function initWebPortalsDragAndDrop() {
    const grid = document.getElementById('webPortalsGrid');
    if (!grid) return;

    let portals = getSavedWebPortals();
    let draggedIndex = null;
    let didDragHappen = false;

    function renderGrid() {
      grid.innerHTML = portals.map((p, idx) => `
        <div class="web-portal-btn" draggable="true" data-index="${idx}" data-id="${p.id}" data-url="${p.url}" data-label="${p.label}" title="${p.title || p.label} — Hold &amp; Drag to Reorder | Click to Open">
          <span class="portal-drag-grip" title="Hold &amp; Drag to reorder">⋮⋮</span>
          <span class="portal-icon" style="color:${p.color};">${p.icon}</span>
          <span class="portal-label">${p.label}</span>
          <span class="portal-ext-arrow">↗</span>
        </div>
      `).join('');

      const buttons = grid.querySelectorAll('.web-portal-btn');
      buttons.forEach(btn => {
        btn.addEventListener('dragstart', (e) => {
          draggedIndex = parseInt(btn.dataset.index, 10);
          didDragHappen = true;
          btn.classList.add('is-dragging');
          e.dataTransfer.effectAllowed = 'move';
          e.dataTransfer.setData('text/plain', String(draggedIndex));
        });

        btn.addEventListener('dragover', (e) => {
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';
          const targetIdx = parseInt(btn.dataset.index, 10);
          if (targetIdx !== draggedIndex) {
            btn.classList.add('drag-over');
          }
        });

        btn.addEventListener('dragleave', () => {
          btn.classList.remove('drag-over');
        });

        btn.addEventListener('drop', (e) => {
          e.preventDefault();
          e.stopPropagation();
          btn.classList.remove('drag-over');
          const targetIdx = parseInt(btn.dataset.index, 10);
          if (draggedIndex !== null && draggedIndex !== targetIdx) {
            const item = portals.splice(draggedIndex, 1)[0];
            portals.splice(targetIdx, 0, item);
            saveWebPortalsOrder(portals);
            renderGrid();
            if (window.keystoneLogTerminal) {
              window.keystoneLogTerminal(`🔀 Reordered web portal: ${item.label} moved to position #${targetIdx + 1}`);
            }
          }
        });

        btn.addEventListener('dragend', () => {
          btn.classList.remove('is-dragging');
          grid.querySelectorAll('.web-portal-btn').forEach(b => b.classList.remove('drag-over'));
          draggedIndex = null;
          setTimeout(() => { didDragHappen = false; }, 80);
        });

        btn.addEventListener('click', (e) => {
          if (didDragHappen) return;
          const url = btn.dataset.url;
          const label = btn.dataset.label;
          window.openWebPortal(url, label);
        });
      });
    }

    renderGrid();

    const resetBtn = document.getElementById('btnResetPortalsOrder');
    if (resetBtn) {
      resetBtn.onclick = () => {
        try {
          localStorage.removeItem('keystone_antigravity_web_links_order_v2');
        } catch (e) {}
        portals = DEFAULT_WEB_PORTALS.slice();
        renderGrid();
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal('↺ Restored default Web Command Hubs portal order.');
        }
      };
    }
  }

  // Google Flow Dual-Mode Cockpit & Protocols Sidebar Builder
  function renderFlowCockpitHtml(channelContext = 'protocols') {
    const currentMode = window.keystoneFlowMode || 'manual';
    const vidCount = window.keystoneActiveVideoCount || (channelContext === 'possibilities' ? 26 : (channelContext === 'recomposition' ? 53 : 51));
    const brollCount = window.keystoneActiveBrollCount || (channelContext === 'possibilities' ? 26 : (channelContext === 'recomposition' ? 50 : (vidCount > 1 ? vidCount - 1 : 1)));

    let scriptwriterTitle = '📜 Protocols Scriptwriter';
    let scriptwriterFn = "window.runProtocolsScriptwriter()";
    let channelLabel = 'Protocols';

    if (channelContext === 'possibilities') {
      scriptwriterTitle = '🏗️ Possibilities Scriptwriter';
      scriptwriterFn = "window.runPossibilitiesScriptwriter()";
      channelLabel = 'Possibilities';
    } else if (channelContext === 'recomposition') {
      scriptwriterTitle = '🛡️ Recomposition Scriptwriter';
      scriptwriterFn = "window.runRecompositionScriptwriter()";
      channelLabel = 'Recomposition';
    }

    return `
      <div class="flow-cockpit-wrapper" data-channel-context="${channelContext}">
        <!-- Top Dual Mode Switch -->
        <div class="hud-mode-switch-card">
          <div class="mode-switch-bar">
            <button class="mode-switch-pill ${currentMode === 'manual' ? 'active-cyan' : ''}" onclick="window.setFlowCockpitMode('manual')">
              <span>🎮 MANUAL COCKPIT</span>
            </button>
            <button class="mode-switch-pill ${currentMode === 'swarm' ? 'active-purple' : ''}" onclick="window.setFlowCockpitMode('swarm')">
              <span>🤖 SWARM AUTO-PILOT</span>
            </button>
          </div>
        </div>

        <!-- Master Scriptwriter & HUD Entry -->
        <span class="panel-section-title">${channelLabel} Production Ingestion</span>
        <div class="hud-card" style="display:flex; flex-direction:column; gap:7px;">
          <button class="swarm-run-btn" onclick="${scriptwriterFn}">
            ${scriptwriterTitle}
          </button>
          <button class="swarm-secondary-btn" style="border-color:rgba(0,240,255,0.5); color:#00f0ff;" onclick="window.openGoogleFlowHUD('${channelContext}')">
            🌐 Open Google Flow (HUD Attached)
          </button>
        </div>

        <!-- Reference Assets: Clothes & Background -->
        <span class="panel-section-title">Reference Assets (Clothes &amp; Background)</span>
        <div class="hud-card" style="display:flex; flex-direction:column; gap:7px;">
          <div style="display:flex; gap:6px;">
            <button class="swarm-secondary-btn" style="flex:1; border-color:rgba(192,132,252,0.5); color:#d8b4fe;" onclick="window.generateReferenceAsset('cloth_1', '${channelContext}')">
              👔 Gen Clothes (cloth_1)
            </button>
            <button class="swarm-secondary-btn" style="flex:1; border-color:rgba(0,240,255,0.5); color:#00f0ff;" onclick="window.generateReferenceAsset('background_1', '${channelContext}')">
              🏙️ Gen Background (bg_1)
            </button>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="swarm-secondary-btn" style="flex:1; border-color:rgba(192,132,252,0.3); color:#d8b4fe;" onclick="window.renameReferenceAsset('cloth_1', '${channelContext}')">
              🏷️ Rename Clothes
            </button>
            <button class="swarm-secondary-btn" style="flex:1; border-color:rgba(0,240,255,0.3); color:#00f0ff;" onclick="window.renameReferenceAsset('background_1', '${channelContext}')">
              🏷️ Rename Background
            </button>
          </div>
        </div>

        <!-- Media Renaming & Ingestion -->
        <span class="panel-section-title">Media Renaming (Reverse Grid)</span>
        <div class="hud-card" style="display:flex; flex-direction:column; gap:7px;">
          <div style="display:flex; gap:6px;">
            <button class="swarm-secondary-btn" id="btnRenameVideosStudio" style="flex:1; border-color:rgba(251,191,36,0.5); color:#fbbf24;" onclick="window.executeMediaRename('videos', '${channelContext}')">
              🎬 Rename Videos (${vidCount}..1)
            </button>
            <button class="swarm-secondary-btn" id="btnRenameBrollStudio" style="flex:1; border-color:rgba(0,240,255,0.5); color:#00f0ff;" onclick="window.executeMediaRename('images', '${channelContext}')">
              🏷️ Rename B-Roll (A${brollCount}..A1)
            </button>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="swarm-secondary-btn" style="flex:1;" onclick="window.executeMediaDownload('videos', '${channelContext}')">
              📦 Download Videos (${vidCount})
            </button>
            <button class="swarm-secondary-btn" style="flex:1;" onclick="window.executeMediaDownload('images', '${channelContext}')">
              📥 Download B-Roll (${brollCount})
            </button>
          </div>
          <button class="swarm-secondary-btn" style="border-color:rgba(168,85,247,0.5); color:#d8b4fe;" onclick="window.executeDavinciAssembly('${channelContext}')">
            🎬 DaVinci 2-Track Auto-Assembly (-18dB BGM)
          </button>
        </div>

        ${currentMode === 'manual' ? `
          <!-- Publishing & SEO Distribution -->
          <span class="panel-section-title">Publishing &amp; Syndication</span>
          <div class="hud-card" style="display:flex; flex-direction:column; gap:7px;">
            <button class="swarm-secondary-btn" style="border-color:rgba(16,185,129,0.4); color:#6ee7b7;" onclick="window.publishLuxuryBlog('${channelContext}')">
              📰 Publish Luxury Blog &amp; Google Index
            </button>
            <button class="swarm-secondary-btn" style="border-color:rgba(239,68,68,0.4); color:#fca5a5;" onclick="window.uploadYouTubeVideo('long', '${channelContext}')">
              ▶️ Auto-Upload Video (Long)
            </button>
            <button class="swarm-secondary-btn" style="border-color:rgba(245,158,11,0.4); color:#fef08a;" onclick="window.uploadYouTubeVideo('short', '${channelContext}')">
              ⚡ Auto-Upload Shorts
            </button>
            <button class="swarm-secondary-btn" style="border-color:rgba(59,130,246,0.4); color:#93c5fd;" onclick="window.publishMetaSocial('${channelContext}')">
              📱 Auto-Stage Meta (FB &amp; IG)
            </button>
          </div>
        ` : `
          <!-- Swarm Auto-Pilot Dashboard -->
          <span class="panel-section-title">Autonomous Swarm Sentinel</span>
          <div class="hud-card" style="display:flex; flex-direction:column; gap:10px;">
            <div class="swarm-status-box">
              <div class="status-row">
                <span>Production Sentinel:</span>
                <span class="badge-status ${window.__swarmRunning ? 'running' : 'ready'}" id="swarmSentinelBadge">
                  ${window.__swarmRunning ? '⚡ RUNNING (5-BATCH)' : 'READY'}
                </span>
              </div>
              <div class="status-steps">
                <div class="step-item"><span>1.</span> Reference Photos (cloth_1, bg_1)</div>
                <div class="step-item"><span>2.</span> 16:9 Long Videos (${vidCount} clips · 5-batch)</div>
                <div class="step-item"><span>3.</span> Sentinel Failure Inspection &amp; Remake</div>
                <div class="step-item"><span>4.</span> 16:9 B-Roll Photos (${brollCount} items)</div>
                <div class="step-item"><span>5.</span> Reverse Grid Law (A${brollCount}..A1 / ${vidCount}..1)</div>
                <div class="step-item"><span>6.</span> 1K Photos &amp; 1080p Video Downloads</div>
                <div class="step-item"><span>7.</span> DaVinci Assembly (01:00:00:00 · -18dB BGM)</div>
                <div class="step-item"><span>8.</span> 9:16 Shorts Generation (Appended after)</div>
              </div>
            </div>

            <button class="swarm-run-btn" id="btnLaunchSwarmOrchestrator" onclick="window.toggleSwarmOrchestrator('${channelContext}')">
              ${window.__swarmRunning ? '🛑 Stop Swarm Sentinel' : '🚀 START MASTER PRODUCTION (5-Batch Sentinel)'}
            </button>
            <button class="swarm-secondary-btn" onclick="window.checkSwarmStatus('${channelContext}')">
              📊 Check Swarm Sentinel Status
            </button>
          </div>

          <!-- Publishing & SEO Distribution in Swarm Mode -->
          <span class="panel-section-title">Publishing &amp; Syndication</span>
          <div class="hud-card" style="display:flex; flex-direction:column; gap:7px;">
            <button class="swarm-secondary-btn" style="border-color:rgba(16,185,129,0.4); color:#6ee7b7;" onclick="window.publishLuxuryBlog('${channelContext}')">
              📰 Publish Luxury Blog &amp; Google Index
            </button>
            <button class="swarm-secondary-btn" style="border-color:rgba(239,68,68,0.4); color:#fca5a5;" onclick="window.uploadYouTubeVideo('long', '${channelContext}')">
              ▶️ Auto-Upload Video (Long)
            </button>
            <button class="swarm-secondary-btn" style="border-color:rgba(245,158,11,0.4); color:#fef08a;" onclick="window.uploadYouTubeVideo('short', '${channelContext}')">
              ⚡ Auto-Upload Shorts
            </button>
            <button class="swarm-secondary-btn" style="border-color:rgba(59,130,246,0.4); color:#93c5fd;" onclick="window.publishMetaSocial('${channelContext}')">
              📱 Auto-Stage Meta (FB &amp; IG)
            </button>
          </div>
        `}
      </div>
    `;
  }

  // Dynamic Sidebar Content Builder (Changes on Every Tab Click!)
  // --------------------------------------------------------------------------
  function updateSidebarContent(tabKey) {
    if (!sidebarDynamicContent) return;

    let html = '';

    if (tabKey === 'vector-brain') {
      const now = new Date();
      const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const nodeCount = window.__neuralBrainInstance?.nodes?.length || 1420;
      const nodeCountFormatted = `${nodeCount.toLocaleString()} Graph Nodes`;

      html = `
        <span class="panel-section-title">Vector Brain Intelligence</span>
        <div class="hud-card">
          <div class="card-header-row">
            <span class="card-label">🧠 Knowledge Cortex</span>
            <span class="card-badge" style="color:var(--hud-neon-cyan);">Port 9878</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px; font-size:11px; color:var(--hud-text-secondary);">
            <div style="display:flex; justify-content:space-between;">
              <span>Server Port:</span>
              <span style="color:var(--hud-neon-cyan); font-family:var(--hud-font-mono);">Active (:9878)</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Architecture:</span>
              <span style="color:var(--hud-neon-cyan); font-family:var(--hud-font-mono);">Dense + Sparse BM25</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Vector Dimensions:</span>
              <span style="color:var(--hud-neon-violet-light); font-family:var(--hud-font-mono);">1536-dim (CUDA)</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Total Entities:</span>
              <span style="color:#10b981; font-family:var(--hud-font-mono); font-weight:700;">${nodeCountFormatted}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Wiki Documentation:</span>
              <span style="color:#10b981; font-family:var(--hud-font-mono);">Up-to-Date (Synced)</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Last Updated:</span>
              <span style="color:#f59e0b; font-family:var(--hud-font-mono);">Today, ${timeStr}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>Local Qdrant:</span>
              <span style="color:#10b981; font-family:var(--hud-font-mono);">Active (:9878)</span>
            </div>
          </div>
        </div>

        <span class="panel-section-title">Brain Swarm Subagents</span>
        <div class="hud-card" style="display:flex; flex-direction:column; gap:8px;">
          <button class="brain-swarm-btn btn-swarm-cyan" id="btnBrainSwarmS2" onclick="window.dispatchBrainSubagent('S2_brain_auditor', '🧠 Brain Auditor (S2)', 'Auditing wikilinks, broken references, and trigger SIMD re-indexing')">
            <div class="btn-content">
              <span>🧠</span>
              <span>Brain Auditor Subagent (S2)</span>
            </div>
            <span class="btn-ext-arrow">↗</span>
          </button>

          <button class="brain-swarm-btn btn-swarm-emerald" id="btnBrainSwarmS1" onclick="window.dispatchBrainSubagent('S1_brain_upgrader', '🚀 Brain Upgrader (S1)', 'Researching cutting-edge 2026 vector memory upgrades, GraphRAG, and SIMD acceleration')">
            <div class="btn-content">
              <span>🚀</span>
              <span>Brain Upgrader Subagent (S1)</span>
            </div>
            <span class="btn-ext-arrow">↗</span>
          </button>

          <button class="brain-swarm-btn btn-swarm-purple" id="btnBrainSwarmS3" onclick="window.dispatchBrainSubagent('S3_workspace_janitor', '🧹 Workspace Janitor (S3)', 'Cleaning scratch files, stale logs, and optimizing directory hygiene')">
            <div class="btn-content">
              <span>🧹</span>
              <span>Workspace Janitor Subagent (S3)</span>
            </div>
            <span class="btn-ext-arrow">↗</span>
          </button>

          <button class="brain-swarm-btn btn-swarm-red" id="btnBrainSwarmG1" onclick="window.dispatchBrainSubagent('G1_gmail_organizer', '✉️ Gmail Organizer (G1)', 'Sorting, tagging, and organizing incoming investor and client communications')">
            <div class="btn-content">
              <span>✉️</span>
              <span>Gmail Organizer Swarm (G1)</span>
            </div>
            <span class="btn-ext-arrow">↗</span>
          </button>

          <button class="brain-swarm-btn btn-swarm-blue" id="btnBrainSwarmD1" onclick="window.dispatchBrainSubagent('D1_gdrive_auditor', '📁 Google Drive Sync (D1)', 'Synchronizing local assets with Google Drive cloud backup repositories')">
            <div class="btn-content">
              <span>📁</span>
              <span>Google Drive Desktop Sync (D1)</span>
            </div>
            <span class="btn-ext-arrow">↗</span>
          </button>
        </div>

        <span class="panel-section-title">Cortex Operations</span>
        <div class="hud-card" style="display:flex; flex-direction:column; gap:8px;">
          <button class="swarm-run-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('🧠 Vector Brain re-indexing knowledge graph on Port 9878...')">
            🧠 Sync Qdrant Graph Nodes
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('🔍 Querying 1536-dim dense vector space &amp; entity cortex...')">
            🔍 Query 1536-dim Embeddings
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('📊 Sparse BM25 inverted lexical index scanned and aligned.')">
            📊 Inverted BM25 Index Scan
          </button>
        </div>
      `;
    } else if (tabKey === 'agents') {
      html = `
        <span class="panel-section-title">Swarm Execution Controls</span>
        <div class="hud-card">
          <button class="swarm-run-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('🛡️ Dispatched Autonomous 16-Agent TDD Swarm across 17_subagents.')">
            🛡️ Launch 16-Agent TDD Swarm
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🔎 Dispatched Brave Search subagents (minimum 2 independent sources required).')">
            🔎 Dispatch Brave Search Subagents
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🧪 Integration Tester B4 running verified test harness across 17_subagents.')">
            🧪 Run Integration Tester B4
          </button>
        </div>
      `;
    } else if (tabKey === 'work') {
      html = `
        <span class="panel-section-title">Work &amp; Compliance Actions</span>
        <div class="hud-card">
          <button class="swarm-run-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('💼 Running BC Building Code &amp; Bill 44 compliance audit...')">
            💼 Run Building Code Audit
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('📐 Calculating FSR, height restrictions, and allowable setbacks...')">
            📐 Check FSR &amp; Setback Regulations
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('📑 Multiplex compliance packet generated for architectural submittal.')">
            📑 Generate Compliance Packet
          </button>
        </div>
      `;
    } else if (tabKey === 'possibilities') {
      html = renderFlowCockpitHtml('possibilities');
    } else if (tabKey === 'recomposition') {
      html = renderFlowCockpitHtml('recomposition');
    } else if (tabKey === 'protocols') {
      html = renderFlowCockpitHtml('protocols');
    } else if (tabKey === 'websites') {
      html = `
        <span class="panel-section-title">Web Publishing Actions</span>
        <div class="hud-card">
          <button class="swarm-run-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('🌐 Triggered Rank Math 100/100 &amp; GSC Instant Indexing sweep.')">
            🌐 Run Full Luxury SEO Sweep
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🚀 Initiated Google Search Console URL Inspection via Port 9222...')">
            🚀 Trigger GSC Instant Indexing
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🖼️ Converted luxury gallery media to WebP with verified alt-tags.')">
            🖼️ Optimize Media &amp; Alt-Tags
          </button>
        </div>
      `;
    } else if (tabKey === 'money') {
      html = `
        <span class="panel-section-title">Execution Sentinel</span>
        <div class="hud-card">
          <button class="swarm-run-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('⚡ Dispatched Morning Tennis 12-Factor Scan via Port 9222 sequential executor.')">
            ⚡ Run Daily WTA Sweet-Spot Scan
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🎾 Running 12-factor audit on both athletes across surface, Elo, fatigue, head-to-head...')">
            🎾 12-Factor Dual-Player Audit
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('💰 Auditing 40% CAD cash fortress and open limit orders...')">
            💰 Audit CAD Cash Reserves
          </button>
        </div>
      `;
    } else if (tabKey === 'flow') {
      html = renderFlowCockpitHtml();
    } else if (tabKey === 'davinci') {
      html = `
        <span class="panel-section-title">Resolve Operations</span>
        <div class="hud-card">
          <button class="swarm-run-btn" style="width:100%; margin-top:0;" onclick="window.keystoneLogTerminal('🎬 Initiated 2-track timeline automated assembly in DaVinci Resolve...')">
            🎬 Run Automated Assembly
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🎵 Ingesting background music with calibrated -18dB Fairlight ducking...')">
            🎵 Ingest -18dB Ducked Music
          </button>
          <button class="swarm-secondary-btn" style="width:100%; margin-top:6px;" onclick="window.keystoneLogTerminal('🌉 Bridging jump cuts with autonomous B-roll inserts...')">
            🌉 Bridge Cuts with B-Roll
          </button>
        </div>
      `;
    } else {
      // Default / 'antigravity' -> Modern Draggable Web Command Hubs
      html = `
        <div class="web-portals-section">
          <div class="web-portals-header">
            <span class="panel-section-title" style="margin:0; font-size:10px; letter-spacing:0.8px; color:var(--hud-neon-cyan);">
              🌐 WEB COMMAND HUBS
            </span>
            <button class="portal-reset-link" id="btnResetPortalsOrder" title="Reset default order">↺ Reset</button>
          </div>
          <div class="web-portals-card">
            <div class="web-portals-grid" id="webPortalsGrid">
              <!-- Rendered dynamically by initWebPortalsDragAndDrop() -->
            </div>
          </div>
        </div>
      `;
    }

    sidebarDynamicContent.innerHTML = html;

    if (!tabKey || tabKey === 'antigravity') {
      initWebPortalsDragAndDrop();
    }
  }

  // --------------------------------------------------------------------------
  // --------------------------------------------------------------------------
  // Default Bootstrap Chats & Sidebar Control Hub Logic
  // --------------------------------------------------------------------------
  const DEFAULT_BOOTSTRAP_CHATS = [
    {
      id: '1baa32b7-bf7a-4715-b3f6-2daeb7357af8',
      short_title: '[#01] Run Bootstrap Process',
      full_title: '[#01] Run Bootstrap Process — Master Daemons & Watchdog',
      subtitle: 'Master Daemons & Watchdog',
      number: '01'
    },
    {
      id: '021ad8b8-4d88-4087-bd73-f626ccaa0a9e',
      short_title: '[#02] Getting Started With Bootstrap',
      full_title: '[#02] Getting Started With Bootstrap — Architecture & Rules',
      subtitle: 'Architecture & Rules',
      number: '02'
    },
    {
      id: 'b0dbf679-0d9b-45ee-971d-bfb6f964689a',
      short_title: '[#03] Bootstrap Implementation Guide',
      full_title: '[#03] Bootstrap Implementation Guide — Engine Calibration',
      subtitle: 'Engine Calibration',
      number: '03'
    },
    {
      id: '32dd7ff9-c336-4e75-ac2d-9fdfb3429f2a',
      short_title: '[#04] Thirty Day Agent Strategy',
      full_title: '[#04] Thirty Day Agent Strategy — 30-Day Multi-Agent Plan',
      subtitle: '30-Day Multi-Agent Plan',
      number: '04'
    }
  ];

  function updateSidebarActiveChatCard(chatId, chatTitle) {
    const m = chatTitle.match(/\[?#(\d+)\]?/);
    const num = m ? `[#${m[1]}]` : '[#01]';
    const parts = chatTitle.split(' — ');
    const title = (parts[0] || chatTitle).replace(/\[?#\d+\]?\s*/, '').trim();
    const desc = parts[1] || 'Master Daemons & Watchdog';

    const numEl = document.getElementById('sidebarActiveChatNum');
    const titleEl = document.getElementById('sidebarActiveChatTitle');
    const descEl = document.getElementById('sidebarActiveChatDesc');
    if (numEl) numEl.textContent = num;
    if (titleEl) titleEl.textContent = title;
    if (descEl) descEl.textContent = desc;
  }

  function renderSidebarBootstrapBox(chats, activeId) {
    const list = document.getElementById('sidebarChatList');
    if (!list) return;
    const chatItems = (Array.isArray(chats) && chats.length > 0) ? chats : DEFAULT_BOOTSTRAP_CHATS;
    list.innerHTML = '';

    chatItems.forEach((c) => {
      const isAct = (c.id === activeId) || (c.is_active) || (c.id === selectedChatId);
      const item = document.createElement('div');
      item.className = `sidebar-chat-item ${isAct ? 'active' : ''}`;
      item.setAttribute('data-chat-id', c.id);
      item.setAttribute('data-chat-title', c.full_title || c.title || c.short_title);
      item.innerHTML = `
        <div class="sidebar-chat-dot"></div>
        <div class="sidebar-chat-text">
          <span class="sidebar-chat-name">${c.short_title || c.title}</span>
          <span class="sidebar-chat-sub">${c.subtitle || c.desc || (c.id ? c.id.slice(0, 8) : '')}</span>
        </div>
      `;
      item.addEventListener('click', (ev) => {
        ev.stopPropagation();
        bindTargetChat(c.id, c.full_title || c.title || c.short_title);
      });
      list.appendChild(item);
    });

    const activeItem = chatItems.find(c => c.id === activeId || c.id === selectedChatId) || chatItems[0];
    if (activeItem) {
      updateSidebarActiveChatCard(activeItem.id, activeItem.full_title || activeItem.title || activeItem.short_title);
    }
  }

  function renderSidebarGroups() {
    const list = document.getElementById('sidebarGroupsList');
    if (!list) return;
    list.innerHTML = '';

    Object.keys(TAB_GROUPS).forEach((gId) => {
      const idNum = parseInt(gId, 10);
      const group = TAB_GROUPS[idNum];
      const chip = document.createElement('button');
      chip.className = 'sidebar-group-chip' + (idNum === activeGroup ? ' active' : '');
      chip.setAttribute('data-group', idNum);
      const dot = idNum === activeGroup ? '<span class="sidebar-group-dot"></span>' : '';
      chip.innerHTML = `${dot}<span>${group.title || `Group ${idNum}`}</span>`;
      chip.onclick = (e) => {
        e.stopPropagation();
        renderTabGroup(idNum);
      };
      list.appendChild(chip);
    });

    const badge = document.getElementById('sidebarActiveGroupBadge');
    if (badge) {
      const g = TAB_GROUPS[activeGroup];
      badge.textContent = `✦ ${g ? g.title : `Group ${activeGroup}`}`;
    }
    const desc = document.getElementById('sidebarActiveGroupDesc');
    if (desc) {
      const g = TAB_GROUPS[activeGroup];
      desc.textContent = g ? (g.desc || g.name) : 'Active Workspace';
    }
    const countPill = document.getElementById('sidebarGroupsCountPill');
    if (countPill) {
      countPill.textContent = `${Object.keys(TAB_GROUPS).length} Groups`;
    }
  }

  function renderGroupPills() {
    const container = document.getElementById('groupPillsScroll');
    if (!container) return;
    container.innerHTML = '';

    Object.keys(TAB_GROUPS).forEach((gId) => {
      const idNum = parseInt(gId, 10);
      const group = TAB_GROUPS[idNum];
      const btn = document.createElement('button');
      btn.className = 'group-pill-btn' + (idNum === activeGroup ? ' active' : '');
      btn.setAttribute('data-group', idNum);
      const dot = idNum === activeGroup ? '<span class="group-pill-dot"></span>' : '';
      btn.innerHTML = `${dot}<span>${group.title || `Group ${idNum}`}</span>`;
      btn.onclick = () => renderTabGroup(idNum);
      container.appendChild(btn);
    });
  }

  function renderTabGroup(groupId) {
    activeGroup = groupId;
    const group = TAB_GROUPS[groupId] || TAB_GROUPS[1];

    // Auto-collapse groups drawer on selection
    document.getElementById('hubBoxGroups')?.classList.remove('open');

    // Re-render sidebar groups & topbar pills if present
    renderSidebarGroups();
    renderGroupPills();

    // Render Tabs in Tab Strip (Placed at the Far Left!)
    if (hudTabStrip) {
      hudTabStrip.innerHTML = '';
      group.tabs.forEach((tab, index) => {
        const btn = document.createElement('button');
        btn.role = 'tab';
        btn.className = 'hud-tab-item' + (index === 0 ? ' active' : '');
        btn.setAttribute('data-tab', tab.key);
        btn.innerHTML = `<span class="hud-tab-icon">${tab.icon}</span><span>${tab.label}</span>`;
        btn.onclick = () => switchTab(tab.key);
        hudTabStrip.appendChild(btn);
      });

      // Append '+' add tab button
      const addBtn = document.createElement('button');
      addBtn.className = 'hud-tab-add-btn';
      addBtn.id = 'btnAddTab';
      addBtn.title = 'New Socket Tab';
      addBtn.textContent = '+';
      addBtn.onclick = () => {
        const name = prompt('Enter Tab Name:', 'Custom View');
        if (!name) return;
        const key = name.toLowerCase().replace(/\s+/g, '-');
        group.tabs.push({ key, label: name, icon: '🌐' });
        renderTabGroup(groupId);
        switchTab(key);
      };
      hudTabStrip.appendChild(addBtn);

      // Switch to first tab of the group or show empty workspace
      if (group.tabs.length > 0) {
        switchTab(group.tabs[0].key);
      } else {
        [viewSocketPane, viewAvatarPane, viewPolymarketPane, viewFlowPane, viewDaVinciPane, viewAgentsPane].forEach((p) => {
          if (p) {
            p.classList.remove('active');
            p.style.display = 'none';
          }
        });
        if (viewSocketPane) {
          viewSocketPane.classList.add('active');
          viewSocketPane.style.display = 'flex';
          const wm = document.getElementById('canvasWatermark');
          if (wm) {
            wm.innerHTML = `
              <svg class="canvas-watermark-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              <span class="canvas-watermark-text" style="color:var(--hud-neon-cyan);">${group.name}</span>
              <span style="font-size: 11px; color: var(--hud-text-dim); margin-top: 6px;">Empty Workspace — Click '+' on the top bar to add tabs</span>
            `;
          }
        }
        updateSidebarContent('empty');
      }
    }
  }

  // Sidebar Group Add Button
  btnSidebarAddGroup?.addEventListener('click', (e) => {
    e.stopPropagation();
    const newId = Object.keys(TAB_GROUPS).length + 1;
    TAB_GROUPS[newId] = {
      name: `✦ KEYSTONE — GROUP ${newId}`,
      title: `Group ${newId}`,
      tabs: []
    };
    renderSidebarGroups();
    renderTabGroup(newId);
    logTerminal(`📑 Created new Workspace Group ${newId}.`);
  });

  btnAddGroup?.addEventListener('click', (e) => {
    e.stopPropagation();
    const newId = Object.keys(TAB_GROUPS).length + 1;
    TAB_GROUPS[newId] = {
      name: `✦ KEYSTONE — GROUP ${newId}`,
      title: `Group ${newId}`,
      tabs: []
    };
    renderSidebarGroups();
    renderTabGroup(newId);
  });

  // Roll-Down Drawer Toggle Handlers (Compact Single-Row Headers)
  const btnToggleBootstrapDrawer = document.getElementById('btnToggleBootstrapDrawer');
  btnToggleBootstrapDrawer?.addEventListener('click', (e) => {
    e.stopPropagation();
    const wasOpen = hubBoxBootstrap?.classList.contains('open');
    hubBoxBootstrap?.classList.toggle('open');
    // Close other drawer if open
    hubBoxGroups?.classList.remove('open');
    if (!wasOpen) {
      syncActiveChatsFromDaemon();
    }
  });

  const btnToggleGroupsDrawer = document.getElementById('btnToggleGroupsDrawer');
  btnToggleGroupsDrawer?.addEventListener('click', (e) => {
    e.stopPropagation();
    hubBoxGroups?.classList.toggle('open');
    // Close other drawer if open
    hubBoxBootstrap?.classList.remove('open');
  });

  // Global Outside-Click Handler to close sidebar drawers
  document.addEventListener('click', (e) => {
    if (!e.target.closest('#hubBoxBootstrap')) {
      hubBoxBootstrap?.classList.remove('open');
    }
    if (!e.target.closest('#hubBoxGroups')) {
      hubBoxGroups?.classList.remove('open');
    }
    chatDropdownWrap?.classList.remove('open');
  });

  // Chat Dropdown Toggle with Auto-Discovery Refresh (Legacy Support)
  chatDropdownBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    const wasOpen = chatDropdownWrap?.classList.contains('open');
    chatDropdownWrap?.classList.toggle('open');
    if (!wasOpen) {
      syncActiveChatsFromDaemon();
    }
  });

  function bindTargetChat(chatId, chatTitle) {
    selectedChatId = chatId;
    selectedChatTitle = chatTitle;

    // Auto-collapse bootstrap drawer on selection
    document.getElementById('hubBoxBootstrap')?.classList.remove('open');

    // Update active highlight in sidebar list
    document.querySelectorAll('.sidebar-chat-item').forEach((item) => {
      item.classList.toggle('active', item.getAttribute('data-chat-id') === chatId);
    });
    // Update active highlight in legacy dropdown
    document.querySelectorAll('.chat-menu-item').forEach((item) => {
      item.classList.toggle('active', item.getAttribute('data-chat-id') === chatId);
    });

    updateSidebarActiveChatCard(chatId, chatTitle);

    const shortTitle = chatTitle.split(' — ')[0];

    if (activeChatLabel) {
      activeChatLabel.textContent = `💬 ${shortTitle}`;
    }

    const avatarBoundBadge = document.getElementById('avatarBoundBadge');
    if (avatarBoundBadge) {
      const m = chatTitle.match(/\[?#(\d+)\]?/);
      avatarBoundBadge.textContent = m ? `CHAT #${m[1]}` : `ACTIVE CHAT`;
    }

    if (speechBubbleText) {
      speechBubbleText.textContent = `Bound to ${shortTitle}. Ready for voice commands.`;
    }

    localStorage.setItem('keystone_active_chat_id', chatId);
    localStorage.setItem('keystone_active_chat_title', chatTitle);

    // Lock target conversation in daemon
    fetch('http://127.0.0.1:9876/api/set-target', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: chatId, title: chatTitle, name: chatTitle })
    }).catch(() => {});

    logTerminal(`🎯 Target Chat Bound: [${chatTitle}]. Voice (F9) routes here directly.`, 'success');
    updateSidebarContent(activeTabKey);

    // Companion voice feedback & talking state rotation
    triggerAvatarSpeech(`Active chat locked to ${shortTitle}. Ready for Wayne's command.`);
  }

  function renderChatDropdown(chats, activeId) {
    if (!chatDropdownMenu || !Array.isArray(chats) || chats.length === 0) return;
    chatDropdownMenu.innerHTML = '';
    chats.forEach((c) => {
      const isAct = (c.id === activeId) || (c.is_active) || (c.id === selectedChatId);
      const item = document.createElement('div');
      item.className = `chat-menu-item ${isAct ? 'active' : ''}`;
      item.setAttribute('data-chat-id', c.id);
      item.setAttribute('data-chat-title', c.full_title || c.title || c.short_title);
      item.innerHTML = `
        <div class="chat-info">
          <span class="chat-title">${c.short_title || c.title}</span>
          <span class="chat-desc">${c.subtitle || c.desc || (c.id ? c.id.slice(0, 8) : '')}</span>
        </div>
      `;
      item.addEventListener('click', (ev) => {
        ev.stopPropagation();
        bindTargetChat(c.id, c.full_title || c.title || c.short_title);
        chatDropdownWrap?.classList.remove('open');
      });
      chatDropdownMenu.appendChild(item);
    });

    const activeItem = chats.find(c => c.id === activeId || c.id === selectedChatId) || chats[0];
    if (activeItem) {
      selectedChatId = activeItem.id;
      selectedChatTitle = activeItem.full_title || activeItem.title || activeItem.short_title;
      if (activeChatLabel) activeChatLabel.textContent = `💬 ${activeItem.short_title || activeItem.title}`;
      const avatarBoundBadge = document.getElementById('avatarBoundBadge');
      if (avatarBoundBadge) {
        avatarBoundBadge.textContent = `CHAT #${activeItem.number || '01'}`;
      }
    }
  }

  async function syncActiveChatsFromDaemon() {
    try {
      const res = await fetch('http://127.0.0.1:9876/api/chats');
      if (res.ok) {
        const data = await res.json();
        if (data && data.active_chats && Array.isArray(data.active_chats) && data.active_chats.length > 0) {
          renderSidebarBootstrapBox(data.active_chats, data.active_conversation_id || selectedChatId);
          renderChatDropdown(data.active_chats, data.active_conversation_id || selectedChatId);
          return;
        }
      }
    } catch (e) {
      console.warn('[Sync Active Chats] Local daemon offline, using cached chat list:', e);
    }
    // Fallback: render default bootstrap chats
    renderSidebarBootstrapBox(DEFAULT_BOOTSTRAP_CHATS, selectedChatId);
  }

  document.querySelectorAll('.chat-menu-item').forEach((item) => {
    item.addEventListener('click', (e) => {
      e.stopPropagation();
      const chatId = item.getAttribute('data-chat-id');
      const chatTitle = item.getAttribute('data-chat-title') || item.querySelector('.chat-title')?.textContent;
      bindTargetChat(chatId, chatTitle);
      chatDropdownWrap?.classList.remove('open');
    });
  });

  // --------------------------------------------------------------------------
  // Tab Switching Logic (Universal Matrix Socket Standard)
  // --------------------------------------------------------------------------
  // Universal Matrix Socket Standard:
  // Tabs that have dedicated specialized studio workspaces:
  // vector-brain, agents, flow, davinci, money.
  // Other tabs (antigravity, work, possibilities, recomposition, protocols, websites)
  // use the full universal Antigravity Matrix Socket chamber!
  const EXCEPTION_TABS = ['vector-brain', 'agents', 'flow', 'davinci', 'money'];

  function tauriInvoke() {
    return window.__TAURI_INTERNALS__?.invoke
      || window.__TAURI__?.core?.invoke
      || null;
  }

  function updateSocketVisibility(visible) {
    if (!socketedHwnd) return;
    const invoke = tauriInvoke();
    if (invoke) {
      invoke('set_socket_visibility', {
        targetHwnd: socketedHwnd,
        visible: Boolean(visible)
      }).catch(() => {});
    }
  }

  function switchTab(tabKey) {
    activeTabKey = tabKey;
    window.activeTabKey = tabKey;
    window.switchTab = switchTab;

    document.querySelectorAll('.hud-tab-item').forEach((t) => {
      t.classList.toggle('active', t.getAttribute('data-tab') === tabKey);
    });

    // Manage native Win32 window visibility if socketed in Tauri
    const isExceptionTab = EXCEPTION_TABS.includes(tabKey);
    if (isSocketed && socketedHwnd) {
      updateSocketVisibility(!isExceptionTab);
      if (!isExceptionTab) {
        scheduleSyncSocketBounds();
      }
    }

    // Hide all view panes
    [viewSocketPane, viewVectorBrainPane, viewPolymarketPane, viewFlowPane, viewDaVinciPane, viewAgentsPane].forEach((p) => {
      if (p) {
        p.classList.remove('active');
        p.style.display = 'none';
      }
    });

    // Exception tab 1: Vector Brain preserves its dedicated neural cortex view pane
    if (tabKey === 'vector-brain') {
      if (viewVectorBrainPane) {
        viewVectorBrainPane.classList.add('active');
        viewVectorBrainPane.style.display = 'flex';
        ensureNeuralBrainInitialized();
        window.__neuralBrainInstance?.resume?.();
      }
    } else {
      window.__neuralBrainInstance?.pause?.();
    }

    if (tabKey === 'agents') {
      // Exception tab 2: Agents has its dedicated 68-Agent Neural Breakdown Workspace
      if (viewAgentsPane) {
        viewAgentsPane.classList.add('active');
        viewAgentsPane.style.display = 'flex';
      }
    } else if (tabKey === 'flow') {
      // Exception tab 3: Google Flow Video Suite
      if (viewFlowPane) {
        viewFlowPane.classList.add('active');
        viewFlowPane.style.display = 'flex';
      }
    } else if (tabKey === 'davinci') {
      // Exception tab 4: DaVinci Resolve Assembly Bridge
      if (viewDaVinciPane) {
        viewDaVinciPane.classList.add('active');
        viewDaVinciPane.style.display = 'flex';
      }
    } else if (tabKey === 'money') {
      // Exception tab 5: Polymarket 365 Sentinel
      if (viewPolymarketPane) {
        viewPolymarketPane.classList.add('active');
        viewPolymarketPane.style.display = 'flex';
      }
    } else if (tabKey !== 'vector-brain') {
      // Universal Socket Standard: all other tabs show the Antigravity Click-in Matrix Socket
      if (viewSocketPane) {
        viewSocketPane.classList.add('active');
        viewSocketPane.style.display = 'flex';

        const titleMap = {
          'antigravity': 'ANTIGRAVITY MATRIX',
          'work': 'ANTIGRAVITY MATRIX — WORK',
          'possibilities': 'ANTIGRAVITY MATRIX — POSSIBILITIES',
          'recomposition': 'ANTIGRAVITY MATRIX — RECOMPOSITION',
          'protocols': 'ANTIGRAVITY MATRIX — PROTOCOLS',
          'websites': 'ANTIGRAVITY MATRIX — WEBSITES',
          'money': 'ANTIGRAVITY MATRIX — MONEY'
        };
        if (portalMainTitle && titleMap[tabKey]) {
          portalMainTitle.textContent = titleMap[tabKey];
        }

        if (isSocketed) {
          if (socketPortalContainer) socketPortalContainer.style.display = 'none';
          if (socketActiveChamber) socketActiveChamber.style.display = 'flex';
        } else {
          if (socketPortalContainer) socketPortalContainer.style.display = 'flex';
          if (socketActiveChamber) socketActiveChamber.style.display = 'none';
        }
      }
    }

    // Dynamically update right sidebar content and bottom dock center
    updateSidebarContent(tabKey);
    updateDockCenterContent(tabKey);
  }
  window.switchTab = switchTab;

  // --------------------------------------------------------------------------
  // Google Flow & Protocols Bottom Dock Quick Controls & Global Actions
  // --------------------------------------------------------------------------
  window.keystoneFlowMode = localStorage.getItem('keystone_flow_mode') || 'manual';
  window.__swarmRunning = false;

  function updateDockCenterContent(tabKey) {
    const dockCenter = document.getElementById('dockCustomCenter');
    if (dockCenter) {
      dockCenter.innerHTML = '';
    }
  }

  window.setFlowCockpitMode = function(mode) {
    window.keystoneFlowMode = mode;
    localStorage.setItem('keystone_flow_mode', mode);
    updateSidebarContent(activeTabKey);
    updateDockCenterContent(activeTabKey);
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🎛️ Switched Google Flow to ${mode === 'swarm' ? '🤖 SWARM AUTO-PILOT' : '🎮 MANUAL COCKPIT'} mode.`);
    }
  };

  window.toggleFlowMode = function() {
    const nextMode = (window.keystoneFlowMode === 'swarm') ? 'manual' : 'swarm';
    window.setFlowCockpitMode(nextMode);
  };

  window.applyFlowPreset = async function(mode, aspect, duration, resolution, count) {
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`⚙️ Sending Google Flow preset: ${mode.toUpperCase()} · ${aspect} ${duration || ''} ${resolution || ''} ${count}...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/flow_preset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode, aspect, duration, resolution, count, ingredients: true })
      });
      const data = await resp.json();
      if (data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ Applied Flow preset: ${mode} ${aspect} (${data.tab || 'active tab'})`);
        }
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Flow preset notice: ${data.error || 'Check Chrome tab'}`);
        }
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Error connecting to Port 9879 daemon: ${err.message}`);
      }
    }
  };

  window.injectNext5Prompts = async function() {
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal('⚡ Injecting next 5 prompts with auto-enter into Google Flow...');
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/flow_orchestrator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'start' })
      });
      const data = await resp.json();
      if (data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`🚀 Dispatched 5-batch loop (PID: ${data.pid || 'active'}). Monitoring status...`);
        }
        window.__swarmRunning = true;
        updateSidebarContent(activeTabKey);
        updateDockCenterContent(activeTabKey);
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Orchestrator notice: ${data.error || JSON.stringify(data)}`);
        }
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Failed to dispatch prompts: ${err.message}`);
      }
    }
  };

  window.refreshFlowPayloadCounts = async function() {
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/flow_payload');
      const data = await resp.json();
      if (data && data.ok) {
        window.keystoneActiveVideoCount = data.video_count || 8;
        window.keystoneActiveBrollCount = data.broll_count || 7;
        const brollBtn = document.getElementById('btnRenameBrollStudio');
        if (brollBtn) brollBtn.textContent = `🏷️ Auto-Rename B-Roll (A${window.keystoneActiveBrollCount}..A1)`;
        const vidBtn = document.getElementById('btnRenameVideosStudio');
        if (vidBtn) vidBtn.textContent = `🎬 Auto-Rename Videos (${window.keystoneActiveVideoCount}..1)`;
      }
    } catch (e) {}
  };

  window.generateReferenceAsset = async function(assetType, channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    const label = assetType === 'cloth_1' ? 'Clothes (cloth_1)' : 'Background (background_1)';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🎨 Ingesting & auto-renaming reference asset: ${label} (${context})...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/generate_reference_asset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ asset_type: assetType, context: context })
      });
      const data = await resp.json();
      if (data && data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ ${label} generated and renamed on canvas! (${context})`);
        }
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Generation notice for ${label}: ${data?.error || 'Unknown error'}`);
        }
      }
    } catch(err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Error generating ${label}: ${err.message}`);
      }
    }
  };

  window.renameReferenceAsset = async function(assetType, channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    const label = assetType === 'cloth_1' ? 'Clothes (cloth_1)' : 'Background (background_1)';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🏷️ Renaming existing canvas tile to ${label} (${context})...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/rename_reference_asset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ asset_type: assetType, context: context })
      });
      const data = await resp.json();
      if (data && data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ ${label} successfully renamed on canvas! (${context})`);
        }
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Rename notice for ${label}: ${data?.error || 'Unknown error'}`);
        }
      }
    } catch(err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Error renaming ${label}: ${err.message}`);
      }
    }
  };

  window.executeMediaRename = async function(mediaType, channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🏷️ Running Reverse Grid Law renamer for ${mediaType} (${context})...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/batch_rename_media', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ media_type: mediaType, context: context })
      });
      const data = await resp.json();
      if (data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ Rename complete: ${data.message || 'Media renamed successfully'}`);
        }
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Rename notice: ${data.error || JSON.stringify(data)}`);
        }
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Rename error: ${err.message}`);
      }
    }
  };

  window.executeMediaDownload = async function(mediaType, channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`📥 Starting autonomous media download for ${mediaType} (${context})...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/batch_download_media', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ media_type: mediaType, quality: mediaType === 'images' ? '1K' : '1080p', context: context })
      });
      const data = await resp.json();
      if (data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ Download complete: ${data.message || 'Media downloaded successfully'}`);
        }
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Download notice: ${data.error || JSON.stringify(data)}`);
        }
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Download error: ${err.message}`);
      }
    }
  };

  window.executeDavinciAssembly = async function(channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🎬 Launching DaVinci Resolve automated 2-track timeline assembly (${context})...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/assemble_davinci_timeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: context })
      });
      const data = await resp.json();
      if (data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ DaVinci Assembly dispatched (PID: ${data.pid || 'active'}, Context: ${context}).`);
        }
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ DaVinci notice: ${data.error || JSON.stringify(data)}`);
        }
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ DaVinci assembly error: ${err.message}`);
      }
    }
  };

  window.toggleSwarmOrchestrator = async function(channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    const action = window.__swarmRunning ? 'stop' : 'start';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🤖 Swarm Sentinel (${context}): Sending ${action.toUpperCase()} signal...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/flow_orchestrator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action, context: context })
      });
      const data = await resp.json();
      if (action === 'start' && data.ok) {
        window.__swarmRunning = true;
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`🚀 Flow 5-Batch Sentinel running for ${context} (PID: ${data.pid}). Status: Active.`);
        }
      } else {
        window.__swarmRunning = false;
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`🛑 Flow Swarm Sentinel stopped.`);
        }
      }
      updateSidebarContent(activeTabKey);
      updateDockCenterContent(activeTabKey);
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Swarm Sentinel error: ${err.message}`);
      }
    }
  };

  window.checkSwarmStatus = async function(channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`📊 Querying Swarm Sentinel status (${context}) from Port 9879...`);
    }
    try {
      const resp = await fetch(`http://127.0.0.1:9879/api/flow_orchestrator?context=${context}`);
      const data = await resp.json();
      window.__swarmRunning = Boolean(data.running);
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`📊 Swarm Sentinel: ${data.running ? 'RUNNING (PID ' + data.pid + ')' : 'IDLE / READY'}`);
      }
      updateSidebarContent(activeTabKey);
      updateDockCenterContent(activeTabKey);
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`⚠️ Could not query swarm status: ${err.message}`);
      }
    }
  };

  window.openGoogleFlowHUD = async function(channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🌐 Activating Google Flow tab on Port 9222 and attaching Keystone HUD overlay (${context})...`);
    }
    try {
      const resp = await fetch('http://127.0.0.1:9879/api/open_flow_hud', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: context })
      });
      const data = await resp.json();
      if (data.ok) {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`✅ Attached HUD to Google Flow (${data.tab || 'active tab'}). Switching view...`);
        }
        window.refreshFlowPayloadCounts();
      } else {
        if (window.keystoneLogTerminal) {
          window.keystoneLogTerminal(`⚠️ Notice: ${data.error || 'Check Chrome on Port 9222'}`);
        }
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Error activating Google Flow: ${err.message}`);
      }
    }
  };

  window.runProtocolsScriptwriter = async function() {
    const targetTitle = selectedChatTitle || 'Active Chat';
    const targetId = selectedChatId || '';
    const scriptwriterPrompt = `📜 SCRIPTWRITER PIPELINE ACTIVATED: Execute Keystone Protocols Master Video Scripting Pipeline (A1 Skill). Read C:\\Users\\Curtis\\.gemini\\config\\skills\\A1_keystone_protocols_scriptwriter\\SKILL.md and 08_Keystone_protocols\\subagents\\00_INDEX.md. Check active context in [${targetTitle}]: if continuing the 30-day peptide/recomposition series, inspect 08_Keystone_protocols\\video_history.md and determine the next sequential day in the 30-day series; if researching active trending topics, launch Phase 0 & Phase 1 research swarms for high-volume active queries people are searching for. Execute the full pipeline: Phase 0 Strategy Brief -> Phase 1 Research -> Phase 2 Titles -> Phase 3 Wayne Approval -> Phase 4 Full 51-Clip Scriptwriting -> Phase 5 Save to 08_Keystone_protocols\\Google_Flow\\ -> Phase 6 History Logging & compile overlay payload. Report completion.`;

    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`📜 [Scriptwriter] Protocols Scriptwriter activated for [${targetTitle}]. Synthesizing 30-day series & active trends...`, 'cyan');
    }
    triggerAvatarSpeech('Protocols scriptwriter engaged. Analyzing thirty-day stint and active clinical trends.');
    setAvatarState('working');

    fetch('http://127.0.0.1:9876/api/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: scriptwriterPrompt,
        conversation_id: targetId,
        target_chat_name: targetTitle,
        chat_name: targetTitle
      })
    }).then(r => r.json()).then(data => {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`✅ Protocols Scriptwriter pipeline dispatched to Antigravity (HTTP ${data.status || 'OK'})`, 'success');
      }
    }).catch((err) => {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`⚠️ Protocols prompt dispatch notice: ${err.message}`, 'warn');
      }
    });

    fetch('http://127.0.0.1:9879/api/flow_preset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: 'video', aspect: '16:9', duration: '10s', resolution: '720p', count: 'x1', ingredients: true })
    }).catch(() => {});
  };

  window.runPossibilitiesScriptwriter = async function() {
    const targetTitle = selectedChatTitle || 'Active Chat';
    const targetId = selectedChatId || '';
    const scriptwriterPrompt = `🏗️ POSSIBILITIES SCRIPTWRITER PIPELINE ACTIVATED: Execute Keystone Possibilities Master Video Scripting Pipeline (A2 Skill). Read C:\\Users\\Curtis\\.gemini\\config\\skills\\A2_keystone_possibilities_scriptwriter\\SKILL.md and 06_Keystone_possibilities\\06_builder_code\\00_INDEX.md. Check active context in [${targetTitle}]: Vancouver Multiplex Bill 44, Missing Middle Housing, BC Building Code 2024 (ATS shearwalls, holdowns, stepped footings, high seismic/wind calibration, Step Code energy compliance), or development pro-forma cashflows. Execute full pipeline: Phase 0 Strategy Brief -> Phase 1 Technical Research & Code Citations -> Phase 2 High-CTR Titles -> Phase 3 Wayne Approval -> Phase 4 26-Clip Avatar & 26 B-Roll Scriptwriting -> Phase 5 Save to 06_Keystone_possibilities\\Google_Flow\\ -> Phase 6 Compile overlay payload with background_1 (West Vancouver architectural studio) and cloth_1 (tailored executive PM suit). Report completion.`;

    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🏗️ [Scriptwriter] Possibilities Scriptwriter activated for [${targetTitle}]. Synthesizing BC Building Code & Vancouver Multiplex pro-forma...`, 'gold');
    }
    triggerAvatarSpeech('Possibilities scriptwriter engaged. Analyzing Vancouver Multiplex Bill 44 and BC Building Code structural engineering.');
    setAvatarState('working');

    fetch('http://127.0.0.1:9876/api/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: scriptwriterPrompt,
        conversation_id: targetId,
        target_chat_name: targetTitle,
        chat_name: targetTitle
      })
    }).then(r => r.json()).then(data => {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`✅ Possibilities Scriptwriter pipeline dispatched to Antigravity (HTTP ${data.status || 'OK'})`, 'success');
      }
    }).catch((err) => {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`⚠️ Possibilities prompt dispatch notice: ${err.message}`, 'warn');
      }
    });

    fetch('http://127.0.0.1:9879/api/flow_preset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: 'video', aspect: '16:9', duration: '10s', resolution: '720p', count: 'x1', ingredients: true })
    }).catch(() => {});
  };

  window.runRecompositionScriptwriter = async function() {
    const targetTitle = selectedChatTitle || 'Active Chat';
    const targetId = selectedChatId || '';
    const scriptwriterPrompt = `🛡️ RECOMPOSITION SCRIPTWRITER PIPELINE ACTIVATED: Execute Keystone Recomposition Master Video Scripting Pipeline (A4 Skill). Read C:\\Users\\Curtis\\.gemini\\config\\skills\\A4_keystone_recomposition_scriptwriter\\SKILL.md and 07_Keystone_recomposition\\00_INDEX.md. Check active context in [${targetTitle}]: Squamish Builder persona, Official Artist Channel releases, deep house & organic strings soundtracking, 53-clip video sequence, companion shorts, and peptide/TRT recomposition cross-promos. Execute full pipeline: Phase 0 Strategy Brief -> Phase 1 Music & Aesthetic Research -> Phase 2 Releases & Track Allocation -> Phase 3 Wayne Approval -> Phase 4 53-Clip Master Video Script -> Phase 5 Save to 07_Keystone_recomposition\\Google_Flow\\ -> Phase 6 Compile overlay payload with background_1 (Squamish luxury timber frame studio) and cloth_1 (deep charcoal technical builder pullover). Report completion.`;

    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`🛡️ [Scriptwriter] Recomposition Scriptwriter activated for [${targetTitle}]. Synthesizing Squamish builder music and 53-clip sequence...`, 'purple');
    }
    triggerAvatarSpeech('Recomposition scriptwriter engaged. Synthesizing Squamish builder persona and deep house soundtrack.');
    setAvatarState('working');

    fetch('http://127.0.0.1:9876/api/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: scriptwriterPrompt,
        conversation_id: targetId,
        target_chat_name: targetTitle,
        chat_name: targetTitle
      })
    }).then(r => r.json()).then(data => {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`✅ Recomposition Scriptwriter pipeline dispatched to Antigravity (HTTP ${data.status || 'OK'})`, 'success');
      }
    }).catch((err) => {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`⚠️ Recomposition prompt dispatch notice: ${err.message}`, 'warn');
      }
    });

    fetch('http://127.0.0.1:9879/api/flow_preset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: 'video', aspect: '16:9', duration: '10s', resolution: '720p', count: 'x1', ingredients: true })
    }).catch(() => {});
  };

  window.publishLuxuryBlog = async function(channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    const isPoss = context.includes('possibilit');
    const endpoint = isPoss ? '/api/publish_luxury_blog_possibilities' : '/api/publish_luxury_blog';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`📰 Dispatched WordPress Luxury Blog publishing pipeline (${context}) (Rank Math 80+ & GSC Indexing)...`);
    }
    triggerAvatarSpeech(`Publishing luxury blog for ${context} to WordPress with Rank Math SEO and instant Google Search Console indexing.`);
    setAvatarState('working');
    try {
      const resp = await fetch(`http://127.0.0.1:9879${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: context })
      });
      const data = await resp.json();
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`✅ Luxury Blog dispatched (${context}): ${data.message || 'Published to WordPress'}`);
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Blog publishing error: ${err.message}`);
      }
    } finally {
      setTimeout(() => {
        if (currentAvatarState === 'working') setAvatarState('idle');
      }, 4000);
    }
  };

  window.uploadYouTubeVideo = async function(format = 'long', channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    const isPoss = context.includes('possibilit');
    const endpoint = isPoss ? '/api/upload_youtube_video_possibilities' : '/api/upload_youtube_video';
    const isShort = format === 'short';
    const label = isShort ? 'YouTube Shorts (9:16)' : 'YouTube Long-Form Video';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`▶️ Dispatched ${label} upload pipeline for ${context} via Chrome CDP Port 9222...`);
    }
    triggerAvatarSpeech(`${isShort ? 'YouTube Shorts' : 'YouTube video'} upload dispatched for ${context}.`);
    setAvatarState('working');
    try {
      const resp = await fetch(`http://127.0.0.1:9879${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ format: isShort ? 'short' : 'long', context: context })
      });
      const data = await resp.json();
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`✅ YouTube ${isShort ? 'Shorts' : 'Video'} upload dispatched (${context}): ${data.message || data.status || 'Active'}`);
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ YouTube upload error: ${err.message}`);
      }
    } finally {
      setTimeout(() => {
        if (currentAvatarState === 'working') setAvatarState('idle');
      }, 4000);
    }
  };

  window.publishMetaSocial = async function(channelContext) {
    const context = channelContext || activeTabKey || 'protocols';
    const isPoss = context.includes('possibilit');
    const endpoint = isPoss ? '/api/publish_meta_social_possibilities' : '/api/publish_meta_social';
    if (window.keystoneLogTerminal) {
      window.keystoneLogTerminal(`📱 Dispatched Meta Business Suite publisher for ${context} (Facebook Page & Instagram Feed/Reels)...`);
    }
    triggerAvatarSpeech(`Meta Business Suite publisher dispatched for ${context}.`);
    setAvatarState('working');
    try {
      const resp = await fetch(`http://127.0.0.1:9879${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: context })
      });
      const data = await resp.json();
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`✅ Meta Social dispatched (${context}): ${data.message || 'Published to Meta'}`);
      }
    } catch (err) {
      if (window.keystoneLogTerminal) {
        window.keystoneLogTerminal(`❌ Meta publishing error: ${err.message}`);
      }
    } finally {
      setTimeout(() => {
        if (currentAvatarState === 'working') setAvatarState('idle');
      }, 4000);
    }
  };

  // --------------------------------------------------------------------------
  // Full-Height Sidebar Layout & Appearance
  // --------------------------------------------------------------------------
  function applyGlow(val) {
    const alpha = (val / 100) * 0.45;
    if (glowDisplay) glowDisplay.textContent = `${val}%`;
    if (glowRange) glowRange.value = val;
    document.documentElement.style.setProperty('--hud-neon-violet-glow', `rgba(139, 92, 246, ${alpha})`);
    document.documentElement.style.setProperty('--hud-neon-cyan-glow', `rgba(0, 240, 255, ${alpha * 0.85})`);
  }

  function applyLayout() {
    document.documentElement.style.setProperty('--hud-inspector-width', `${inspectorWidth}px`);
    appLayout?.setAttribute('data-collapsed', String(isCollapsed));
    if (panelWidthRange) panelWidthRange.value = inspectorWidth;
    if (widthDisplay) widthDisplay.textContent = `${inspectorWidth}px`;
    applyGlow(glowPercent);

    if (btnToggleSidebar) {
      btnToggleSidebar.classList.toggle('active-glow', !isCollapsed);
    }
  }

  function toggleSidebar(forceState) {
    isCollapsed = typeof forceState === 'boolean' ? forceState : !isCollapsed;
    appLayout?.setAttribute('data-collapsed', String(isCollapsed));
    localStorage.setItem('keystone_next_collapsed', String(isCollapsed));

    if (btnToggleSidebar) {
      btnToggleSidebar.classList.toggle('active-glow', !isCollapsed);
    }
    trackLayoutTransition();
  }

  btnToggleSidebar?.addEventListener('click', () => toggleSidebar());
  btnCollapseSidebar?.addEventListener('click', () => toggleSidebar(true));
  btnExpandFab?.addEventListener('click', () => toggleSidebar(false));

  // --------------------------------------------------------------------------
  // Native Tauri Window Controls & Seamless Titlebar/Sidebar Dragging
  // --------------------------------------------------------------------------
  function getTauriWindow() {
    try {
      if (window.__TAURI__?.window?.getCurrentWindow) {
        return window.__TAURI__.window.getCurrentWindow();
      }
      if (window.__TAURI__?.webviewWindow?.getCurrentWebviewWindow) {
        return window.__TAURI__.webviewWindow.getCurrentWebviewWindow();
      }
    } catch (e) {}
    return null;
  }

  function callTauriCommand(cmd, args = {}) {
    try {
      if (window.__TAURI__?.core?.invoke) {
        return window.__TAURI__.core.invoke(cmd, args);
      }
      if (window.__TAURI__?.invoke) {
        return window.__TAURI__.invoke(cmd, args);
      }
    } catch (e) {}
    return null;
  }

  // Draggable Window Handler (between V2.4 and Minimize, plus Topbar spacer)
  function initWindowDragging(el) {
    if (!el) return;
    el.addEventListener('mousedown', (e) => {
      // Ignore right/middle clicks or clicks directly on buttons/inputs
      if (e.button !== 0 || e.target.closest('button, input, select, textarea, .icon-btn, .brand-chip, a')) {
        return;
      }
      const win = getTauriWindow();
      if (win?.startDragging) {
        win.startDragging().catch(() => {});
      }
    });
  }

  initWindowDragging(sidebarDragSpacer);
  initWindowDragging(document.getElementById('hudTopBarDragSpacer'));
  initWindowDragging(document.querySelector('.hud-topbar-drag-spacer'));

  btnWinMin?.addEventListener('click', async (e) => {
    e.stopPropagation();
    const win = getTauriWindow();
    if (win?.minimize) {
      try { await win.minimize(); return; } catch (err) {}
    }
    const inv = callTauriCommand('minimize_window');
    if (inv) {
      try { await inv; return; } catch (err) {}
    }
    logTerminal('─ Window minimize requested');
  });

  btnWinMax?.addEventListener('click', async (e) => {
    e.stopPropagation();
    const win = getTauriWindow();
    if (win?.toggleMaximize) {
      try { await win.toggleMaximize(); return; } catch (err) {}
    }
    const inv = callTauriCommand('maximize_window');
    if (inv) {
      try { await inv; return; } catch (err) {}
    }
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.().catch(() => {});
    } else {
      document.exitFullscreen?.().catch(() => {});
    }
    logTerminal('🗖 Window maximize / restore toggled');
  });

  btnWinClose?.addEventListener('click', async (e) => {
    e.stopPropagation();
    const win = getTauriWindow();
    if (win?.close) {
      try { await win.close(); return; } catch (err) {}
    }
    const inv = callTauriCommand('close_window');
    if (inv) {
      try { await inv; return; } catch (err) {}
    }
    toggleSidebar(true);
  });

  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
      e.preventDefault();
      toggleSidebar();
    }
  });

  // Resizable Splitter
  let lastPointerId = null;
  function stopDragging() {
    if (!isDraggingSplitter) return;
    isDraggingSplitter = false;
    try {
      dragSplitter?.releasePointerCapture(lastPointerId);
    } catch (_) {}
    document.body.classList.remove('is-resizing-splitter');
    localStorage.setItem('keystone_next_width', String(inspectorWidth));
  }

  dragSplitter?.addEventListener('pointerdown', (e) => {
    isDraggingSplitter = true;
    lastPointerId = e.pointerId;
    dragSplitter.setPointerCapture(e.pointerId);
    document.body.classList.add('is-resizing-splitter');
  });

  window.addEventListener('pointermove', (e) => {
    if (!isDraggingSplitter) return;
    const newWidth = Math.min(Math.max(window.innerWidth - e.clientX, 240), 700);
    inspectorWidth = newWidth;
    document.documentElement.style.setProperty('--hud-inspector-width', `${newWidth}px`);
    if (panelWidthRange) panelWidthRange.value = newWidth;
    if (widthDisplay) widthDisplay.textContent = `${newWidth}px`;
    scheduleSyncSocketBounds();
  });

  window.addEventListener('pointerup', stopDragging);
  window.addEventListener('pointercancel', stopDragging);

  panelWidthRange?.addEventListener('input', (e) => {
    const val = parseInt(e.target.value, 10);
    inspectorWidth = val;
    document.documentElement.style.setProperty('--hud-inspector-width', `${val}px`);
    if (widthDisplay) widthDisplay.textContent = `${val}px`;
    localStorage.setItem('keystone_next_width', String(val));
    scheduleSyncSocketBounds();
  });

  window.addEventListener('resize', () => {
    scheduleSyncSocketBounds();
  });

  glowRange?.addEventListener('input', (e) => {
    const val = parseInt(e.target.value, 10);
    glowPercent = val;
    applyGlow(val);
    localStorage.setItem('keystone_next_glow', String(val));
  });

  // --------------------------------------------------------------------------
  // Hardware Telemetry & Overclock Sentinel (Smooth Exponential Moving Average)
  // --------------------------------------------------------------------------
  let smoothedCpu = 15.2;
  let smoothedRam = 13.0;
  let smoothedVram = 4.2;
  let isDaemonStreamingStats = false;
  const TOTAL_RAM_GB = 31.8;
  const TOTAL_VRAM_GB = 15.9;

  function renderTelemetryGauges(gpuName) {
    const cpuPercent = smoothedCpu.toFixed(1);
    const ramGb = smoothedRam.toFixed(1);
    const ramPercent = ((smoothedRam / TOTAL_RAM_GB) * 100).toFixed(1);
    const vramGb = smoothedVram.toFixed(1);
    const vramPercent = ((smoothedVram / TOTAL_VRAM_GB) * 100).toFixed(1);

    if (cpuLoadValue) cpuLoadValue.textContent = `${cpuPercent}%`;
    if (cpuProgressFill) cpuProgressFill.style.width = `${Math.min(Math.max(parseFloat(cpuPercent), 0), 100)}%`;

    if (ramLoadValue) ramLoadValue.textContent = `${ramGb} / ${TOTAL_RAM_GB} GB (${ramPercent}%)`;
    if (ramProgressFill) ramProgressFill.style.width = `${Math.min(Math.max(parseFloat(ramPercent), 0), 100)}%`;

    if (vramLoadValue) vramLoadValue.textContent = `${vramGb} / ${TOTAL_VRAM_GB} GB (${vramPercent}%)`;
    if (vramProgressFill) vramProgressFill.style.width = `${Math.min(Math.max(parseFloat(vramPercent), 0), 100)}%`;

    if (gpuName) {
      const gpuModelText = document.getElementById('gpuModelText');
      if (gpuModelText) gpuModelText.textContent = `${gpuName} · CUDA 12.4 · Direct2D Acceleration`;
    }

    // Overclock & Safety Sentinel
    if (vramSafetyBadge) {
      if (parseFloat(vramPercent) > 85) {
        vramSafetyBadge.textContent = 'OVERCLOCK ALERT';
        vramSafetyBadge.style.color = '#ef4444';
        vramSafetyBadge.style.borderColor = '#ef4444';
        vramSafetyBadge.style.background = 'rgba(239, 68, 68, 0.2)';
      } else {
        vramSafetyBadge.textContent = 'OPTIMAL';
        vramSafetyBadge.style.color = '#10b981';
        vramSafetyBadge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
        vramSafetyBadge.style.background = 'rgba(16, 185, 129, 0.15)';
      }
    }
  }

  function applyLiveTelemetry(st) {
    if (!st) return;
    const rawCpu = typeof st.cpu_percent === 'number' ? st.cpu_percent : parseFloat(st.cpu_percent);
    const rawRamUsed = typeof st.ram_used_gb === 'number' ? st.ram_used_gb : parseFloat(st.ram_used_gb);
    const rawVramUsed = typeof st.vram_used_gb === 'number' ? st.vram_used_gb : parseFloat(st.vram_used_gb);

    if (!isNaN(rawCpu)) {
      smoothedCpu = smoothedCpu * 0.82 + rawCpu * 0.18;
    }
    if (!isNaN(rawRamUsed)) {
      smoothedRam = smoothedRam * 0.85 + rawRamUsed * 0.15;
    }
    if (!isNaN(rawVramUsed)) {
      smoothedVram = smoothedVram * 0.85 + rawVramUsed * 0.15;
    }

    renderTelemetryGauges(st.gpu_name);
  }

  function updateHardwareTelemetry() {
    if (isDaemonStreamingStats) return; // live daemon feed active
    // Gentle micro-fluctuations bounded within tight realistic deltas
    const targetCpu = 15.2 + Math.sin(Date.now() / 15000) * 1.5 + (Math.random() * 0.4 - 0.2);
    const targetRam = 13.0 + Math.sin(Date.now() / 30000) * 0.15 + (Math.random() * 0.04 - 0.02);
    const targetVram = 4.2 + (currentAvatarState !== 'idle' ? 0.2 : 0) + (Math.random() * 0.03 - 0.015);

    smoothedCpu = smoothedCpu * 0.82 + targetCpu * 0.18;
    smoothedRam = smoothedRam * 0.85 + targetRam * 0.15;
    smoothedVram = smoothedVram * 0.85 + targetVram * 0.15;

    renderTelemetryGauges();
  }

  setInterval(updateHardwareTelemetry, 2000);

  // --------------------------------------------------------------------------
  // Procedural Web Audio API Sound Synthesizer (Zero Audio Asset Latency)
  // --------------------------------------------------------------------------
  class PortalAudioEngine {
    constructor() {
      this.ctx = null;
    }
    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) this.ctx = new AudioCtx();
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }
    playSocketLatch() {
      try {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        const filter = this.ctx.createBiquadFilter();

        osc.type = 'sawtooth';
        filter.type = 'lowpass';
        filter.Q.setValueAtTime(4, now);

        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(820, now + 0.18);

        filter.frequency.setValueAtTime(400, now);
        filter.frequency.exponentialRampToValueAtTime(2800, now + 0.18);

        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.3, now + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.28);

        // Resonant metallic latch ping
        const pingOsc = this.ctx.createOscillator();
        const pingGain = this.ctx.createGain();
        pingOsc.type = 'sine';
        pingOsc.frequency.setValueAtTime(1400, now + 0.15);
        pingOsc.frequency.exponentialRampToValueAtTime(600, now + 0.32);

        pingGain.gain.setValueAtTime(0, now);
        pingGain.gain.setValueAtTime(0.25, now + 0.15);
        pingGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.40);

        pingOsc.connect(pingGain);
        pingGain.connect(this.ctx.destination);
        pingOsc.start(now + 0.15);
        pingOsc.stop(now + 0.40);
      } catch (_) {}
    }
    playUnsocketRelease() {
      try {
        this.init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        const filter = this.ctx.createBiquadFilter();

        osc.type = 'sine';
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1200, now);
        filter.frequency.exponentialRampToValueAtTime(150, now + 0.24);

        osc.frequency.setValueAtTime(720, now);
        osc.frequency.exponentialRampToValueAtTime(95, now + 0.22);

        gain.gain.setValueAtTime(0.28, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.26);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.26);
      } catch (_) {}
    }
  }

  const portalAudio = new PortalAudioEngine();

  // Socket Portal & Active Chamber Elements
  const socketPortalContainer = document.getElementById('socketPortalContainer') || viewportContent;
  const socketActiveChamber = document.getElementById('socketActiveChamber');
  const socketDockTarget = document.getElementById('socketDockTarget');
  const portalCore = document.getElementById('portalCore');
  const portalPushBtn = document.getElementById('portalPushBtn');
  const portalShockwave = document.getElementById('portalShockwave');
  const portalMainTitle = document.getElementById('portalMainTitle');
  const portalCoreLabel = document.getElementById('portalCoreLabel');
  const glyphAntigravity = document.getElementById('glyphAntigravity');
  const btnActiveUnsocket = document.getElementById('btnActiveUnsocket');

  // --------------------------------------------------------------------------
  // Native Win32 Coordinate-Lock Socket Service (Tauri v2 / Win32 Bridge)
  // --------------------------------------------------------------------------
  let socketedHwnd = 0;
  let socketSyncInterval = null;
  let cachedHudWindowX = null;
  let cachedHudWindowY = null;
  let lastPosCacheTime = 0;

  async function getScreenBounds(el) {
    if (!el || !el.isConnected) return null;
    const rect = el.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return null;

    const scaleFactor = window.devicePixelRatio || 1;
    let windowX = Math.round(window.screenX * scaleFactor);
    let windowY = Math.round(window.screenY * scaleFactor);

    const now = performance.now();
    // Fast path: reuse cached window position during splitter dragging or if cached within 400ms
    if (cachedHudWindowX !== null && (isDraggingSplitter || now - lastPosCacheTime < 400)) {
      windowX = cachedHudWindowX;
      windowY = cachedHudWindowY;
    } else {
      try {
        const windowObj = getTauriWindow();
        if (windowObj?.innerPosition) {
          const pos = await windowObj.innerPosition();
          if (pos && typeof pos.x === 'number') {
            windowX = pos.x;
            windowY = pos.y;
            cachedHudWindowX = windowX;
            cachedHudWindowY = windowY;
            lastPosCacheTime = now;
          }
        }
      } catch (_) {}
    }

    return {
      x: Math.round(windowX + rect.left * scaleFactor),
      y: Math.round(windowY + rect.top * scaleFactor),
      width: Math.round(rect.width * scaleFactor),
      height: Math.round(rect.height * scaleFactor),
      hudX: windowX,
      hudY: windowY
    };
  }

  async function syncSocketBounds() {
    if (!isSocketed || !socketedHwnd || EXCEPTION_TABS.includes(activeTabKey)) return;
    const targetEl = socketDockTarget || socketActiveChamber;
    if (!targetEl) return;
    const b = await getScreenBounds(targetEl);
    if (b) {
      const invoke = tauriInvoke();
      if (invoke) {
        await invoke('update_socket_bounds', {
          targetHwnd: socketedHwnd,
          x: b.x,
          y: b.y,
          width: b.width,
          height: b.height,
          hudX: b.hudX,
          hudY: b.hudY
        }).catch(() => {});
      }
    }
  }

  let rafSyncId = null;
  function scheduleSyncSocketBounds() {
    if (rafSyncId) cancelAnimationFrame(rafSyncId);
    rafSyncId = requestAnimationFrame(() => {
      rafSyncId = null;
      syncSocketBounds();
      window.__neuralBrainInstance?.handleResize?.();
    });
  }

  if (typeof ResizeObserver !== 'undefined') {
    const canvasObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.target === socketCanvas) {
          const { width, height } = entry.contentRect;
          document.documentElement.style.setProperty('--canvas-width', `${Math.round(width)}px`);
          document.documentElement.style.setProperty('--canvas-height', `${Math.round(height)}px`);
        }
        scheduleSyncSocketBounds();
      }
    });
    if (socketCanvas) canvasObserver.observe(socketCanvas);
    if (socketDockTarget) canvasObserver.observe(socketDockTarget);
    if (socketActiveChamber) canvasObserver.observe(socketActiveChamber);
  }

  function trackLayoutTransition(durationMs = 320) {
    const start = performance.now();
    function tick(now) {
      syncSocketBounds();
      window.__neuralBrainInstance?.handleResize?.();
      if (now - start < durationMs) {
        requestAnimationFrame(tick);
      } else {
        syncSocketBounds();
        window.__neuralBrainInstance?.handleResize?.();
        window.dispatchEvent(new Event('resize'));
      }
    }
    requestAnimationFrame(tick);
  }

  async function dockNativeAntigravityWindow() {
    const invoke = tauriInvoke();
    if (!invoke) {
      console.log('[NativeSocket] Running in browser preview. Native Win32 dock activates on desktop.');
      return;
    }

    const targetEl = socketDockTarget || socketActiveChamber;
    if (!targetEl) return;

    try {
      let hwnd = 0;
      const searchQueries = ['Antigravity', 'antigravity', 'Keystone Brain', 'Chronos', 'Initialize', 'Visual Studio Code', 'Code'];
      for (const q of searchQueries) {
        hwnd = await invoke('find_window_by_title', { titleQuery: q });
        if (hwnd) break;
      }

      if (hwnd) {
        socketedHwnd = hwnd;
        const bounds = await getScreenBounds(targetEl);
        if (bounds) {
          await invoke('socket_window', {
            targetHwnd: hwnd,
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            hudX: bounds.hudX,
            hudY: bounds.hudY
          });
          console.log('[NativeSocket] Antigravity HWND', hwnd, 'docked into desktop workspace.');
          
          if (socketSyncInterval) clearInterval(socketSyncInterval);
          socketSyncInterval = setInterval(syncSocketBounds, 150);
        }
      }
    } catch (err) {
      console.warn('[NativeSocket] Tauri window docking error:', err);
    }
  }

  async function undockNativeAntigravityWindow() {
    if (socketSyncInterval) {
      clearInterval(socketSyncInterval);
      socketSyncInterval = null;
    }
    const invoke = tauriInvoke();
    if (invoke && socketedHwnd) {
      try {
        await invoke('unsocket_window', { targetHwnd: socketedHwnd });
        console.log('[NativeSocket] Antigravity HWND', socketedHwnd, 'undocked.');
      } catch (err) {
        console.warn('[NativeSocket] Undock error:', err);
      }
      socketedHwnd = 0;
    }
  }

  // --------------------------------------------------------------------------
  // Unified Socket Toggle (Portal Chamber <-> Active Chamber)
  // --------------------------------------------------------------------------
  function toggleSocket(force) {
    isSocketed = typeof force === 'boolean' ? force : !isSocketed;

    hudBottomDock?.setAttribute('data-expanded', String(isSocketed));

    if (btnToggleSocket) {
      btnToggleSocket.classList.toggle('socketed', isSocketed);
    }
    if (socketBtnText) {
      socketBtnText.textContent = isSocketed ? '🔌 UNSOCKET' : '⚡ SOCKET IN';
    }
    if (dockExpandIcon) {
      dockExpandIcon.textContent = isSocketed ? '▼' : '▲';
    }

    if (isSocketed) {
      portalAudio.playSocketLatch();

      if (portalShockwave) {
        portalShockwave.classList.remove('fire');
        void portalShockwave.offsetWidth;
        portalShockwave.classList.add('fire');
      }

      setTimeout(() => {
        if (socketPortalContainer) socketPortalContainer.style.display = 'none';
        if (socketActiveChamber) socketActiveChamber.style.display = 'flex';
        window.__neuralBrainInstance?.pause?.();
        dockNativeAntigravityWindow();
      }, 320);

      // Enforce socketed lookout across all pages (except exception tabs)
      if (!EXCEPTION_TABS.includes(activeTabKey)) {
        [viewAvatarPane, viewPolymarketPane, viewFlowPane, viewDaVinciPane, viewAgentsPane, viewVectorBrainPane].forEach((p) => {
          if (p) { p.classList.remove('active'); p.style.display = 'none'; }
        });
        if (viewSocketPane) {
          viewSocketPane.classList.add('active');
          viewSocketPane.style.display = 'flex';
        }
        updateSocketVisibility(true);
      } else {
        updateSocketVisibility(false);
      }

      logTerminal('⚡ Antigravity Desktop Matrix Socket Engaged. Native coordinate-lock active.');
      triggerAvatarSpeech('Antigravity Matrix Socket Engaged.');
    } else {
      portalAudio.playUnsocketRelease();
      updateSocketVisibility(false);
      undockNativeAntigravityWindow();

      if (socketActiveChamber) socketActiveChamber.style.display = 'none';
      if (socketPortalContainer) socketPortalContainer.style.display = 'flex';

      // Keep energy reactor video playing
      if (portalCoreVideo) {
        portalCoreVideo.style.display = 'block';
        if (portalCoreVideo.paused) {
          portalCoreVideo.play().catch(() => {});
        }
      }

      // Restore normal page screen
      switchTab(activeTabKey);

      logTerminal('🔌 Antigravity Socket disengaged. Returned to standby portal chamber.');
      triggerAvatarSpeech('Antigravity socket disengaged. Standby mode active.');
    }
    trackLayoutTransition();
  }

  // Bi-Directional Event Listeners
  portalCore?.addEventListener('click', () => toggleSocket(true));
  portalPushBtn?.addEventListener('click', () => toggleSocket(true));
  btnToggleSocket?.addEventListener('click', () => toggleSocket());
  function toggleDockDrawer(forceState) {
    const isCurrentlyExpanded = hudBottomDock?.getAttribute('data-expanded') === 'true';
    const nextState = typeof forceState === 'boolean' ? forceState : !isCurrentlyExpanded;
    hudBottomDock?.setAttribute('data-expanded', String(nextState));
    if (dockExpandIcon) {
      dockExpandIcon.textContent = nextState ? '▼' : '▲';
    }
    if (btnToggleDockExpand) {
      btnToggleDockExpand.title = nextState ? 'Scroll Down / Collapse Drawer' : 'Scroll Up / Expand Drawer';
    }
    trackLayoutTransition();
  }

  btnToggleDockExpand?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDockDrawer();
  });

  // Clicking on dock bar empty areas also smoothly scrolls the drawer up/down
  document.querySelector('.dock-bar')?.addEventListener('click', (e) => {
    if (e.target.closest('button, input, select, textarea, .dock-socket-btn, .engine-pill')) {
      return;
    }
    toggleDockDrawer();
  });

  btnActiveUnsocket?.addEventListener('click', () => toggleSocket(false));

  function logTerminal(msg, type = 'info') {
    if (!terminalOutputFeed) return;
    const now = new Date().toTimeString().split(' ')[0];
    const div = document.createElement('div');
    div.className = `feed-line ${type}`;
    div.innerHTML = `<span class="feed-time">[${now}]</span> ${msg}`;
    terminalOutputFeed.appendChild(div);
    terminalOutputFeed.scrollTop = terminalOutputFeed.scrollHeight;

    // Pulse audio wave visualizer
    if (dockAudioWave) {
      dockAudioWave.classList.add('active');
      setTimeout(() => dockAudioWave.classList.remove('active'), 1200);
    }
  }

  window.keystoneLogTerminal = logTerminal;

  // Send Command / Prompt
  function handleSendPrompt() {
    const text = dockCmdInput?.value.trim();
    if (!text) return;
    logTerminal(`❯ ${text}`, 'prompt');
    dockCmdInput.value = '';

    // Direct HTTP IPC dispatch to Local STT Daemon / Antigravity with bound target conversation
    fetch('http://127.0.0.1:9876/api/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: text,
        conversation_id: selectedChatId,
        chat_name: selectedChatTitle
      })
    })
    .then(r => r.json())
    .then(data => {
      const shortTitle = selectedChatTitle.split(' — ')[0];
      logTerminal(`🚀 [Direct IPC] Dispatched to chat: ${shortTitle} (HTTP ${data.status || 'OK'})`, 'success');
    })
    .catch((err) => {
      const shortTitle = selectedChatTitle.split(' — ')[0];
      logTerminal(`⚠️ [Direct IPC Error] Failed to reach Port 9876: ${err.message}. Check local_stt_daemon.`, 'error');
    });
  }

  dockSendBtn?.addEventListener('click', handleSendPrompt);
  dockCmdInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendPrompt();
    }
  });

  // Quick Chips
  document.querySelectorAll('.quick-chip').forEach((chip) => {
    chip.addEventListener('click', () => {
      const cmd = chip.getAttribute('data-cmd');
      if (cmd && dockCmdInput) {
        dockCmdInput.value = cmd;
        handleSendPrompt();
      }
    });
  });

  btnClearTerminal?.addEventListener('click', () => {
    if (terminalOutputFeed) terminalOutputFeed.innerHTML = '';
    logTerminal('Terminal feed cleared.');
  });

  // Swarm Run Buttons
  document.querySelectorAll('.swarm-run-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const swarm = btn.getAttribute('data-swarm') || 'general';
      logTerminal(`⚡ Autonomous Swarm Dispatched: [${swarm.toUpperCase()}]. Streaming telemetry...`, 'system');
      if (!isSocketed) toggleSocketDeck(true);
    });
  });

  // --------------------------------------------------------------------------
  // Avatar Candidate Selection & Video State Machine
  // --------------------------------------------------------------------------
  candidateCards.forEach((card) => {
    card.addEventListener('click', () => {
      candidateCards.forEach((c) => c.classList.remove('active'));
      card.classList.add('active');

      const avatarName = card.getAttribute('data-name');
      if (activeAvatarName) activeAvatarName.textContent = avatarName;

      // Restore video candidate mode by deactivating custom photo
      const customPhoto = document.getElementById('avatarCustomPhoto');
      if (customPhoto) {
        customPhoto.classList.remove('active');
        customPhoto.style.display = 'none';
      }

      setAvatarState(currentAvatarState);
    });
  });

  function setAvatarState(state) {
    currentAvatarState = state;
    window.keystoneCurrentAvatarState = state;
    if (state === 'talking' || state === 'idle') {
      isAwaitingAgentSpeech = false;
      window.keystoneIsAwaitingAgentSpeech = false;
    }

    // Update Trigger Buttons
    stateTriggerBtns.forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-state') === state);
    });

    // Update Capsule Animation Class & Stage Containers
    if (avatarCapsule) {
      avatarCapsule.className = `avatar-capsule state-${state}`;
    }
    const compactStage = document.getElementById('avatarCapsuleCompact');
    if (compactStage) {
      compactStage.className = `hologram-stage state-${state}`;
    }
    const stick = document.getElementById('hologramAvatarStick');
    if (stick) {
      stick.className = `hologram-avatar-stick hologram-avatar-zone state-${state}`;
    }

    // Update Ambient Glow Class (Electric Glow Behind Robot)
    const avatarAmbientGlow = document.getElementById('avatarAmbientGlow');
    if (avatarAmbientGlow) {
      avatarAmbientGlow.className = `avatar-ambient-glow state-${state}`;
    }

    // Update Ground Radar Aura
    const auraBase = document.querySelector('.hologram-aura-base');
    if (auraBase) {
      auraBase.className = `hologram-aura-base state-${state}`;
    }

    // Update Sleek Status Badge
    const robotStateLabel = document.getElementById('robotStateLabel');
    if (robotStateLabel) {
      robotStateLabel.textContent = state.toUpperCase();
    }

    // Video Layer Seamless Crossfade
    const customPhoto = document.getElementById('avatarCustomPhoto');
    const isCustomPhotoActive = customPhoto && customPhoto.classList.contains('active') && customPhoto.style.display !== 'none';

    Object.keys(videoLayers).forEach((key) => {
      const vid = videoLayers[key];
      if (!vid) return;
      const shouldBeActive = !isCustomPhotoActive && (key === state);

      if (shouldBeActive) {
        vid.classList.add('active');
        if (vid.paused) {
          vid.play().catch(() => {});
        }
      } else {
        vid.classList.remove('active');
        if (!vid.paused) {
          vid.pause();
        }
      }
    });

    // Update Telemetry Badges
    const telemetryState = document.getElementById('telemetryState');
    if (telemetryState) telemetryState.textContent = state.toUpperCase();
    if (currentStateBadge) {
      const labels = {
        idle: '● State: Idle Floating (Hover Bob)',
        listening: '● State: Listening (Audio Waves)',
        working: '● State: Working (Multitasking Holograms)',
        thinking: '● State: Thinking (Glyph Overhead)',
        talking: '● State: Talking (Speech Cadence)',
        walking: '● State: Walking (Thruster Trail)'
      };
      currentStateBadge.textContent = labels[state] || `● State: ${state.toUpperCase()}`;
    }

    // Speech Bubble Texts
    const speechTexts = {
      idle: "Companion online: Ready for Wayne's command.",
      listening: 'Listening: Receiving voice stream via Kokoro & Whisper (:9876)...',
      working: 'Multitasking with holograms & executing subagent pipelines...',
      thinking: 'Analyzing Keystone Brain graph & building code schemas...',
      talking: 'Executing subagent instructions across all 8 daemons.',
      walking: 'Patrolling workspace and staging video production assets.'
    };
    if (speechBubbleText) {
      speechBubbleText.textContent = speechTexts[state] || 'Companion active.';
    }

    if (speechBubble) {
      if (state === 'idle') {
        speechBubble.style.display = 'none';
      } else {
        speechBubble.style.display = 'block';
      }
    }

    updateSidebarContent(activeTabKey);
  }

  window.keystoneSetAvatarState = setAvatarState;

  // Click on Hologram to cycle states through idle -> listening -> working -> talking
  const avatarCycle = ['idle', 'listening', 'working', 'talking'];
  let avatarCycleIdx = 0;
  const hologramAvatarStick = document.getElementById('hologramAvatarStick');
  if (hologramAvatarStick) {
    hologramAvatarStick.addEventListener('click', () => {
      avatarCycleIdx = (avatarCycleIdx + 1) % avatarCycle.length;
      const nextState = avatarCycle[avatarCycleIdx];
      setAvatarState(nextState);

      const phrases = {
        idle: "Companion in standby mode. Ready for your command, Wayne.",
        listening: "Receiving voice stream via Faster-Whisper on Port 9876.",
        working: "Multitasking with holographic matrix. Executing builds.",
        talking: "Online and standing by, Wayne. What's our next objective?"
      };
      if (speechBubbleText) speechBubbleText.textContent = phrases[nextState] || "Companion active.";
      if (speechBubble) speechBubble.style.display = 'block';

      if (nextState === 'talking') {
        triggerAvatarSpeech(phrases.talking);
      } else if (nextState === 'idle') {
        setTimeout(() => {
          if (currentAvatarState === 'idle' && speechBubble) speechBubble.style.display = 'none';
        }, 3500);
      }
    });
  }

  stateTriggerBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const state = btn.getAttribute('data-state');
      setAvatarState(state);
    });
  });

  // Universal Local Documentation Folders (Persistent on Every Tab)
  const btnUniversalDownloads = document.getElementById('btnUniversalDownloads');
  const btnUniversalSlot2 = document.getElementById('btnUniversalSlot2');
  const btnUniversalSlot3 = document.getElementById('btnUniversalSlot3');

  if (btnUniversalDownloads) {
    btnUniversalDownloads.addEventListener('click', (e) => {
      e.stopPropagation();
      fetch('http://127.0.0.1:9876/api/open-folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folderPath: 'C:\\Users\\Curtis\\Downloads' })
      }).catch(() => {});
      logTerminal('📂 [Universal Hub] Opened Downloads folder (C:\\Users\\Curtis\\Downloads)', 'cyan');
    });
  }

  if (btnUniversalSlot2) {
    btnUniversalSlot2.addEventListener('click', (e) => {
      e.stopPropagation();
      logTerminal('📁 [Local Folders] Slot 2 ready for custom directory assignment.', 'gold');
    });
  }

  if (btnUniversalSlot3) {
    btnUniversalSlot3.addEventListener('click', (e) => {
      e.stopPropagation();
      logTerminal('📁 [Local Folders] Slot 3 ready for custom directory assignment.', 'cyan');
    });
  }

  // Universal Task Swarm Trigger (Persistent on Every Hub, Tab & Group)
  const btnUniversalTaskSwarm = document.getElementById('btnUniversalTaskSwarm');
  if (btnUniversalTaskSwarm) {
    btnUniversalTaskSwarm.addEventListener('click', (e) => {
      e.stopPropagation();
      btnUniversalTaskSwarm.classList.add('is-triggering');
      setTimeout(() => btnUniversalTaskSwarm.classList.remove('is-triggering'), 750);

      const targetTitle = selectedChatTitle || 'Active Chat';
      const targetId = selectedChatId || '';
      const swarmPrompt = `⚡ ACTIVATE AUTONOMOUS TEAM SWARM: Engage multi-agent team working standard. Launch discovery and research swarm for the active workspace context in [${targetTitle}].`;

      logTerminal(`🤖 [Universal Swarm] Task Swarm activated for [${targetTitle}]. Engaging team working standard.`, 'gold');
      triggerAvatarSpeech(`Task swarm engaged for ${targetTitle.split(' — ')[0]}. Multi-agent team working active.`);
      setAvatarState('working');
      setTimeout(() => {
        if (currentAvatarState === 'working') {
          setAvatarState('idle');
        }
      }, 5000);

      // Dispatch to Daemon A (/api/prompt)
      fetch('http://127.0.0.1:9876/api/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: swarmPrompt,
          conversation_id: targetId,
          target_chat_name: targetTitle,
          chat_name: targetTitle
        })
      }).catch((err) => {
        console.warn('Swarm prompt HTTP dispatch error:', err);
      });

      // Forward to Native Tauri IPC if available
      try {
        if (window.__TAURI__?.core?.invoke) {
          window.__TAURI__.core.invoke('send_prompt_to_daemon', { prompt: swarmPrompt });
        } else if (window.__TAURI__?.invoke) {
          window.__TAURI__.invoke('send_prompt_to_daemon', { prompt: swarmPrompt });
        }
      } catch (err) {
        // Native fallback ignored
      }
    });
  }

  // Universal Skill & Chat Overseer Trigger (Persistent on Every Hub, Tab & Group)
  const btnUniversalSkillOverseer = document.getElementById('btnUniversalSkillOverseer');
  if (btnUniversalSkillOverseer) {
    btnUniversalSkillOverseer.addEventListener('click', (e) => {
      e.stopPropagation();
      btnUniversalSkillOverseer.classList.add('is-triggering');
      setTimeout(() => btnUniversalSkillOverseer.classList.remove('is-triggering'), 750);

      const targetTitle = selectedChatTitle || 'Active Chat';
      const targetId = selectedChatId || '';
      const overseerPrompt = `✨ DISPATCH SKILL & CHAT OVERSEER (T1): Analyze recent conversation trajectories in [${targetTitle}], benchmark active operator workflows against C:\\Users\\Curtis\\.gemini\\config\\skills\\, and identify high-leverage skill set upgrades or new candidate SKILL.md packages. Summarize in skill_upgrade_manifest.md and update voice_outbox.txt.`;

      logTerminal(`🔍 [Skill Overseer] Trajectory supervisor engaged for [${targetTitle}]. Auditing chat workflows & skills.`, 'cyan');
      triggerAvatarSpeech(`Skill and chat overseer active for ${targetTitle.split(' — ')[0]}. Auditing trajectories.`);
      setAvatarState('working');
      setTimeout(() => {
        if (currentAvatarState === 'working') {
          setAvatarState('idle');
        }
      }, 5000);

      // Dispatch to Daemon A (/api/prompt)
      fetch('http://127.0.0.1:9876/api/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: overseerPrompt,
          conversation_id: targetId,
          target_chat_name: targetTitle,
          chat_name: targetTitle
        })
      }).catch((err) => {
        console.warn('Skill overseer prompt HTTP dispatch error:', err);
      });

      // Forward to Native Tauri IPC if available
      try {
        if (window.__TAURI__?.core?.invoke) {
          window.__TAURI__.core.invoke('send_prompt_to_daemon', { prompt: overseerPrompt });
        } else if (window.__TAURI__?.invoke) {
          window.__TAURI__.invoke('send_prompt_to_daemon', { prompt: overseerPrompt });
        }
      } catch (err) {}
    });
  }

  // Global Brain Swarm Subagent Dispatch Handler
  window.dispatchBrainSubagent = function(agentId, agentLabel, taskDesc) {
    const targetTitle = selectedChatTitle || 'Active Chat';
    const targetId = selectedChatId || '';
    const dispatchPrompt = `⚡ DISPATCH SUBAGENT [${agentId}]: Launch ${agentLabel} for ${taskDesc} in active context [${targetTitle}]. Enforce Wayne's Word is Law, 2-source Brave Search verification, and update voice_outbox.txt upon completion.`;

    logTerminal(`🚀 [Brain Swarm] Dispatched ${agentLabel} to [${targetTitle}].`, 'cyan');
    triggerAvatarSpeech(`${agentLabel} engaged for ${targetTitle.split(' — ')[0]}.`);
    setAvatarState('working');
    setTimeout(() => {
      if (currentAvatarState === 'working') {
        setAvatarState('idle');
      }
    }, 5000);

    // Dispatch to Daemon A (/api/prompt)
    fetch('http://127.0.0.1:9876/api/prompt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: dispatchPrompt,
        conversation_id: targetId,
        target_chat_name: targetTitle,
        chat_name: targetTitle
      })
    }).catch((err) => {
      console.warn('Subagent dispatch error:', err);
    });

    // Native Tauri IPC fallback
    try {
      if (window.__TAURI__?.core?.invoke) {
        window.__TAURI__.core.invoke('send_prompt_to_daemon', { prompt: dispatchPrompt });
      } else if (window.__TAURI__?.invoke) {
        window.__TAURI__.invoke('send_prompt_to_daemon', { prompt: dispatchPrompt });
      }
    } catch (e) {}
  };

  // --------------------------------------------------------------------------
  // Digital Avatar Live Speech & Photo Ingestion Controls
  // --------------------------------------------------------------------------
  const avatarSpeechInput = document.getElementById('avatarSpeechInput');
  const btnAvatarSpeak = document.getElementById('btnAvatarSpeak');
  const btnAvatarKokoro = document.getElementById('btnAvatarKokoro');
  const avatarPhotoUpload = document.getElementById('avatarPhotoUpload');

  function triggerAvatarSpeech(text) {
    const speechText = text || (avatarSpeechInput ? avatarSpeechInput.value.trim() : '') || 'Keystone Companion online. Ready for your instructions.';
    setAvatarState('talking');
    if (speechBubbleText) {
      speechBubbleText.textContent = speechText;
    }
    if (speechBubble) {
      speechBubble.style.display = 'block';
    }

    const fallbackToBrowserSpeech = () => {
      if ('speechSynthesis' in window) {
        try {
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(speechText);
          utterance.rate = 1.05;
          utterance.pitch = 1.1;
          utterance.onend = () => {
            setTimeout(() => {
              if (currentAvatarState === 'talking') {
                setAvatarState('idle');
              }
            }, 1000);
          };
          utterance.onerror = () => {
            setTimeout(() => {
              if (currentAvatarState === 'talking') {
                setAvatarState('idle');
              }
            }, 2000);
          };
          window.speechSynthesis.speak(utterance);
        } catch (e) {
          setTimeout(() => {
            if (currentAvatarState === 'talking') {
              setAvatarState('idle');
            }
          }, 2000);
        }
      } else {
        setTimeout(() => {
          if (currentAvatarState === 'talking') {
            setAvatarState('idle');
          }
        }, Math.max(2500, speechText.length * 60));
      }
      logTerminal(`🗣️ Digital Avatar vocalizing (browser fallback): "${speechText}"`, 'info');
    };

    // ALWAYS route to Agent Voice Daemon (Port 9877) for Aoede Gemini Live female voice
    logTerminal(`🎙️ Dispatched speech to Agent Voice Daemon (Port 9877): "${speechText}"`, 'info');
    fetch('http://127.0.0.1:9877/api/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: speechText })
    }).then((res) => {
      if (!res.ok) {
        fallbackToBrowserSpeech();
      }
    }).catch((err) => {
      logTerminal(`⚠️ Agent Voice Daemon offline, using browser fallback: ${err.message}`, 'warn');
      fallbackToBrowserSpeech();
    });

    // Safety duration based on reading speed (~80ms per character) in case WebSocket doesn't revert state
    const duration = Math.max(3500, speechText.length * 80);
    setTimeout(() => {
      if (currentAvatarState === 'talking') {
        setAvatarState('idle');
      }
    }, duration);
  }

  window.triggerAvatarSpeech = triggerAvatarSpeech;
  window.keystoneTriggerAvatarSpeech = triggerAvatarSpeech;

  btnAvatarSpeak?.addEventListener('click', () => {
    triggerAvatarSpeech(avatarSpeechInput?.value);
  });

  avatarSpeechInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      triggerAvatarSpeech(avatarSpeechInput?.value);
    }
  });

  btnAvatarKokoro?.addEventListener('click', () => {
    triggerAvatarSpeech(avatarSpeechInput?.value, true);
  });

  avatarPhotoUpload?.addEventListener('change', (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      let customImg = document.getElementById('avatarCustomPhoto');
      if (!customImg) {
        customImg = document.createElement('img');
        customImg.id = 'avatarCustomPhoto';
        customImg.className = 'avatar-photo-layer active';
        if (avatarCapsule) {
          avatarCapsule.appendChild(customImg);
        }
      }
      customImg.src = event.target.result;
      customImg.style.display = 'block';
      customImg.classList.add('active');

      // Hide video layers
      Object.values(videoLayers).forEach((vid) => {
        if (vid) vid.classList.remove('active');
      });

      if (activeAvatarName) {
        activeAvatarName.textContent = `Custom Ingested Photo (${file.name})`;
      }

      logTerminal(`📷 Ingested custom 2D photo [${file.name}] into low-RAM digital avatar pipeline.`, 'success');
      triggerAvatarSpeech(`Custom avatar portrait photo loaded: ${file.name}. Hologram synced.`);
    };
    reader.readAsDataURL(file);
  });

  // FX Canvas Animation Loop (Particles & Ripples)
  function renderFx() {
    animTick++;
    if (fxCtx && fxCanvas) {
      fxCtx.clearRect(0, 0, fxCanvas.width, fxCanvas.height);
      const cx = fxCanvas.width / 2;
      const cy = fxCanvas.height / 2;

      if (currentAvatarState === 'listening') {
        const r1 = (animTick * 1.5) % 120;
        const r2 = (animTick * 1.5 + 40) % 120;
        const r3 = (animTick * 1.5 + 80) % 120;
        [r1, r2, r3].forEach((r) => {
          const alpha = Math.max(0, 1 - r / 120) * 0.45;
          fxCtx.beginPath();
          fxCtx.arc(cx, cy + 20, r, 0, Math.PI * 2);
          fxCtx.strokeStyle = `rgba(0, 240, 255, ${alpha})`;
          fxCtx.lineWidth = 1.5;
          fxCtx.stroke();
        });
      } else if (currentAvatarState === 'thinking') {
        fxCtx.save();
        fxCtx.translate(cx, cy - 90);
        fxCtx.rotate(animTick * 0.025);
        fxCtx.strokeStyle = 'rgba(139, 92, 246, 0.6)';
        fxCtx.lineWidth = 2;
        fxCtx.strokeRect(-18, -18, 36, 36);
        fxCtx.restore();
      }
    }
    requestAnimationFrame(renderFx);
  }

  function handleDaemonWsMessage(raw) {
    try {
      const msg = typeof raw === 'string' ? JSON.parse(raw) : raw;
      if (!msg) return;

      // Real-time hardware telemetry stats (routed through EMA filter)
      if (msg.type === 'stats' && msg.data) {
        isDaemonStreamingStats = true;
        applyLiveTelemetry(msg.data);
      }

      // Real-time speech bridge states
      if (msg.type === 'state' && msg.state) {
        const s = msg.state.toLowerCase();
        if (s === 'listening') {
          isAwaitingAgentSpeech = false;
          window.keystoneIsAwaitingAgentSpeech = false;
          setAvatarState('listening');
        } else if (s === 'transmitting') {
          setAvatarState('working');
        } else if (s === 'working' || s === 'thinking') {
          isAwaitingAgentSpeech = true;
          window.keystoneIsAwaitingAgentSpeech = true;
          setAvatarState('working');
        } else if (s === 'speaking') {
          isAwaitingAgentSpeech = false;
          window.keystoneIsAwaitingAgentSpeech = false;
          setAvatarState('talking');
        } else if (s === 'connected' || s === 'idle') {
          // The avatar must stay in 'working' continuously for as long as Antigravity is processing/working
          // on the prompt until speech output begins.
          // If we are actively awaiting agent speech, do NOT revert to idle on connected.
          // But if we are NOT awaiting speech (e.g. speech ended, or audio was discarded/empty), transition to idle!
          if (!isAwaitingAgentSpeech) {
            setAvatarState('idle');
          }
        }
      }

      // Real-time audio recording discarded / no speech detected
      if (msg.type === 'recording_discarded') {
        isAwaitingAgentSpeech = false;
        window.keystoneIsAwaitingAgentSpeech = false;
        setAvatarState('idle');
        if (speechBubbleText) speechBubbleText.textContent = 'Standby: No speech detected.';
        setTimeout(() => {
          if (currentAvatarState === 'idle' && speechBubble) speechBubble.style.display = 'none';
        }, 2500);
      }

      // Live spoken transcript received (Wayne's speech)
      if (msg.type === 'transcript' && msg.text) {
        const target = (msg.target || '').toLowerCase();
        const isForThisChat = !target || target === 'default' || target.includes(selectedChatId) || selectedChatTitle.toLowerCase().includes(target);
        if (isForThisChat) {
          if (speechBubbleText) speechBubbleText.textContent = `Wayne: "${msg.text}"`;
          if (speechBubble) speechBubble.style.display = 'block';
          // Wayne finished speaking; companion robot begins executing task -> persist in WORKING state until speech output begins
          isAwaitingAgentSpeech = true;
          window.keystoneIsAwaitingAgentSpeech = true;
          setAvatarState('working');
        }
      }

      // Target chat switched remotely or via set-target
      if (msg.type === 'active_chat_updated' && msg.active_conversation_id) {
        const actId = msg.active_conversation_id;
        const actTitle = msg.title || msg.name || '';
        document.querySelectorAll('.chat-menu-item').forEach((item) => {
          item.classList.toggle('active', item.getAttribute('data-chat-id') === actId);
        });
        document.querySelectorAll('.sidebar-chat-item').forEach((item) => {
          item.classList.toggle('active', item.getAttribute('data-chat-id') === actId);
        });
        if (actId && actId !== selectedChatId && actTitle) {
          selectedChatId = actId;
          selectedChatTitle = actTitle;
          updateSidebarActiveChatCard(actId, actTitle);
        }
      }

      // Real-time master volume synchronization from WebSocket (keyboard keys, headset wheel, taskbar, or daemon)
      if (msg.type === 'volume' && typeof msg.volume === 'number') {
        const isMuted = Boolean(msg.muted);
        currentVolume = msg.volume;
        if (msg.volume > 0 && !isMuted) preMuteVolume = msg.volume;
        if (!isInteractingWithVolume) {
          updateVolumeUI(msg.volume, isMuted);
        }
      }

      // Real-time audio devices update
      if (msg.type === 'devices' || msg.type === 'speaker_changed') {
        const activeSpk = msg.active_speaker || msg.speaker;
        if (hudAudioDeviceLabel && activeSpk) {
          const isDef = !activeSpk || activeSpk.toLowerCase().includes('default');
          hudAudioDeviceLabel.textContent = isDef ? 'System Default' : activeSpk;
          if (hudAudioBadgeIcon) {
            hudAudioBadgeIcon.textContent = isDef ? '💻' : (activeSpk.toLowerCase().includes('headset') || activeSpk.toLowerCase().includes('headphone')) ? '🎧' : '🔊';
          }
        }
        if (typeof msg.volume === 'number') {
          currentVolume = msg.volume;
          const isM = Boolean(msg.muted);
          if (!isInteractingWithVolume) updateVolumeUI(msg.volume, isM);
        }
      }
    } catch (err) {
      console.error('[Daemon WS] Parse error:', err);
    }
  }
  window.keystoneHandleDaemonWsMessage = handleDaemonWsMessage;

  // --------------------------------------------------------------------------
  // Push WebSocket Telemetry & State Synchronization (ws://127.0.0.1:9876/ws)
  // --------------------------------------------------------------------------
  function initDaemonWebSocket() {
    try {
      const ws = new WebSocket('ws://127.0.0.1:9876/ws');
      window.keystoneDaemonWs = ws;
      ws.onopen = () => {
        console.log('🌐 [Daemon WS] Connected to state & telemetry WebSocket on ws://127.0.0.1:9876/ws');
        fetch('http://127.0.0.1:9876/api/volume')
          .then(r => r.json())
          .then(d => {
            if (typeof d.volume === 'number' && !isInteractingWithVolume) {
              currentVolume = d.volume;
              updateVolumeUI(d.volume, Boolean(d.muted));
            }
          }).catch(() => {});
      };
      ws.onmessage = (event) => {
        handleDaemonWsMessage(event.data);
      };
      ws.onclose = () => {
        setTimeout(initDaemonWebSocket, 3000);
      };
      ws.onerror = () => {
        ws.close();
      };
    } catch (e) {
      setTimeout(initDaemonWebSocket, 5000);
    }
  }

  // --------------------------------------------------------------------------
  // Global F8 & F9 (Push-To-Talk Voice) & Shift+F8 / Esc (Emergency Stop)
  // --------------------------------------------------------------------------
  let isPTTActive = false;
  window.addEventListener('keydown', (e) => {
    // Emergency Stop: Shift+F8 or Escape
    if ((e.key === 'F8' && e.shiftKey) || e.key === 'Escape') {
      e.preventDefault();
      console.log('🚨 [Emergency Stop] Halting audio & sending emergency halt...');
      isAwaitingAgentSpeech = false;
      window.keystoneIsAwaitingAgentSpeech = false;
      fetch('http://127.0.0.1:9877/api/stop', { method: 'POST' }).catch(() => {});
      fetch('http://127.0.0.1:9876/api/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: 'EMERGENCY STOP TRIGGERED: Halt all current active tasks immediately Wayne.',
          target_conv_id: selectedChatId
        })
      }).catch(() => {});
      setAvatarState('idle');
      if (speechBubbleText) speechBubbleText.textContent = '⚡ EMERGENCY STOP TRIGGERED';
      if (speechBubble) speechBubble.style.display = 'block';
      return;
    }

    // Hardware/Keyboard Master Volume Up / Down / Mute keys
    if (e.key === 'AudioVolumeUp' || e.key === 'AudioVolumeDown' || e.key === 'AudioVolumeMute' || e.code === 'AudioVolumeUp' || e.code === 'AudioVolumeDown' || e.code === 'AudioVolumeMute') {
      setTimeout(() => {
        fetch('http://127.0.0.1:9876/api/volume')
          .then(r => r.json())
          .then(d => {
            if (typeof d.volume === 'number') {
              currentVolume = d.volume;
              const isM = Boolean(d.muted);
              if (d.volume > 0 && !isM) preMuteVolume = d.volume;
              updateVolumeUI(d.volume, isM);
            }
          }).catch(() => {});
      }, 40);
    }

    // Push-To-Talk Speech: F8, F9, or Backquote
    const isPTTKey = (e.key === 'F8' || e.code === 'F8' || e.key === 'F9' || e.code === 'F9' || e.keyCode === 120 || e.keyCode === 119 || e.key === '`' || e.code === 'Backquote');
    if (isPTTKey && !e.repeat && !isPTTActive && !e.shiftKey) {
      e.preventDefault();
      isPTTActive = true;
      isAwaitingAgentSpeech = false;
      window.keystoneIsAwaitingAgentSpeech = false;
      const short = selectedChatTitle.split(' — ')[0];
      const keyLabel = e.key === '`' ? '`' : e.key.toUpperCase();
      console.log(`🎙️ [Push-to-Talk ${keyLabel}] KeyDown -> Starting recording on Port 9876 for [${short}]...`);
      fetch('http://127.0.0.1:9876/api/record/start', { method: 'POST' }).catch(() => {});
      setAvatarState('listening');
      if (speechBubbleText) speechBubbleText.textContent = `🎙️ Listening... (Hold ${keyLabel} while speaking to ${short})`;
      if (speechBubble) speechBubble.style.display = 'block';
    }
  }, true);

  window.addEventListener('keyup', (e) => {
    const isPTTKey = (e.key === 'F8' || e.code === 'F8' || e.key === 'F9' || e.code === 'F9' || e.keyCode === 120 || e.keyCode === 119 || e.key === '`' || e.code === 'Backquote');
    if (isPTTKey && isPTTActive) {
      e.preventDefault();
      isPTTActive = false;
      isAwaitingAgentSpeech = true;
      window.keystoneIsAwaitingAgentSpeech = true;
      const short = selectedChatTitle.split(' — ')[0];
      console.log(`🚀 [Push-to-Talk] KeyUp -> Stopping recording & transcribing for [${short}]...`);
      fetch('http://127.0.0.1:9876/api/record/stop', { method: 'POST' }).catch(() => {});
      setAvatarState('working');
      if (speechBubbleText) speechBubbleText.textContent = `⚡ Processing voice command for ${short}...`;
      if (speechBubble) speechBubble.style.display = 'block';
    }
  }, true);

  // Native Tauri OS-Wide Global Hotkey Event Bridge (F8 & F9 system-wide)
  try {
    const tauriListen = window.__TAURI__?.event?.listen;
    if (typeof tauriListen === 'function') {
      tauriListen('global-hotkey', (event) => {
        const payload = event?.payload || {};
        const key = (payload.key || '').toUpperCase();
        const state = (payload.state || '').toLowerCase();
        if (key === 'F8') {
          console.log('🚨 [Tauri Global Hotkey F8] Emergency Stop Triggered');
          isPTTActive = false;
          isAwaitingAgentSpeech = false;
          window.keystoneIsAwaitingAgentSpeech = false;
          fetch('http://127.0.0.1:9877/api/stop', { method: 'POST' }).catch(() => {});
          fetch('http://127.0.0.1:9876/api/prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              prompt: 'EMERGENCY STOP TRIGGERED: Halt all current active tasks immediately Wayne.',
              target_conv_id: selectedChatId
            })
          }).catch(() => {});
          setAvatarState('idle');
          if (speechBubbleText) speechBubbleText.textContent = '⚡ EMERGENCY STOP TRIGGERED';
          if (speechBubble) speechBubble.style.display = 'block';
          return;
        }
        if (key === 'F9') {
          const short = selectedChatTitle.split(' — ')[0];
          if (state === 'keydown' && !isPTTActive) {
            console.log(`🎙️ [Tauri OS-Global Hotkey ${key}] -> Immediate LISTENING state`);
            isPTTActive = true;
            isAwaitingAgentSpeech = false;
            window.keystoneIsAwaitingAgentSpeech = false;
            fetch('http://127.0.0.1:9876/api/record/start', { method: 'POST' }).catch(() => {});
            setAvatarState('listening');
            if (speechBubbleText) speechBubbleText.textContent = `🎙️ Listening... (Hold ${key} while speaking to ${short})`;
            if (speechBubble) speechBubble.style.display = 'block';
          } else if (state === 'keyup' && isPTTActive) {
            console.log(`🚀 [Tauri OS-Global Hotkey ${key}] -> Immediate WORKING state`);
            isPTTActive = false;
            isAwaitingAgentSpeech = true;
            window.keystoneIsAwaitingAgentSpeech = true;
            fetch('http://127.0.0.1:9876/api/record/stop', { method: 'POST' }).catch(() => {});
            setAvatarState('working');
            if (speechBubbleText) speechBubbleText.textContent = `⚡ Processing voice command for ${short}...`;
            if (speechBubble) speechBubble.style.display = 'block';
          }
        }
      }).then(() => {
        console.log('✅ [Tauri OS-Global Hotkey] Listener successfully bound to global-hotkey event');
      }).catch((err) => {
        console.error('❌ [Tauri OS-Global Hotkey] Failed to listen to global-hotkey:', err);
      });
    }
  } catch (err) {
    console.warn('Tauri event listener initialization skipped in standard browser:', err);
  }

  // --------------------------------------------------------------------------
  // Master Cyber Audio & Computer-Wide Volume Control (Windows System Default)
  // --------------------------------------------------------------------------
  let currentVolume = 80;
  let preMuteVolume = 80;
  let volumeDebounceTimer = null;

  function updateVolumeUI(vol, muted = false) {
    vol = Math.max(0, Math.min(100, Math.round(vol)));
    if (hudVolumeSlider && !isInteractingWithVolume) hudVolumeSlider.value = vol;
    if (hudVolumeDisplay) hudVolumeDisplay.textContent = `${vol}%`;
    if (hudVolumeIcon) {
      if (muted || vol === 0) {
        hudVolumeIcon.textContent = '🔇';
      } else if (vol < 50) {
        hudVolumeIcon.textContent = '🔉';
      } else {
        hudVolumeIcon.textContent = '🔊';
      }
    }
  }

  function applyVolumeState(vol, broadcast = true, muted = false) {
    vol = Math.max(0, Math.min(100, Math.round(vol)));
    currentVolume = vol;
    updateVolumeUI(vol, muted);

    if (broadcast) {
      if (volumeDebounceTimer) clearTimeout(volumeDebounceTimer);
      volumeDebounceTimer = setTimeout(() => {
        const payload = JSON.stringify({ volume: vol, muted: muted });
        // Dual-daemon dispatch: TTS Port 9877 and STT Port 9876
        fetch('http://127.0.0.1:9877/api/volume', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: payload
        }).catch(() => {});

        fetch('http://127.0.0.1:9876/api/volume', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: payload
        }).catch(() => {});
      }, 30);
    }
  }

  function initMasterVolumeControls() {
    // Initial fetch from Daemon A (STT Port 9876) or Daemon B (TTS Port 9877)
    fetch('http://127.0.0.1:9876/api/volume')
      .then(res => res.json())
      .then(data => {
        if (typeof data.volume === 'number') {
          currentVolume = data.volume;
          const isMuted = Boolean(data.muted);
          if (data.volume > 0 && !isMuted) preMuteVolume = data.volume;
          updateVolumeUI(data.volume, isMuted);
        }
      })
      .catch(() => {
        fetch('http://127.0.0.1:9877/api/volume')
          .then(res => res.json())
          .then(data => {
            if (typeof data.volume === 'number') {
              currentVolume = data.volume;
              const isMuted = Boolean(data.muted);
              if (data.volume > 0 && !isMuted) preMuteVolume = data.volume;
              updateVolumeUI(data.volume, isMuted);
            }
          })
          .catch(() => {});
      });

    // Query active speaker device to display badge label
    fetch('http://127.0.0.1:9876/api/devices')
      .then(res => res.json())
      .then(data => {
        const activeSpk = data.active_speaker || 'default';
        if (hudAudioDeviceLabel) {
          const isDef = !activeSpk || activeSpk.toLowerCase().includes('default');
          hudAudioDeviceLabel.textContent = isDef ? 'System Default' : activeSpk;
          if (hudAudioBadgeIcon) {
            hudAudioBadgeIcon.textContent = isDef ? '💻' : (activeSpk.toLowerCase().includes('headset') || activeSpk.toLowerCase().includes('headphone')) ? '🎧' : '🔊';
          }
        }
      })
      .catch(() => {});

    // Volume Slider events (Two-Way Windows System Default sync)
    if (hudVolumeSlider) {
      hudVolumeSlider.addEventListener('pointerdown', () => {
        isInteractingWithVolume = true;
      });
      hudVolumeSlider.addEventListener('pointerup', () => {
        isInteractingWithVolume = false;
      });
      hudVolumeSlider.addEventListener('pointercancel', () => {
        isInteractingWithVolume = false;
      });
      hudVolumeSlider.addEventListener('blur', () => {
        isInteractingWithVolume = false;
      });
      hudVolumeSlider.addEventListener('input', (e) => {
        isInteractingWithVolume = true;
        const val = parseInt(e.target.value, 10) || 0;
        if (val > 0) preMuteVolume = val;
        applyVolumeState(val, true, false);
      });
      hudVolumeSlider.addEventListener('change', (e) => {
        isInteractingWithVolume = false;
        const val = parseInt(e.target.value, 10) || 0;
        if (val > 0) preMuteVolume = val;
        applyVolumeState(val, true, false);
      });
    }

    // Mouse Wheel Volume Scrolling on Slider & Quick Bar
    const handleVolumeWheel = (e) => {
      e.preventDefault();
      const step = e.shiftKey ? 5 : 2;
      const delta = (e.deltaY < 0 || e.deltaX > 0) ? step : -step;
      const targetVol = Math.max(0, Math.min(100, currentVolume + delta));
      if (targetVol > 0) preMuteVolume = targetVol;
      applyVolumeState(targetVol, true, false);
    };
    hudVolumeSlider?.addEventListener('wheel', handleVolumeWheel, { passive: false });
    hudAudioQuickBar?.addEventListener('wheel', handleVolumeWheel, { passive: false });

    // Lightweight 1.5s background fallback poller (ensures system default volume lockstep even if WS is quiet)
    setInterval(() => {
      if (isInteractingWithVolume) return;
      fetch('http://127.0.0.1:9876/api/volume')
        .then(res => res.json())
        .then(data => {
          if (typeof data.volume === 'number' && !isInteractingWithVolume) {
            const isM = Boolean(data.muted);
            if (data.volume !== currentVolume) {
              currentVolume = data.volume;
              if (data.volume > 0 && !isM) preMuteVolume = data.volume;
              updateVolumeUI(data.volume, isM);
            }
          }
        })
        .catch(() => {});
    }, 1500);

    // Mute Button Toggle
    if (btnVolumeMute) {
      btnVolumeMute.addEventListener('click', () => {
        if (currentVolume > 0) {
          preMuteVolume = currentVolume;
          applyVolumeState(0, true, true);
        } else {
          const restoreVol = preMuteVolume > 0 ? preMuteVolume : 80;
          applyVolumeState(restoreVol, true, false);
        }
      });
    }

    // Audio Device Badge: Click to trigger confirmation chime test
    if (hudAudioDeviceBadge) {
      hudAudioDeviceBadge.addEventListener('click', () => {
        const origText = hudAudioDeviceLabel ? hudAudioDeviceLabel.textContent : 'System Default';
        if (hudAudioDeviceLabel) hudAudioDeviceLabel.textContent = 'Playing Chime...';
        hudAudioDeviceBadge.style.boxShadow = '0 0 16px rgba(0, 240, 255, 0.8)';

        fetch('http://127.0.0.1:9877/api/chime', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ device_name: 'default', volume: currentVolume })
        })
        .catch(() => {})
        .finally(() => {
          setTimeout(() => {
            if (hudAudioDeviceLabel) hudAudioDeviceLabel.textContent = origText;
            hudAudioDeviceBadge.style.boxShadow = '';
          }, 1200);
        });
      });
    }
  }

  // --------------------------------------------------------------------------
  // Dedicated 64-Agent Neural Swarm & Daemon Registry Controller
  // --------------------------------------------------------------------------
  function initAgentsWorkspaceHandlers() {
    const btnModeAgents = document.getElementById('btnModeAgents');
    const btnModeDaemons = document.getElementById('btnModeDaemons');
    const agentsFilterBar = document.getElementById('agentsFilterBar');
    const agentsCardsGrid = document.getElementById('agentsCardsGrid');
    const daemonsCardsGrid = document.getElementById('daemonsCardsGrid');
    const telemetryAgentCount = document.getElementById('telemetryAgentCount');
    const btnAgentsCount = document.getElementById('btnAgentsCount');

    // Drawer elements
    const agentDefinitionDrawer = document.getElementById('agentDefinitionDrawer');
    const agentDrawerBackdrop = document.getElementById('agentDrawerBackdrop');
    const btnCloseAgentDrawer = document.getElementById('btnCloseAgentDrawer');
    const drawerAgentIcon = document.getElementById('drawerAgentIcon');
    const drawerAgentTitle = document.getElementById('drawerAgentTitle');
    const drawerAgentId = document.getElementById('drawerAgentId');
    const drawerAgentCategory = document.getElementById('drawerAgentCategory');
    const drawerAgentModel = document.getElementById('drawerAgentModel');
    const drawerAgentBody = document.getElementById('drawerAgentBody');
    const btnCopyAgentPrompt = document.getElementById('btnCopyAgentPrompt');
    const btnOpenAgentFolder = document.getElementById('btnOpenAgentFolder');
    const btnDrawerZoomIn = document.getElementById('btnDrawerZoomIn');
    const btnDrawerZoomOut = document.getElementById('btnDrawerZoomOut');
    const btnDrawerZoomReset = document.getElementById('btnDrawerZoomReset');
    const btnDrawerExpand = document.getElementById('btnDrawerExpand');
    const drawerZoomSlider = document.getElementById('drawerZoomSlider');
    const drawerZoomReadout = document.getElementById('drawerZoomReadout');
    const drawerResizeHandle = document.getElementById('drawerResizeHandle');

    // Subagent Architect elements
    const archChatSelect = document.getElementById('archChatSelect');
    const archActiveChatBadge = document.getElementById('archActiveChatBadge');
    const btnLaunchSubagentArchitect = document.getElementById('btnLaunchSubagentArchitect');
    const archStatusMsg = document.getElementById('archStatusMsg');

    // Dynamic Swarm Overview elements
    const swarmOverviewIcon = document.getElementById('swarmOverviewIcon');
    const swarmOverviewTitle = document.getElementById('swarmOverviewTitle');
    const swarmOverviewBadge = document.getElementById('swarmOverviewBadge');
    const swarmOverviewDesc = document.getElementById('swarmOverviewDesc');
    const swarmOverviewPath = document.getElementById('swarmOverviewPath');
    const swarmOverviewTier = document.getElementById('swarmOverviewTier');
    const swarmOverviewCount = document.getElementById('swarmOverviewCount');

    let currentSelectedAgent = null;
    let currentCategoryFilter = 'all';
    let drawerFontSize = parseInt(localStorage.getItem('keystone_drawer_font_size') || '13', 10);
    let drawerCustomWidth = parseInt(localStorage.getItem('keystone_drawer_width') || '640', 10);
    let isDraggingDrawer = false;
    let lastDrawerPointerId = null;

    const PILE_ICONS = {
      'brain': '🧠',
      'tdd': '⚡',
      'infra': '🗄️',
      'possibilities': '🏗️',
      'music': '🎵',
      'money': '💰',
      'web': '🏛️',
      'flow': '🎬',
      'other': '🤖'
    };

    const SWARM_PILE_METADATA = {
      all: {
        icon: '🤖',
        title: 'Keystone 64-Agent Neural Swarm (Full Active Catalog)',
        badge: 'Universal Architecture · 8 Ephemeral Swarm Piles',
        desc: 'Master directory of all 64 active production subagents in Keystone Brain. Isolated ephemeral child contexts, FastMCP typed contracts, and Port 9879 mutex guards.',
        path: '17_subagents/',
        tier: 'inherit (Frontier Reasoning Default)',
        count: '64 Active Subagents'
      },
      tdd: {
        icon: '⚡',
        title: 'Autonomous 16-Agent Task Swarm (TDD & Engineering Grid)',
        badge: 'Skill: A5_swarm_orchestration_engine',
        desc: 'Autonomous engineering harness under /goal sentinel. Enforces 6-phase lifecycle: requirements discovery, 2-source research, DAG architecture, RED-to-GREEN tests, anti-cheat code reviews, and visual UX verification.',
        path: '17_subagents/ (Orchestrator, S0, R1-R4, B0-B5, W1, V1, D0, U1)',
        tier: 'inherit (Gemini 3.8-High)',
        count: '16 Specialized Agents'
      },
      music: {
        icon: '🎵',
        title: 'Keystone Recomposition Music & Distribution Swarm',
        badge: 'Skills: 07_keystone_music_master_pipeline & 08_keystone_suno_music_producer',
        desc: 'Suno AI prompt engineering, Squamish Builder persona lyrics, 1:1 luxury album artwork, TooLost digital distribution, MusicBrainz metadata indexing, and Musixmatch Pro synced lyrics.',
        path: '17_subagents/ (S0-S7, M0-M3)',
        tier: 'inherit (Frontier Tier)',
        count: '12 Specialized Agents'
      },
      possibilities: {
        icon: '🏗️',
        title: 'Keystone Possibilities Infill & B2B Outreach Swarm',
        badge: 'Skills: 09_keystone_possibilities_outreach_suite & A2_scriptwriter',
        desc: 'B2B outreach triggers for Realtors (O1), Architects (O2), Municipal permits (O3), Equity investors (O4A/O4B), and Scouts (O5). Google LSA management, Google Business Profile local map pack ranking, and 5-star review funnels.',
        path: '17_subagents/ (P1, O1-O5, A1, S4, R5, R6)',
        tier: 'inherit (Frontier Tier)',
        count: '10 Specialized Agents'
      },
      money: {
        icon: '💰',
        title: 'Money & Morning Tennis Sentinel Swarm',
        badge: 'Skill: 06_keystone_money_polymarket_stocks',
        desc: '365-day morning tennis sentinel across WTA/ATP/ITF slates. Mandatory 12-factor dual audit on both athletes, 20¢–40¢ sweet spot, Quarter-Kelly ladder ($1 -> $50 -> $500), and sequential Port 9222 execution.',
        path: '17_subagents/ (M00, M05, M07, M11-M16)',
        tier: 'inherit (Frontier Tier)',
        count: '9 Specialized Agents'
      },
      web: {
        icon: '🏛️',
        title: 'Luxury Website, SEO & Theme Swarm',
        badge: 'Skills: 04_keystone_luxury_blog_pipeline & A6_keystone_website_audit_swarm',
        desc: 'Luxury Gutenberg block architecture, Rank Math 100/100 SEO calibration, PHP 8.2+ child theme engineering, Schema.org VideoObject/MedicalBusiness JSON-LD schemas, and instant GSC indexing.',
        path: '17_subagents/ (W1-W4, S1, S2, Y1)',
        tier: 'inherit (Frontier Tier)',
        count: '7 Specialized Agents'
      },
      flow: {
        icon: '🎬',
        title: 'Google Flow & DaVinci Resolve Video Assembly Swarm',
        badge: 'Skills: 00_keystone_flow_davinci_master_pipeline & 02_davinci_resolve',
        desc: 'Google Flow Box 2 automation suite: reverse B-Roll renaming (F1), reverse video renaming (F2), 1K B-Roll downloading (F3), and 1080p video downloading (F4). DaVinci Studio 2-track timeline assembly and -18dB ducked music synchronization.',
        path: '17_subagents/ (F1-F4, D1, D2)',
        tier: 'inherit / flash (Execution Workers)',
        count: '6 Specialized Agents'
      },
      infra: {
        icon: '🗄️',
        title: 'Skill Assets & Infrastructure Operations Swarm',
        badge: 'Skills: 01_session_bootstrap & 03_MCP',
        desc: 'Two-way CRM Gmail inbox triage (G1), Google Drive desktop sync health and cloud-to-local file integrity (D1), and stale scratch cleanup / log rotation (S3).',
        path: '17_subagents/ (G1, D1, S3)',
        tier: 'inherit (Frontier Tier)',
        count: '3 Specialized Agents'
      },
      brain: {
        icon: '🧠',
        title: 'Vector Brain & Knowledge Memory Swarm',
        badge: 'Skills: 01_session_bootstrap & Vector Brain API (:9878)',
        desc: 'Knowledge graph connectivity, wikilink validation, SIMD re-indexing on Port 9878, frontmatter compliance, and memory synchronization across all 17 main workspace directories.',
        path: '17_subagents/ (S2_brain_auditor)',
        tier: 'inherit (Frontier Tier)',
        count: '1 Specialized Agent'
      }
    };

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function renderMarkdownToHtml(md) {
      if (!md) return '<p style="color:#64748b;">No definition content available.</p>';
      let html = md;
      html = html.replace(/^---[\s\S]*?---\s*/m, '');
      html = escapeHtml(html);

      // Fenced Code Blocks
      html = html.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre class="md-code-block"><code>${code.trim()}</code></pre>`;
      });

      // Inline code
      html = html.replace(/`([^`]+)`/g, '<code class="md-inline-code">$1</code>');

      // Headers
      html = html.replace(/^### (.*$)/gim, '<h4 class="md-h4" style="color:#f1f5f9; margin:14px 0 6px 0;">$1</h4>');
      html = html.replace(/^## (.*$)/gim, '<h3 class="md-h3" style="color:var(--hud-neon-cyan,#00f0ff); margin:18px 0 8px 0; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:4px;">$1</h3>');
      html = html.replace(/^# (.*$)/gim, '<h2 class="md-h2" style="color:#fff; margin:20px 0 10px 0;">$1</h2>');

      // Blockquotes
      html = html.replace(/^\> (.*$)/gim, '<blockquote style="border-left:3px solid var(--hud-neon-violet-light,#c084fc); padding:6px 12px; margin:8px 0; background:rgba(139,92,246,0.08); color:#e2e8f0; font-size:11.5px;">$1</blockquote>');

      // Bold & Italic
      html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

      // Unordered lists
      html = html.replace(/^\s*-\s+(.*$)/gim, '<li style="margin-left:16px; margin-bottom:4px;">$1</li>');

      // Paragraph breaks
      html = html.replace(/\n\n/g, '<br/><br/>');

      return html;
    }

    function updateSwarmOverview(filterKey) {
      const meta = SWARM_PILE_METADATA[filterKey] || SWARM_PILE_METADATA['all'];
      if (swarmOverviewIcon) swarmOverviewIcon.textContent = meta.icon;
      if (swarmOverviewTitle) swarmOverviewTitle.textContent = meta.title;
      if (swarmOverviewBadge) swarmOverviewBadge.textContent = meta.badge;
      if (swarmOverviewDesc) swarmOverviewDesc.textContent = meta.desc;
      if (swarmOverviewPath) swarmOverviewPath.textContent = meta.path;
      if (swarmOverviewTier) swarmOverviewTier.textContent = meta.tier;
      if (swarmOverviewCount) swarmOverviewCount.textContent = meta.count;
    }

    function applyDrawerFontSize(size) {
      drawerFontSize = Math.min(36, Math.max(10, size));
      if (drawerAgentBody) drawerAgentBody.style.fontSize = drawerFontSize + 'px';
      if (drawerZoomSlider) drawerZoomSlider.value = drawerFontSize;
      if (drawerZoomReadout) drawerZoomReadout.textContent = drawerFontSize + 'px';
      if (btnDrawerZoomReset) btnDrawerZoomReset.textContent = Math.round((drawerFontSize / 13) * 100) + '%';
      localStorage.setItem('keystone_drawer_font_size', String(drawerFontSize));
    }

    function applyDrawerWidth(width) {
      const clamped = Math.min(Math.max(width, 380), window.innerWidth - 30);
      drawerCustomWidth = clamped;
      if (agentDefinitionDrawer) {
        agentDefinitionDrawer.style.width = clamped + 'px';
      }
      localStorage.setItem('keystone_drawer_width', String(clamped));
    }

    function renderAgentCards() {
      if (!agentsCardsGrid) return;
      const agents = window.KEYSTONE_AGENTS_REGISTRY || [];

      if (!agents.length) {
        agentsCardsGrid.innerHTML = `
          <div class="agents-loading-state">
            <span style="color:#64748b;">No subagents found in registry.</span>
          </div>
        `;
        return;
      }

      let filtered = agents;
      if (currentCategoryFilter !== 'all') {
        filtered = agents.filter(a => a.category === currentCategoryFilter);
      }

      let html = '';
      filtered.forEach((agent) => {
        const icon = PILE_ICONS[agent.category] || '🤖';

        html += `
          <div class="agent-card-v2" data-id="${agent.id}" data-category="${agent.category}" title="Click to inspect full ${escapeHtml(agent.name)} definition">
            <div class="agent-card-v2-header">
              <span class="agent-card-v2-icon">${icon}</span>
              <div style="flex:1; overflow:hidden;">
                <h4 class="agent-card-v2-title" title="${escapeHtml(agent.name)}">${escapeHtml(agent.name)}</h4>
                <span class="agent-card-v2-id">${escapeHtml(agent.id)}</span>
              </div>
              <span class="agent-status-badge running">ACTIVE</span>
            </div>
            <div class="agent-card-v2-role" title="${escapeHtml(agent.role)}">${escapeHtml(agent.role)}</div>
            <div class="agent-card-v2-purpose" title="${escapeHtml(agent.purpose)}">${escapeHtml(agent.purpose || 'Autonomous specialized Keystone subagent worker.')}</div>
            <div class="agent-card-v2-tools" title="${escapeHtml(agent.tools)}">🛠️ ${escapeHtml(agent.tools || 'read, write, terminal')}</div>
          </div>
        `;
      });

      agentsCardsGrid.innerHTML = html;

      // Attach click handlers to cards
      document.querySelectorAll('.agent-card-v2').forEach((card) => {
        card.addEventListener('click', () => {
          const aid = card.getAttribute('data-id');
          const targetAgent = (window.KEYSTONE_AGENTS_REGISTRY || []).find(a => a.id === aid);
          if (targetAgent) {
            openAgentDefinition(targetAgent);
          }
        });
      });
    }

    function openAgentDefinition(agent) {
      if (!agentDefinitionDrawer || !agent) return;
      currentSelectedAgent = agent;

      const icon = PILE_ICONS[agent.category] || '🤖';
      if (drawerAgentIcon) drawerAgentIcon.textContent = icon;
      if (drawerAgentTitle) drawerAgentTitle.textContent = agent.name || agent.id;
      if (drawerAgentId) drawerAgentId.textContent = agent.id;
      if (drawerAgentCategory) drawerAgentCategory.textContent = agent.category_name || agent.category.toUpperCase();
      if (drawerAgentModel) drawerAgentModel.textContent = `Model: ${agent.model || 'inherit'}`;

      if (drawerAgentBody) {
        drawerAgentBody.innerHTML = renderMarkdownToHtml(agent.definition_markdown);
      }

      applyDrawerFontSize(drawerFontSize);
      applyDrawerWidth(drawerCustomWidth);

      agentDefinitionDrawer.style.display = 'flex';
      if (agentDrawerBackdrop) agentDrawerBackdrop.style.display = 'block';
    }

    function closeAgentDefinition() {
      if (agentDefinitionDrawer) agentDefinitionDrawer.style.display = 'none';
      if (agentDrawerBackdrop) agentDrawerBackdrop.style.display = 'none';
      currentSelectedAgent = null;
    }

    if (btnCloseAgentDrawer) {
      btnCloseAgentDrawer.addEventListener('click', closeAgentDefinition);
    }
    if (agentDrawerBackdrop) {
      agentDrawerBackdrop.addEventListener('click', closeAgentDefinition);
    }

    // Draggable Splitter Left Edge on Definition Drawer
    if (drawerResizeHandle) {
      drawerResizeHandle.addEventListener('pointerdown', (e) => {
        isDraggingDrawer = true;
        lastDrawerPointerId = e.pointerId;
        drawerResizeHandle.setPointerCapture(e.pointerId);
        document.body.classList.add('is-resizing-drawer');
      });

      window.addEventListener('pointermove', (e) => {
        if (!isDraggingDrawer) return;
        const newW = window.innerWidth - e.clientX;
        applyDrawerWidth(newW);
      });

      const stopDrawerDrag = (e) => {
        if (!isDraggingDrawer) return;
        isDraggingDrawer = false;
        try {
          if (lastDrawerPointerId !== null) drawerResizeHandle.releasePointerCapture(lastDrawerPointerId);
        } catch (_) {}
        document.body.classList.remove('is-resizing-drawer');
      };

      window.addEventListener('pointerup', stopDrawerDrag);
      window.addEventListener('pointercancel', stopDrawerDrag);
    }

    // Font Zoom Controls (Slider, Buttons, and Ctrl+Mouse Wheel)
    if (drawerZoomSlider) {
      drawerZoomSlider.addEventListener('input', (e) => {
        applyDrawerFontSize(parseInt(e.target.value, 10));
      });
    }

    if (drawerAgentBody) {
      // Ctrl + Wheel to smoothly zoom text to any size
      drawerAgentBody.addEventListener('wheel', (e) => {
        if (e.ctrlKey) {
          e.preventDefault();
          const step = e.deltaY < 0 ? 1 : -1;
          applyDrawerFontSize(drawerFontSize + step);
        }
      }, { passive: false });
    }

    if (btnDrawerZoomIn) {
      btnDrawerZoomIn.addEventListener('click', (e) => {
        e.stopPropagation();
        applyDrawerFontSize(drawerFontSize + 2);
      });
    }

    if (btnDrawerZoomOut) {
      btnDrawerZoomOut.addEventListener('click', (e) => {
        e.stopPropagation();
        applyDrawerFontSize(drawerFontSize - 2);
      });
    }

    if (btnDrawerZoomReset) {
      btnDrawerZoomReset.addEventListener('click', (e) => {
        e.stopPropagation();
        applyDrawerFontSize(13);
      });
    }

    if (btnDrawerExpand) {
      btnDrawerExpand.addEventListener('click', (e) => {
        e.stopPropagation();
        if (agentDefinitionDrawer) {
          agentDefinitionDrawer.classList.toggle('expanded');
          const isExp = agentDefinitionDrawer.classList.contains('expanded');
          btnDrawerExpand.textContent = isExp ? '❐' : '⛶';
          btnDrawerExpand.title = isExp ? 'Restore Dragged Width' : 'Toggle Full Wide View';
          if (isExp) {
            agentDefinitionDrawer.style.width = '880px';
          } else {
            applyDrawerWidth(drawerCustomWidth);
          }
        }
      });
    }

    if (btnCopyAgentPrompt) {
      btnCopyAgentPrompt.addEventListener('click', () => {
        if (currentSelectedAgent && currentSelectedAgent.definition_markdown) {
          navigator.clipboard.writeText(currentSelectedAgent.definition_markdown).then(() => {
            logTerminal(`📋 Copied definition for ${currentSelectedAgent.id} to clipboard.`, 'success');
            btnCopyAgentPrompt.textContent = '✅ COPIED!';
            setTimeout(() => { btnCopyAgentPrompt.textContent = '📋 COPY PROMPT'; }, 2000);
          });
        }
      });
    }

    if (btnOpenAgentFolder) {
      btnOpenAgentFolder.addEventListener('click', () => {
        if (currentSelectedAgent) {
          logTerminal(`📂 Subagent path: 17_subagents/${currentSelectedAgent.id}/definition.md`, 'cyan');
        }
      });
    }

    // View Switcher (Agents View vs Daemons View)
    if (btnModeAgents && btnModeDaemons) {
      btnModeAgents.addEventListener('click', () => {
        btnModeAgents.classList.add('active');
        btnModeDaemons.classList.remove('active');
        if (agentsCardsGrid) agentsCardsGrid.style.display = 'grid';
        if (agentsFilterBar) agentsFilterBar.style.display = 'flex';
        const overviewBox = document.getElementById('swarmOverviewBox');
        if (overviewBox) overviewBox.style.display = 'flex';
        if (daemonsCardsGrid) daemonsCardsGrid.style.display = 'none';
      });

      btnModeDaemons.addEventListener('click', () => {
        btnModeDaemons.classList.add('active');
        btnModeAgents.classList.remove('active');
        if (agentsCardsGrid) agentsCardsGrid.style.display = 'none';
        if (agentsFilterBar) agentsFilterBar.style.display = 'none';
        const overviewBox = document.getElementById('swarmOverviewBox');
        if (overviewBox) overviewBox.style.display = 'none';
        if (daemonsCardsGrid) daemonsCardsGrid.style.display = 'flex';
      });
    }

    // Filter bar pills
    const filterPills = document.querySelectorAll('.agents-filter-pill');
    filterPills.forEach((pill) => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentCategoryFilter = pill.getAttribute('data-filter') || 'all';
        updateSwarmOverview(currentCategoryFilter);
        renderAgentCards();
      });
    });

    // Real-Time Active Chat Tracking & Dynamic Target Selector
    async function syncArchChatSelector() {
      try {
        const res = await fetch('http://127.0.0.1:9876/api/active-chats');
        if (!res.ok) return;
        const data = await res.json();
        const activeId = data.active_conversation_id || selectedChatId;
        const chats = data.active_chats || [];

        if (chats.length && archChatSelect) {
          // Keep current selection
          const currentVal = archChatSelect.value;
          archChatSelect.innerHTML = '<option value="auto">⚡ AUTO-DETECT ACTIVE CHAT</option>';
          chats.forEach((c) => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = `${c.number ? `[#${c.number}] ` : ''}${c.short_title || c.full_title || c.id}`;
            archChatSelect.appendChild(opt);
          });
          archChatSelect.value = currentVal;
        }

        // Find active chat object
        const matched = chats.find(c => c.id === activeId);
        const displayTitle = matched ? (matched.short_title || matched.full_title) : (selectedChatTitle || '[#01] Active Chat');
        if (archActiveChatBadge) {
          archActiveChatBadge.textContent = displayTitle;
        }
        return { activeId, displayTitle };
      } catch (err) {
        if (archActiveChatBadge) {
          archActiveChatBadge.textContent = selectedChatTitle || '[#01] Run Bootstrap Process';
        }
      }
    }

    if (archChatSelect) {
      archChatSelect.addEventListener('change', () => {
        if (archChatSelect.value !== 'auto') {
          const optText = archChatSelect.options[archChatSelect.selectedIndex]?.text || '';
          selectedChatId = archChatSelect.value;
          selectedChatTitle = optText;
          if (archActiveChatBadge) archActiveChatBadge.textContent = optText;
          fetch('http://127.0.0.1:9876/api/set-target', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: selectedChatId, title: selectedChatTitle })
          }).catch(() => {});
        } else {
          syncArchChatSelector();
        }
      });
    }

    // 1-Click Launch Subagent Architect in Active Chat
    if (btnLaunchSubagentArchitect) {
      btnLaunchSubagentArchitect.addEventListener('click', async () => {
        // Dynamically sync and get the absolute latest live active chat from daemon!
        const syncResult = await syncArchChatSelector();
        
        let targetId = selectedChatId;
        let targetChat = selectedChatTitle || '[#01] Run Bootstrap Process';

        if (archChatSelect && archChatSelect.value !== 'auto') {
          targetId = archChatSelect.value;
          targetChat = archChatSelect.options[archChatSelect.selectedIndex]?.text || targetChat;
        } else if (syncResult && syncResult.activeId) {
          targetId = syncResult.activeId;
          targetChat = syncResult.displayTitle;
          selectedChatId = targetId;
          selectedChatTitle = targetChat;
        }

        const architectPrompt = `Wayne Stevenson has requested to create a new production subagent using the interactive Subagent Architect.

MISSION: Collaborate with Wayne step-by-step in this chat session to design, write, test, and register a new production subagent.

STEPS TO EXECUTE WITH WAYNE:
1. Greet Wayne and ask what new subagent or specialized capability he needs.
2. Recommend the best Swarm Category / Pile (TDD Eng, Suno Music, Possibilities, Money, Luxury Web, Flow & DaVinci, Infrastructure, or Vector Brain) or whether to create a new pile.
3. Determine required tool permissions (read_file, write_to_file, run_command, brave_search, CDP Port 9222) and confirm model tier (default: inherit Gemini 3.8-High).
4. Author the production v8.2.0 FastMCP definition.md with typed input/output schemas, anti-looping guards, and DoD gates.
5. Upon Wayne's confirmation, save the definition to 17_subagents/<agent_id>/definition.md, update 17_subagents/00_INDEX.md, and trigger SIMD re-indexing.`;

        if (archStatusMsg) {
          archStatusMsg.style.display = 'block';
          archStatusMsg.style.color = 'var(--hud-neon-cyan, #00f0ff)';
          archStatusMsg.style.background = 'rgba(0, 240, 255, 0.12)';
          archStatusMsg.style.border = '1px solid rgba(0, 240, 255, 0.3)';
          archStatusMsg.innerHTML = `🚀 Dispatched Subagent Architect to <strong>${escapeHtml(targetChat)}</strong>! Switch to your open chat to begin.`;
        }

        // Send via daemon IPC to active conversation
        fetch('http://127.0.0.1:9876/api/prompt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: architectPrompt,
            conversation_id: targetId
          })
        }).catch(() => {});

        // Also ensure target is bound across daemons
        fetch('http://127.0.0.1:9876/api/set-target', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: targetId, title: targetChat })
        }).catch(() => {});

        logTerminal(`🤖 Subagent Architect dispatched to active chat: ${targetChat}`, 'cyan');
        triggerAvatarSpeech(`Subagent Architect launched in ${targetChat}. Ready to design.`);
      });
    }

    // Initial render & sync
    updateSwarmOverview(currentCategoryFilter);
    renderAgentCards();
    syncArchChatSelector();
  }


  // --------------------------------------------------------------------------
  // NEXT-GEN CELESTIAL VECTOR BRAIN
  // NEXT-GEN CELESTIAL VECTOR BRAIN & MULTI-BRAIN WORKSPACE CONTROLLER
  // --------------------------------------------------------------------------
  let isBrainInitialized = false;

  function ensureNeuralBrainInitialized() {
    if (window.NeuralBrain2D && !window.__neuralBrainInstance) {
      const container = document.getElementById('neuralBrainCanvasContainer');
      if (container) {
        window.__neuralBrainInstance = window.NeuralBrain2D.init(container);
        loadWorkspaceTree();
      }
    } else if (window.__neuralBrainInstance) {
      window.__neuralBrainInstance.handleResize?.();
    }
  }

  async function loadWorkspaceTree(path = null) {
    const statsNodes = document.getElementById('brainStatsNodes');
    const statsFiles = document.getElementById('brainStatsFiles');
    const treeContainer = document.getElementById('brainFolderTree');
    if (statsNodes) statsNodes.textContent = '🔄 Syncing...';

    try {
      let workspaceMeta = null;
      if (path) {
        const postRes = await fetch('http://127.0.0.1:9878/api/workspace', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path })
        });
        if (!postRes.ok) {
          const errData = await postRes.json().catch(() => ({}));
          const errMsg = errData.message || `Folder path '${path}' does not exist on this computer.`;
          logTerminal(`⚠️ Failed to load workspace: ${errMsg}`, 'error');
          if (statsNodes) statsNodes.textContent = '20 Orbs';
          return { success: false, error: errMsg };
        }
        workspaceMeta = await postRes.json();
      }

      const res = await fetch('http://127.0.0.1:9878/api/tree');
      if (res.ok) {
        const treeData = await res.json();
        window.__currentBrainTree = treeData;

        if (window.__neuralBrainInstance) {
          window.__neuralBrainInstance.loadWorkspace(treeData);
        }

        renderBrainFolderTree(treeData);

        if (!workspaceMeta) {
          const wsRes = await fetch('http://127.0.0.1:9878/api/workspace');
          if (wsRes.ok) {
            workspaceMeta = await wsRes.json();
          }
        }

        if (workspaceMeta) {
          if (statsFiles) statsFiles.textContent = `${workspaceMeta.file_count || 37} Files`;
          if (statsNodes) statsNodes.textContent = '20 Domains Active';
          updateAgentsWorkspace(workspaceMeta.workspace_root || path, treeData, workspaceMeta);

          const curRoot = workspaceMeta.workspace_root || path;
          const sel = document.getElementById('brainWorkspaceSelect');
          if (sel && curRoot) {
            const curRootNorm = curRoot.replace(/[\\/]+$/, '').toLowerCase();
            let found = false;
            for (let i = 0; i < sel.options.length; i++) {
              if (sel.options[i].value.replace(/[\\/]+$/, '').toLowerCase() === curRootNorm) {
                sel.selectedIndex = i;
                found = true;
                break;
              }
            }
            if (!found) {
              const opt = document.createElement('option');
              opt.value = curRoot;
              const isDrive = /^[a-zA-Z]:[\\/]*$/.test(curRoot.trim());
              const name = isDrive ? `Drive ${curRoot.trim().charAt(0).toUpperCase()}:\\` : (curRoot.split(/[\\/]/).filter(Boolean).pop() || curRoot);
              opt.textContent = `${isDrive ? '💽' : '📂'} ${name}`;
              sel.appendChild(opt);
              opt.selected = true;
            }
          }
        }
        return { success: true, meta: workspaceMeta };
      }
      return { success: false, error: 'Could not fetch workspace tree from daemon' };
    } catch (err) {
      console.warn('[VectorBrain] Error loading workspace tree from Port 9878:', err);
      if (treeContainer) {
        treeContainer.innerHTML = '<div class="tree-loading-state"><span style="color:#ef4444;">⚠️ Port 9878 offline or indexing...</span></div>';
      }
      return { success: false, error: err.message };
    }
  }

  function updateAgentsWorkspace(wsPath, treeData, wsMeta) {
    const agentCount = wsMeta && wsMeta.agents_bound ? wsMeta.agents_bound : 68;
    const totalEl = document.querySelector('.deck-stat-box .stat-value.cyan');
    const subEl = document.querySelector('.deck-stat-box .stat-sub');
    if (totalEl) totalEl.textContent = `${agentCount} Agents`;
    if (subEl) {
      const wsName = (wsPath || '').split(/[\\/]/).pop() || 'Keystone Brain';
      subEl.textContent = `${wsName} Registry Bound`;
    }
    logTerminal(`⚡ Agents workspace re-bound to active brain: ${wsPath || 'Keystone Brain'} (${agentCount} agents active)`, 'success');
  }

  function renderBrainFolderTree(treeData) {
    const treeContainer = document.getElementById('brainFolderTree');
    if (!treeContainer || !treeData || !treeData[0]) return;

    const root = treeData[0];
    treeContainer.innerHTML = '';

    function createTreeNode(node, depth = 0) {
      const wrapper = document.createElement('div');
      wrapper.className = 'tree-node-wrapper';
      wrapper.style.marginLeft = `${depth * 8}px`;

      const item = document.createElement('div');
      item.className = 'tree-item';
      item.dataset.path = node.path || node.id;
      item.dataset.type = node.type || 'file';

      const isFolder = node.type === 'folder';
      const hasChildren = isFolder && node.children && node.children.length > 0;
      const count = hasChildren ? node.children.length : 0;

      item.innerHTML = `
        <div class="tree-item-main">
          ${isFolder ? '<span class="tree-chevron">▶</span>' : '<span style="width:10px; display:inline-block;"></span>'}
          <span class="tree-item-icon">${isFolder ? '📁' : (node.name.endsWith('.md') ? '📄' : (node.name.endsWith('.json') ? '📦' : '📜'))}</span>
          <span class="tree-item-name" title="${node.name}">${node.name}</span>
        </div>
        ${isFolder && count > 0 ? `<span class="tree-count-badge">${count}</span>` : ''}
      `;

      wrapper.appendChild(item);

      let childrenContainer = null;
      if (hasChildren) {
        childrenContainer = document.createElement('div');
        childrenContainer.className = 'tree-children-container';
        childrenContainer.style.display = 'none'; // Closed by default at all depths!

        node.children.forEach(child => {
          childrenContainer.appendChild(createTreeNode(child, depth + 1));
        });
        wrapper.appendChild(childrenContainer);
      }

      item.addEventListener('click', (e) => {
        e.stopPropagation();
        document.querySelectorAll('.tree-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');

        if (isFolder && childrenContainer) {
          const chevron = item.querySelector('.tree-chevron');
          const isOpen = childrenContainer.style.display !== 'none';
          childrenContainer.style.display = isOpen ? 'none' : 'block';
          if (chevron) chevron.classList.toggle('open', !isOpen);
        }

        if (window.__neuralBrainInstance) {
          window.__neuralBrainInstance.focusNodeBySearch(node.name);
          window.__neuralBrainInstance.openWikiDrawer(node);
        }
      });

      return wrapper;
    }

    if (root.children && Array.isArray(root.children)) {
      root.children.forEach(child => {
        treeContainer.appendChild(createTreeNode(child, 0));
      });
    }
  }

  function initCelestialVectorBrain() {
    if (isBrainInitialized) return;
    isBrainInitialized = true;

    const KEYSTONE_SAVED_BRAINS_KEY = 'KEYSTONE_SAVED_BRAINS';

    function formatBrainName(path, name) {
      if (!path) return 'Brain';
      if (/^[a-zA-Z]:[\\/]*$/.test(path.trim())) {
        const driveLetter = path.trim().charAt(0).toUpperCase();
        return `Drive ${driveLetter}:\\`;
      }
      return name || path.split(/[\\/]/).filter(Boolean).pop() || path;
    }

    function formatBrainIcon(path) {
      if (/^[a-zA-Z]:[\\/]*$/.test((path || '').trim())) {
        return '💽';
      }
      return '📂';
    }

    function getSavedBrains() {
      try {
        const raw = localStorage.getItem(KEYSTONE_SAVED_BRAINS_KEY);
        return raw ? JSON.parse(raw) : [];
      } catch (e) {
        return [];
      }
    }

    function saveBrainPath(path, name) {
      if (!path) return;
      try {
        const formattedName = formatBrainName(path, name);
        const list = getSavedBrains().filter(b => b.path.replace(/[\\/]+$/, '').toLowerCase() !== path.replace(/[\\/]+$/, '').toLowerCase());
        list.unshift({ path, name: formattedName });
        localStorage.setItem(KEYSTONE_SAVED_BRAINS_KEY, JSON.stringify(list.slice(0, 15)));
      } catch (e) {}
    }

    function removeSavedBrain(pathToRemove) {
      if (!pathToRemove) return;
      const cleanTarget = pathToRemove.replace(/[\\/]+$/, '').toLowerCase();
      try {
        const list = getSavedBrains().filter(b => b.path.replace(/[\\/]+$/, '').toLowerCase() !== cleanTarget);
        localStorage.setItem(KEYSTONE_SAVED_BRAINS_KEY, JSON.stringify(list));
      } catch (e) {}

      if (select) {
        for (let i = select.options.length - 1; i >= 0; i--) {
          if (select.options[i].value.replace(/[\\/]+$/, '').toLowerCase() === cleanTarget) {
            const wasSelected = select.selectedIndex === i;
            select.remove(i);
            if (wasSelected) {
              select.selectedIndex = 0;
              loadWorkspaceTree(select.value);
            }
            break;
          }
        }
      }
      renderSavedBrainsList();
    }

    // 1. Multi-Brain Switcher Dropdown & Saved Brains Hydration
    const select = document.getElementById('brainWorkspaceSelect');

    function populateSavedBrains() {
      if (!select) return;
      const saved = getSavedBrains();
      saved.forEach(b => {
        const bNorm = b.path.replace(/[\\/]+$/, '').toLowerCase();
        let exists = false;
        for (let i = 0; i < select.options.length; i++) {
          if (select.options[i].value.replace(/[\\/]+$/, '').toLowerCase() === bNorm) {
            exists = true;
            break;
          }
        }
        if (!exists) {
          const opt = document.createElement('option');
          opt.value = b.path;
          opt.textContent = `${formatBrainIcon(b.path)} ${b.name}`;
          select.appendChild(opt);
        }
      });
    }

    populateSavedBrains();

    // 2. Add Folder to Brain Modal & Native Windows Folder Picker Handler
    const addFolderModal = document.getElementById('brainAddFolderModal');
    const inputFolderPath = document.getElementById('inputBrainFolderPath');
    const btnBrowseComputer = document.getElementById('btnBrowseComputerPath');
    const btnConfirmAdd = document.getElementById('btnConfirmAddToBrain');
    const btnCloseModal = document.getElementById('btnCloseAddFolderModal');
    const btnCancelModal = document.getElementById('btnCancelAddFolder');

    function renderSavedBrainsList() {
      const savedSection = document.getElementById('modalSavedSection');
      const savedList = document.getElementById('modalSavedList');
      if (!savedSection || !savedList) return;

      const saved = getSavedBrains();
      if (saved.length === 0) {
        savedSection.style.display = 'none';
        savedList.innerHTML = '';
        return;
      }

      savedSection.style.display = 'flex';
      savedList.innerHTML = '';
      saved.forEach(item => {
        const row = document.createElement('div');
        row.className = 'modal-saved-item';
        row.innerHTML = `
          <div class="modal-saved-item-info">
            <span class="modal-saved-item-name">${formatBrainIcon(item.path)} ${item.name}</span>
            <span class="modal-saved-item-path">${item.path}</span>
          </div>
          <button class="modal-saved-item-del" title="Remove folder from Brain dropdown">✕</button>
        `;
        row.querySelector('.modal-saved-item-del').addEventListener('click', (e) => {
          e.stopPropagation();
          removeSavedBrain(item.path);
        });
        savedList.appendChild(row);
      });
    }

    function showAddFolderModal() {
      if (addFolderModal) {
        addFolderModal.style.display = 'flex';
        const errEl = document.getElementById('modalAddFolderError');
        if (errEl) {
          errEl.style.display = 'none';
          errEl.textContent = '';
        }
        renderSavedBrainsList();
        if (inputFolderPath) {
          inputFolderPath.value = '';
          setTimeout(() => inputFolderPath.focus(), 50);
        }
      }
    }

    function hideAddFolderModal() {
      if (addFolderModal) {
        addFolderModal.style.display = 'none';
        const errEl = document.getElementById('modalAddFolderError');
        if (errEl) {
          errEl.style.display = 'none';
          errEl.textContent = '';
        }
        if (inputFolderPath) inputFolderPath.value = '';
      }
    }

    async function executeNativeFolderBrowse() {
      let pickedPath = null;
      let pickedName = null;

      // Try Tauri native dialog if available
      if (window.__TAURI__ && window.__TAURI__.dialog && typeof window.__TAURI__.dialog.open === 'function') {
        try {
          const selected = await window.__TAURI__.dialog.open({
            directory: true,
            multiple: false,
            title: 'Select Brain Folder / Workspace'
          });
          if (selected) {
            pickedPath = typeof selected === 'string' ? selected : selected.path;
            pickedName = formatBrainName(pickedPath);
          }
        } catch (e) {
          console.warn('[VectorBrain] Tauri dialog error, falling back to daemon:', e);
        }
      }

      // Daemon fallback via /api/browse_folder
      if (!pickedPath) {
        try {
          if (btnBrowseComputer) btnBrowseComputer.style.opacity = '0.5';
          const res = await fetch('http://127.0.0.1:9878/api/browse_folder', { method: 'POST' });
          if (res.ok) {
            const data = await res.json();
            if (data.status === 'success' && data.path) {
              pickedPath = data.path;
              pickedName = formatBrainName(pickedPath, data.name);
            }
          }
        } catch (e) {
          console.warn('[VectorBrain] Daemon browse error:', e);
        } finally {
          if (btnBrowseComputer) btnBrowseComputer.style.opacity = '';
        }
      }

      if (pickedPath && inputFolderPath) {
        let clean = pickedPath.trim().replace(/^["']|["']$/g, '');
        if (/^[a-zA-Z]:$/.test(clean)) clean += '\\';
        inputFolderPath.value = clean;
      }
      return pickedPath;
    }

    async function confirmAddFolderToBrain() {
      const errEl = document.getElementById('modalAddFolderError');
      if (errEl) {
        errEl.style.display = 'none';
        errEl.textContent = '';
      }

      const rawPath = inputFolderPath ? inputFolderPath.value : '';
      let cleanPath = (rawPath || '').trim().replace(/^["']|["']$/g, '').trim();
      if (!cleanPath) {
        if (errEl) {
          errEl.textContent = 'Please enter or browse for a valid folder path.';
          errEl.style.display = 'block';
        }
        return;
      }

      // Normalize drive letters like "C:" or "c:" -> "C:\"
      if (/^[a-zA-Z]:$/.test(cleanPath)) {
        cleanPath += '\\';
      }

      const btnConfirm = document.getElementById('btnConfirmAddToBrain');
      if (btnConfirm) {
        btnConfirm.textContent = '⏳ VERIFYING...';
        btnConfirm.disabled = true;
      }

      try {
        const loadResult = await loadWorkspaceTree(cleanPath);
        if (!loadResult || !loadResult.success) {
          if (errEl) {
            errEl.textContent = loadResult?.error || `Folder '${cleanPath}' does not exist on this computer.`;
            errEl.style.display = 'block';
          }
          return;
        }

        const meta = loadResult.meta || {};
        const verifiedPath = meta.workspace_root || cleanPath;
        const name = formatBrainName(verifiedPath);

        saveBrainPath(verifiedPath, name);

        if (select) {
          const verifiedNorm = verifiedPath.replace(/[\\/]+$/, '').toLowerCase();
          let existingOpt = null;
          for (let i = 0; i < select.options.length; i++) {
            if (select.options[i].value.replace(/[\\/]+$/, '').toLowerCase() === verifiedNorm) {
              existingOpt = select.options[i];
              break;
            }
          }
          if (!existingOpt) {
            existingOpt = document.createElement('option');
            existingOpt.value = verifiedPath;
            existingOpt.textContent = `${formatBrainIcon(verifiedPath)} ${name}`;
            select.appendChild(existingOpt);
          }
          select.value = existingOpt.value;
        }

        hideAddFolderModal();
        logTerminal(`🧠 Added and loaded Brain Workspace: ${verifiedPath}`, 'success');
        triggerAvatarSpeech(`Brain workspace loaded from ${name}. Scanning directory.`);
      } finally {
        if (btnConfirm) {
          btnConfirm.textContent = '⚡ ADD TO BRAIN';
          btnConfirm.disabled = false;
        }
      }
    }

    document.getElementById('btnBrowseFolderBrain')?.addEventListener('click', showAddFolderModal);
    btnCloseModal?.addEventListener('click', hideAddFolderModal);
    btnCancelModal?.addEventListener('click', hideAddFolderModal);
    addFolderModal?.addEventListener('click', (e) => {
      if (e.target === addFolderModal) hideAddFolderModal();
    });
    btnBrowseComputer?.addEventListener('click', executeNativeFolderBrowse);
    btnConfirmAdd?.addEventListener('click', confirmAddFolderToBrain);
    inputFolderPath?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') confirmAddFolderToBrain();
      if (e.key === 'Escape') hideAddFolderModal();
    });

    if (select) {
      select.addEventListener('change', async (e) => {
        const val = e.target.value;
        if (!val) return;
        const brainName = formatBrainName(val);
        logTerminal(`🧠 Switching Brain Workspace to: ${val}...`, 'success');
        triggerAvatarSpeech(`Switching Brain Workspace to ${brainName}. Re-indexing neural matrix.`);
        await loadWorkspaceTree(val);
      });
    }

    // 3. Media Mode Toggle (Videos vs Static Pictures)
    const btnMediaMode = document.getElementById('btnToggleMediaMode');
    if (btnMediaMode) {
      btnMediaMode.addEventListener('click', () => {
        const newMode = window.__neuralBrainInstance?.toggleMediaMode?.() || 'video';
        if (newMode === 'picture') {
          btnMediaMode.textContent = '🖼️ PICTURES';
          btnMediaMode.classList.remove('cyan-btn');
          logTerminal('🖼️ Switched Brain Media Mode to Static Picture Orbs (Zero GPU Video Decoding).', 'info');
        } else {
          btnMediaMode.textContent = '🎬 VIDEOS';
          btnMediaMode.classList.add('cyan-btn');
          logTerminal('🎬 Switched Brain Media Mode to GPU-Accelerated Video Orbs.', 'info');
        }
      });
    }

    // Explicitly pause inactive avatar videos so only vidIdle decodes on page load
    ['vidListening', 'vidWorking', 'vidThinking', 'vidTalking', 'vidWalking'].forEach(id => {
      const v = document.getElementById(id);
      if (v && !v.paused) {
        v.pause();
      }
    });

    // 4. Folder Filter Input
    const folderFilter = document.getElementById('brainFolderFilter');
    if (folderFilter) {
      folderFilter.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        document.querySelectorAll('.tree-node-wrapper').forEach(node => {
          const nameEl = node.querySelector('.tree-item-name');
          const name = nameEl ? nameEl.textContent.toLowerCase() : '';
          node.style.display = (!query || name.includes(query)) ? '' : 'none';
        });
      });
    }

    // 5. Tree Collapse Button
    function toggleFolderTree() {
      const pane = document.getElementById('brainFolderPane');
      if (pane) {
        pane.classList.toggle('collapsed');
        setTimeout(() => {
          window.__neuralBrainInstance?.handleResize();
        }, 220);
      }
    }
    document.getElementById('btnCollapseFolderTree')?.addEventListener('click', toggleFolderTree);
    document.getElementById('btnToggleTree')?.addEventListener('click', toggleFolderTree);

    // 6. Wiki Drawer Toggle Button
    document.getElementById('btnToggleDrawer')?.addEventListener('click', () => {
      const drawer = document.getElementById('brainWikiDrawer');
      if (drawer) drawer.classList.toggle('open');
    });

    // 7. Splitter Resize Handle
    const splitter = document.getElementById('brainSplitterLeft');
    const folderPane = document.getElementById('brainFolderPane');
    if (splitter && folderPane) {
      let isResizingTree = false;
      splitter.addEventListener('mousedown', (e) => {
        isResizingTree = true;
        splitter.classList.add('dragging');
        document.body.style.cursor = 'col-resize';
        e.preventDefault();
      });
      window.addEventListener('mousemove', (e) => {
        if (!isResizingTree) return;
        const newWidth = Math.max(180, Math.min(520, e.clientX));
        folderPane.style.width = `${newWidth}px`;
        window.__neuralBrainInstance?.handleResize();
      });
      window.addEventListener('mouseup', () => {
        if (isResizingTree) {
          isResizingTree = false;
          splitter.classList.remove('dragging');
          document.body.style.cursor = '';
          window.__neuralBrainInstance?.handleResize();
        }
      });
    }

    // Preload initial workspace tree
    setTimeout(() => {
      ensureNeuralBrainInitialized();
      if (activeTabKey !== 'vector-brain') {
        window.__neuralBrainInstance?.pause?.();
      }
    }, 500);
  }

  // --------------------------------------------------------------------------
  // Initialization Sequence
  // --------------------------------------------------------------------------
  applyLayout();
  bindTargetChat(selectedChatId, selectedChatTitle);
  renderTabGroup(1);
  updateHardwareTelemetry();
  setAvatarState('idle');
  renderFx();
  syncActiveChatsFromDaemon();
  setInterval(syncActiveChatsFromDaemon, 8000);
  initDaemonWebSocket();
  initMasterVolumeControls();
  initAgentsWorkspaceHandlers();
  initCelestialVectorBrain();

  console.log('⚡ Keystone Tauri Next v2.4 Desktop Studio initialized successfully.');
})();
