/* FuturePath — interaction layer.
 *
 * Three pieces, all progressive: the page is fully readable with JavaScript off,
 * and each enhancement only adds to it.
 *   1. Reveal on scroll — sections fade and rise as they enter the viewport.
 *   2. Animated counters — match percentages and metrics count up.
 *   3. Animated bars — match bars fill from zero when they become visible.
 */

(function () {
  'use strict';

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ------------------------------------------------------------ 1. reveal
  function initReveal() {
    const targets = document.querySelectorAll(
      '.card, .metric, .section > h2, .section-head, .milestone, .hero-panel, .step-card, .table-wrap'
    );
    if (reduced || !('IntersectionObserver' in window)) return;

    targets.forEach(el => el.classList.add('reveal'));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        // Stagger items that appear together, so a grid cascades rather than pops.
        const delay = Math.min(i * 55, 330);
        setTimeout(() => entry.target.classList.add('reveal-in'), delay);
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -40px 0px', threshold: 0.06 });

    targets.forEach(el => io.observe(el));
  }

  // ------------------------------------------------------------ 2. counters
  function animateNumber(el, to, suffix, duration) {
    if (reduced) { el.textContent = to + suffix; return; }
    const from = 0;
    const start = performance.now();
    duration = duration || 900;
    function frame(now) {
      const t = Math.min(1, (now - start) / duration);
      // easeOutCubic — fast start, gentle settle
      const eased = 1 - Math.pow(1 - t, 3);
      const value = from + (to - from) * eased;
      el.textContent = (Number.isInteger(to) ? Math.round(value) : value.toFixed(1)) + suffix;
      if (t < 1) requestAnimationFrame(frame);
      else el.textContent = to + suffix;
    }
    requestAnimationFrame(frame);
  }

  function initCounters() {
    const els = document.querySelectorAll('[data-count]');
    if (!els.length) return;

    const run = (el) => {
      const to = parseFloat(el.dataset.count);
      if (isNaN(to)) return;
      animateNumber(el, to, el.dataset.suffix || '', parseInt(el.dataset.duration || '900', 10));
    };

    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        run(entry.target);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.3 });
    els.forEach(el => io.observe(el));
  }

  // ---------------------------------------------------------------- 3. bars
  function initBars() {
    const bars = document.querySelectorAll('.match-bar > i, .riasec-row .bar > i');
    if (!bars.length) return;

    bars.forEach(bar => {
      // Read the target from the inline width, then reset so it can animate in.
      const target = bar.style.width || '0%';
      bar.dataset.target = target;
      bar.style.width = '0%';
    });

    const fill = (bar) => {
      requestAnimationFrame(() => { bar.style.width = bar.dataset.target; });
    };

    if (!('IntersectionObserver' in window) || reduced) { bars.forEach(fill); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        setTimeout(() => fill(entry.target), Math.min(i * 40, 260));
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15 });
    bars.forEach(bar => io.observe(bar));
  }

  // ------------------------------------------------------- 4. active section
  // Keeps the nav honest as the user scrolls a long page.
  function initScrollSpy() {
    const sections = document.querySelectorAll('[data-spy]');
    if (!sections.length || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const link = document.querySelector(`nav.top a[data-spy-link="${entry.target.dataset.spy}"]`);
        if (link) link.classList.toggle('active', entry.isIntersecting);
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    sections.forEach(s => io.observe(s));
  }

  // ------------------------------------------------------- 5. aurora backdrop
  // Slow-moving colour blobs behind the page. Pure CSS transforms, GPU
  // composited, and disabled entirely under reduced-motion.
  function initAurora() {
    if (reduced) return;
    const aurora = document.createElement('div');
    aurora.className = 'aurora';
    aurora.setAttribute('aria-hidden', 'true');
    aurora.innerHTML = '<span class="a1"></span><span class="a2"></span><span class="a3"></span>';
    document.body.prepend(aurora);
  }

  // ----------------------------------------------------------- 6. card tilt
  // A very small parallax tilt on pointer devices only. 3 degrees, so it reads
  // as responsiveness rather than a gimmick.
  function initTilt() {
    if (reduced) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    document.querySelectorAll('.card.link, .metric').forEach(card => {
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform =
          `perspective(900px) rotateY(${px * 3}deg) rotateX(${-py * 3}deg) translateY(-2px)`;
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  // ------------------------------------------------------- 7. live clock dot
  // Small signal that the page is alive, used on the hero panel.
  function initLiveDot() {
    document.querySelectorAll('[data-live]').forEach(el => {
      el.innerHTML = '<span class="livedot"></span>' + el.innerHTML;
    });
  }

  // --------------------------------------------------- circular progress ring
  // Used on the dashboard and the profile page. Animates stroke-dashoffset from
  // empty to the value rendered by the server.
  function initProgressRings() {
    document.querySelectorAll('.pr-fill').forEach(ring => {
      const target = ring.dataset.offset;
      if (target === undefined) return;
      const run = () => {
        if (reduced) { ring.style.strokeDashoffset = target; return; }
        ring.style.transition = 'stroke-dashoffset 1.3s cubic-bezier(.2,.8,.2,1)';
        ring.style.strokeDashoffset = target;
      };
      if (!('IntersectionObserver' in window)) { run(); return; }
      const io = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) { run(); io.disconnect(); }
      }, { threshold: 0.25 });
      io.observe(ring);
    });
  }

  // ------------------------------------------------- roadmap connector lines
  function initRoadmapFlow() {
    const nodes = document.querySelectorAll('.flow-node');
    const conns = document.querySelectorAll('.flow-connector');
    if (!nodes.length) return;
    if (!('IntersectionObserver' in window)) { conns.forEach(c => c.classList.add('flow-lit')); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const i = Number(entry.target.dataset.node);
        const conn = document.querySelector(`.flow-connector[data-node="${i}"]`);
        if (conn) setTimeout(() => conn.classList.add('flow-lit'), 170);
        entry.target.classList.add('flow-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.35 });
    nodes.forEach(n => io.observe(n));
  }

  // --------------------------------------------------------- career filters
  function initFilters() {
    const bar = document.getElementById('fieldFilters');
    const grid = document.getElementById('explorerGrid');
    const empty = document.getElementById('explorerEmpty');
    if (!bar || !grid) return;
    bar.addEventListener('click', (e) => {
      const btn = e.target.closest('.chip');
      if (!btn) return;
      bar.querySelectorAll('.chip').forEach(c => c.classList.remove('chip-on'));
      btn.classList.add('chip-on');
      const field = btn.dataset.field;
      let shown = 0;
      grid.querySelectorAll('.explorer-card').forEach((card, i) => {
        const match = !field || card.dataset.field === field;
        card.classList.toggle('is-hidden', !match);
        if (!match) return;
        shown++;
        if (reduced) return;
        card.style.animation = 'none';
        void card.offsetWidth;   // force reflow so the animation replays
        card.style.animation = `cardIn .38s cubic-bezier(.2,.8,.2,1) ${Math.min(i * 35, 280)}ms both`;
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
    });
  }

  // ------------------------------------------------------- staggered reveals
  // Cards inside a grid enter in sequence rather than all at once, which is what
  // makes a long page feel like it is assembling rather than appearing.
  function initStagger() {
    if (reduced) return;
    document.querySelectorAll('.career-grid, .why-grid, .cat-grid, .steps, .grid').forEach(grid => {
      const kids = [...grid.children];
      kids.forEach((k, i) => {
        k.style.transitionDelay = Math.min(i * 55, 330) + 'ms';
      });
    });
  }

  // ----------------------------------------------------------- image parallax
  // A very small vertical offset on card imagery as it crosses the viewport.
  // 12px at most — enough to feel dimensional, not enough to notice as motion.
  function initParallax() {
    if (reduced) return;
    const media = document.querySelectorAll('.cc-media img, .why-media img');
    if (!media.length || !('IntersectionObserver' in window)) return;
    let ticking = false;
    const update = () => {
      const vh = window.innerHeight;
      media.forEach(img => {
        const r = img.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        const progress = (r.top + r.height / 2 - vh / 2) / vh;   // -0.5 .. 0.5
        img.style.transform = `scale(1.06) translateY(${(-progress * 14).toFixed(1)}px)`;
      });
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  // ------------------------------------------------- live match-score ticker
  // Counts each match percentage up from zero when it scrolls into view, then
  // holds. Reads the real value from the server-rendered markup.
  function initMatchTicker() {
    const els = document.querySelectorAll('[data-count]');
    if (!els.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(el => { el.textContent = el.dataset.count + (el.dataset.suffix || ''); });
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const to = parseFloat(el.dataset.count);
        const suffix = el.dataset.suffix || '';
        if (isNaN(to)) { io.unobserve(el); return; }
        const dur = parseInt(el.dataset.duration || '900', 10);
        const t0 = performance.now();
        const step = (now) => {
          const t = Math.min(1, (now - t0) / dur);
          const eased = 1 - Math.pow(1 - t, 3);
          const val = to * eased;
          el.textContent = (Number.isInteger(to) ? Math.round(val) : val.toFixed(1)) + suffix;
          if (t < 1) requestAnimationFrame(step);
          else el.textContent = to + suffix;
        };
        requestAnimationFrame(step);
        io.unobserve(el);
      });
    }, { threshold: 0.25 });
    els.forEach(el => io.observe(el));
  }

  // ------------------------------------------------------- robot eye tracking
  // Only the PUPILS move — the head stays still, which reads as the robot
  // watching you rather than the whole thing sliding about. Damped so it eases
  // toward the pointer instead of snapping, and returns to centre on leave.
  function initRobotTracking() {
    const ai = document.querySelector('.orbit-ai');
    if (!ai) return;
    if (reduced) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    const MAX_X = 3.4;    // px the pupils may travel horizontally
    const MAX_Y = 2.6;    // and vertically (a little less, eyes move less up/down)
    let tx = 0, ty = 0, cx = 0, cy = 0, running = false;

    const write = () => {
      ai.style.setProperty('--look-x', cx.toFixed(2));
      ai.style.setProperty('--look-y', cy.toFixed(2));
    };

    const tick = () => {
      const k = 0.18;
      cx += (tx - cx) * k;
      cy += (ty - cy) * k;
      write();
      if (Math.abs(tx - cx) < 0.02 && Math.abs(ty - cy) < 0.02) {
        cx = tx; cy = ty; write(); running = false; return;
      }
      requestAnimationFrame(tick);
    };
    const start = () => { if (!running) { running = true; requestAnimationFrame(tick); } };

    window.addEventListener('pointermove', (e) => {
      const r = ai.getBoundingClientRect();
      const centreX = r.left + r.width / 2;
      const centreY = r.top + r.height / 2;
      const reach = Math.max(window.innerWidth, window.innerHeight) * 0.45;
      let nx = Math.max(-1, Math.min(1, (e.clientX - centreX) / reach));
      let ny = Math.max(-1, Math.min(1, (e.clientY - centreY) / reach));
      tx = nx * MAX_X;
      ty = ny * MAX_Y;
      start();
    }, { passive: true });

    window.addEventListener('pointerleave', () => { tx = 0; ty = 0; start(); });
  }

  // -------------------------------------------------- click an orbit icon
  // Clicking a career icon names it in a minimal readout under the robot, with
  // a single link to its full page. No hover tooltips — the label appears only
  // when asked for, and clicking elsewhere or pressing Escape clears it.
  function initOrbitSelection() {
    const nodes = document.querySelectorAll('.orbit-node[data-label]');
    const readout = document.getElementById('orbitReadout');
    if (!nodes.length || !readout) return;

    const labelEl = readout.querySelector('.or-label');
    const linkEl = readout.querySelector('.or-link');
    let active = null;

    function select(node) {
      if (active === node) { clear(); return; }   // clicking again closes it
      nodes.forEach(n => n.classList.remove('is-active'));
      node.classList.add('is-active');
      labelEl.textContent = node.dataset.label;
      linkEl.setAttribute('href', '/career/' + node.dataset.slug);
      readout.hidden = false;
      // Restart the entrance animation.
      readout.classList.remove('is-in');
      void readout.offsetWidth;
      readout.classList.add('is-in');
      active = node;
    }

    function clear() {
      nodes.forEach(n => n.classList.remove('is-active'));
      readout.hidden = true;
      readout.classList.remove('is-in');
      active = null;
    }

    nodes.forEach(node => {
      node.addEventListener('click', (e) => { e.preventDefault(); select(node); });
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') clear(); });
    document.addEventListener('click', (e) => {
      if (e.target.closest('.orbit-node') || e.target.closest('.orbit-readout')) return;
      if (active) clear();
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    // initAurora() intentionally not called: the drifting colour blobs read as
    // decorative noise in the editorial design. Left in the file, unused.
    initProgressRings();
    initRoadmapFlow();
    initFilters();
    initStagger();
    initParallax();
    initMatchTicker();
    initRobotTracking();
    initOrbitSelection();
    initReveal();
    initBars();
    initScrollSpy();
    initLiveDot();
  });

  // Expose for pages that inject content after load (e.g. the generator preview).
  window.FX = { initReveal, initCounters, initBars };
})();
