/**
 * East Blue Gym — Light Entrance Animations (NO scroll hijacking)
 * Pure GSAP ScrollTrigger only — native browser scroll kept intact
 */

(function () {
  'use strict';

  /* Load GSAP + ScrollTrigger only */
  function loadScript(src, onload) {
    const s = document.createElement('script');
    s.src = src;
    s.onload = onload;
    document.head.appendChild(s);
  }

  loadScript(
    'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js',
    () => loadScript(
      'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js',
      init
    )
  );

  function init() {
    gsap.registerPlugin(ScrollTrigger);

    /* ── Stagger groups (cards, accordions, stats, etc.) ── */
    const staggerGroups = [
      '.pricing-card',
      '.card',
      '.feature-item',
      '.stat-item',
      '.accordion-item',
      '.testi-card',
      '.class-card',
      '.trainer-card',
      '.shop-card',
      '.cert-item',
    ];

    staggerGroups.forEach((sel) => {
      const byParent = {};
      document.querySelectorAll(sel).forEach((el) => {
        const key = el.parentElement;
        if (!key) return;
        (byParent[key] = byParent[key] || []).push(el);
      });

      Object.values(byParent).forEach((siblings) => {
        if (siblings.length < 2) return;
        gsap.set(siblings, { opacity: 0, y: 36 });
        ScrollTrigger.create({
          trigger: siblings[0],
          start: 'top 88%',
          once: true,
          onEnter: () =>
            gsap.to(siblings, {
              opacity: 1, y: 0,
              duration: 0.75, stagger: 0.1,
              ease: 'power3.out',
            }),
        });
      });
    });

    /* ── Individual text reveals ── */
    document.querySelectorAll(
      '.section-label, .section-title, .section-title-sm, .section-subtitle, .divider'
    ).forEach((el) => {
      if (el.closest('[data-no-reveal]')) return;

      let delay = 0;
      if (el.classList.contains('section-title')) delay = 0.06;
      if (el.classList.contains('section-subtitle')) delay = 0.12;

      if (el.classList.contains('divider')) {
        gsap.set(el, { scaleX: 0, transformOrigin: 'left center', opacity: 0 });
        ScrollTrigger.create({
          trigger: el, start: 'top 92%', once: true,
          onEnter: () =>
            gsap.to(el, { scaleX: 1, opacity: 1, duration: 0.65, delay, ease: 'power3.out' }),
        });
        return;
      }

      gsap.set(el, { opacity: 0, y: 22 });
      ScrollTrigger.create({
        trigger: el, start: 'top 90%', once: true,
        onEnter: () =>
          gsap.to(el, { opacity: 1, y: 0, duration: 0.85, delay, ease: 'power3.out' }),
      });
    });

    /* ── Hero entrance on page load ── */
    const heroEls = [
      '.page-hero .hero-tag',
      '.page-hero-content h1',
      '.page-hero-content p',
    ].flatMap((s) => [...document.querySelectorAll(s)]);

    if (heroEls.length) {
      gsap.set(heroEls, { opacity: 0, y: 28 });
      gsap.to(heroEls, {
        opacity: 1, y: 0,
        duration: 0.9, stagger: 0.13,
        ease: 'power3.out', delay: 0.25,
      });
    }

    /* ── Thin scroll progress bar at very top ── */
    const bar = document.createElement('div');
    bar.style.cssText =
      'position:fixed;top:0;left:0;height:2px;width:0;background:var(--yellow);z-index:9999;pointer-events:none;';
    document.body.appendChild(bar);
    ScrollTrigger.create({
      start: 0, end: 'max',
      onUpdate: ({ progress }) => (bar.style.width = progress * 100 + '%'),
    });
  }
})();
