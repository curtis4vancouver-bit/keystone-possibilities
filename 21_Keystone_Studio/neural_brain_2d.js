/* ==========================================================================
   KEYSTONE NEXT-GEN CELESTIAL VECTOR BRAIN & KNOWLEDGE CORTEX ENGINE (2026)
   Aesthetic: Stationary Galaxy Clusters (Non-Spinning by Default),
              Concentric Multi-Tier Polar Layout (Rings 1-4: 140px / 225px / 315px / 410px),
              Tier 3 Subfolder-Centered File Clustered Fan-Outs (Wayne's Image 5 Layout),
              Dark Glass HUD Backdrop Pills for Subfolders ([blog posts], [music], etc.),
              2D Quadtree Screen-Space Label Collision Solver (Zero Label Smearing),
              Smooth Focus & Zoom-In on Click ("When you zoom in, you click on it, it opens up"),
              2-Pass Curved Quadratic Bezier Wikilink Laser Filaments,
              Zero-Glitch Offscreen Frame Memoization & Frustum Culling,
              1-Click Video / Picture Toggle, Kinematic Cluster Dragging,
              and Interactive Markdown Wiki Reader.
   ========================================================================== */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory();
  } else {
    root.NeuralBrain2D = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // The 20 Canonical Keystone Brain Orb Mappings (High-Resolution Stagnant Pictures)
  const VIDEO_ORB_DEFS = [
    { key: '04_vector_brain', match: ['04_vector_brain', 'vector_brain', 'cortex', 'root'], image: 'assets/brain_orbs/01_core_brain_nucleus.png', color: '#00f0ff', isCore: true, name: '04_vector_brain (Core Nucleus)' },
    { key: '00_todays_video_upload', match: ['00_todays_video_upload', 'video_upload', 'todays_video'], image: 'assets/brain_orbs/02_00_todays_video_upload.png', color: '#ff5722', name: '00_todays_video_upload' },
    { key: '01_system_rules', match: ['01_system_rules', '01_overview', 'rules', 'system_rules'], image: 'assets/brain_orbs/03_01_system_rules.png', color: '#f59e0b', name: '01_system_rules' },
    { key: '02_skills', match: ['02_skills', 'skills'], image: 'assets/brain_orbs/04_02_skills.png', color: '#06b6d4', name: '02_skills' },
    { key: '03_MCP', match: ['03_mcp', 'mcp'], image: 'assets/brain_orbs/05_03_mcp.png', color: '#3b82f6', name: '03_MCP' },
    { key: '04_Wayne_Stevenson_health_stats', match: ['04_wayne_stevenson_health_stats', 'health_stats', 'wolverine'], image: 'assets/brain_orbs/06_04_health_stats.png', color: '#10b981', name: '04_health_stats' },
    { key: '04_brand_assets', match: ['04_brand_assets', 'brand_assets'], image: 'assets/brain_orbs/07_04_brand_assets.png', color: '#ec4899', name: '04_brand_assets' },
    { key: '05_Keystone_HUD', match: ['05_keystone_hud', 'hud'], image: 'assets/brain_orbs/08_05_keystone_hud.png', color: '#8b5cf6', name: '05_Keystone_HUD' },
    { key: '06_Keystone_possibilities', match: ['06_keystone_possibilities', 'possibilities', 'bill_44'], image: 'assets/brain_orbs/09_06_keystone_possibilities.png', color: '#38bdf8', name: '06_Keystone_possibilities' },
    { key: '06_keystone_money_polymarket_stocks', match: ['06_keystone_money_polymarket_stocks', 'money_polymarket', 'polymarket_stocks', 'tennis_sentinel'], image: 'assets/brain_orbs/10_06_money_polymarket.png', color: '#10b981', name: '06_money_polymarket' },
    { key: '07_Keystone_recomposition', match: ['07_keystone_recomposition', 'recomposition', 'deep_house'], image: 'assets/brain_orbs/11_07_keystone_recomposition.png', color: '#f97316', name: '07_Keystone_recomposition' },
    { key: '08_Keystone_protocols', match: ['08_keystone_protocols', 'protocols', 'peptides'], image: 'assets/brain_orbs/12_08_keystone_protocols.png', color: '#a855f7', name: '08_Keystone_protocols' },
    { key: '09_Keystone_websites', match: ['09_keystone_websites', 'websites', 'wordpress'], image: 'assets/brain_orbs/13_09_keystone_websites.png', color: '#06b6d4', name: '09_Keystone_websites' },
    { key: '10_researcher', match: ['10_researcher', 'researcher'], image: 'assets/brain_orbs/14_10_researcher.png', color: '#6366f1', name: '10_researcher' },
    { key: '11_global_LLM_engines', match: ['11_global_llm_engines', 'global_llm_engines', 'llm_engines'], image: 'assets/brain_orbs/15_11_global_llm_engines.png', color: '#fbbf24', name: '11_global_LLM_engines' },
    { key: '16_daemons', match: ['16_daemons', 'daemons'], image: 'assets/brain_orbs/16_16_daemons.png', color: '#ef4444', name: '16_daemons' },
    { key: '17_subagents', match: ['17_subagents', 'subagents'], image: 'assets/brain_orbs/17_17_subagents.png', color: '#f43f5e', name: '17_subagents' },
    { key: '18_session_continuity', match: ['18_session_continuity', 'session_continuity', 'continuity'], image: 'assets/brain_orbs/18_18_session_continuity.png', color: '#14b8a6', name: '18_session_continuity' },
    { key: '19_hardware_profiles', match: ['19_hardware_profiles', 'hardware_profiles', 'yunzii'], image: 'assets/brain_orbs/19_19_hardware_profiles.png', color: '#84cc16', name: '19_hardware_profiles' },
    { key: '20_Keystone_money', match: ['20_keystone_money', 'keystone_money', 'wealth'], image: 'assets/brain_orbs/20_20_keystone_money.png', color: '#10b981', name: '20_Keystone_money' }
  ];

  // Image Element Cache for Zero-Glitch Stagnant Orb Pictures
  const IMAGE_CACHE = new Map();

  function getOrbImage(imagePath) {
    if (!imagePath) return null;
    if (IMAGE_CACHE.has(imagePath)) {
      return IMAGE_CACHE.get(imagePath);
    }
    const img = new Image();
    img.src = imagePath;
    IMAGE_CACHE.set(imagePath, img);
    return img;
  }

  // Helper: Markdown to HTML Formatter with [[wikilinks]]
  function parseMarkdown(md) {
    if (!md) return '';
    let html = md
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // [[wikilinks]] -> Interactive clickable links
    html = html.replace(/\[\[(.*?)\]\]/g, (match, linkText) => {
      const parts = linkText.split('|');
      const target = parts[0].trim();
      const display = parts[1] ? parts[1].trim() : target;
      return `<a class="wiki-link" data-wiki-target="${target}" title="Jump to ${target}">[[${display}]]</a>`;
    });

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h4 style="color:#00f0ff; margin:14px 0 6px; font-size:13px;">$1</h4>');
    html = html.replace(/^## (.*$)/gim, '<h3 style="color:#fbbf24; margin:16px 0 8px; font-size:14px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:4px;">$1</h3>');
    html = html.replace(/^# (.*$)/gim, '<h2 style="color:#fff; margin:18px 0 10px; font-size:16px; border-bottom:1px solid rgba(0,240,255,0.25); padding-bottom:6px;">$1</h2>');

    // Code blocks
    html = html.replace(/```([a-zA-Z0-9_\-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre style="background:rgba(0,0,0,0.5); border:1px solid rgba(0,240,255,0.2); border-radius:6px; padding:10px; font-family:'JetBrains Mono',monospace; font-size:11px; color:#a78bfa; overflow-x:auto;"><code>${code}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,0.08); border-radius:3px; padding:1px 5px; font-family:\'JetBrains Mono\',monospace; color:#00f0ff;">$1</code>');

    // Bold & Italics
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong style="color:#fff;">$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em style="color:#cbd5e1;">$1</em>');

    // Bullet points
    html = html.replace(/^\s*[\-\*]\s+(.*$)/gim, '<li style="margin-left:16px; margin-bottom:4px;">$1</li>');

    // Paragraph breaks
    html = html.replace(/\n\n+/g, '<br><br>');

    return html;
  }

  // --------------------------------------------------------------------------
  // 2D Quadtree Spatial Index & Screen-Space Label Collision Solver
  // Adapted from Wayne's favorite 05_Keystone_HUD labelCollisionSolver
  // --------------------------------------------------------------------------
  class Quadtree {
    constructor(bounds, maxItems = 6, maxDepth = 8, depth = 0) {
      this.bounds = bounds;
      this.maxItems = maxItems;
      this.maxDepth = maxDepth;
      this.depth = depth;
      this.items = [];
      this.nodes = [];
    }

    clear() {
      this.items = [];
      for (let i = 0; i < this.nodes.length; i++) {
        this.nodes[i].clear();
      }
      this.nodes = [];
    }

    subdivide() {
      const subWidth = this.bounds.width / 2;
      const subHeight = this.bounds.height / 2;
      const x = this.bounds.x;
      const y = this.bounds.y;
      this.nodes[0] = new Quadtree({ x, y, width: subWidth, height: subHeight }, this.maxItems, this.maxDepth, this.depth + 1);
      this.nodes[1] = new Quadtree({ x: x + subWidth, y, width: subWidth, height: subHeight }, this.maxItems, this.maxDepth, this.depth + 1);
      this.nodes[2] = new Quadtree({ x, y: y + subHeight, width: subWidth, height: subHeight }, this.maxItems, this.maxDepth, this.depth + 1);
      this.nodes[3] = new Quadtree({ x: x + subWidth, y: y + subHeight, width: subWidth, height: subHeight }, this.maxItems, this.maxDepth, this.depth + 1);
    }

    getQuadrantIndex(box) {
      const midX = this.bounds.x + this.bounds.width / 2;
      const midY = this.bounds.y + this.bounds.height / 2;
      const boxMinX = box.x - box.width / 2;
      const boxMaxX = box.x + box.width / 2;
      const boxMinY = box.y - box.height / 2;
      const boxMaxY = box.y + box.height / 2;

      const topQuadrant = boxMaxY <= midY;
      const bottomQuadrant = boxMinY >= midY;

      if (boxMaxX <= midX) {
        if (topQuadrant) return 0;
        if (bottomQuadrant) return 2;
      } else if (boxMinX >= midX) {
        if (topQuadrant) return 1;
        if (bottomQuadrant) return 3;
      }
      return -1;
    }

    insert(box) {
      if (this.nodes.length > 0) {
        const index = this.getQuadrantIndex(box);
        if (index !== -1) {
          this.nodes[index].insert(box);
          return;
        }
      }

      this.items.push(box);

      if (this.items.length > this.maxItems && this.depth < this.maxDepth) {
        if (this.nodes.length === 0) {
          this.subdivide();
        }
        let i = 0;
        while (i < this.items.length) {
          const item = this.items[i];
          const index = this.getQuadrantIndex(item);
          if (index !== -1) {
            this.nodes[index].insert(item);
            this.items.splice(i, 1);
          } else {
            i++;
          }
        }
      }
    }

    intersects(bounds, box) {
      const boxMinX = box.x - box.width / 2;
      const boxMaxX = box.x + box.width / 2;
      const boxMinY = box.y - box.height / 2;
      const boxMaxY = box.y + box.height / 2;
      return !(
        boxMinX > bounds.x + bounds.width ||
        boxMaxX < bounds.x ||
        boxMinY > bounds.y + bounds.height ||
        boxMaxY < bounds.y
      );
    }

    retrieve(returnObjects, box) {
      const index = this.getQuadrantIndex(box);
      if (index !== -1 && this.nodes.length > 0) {
        this.nodes[index].retrieve(returnObjects, box);
      } else if (this.nodes.length > 0) {
        for (let i = 0; i < this.nodes.length; i++) {
          if (this.intersects(this.nodes[i].bounds, box)) {
            this.nodes[i].retrieve(returnObjects, box);
          }
        }
      }
      for (let i = 0; i < this.items.length; i++) {
        returnObjects.push(this.items[i]);
      }
      return returnObjects;
    }
  }

  function solveLabelCollisions(boxes, viewportBounds) {
    if (!boxes || boxes.length === 0) return [];
    const indexedBoxes = boxes.map((box, index) => ({ box: { ...box }, originalIndex: index }));
    // Sort descending by priority (highest priority processed first)
    indexedBoxes.sort((a, b) => b.box.priority - a.box.priority);

    let minX = viewportBounds ? viewportBounds.x : -2000;
    let minY = viewportBounds ? viewportBounds.y : -2000;
    let width = viewportBounds ? viewportBounds.width : 4000;
    let height = viewportBounds ? viewportBounds.height : 4000;

    const quadtree = new Quadtree({ x: minX - 100, y: minY - 100, width: width + 200, height: height + 200 }, 6, 8);
    const accepted = [];

    indexedBoxes.forEach(({ box }) => {
      // Selected or Hovered nodes are always visible
      if (box.priority >= 380) {
        box.visible = true;
        accepted.push(box);
        quadtree.insert(box);
        return;
      }

      const halfW1 = box.width / 2;
      const halfH1 = box.height / 2;
      const candidateBoxes = quadtree.retrieve([], box);

      const hasCollision = candidateBoxes.some(other => {
        const halfW2 = other.width / 2;
        const halfH2 = other.height / 2;
        return (
          Math.abs(box.x - other.x) < (halfW1 + halfW2 + 4) &&
          Math.abs(box.y - other.y) < (halfH1 + halfH2 + 3)
        );
      });

      if (hasCollision) {
        box.visible = false;
      } else {
        box.visible = true;
        accepted.push(box);
        quadtree.insert(box);
      }
    });

    indexedBoxes.sort((a, b) => a.originalIndex - b.originalIndex);
    return indexedBoxes.map(item => item.box);
  }

  /**
   * Golden-Angle Non-Overlapping Spot Allocator for Domain Hub Centroids.
   * Adapted from Wayne's favorite 05_Keystone_HUD VectorBrainPage engine.
   */
  function allocateCanvasFolderSpots(folderNames, centerX, centerY, clusterRadiiMap) {
    const allocated = {};
    const MARGIN = 120;
    const GOLDEN_ANGLE = 137.507764 * (Math.PI / 180);
    const BASE_ORBIT_RADIUS = 660;
    const RADIAL_STEP = 65;

    folderNames.forEach(folderId => {
      const radiusA = clusterRadiiMap[folderId] || 250;
      let spotX = centerX;
      let spotY = centerY;
      let found = false;

      for (let step = 0; step < 10000 && !found; step++) {
        const angle = step * GOLDEN_ANGLE;
        const distFromCenter = BASE_ORBIT_RADIUS + Math.sqrt(step) * RADIAL_STEP;
        const candX = centerX + distFromCenter * Math.cos(angle);
        const candY = centerY + distFromCenter * Math.sin(angle);

        let overlaps = false;
        for (const placedId of Object.keys(allocated)) {
          const placed = allocated[placedId];
          const dx = candX - placed.x;
          const dy = candY - placed.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const minDist = radiusA + placed.clusterRadius + MARGIN;
          if (dist < minDist) {
            overlaps = true;
            break;
          }
        }

        if (!overlaps) {
          spotX = candX;
          spotY = candY;
          found = true;
        }
      }

      allocated[folderId] = {
        x: spotX,
        y: spotY,
        clusterRadius: radiusA
      };
    });

    const result = {};
    Object.keys(allocated).forEach(id => {
      result[id] = { x: allocated[id].x, y: allocated[id].y };
    });
    return result;
  }

  class CelestialVectorBrainVisualizer {
    constructor(container) {
      this.container = container;
      this.canvas = null;
      this.ctx = null;
      this.width = container.clientWidth || 1000;
      this.height = container.clientHeight || 700;

      // Transform & Camera
      this.panX = this.width / 2;
      this.panY = this.height / 2;
      this.scale = 0.85;

      // Smooth Camera Animation ("When you zoom in, you click on it, it opens up")
      this.targetPanX = this.panX;
      this.targetPanY = this.panY;
      this.targetScale = this.scale;
      this.isAnimatingCamera = false;

      // Drag vs Click Tracking
      this.pointerDownX = 0;
      this.pointerDownY = 0;
      this.dragDistance = 0;

      // Celestial Graph Nodes, Links, Particles & Wikilinks
      this.nodes = [];
      this.links = [];
      this.wikilinkEdges = [];
      this.particles = [];
      this.nodeMap = new Map();
      this.coreNode = null;
      this.selectedNode = null;

      // Physics & Celestial Orbit Parameters (Stationary by default!)
      this.time = 0;
      this.orbitsEnabled = false; // Default: Wayne's preferred non-spinning stationary graph!
      this.showOrbits = true;
      this.keplerSpeedMult = 0.25;
      this.bloomEnabled = true;
      this.mediaMode = 'video'; // 'video' or 'picture'

      // Interaction States
      this.isDragging = false;
      this.dragNode = null;
      this.hoverNode = null;
      this.lastMouseX = 0;
      this.lastMouseY = 0;
      this.searchQuery = '';
      this.matchedNodeIds = new Set();

      // Drawer DOM References
      this.drawer = document.getElementById('brainWikiDrawer');

      this.initCanvas();
      this.preloadOrbImages();
      this.bindDOMControls();
      this.buildDefaultSolarSystem();
      this.isPaused = false;
      this.animationFrameId = null;
      this.animate = this.animate.bind(this);
      this.animationFrameId = requestAnimationFrame(this.animate);
    }

    initCanvas() {
      this.container.innerHTML = '';
      this.container.style.position = 'relative';
      this.container.style.width = '100%';
      this.container.style.height = '100%';
      this.container.style.overflow = 'hidden';

      this.canvas = document.createElement('canvas');
      this.canvas.id = 'neuralBrainCanvas';
      this.canvas.style.position = 'absolute';
      this.canvas.style.top = '0';
      this.canvas.style.left = '0';
      this.canvas.style.width = '100%';
      this.canvas.style.height = '100%';
      this.ctx = this.canvas.getContext('2d');
      this.container.appendChild(this.canvas);
      this.handleResize();

      // Tooltip
      this.tooltip = document.createElement('div');
      this.tooltip.className = 'cortex-tooltip';
      this.tooltip.style.display = 'none';
      this.container.appendChild(this.tooltip);
    }

    handleResize() {
      const dpr = window.devicePixelRatio || 1;
      this.width = this.container.clientWidth || 1000;
      this.height = this.container.clientHeight || 700;
      this.canvas.width = this.width * dpr;
      this.canvas.height = this.height * dpr;
      this.ctx.scale(dpr, dpr);
    }

    preloadOrbImages() {
      VIDEO_ORB_DEFS.forEach(def => {
        if (def.image) {
          getOrbImage(def.image);
        }
      });
    }

    toggleMediaMode() {
      return 'picture';
    }

    setMediaMode(mode) {
      this.mediaMode = 'picture';
    }

    buildDefaultSolarSystem() {
      const sunDef = VIDEO_ORB_DEFS[0];
      const sunNode = {
        id: 'keystone-brain',
        name: 'Keystone Brain Core',
        type: 'core',
        val: 38,
        color: '#00f0ff',
        image: getOrbImage(sunDef.image),
        imageDef: sunDef,
        x: 0,
        y: 0,
        vx: 0,
        vy: 0,
        orbitRadius: 0,
        baseAngle: 0,
        currentAngle: 0,
        path: '04_vector_brain',
        description: 'Central SIMD Vector Brain Nucleus, Qdrant memory matrix & 3D semantic graph.',
        tags: ['#nucleus', '#vector_brain', '#port9878', '#simd'],
        childrenNodes: []
      };
      this.coreNode = sunNode;
      this.nodes = [sunNode];
      this.nodeMap.clear();
      this.nodeMap.set(sunNode.id, sunNode);
    }

    // Dynamic Hot-Reloading from Workspace Tree JSON
    loadWorkspace(treeData) {
      if (!treeData || !Array.isArray(treeData) || treeData.length === 0) return;
      const rootItem = treeData[0];
      const children = rootItem.children || [];

      // 1. Central Core Nucleus (Keystone Brain Sun)
      const sunDef = VIDEO_ORB_DEFS[0];
      this.coreNode = {
        id: 'keystone-brain',
        name: rootItem.name || '🧠 KEYSTONE BRAIN',
        type: 'core',
        val: 38,
        color: '#00f0ff',
        image: getOrbImage(sunDef.image),
        imageDef: sunDef,
        x: 0,
        y: 0,
        vx: 0,
        vy: 0,
        orbitRadius: 0,
        baseAngle: 0,
        currentAngle: 0,
        path: rootItem.path || 'c:/Users/Curtis/Desktop/Keystone Brain',
        description: `Central SIMD Vector Brain Nucleus & Operational Galaxy Cortex for ${rootItem.name || 'Keystone Brain'}.`,
        tags: ['#nucleus', '#keystone_brain', '#simd', '#galaxy'],
        childrenNodes: []
      };

      this.nodes = [this.coreNode];
      this.nodeMap.clear();
      this.nodeMap.set(this.coreNode.id, this.coreNode);

      // 2. Identify Domain Folders
      const folderEntries = children.filter(c => c.type === 'folder');
      const allFolderNames = folderEntries.map(f => f.name);

      // Compute cluster radii for all folders prior to spot allocation
      const clusterRadiiMap = {};
      folderEntries.forEach(f => {
        const rawChildren = (f.children && Array.isArray(f.children)) ? f.children : [];
        const subfolderCount = rawChildren.filter(c => c.type === 'folder' || (c.children && Array.isArray(c.children))).length;
        let maxRadius = 160;
        if (subfolderCount > 8) maxRadius = 245;
        if (subfolderCount > 20) maxRadius = 335;
        if (subfolderCount > 36) maxRadius = 430;
        if (subfolderCount > 56) maxRadius = 540;
        clusterRadiiMap[f.name] = maxRadius + 75;
      });

      // Allocate canvas-wide non-overlapping spots using Golden-Angle multi-ring spot allocator
      const allocatedSpots = allocateCanvasFolderSpots(allFolderNames, 0, 0, clusterRadiiMap);
      const planetOrbDefs = VIDEO_ORB_DEFS.slice(1);

      folderEntries.forEach((f, idx) => {
        const spot = allocatedSpots[f.name] || { x: 500, y: 0 };
        const initialX = spot.x;
        const initialY = spot.y;
        const lowerName = f.name.toLowerCase();

        let matchedDef = planetOrbDefs.find(d => lowerName === d.key.toLowerCase()) ||
                         planetOrbDefs.find(d => d.match.some(m => lowerName.startsWith(m.toLowerCase()) || lowerName === m.toLowerCase())) ||
                         planetOrbDefs.find(d => d.match.some(m => lowerName.includes(m.toLowerCase())));

        const color = matchedDef ? matchedDef.color : `hsl(${(idx * 37) % 360}, 85%, 60%)`;
        const image = matchedDef ? getOrbImage(matchedDef.image) : null;

        const domainNode = {
          id: f.path || f.id || f.name,
          name: f.name,
          type: 'domain',
          val: matchedDef ? 22 : 18,
          color,
          image,
          imageDef: matchedDef,
          orbitRadius: Math.hypot(initialX, initialY),
          baseAngle: Math.atan2(initialY, initialX),
          currentAngle: Math.atan2(initialY, initialX),
          x: initialX,
          y: initialY,
          vx: 0,
          vy: 0,
          path: f.path || f.name,
          description: f.description || `Operational Domain Cluster: ${f.name}`,
          tags: f.tags || ['#domain', '#' + f.name.toLowerCase()],
          childrenNodes: [],
          guideRings: [140]
        };

        this.nodes.push(domainNode);
        this.nodeMap.set(domainNode.id, domainNode);

        // Group children into Subfolders vs Direct Files
        const rawChildren = (f.children && Array.isArray(f.children)) ? f.children : [];
        const subfolderItems = [];
        const directFileItems = [];

        rawChildren.forEach(child => {
          const isSub = child.type === 'folder' || (child.children && Array.isArray(child.children));
          if (isSub) {
            subfolderItems.push(child);
          } else {
            directFileItems.push(child);
          }
        });

        // Place subfolders across concentric polar tiers (prevents label overlap!)
        const SUBFOLDER_TIERS = [
          { capacity: 8, radius: 140 },
          { capacity: 12, radius: 225 },
          { capacity: 16, radius: 315 },
          { capacity: 20, radius: 410 },
          { capacity: 30, radius: 520 }
        ];

        let currentTierIdx = 0;
        let countInCurrentTier = 0;
        const subfolderPlacements = [];

        subfolderItems.forEach(sub => {
          while (currentTierIdx < SUBFOLDER_TIERS.length - 1 && countInCurrentTier >= SUBFOLDER_TIERS[currentTierIdx].capacity) {
            currentTierIdx++;
            countInCurrentTier = 0;
          }
          subfolderPlacements.push({
            item: sub,
            tierIndex: currentTierIdx,
            radius: SUBFOLDER_TIERS[currentTierIdx].radius
          });
          countInCurrentTier++;
        });

        const tierCounts = {};
        subfolderPlacements.forEach(p => {
          tierCounts[p.tierIndex] = (tierCounts[p.tierIndex] || 0) + 1;
        });

        const tierIndexCurrent = {};
        const guideRingsSet = new Set([140]);

        subfolderPlacements.forEach(({ item, tierIndex, radius }) => {
          guideRingsSet.add(radius);
          const totalInTier = tierCounts[tierIndex] || 1;
          const idxInTier = tierIndexCurrent[tierIndex] || 0;
          tierIndexCurrent[tierIndex] = idxInTier + 1;

          const angle = (idxInTier * 2 * Math.PI) / totalInTier + (tierIndex * Math.PI) / 4;
          const relX = radius * Math.cos(angle);
          const relY = radius * Math.sin(angle);

          const subNode = {
            id: item.path || `sub:${f.name}/${item.name}`,
            parent: domainNode.id,
            name: item.name,
            type: 'subfolder',
            isSub: true,
            val: 6.0,
            radius: 5.5,
            color: domainNode.color,
            relX,
            relY,
            x: initialX + relX,
            y: initialY + relY,
            vx: 0,
            vy: 0,
            path: item.path || `${f.name}/${item.name}`,
            description: item.description || `Subfolder: ${item.name}`,
            tags: item.tags || ['#folder', '#' + item.name.toLowerCase()],
            childrenNodes: []
          };

          this.nodes.push(subNode);
          this.nodeMap.set(subNode.id, subNode);
          domainNode.childrenNodes.push(subNode);

          // TIER 3: CHILD FILES ORBITING DIRECTLY AROUND THIS SUBFOLDER PILL (Wayne's Image 5 Layout!)
          const childFiles = (item.children && Array.isArray(item.children))
            ? item.children.filter(c => c.type !== 'folder')
            : [];

          if (childFiles.length > 0) {
            childFiles.forEach((subFile, sfIdx) => {
              const sfAngle = (sfIdx * 2 * Math.PI) / childFiles.length;
              const sfRadius = Math.min(65, 36 + Math.min(childFiles.length * 2.2, 28));
              const sfRelX = sfRadius * Math.cos(sfAngle);
              const sfRelY = sfRadius * Math.sin(sfAngle);

              const fileNode = {
                id: subFile.path || `file:${f.name}/${item.name}/${subFile.name}`,
                parent: subNode.id, // Linked to subfolder pill!
                name: subFile.name,
                type: 'file',
                isSub: false,
                val: 3.5,
                radius: 3.5,
                color: '#38bdf8',
                relX: sfRelX,
                relY: sfRelY,
                x: subNode.x + sfRelX,
                y: subNode.y + sfRelY,
                vx: 0,
                vy: 0,
                path: subFile.path || `${f.name}/${item.name}/${subFile.name}`,
                description: subFile.description || `Document: ${subFile.name}`,
                tags: subFile.tags || ['#file', '#' + item.name.toLowerCase()],
                childrenNodes: []
              };

              this.nodes.push(fileNode);
              this.nodeMap.set(fileNode.id, fileNode);
              subNode.childrenNodes.push(fileNode);
              domainNode.childrenNodes.push(fileNode); // for kinematic cluster drag
            });
          }
        });

        // Top-level direct files in domain (files not placed inside any subfolder)
        if (directFileItems.length > 0) {
          const highestSubRadius = subfolderPlacements.length > 0
            ? subfolderPlacements[subfolderPlacements.length - 1].radius
            : 140;
          const directFileRadius = highestSubRadius + 75;
          guideRingsSet.add(directFileRadius);

          directFileItems.forEach((df, dfIdx) => {
            const angle = (dfIdx * 2 * Math.PI) / directFileItems.length + Math.PI / 6;
            const relX = directFileRadius * Math.cos(angle);
            const relY = directFileRadius * Math.sin(angle);

            const fileNode = {
              id: df.path || `file:${f.name}/${df.name}`,
              parent: domainNode.id,
              name: df.name,
              type: 'file',
              isSub: false,
              val: 3.5,
              radius: 3.5,
              color: '#38bdf8',
              relX,
              relY,
              x: initialX + relX,
              y: initialY + relY,
              vx: 0,
              vy: 0,
              path: df.path || `${f.name}/${df.name}`,
              description: df.description || `Document: ${df.name}`,
              tags: df.tags || ['#file', '#' + f.name.toLowerCase()],
              childrenNodes: []
            };

            this.nodes.push(fileNode);
            this.nodeMap.set(fileNode.id, fileNode);
            domainNode.childrenNodes.push(fileNode);
          });
        }

        domainNode.guideRings = Array.from(guideRingsSet).sort((a, b) => a - b);
      });

      this.rebuildLinksAndWikilinks();
      this.centerCamera();

      const badge = document.getElementById('brainStatsNodes');
      if (badge) {
        badge.textContent = `${folderEntries.length} Domains Active`;
      }
    }

    rebuildLinksAndWikilinks() {
      this.links = [];
      this.wikilinkEdges = [];
      this.particles = [];

      // 1. Structural Intra-Cluster Links
      this.nodes.forEach(node => {
        if (node.type === 'domain') {
          this.links.push({
            source: this.coreNode,
            target: node,
            weight: 2.0,
            color: node.color
          });
        } else if (node.parent) {
          const parentNode = this.nodeMap.get(node.parent);
          if (parentNode) {
            this.links.push({
              source: parentNode,
              target: node,
              weight: node.isSub ? 1.5 : 0.8,
              color: parentNode.color || node.color || '#00f0ff'
            });
          }
        }
      });

      // 2. Canonical Cross-Cluster Wikilink Filaments (Laser Edges)
      const crossClusterPairs = [
        { from: '00_todays_video_upload', to: '07_Keystone_recomposition' },
        { from: '07_Keystone_recomposition', to: '08_Keystone_protocols' },
        { from: '06_keystone_money_polymarket_stocks', to: '20_Keystone_money' },
        { from: '01_system_rules', to: '02_skills' },
        { from: '02_skills', to: '03_MCP' },
        { from: '03_MCP', to: '16_daemons' },
        { from: '16_daemons', to: '17_subagents' },
        { from: '17_subagents', to: '18_session_continuity' },
        { from: '05_Keystone_HUD', to: '09_Keystone_websites' },
        { from: '10_researcher', to: '11_global_LLM_engines' }
      ];

      crossClusterPairs.forEach(pair => {
        const src = this.nodes.find(n => n.name.toLowerCase().includes(pair.from.toLowerCase()));
        const tgt = this.nodes.find(n => n.name.toLowerCase().includes(pair.to.toLowerCase()));
        if (src && tgt) {
          this.wikilinkEdges.push({
            source: src.id,
            target: tgt.id,
            color: 'rgba(0, 240, 255, 0.45)',
            label: 'wikilink'
          });
        }
      });

      // 3. Action-Potential Particles
      for (let i = 0; i < 45; i++) {
        if (this.links.length === 0) break;
        const link = this.links[Math.floor(Math.random() * this.links.length)];
        this.particles.push({
          link,
          t: Math.random(),
          speed: 0.003 + Math.random() * 0.007,
          size: 1.5 + Math.random() * 2.0,
          color: link.color || '#00f0ff'
        });
      }
    }

    bindDOMControls() {
      window.addEventListener('resize', () => this.handleResize());

      // Recenter Camera Button
      document.getElementById('btnRecenterBrain')?.addEventListener('click', () => {
        this.centerCamera();
      });

      // Orbits Toggle Button
      const orbitsBtn = document.getElementById('btnToggleOrbits');
      if (orbitsBtn) {
        orbitsBtn.addEventListener('click', () => {
          this.orbitsEnabled = !this.orbitsEnabled;
          orbitsBtn.textContent = this.orbitsEnabled ? '🪐 60 FPS ORBITS' : '⏸️ ORBITS: STATIONARY';
          orbitsBtn.style.color = this.orbitsEnabled ? '#00f0ff' : '#94a3b8';
        });
      }

      // Drawer Close Button
      document.getElementById('btnCloseWikiDrawer')?.addEventListener('click', () => {
        this.closeWikiDrawer();
      });

      // Canvas Dragging & Interaction
      this.canvas.addEventListener('mousedown', (e) => {
        this.isAnimatingCamera = false;
        this.pointerDownX = e.clientX;
        this.pointerDownY = e.clientY;
        this.dragDistance = 0;

        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const worldPos = this.screenToWorld(mx, my);

        const clicked = this.getNodeAt(worldPos.x, worldPos.y);
        if (clicked) {
          this.isDragging = true;
          this.dragNode = clicked;
          this.canvas.style.cursor = 'grabbing';
        } else {
          this.isDragging = true;
          this.dragNode = null;
          this.canvas.style.cursor = 'grabbing';
        }
        this.lastMouseX = e.clientX;
        this.lastMouseY = e.clientY;
      });

      window.addEventListener('mousemove', (e) => {
        if (this.isDragging) {
          this.dragDistance = Math.hypot(e.clientX - this.pointerDownX, e.clientY - this.pointerDownY);
          const dx = (e.clientX - this.lastMouseX) / this.scale;
          const dy = (e.clientY - this.lastMouseY) / this.scale;

          if (this.dragNode) {
            this.dragNode.x += dx;
            this.dragNode.y += dy;

            // Kinematic tied cluster dragging: translate all descendants in real-time lockstep
            if (this.dragNode.childrenNodes && this.dragNode.childrenNodes.length > 0) {
              this.dragNode.childrenNodes.forEach(child => {
                child.x += dx;
                child.y += dy;
              });
            }
          } else {
            this.panX += e.clientX - this.lastMouseX;
            this.panY += e.clientY - this.lastMouseY;
          }

          this.lastMouseX = e.clientX;
          this.lastMouseY = e.clientY;
        } else {
          const rect = this.canvas.getBoundingClientRect();
          const mx = e.clientX - rect.left;
          const my = e.clientY - rect.top;
          const worldPos = this.screenToWorld(mx, my);
          const hovered = this.getNodeAt(worldPos.x, worldPos.y);
          this.hoverNode = hovered;

          if (hovered) {
            this.canvas.style.cursor = 'pointer';
            this.tooltip.style.display = 'block';
            this.tooltip.style.left = `${mx + 12}px`;
            this.tooltip.style.top = `${my + 12}px`;
            this.tooltip.innerHTML = `<strong>${hovered.name}</strong><br><span style="color:${hovered.color};">${hovered.type.toUpperCase()}</span> • ${hovered.tags ? hovered.tags.join(' ') : ''}`;
          } else {
            this.canvas.style.cursor = 'grab';
            this.tooltip.style.display = 'none';
          }
        }
      });

      window.addEventListener('mouseup', () => {
        this.isDragging = false;
        this.dragNode = null;
        this.canvas.style.cursor = 'grab';
      });

      // Canvas Click -> Smooth Focus/Zoom & Open Slide-out Wiki Reader Drawer
      this.canvas.addEventListener('click', (e) => {
        // If dragged more than 5px, ignore click (user was panning canvas or dragging a node)
        if (this.dragDistance >= 6) return;

        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const worldPos = this.screenToWorld(mx, my);
        const clicked = this.getNodeAt(worldPos.x, worldPos.y);

        if (clicked) {
          this.selectedNode = clicked;
          this.focusNode(clicked);
          this.openWikiDrawer(clicked);
        }
      });

      // Canvas Focal-Point Mouse Wheel Zooming
      this.canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        this.isAnimatingCamera = false;
        const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        const newScale = Math.max(0.12, Math.min(6.0, this.scale * zoomFactor));
        this.panX = mouseX - (mouseX - this.panX) * (newScale / this.scale);
        this.panY = mouseY - (mouseY - this.panY) * (newScale / this.scale);
        this.scale = newScale;
      }, { passive: false });

      // Delegate Wikilink Clicks inside Wiki Drawer
      document.addEventListener('click', (e) => {
        const link = e.target.closest('.wiki-link');
        if (link) {
          e.preventDefault();
          const target = link.dataset.wikiTarget;
          if (target) {
            this.focusNodeBySearch(target);
          }
        }
      });
    }

    screenToWorld(sx, sy) {
      return {
        x: (sx - this.panX) / this.scale,
        y: (sy - this.panY) / this.scale
      };
    }

    getNodeAt(wx, wy) {
      for (let i = this.nodes.length - 1; i >= 0; i--) {
        const n = this.nodes[i];
        const hitRadius = (n.val || n.radius || 4) + (n.type === 'subfolder' || n.isSub ? 16 : 8);
        const dist = Math.hypot(n.x - wx, n.y - wy);
        if (dist <= hitRadius) return n;
      }
      return null;
    }

    centerCamera() {
      this.targetPanX = this.width / 2;
      this.targetPanY = this.height / 2;
      this.targetScale = 0.85;
      this.isAnimatingCamera = true;
    }

    focusNode(node, targetZoom = null) {
      if (!node) return;
      let zoom = targetZoom;
      if (zoom === null) {
        if (node.type === 'core') zoom = 0.95;
        else if (node.type === 'domain') zoom = 1.35;
        else if (node.type === 'subfolder' || node.isSub) zoom = 1.65;
        else zoom = 2.0;
      }
      this.targetScale = Math.max(0.15, Math.min(5.0, zoom));
      this.targetPanX = this.width / 2 - node.x * this.targetScale;
      this.targetPanY = this.height / 2 - node.y * this.targetScale;
      this.isAnimatingCamera = true;
    }

    focusNodeBySearch(query) {
      const q = (query || '').trim().toLowerCase();
      if (!q) return;
      const match = this.nodes.find(n => n.name.toLowerCase().includes(q) || n.id.toLowerCase().includes(q));
      if (match) {
        this.selectedNode = match;
        this.focusNode(match);
        this.openWikiDrawer(match);
      }
    }

    search(query) {
      this.searchQuery = (query || '').trim().toLowerCase();
      this.matchedNodeIds.clear();
      if (!this.searchQuery) return;

      this.nodes.forEach(n => {
        const matchName = n.name && n.name.toLowerCase().includes(this.searchQuery);
        const matchPath = n.path && n.path.toLowerCase().includes(this.searchQuery);
        const matchDesc = n.description && n.description.toLowerCase().includes(this.searchQuery);
        const matchTags = n.tags && n.tags.some(t => t.toLowerCase().includes(this.searchQuery));

        if (matchName || matchPath || matchDesc || matchTags) {
          this.matchedNodeIds.add(n.id);
        }
      });
    }

    async openWikiDrawer(node) {
      const drawer = document.getElementById('brainWikiDrawer');
      if (!drawer) return;

      drawer.classList.add('open');

      const title = document.getElementById('wikiDrawerTitle');
      const filename = document.getElementById('wikiFilename');
      const typePill = document.getElementById('wikiTypePill');
      const tagsContainer = document.getElementById('wikiTagsContainer');
      const body = document.getElementById('wikiDrawerBody');

      if (title) title.textContent = node.name;
      if (filename) filename.textContent = node.path || node.id;
      if (typePill) {
        typePill.textContent = (node.type || 'NODE').toUpperCase();
        typePill.style.color = node.color || '#00f0ff';
        typePill.style.borderColor = node.color || '#00f0ff';
      }

      if (tagsContainer) {
        tagsContainer.innerHTML = '';
        (node.tags || []).forEach(t => {
          const span = document.createElement('span');
          span.className = 'wiki-tag';
          span.textContent = t.startsWith('#') ? t : '#' + t;
          tagsContainer.appendChild(span);
        });
      }

      if (body) {
        body.innerHTML = `
          <div class="wiki-intro-card">
            <span class="tree-spinner" style="margin:0 auto 10px; display:block;"></span>
            <p style="text-align:center; color:#94a3b8;">Querying Vector Brain Port 9878 for node telemetry...</p>
          </div>
        `;
      }

      let content = '';
      if (node.path) {
        try {
          const res = await fetch(`http://127.0.0.1:9878/api/read_file?path=${encodeURIComponent(node.path)}`);
          if (res.ok) {
            const data = await res.json();
            content = data.content || '';
          }
        } catch (e) {}
      }

      if (body) {
        if (content) {
          body.innerHTML = parseMarkdown(content.slice(0, 16000));
        } else {
          body.innerHTML = `
            <div class="wiki-intro-card">
              <h4>${node.name}</h4>
              <p>${node.description || 'Knowledge Node actively indexed in Keystone Celestial Cortex.'}</p>
              <div style="margin-top:12px; font-family:'JetBrains Mono',monospace; font-size:11px; line-height:1.7;">
                <div><strong style="color:#00f0ff;">Node ID:</strong> ${node.id}</div>
                <div><strong style="color:#8b5cf6;">Type:</strong> ${node.type.toUpperCase()}</div>
                <div><strong style="color:#10b981;">Path:</strong> ${node.path || node.id}</div>
              </div>
            </div>
          `;
        }
      }

      const btnOpen = document.getElementById('btnOpenInExplorer');
      if (btnOpen) {
        btnOpen.onclick = async () => {
          try {
            await fetch('http://127.0.0.1:9878/api/reveal_in_explorer', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ path: node.path || node.id })
            });
          } catch (e) {}
        };
      }

      const btnCopy = document.getElementById('btnCopyWikiPath');
      if (btnCopy) {
        btnCopy.onclick = () => {
          navigator.clipboard?.writeText(node.path || node.id);
          btnCopy.textContent = '✅ COPIED!';
          setTimeout(() => { btnCopy.textContent = '📋 COPY PATH'; }, 1600);
        };
      }
    }

    closeWikiDrawer() {
      const drawer = document.getElementById('brainWikiDrawer');
      if (drawer) drawer.classList.remove('open');
    }

    updatePhysics() {
      this.time += 0.016;

      // Smooth Camera Interpolation ("When you zoom in, you click on it, it opens up")
      if (this.isAnimatingCamera) {
        this.panX += (this.targetPanX - this.panX) * 0.16;
        this.panY += (this.targetPanY - this.panY) * 0.16;
        this.scale += (this.targetScale - this.scale) * 0.16;
        if (
          Math.abs(this.targetPanX - this.panX) < 0.5 &&
          Math.abs(this.targetPanY - this.panY) < 0.5 &&
          Math.abs(this.targetScale - this.scale) < 0.005
        ) {
          this.panX = this.targetPanX;
          this.panY = this.targetPanY;
          this.scale = this.targetScale;
          this.isAnimatingCamera = false;
        }
      }

      // Only drift if user explicitly toggled orbits on!
      if (!this.orbitsEnabled) return;

      this.nodes.forEach(n => {
        if (n.type === 'core') return;
        if (n.type === 'domain' && n.orbitRadius && n !== this.dragNode) {
          const omega = 0.0008 * this.keplerSpeedMult;
          n.currentAngle = (n.currentAngle + omega) % (Math.PI * 2);
          const oldX = n.x;
          const oldY = n.y;
          n.x = Math.cos(n.currentAngle) * n.orbitRadius;
          n.y = Math.sin(n.currentAngle) * n.orbitRadius;
          const dx = n.x - oldX;
          const dy = n.y - oldY;

          if (n.childrenNodes) {
            n.childrenNodes.forEach(child => {
              child.x += dx;
              child.y += dy;
            });
          }
        }
      });
    }

    pause() {
      this.isPaused = true;
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
        this.animationFrameId = null;
      }
    }

    resume() {
      if (!this.isPaused) return;
      this.isPaused = false;
      this.handleResize();
      if (!this.animationFrameId) {
        this.animationFrameId = requestAnimationFrame(this.animate);
      }
    }

    animate() {
      if (this.isPaused) return;
      this.updatePhysics();
      this.render();
      this.animationFrameId = requestAnimationFrame(this.animate);
    }

    render() {
      const ctx = this.ctx;
      ctx.save();
      ctx.clearRect(0, 0, this.width, this.height);

      // Compute screen-space label bounding boxes and solve collisions using Quadtree
      const candidateBoxes = [];
      this.nodes.forEach(n => {
        const screenX = n.x * this.scale + this.panX;
        const screenY = n.y * this.scale + this.panY;
        const radiusScreen = (n.val || n.radius || 4) * this.scale;
        const isVisible = (
          screenX >= -radiusScreen - 120 &&
          screenX <= this.width + radiusScreen + 120 &&
          screenY >= -radiusScreen - 120 &&
          screenY <= this.height + radiusScreen + 120
        );
        n._screenX = screenX;
        n._screenY = screenY;
        n._isVisible = isVisible;
        if (!isVisible) return;

        const isHover = n === this.hoverNode;
        const isSelected = n === this.selectedNode;
        const isMatch = this.matchedNodeIds.has(n.id);

        let priority = 100;
        let labelOffsetY = n.val ? (n.val * this.scale + 14) : ((n.radius || 4) * this.scale + 10);
        let labelText = n.name || n.id;
        let fontCharWidth = 6.2;
        let fontSize = 10;

        if (isSelected) priority = 400;
        else if (isHover) priority = 380;
        else if (isMatch) priority = 350;
        else if (n.type === 'core') priority = 300;
        else if (n.type === 'domain') priority = 220;
        else if (n.type === 'subfolder' || n.isSub) {
          priority = 160;
          labelText = n.name.startsWith('[') ? n.name : `[${n.name}]`;
          fontCharWidth = 6.8;
          fontSize = 11;
        } else {
          priority = 90;
          fontCharWidth = 5.5;
          fontSize = 9;
        }

        const boxW = Math.max(16, labelText.length * fontCharWidth + 14);
        const boxH = fontSize + 8;

        candidateBoxes.push({
          id: n.id,
          label: labelText,
          x: screenX,
          y: screenY + labelOffsetY,
          width: boxW,
          height: boxH,
          priority,
          visible: true,
          node: n
        });
      });

      const solvedBoxes = solveLabelCollisions(candidateBoxes, { x: 0, y: 0, width: this.width, height: this.height });
      const labelVisibilityMap = new Map();
      solvedBoxes.forEach(b => {
        labelVisibilityMap.set(b.id, b.visible);
      });

      ctx.translate(this.panX, this.panY);
      ctx.scale(this.scale, this.scale);

      // 1. Draw Concentric Orbital Guide Rings around Domain Hubs
      if (this.showOrbits) {
        ctx.save();
        ctx.strokeStyle = 'rgba(0, 240, 255, 0.08)';
        ctx.lineWidth = 1.0;
        ctx.setLineDash([3, 7]);

        this.nodes.forEach(n => {
          if (n.type === 'domain' && n.guideRings) {
            n.guideRings.forEach(r => {
              ctx.beginPath();
              ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
              ctx.stroke();
            });
          }
        });
        ctx.restore();
      }

      // 2. Draw 2-Pass Curved Quadratic Bezier Wikilink Filaments
      this.wikilinkEdges.forEach(edge => {
        const src = this.nodeMap.get(edge.source);
        const tgt = this.nodeMap.get(edge.target);
        if (!src || !tgt) return;

        const isHover = this.hoverNode && (src === this.hoverNode || tgt === this.hoverNode);
        const isSelected = this.selectedNode && (src === this.selectedNode || tgt === this.selectedNode);
        const isMatched = this.matchedNodeIds.size > 0 && (this.matchedNodeIds.has(src.id) || this.matchedNodeIds.has(tgt.id));

        const midX = (src.x + tgt.x) / 2;
        const midY = (src.y + tgt.y) / 2;
        const dx = tgt.x - src.x;
        const dy = tgt.y - src.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const curvature = Math.min(80, dist * 0.18);
        const controlX = midX - (dy / dist) * curvature;
        const controlY = midY + (dx / dist) * curvature;

        const isHighlighted = isHover || isSelected || isMatched;
        const alpha = isHighlighted ? 0.9 : 0.45;

        // Pass 1: Diffuse outer neon glow
        ctx.save();
        ctx.shadowBlur = isHighlighted ? 18 : 12;
        ctx.shadowColor = '#00f0ff';
        ctx.lineWidth = isHighlighted ? 3.2 : 2.0;
        ctx.strokeStyle = edge.color || 'rgba(0, 240, 255, 0.4)';
        ctx.globalAlpha = alpha;

        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.quadraticCurveTo(controlX, controlY, tgt.x, tgt.y);
        ctx.stroke();
        ctx.restore();

        // Pass 2: High-intensity laser core
        ctx.save();
        ctx.shadowBlur = 0;
        ctx.lineWidth = isHighlighted ? 1.4 : 0.85;
        ctx.strokeStyle = isHighlighted ? '#ffffff' : '#00f0ff';
        ctx.globalAlpha = alpha;

        ctx.beginPath();
        ctx.moveTo(src.x, src.y);
        ctx.quadraticCurveTo(controlX, controlY, tgt.x, tgt.y);
        ctx.stroke();
        ctx.restore();
      });

      // 3. Draw Synaptic Links
      this.links.forEach(link => {
        const isHover = this.hoverNode && (link.source === this.hoverNode || link.target === this.hoverNode);
        const isSelected = this.selectedNode && (link.source === this.selectedNode || link.target === this.selectedNode);
        const isMatched = this.matchedNodeIds.size > 0 && (this.matchedNodeIds.has(link.source.id) || this.matchedNodeIds.has(link.target.id));

        const isHigh = isHover || isSelected || isMatched;
        ctx.strokeStyle = isHigh
          ? 'rgba(0, 240, 255, 0.75)'
          : (link.color ? `${link.color}28` : 'rgba(139, 92, 246, 0.15)');
        ctx.lineWidth = isHigh ? 2.0 : 0.9;

        ctx.beginPath();
        ctx.moveTo(link.source.x, link.source.y);
        ctx.lineTo(link.target.x, link.target.y);
        ctx.stroke();
      });

      // 4. Draw Action-Potential Particles
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      this.particles.forEach(p => {
        p.t += p.speed;
        if (p.t > 1) p.t = 0;

        const lx = p.link.source.x + (p.link.target.x - p.link.source.x) * p.t;
        const ly = p.link.source.y + (p.link.target.y - p.link.source.y) * p.t;

        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(lx, ly, p.size, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.restore();

      // 5. Render All Nodes
      this.nodes.forEach(n => {
        const isHover = n === this.hoverNode;
        const isSelected = n === this.selectedNode;
        const isMatch = this.matchedNodeIds.has(n.id);
        const hasSearch = this.searchQuery.length > 0;
        const isDimmed = hasSearch && !isMatch;
        const isVisible = n._isVisible !== false;

        ctx.save();
        if (isDimmed) ctx.globalAlpha = 0.18;

        // A. Central Black Hole / Sun Core
        if (n.type === 'core') {
          const coronaPulse = 1.0 + Math.sin(this.time * 2.2) * 0.06;
          const sunGrad = ctx.createRadialGradient(n.x, n.y, n.val * 0.5, n.x, n.y, n.val * 2.4 * coronaPulse);
          sunGrad.addColorStop(0, 'rgba(0, 240, 255, 0.45)');
          sunGrad.addColorStop(0.4, 'rgba(139, 92, 246, 0.22)');
          sunGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
          ctx.fillStyle = sunGrad;
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.val * 2.4 * coronaPulse, 0, Math.PI * 2);
          ctx.fill();

          // Singularity dashed reticle
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.val + 8, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(0, 240, 255, 0.6)';
          ctx.lineWidth = 1.2;
          ctx.setLineDash([8, 6]);
          ctx.stroke();
          ctx.setLineDash([]);
        } else if (this.bloomEnabled && (isHover || isSelected || isMatch || n.type === 'domain')) {
          const glowRadius = (n.val || n.radius || 4) * 2.0;
          const glowGrad = ctx.createRadialGradient(n.x, n.y, (n.val || n.radius || 4) * 0.4, n.x, n.y, glowRadius);
          glowGrad.addColorStop(0, n.color || '#00f0ff');
          glowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
          ctx.fillStyle = glowGrad;
          ctx.beginPath();
          ctx.arc(n.x, n.y, glowRadius, 0, Math.PI * 2);
          ctx.fill();
        }

        // B. Node Rendering: Core & Domain vs Subfolder Pills vs File Nodes
        if (n.type === 'core' || n.type === 'domain') {
          let frameDrawn = false;

          // ZERO-GLITCH HARDWARE-ACCELERATED HIGH-RESOLUTION ORB PICTURE RENDERING
          const orbImg = n.image;
          if (orbImg && orbImg.complete && orbImg.naturalWidth > 0) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.val, 0, Math.PI * 2);
            ctx.closePath();
            ctx.clip();
            try {
              ctx.drawImage(orbImg, n.x - n.val, n.y - n.val, n.val * 2, n.val * 2);
              frameDrawn = true;
            } catch (e) {}
            ctx.restore();
          }

          // Fallback Cyber Gradient Base if image not yet loaded
          if (!frameDrawn) {
            const grad = ctx.createRadialGradient(n.x, n.y, 4, n.x, n.y, n.val);
            grad.addColorStop(0, n.color || '#00f0ff');
            grad.addColorStop(1, '#050714');
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.val, 0, Math.PI * 2);
            ctx.fill();
          }

          // Precision Border Rings
          ctx.strokeStyle = isMatch ? '#ffd700' : (isSelected ? '#ffffff' : (n.color || '#00f0ff'));
          ctx.lineWidth = isMatch || isSelected ? 3.0 : 1.8;
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.val, 0, Math.PI * 2);
          ctx.stroke();

          // Caliper Outer Ring
          ctx.strokeStyle = isMatch ? '#ffd700' : 'rgba(0, 240, 255, 0.4)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.val + 5, 0, Math.PI * 2);
          ctx.stroke();

          // Domain Hub Title Label
          ctx.font = n.type === 'core' ? 'bold 13px "JetBrains Mono", Outfit, sans-serif' : 'bold 11px "JetBrains Mono", Outfit, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillStyle = isMatch ? '#ffd700' : (isSelected ? '#00f0ff' : '#ffffff');
          ctx.shadowColor = '#000000';
          ctx.shadowBlur = 6;
          ctx.fillText(n.name, n.x, n.y + n.val + 15);
          ctx.shadowBlur = 0;
        }

        // C. Subfolder Nodes: Dark Glass HUD Backdrop Pills [blog posts], [music], etc.
        else if (n.type === 'subfolder' || n.isSub) {
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.radius || 5.5, 0, Math.PI * 2);
          ctx.fillStyle = n.color || '#00f0ff';
          ctx.shadowColor = n.color || '#00f0ff';
          ctx.shadowBlur = isHover || isSelected ? 12 : 5;
          ctx.fill();
          ctx.shadowBlur = 0;

          // Only render HUD Backdrop Pill if collision solver permitted it
          const showPill = labelVisibilityMap.get(n.id);
          if (showPill) {
            const pillText = n.name.startsWith('[') ? n.name : `[${n.name}]`;
            ctx.font = 'bold 10px "JetBrains Mono", monospace';
            const metrics = ctx.measureText(pillText);
            const padX = 6;
            const padY = 3;
            const pillW = metrics.width + padX * 2;
            const pillH = 16;
            const pillX = n.x - pillW / 2;
            const pillY = n.y + (n.radius || 5.5) + 3;

            ctx.fillStyle = 'rgba(5, 6, 8, 0.88)';
            ctx.strokeStyle = isMatch ? '#ffd700' : (isSelected ? '#00f0ff' : (n.color ? `${n.color}88` : 'rgba(0, 240, 255, 0.5)'));
            ctx.lineWidth = isMatch || isSelected || isHover ? 1.5 : 1.0;
            ctx.beginPath();
            if (typeof ctx.roundRect === 'function') {
              ctx.roundRect(pillX, pillY, pillW, pillH, 4);
            } else {
              ctx.rect(pillX, pillY, pillW, pillH);
            }
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = isMatch ? '#ffd700' : (isSelected || isHover ? '#00f0ff' : '#ffffff');
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.shadowColor = '#000000';
            ctx.shadowBlur = 4;
            ctx.fillText(pillText, n.x, pillY + pillH / 2);
            ctx.shadowBlur = 0;
            ctx.textBaseline = 'alphabetic';
          }
        }

        // D. File Leaf Nodes: Crisp Dots with JetBrains Mono File Labels
        else {
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.radius || 3.5, 0, Math.PI * 2);
          ctx.fillStyle = isMatch ? '#ffd700' : (isSelected ? '#ffffff' : '#38bdf8');
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = isMatch || isSelected || isHover ? 10 : 3;
          ctx.fill();
          ctx.shadowBlur = 0;

          const isLabelVisible = labelVisibilityMap.get(n.id);
          const shouldDrawLabel = isLabelVisible && (isHover || isSelected || isMatch || this.scale >= 0.95);
          if (shouldDrawLabel) {
            ctx.font = '9px "JetBrains Mono", monospace';
            ctx.fillStyle = isMatch ? '#ffd700' : (isSelected || isHover ? '#00f0ff' : '#cbd5e1');
            ctx.textAlign = 'center';
            ctx.shadowColor = '#000000';
            ctx.shadowBlur = 4;
            ctx.fillText(n.name, n.x, n.y + (n.radius || 3.5) + 11);
            ctx.shadowBlur = 0;
          }
        }

        ctx.restore();
      });

      ctx.restore();
    }
  }

  return {
    init: function (container) {
      if (!container) return null;
      return new CelestialVectorBrainVisualizer(container);
    }
  };
});
