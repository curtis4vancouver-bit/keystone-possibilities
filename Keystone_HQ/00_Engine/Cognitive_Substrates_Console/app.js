// =====================================================================
// KRONOS AI OPERATING SYSTEM - PERSISTENT ENGINE V3.2
// Dynamic Multi-Agent Context Partitioning & Simulation Core
// =====================================================================

// 1. ACTIVE PARTITION STATE
let activeAgentTab = 'keystone'; // 'keystone' | 'protocol' | 'spark'

// 2. EPISTEMIC GRAPH SCHEMAS PER ISOLATED PARTITION
const PARTITION_SCHEMAS = {
    keystone: {
        title: "🏗️ Keystone Fiduciary Context Vault",
        badge: "FTS5 + SQLite-Vec",
        desc: "Active document indices loaded in memory. These credentials, blueprints, and local SEO assets are partitioned to isolate brand intelligence.",
        docs: [
            { name: "squamish_custom_homes.html", path: "Local_SEO_Domination/squamish_custom_homes.html", size: "10.9 kB", icon: "🌐" },
            { name: "whistler_custom_homes.html", path: "Local_SEO_Domination/whistler_custom_homes.html", size: "10.9 kB", icon: "🌐" },
            { name: "west_vancouver_custom_homes.html", path: "Local_SEO_Domination/west_vancouver_custom_homes.html", size: "10.9 kB", icon: "🌐" },
            { name: "north_vancouver_custom_homes.html", path: "Local_SEO_Domination/north_vancouver_custom_homes.html", size: "10.9 kB", icon: "🌐" },
            { name: "fiduciary_pm_luxury_homes_blog.md", path: "Local_SEO_Domination/fiduciary_pm_luxury_homes_blog.md", size: "5.7 kB", icon: "📄" },
            { name: "whistler_villa_30s_short.md", path: "Scripts_Approved/whistler_villa_30s_short.md", size: "3.2 kB", icon: "🎬" }
        ],
        suiteTitle: "🛠️ Keystone Fiduciary Automation Tools",
        suiteActions: [
            { name: "Verify NAP Citations", icon: "🔍", action: "triggerVerifyNAP()" },
            { name: "Audit Sitelink Schemas", icon: "🏷️", action: "triggerAuditSchema()" },
            { name: "Run Instant Indexing", icon: "📡", action: "triggerIndexing()" },
            { name: "Compile 30s Short Script", icon: "🎬", action: "triggerVideoCompile()" }
        ],
        graph: {
            nodes: [
                { id: "FIDUCIARY PM", name: "FIDUCIARY PM", type: "Keystone", x: 150, y: 120, colorClass: "keystone" },
                { id: "BUILDER LICENSE", name: "LICENSE #52603", type: "Legal", x: 100, y: 220, colorClass: "keystone" },
                { id: "WHISTLER CHALET", name: "WHISTLER CHALET", type: "Asset", x: 300, y: 150, colorClass: "auxiliary" },
                { id: "WEST VANCOUVER", name: "WEST VANCOUVER", type: "Region", x: 480, y: 130, colorClass: "auxiliary" },
                { id: "COGNITIVE GRAPH", name: "LOCAL CITATIONS", type: "SEO", x: 360, y: 240, colorClass: "keystone" }
            ],
            edges: [
                { id: "ks_edge_01", source: "FIDUCIARY PM", target: "BUILDER LICENSE", relationship: "licensed_by", observation: "Keystone PM services are fully backed by BC Builder License #52603.", sourceName: "Builder Registry" },
                { id: "ks_edge_02", source: "WHISTLER CHALET", target: "FIDUCIARY PM", relationship: "managed_via", observation: "Alpine chalet custom build operates on 100% cost transparency.", sourceName: "Owner PM Contract" },
                { id: "ks_edge_03", source: "WHISTLER CHALET", target: "WEST VANCOUVER", relationship: "aligned_with", observation: "Architectural guidelines match high-end West Vancouver coastal layouts.", sourceName: "Quiet Luxury Playbook" },
                { id: "ks_edge_04", source: "COGNITIVE GRAPH", target: "FIDUCIARY PM", relationship: "ranks_up", observation: "Local SEO landing pages raise Map Pack credibility significantly.", sourceName: "Local SEO fly-wheel" }
            ]
        },
        agents: {
            "worker-01": { id: "worker-01", name: "SEO_Autopilot_01", task: "Map Pack Citations", pheromone: 1.0, lastHeartbeat: 0.0, crashed: false, backupActive: false, heartbeatRate: 1.4 },
            "worker-02": { id: "worker-02", name: "GTAG_Validator_02", task: "Ads Conversion Auditing", pheromone: 1.0, lastHeartbeat: 0.0, crashed: false, backupActive: false, heartbeatRate: 1.8 }
        },
        mdTitle: "📄 Local SEO Indexing Serializer Payload",
        mdSavings: "Saved 28.14% Context"
    },
    protocol: {
        title: "🧬 Protocol B2C Context Vault",
        badge: "Vector Index / Peptides",
        desc: "Active document indices loaded in memory. These hypertrophic guidelines, dosage titration tables, and look-off video scripts scale B2C global coaching.",
        docs: [
            { name: "glp1_sarcopenia_40s_short.md", path: "Scripts_Approved/glp1_sarcopenia_40s_short.md", size: "3.9 kB", icon: "🎬" },
            { name: "omni_broll_and_transition_tests.md", path: "Scripts_Approved/omni_broll_and_transition_tests.md", size: "4.2 kB", icon: "🎬" },
            { name: "glp1_sarcopenia_8min_masterpiece.md", path: "Scripts_Approved/keystone_8min_glp1_masterpiece.md", size: "41.1 kB", icon: "📄" },
            { name: "AVATAR-WAYNE.md", path: "Scripts_Approved/AVATAR-WAYNE.md", size: "2.0 kB", icon: "👤" }
        ],
        suiteTitle: "🛠️ Peptide Longevity & Media Tools",
        suiteActions: [
            { name: "Compile Look-Off Script", icon: "🎬", action: "triggerScriptCompile()" },
            { name: "Audit Voice Synthesis", icon: "🎙️", action: "triggerVoiceAudit()" },
            { name: "Calculate Protein Floor", icon: "⚖️", action: "triggerProteinFloor()" },
            { name: "Check GLP-1 Titration", icon: "🩸", action: "triggerGLP1Check()" }
        ],
        graph: {
            nodes: [
                { id: "SEMAGLUTIDE", name: "SEMAGLUTIDE", type: "Clinical", x: 120, y: 120, colorClass: "protocol" },
                { id: "SARCOPENIA", name: "SARCOPENIA", type: "Medical", x: 260, y: 150, colorClass: "auxiliary" },
                { id: "RESISTANCE LOADS", name: "RESISTANCE LOADS", type: "Therapy", x: 440, y: 110, colorClass: "protocol" },
                { id: "PROTEIN TITRATION", name: "PROTEIN TITRATION", type: "Dietary", x: 490, y: 220, colorClass: "protocol" },
                { id: "LOOK-OFF HACK", name: "LOOK-OFF HACK", type: "Media", x: 300, y: 240, colorClass: "protocol" }
            ],
            edges: [
                { id: "pr_edge_01", source: "SEMAGLUTIDE", target: "SARCOPENIA", relationship: "accelerates", observation: "Sarcopenia muscle wasting is accelerated by rapid GLP-1 weight decreases.", sourceName: "Clinical Guidelines" },
                { id: "pr_edge_02", source: "SARCOPENIA", target: "RESISTANCE LOADS", relationship: "mitigated_by", observation: "Sarcopenia muscle degradation is actively mitigated via heavy resistance loads.", sourceName: "Clinical Study v1" },
                { id: "pr_edge_03", source: "RESISTANCE LOADS", target: "PROTEIN TITRATION", relationship: "synergizes_with", observation: "High-tension loading pairs with protein titration floor of two hundred grams.", sourceName: "Hypertrophy Playbook" },
                { id: "pr_edge_04", source: "LOOK-OFF HACK", target: "SEMAGLUTIDE", relationship: "enforced_on", observation: "Always prioritize confident sideway look-offs to mask video cuts during talking heads.", sourceName: "MediaClaw v3.1 Specifications" }
            ]
        },
        agents: {
            "worker-01": { id: "worker-01", name: "Vocal_Synthesizer_01", task: "ElevenLabs Vocal Render", pheromone: 1.0, lastHeartbeat: 0.0, crashed: false, backupActive: false, heartbeatRate: 1.3 },
            "worker-02": { id: "worker-02", name: "LipSync_Engine_02", task: "Google Flow Audio Sync", pheromone: 1.0, lastHeartbeat: 0.0, crashed: false, backupActive: false, heartbeatRate: 1.7 }
        },
        mdTitle: "📄 Bio-Philic Longevity Markdown Serializer",
        mdSavings: "Saved 31.42% Context"
    },
    spark: {
        title: "⚡ Gemini Spark Context Vault",
        badge: "Secure SDK Daemon",
        desc: "Active API security configurations, local SQLite-Vec database connections, and US proxy routing gateway guidelines to bypass early access geo-blocks.",
        docs: [
            { name: "server.py", path: "Cognitive_Substrates_Console/server.py", size: "1.6 kB", icon: "🐍" },
            { name: "overnight_research_daemon.py", path: "overnight_research_daemon.py", size: "22.1 kB", icon: "🐍" },
            { name: "local_vector_db/", path: "local_vector_db/", size: "[Directory]", icon: "📁" },
            { name: "ag-stop-probe.json", path: "ag-stop-probe.json", size: "107 kB", icon: "🔧" }
        ],
        suiteTitle: "🛠️ Spark US Proxy & Daemon Tools",
        suiteActions: [
            { name: "Test US VPN Connection", icon: "⚡", action: "triggerVPNAudit()" },
            { name: "Run Scraping Daemon", icon: "📡", action: "triggerScrapingDaemon()" },
            { name: "Refresh Vector DB Sync", icon: "📂", action: "triggerVectorSync()" },
            { name: "Decrypt Secrets Plexus", icon: "🔑", action: "triggerCryptVault()" }
        ],
        graph: {
            nodes: [
                { id: "US PROXY GATEWAY", name: "US PROXY GATEWAY", type: "Network", x: 130, y: 110, colorClass: "spark" },
                { id: "GEMINI SPARK API", name: "GEMINI SPARK API", type: "API", x: 300, y: 140, colorClass: "spark" },
                { id: "VECTOR STORAGE", name: "VECTOR STORAGE", type: "Database", x: 470, y: 110, colorClass: "spark" },
                { id: "AES-256 VAULT", name: "PLEDGER VAULT", type: "Security", x: 420, y: 230, colorClass: "spark" },
                { id: "DAEMON INTERFACES", name: "DAEMON SCRIPT", type: "Process", x: 210, y: 220, colorClass: "spark" }
            ],
            edges: [
                { id: "sp_edge_01", source: "US PROXY GATEWAY", target: "GEMINI SPARK API", relationship: "routes_to", observation: "Proxy tunnel intercepts geolocation triggers, routing queries through Virginia endpoint.", sourceName: "Network Proxy Config" },
                { id: "sp_edge_02", source: "DAEMON INTERFACES", target: "US PROXY GATEWAY", relationship: "queries_via", observation: "Scraper script launches headless browser through active proxy tunnel.", sourceName: "Daemon Script Config" },
                { id: "sp_edge_03", source: "AES-256 VAULT", target: "VECTOR STORAGE", relationship: "decrypts", observation: "CryptVault handles symmetric decryption of private vector chunks at runtime.", sourceName: "Plexus Security Spec" },
                { id: "sp_edge_04", source: "VECTOR STORAGE", target: "GEMINI SPARK API", relationship: "feeds_context_to", observation: "Local pgvector schema feeds semantic target chunks directly to context window.", sourceName: "Local Database Daemon" }
            ]
        },
        agents: {
            "worker-01": { id: "worker-01", name: "VPN_Tunnel_01", task: "Proxy US Gateway Jitter", pheromone: 1.0, lastHeartbeat: 0.0, crashed: false, backupActive: false, heartbeatRate: 1.5 },
            "worker-02": { id: "worker-02", name: "DB_Daemon_02", task: "Supabase Local Sync", pheromone: 1.0, lastHeartbeat: 0.0, crashed: false, backupActive: false, heartbeatRate: 2.0 }
        },
        mdTitle: "📄 Spark Daemon Pipeline Transport Payload",
        mdSavings: "Saved 24.89% Context"
    }
};

// State management for active simulation
let graphData = null;
let agentsState = null;
let currentSimulationTime = 0.0;
const pheromoneDecayRate = 0.22; // decays per second
const recoveryThreshold = 0.3;

// Initialize app elements on load
window.addEventListener("DOMContentLoaded", () => {
    // Force active tab on startup
    switchAgentTab('keystone');
    
    // Core telemetry heartbeat interval timer (100ms ticks)
    setInterval(updateTelemetryStep, 100);
});

// =====================================================================
// DYNAMIC PARTITION SWITCHING LAYER (KRONOS CORE)
// =====================================================================
function switchAgentTab(tabId) {
    if (!PARTITION_SCHEMAS[tabId]) return;
    
    activeAgentTab = tabId;
    
    // 1. Update Tab Button Visual states
    document.querySelectorAll(".nav-tab").forEach(tab => {
        tab.classList.remove("active");
    });
    
    const clickedTab = document.querySelector(`.nav-tab[onclick*="${tabId}"]`);
    if (clickedTab) clickedTab.classList.add("active");
    
    // 2. Load context specific text
    const config = PARTITION_SCHEMAS[tabId];
    
    document.getElementById("vault-title").textContent = config.title;
    document.getElementById("vault-badge").textContent = config.badge;
    document.getElementById("vault-desc").textContent = config.desc;
    document.getElementById("suite-title").textContent = config.suiteTitle;
    document.getElementById("md-title").textContent = config.mdTitle;
    document.getElementById("md-badge-savings").textContent = config.mdSavings;
    
    // Set theme styling colors dynamically on header status components
    const daemonVal = document.getElementById("telemetry-daemon-val");
    const dbVal = document.getElementById("telemetry-db-val");
    const pingDot = document.getElementById("telemetry-ping-dot");
    const dbDot = document.getElementById("telemetry-db-dot");
    
    // Remove old coloring
    daemonVal.className = "telemetry-value";
    dbVal.className = "telemetry-value";
    pingDot.className = "status-dot pulse";
    dbDot.className = "status-dot";
    
    if (tabId === 'keystone') {
        daemonVal.classList.add("text-gold");
        dbVal.classList.add("text-gold");
        pingDot.classList.add("gold");
        dbDot.classList.add("gold");
    } else if (tabId === 'protocol') {
        daemonVal.classList.add("text-green");
        dbVal.classList.add("text-green");
        pingDot.classList.add("green");
        dbDot.classList.add("green");
    } else {
        daemonVal.classList.add("text-cyan");
        dbVal.classList.add("text-cyan");
        pingDot.classList.add("cyan");
        dbDot.classList.add("cyan");
    }
    
    // 3. Render dynamic lists & layouts
    renderVaultTree(config.docs);
    renderSuiteActions(config.suiteActions);
    
    // Load isolated graph schemas
    graphData = JSON.parse(JSON.stringify(config.graph));
    renderGraph();
    
    // Load isolated workers telemetry
    agentsState = JSON.parse(JSON.stringify(config.agents));
    renderAgentTelemetryGrid();
    
    // Reset path/logging states
    clearConsoleLogs();
    logToConsole(`KRONOS swiped memory focus to [${tabId.toUpperCase()}] partition successfully.`, "success");
    logToConsole(`Loaded ${config.docs.length} semantic assets to isolated active context.`, "info");
    
    detectConflicts();
    updateMarkdownViewer();
}

// Render dynamic documents tree list
function renderVaultTree(docs) {
    const container = document.getElementById("vault-tree-container");
    container.innerHTML = "";
    
    document.getElementById("vault-count").textContent = `${docs.length} Documents`;
    
    docs.forEach(doc => {
        const row = document.createElement("div");
        row.className = "vault-tree-item";
        row.innerHTML = `
            <div class="vault-item-left">
                <span class="vault-item-icon">${doc.icon}</span>
                <div class="vault-item-info">
                    <span class="vault-item-name">${doc.name}</span>
                    <span class="vault-item-path">${doc.path}</span>
                </div>
            </div>
            <span class="vault-item-size">${doc.size}</span>
        `;
        container.appendChild(row);
    });
}

// Render dynamic button action suite
function renderSuiteActions(actions) {
    const container = document.getElementById("suite-actions-container");
    container.innerHTML = "";
    
    actions.forEach(act => {
        const btn = document.createElement("button");
        btn.className = `btn btn-glass`;
        
        // Dynamically color hover styles
        if (activeAgentTab === 'keystone') {
            btn.onclick = new Function(`btnHoverColor(this, 'gold'); ${act.action}`);
        } else if (activeAgentTab === 'protocol') {
            btn.onclick = new Function(`btnHoverColor(this, 'green'); ${act.action}`);
        } else {
            btn.onclick = new Function(`btnHoverColor(this, 'cyan'); ${act.action}`);
        }
        
        btn.innerHTML = `<span class="btn-icon">${act.icon}</span> <span class="btn-text">${act.name}</span>`;
        container.appendChild(btn);
    });
}

function btnHoverColor(btn, theme) {
    // Dynamic color click highlights
    document.querySelectorAll(".actions-grid .btn").forEach(b => {
        b.className = "btn btn-glass";
    });
    btn.className = `btn btn-${theme}`;
}

// =====================================================================
// GRAPH SCHEMA RENDER ENGINE
// =====================================================================
function renderGraph() {
    const svg = document.getElementById("graph-svg");
    svg.innerHTML = ""; // Clear existing elements

    const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    defs.innerHTML = `
        <marker id="arrow" viewBox="0 0 10 10" refX="16" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(255, 255, 255, 0.15)"/>
        </marker>
        <marker id="arrow-active" viewBox="0 0 10 10" refX="16" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#D4AF37"/>
        </marker>
        <marker id="arrow-protocol" viewBox="0 0 10 10" refX="16" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#34D399"/>
        </marker>
        <marker id="arrow-spark" viewBox="0 0 10 10" refX="16" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#22D3EE"/>
        </marker>
    `;
    svg.appendChild(defs);

    // 1. Draw Links
    graphData.edges.forEach(edge => {
        const sourceNode = graphData.nodes.find(n => n.id === edge.source);
        const targetNode = graphData.nodes.find(n => n.id === edge.target);
        if (!sourceNode || !targetNode) return;

        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("id", edge.id);
        line.setAttribute("x1", sourceNode.x);
        line.setAttribute("y1", sourceNode.y);
        line.setAttribute("x2", targetNode.x);
        line.setAttribute("y2", targetNode.y);
        line.setAttribute("class", "edge-line");
        line.setAttribute("marker-end", "url(#arrow)");
        svg.appendChild(line);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("id", edge.id + "_label");
        text.setAttribute("x", (sourceNode.x + targetNode.x) / 2);
        text.setAttribute("y", (sourceNode.y + targetNode.y) / 2 - 6);
        text.setAttribute("class", "edge-label");
        text.textContent = edge.relationship;
        svg.appendChild(text);
    });

    // 2. Draw Nodes
    graphData.nodes.forEach(node => {
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("transform", `translate(${node.x}, ${node.y})`);
        g.style.cursor = "pointer";
        g.onclick = () => selectNode(node);

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("r", "15");
        circle.setAttribute("id", `node-${node.id}`);
        circle.setAttribute("class", `node-circle ${node.colorClass}`);
        g.appendChild(circle);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("class", "node-text");
        text.setAttribute("y", "3");
        text.textContent = node.name.length > 12 ? node.name.slice(0, 10) + ".." : node.name;
        g.appendChild(text);

        svg.appendChild(g);
    });
}

function selectNode(node) {
    document.querySelectorAll(".node-circle").forEach(c => c.classList.remove("active"));
    const circle = document.getElementById(`node-${node.id}`);
    if (circle) circle.classList.add("active");

    logToConsole(`[Graph-RAG] Inspected node '${node.name}' (Type: ${node.type})`, "info");
    
    // Find all edges linked
    const relatedEdges = graphData.edges.filter(e => e.source === node.id || e.target === node.id);
    if (relatedEdges.length > 0) {
        relatedEdges.forEach(e => {
            logToConsole(`- Linked Observation: [${e.source}] --(${e.relationship})--> [${e.target}] // "${e.observation}"`, "success");
            
            // Visual highlight of active edges in graph
            const visualEdge = document.getElementById(e.id);
            const visualLabel = document.getElementById(e.id + "_label");
            if (visualEdge) {
                visualEdge.classList.add("active-path");
                visualEdge.classList.add(activeAgentTab);
                
                let markerId = "arrow-active";
                if (activeAgentTab === 'protocol') markerId = "arrow-protocol";
                if (activeAgentTab === 'spark') markerId = "arrow-spark";
                visualEdge.setAttribute("marker-end", `url(#${markerId})`);
            }
            if (visualLabel) {
                visualLabel.classList.add("active-path");
            }
        });
    } else {
        logToConsole(`No immediate semantic paths found on node ${node.name}.`, "warn");
    }
}

function resetGraph() {
    const config = PARTITION_SCHEMAS[activeAgentTab];
    graphData = JSON.parse(JSON.stringify(config.graph));
    renderGraph();
    logToConsole(`[Graph-RAG] Restored original schema coordinates for the [${activeAgentTab.toUpperCase()}] partition.`, "success");
}

// =====================================================================
// DECAYING PHEROMONE MULTI-AGENT HEALING GRID
// =====================================================================
function renderAgentTelemetryGrid() {
    const container = document.getElementById("agent-telemetry-container");
    container.innerHTML = "";
    
    Object.keys(agentsState).forEach(id => {
        const agent = agentsState[id];
        const card = document.createElement("div");
        card.className = "agent-card glass-panel";
        card.id = agent.id;
        
        card.innerHTML = `
            <div class="agent-header">
                <span class="agent-name">${agent.name}</span>
                <span class="agent-status status-healthy" id="${agent.id}-status">Healthy</span>
            </div>
            <div class="agent-details">
                <p class="agent-task">Task: ${agent.task}</p>
                <div class="progress-bar-wrap">
                    <div class="progress-label">Pheromone: <span id="${agent.id}-ph">1.00</span></div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill fill-green" id="${agent.id}-fill" style="width: 100%;"></div>
                    </div>
                </div>
                <div class="agent-actions">
                    <button class="btn btn-sm btn-red" onclick="crashWorker('${agent.id}')">Trigger Crash</button>
                    <span class="heartbeat-pulse" id="${agent.id}-hb"></span>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

function updateTelemetryStep() {
    if (!agentsState) return;
    currentSimulationTime += 0.1;

    Object.keys(agentsState).forEach(id => {
        let agent = agentsState[id];

        if (agent.crashed) {
            if (agent.pheromone > 0.0) {
                agent.pheromone = Math.max(0.0, parseFloat((agent.pheromone - pheromoneDecayRate * 0.1).toFixed(3)));
                updateAgentDOM(agent);
            }
            
            if (agent.pheromone < recoveryThreshold && !agent.backupActive) {
                agent.backupActive = true;
                triggerSelfHealing(agent);
            }
        } else {
            // Heartbeat loop trigger
            if (currentSimulationTime - agent.lastHeartbeat >= agent.heartbeatRate) {
                agent.lastHeartbeat = currentSimulationTime;
                agent.pheromone = 1.0;
                triggerHeartbeatDOM(agent.id);
                updateAgentDOM(agent);
            }
        }
    });
}

function updateAgentDOM(agent) {
    const phLabel = document.getElementById(`${agent.id}-ph`);
    const barFill = document.getElementById(`${agent.id}-fill`);
    const statusLabel = document.getElementById(`${agent.id}-status`);

    if (phLabel) phLabel.textContent = agent.pheromone.toFixed(2);
    
    if (barFill) {
        barFill.style.width = `${agent.pheromone * 100}%`;
        if (agent.pheromone >= 0.7) {
            barFill.className = "progress-bar-fill fill-green";
        } else if (agent.pheromone >= 0.3) {
            barFill.className = "progress-bar-fill fill-yellow";
        } else {
            barFill.className = "progress-bar-fill fill-red";
        }
    }

    if (statusLabel) {
        if (agent.crashed) {
            statusLabel.textContent = "Silent";
            statusLabel.className = "agent-status status-crashed";
        } else {
            statusLabel.textContent = "Healthy";
            statusLabel.className = "agent-status status-healthy";
        }
    }
}

function triggerHeartbeatDOM(id) {
    const hb = document.getElementById(`${id}-hb`);
    if (hb) {
        hb.classList.add("beat");
        setTimeout(() => hb.classList.remove("beat"), 400);
    }
}

function crashWorker(id) {
    let agent = agentsState[id];
    if (agent.crashed) return;

    agent.crashed = true;
    agent.pheromone = 0.99;
    logToConsole(`[CRITICAL] Agent '${agent.name}' went silent! Heartbeats stopped. Pheromones decaying...`, "err");
    updateAgentDOM(agent);
}

function triggerSelfHealing(agent) {
    logToConsole(`[Self-Healing] Pheromone level for Agent '${agent.name}' fell below recovery threshold (${agent.pheromone.toFixed(2)}).`, "warn");
    logToConsole(`[Self-Healing] Reallocating Task '${agent.task}' to healthy backup worker...`, "info");
    
    const overlay = document.getElementById("self-healing-alert");
    const alertText = document.getElementById("alert-text");
    
    let backupName = "Backup_PM_Worker_99";
    if (activeAgentTab === 'protocol') backupName = "Backup_Voice_Worker_99";
    if (activeAgentTab === 'spark') backupName = "Backup_Tunnel_Worker_99";
    
    if (overlay && alertText) {
        alertText.innerHTML = `Emergency Intercept: Task **'${agent.task}'** failed.<br>Migrating from decayed <strong>${agent.name}</strong> to fresh backup <strong>${backupName}</strong>.`;
        overlay.classList.remove("hidden");
    }

    setTimeout(() => {
        agent.crashed = false;
        agent.backupActive = false;
        agent.name = backupName;
        agent.pheromone = 1.0;
        agent.lastHeartbeat = currentSimulationTime;
        
        if (overlay) overlay.classList.add("hidden");
        
        updateAgentDOM(agent);
        
        // Update local status card in panel representation
        const cardTitleName = document.querySelector(`#${agent.id} .agent-name`);
        if (cardTitleName) cardTitleName.textContent = backupName;
        
        logToConsole(`[Self-Healing Completed] Task '${agent.task}' successfully recovered under Worker '${backupName}'.`, "success");
    }, 1800);
}

// =====================================================================
// SEMANTIC CONFLICT RESOLUTION AUDITOR
// =====================================================================
function detectConflicts() {
    const warningContainer = document.getElementById("conflict-warning-container");
    const conflictSection = document.getElementById("conflict-card-section");
    const badge = document.getElementById("conflict-badge-status");
    
    warningContainer.innerHTML = "";
    let conflicts = [];

    // Simple semantic analysis for opposites
    for (let i = 0; i < graphData.edges.length; i++) {
        for (let j = i + 1; j < graphData.edges.length; j++) {
            let e1 = graphData.edges[i];
            let e2 = graphData.edges[j];

            if (e1.source === e2.source && e1.target === e2.target) {
                // Potential duplicate, verify if observations contradict
                let obs1 = e1.observation.toLowerCase();
                let obs2 = e2.observation.toLowerCase();

                const contradictoryCouplets = [
                    ["prevent", "cause"], ["prioritize", "avoid"],
                    ["cost transparency", "markup"], ["always", "never"],
                    ["transparent", "hidden"]
                ];

                contradictoryCouplets.forEach(([w1, w2]) => {
                    if ((obs1.includes(w1) && obs2.includes(w2)) || (obs2.includes(w1) && obs1.includes(w2))) {
                        conflicts.push({
                            entity: e1.source,
                            target: e1.target,
                            obs1: e1.observation,
                            src1: e1.sourceName,
                            obs2: e2.observation,
                            src2: e2.sourceName
                        });
                    }
                });
            }
        }
    }

    if (conflicts.length > 0) {
        conflictSection.classList.remove("hidden");
        badge.textContent = `${conflicts.length} Contradictions Found`;
        badge.className = "card-badge text-red";
        
        conflicts.forEach(conf => {
            const card = document.createElement("div");
            card.className = "conflict-alert-card";
            card.innerHTML = `
                <div class="conflict-card-title">⚡ Go-Style Semantic Contradiction: [${conf.entity}]</div>
                <div class="conflict-card-desc">
                    <span><strong>Contradiction detected targeting:</strong> ${conf.target}</span>
                    <span><strong>Observation 1 (Source: ${conf.src1}):</strong> "${conf.obs1}"</span>
                    <span><strong>Observation 2 (Source: ${conf.src2}):</strong> "${conf.obs2}"</span>
                </div>
            `;
            warningContainer.appendChild(card);
            logToConsole(`[GSC Auditor] WARNING: Epistemic contradiction found on Node '${conf.entity}'!`, "err");
        });
    } else {
        conflictSection.classList.add("hidden");
        badge.textContent = "0 Conflicts";
        badge.className = "card-badge";
    }
}

// =====================================================================
// INTERACTIVE SIMULATION UTILITIES
// =====================================================================
function logToConsole(message, type = "info") {
    const window = document.getElementById("console-logs-window");
    if (!window) return;

    const row = document.createElement("div");
    row.className = "log-row";

    const time = new Date().toLocaleTimeString();
    
    let tag = "";
    if (type === "success") tag = `<span class="log-tag-success">[SUCCESS]</span>`;
    else if (type === "warn") tag = `<span class="log-tag-warn">[WARN]</span>`;
    else if (type === "err") tag = `<span class="log-tag-err">[ERROR]</span>`;
    else tag = `<span class="log-tag-info">[INFO]</span>`;

    row.innerHTML = `<span class="log-timestamp">[${time}]</span> ${tag} ${message}`;
    
    window.appendChild(row);
    window.scrollTop = window.scrollHeight; // Auto-scroll
}

function clearConsoleLogs() {
    const window = document.getElementById("console-logs-window");
    if (window) window.innerHTML = "";
}

// Markdown Serializer View updates
function updateMarkdownViewer() {
    const viewer = document.getElementById("markdown-payload-viewer");
    if (!viewer) return;

    let lines = [`# 🧠 Epistemic observations - ${activeAgentTab.toUpperCase()}`];
    
    graphData.edges.forEach((edge, idx) => {
        let indexStr = (idx + 1).toString().padStart(2, '0');
        lines.push(`## [${indexStr}] ${edge.source} --(${edge.relationship})--> ${edge.target}`);
        lines.push(`- **Observation:** ${edge.observation}`);
        lines.push(`- **Metadata Source:** ${edge.sourceName}`);
    });

    const payload = lines.join("\n");
    viewer.textContent = payload;
}

// =====================================================================
// INTERACTIVE AUTOMATION TOOLS TRIGGERS
// =====================================================================

// KEYSTONE ACTIONS
function triggerVerifyNAP() {
    logToConsole("Initiating hyper-local citation consistency sweep...", "info");
    setTimeout(() => {
        logToConsole("Auditing Squamish GBP registry entry: Active.", "info");
        logToConsole("Verifying NAP character-for-character consistency across Yelp, BBB and local schema...", "info");
        logToConsole("BC Builder License #52603 aligned across all local profiles.", "success");
        logToConsole("NAP consistency successfully verified! Zero discrepancies found.", "success");
    }, 600);
}

function triggerAuditSchema() {
    logToConsole("Auditing local custom home HTML landing page schemas...", "info");
    setTimeout(() => {
        logToConsole("Checking /project-management/whistler_custom_homes.html LocalBusiness metadata...", "info");
        logToConsole("Schema matches Squamish coordinate coordinates, builder registration, and fiduciary PM tags.", "info");
        logToConsole("GSC schema validation: PASS (Zero errors, Zero warnings).", "success");
    }, 700);
}

function triggerIndexing() {
    logToConsole("Activating Rank Math Instant Indexing service account proxy...", "info");
    logToConsole("Sending POST query to Google Indexing API endpoint...", "info");
    setTimeout(() => {
        logToConsole("Payload: https://keystonepossibilities.ca/project-management/whistler_custom_homes.html", "info");
        logToConsole("Google Crawler response: 200 OK. URL enqueued for instant crawl sweep.", "success");
        logToConsole("Next.js local SEO static assets successfully indexing live!", "success");
    }, 800);
}

function triggerVideoCompile() {
    logToConsole("Parsing approved media timeline: whistler_villa_30s_short.md...", "info");
    setTimeout(() => {
        logToConsole("verifying strict 10s modular scene segmentation: PASS (3 scenes).", "info");
        logToConsole("verifying 14-word builder voiceover limit check: PASS (14, 14, and 15 words).", "info");
        logToConsole("evaluating Look-Off transitions at second 8 of Clips 001 and 002: PASS.", "info");
        logToConsole("DaVinci Resolve timeline compilation successful! Ready for rendering.", "success");
    }, 600);
}

// PROTOCOL ACTIONS
function triggerScriptCompile() {
    logToConsole("Processing GLP-1 peptide hypertrophy video timeline scripts...", "info");
    setTimeout(() => {
        logToConsole("Analyzing script path: Scripts_Approved/glp1_sarcopenia_40s_short.md", "info");
        logToConsole("verifying confident sideways look-off gestures at second 8: PASS.", "info");
        logToConsole("ElevenLabs continuous voice file successfully compiled with look-off alignment.", "success");
    }, 700);
}

function triggerVoiceAudit() {
    logToConsole("Auditing ElevenLabs audio vocal pace consistency...", "info");
    setTimeout(() => {
        logToConsole("Evaluating voice track duration: 30.12s against script total.", "info");
        logToConsole("Voice jitter coefficient: 0.02 (Optimal steady PNW builder tone).", "success");
        logToConsole("Lip-sync vocal alignment checks completely satisfied.", "success");
    }, 600);
}

function triggerProteinFloor() {
    logToConsole("Calculating optimal protein floor titration schedules...", "info");
    setTimeout(() => {
        logToConsole("Patient parameter constraints loaded: Age 43, heavy resistance load training, active GLP-1 therapy.", "info");
        logToConsole("Targeting optimal skeletal muscle hypertrophic preservation floor...", "info");
        logToConsole("Calculation result: 2.2 grams of protein per kg of lean mass = 200g daily floor.", "success");
    }, 500);
}

function triggerGLP1Check() {
    logToConsole("Reviewing GLP-1 peptide cell titration protocols...", "info");
    setTimeout(() => {
        logToConsole("Comparing Tirzepatide, Retatrutide, and Semaglutide efficacy guides...", "info");
        logToConsole("Warning: Rapid weight decreases accelerate muscle sarcopenia states. Keep protein floor locked.", "warn");
        logToConsole("longevity protocols verified successfully.", "success");
    }, 800);
}

// SPARK ACTIONS
function triggerVPNAudit() {
    logToConsole("Testing US proxy routing tunnel latency...", "info");
    setTimeout(() => {
        logToConsole("Current Local IP Location: Canada (Squamish / Vancouver).", "warn");
        logToConsole("Redirecting API traffic through Virginia proxy gateway...", "info");
        logToConsole("US Proxy redirection handshake: success.", "success");
        logToConsole("Response Latency: 42ms. Early-access blocks bypassed successfully.", "success");
    }, 650);
}

function triggerScrapingDaemon() {
    logToConsole("Launching headless scraping browser daemon...", "info");
    setTimeout(() => {
        logToConsole("Target endpoint enqueued: early release developer targets.", "info");
        logToConsole("Running background workers on US proxy tunnel...", "info");
        logToConsole("Scraping status: Listening. Enqueueing database sync payloads.", "success");
    }, 750);
}

function triggerVectorSync() {
    logToConsole("Refreshing SQLite-Vec database partition embeddings...", "info");
    setTimeout(() => {
        logToConsole("Verifying local database connection at local_vector_db/...", "info");
        logToConsole("Ingested 4 distinct document chunks to pgvector indices.", "info");
        logToConsole("Deduplication check: Dissolved 2 duplicate entries cleanly.", "success");
        logToConsole("Vector sync completed. Embedding coordinates fully updated.", "success");
    }, 800);
}

function triggerCryptVault() {
    logToConsole("Decrypting Plexus symmetric credentials vault...", "info");
    setTimeout(() => {
        logToConsole("Sovereign coordinator key handshake active...", "info");
        logToConsole("credentials decrypted safely at rest. Token quotas active.", "success");
    }, 550);
}
