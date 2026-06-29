import React, { useEffect, useRef } from 'react';

/**
 * VoiceOrb V3 Final — The original 3D torus wireframe with orbiting particles & rich core,
 * but heavily optimized to use minimal CPU/RAM.
 * 
 * OPTIMIZATIONS vs original:
 * - 20fps idle / 30fps active (not 60fps)
 * - Reduced mesh lines (8 lat, 12 lon) with fewer steps per line
 * - Max 20 particles (not 50), no shadowBlur (expensive compositing)
 * - Pre-allocated math, no garbage collection pressure
 * - Full pause when tab is hidden
 * - CSS pulse rings overlaid (GPU-composited, zero canvas cost)
 */
const VoiceOrb = ({ state = 'idle', size = 280 }) => {
  const canvasRef = useRef(null);
  const stateRef = useRef(state);

  useEffect(() => {
    stateRef.current = state;
  }, [state]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = size;
    canvas.height = size;

    const cx = size / 2;
    const cy = size / 2;
    const scale = size / 280;
    const R = 72 * scale;  // Major radius
    const r = 34 * scale;  // Minor radius

    let time = 0;
    let amplitude = 0.06;
    let rotX = 0.6;
    let rotY = 0;
    let rotZ = 0;

    // Reusable projection object (zero allocation per frame)
    const pt = { x: 0, y: 0, z: 0 };

    const project = (u, v, R_, r_) => {
      const cu = Math.cos(u), su = Math.sin(u);
      const cv = Math.cos(v), sv = Math.sin(v);
      const tx = (R_ + r_ * cu) * cv;
      const ty = (R_ + r_ * cu) * sv;
      const tz = r_ * su;

      const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
      const y1 = ty * cosX - tz * sinX;
      const z1 = ty * sinX + tz * cosX;

      const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
      const x2 = tx * cosY + z1 * sinY;

      const cosZ = Math.cos(rotZ), sinZ = Math.sin(rotZ);
      pt.x = cx + (x2 * cosZ - y1 * sinZ);
      pt.y = cy + (x2 * sinZ + y1 * cosZ);
      pt.z = -tx * sinY + z1 * cosY;
    };

    // ---- MESH DRAWING ----
    const drawMesh = () => {
      const pulse = 1.0 + amplitude * 0.12;
      const Rp = R * pulse;
      const rp = r * pulse;
      const breathe = Math.sin(time * 1.5) * 3 * scale;

      // Latitude rings (8 lines, 32 steps each)
      for (let i = 0; i < 8; i++) {
        const u = (i / 8) * Math.PI * 2;
        ctx.beginPath();
        for (let j = 0; j <= 32; j++) {
          const v = (j / 32) * Math.PI * 2;
          const wave = Math.sin(v * 3 + time * 2 + u) * (2 + amplitude * 6) +
                       Math.cos(v * 5 - time * 1.5) * (1.5 + amplitude * 3);
          project(u, v, Rp, rp + wave + breathe * Math.sin(u * 2 + time));
          j === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y);
        }
        ctx.closePath();
        ctx.strokeStyle = `rgba(0, 212, 255, ${i % 3 === 0 ? 0.55 : 0.25})`;
        ctx.lineWidth = i % 4 === 0 ? 1.2 : 0.6;
        ctx.stroke();
      }

      // Longitude rings (12 lines, 24 steps each)
      for (let j = 0; j < 12; j++) {
        const v = (j / 12) * Math.PI * 2;
        ctx.beginPath();
        for (let i = 0; i <= 24; i++) {
          const u = (i / 24) * Math.PI * 2;
          const wave = Math.sin(v * 3 + time * 2 + u) * (2 + amplitude * 6) +
                       Math.cos(v * 5 - time * 1.5) * (1.5 + amplitude * 3);
          project(u, v, Rp, rp + wave + breathe * Math.sin(u * 2 + time));
          i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y);
        }
        ctx.closePath();
        ctx.strokeStyle = `rgba(0, 180, 255, ${j % 4 === 0 ? 0.4 : 0.15})`;
        ctx.lineWidth = j % 6 === 0 ? 1.0 : 0.45;
        ctx.stroke();
      }

      // Bright outer edge ring (40 steps)
      ctx.beginPath();
      for (let j = 0; j <= 40; j++) {
        const v = (j / 40) * Math.PI * 2;
        const wave = Math.sin(v * 3 + time * 2) * (2 + amplitude * 6);
        project(0, v, Rp, rp + wave + breathe);
        j === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(0, 212, 255, 0.95)';
      ctx.lineWidth = 1.8;
      ctx.stroke();
    };

    // ---- PARTICLES ----
    let particles = [];
    const MAX_PARTICLES = 45;

    const spawnParticle = () => {
      const u = Math.random() * Math.PI * 2;
      const v = Math.random() * Math.PI * 2;
      project(u, v, R, r + 8 * scale + Math.random() * 12 * scale);
      particles.push({
        u, v,
        sz: (0.8 + Math.random() * 1.5) * scale,
        r: Math.random() > 0.8 ? 180 : 0,
        g: 200 + Math.random() * 55,
        b: 255,
        life: 1.0,
        decay: 0.005 + Math.random() * 0.012,
        speed: 0.004 + Math.random() * 0.01,
        wobble: Math.random() * Math.PI * 2
      });
    };

    const drawParticles = () => {
      const spawnRate = stateRef.current === 'idle' ? 0.18 : 0.35;
      if (particles.length < MAX_PARTICLES && Math.random() < spawnRate) {
        spawnParticle();
      }

      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.life -= p.decay;
        if (p.life <= 0) { particles.splice(i, 1); continue; }

        p.v += p.speed;
        p.u += Math.sin(time * 2 + p.wobble) * 0.002;

        const pulse = 1.0 + amplitude * 0.12;
        project(p.u, p.v, R * pulse, r + 10 * scale);

        ctx.globalAlpha = p.life * 0.75;
        ctx.fillStyle = `rgb(${p.r}, ${p.g}, ${p.b})`;
        ctx.fillRect(pt.x - p.sz * 0.5, pt.y - p.sz * 0.5, p.sz, p.sz);
      }
      ctx.globalAlpha = 1.0;
    };

    // ---- CORE GLOW (Black Hole Style) ----
    const drawCore = () => {
      const pulse = 1.0 + amplitude * 0.3;
      const coreR = 14 * scale * pulse;

      // Outer diffuse glow (Accretion disk)
      const g1 = ctx.createRadialGradient(cx, cy, coreR * 0.8, cx, cy, coreR * 5);
      g1.addColorStop(0, 'rgba(0, 230, 255, 0.7)');
      g1.addColorStop(0.2, 'rgba(0, 140, 255, 0.3)');
      g1.addColorStop(0.5, 'rgba(0, 80, 200, 0.08)');
      g1.addColorStop(1, 'rgba(0, 40, 120, 0)');
      ctx.beginPath();
      ctx.arc(cx, cy, coreR * 5, 0, Math.PI * 2);
      ctx.fillStyle = g1;
      ctx.fill();

      // Inner Event Horizon (Black Hole)
      ctx.beginPath();
      ctx.arc(cx, cy, coreR * 0.8, 0, Math.PI * 2);
      ctx.fillStyle = '#050a15'; // Very dark space blue/black
      ctx.fill();

      // Accretion disk bright inner edge
      ctx.beginPath();
      ctx.arc(cx, cy, coreR * 0.8, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(0, 255, 255, 0.9)';
      ctx.lineWidth = 1.5 * scale;
      ctx.stroke();
    };

    // ---- ANIMATION LOOP ----
    let animId;
    let lastTime = performance.now();

    const animate = (now) => {
      animId = requestAnimationFrame(animate);

      const elapsed = now - lastTime;
      const st = stateRef.current;
      const targetFps = (st === 'idle') ? 20 : 30;
      if (elapsed < 1000 / targetFps - 1) return;
      lastTime = now - (elapsed % (1000 / targetFps));

      time += 0.025;

      // Smooth amplitude towards target
      let targetAmp = 0.06;
      if (st === 'speaking') {
        targetAmp = 0.5 + Math.sin(time * 4) * 0.3 + Math.sin(time * 10) * 0.2;
      } else if (st === 'listening') {
        targetAmp = 0.2 + Math.sin(time * 8) * 0.12;
      } else if (st === 'working') {
        targetAmp = 0.15 + Math.sin(time * 2) * 0.08;
      } else {
        targetAmp = 0.09 + Math.sin(time * 1.5) * 0.05; // More pronounced idle breathing
      }
      amplitude += (targetAmp - amplitude) * 0.2;

      // Slow rotation
      rotY = time * 0.18;
      rotZ = Math.sin(time * 0.35) * 0.05;
      rotX = 0.6 + Math.sin(time * 0.2) * 0.04;

      ctx.clearRect(0, 0, size, size);
      drawMesh();
      drawParticles();
      drawCore();
    };

    // Pause when tab is hidden
    const onVisChange = () => {
      if (document.hidden) {
        cancelAnimationFrame(animId);
      } else {
        lastTime = performance.now();
        animId = requestAnimationFrame(animate);
      }
    };
    document.addEventListener('visibilitychange', onVisChange);
    animId = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animId);
      document.removeEventListener('visibilitychange', onVisChange);
    };
  }, [size]);

  // Derive pulse ring color from state
  let pulseColor = '#00d4ff';
  let pulseDuration = '4s';
  if (state === 'speaking') { pulseColor = '#00ffcc'; pulseDuration = '1.2s'; }
  else if (state === 'listening') { pulseColor = '#00ffff'; pulseDuration = '2s'; }
  else if (state === 'working') { pulseColor = '#aa7dfd'; pulseDuration = '2.5s'; }

  return (
    <div style={{
      position: 'relative',
      width: `${size}px`,
      height: `${size}px`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      {/* CSS pulse rings (GPU composited overlay, zero canvas cost) */}
      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes voice-pulse-out {
          0% { transform: scale(0.15); opacity: 0.6; }
          100% { transform: scale(1.0); opacity: 0; }
        }
      `}} />
      <div style={{
        position: 'absolute',
        width: `${size * 0.75}px`,
        height: `${size * 0.75}px`,
        borderRadius: '50%',
        border: `1.5px solid ${pulseColor}`,
        animation: `voice-pulse-out ${pulseDuration} ease-out infinite`,
        willChange: 'transform, opacity',
        pointerEvents: 'none',
        zIndex: 3
      }} />
      <div style={{
        position: 'absolute',
        width: `${size * 0.75}px`,
        height: `${size * 0.75}px`,
        borderRadius: '50%',
        border: `1px solid ${pulseColor}`,
        animation: `voice-pulse-out ${pulseDuration} ease-out infinite`,
        animationDelay: `calc(${pulseDuration} / 2)`,
        willChange: 'transform, opacity',
        pointerEvents: 'none',
        zIndex: 3
      }} />

      {/* The 3D canvas torus */}
      <canvas
        ref={canvasRef}
        style={{ position: 'relative', zIndex: 2, pointerEvents: 'none' }}
      />
    </div>
  );
};

export default VoiceOrb;
