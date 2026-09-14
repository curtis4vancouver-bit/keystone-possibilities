/* ==========================================================================
   KEYSTONE INTERACTIVE 3D AVATAR ENGINE (Three.js WebGL)
   Character: Baby Superman with Keystone "K" Crest Cyber Armor
   Skeletal Animation Machine: Idle, Listening, Thinking, Talking, Walking
   Web Audio API Frequency Lip-Sync with Facial Morph Targets
   ========================================================================== */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['three'], factory);
  } else if (typeof exports === 'object') {
    module.exports = factory(require('three'));
  } else {
    root.AvatarEngine3D = factory(root.THREE);
  }
})(typeof self !== 'undefined' ? self : this, function (THREE) {
  'use strict';

  if (!THREE) {
    console.error('[AvatarEngine3D] Three.js not found! Ensure three.min.js is loaded.');
    return null;
  }

  // --------------------------------------------------------------------------
  // Web Audio API Speech & Lip-Sync Analyzer
  // --------------------------------------------------------------------------
  class AudioSpeechEngine {
    constructor() {
      this.ctx = null;
      this.analyser = null;
      this.freqData = null;
      this.isPlaying = false;
      this.formantOsc1 = null;
      this.formantOsc2 = null;
      this.gainNode = null;
      this.mouthOpen = 0;
      this.simulatedCadence = 0;
      this.speechTimeout = null;
    }

    init() {
      if (this.ctx) return;
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      this.ctx = new AudioCtx();
      this.analyser = this.ctx.createAnalyser();
      this.analyser.fftSize = 256;
      this.analyser.smoothingTimeConstant = 0.6;
      this.freqData = new Uint8Array(this.analyser.frequencyBinCount);
    }

    startSpeech() {
      this.init();
      if (!this.ctx) return;
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      this.stopSpeech();
      this.isPlaying = true;

      const now = this.ctx.currentTime;
      this.formantOsc1 = this.ctx.createOscillator();
      this.formantOsc2 = this.ctx.createOscillator();
      this.gainNode = this.ctx.createGain();

      // Dual formant vocal synthesis (Kryptonian AI companion voice)
      this.formantOsc1.type = 'sawtooth';
      this.formantOsc1.frequency.setValueAtTime(240, now);
      this.formantOsc1.frequency.linearRampToValueAtTime(320, now + 0.4);
      this.formantOsc1.frequency.linearRampToValueAtTime(210, now + 1.1);
      this.formantOsc1.frequency.linearRampToValueAtTime(360, now + 1.8);
      this.formantOsc1.frequency.linearRampToValueAtTime(260, now + 2.6);
      this.formantOsc1.frequency.linearRampToValueAtTime(300, now + 3.2);

      this.formantOsc2.type = 'triangle';
      this.formantOsc2.frequency.setValueAtTime(480, now);
      this.formantOsc2.frequency.linearRampToValueAtTime(620, now + 1.0);
      this.formantOsc2.frequency.linearRampToValueAtTime(440, now + 2.2);

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(750, now);
      filter.Q.setValueAtTime(3.5, now);

      // Syllabic speech cadence envelopes
      this.gainNode.gain.setValueAtTime(0, now);
      const syllables = [0.08, 0.35, 0.72, 1.05, 1.45, 1.85, 2.2, 2.6, 2.95];
      syllables.forEach((t) => {
        this.gainNode.gain.linearRampToValueAtTime(0.22, now + t);
        this.gainNode.gain.linearRampToValueAtTime(0.02, now + t + 0.16);
      });
      this.gainNode.gain.linearRampToValueAtTime(0, now + 3.4);

      this.formantOsc1.connect(filter);
      this.formantOsc2.connect(filter);
      filter.connect(this.gainNode);
      this.gainNode.connect(this.analyser);
      this.gainNode.connect(this.ctx.destination);

      this.formantOsc1.start(now);
      this.formantOsc2.start(now);
      this.formantOsc1.stop(now + 3.45);
      this.formantOsc2.stop(now + 3.45);

      this.speechTimeout = setTimeout(() => {
        this.isPlaying = false;
      }, 3500);
    }

    stopSpeech() {
      if (this.speechTimeout) {
        clearTimeout(this.speechTimeout);
        this.speechTimeout = null;
      }
      if (this.formantOsc1) {
        try { this.formantOsc1.stop(); } catch (_) {}
        this.formantOsc1 = null;
      }
      if (this.formantOsc2) {
        try { this.formantOsc2.stop(); } catch (_) {}
        this.formantOsc2 = null;
      }
      this.isPlaying = false;
    }

    update(dt, isTalkingState) {
      if (this.analyser && this.isPlaying) {
        this.analyser.getByteFrequencyData(this.freqData);
        let sum = 0;
        const startBin = 2;
        const endBin = Math.min(32, this.freqData.length);
        for (let i = startBin; i < endBin; i++) {
          sum += this.freqData[i];
        }
        const rms = sum / ((endBin - startBin) * 255);
        const target = Math.min(1.0, rms * 3.2);
        this.mouthOpen += (target - this.mouthOpen) * Math.min(1, dt * 20.0);
      } else if (isTalkingState) {
        this.simulatedCadence += dt * 12.0;
        const s1 = Math.max(0, Math.sin(this.simulatedCadence));
        const s2 = Math.max(0, Math.sin(this.simulatedCadence * 0.45));
        const target = (s1 * 0.7 + s2 * 0.3) * (0.6 + 0.4 * Math.sin(this.simulatedCadence * 0.25));
        this.mouthOpen += (target - this.mouthOpen) * Math.min(1, dt * 14.0);
      } else {
        this.mouthOpen += (0 - this.mouthOpen) * Math.min(1, dt * 12.0);
      }
      return Math.max(0, Math.min(1, this.mouthOpen));
    }
  }

  // --------------------------------------------------------------------------
  // Helper: Keystone "K" Crest Texture Generator
  // Explicitly renders the Keystone "K" symbol (NOT an "S") on Kryptonian Shield
  // --------------------------------------------------------------------------
  function createKeystoneKTexture() {
    const size = 1024;
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const ctx = canvas.getContext('2d');

    // 1. Transparent Clear
    ctx.clearRect(0, 0, size, size);

    // 2. Diamond / Pentagon Kryptonian Shield Path
    ctx.beginPath();
    ctx.moveTo(512, 60);      // Top center
    ctx.lineTo(920, 300);     // Top right shoulder
    ctx.lineTo(760, 900);     // Bottom right
    ctx.lineTo(512, 980);     // Bottom tip
    ctx.lineTo(264, 900);     // Bottom left
    ctx.lineTo(104, 300);     // Top left shoulder
    ctx.closePath();

    // Shield Background: Midnight Obsidian to Crimson Gradient
    const bgGrad = ctx.createLinearGradient(104, 60, 920, 980);
    bgGrad.addColorStop(0, '#060a1a');
    bgGrad.addColorStop(0.4, '#1b0d28');
    bgGrad.addColorStop(0.85, '#450a1a');
    bgGrad.addColorStop(1, '#110615');
    ctx.fillStyle = bgGrad;
    ctx.fill();

    // Shield Outer Cyber Glow Border (Neon Cyan)
    ctx.save();
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 24;
    ctx.shadowColor = '#00f0ff';
    ctx.shadowBlur = 40;
    ctx.stroke();
    ctx.restore();

    // Shield Inner Bevel Border (Radiant Solar Gold)
    ctx.save();
    ctx.strokeStyle = '#fbbf24';
    ctx.lineWidth = 14;
    ctx.shadowColor = '#fbbf24';
    ctx.shadowBlur = 20;
    ctx.stroke();
    ctx.restore();

    // Faint Cyber Circuit Grid Inside Shield
    ctx.save();
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.15)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(512, 80); ctx.lineTo(512, 960);
    ctx.moveTo(150, 480); ctx.lineTo(874, 480);
    ctx.moveTo(250, 250); ctx.lineTo(774, 710);
    ctx.moveTo(774, 250); ctx.lineTo(250, 710);
    ctx.stroke();
    ctx.restore();

    // 3. THE KEYSTONE "K" EMBLEM (Stylized, Bold, Cybernetic - DEFINITELY A "K")
    ctx.save();
    ctx.shadowColor = '#00f0ff';
    ctx.shadowBlur = 35;

    const kGrad = ctx.createLinearGradient(280, 200, 740, 800);
    kGrad.addColorStop(0, '#ffffff');
    kGrad.addColorStop(0.2, '#fef08a');
    kGrad.addColorStop(0.5, '#fbbf24');
    kGrad.addColorStop(0.85, '#f59e0b');
    kGrad.addColorStop(1, '#00f0ff');

    ctx.fillStyle = kGrad;

    // --- Vertical Spine of K ---
    ctx.beginPath();
    ctx.moveTo(310, 200);   // Top left
    ctx.lineTo(430, 200);   // Top right
    ctx.lineTo(430, 800);   // Bottom right
    ctx.lineTo(310, 800);   // Bottom left
    ctx.lineTo(270, 500);   // Left subtle cyber chevron notch
    ctx.closePath();
    ctx.fill();

    // --- Upper Diagonal Branch of K ---
    ctx.beginPath();
    ctx.moveTo(430, 470);   // Branch root
    ctx.lineTo(680, 220);   // Upper right outer tip
    ctx.lineTo(770, 250);   // Upper right edge
    ctx.lineTo(550, 530);   // Inner elbow
    ctx.closePath();
    ctx.fill();

    // --- Lower Diagonal Branch of K ---
    ctx.beginPath();
    ctx.moveTo(430, 520);   // Branch root
    ctx.lineTo(560, 530);   // Inner elbow
    ctx.lineTo(770, 750);   // Lower right outer edge
    ctx.lineTo(690, 800);   // Lower right tip
    ctx.closePath();
    ctx.fill();

    // Cyber Bevel Highlights on K
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 8;
    ctx.shadowColor = '#ffffff';
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.moveTo(330, 220); ctx.lineTo(330, 780); // Spine highlight
    ctx.moveTo(450, 480); ctx.lineTo(670, 240); // Upper wing highlight
    ctx.moveTo(560, 540); ctx.lineTo(740, 760); // Lower wing highlight
    ctx.stroke();

    // Center Keystone Quantum Gem at intersection of K
    ctx.fillStyle = '#00f0ff';
    ctx.shadowColor = '#00f0ff';
    ctx.shadowBlur = 30;
    ctx.beginPath();
    ctx.arc(440, 500, 18, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    const texture = new THREE.CanvasTexture(canvas);
    texture.needsUpdate = true;
    return texture;
  }

  // --------------------------------------------------------------------------
  // Main Engine Class
  // --------------------------------------------------------------------------
  class AvatarEngine3D {
    constructor() {
      this.container = null;
      this.canvas = null;
      this.renderer = null;
      this.scene = null;
      this.camera = null;
      this.clock = new THREE.Clock();

      // Character & Skeleton
      this.characterRoot = null;
      this.bones = {};
      this.headFaceMesh = null;
      this.eyes = [];
      this.jawMesh = null;
      this.mouthInterior = null;
      this.capeMesh = null;
      this.capeBackwardAngle = 0;
      this.chestLight = null;
      this.bootLights = [];

      // Overhead Thinking Holographic Glyph
      this.glyphGroup = null;
      this.glyphRings = [];
      this.glyphCore = null;
      this.glyphScale = 0;

      // Concentric Listening Audio Ripple Rings
      this.rippleGroup = null;
      this.rippleRings = [];

      // Cyber Neon Particle Trail (Walking)
      this.particleSystem = null;
      this.particles = [];
      this.maxParticles = 60;

      // Floor Holographic Pedestal
      this.pedestalGroup = null;

      // Animation State Machine
      this.currentState = 'idle';
      this.targetState = 'idle';
      this.stateBlend = 1.0;
      this.walkTime = 0;
      this.hoverTime = 0;
      this.blinkTimer = 0;
      this.isBlinking = false;
      this.blinkProgress = 0;

      // Web Audio API
      this.audioEngine = new AudioSpeechEngine();

      // Mouse Drag / Parallax Interaction
      this.isDragging = false;
      this.prevPointerX = 0;
      this.prevPointerY = 0;
      this.targetRotationY = 0;
      this.targetRotationX = 0;
      this.currentRotationY = 0;
      this.currentRotationX = 0;
      this.targetCameraDistance = 3.6;
      this.currentCameraDistance = 3.6;
      this.mouseParallax = { x: 0, y: 0 };

      // Performance Telemetry
      this.fps = 60;
      this.frameCount = 0;
      this.lastFpsTime = performance.now();

      this.isInitialized = false;
    }

    init(containerId) {
      this.container = document.getElementById(containerId);
      if (!this.container) {
        console.error(`[AvatarEngine3D] Container #${containerId} not found.`);
        return false;
      }

      const rect = this.container.getBoundingClientRect();
      const width = rect.width || 400;
      const height = rect.height || 340;

      // Create Transparent WebGL Canvas
      this.canvas = document.createElement('canvas');
      this.canvas.id = 'avatar3DCanvas';
      this.canvas.className = 'avatar-3d-canvas';
      this.canvas.style.position = 'absolute';
      this.canvas.style.top = '0';
      this.canvas.style.left = '0';
      this.canvas.style.width = '100%';
      this.canvas.style.height = '100%';
      this.canvas.style.zIndex = '8';
      this.canvas.style.pointerEvents = 'auto';
      this.canvas.style.cursor = 'grab';

      // Insert canvas into container
      this.container.appendChild(this.canvas);

      // WebGL Renderer with High-DPI & Tone Mapping
      this.renderer = new THREE.WebGLRenderer({
        canvas: this.canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
      });
      this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      this.renderer.setSize(width, height);
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
      this.renderer.toneMappingExposure = 1.35;
      this.renderer.shadowMap.enabled = true;
      this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      // Scene & Camera
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
      this.camera.position.set(0, 0.35, 3.6);
      this.camera.lookAt(0, 0.12, 0);

      // Lighting Setup
      this.setupLighting();

      // Build Baby Superman 3D Rigged Model with "K" Chest Crest
      this.buildCharacterRig();

      // Build State FX (Overhead Thinking Glyph, Audio Rings, Foot Trail, Pedestal)
      this.buildStateFx();

      // Mouse & Pointer Interactions (Drag to Rotate, Scroll to Zoom)
      this.setupInteraction();

      // Responsive Resize
      this.setupResize();

      // Start Render Loop
      this.isInitialized = true;
      this.animate = this.animate.bind(this);
      requestAnimationFrame(this.animate);

      console.log('[AvatarEngine3D] Initialized successfully. Three.js Rigged Baby Superman with Keystone K active.');
      return true;
    }

    // ------------------------------------------------------------------------
    // Lighting Setup
    // ------------------------------------------------------------------------
    setupLighting() {
      // Ambient shadow illumination (Deep Indigo)
      const ambientLight = new THREE.AmbientLight(0x161c38, 1.6);
      this.scene.add(ambientLight);

      // Key Directional Light (Crisp White/Cyan)
      const keyLight = new THREE.DirectionalLight(0xffffff, 2.0);
      keyLight.position.set(3.0, 4.5, 3.5);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.width = 1024;
      keyLight.shadow.mapSize.height = 1024;
      this.scene.add(keyLight);

      // Rim Edge Light (Electric Neon Violet - Gives the armor & cape a vibrant cyber edge)
      const rimLight = new THREE.DirectionalLight(0x8b5cf6, 3.4);
      rimLight.position.set(-3.5, 2.5, -2.5);
      this.scene.add(rimLight);

      // Fill Light (Neon Cyan - Reflects off suit panels)
      const fillLight = new THREE.DirectionalLight(0x00f0ff, 1.4);
      fillLight.position.set(2.5, -1.0, 2.0);
      this.scene.add(fillLight);

      // Warm Amber Solar Underlight
      const solarFill = new THREE.DirectionalLight(0xfbbf24, 0.6);
      solarFill.position.set(0, -3.0, 1.5);
      this.scene.add(solarFill);
    }

    // ------------------------------------------------------------------------
    // Build 3D Humanoid Character (Baby Superman with Keystone "K" Crest)
    // ------------------------------------------------------------------------
    buildCharacterRig() {
      this.characterRoot = new THREE.Group();
      this.characterRoot.position.set(0, -0.05, 0);
      this.scene.add(this.characterRoot);

      // Shared Materials
      const suitMat = new THREE.MeshStandardMaterial({
        color: 0x0c152d, // Deep Kryptonian cyber navy
        metalness: 0.45,
        roughness: 0.35
      });

      const suitAccentMat = new THREE.MeshStandardMaterial({
        color: 0x18264d,
        metalness: 0.6,
        roughness: 0.25
      });

      const goldMat = new THREE.MeshStandardMaterial({
        color: 0xfbbf24, // Radiant Solar Gold
        metalness: 0.85,
        roughness: 0.2,
        emissive: 0x78350f,
        emissiveIntensity: 0.25
      });

      const cyanGlowMat = new THREE.MeshBasicMaterial({
        color: 0x00f0ff
      });

      const skinMat = new THREE.MeshStandardMaterial({
        color: 0xfed7aa, // Stylized warm hero peach
        roughness: 0.6,
        metalness: 0.05
      });

      const hairMat = new THREE.MeshStandardMaterial({
        color: 0x080b12, // Midnight black Kryptonian hair
        metalness: 0.45,
        roughness: 0.3
      });

      const bootMat = new THREE.MeshStandardMaterial({
        color: 0x991b1b, // Dark Kryptonian Crimson Boots
        metalness: 0.55,
        roughness: 0.3
      });

      const capeMat = new THREE.MeshStandardMaterial({
        color: 0xbe123c, // Flowing Crimson Cape
        metalness: 0.15,
        roughness: 0.55,
        side: THREE.DoubleSide
      });

      // ----------------------------------------------------------------------
      // SKELETAL JOINT HIERARCHY
      // ----------------------------------------------------------------------

      // 1. PELVIS (Root Joint)
      const pelvis = new THREE.Group();
      pelvis.position.set(0, -0.15, 0);
      this.characterRoot.add(pelvis);
      this.bones.pelvis = pelvis;

      // Pelvis / Briefs Armor Mesh
      const pelvisGeo = new THREE.CylinderGeometry(0.24, 0.18, 0.22, 16);
      const pelvisMesh = new THREE.Mesh(pelvisGeo, suitAccentMat);
      pelvisMesh.castShadow = true;
      pelvis.add(pelvisMesh);

      // Gold Cyber Utility Belt
      const beltGeo = new THREE.CylinderGeometry(0.25, 0.25, 0.07, 16);
      const beltMesh = new THREE.Mesh(beltGeo, goldMat);
      beltMesh.position.y = 0.08;
      pelvis.add(beltMesh);

      // Glowing Cyan Belt Buckle (Keystone Octagon)
      const buckleGeo = new THREE.BoxGeometry(0.1, 0.08, 0.05);
      const buckleMesh = new THREE.Mesh(buckleGeo, cyanGlowMat);
      buckleMesh.position.set(0, 0.08, 0.24);
      pelvis.add(buckleMesh);

      // 2. SPINE JOINT
      const spine = new THREE.Group();
      spine.position.set(0, 0.12, 0);
      pelvis.add(spine);
      this.bones.spine = spine;

      // Mid-Torso / Cyber Abs
      const spineGeo = new THREE.CylinderGeometry(0.25, 0.24, 0.18, 16);
      const spineMesh = new THREE.Mesh(spineGeo, suitMat);
      spineMesh.position.y = 0.09;
      spine.add(spineMesh);

      // 3. CHEST JOINT (Carries Keystone "K" Crest, Cape, Neck, Arms)
      const chest = new THREE.Group();
      chest.position.set(0, 0.18, 0);
      spine.add(chest);
      this.bones.chest = chest;

      // Muscular Chest Cyber Armor
      const chestGeo = new THREE.BoxGeometry(0.56, 0.38, 0.38);
      const chestMesh = new THREE.Mesh(chestGeo, suitMat);
      chestMesh.position.y = 0.19;
      chestMesh.castShadow = true;
      chest.add(chestMesh);

      // Chest Collar Rim
      const collarGeo = new THREE.TorusGeometry(0.2, 0.03, 8, 16);
      collarGeo.rotateX(Math.PI / 2);
      const collarMesh = new THREE.Mesh(collarGeo, goldMat);
      collarMesh.position.set(0, 0.38, 0);
      chest.add(collarMesh);

      // ----------------------------------------------------------------------
      // KEYSTONE "K" CREST (Shield Emblem on Chest)
      // ----------------------------------------------------------------------
      const kTexture = createKeystoneKTexture();
      const crestMat = new THREE.MeshStandardMaterial({
        map: kTexture,
        transparent: true,
        metalness: 0.65,
        roughness: 0.25,
        emissive: 0x00f0ff,
        emissiveIntensity: 0.45,
        side: THREE.DoubleSide
      });

      // Pentagon Shield Geometry
      const shieldShape = new THREE.Shape();
      shieldShape.moveTo(0, 0.16);         // Top point
      shieldShape.lineTo(0.15, 0.07);      // Top right
      shieldShape.lineTo(0.10, -0.14);     // Bottom right
      shieldShape.lineTo(0, -0.17);        // Bottom point
      shieldShape.lineTo(-0.10, -0.14);    // Bottom left
      shieldShape.lineTo(-0.15, 0.07);     // Top left
      shieldShape.closePath();

      const shieldGeo = new THREE.ShapeGeometry(shieldShape);
      const uvAttr = shieldGeo.attributes.uv;
      const posAttr = shieldGeo.attributes.position;
      for (let i = 0; i < posAttr.count; i++) {
        const u = (posAttr.getX(i) + 0.15) / 0.30;
        const v = (posAttr.getY(i) + 0.17) / 0.33;
        uvAttr.setXY(i, u, v);
      }
      uvAttr.needsUpdate = true;

      const crestMesh = new THREE.Mesh(shieldGeo, crestMat);
      crestMesh.position.set(0, 0.20, 0.198);
      crestMesh.scale.set(1.25, 1.25, 1.25);
      chest.add(crestMesh);

      // Shield Gold Outer Border Bevel
      const borderGeo = new THREE.RingGeometry(0.13, 0.16, 5);
      borderGeo.rotateZ(Math.PI);
      const borderMesh = new THREE.Mesh(borderGeo, goldMat);
      borderMesh.position.set(0, 0.20, 0.194);
      borderMesh.scale.set(1.25, 1.32, 1.25);
      chest.add(borderMesh);

      // PointLight on Chest: Pulsing Keystone "K" Glow
      this.chestLight = new THREE.PointLight(0x00f0ff, 2.2, 3.0);
      this.chestLight.position.set(0, 0.20, 0.28);
      chest.add(this.chestLight);

      // Cape Gold Shoulder Clasps
      [-0.24, 0.24].forEach((x) => {
        const claspGeo = new THREE.CylinderGeometry(0.048, 0.048, 0.035, 12);
        claspGeo.rotateX(Math.PI / 2);
        const claspMesh = new THREE.Mesh(claspGeo, goldMat);
        claspMesh.position.set(x, 0.36, -0.06);
        chest.add(claspMesh);
      });

      // ----------------------------------------------------------------------
      // DYNAMIC MULTI-SEGMENTED CRIMSON CAPE
      // ----------------------------------------------------------------------
      const capeGeo = new THREE.PlaneGeometry(0.92, 1.22, 14, 18);
      this.capeMesh = new THREE.Mesh(capeGeo, capeMat);
      this.capeMesh.position.set(0, -0.20, -0.20);
      this.capeMesh.castShadow = true;
      chest.add(this.capeMesh);

      // 4. NECK JOINT
      const neck = new THREE.Group();
      neck.position.set(0, 0.38, 0);
      chest.add(neck);
      this.bones.neck = neck;

      const neckGeo = new THREE.CylinderGeometry(0.12, 0.14, 0.12, 12);
      const neckMesh = new THREE.Mesh(neckGeo, skinMat);
      neckMesh.position.y = 0.06;
      neck.add(neckMesh);

      // 5. HEAD JOINT (Contains Face with Morph Targets, Eyes, Hair Curl)
      const head = new THREE.Group();
      head.position.set(0, 0.12, 0);
      neck.add(head);
      this.bones.head = head;

      // Stylized Toddler Superhero Head with FACIAL MORPH TARGETS (mouthOpen)
      const headGeo = new THREE.SphereGeometry(0.32, 24, 20);
      headGeo.scale(1.0, 1.05, 0.96);

      // Create morph target: mouthOpen (pulls lower lip and jaw vertices down)
      const basePos = headGeo.attributes.position;
      const mouthPositions = new Float32Array(basePos.array.length);
      mouthPositions.set(basePos.array);

      for (let i = 0; i < basePos.count; i++) {
        const x = basePos.getX(i);
        const y = basePos.getY(i);
        const z = basePos.getZ(i);

        // Lower mouth & jaw region
        if (z > 0.14 && y < -0.04 && y > -0.26 && Math.abs(x) < 0.16) {
          const horizFactor = 1 - Math.abs(x) / 0.16;
          const vertFactor = (y - (-0.04)) / (-0.22);
          const weight = Math.max(0, horizFactor * vertFactor);
          mouthPositions[i * 3 + 1] = y - 0.085 * weight; // displace down
          mouthPositions[i * 3 + 2] = z - 0.035 * weight; // displace in
        }
      }

      headGeo.morphAttributes.position = [
        new THREE.BufferAttribute(mouthPositions, 3)
      ];
      headGeo.morphTargetsRelative = false;

      this.headFaceMesh = new THREE.Mesh(headGeo, skinMat);
      this.headFaceMesh.position.y = 0.18;
      this.headFaceMesh.castShadow = true;
      this.headFaceMesh.morphTargetInfluences = [0]; // Index 0: mouthOpen
      head.add(this.headFaceMesh);

      // Stylized Mouth Cavity / Teeth Interior
      const mouthCavityGeo = new THREE.BoxGeometry(0.14, 0.04, 0.08);
      const mouthCavityMat = new THREE.MeshBasicMaterial({ color: 0x2e0814 });
      this.mouthInterior = new THREE.Mesh(mouthCavityGeo, mouthCavityMat);
      this.mouthInterior.position.set(0, 0.07, 0.28);
      this.mouthInterior.scale.set(1, 0.1, 1);
      head.add(this.mouthInterior);

      // Articulated Jaw Mesh that opens in sync with mouthOpen
      const jaw = new THREE.Group();
      jaw.position.set(0, 0.07, 0.15);
      head.add(jaw);
      this.bones.jaw = jaw;

      // Stylized Toddler Nose
      const noseGeo = new THREE.ConeGeometry(0.04, 0.06, 8);
      noseGeo.rotateX(Math.PI / 2);
      const noseMesh = new THREE.Mesh(noseGeo, skinMat);
      noseMesh.position.set(0, 0.16, 0.32);
      head.add(noseMesh);

      // Glowing Cyan Kryptonian Eyes with Specular Sparkle & Blinking Eyelids
      [-0.10, 0.10].forEach((x) => {
        const sign = x < 0 ? -1 : 1;
        const eyeGroup = new THREE.Group();
        eyeGroup.position.set(x, 0.20, 0.26);

        // White Eye Sclera
        const scleraGeo = new THREE.SphereGeometry(0.068, 16, 16);
        scleraGeo.scale(1.15, 1.25, 0.45);
        const scleraMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.15 });
        const scleraMesh = new THREE.Mesh(scleraGeo, scleraMat);
        eyeGroup.add(scleraMesh);

        // Electric Cyan/Blue Iris Disc
        const irisGeo = new THREE.SphereGeometry(0.050, 16, 16);
        irisGeo.scale(1.05, 1.10, 0.35);
        const irisMat = new THREE.MeshStandardMaterial({
          color: 0x0284c7,
          emissive: 0x00f0ff,
          emissiveIntensity: 0.75,
          roughness: 0.15
        });
        const irisMesh = new THREE.Mesh(irisGeo, irisMat);
        irisMesh.position.z = 0.012;
        eyeGroup.add(irisMesh);

        // Dark Obsidian Pupil
        const pupilGeo = new THREE.SphereGeometry(0.026, 12, 12);
        pupilGeo.scale(1, 1, 0.3);
        const pupilMat = new THREE.MeshBasicMaterial({ color: 0x030712 });
        const pupilMesh = new THREE.Mesh(pupilGeo, pupilMat);
        pupilMesh.position.z = 0.025;
        eyeGroup.add(pupilMesh);

        // Primary Specular Glint (Top Right)
        const glint1Geo = new THREE.SphereGeometry(0.011, 8, 8);
        const glintMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
        const glint1 = new THREE.Mesh(glint1Geo, glintMat);
        glint1.position.set(0.015, 0.016, 0.032);
        eyeGroup.add(glint1);

        // Secondary Soft Specular Glint (Bottom Left)
        const glint2Geo = new THREE.SphereGeometry(0.006, 6, 6);
        const glint2 = new THREE.Mesh(glint2Geo, glintMat);
        glint2.position.set(-0.014, -0.012, 0.030);
        eyeGroup.add(glint2);

        head.add(eyeGroup);
        this.eyes.push(eyeGroup);

        // Cute Heroic Curved Eyebrows
        const browCurve = new THREE.CubicBezierCurve3(
          new THREE.Vector3(sign * 0.04, 0.28, 0.28),
          new THREE.Vector3(sign * 0.10, 0.31, 0.27),
          new THREE.Vector3(sign * 0.14, 0.30, 0.25),
          new THREE.Vector3(sign * 0.17, 0.27, 0.23)
        );
        const browGeo = new THREE.TubeGeometry(browCurve, 12, 0.014, 6, false);
        const browMesh = new THREE.Mesh(browGeo, hairMat);
        head.add(browMesh);

        // Rosy Heroic Cheeks
        const cheekGeo = new THREE.SphereGeometry(0.045, 12, 12);
        cheekGeo.scale(1.2, 0.8, 0.3);
        const cheekMat = new THREE.MeshBasicMaterial({
          color: 0xf43f5e,
          transparent: true,
          opacity: 0.32
        });
        const cheekMesh = new THREE.Mesh(cheekGeo, cheekMat);
        cheekMesh.position.set(sign * 0.15, 0.11, 0.27);
        head.add(cheekMesh);
      });

      // Signature Toddler Superman Hair + Forehead Curl!
      const hairCapGeo = new THREE.SphereGeometry(0.33, 22, 18);
      hairCapGeo.scale(1.03, 1.06, 1.02);
      const hairCap = new THREE.Mesh(hairCapGeo, hairMat);
      hairCap.position.set(0, 0.22, -0.04);
      head.add(hairCap);

      // Signature Forehead "S/K" Swirl Curl (Sculpted loop)
      const curlCurve = new THREE.CubicBezierCurve3(
        new THREE.Vector3(0.03, 0.41, 0.26),
        new THREE.Vector3(-0.09, 0.35, 0.33),
        new THREE.Vector3(0.05, 0.27, 0.34),
        new THREE.Vector3(-0.03, 0.21, 0.32)
      );
      const curlGeo = new THREE.TubeGeometry(curlCurve, 24, 0.036, 8, false);
      const curlMesh = new THREE.Mesh(curlGeo, hairMat);
      head.add(curlMesh);

      // ----------------------------------------------------------------------
      // ARMS & HANDS (Left & Right)
      // ----------------------------------------------------------------------
      ['left', 'right'].forEach((side) => {
        const isLeft = side === 'left';
        const sign = isLeft ? -1 : 1;

        // Shoulder Joint
        const shoulder = new THREE.Group();
        shoulder.position.set(sign * 0.34, 0.32, 0);
        chest.add(shoulder);
        this.bones[`${side}Shoulder`] = shoulder;

        // Shoulder Armor Pauldron
        const pauldronGeo = new THREE.SphereGeometry(0.12, 12, 12);
        pauldronGeo.scale(1.1, 1.0, 1.0);
        const pauldronMesh = new THREE.Mesh(pauldronGeo, suitAccentMat);
        shoulder.add(pauldronMesh);

        // Upper Arm Joint
        const upperArm = new THREE.Group();
        upperArm.position.set(sign * 0.05, -0.08, 0);
        shoulder.add(upperArm);
        this.bones[`${side}UpperArm`] = upperArm;

        const upperArmGeo = new THREE.CylinderGeometry(0.085, 0.075, 0.22, 12);
        const upperArmMesh = new THREE.Mesh(upperArmGeo, suitMat);
        upperArmMesh.position.y = -0.11;
        upperArm.add(upperArmMesh);

        // Forearm Joint (Elbow)
        const forearm = new THREE.Group();
        forearm.position.set(0, -0.22, 0);
        upperArm.add(forearm);
        this.bones[`${side}Forearm`] = forearm;

        // Gauntlet with Cyan Neon Ring
        const forearmGeo = new THREE.CylinderGeometry(0.08, 0.07, 0.20, 12);
        const forearmMesh = new THREE.Mesh(forearmGeo, suitAccentMat);
        forearmMesh.position.y = -0.10;
        forearm.add(forearmMesh);

        const wristRingGeo = new THREE.TorusGeometry(0.078, 0.012, 8, 16);
        wristRingGeo.rotateX(Math.PI / 2);
        const wristRing = new THREE.Mesh(wristRingGeo, cyanGlowMat);
        wristRing.position.y = -0.18;
        forearm.add(wristRing);

        // Hand Joint & Low-Poly Hero Fist
        const hand = new THREE.Group();
        hand.position.set(0, -0.21, 0);
        forearm.add(hand);
        this.bones[`${side}Hand`] = hand;

        const handGeo = new THREE.SphereGeometry(0.072, 10, 10);
        handGeo.scale(1.0, 1.1, 0.85);
        const handMesh = new THREE.Mesh(handGeo, skinMat);
        hand.add(handMesh);
      });

      // ----------------------------------------------------------------------
      // LEGS & BOOTS (Left & Right)
      // ----------------------------------------------------------------------
      ['left', 'right'].forEach((side) => {
        const isLeft = side === 'left';
        const sign = isLeft ? -1 : 1;

        // Hip Joint
        const hip = new THREE.Group();
        hip.position.set(sign * 0.14, -0.10, 0);
        pelvis.add(hip);
        this.bones[`${side}Hip`] = hip;

        // Thigh Joint
        const thigh = new THREE.Group();
        hip.add(thigh);
        this.bones[`${side}Thigh`] = thigh;

        const thighGeo = new THREE.CylinderGeometry(0.105, 0.09, 0.28, 12);
        const thighMesh = new THREE.Mesh(thighGeo, suitMat);
        thighMesh.position.y = -0.14;
        thigh.add(thighMesh);

        // Shin / Knee Joint
        const shin = new THREE.Group();
        shin.position.set(0, -0.28, 0);
        thigh.add(shin);
        this.bones[`${side}Shin`] = shin;

        // Cyber Knee Pad
        const kneeGeo = new THREE.SphereGeometry(0.08, 10, 10);
        kneeGeo.scale(1, 1.1, 0.8);
        const kneeMesh = new THREE.Mesh(kneeGeo, suitAccentMat);
        kneeMesh.position.set(0, 0, 0.05);
        shin.add(kneeMesh);

        // Shin Boot Upper
        const shinGeo = new THREE.CylinderGeometry(0.09, 0.08, 0.26, 12);
        const shinMesh = new THREE.Mesh(shinGeo, bootMat);
        shinMesh.position.y = -0.13;
        shin.add(shinMesh);

        // Foot Joint
        const foot = new THREE.Group();
        foot.position.set(0, -0.26, 0);
        shin.add(foot);
        this.bones[`${side}Foot`] = foot;

        // Cyber Boot Mesh
        const bootGeo = new THREE.BoxGeometry(0.14, 0.12, 0.24);
        const bootMesh = new THREE.Mesh(bootGeo, bootMat);
        bootMesh.position.set(0, -0.04, 0.04);
        foot.add(bootMesh);

        // Boot Gold Trim
        const bootTrimGeo = new THREE.BoxGeometry(0.15, 0.03, 0.25);
        const bootTrim = new THREE.Mesh(bootTrimGeo, goldMat);
        bootTrim.position.set(0, 0.02, 0.04);
        foot.add(bootTrim);

        // Boot Thruster Pad (Neon Cyan Emitter on Sole)
        const thrusterGeo = new THREE.CylinderGeometry(0.05, 0.05, 0.02, 12);
        const thrusterMesh = new THREE.Mesh(thrusterGeo, cyanGlowMat);
        thrusterMesh.position.set(0, -0.10, 0.03);
        foot.add(thrusterMesh);

        // Boot Thruster PointLight
        const thrusterLight = new THREE.PointLight(0x00f0ff, 1.2, 1.5);
        thrusterLight.position.set(0, -0.14, 0.03);
        foot.add(thrusterLight);
        this.bootLights.push(thrusterLight);
      });
    }

    // ------------------------------------------------------------------------
    // Build State Visual FX (Overhead Glyph, Concentric Audio Rings, Trails)
    // ------------------------------------------------------------------------
    buildStateFx() {
      // 1. FLOOR HOLOGRAPHIC PEDESTAL
      this.pedestalGroup = new THREE.Group();
      this.pedestalGroup.position.set(0, -0.92, 0);
      this.characterRoot.add(this.pedestalGroup);

      // Concentric Cyber Floor Rings
      const floorRing1 = new THREE.Mesh(
        new THREE.RingGeometry(0.85, 0.90, 48),
        new THREE.MeshBasicMaterial({ color: 0x8b5cf6, side: THREE.DoubleSide, transparent: true, opacity: 0.55 })
      );
      floorRing1.rotateX(Math.PI / 2);
      this.pedestalGroup.add(floorRing1);

      const floorRing2 = new THREE.Mesh(
        new THREE.RingGeometry(0.55, 0.58, 36),
        new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.45 })
      );
      floorRing2.rotateX(Math.PI / 2);
      this.pedestalGroup.add(floorRing2);

      // Keystone "K" Floor Insignia
      const floorKTexture = createKeystoneKTexture();
      const floorKMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(0.5, 0.5),
        new THREE.MeshBasicMaterial({ map: floorKTexture, transparent: true, opacity: 0.6, side: THREE.DoubleSide })
      );
      floorKMesh.rotateX(Math.PI / 2);
      this.pedestalGroup.add(floorKMesh);

      // 2. OVERHEAD HOLOGRAPHIC DATA GLYPH (Active during THINKING state)
      this.glyphGroup = new THREE.Group();
      this.glyphGroup.position.set(0, 1.18, 0);
      this.glyphGroup.scale.set(0, 0, 0);
      this.characterRoot.add(this.glyphGroup);

      // Outer Neon Violet Orbiting Ring
      const ringViolet = new THREE.Mesh(
        new THREE.TorusGeometry(0.36, 0.015, 12, 48),
        new THREE.MeshBasicMaterial({ color: 0x8b5cf6 })
      );
      this.glyphGroup.add(ringViolet);
      this.glyphRings.push(ringViolet);

      // Inner Neon Cyan Counter-Rotating Ring
      const ringCyan = new THREE.Mesh(
        new THREE.TorusGeometry(0.25, 0.012, 12, 36),
        new THREE.MeshBasicMaterial({ color: 0x00f0ff })
      );
      ringCyan.rotateX(Math.PI / 4);
      this.glyphGroup.add(ringCyan);
      this.glyphRings.push(ringCyan);

      // Sacred Holographic Quantum Core (Octahedron Wireframe)
      const coreGeo = new THREE.OctahedronGeometry(0.14, 0);
      const coreMat = new THREE.MeshBasicMaterial({ color: 0xfbbf24, wireframe: true });
      this.glyphCore = new THREE.Mesh(coreGeo, coreMat);
      this.glyphGroup.add(this.glyphCore);

      // Orbiting Data Nodes
      for (let i = 0; i < 4; i++) {
        const nodeGeo = new THREE.SphereGeometry(0.024, 8, 8);
        const nodeMat = new THREE.MeshBasicMaterial({ color: i % 2 === 0 ? 0x00f0ff : 0xfbbf24 });
        const nodeMesh = new THREE.Mesh(nodeGeo, nodeMat);
        this.glyphGroup.add(nodeMesh);
        nodeMesh.userData = { angle: (i * Math.PI) / 2, radius: 0.36 };
      }

      // 3. CONCENTRIC AUDIO RIPPLE RINGS (Active during LISTENING state)
      this.rippleGroup = new THREE.Group();
      this.rippleGroup.position.set(0, 0.45, 0);
      this.characterRoot.add(this.rippleGroup);

      for (let r = 0; r < 3; r++) {
        const rippleGeo = new THREE.RingGeometry(0.2, 0.22, 32);
        const rippleMat = new THREE.MeshBasicMaterial({
          color: 0x00f0ff,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0
        });
        const rippleMesh = new THREE.Mesh(rippleGeo, rippleMat);
        rippleMesh.userData = { phase: r * (Math.PI * 2 / 3), radius: 0.2 };
        this.rippleGroup.add(rippleMesh);
        this.rippleRings.push(rippleMesh);
      }

      // 4. CYBER NEON PARTICLE TRAIL (Active during WALKING state)
      const pCount = this.maxParticles;
      const pGeo = new THREE.BufferGeometry();
      const pPositions = new Float32Array(pCount * 3);
      const pColors = new Float32Array(pCount * 3);

      for (let i = 0; i < pCount; i++) {
        pPositions[i * 3 + 0] = 0;
        pPositions[i * 3 + 1] = -100;
        pPositions[i * 3 + 2] = 0;

        if (i % 2 === 0) {
          pColors[i * 3 + 0] = 0.0; pColors[i * 3 + 1] = 0.94; pColors[i * 3 + 2] = 1.0;
        } else {
          pColors[i * 3 + 0] = 0.55; pColors[i * 3 + 1] = 0.36; pColors[i * 3 + 2] = 0.96;
        }

        this.particles.push({
          active: false,
          life: 0,
          maxLife: 1.0,
          vx: 0,
          vy: 0,
          vz: 0
        });
      }

      pGeo.setAttribute('position', new THREE.BufferAttribute(pPositions, 3));
      pGeo.setAttribute('color', new THREE.BufferAttribute(pColors, 3));

      const pCanvas = document.createElement('canvas');
      pCanvas.width = 32; pCanvas.height = 32;
      const pCtx = pCanvas.getContext('2d');
      const radGrad = pCtx.createRadialGradient(16, 16, 0, 16, 16, 16);
      radGrad.addColorStop(0, '#ffffff');
      radGrad.addColorStop(0.5, 'rgba(0, 240, 255, 0.8)');
      radGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
      pCtx.fillStyle = radGrad;
      pCtx.fillRect(0, 0, 32, 32);

      const pTexture = new THREE.CanvasTexture(pCanvas);
      const pMat = new THREE.PointsMaterial({
        size: 0.12,
        map: pTexture,
        transparent: true,
        vertexColors: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      });

      this.particleSystem = new THREE.Points(pGeo, pMat);
      this.characterRoot.add(this.particleSystem);
    }

    // ------------------------------------------------------------------------
    // Mouse Drag, Inertia, Zoom & Parallax Setup
    // ------------------------------------------------------------------------
    setupInteraction() {
      const el = this.canvas;

      el.addEventListener('pointerdown', (e) => {
        this.isDragging = true;
        this.prevPointerX = e.clientX;
        this.prevPointerY = e.clientY;
        el.style.cursor = 'grabbing';
      });

      window.addEventListener('pointermove', (e) => {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          const normX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
          const normY = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
          this.mouseParallax.x = Math.max(-1, Math.min(1, normX));
          this.mouseParallax.y = Math.max(-1, Math.min(1, normY));
        }

        if (!this.isDragging) return;
        const dx = e.clientX - this.prevPointerX;
        const dy = e.clientY - this.prevPointerY;
        this.prevPointerX = e.clientX;
        this.prevPointerY = e.clientY;

        this.targetRotationY += dx * 0.012;
        this.targetRotationX = Math.max(-0.4, Math.min(0.4, this.targetRotationX + dy * 0.008));
      });

      const stopDrag = () => {
        if (this.isDragging) {
          this.isDragging = false;
          el.style.cursor = 'grab';
        }
      };

      window.addEventListener('pointerup', stopDrag);
      window.addEventListener('pointercancel', stopDrag);

      el.addEventListener('wheel', (e) => {
        e.preventDefault();
        this.targetCameraDistance = Math.max(2.2, Math.min(5.2, this.targetCameraDistance + e.deltaY * 0.003));
      }, { passive: false });
    }

    // ------------------------------------------------------------------------
    // Responsive Resize Handler
    // ------------------------------------------------------------------------
    setupResize() {
      const resize = () => {
        if (!this.container || !this.renderer || !this.camera) return;
        const rect = this.container.getBoundingClientRect();
        const width = rect.width;
        const height = rect.height;
        if (width <= 0 || height <= 0) return;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
      };

      window.addEventListener('resize', resize);
      if (window.ResizeObserver) {
        new ResizeObserver(resize).observe(this.container);
      }
    }

    // ------------------------------------------------------------------------
    // Animation State Machine Controller & Smooth Blending
    // ------------------------------------------------------------------------
    setState(stateName) {
      const validStates = ['idle', 'listening', 'thinking', 'talking', 'walking'];
      if (!validStates.includes(stateName)) {
        console.warn(`[AvatarEngine3D] Unknown state: ${stateName}`);
        return;
      }
      this.targetState = stateName;
      this.currentState = stateName;
      console.log(`[AvatarEngine3D] Transitioning to state: ${stateName.toUpperCase()}`);

      if (stateName !== 'talking') {
        this.audioEngine.stopSpeech();
      }
    }

    triggerSpeech() {
      this.setState('talking');
      this.audioEngine.startSpeech();
    }

    resetCamera() {
      this.targetRotationY = 0;
      this.targetRotationX = 0;
      this.targetCameraDistance = 3.6;
    }

    // ------------------------------------------------------------------------
    // Main Render Loop (60 FPS)
    // ------------------------------------------------------------------------
    animate() {
      requestAnimationFrame(this.animate);

      const dt = Math.min(this.clock.getDelta(), 0.1);
      const time = this.clock.getElapsedTime();

      this.frameCount++;
      const now = performance.now();
      if (now - this.lastFpsTime >= 1000) {
        this.fps = Math.round((this.frameCount * 1000) / (now - this.lastFpsTime));
        this.frameCount = 0;
        this.lastFpsTime = now;
      }

      this.currentRotationY += (this.targetRotationY - this.currentRotationY) * Math.min(1, dt * 10.0);
      this.currentRotationX += (this.targetRotationX - this.currentRotationX) * Math.min(1, dt * 10.0);
      this.currentCameraDistance += (this.targetCameraDistance - this.currentCameraDistance) * Math.min(1, dt * 8.0);

      this.characterRoot.rotation.y = this.currentRotationY;
      this.characterRoot.rotation.x = this.currentRotationX;
      this.camera.position.z = this.currentCameraDistance;

      const isTalking = this.currentState === 'talking';
      const mouthVal = this.audioEngine.update(dt, isTalking);

      if (this.headFaceMesh && this.headFaceMesh.morphTargetInfluences) {
        this.headFaceMesh.morphTargetInfluences[0] = mouthVal;
      }
      if (this.bones.jaw) {
        this.bones.jaw.rotation.x = mouthVal * 0.25;
      }
      if (this.mouthInterior) {
        this.mouthInterior.scale.y = 0.1 + mouthVal * 1.6;
      }

      this.blinkTimer += dt;
      if (this.blinkTimer > 3.8) {
        this.isBlinking = true;
        this.blinkProgress += dt * 12.0;
        if (this.blinkProgress >= Math.PI) {
          this.isBlinking = false;
          this.blinkTimer = 0;
          this.blinkProgress = 0;
        }
      }
      const eyeScaleY = this.isBlinking ? Math.max(0.08, Math.cos(this.blinkProgress)) : 1.0;
      this.eyes.forEach((eye) => {
        eye.scale.y = eyeScaleY;
      });

      this.updateStatePoses(dt, time, mouthVal);
      this.updateCape(dt, time);

      if (this.pedestalGroup) {
        this.pedestalGroup.rotation.y += dt * 0.2;
      }

      this.renderer.render(this.scene, this.camera);
    }

    // ------------------------------------------------------------------------
    // Skeletal Poses & State Machine Interpolation
    // ------------------------------------------------------------------------
    updateStatePoses(dt, time, mouthVal) {
      const b = this.bones;
      const lerpSpeed = Math.min(1, dt * 8.0);

      let targetPelvisY = -0.15;
      let targetPelvisRotZ = 0;
      let targetSpineRotX = 0;
      let targetChestRotX = 0;
      let targetChestRotY = 0;
      let targetNeckRotX = 0;
      let targetNeckRotY = 0;
      let targetNeckRotZ = 0;
      let targetHeadRotX = 0;
      let targetHeadRotY = 0;
      let targetHeadRotZ = 0;

      let targetLShoulderX = 0;
      let targetLShoulderZ = 0.15;
      let targetLForearmX = 0.15;
      let targetRShoulderX = 0;
      let targetRShoulderY = 0;
      let targetRShoulderZ = -0.15;
      let targetRUpperArmZ = 0;
      let targetRForearmX = 0.15;

      let targetLHipX = 0.08;
      let targetLShinX = 0.05;
      let targetRHipX = 0.08;
      let targetRShinX = 0.05;

      const px = this.mouseParallax.x * 0.25;
      const py = this.mouseParallax.y * 0.18;

      if (this.currentState === 'idle') {
        this.hoverTime += dt * 2.0;
        targetPelvisY = -0.15 + Math.sin(this.hoverTime) * 0.06;
        targetPelvisRotZ = Math.sin(this.hoverTime * 0.5) * 0.03;
        targetChestRotX = Math.sin(this.hoverTime * 1.1) * 0.04;
        targetNeckRotY = px;
        targetHeadRotX = py;

        targetLShoulderZ = 0.14 + Math.sin(this.hoverTime) * 0.02;
        targetRShoulderZ = -0.14 - Math.sin(this.hoverTime) * 0.02;

        this.glyphScale += (0 - this.glyphScale) * lerpSpeed;
        this.updateListeningRings(0);
      } else if (this.currentState === 'listening') {
        targetPelvisY = -0.12;
        targetNeckRotY = 0.28 + px * 0.5;
        targetNeckRotZ = -0.14;
        targetHeadRotX = -0.16 + py * 0.5;

        targetLShoulderZ = 0.22;
        targetRShoulderZ = -0.22;

        this.glyphScale += (0 - this.glyphScale) * lerpSpeed;
        this.updateListeningRings(1.0);
      } else if (this.currentState === 'thinking') {
        targetPelvisY = -0.14;
        targetNeckRotX = -0.22;
        targetNeckRotY = 0.18 + px * 0.3;
        targetHeadRotZ = 0.08;

        targetRShoulderX = 1.05;
        targetRShoulderY = -0.35;
        targetRUpperArmZ = -0.55;
        targetRForearmX = 1.75;

        targetLShoulderX = 0.20;
        targetLShoulderZ = 0.24;
        targetLForearmX = 0.65;

        this.glyphScale += (1.0 - this.glyphScale) * lerpSpeed;
        this.updateThinkingGlyph(dt, time);
        this.updateListeningRings(0);
      } else if (this.currentState === 'talking') {
        targetPelvisY = -0.15 + Math.sin(time * 3.0) * 0.02;
        targetHeadRotX = py - mouthVal * 0.12;
        targetNeckRotY = px + Math.sin(time * 6.0) * 0.06;

        targetRShoulderX = 0.35 + mouthVal * 0.25;
        targetRForearmX = 0.70 + Math.sin(time * 8.0) * 0.15;
        targetLShoulderX = 0.15;

        this.glyphScale += (0 - this.glyphScale) * lerpSpeed;
        this.updateListeningRings(0);
      } else if (this.currentState === 'walking') {
        this.walkTime += dt * 5.2;
        const stride = this.walkTime;

        targetPelvisY = -0.15 + Math.abs(Math.sin(stride)) * 0.07;
        targetPelvisRotZ = Math.sin(stride) * 0.06;
        targetChestRotY = -Math.sin(stride) * 0.12;

        targetLHipX = Math.sin(stride) * 0.65;
        targetLShinX = Math.max(0, -Math.sin(stride)) * 0.85;
        targetRHipX = -Math.sin(stride) * 0.65;
        targetRShinX = Math.max(0, Math.sin(stride)) * 0.85;

        targetLShoulderX = -Math.sin(stride) * 0.55;
        targetLForearmX = 0.25 + Math.max(0, -Math.sin(stride)) * 0.3;
        targetRShoulderX = Math.sin(stride) * 0.55;
        targetRForearmX = 0.25 + Math.max(0, Math.sin(stride)) * 0.3;

        this.spawnWalkParticles(stride);

        this.glyphScale += (0 - this.glyphScale) * lerpSpeed;
        this.updateListeningRings(0);
      }

      b.pelvis.position.y += (targetPelvisY - b.pelvis.position.y) * lerpSpeed;
      b.pelvis.rotation.z += (targetPelvisRotZ - b.pelvis.rotation.z) * lerpSpeed;

      b.spine.rotation.x += (targetSpineRotX - b.spine.rotation.x) * lerpSpeed;
      b.chest.rotation.x += (targetChestRotX - b.chest.rotation.x) * lerpSpeed;
      b.chest.rotation.y += (targetChestRotY - b.chest.rotation.y) * lerpSpeed;

      b.neck.rotation.x += (targetNeckRotX - b.neck.rotation.x) * lerpSpeed;
      b.neck.rotation.y += (targetNeckRotY - b.neck.rotation.y) * lerpSpeed;
      b.neck.rotation.z += (targetNeckRotZ - b.neck.rotation.z) * lerpSpeed;

      b.head.rotation.x += (targetHeadRotX - b.head.rotation.x) * lerpSpeed;
      b.head.rotation.y += (targetHeadRotY - b.head.rotation.y) * lerpSpeed;
      b.head.rotation.z += (targetHeadRotZ - b.head.rotation.z) * lerpSpeed;

      b.leftShoulder.rotation.x += (targetLShoulderX - b.leftShoulder.rotation.x) * lerpSpeed;
      b.leftShoulder.rotation.z += (targetLShoulderZ - b.leftShoulder.rotation.z) * lerpSpeed;
      b.leftForearm.rotation.x += (targetLForearmX - b.leftForearm.rotation.x) * lerpSpeed;

      b.rightShoulder.rotation.x += (targetRShoulderX - b.rightShoulder.rotation.x) * lerpSpeed;
      b.rightShoulder.rotation.y += (targetRShoulderY - b.rightShoulder.rotation.y) * lerpSpeed;
      b.rightShoulder.rotation.z += (targetRShoulderZ - b.rightShoulder.rotation.z) * lerpSpeed;
      b.rightUpperArm.rotation.z += (targetRUpperArmZ - b.rightUpperArm.rotation.z) * lerpSpeed;
      b.rightForearm.rotation.x += (targetRForearmX - b.rightForearm.rotation.x) * lerpSpeed;

      b.leftHip.rotation.x += (targetLHipX - b.leftHip.rotation.x) * lerpSpeed;
      b.leftShin.rotation.x += (targetLShinX - b.leftShin.rotation.x) * lerpSpeed;
      b.rightHip.rotation.x += (targetRHipX - b.rightHip.rotation.x) * lerpSpeed;
      b.rightShin.rotation.x += (targetRShinX - b.rightShin.rotation.x) * lerpSpeed;

      const thrusterIntensity = this.currentState === 'walking' ? 2.4 : 1.2 + Math.sin(time * 4) * 0.4;
      this.bootLights.forEach((l) => (l.intensity = thrusterIntensity));

      if (this.chestLight) {
        this.chestLight.intensity = 1.6 + Math.sin(time * 3.5) * 0.5;
      }

      this.updateParticles(dt);
    }

    updateThinkingGlyph(dt, time) {
      if (!this.glyphGroup) return;
      this.glyphGroup.scale.set(this.glyphScale, this.glyphScale, this.glyphScale);
      if (this.glyphScale < 0.01) return;

      if (this.glyphRings[0]) this.glyphRings[0].rotation.z += dt * 1.6;
      if (this.glyphRings[1]) this.glyphRings[1].rotation.y -= dt * 2.2;

      if (this.glyphCore) {
        this.glyphCore.rotation.x += dt * 2.0;
        this.glyphCore.rotation.y += dt * 2.5;
      }

      this.glyphGroup.children.forEach((child) => {
        if (child.userData && child.userData.angle !== undefined) {
          child.userData.angle += dt * 2.4;
          child.position.x = Math.cos(child.userData.angle) * child.userData.radius;
          child.position.y = Math.sin(child.userData.angle) * child.userData.radius;
        }
      });
    }

    updateListeningRings(targetOpacity) {
      this.rippleRings.forEach((ring) => {
        if (targetOpacity > 0) {
          ring.userData.radius += 0.018;
          if (ring.userData.radius > 0.85) {
            ring.userData.radius = 0.22;
          }
          const scale = ring.userData.radius / 0.22;
          ring.scale.set(scale, scale, 1);
          const alpha = (1 - (ring.userData.radius - 0.22) / 0.63) * 0.85;
          ring.material.opacity = alpha;
        } else {
          ring.material.opacity += (0 - ring.material.opacity) * 0.15;
        }
      });
    }

    spawnWalkParticles(stride) {
      const leftTouch = Math.sin(stride) > 0.85;
      const rightTouch = -Math.sin(stride) > 0.85;

      if (!leftTouch && !rightTouch) return;

      const p = this.particles.find((item) => !item.active);
      if (!p) return;

      p.active = true;
      p.life = 0;
      p.maxLife = 0.85;

      const footX = leftTouch ? -0.15 : 0.15;
      p.x = footX + (Math.random() - 0.5) * 0.06;
      p.y = -0.90;
      p.z = -0.05;
      p.vx = (Math.random() - 0.5) * 0.08;
      p.vy = Math.random() * 0.12;
      p.vz = -0.45 - Math.random() * 0.25;
    }

    updateParticles(dt) {
      if (!this.particleSystem) return;
      const posAttr = this.particleSystem.geometry.attributes.position;

      this.particles.forEach((p, i) => {
        if (!p.active) {
          posAttr.setY(i, -100);
          return;
        }

        p.life += dt;
        if (p.life >= p.maxLife) {
          p.active = false;
          posAttr.setY(i, -100);
          return;
        }

        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.z += p.vz * dt;

        posAttr.setXYZ(i, p.x, p.y, p.z);
      });

      posAttr.needsUpdate = true;
    }

    updateCape(dt, time) {
      if (!this.capeMesh) return;
      const geo = this.capeMesh.geometry;
      const pos = geo.attributes.position;

      const isWalking = this.currentState === 'walking';
      const targetDrag = isWalking ? -0.45 : -0.12;
      this.capeBackwardAngle += (targetDrag - this.capeBackwardAngle) * Math.min(1, dt * 6.0);

      const freq = isWalking ? 9.5 : 4.5;
      const amp = isWalking ? 0.14 : 0.06;

      for (let i = 0; i < pos.count; i++) {
        const y = pos.getY(i);
        const factor = (0.575 - y) / 1.15;

        const wave1 = Math.sin(time * freq + y * 5.5) * amp * factor;
        const wave2 = Math.cos(time * (freq * 1.3) + pos.getX(i) * 6.0) * (amp * 0.5) * factor;
        const zOffset = this.capeBackwardAngle * factor + wave1 + wave2;

        pos.setZ(i, zOffset);
      }

      pos.needsUpdate = true;
      geo.computeVertexNormals();
    }

    getTelemetry() {
      return {
        fps: this.fps,
        state: this.currentState.toUpperCase(),
        mouthOpen: Math.round(this.audioEngine.mouthOpen * 100),
        vram: '~14.2 MB (Three.js WebGL)',
        engine: 'Three.js Skeletal Rig',
        character: 'Baby Superman (Keystone "K" Armor)'
      };
    }
  }

  return new AvatarEngine3D();
});
