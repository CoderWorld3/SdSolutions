/* SD Solutions site script. No dependencies except Three.js on the home page. */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;
  root.classList.add('js');

  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var canHover = !!(window.matchMedia && window.matchMedia('(hover: hover)').matches);
  var hasIO = 'IntersectionObserver' in window;

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }

  /* ------------------------------------------------------------ scroll state */
  var header = $('.site-header');
  var bar = $('.progress i');
  var toTop = $('.to-top');
  var ticking = false;

  function onScroll() {
    var y = window.pageYOffset || root.scrollTop || 0;
    var max = root.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    if (header) header.classList.toggle('scrolled', y > 24);
    if (toTop) toTop.classList.toggle('show', y > 700);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }

  /* ------------------------------------------------------------ mobile menu */
  (function () {
    var burger = $('.burger');
    var links = $('.nav-links');
    if (!header || !burger || !links) return;

    function setMenu(open, returnFocus) {
      header.classList.toggle('menu-open', open);
      doc.body.classList.toggle('menu-lock', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (!open && returnFocus) burger.focus();
    }
    burger.addEventListener('click', function () {
      setMenu(!header.classList.contains('menu-open'));
    });
    $$('a', links).forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('menu-open')) setMenu(false, true);
    });
    doc.addEventListener('click', function (e) {
      if (header.classList.contains('menu-open') && !header.contains(e.target)) setMenu(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1020 && header.classList.contains('menu-open')) setMenu(false);
    });
  })();

  /* ------------------------------------------------------------ reveal on scroll */
  (function () {
    var items = $$('.reveal');
    if (!items.length) return;

    $$('[data-stagger]').forEach(function (group) {
      $$('.reveal', group).forEach(function (el, i) {
        el.style.transitionDelay = (i * 90) + 'ms';
      });
    });
    items.forEach(function (el) {
      if (el.dataset.delay) el.style.transitionDelay = el.dataset.delay + 'ms';
    });

    function show(el) {
      el.classList.add('is-visible');
      // clear the stagger delay afterwards so hover/tilt stays instant
      window.setTimeout(function () { el.style.transitionDelay = ''; }, 1600);
    }
    if (!hasIO) { items.forEach(show); return; }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { show(entry.target); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  })();

  /* ------------------------------------------------------------ stairs */
  (function () {
    var stairs = $$('.stairs');
    if (!stairs.length) return;
    if (!hasIO) { stairs.forEach(function (s) { s.classList.add('in-view'); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1 });
    stairs.forEach(function (s) { io.observe(s); });
  })();

  /* ------------------------------------------------------------ count-up */
  (function () {
    var els = $$('[data-count]');
    if (!els.length) return;

    function format(el, value) {
      var dec = parseInt(el.dataset.decimals || '0', 10);
      var n = dec ? value.toFixed(dec) : Math.round(value).toLocaleString('en-US');
      return (el.dataset.prefix || '') + n + (el.dataset.suffix || '');
    }
    function run(el) {
      var end = parseFloat(el.dataset.count);
      if (reduce || isNaN(end)) { el.textContent = format(el, isNaN(end) ? 0 : end); return; }
      var dur = 1700, start = null;
      function step(ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = format(el, end * eased);
        if (p < 1) window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    }
    if (reduce) return; // the HTML already contains the final numbers
    if (!hasIO) { els.forEach(function (el) { run(el); }); return; }
    els.forEach(function (el) { el.textContent = format(el, 0); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    els.forEach(function (el) { io.observe(el); });
  })();

  /* ------------------------------------------------------------ tabs */
  $$('[data-tabs]').forEach(function (wrap) {
    var list = $('[role="tablist"]', wrap);
    var tabs = $$('[role="tab"]', wrap);
    var panels = $$('[role="tabpanel"]', wrap);
    if (!tabs.length || tabs.length !== panels.length) return;

    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (focus) tabs[i].focus();
      if (list && list.scrollWidth > list.clientWidth + 4) {
        list.scrollTo({ left: tabs[i].offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
      }
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i, false); });
      t.addEventListener('keydown', function (e) {
        var n = tabs.length, next = null;
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = (i + 1) % n;
        else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = (i - 1 + n) % n;
        else if (e.key === 'Home') next = 0;
        else if (e.key === 'End') next = n - 1;
        if (next !== null) { e.preventDefault(); select(next, true); }
      });
    });
    var start = tabs.findIndex(function (t) { return t.getAttribute('aria-selected') === 'true'; });
    select(start < 0 ? 0 : start, false);
  });

  /* ------------------------------------------------------------ carousel */
  $$('[data-carousel]').forEach(function (c) {
    var track = $('.track', c);
    var slides = $$('.slide', c);
    var dots = $$('.dots button', c);
    var prev = $('[data-prev]', c);
    var next = $('[data-next]', c);
    if (!track || slides.length < 2) return;

    var idx = 0, timer = null, held = false;

    function go(i) {
      idx = (i + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + (idx * 100) + '%)';
      dots.forEach(function (d, j) { d.setAttribute('aria-current', j === idx ? 'true' : 'false'); });
      slides.forEach(function (s, j) { s.setAttribute('aria-hidden', j === idx ? 'false' : 'true'); });
    }
    function stop() { if (timer) { window.clearInterval(timer); timer = null; } }
    function play() {
      if (reduce || timer || held || doc.hidden) return;
      timer = window.setInterval(function () { go(idx + 1); }, 6500);
    }
    function restart() { stop(); play(); }

    if (prev) prev.addEventListener('click', function () { go(idx - 1); restart(); });
    if (next) next.addEventListener('click', function () { go(idx + 1); restart(); });
    dots.forEach(function (d, j) { d.addEventListener('click', function () { go(j); restart(); }); });

    c.addEventListener('mouseenter', function () { held = true; stop(); });
    c.addEventListener('mouseleave', function () { held = false; play(); });
    c.addEventListener('focusin', function () { held = true; stop(); });
    c.addEventListener('focusout', function () { held = false; play(); });
    doc.addEventListener('visibilitychange', function () { if (doc.hidden) stop(); else play(); });
    c.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { go(idx - 1); restart(); }
      if (e.key === 'ArrowRight') { go(idx + 1); restart(); }
    });

    var x0 = null;
    c.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    c.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) { go(idx + (dx < 0 ? 1 : -1)); restart(); }
      x0 = null;
    }, { passive: true });

    go(0);
    play();
  });

  /* ------------------------------------------------------------ FAQ accordion */
  (function () {
    var items = $$('.faq-item');
    if (!items.length) return;

    function setOpen(item, open) {
      var btn = $('.faq-q', item), panel = $('.faq-a', item);
      item.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      panel.style.height = open ? panel.scrollHeight + 'px' : '0px';
    }
    items.forEach(function (item, i) {
      var btn = $('.faq-q', item), panel = $('.faq-a', item);
      if (!btn || !panel) return;
      var id = 'faq-panel-' + i;
      panel.id = id;
      btn.setAttribute('aria-controls', id);
      setOpen(item, item.classList.contains('open'));
      btn.addEventListener('click', function () {
        var willOpen = !item.classList.contains('open');
        items.forEach(function (o) { if (o !== item) setOpen(o, false); });
        setOpen(item, willOpen);
      });
    });
    window.addEventListener('resize', function () {
      items.forEach(function (item) {
        if (item.classList.contains('open')) {
          var p = $('.faq-a', item); p.style.height = p.scrollHeight + 'px';
        }
      });
    });
  })();

  /* ------------------------------------------------------------ forms */
  (function () {
    var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    var PHONE = /^[+()\-.\s\d]{7,20}$/;

    function validate(input) {
      var field = input.closest('.field');
      if (!field) return true;
      var v = input.type === 'checkbox' ? (input.checked ? '1' : '') : (input.type === 'file' ? '' : input.value.trim());
      var msg = '';
      if (input.type === 'file') {
        var file = input.files && input.files[0];
        if (file) {
          var okType = /\.(pdf|docx?)$/i.test(file.name);
          if (!okType) msg = 'Please attach a PDF or Word file.';
          else if (file.size > 5 * 1024 * 1024) msg = 'That file is over 5 MB. Please attach a smaller one.';
        }
      }
      else if (input.required && !v) msg = input.getAttribute('data-required-msg') || 'This field is required.';
      else if (v && input.type === 'email' && !EMAIL.test(v)) msg = 'Enter a valid email, like name@example.com.';
      else if (v && input.type === 'tel' && !PHONE.test(v)) msg = 'Enter a valid phone number.';
      else if (v && input.minLength > 0 && v.length < input.minLength) msg = 'Please write at least ' + input.minLength + ' characters.';
      var err = $('.err', field);
      if (err) err.textContent = msg;
      field.classList.toggle('invalid', !!msg);
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    }

    // Replace the simulated delay with a real call by adding data-endpoint="https://..." to the form.
    function send(form, payload) {
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) {
        return new Promise(function (resolve) { window.setTimeout(resolve, 900); });
      }
      var hasFile = form.querySelector('input[type="file"]');
      var opts = hasFile
        ? { method: 'POST', body: new FormData(form) }
        : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) };
      return fetch(endpoint, opts).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); });
    }

    $$('form[data-form]').forEach(function (form) {
      form.setAttribute('novalidate', '');
      var kind = form.getAttribute('data-form');
      var inputs = $$('input, textarea, select', form).filter(function (i) { return i.name !== 'website'; });
      var btn = $('button[type="submit"]', form);
      var status = $('.form-status', form) || $('.sub-msg', form);

      inputs.forEach(function (input) {
        var touched = false;
        input.addEventListener('blur', function () { touched = true; validate(input); });
        if (input.type === 'checkbox' || input.type === 'file' || input.tagName === 'SELECT') {
          input.addEventListener('change', function () { touched = true; validate(input); });
        }
        input.addEventListener('input', function () {
          var f = input.closest('.field');
          if (touched || (f && f.classList.contains('invalid'))) validate(input);
        });
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (btn && btn.classList.contains('loading')) return;

        var firstBad = null;
        inputs.forEach(function (input) { if (!validate(input) && !firstBad) firstBad = input; });
        if (firstBad) {
          firstBad.focus();
          if (status && kind === 'newsletter') {
            status.className = 'sub-msg bad';
            status.textContent = 'Please check your email address.';
          }
          return;
        }

        var honeypot = form.querySelector('input[name="website"]');
        var payload = {};
        inputs.forEach(function (i) {
          if (i.type === 'file') return;
          payload[i.name || i.id] = i.type === 'checkbox' ? i.checked : i.value.trim();
        });

        if (btn) { btn.classList.add('loading'); btn.disabled = true; }
        if (status) { status.textContent = ''; status.classList.remove('error'); }

        var job = (honeypot && honeypot.value) ? Promise.resolve() : send(form, payload);
        job.then(function () {
          if (kind === 'newsletter') {
            if (status) { status.className = 'sub-msg ok'; status.textContent = 'You are in. Your first tip lands this week.'; }
            form.reset();
            if (btn) { btn.classList.remove('loading'); btn.disabled = false; }
          } else {
            var shell = form.closest('.form') || form;
            shell.classList.add('done');
            var ok = $('.success h3', shell);
            if (ok) { ok.setAttribute('tabindex', '-1'); ok.focus(); }
          }
        }).catch(function () {
          if (btn) { btn.classList.remove('loading'); btn.disabled = false; }
          if (status) {
            if (kind === 'newsletter') { status.className = 'sub-msg bad'; }
            else { status.className = 'form-status error'; }
            status.textContent = 'That did not go through. Please try again, or email arvinmishraji@gmail.com.';
          }
        });
      });
    });
  })();

  /* ------------------------------------------------------------ tilt */
  if (!reduce && canHover) {
    $$('.tilt').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        el.style.setProperty('--ry', (x * 7) + 'deg');
        el.style.setProperty('--rx', (-y * 7) + 'deg');
      });
      el.addEventListener('mouseleave', function () {
        el.style.setProperty('--ry', '0deg');
        el.style.setProperty('--rx', '0deg');
      });
    });
  }

  /* ------------------------------------------------------------ hero 3D */
  (function () {
    var canvas = $('#hero-canvas');
    if (!canvas) return;
    var box = canvas.parentElement;

    function fallback() { box.classList.add('no-webgl'); }
    if (typeof THREE === 'undefined') { fallback(); return; }

    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    } catch (err) { fallback(); return; }

    var w = box.clientWidth, h = box.clientHeight;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(w, h);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
    camera.position.set(0, 0, 8.2);

    scene.add(new THREE.AmbientLight(0xffffff, 0.75));
    var key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(3, 4, 6); scene.add(key);
    var rim = new THREE.PointLight(0xff5a47, 1.2, 30); rim.position.set(-5, -2, 4); scene.add(rim);
    var fill = new THREE.PointLight(0xffd23f, 0.8, 30); fill.position.set(5, -4, 2); scene.add(fill);

    var group = new THREE.Group();
    scene.add(group);

    var knot = new THREE.Mesh(
      new THREE.TorusKnotGeometry(1.25, 0.42, 220, 36, 2, 3),
      new THREE.MeshStandardMaterial({ color: 0x5b3cff, roughness: 0.28, metalness: 0.12 })
    );
    group.add(knot);

    var ring = new THREE.Mesh(
      new THREE.TorusGeometry(2.7, 0.045, 16, 140),
      new THREE.MeshStandardMaterial({ color: 0x15112b, roughness: 0.5 })
    );
    ring.rotation.x = 1.15; ring.rotation.y = 0.35;
    group.add(ring);

    var orbiters = [];
    function orbiter(geo, color, radius, speed, phase, tilt) {
      var m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: color, roughness: 0.35, metalness: 0.05 }));
      m.userData = { radius: radius, speed: speed, phase: phase, tilt: tilt };
      group.add(m); orbiters.push(m);
    }
    orbiter(new THREE.OctahedronGeometry(0.34), 0xffd23f, 2.7, 0.55, 0.0, 1.15);
    orbiter(new THREE.SphereGeometry(0.26, 32, 32), 0xff5a47, 2.7, 0.55, 2.1, 1.15);
    orbiter(new THREE.IcosahedronGeometry(0.22), 0xffffff, 2.7, 0.55, 4.2, 1.15);
    orbiter(new THREE.BoxGeometry(0.34, 0.34, 0.34), 0x2bc48a, 3.4, -0.32, 1.0, 0.4);

    group.rotation.x = 0.25;
    var tx = group.rotation.x, ty = 0;
    if (canHover) {
      box.addEventListener('mousemove', function (e) {
        if (reduce) return;
        var r = box.getBoundingClientRect();
        ty = ((e.clientX - r.left) / r.width - 0.5) * 0.9;
        tx = 0.25 + ((e.clientY - r.top) / r.height - 0.5) * 0.6;
      });
    }

    window.addEventListener('resize', function () {
      w = box.clientWidth; h = box.clientHeight;
      if (!w || !h) return;
      camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h);
    });

    var t = 0, running = false;
    function draw() {
      t += 0.01;
      knot.rotation.y += 0.006; knot.rotation.x += 0.0025;
      orbiters.forEach(function (m) {
        var u = m.userData, a = t * u.speed * 2 + u.phase;
        var x = Math.cos(a) * u.radius, z = Math.sin(a) * u.radius;
        m.position.set(x, z * Math.sin(u.tilt) * 0.5, z * Math.cos(u.tilt));
        m.rotation.x += 0.02; m.rotation.y += 0.015;
      });
      group.rotation.x += (tx - group.rotation.x) * 0.05;
      group.rotation.y += (ty - group.rotation.y) * 0.05;
      renderer.render(scene, camera);
    }
    function loop() { if (!running) return; draw(); window.requestAnimationFrame(loop); }

    if (reduce) { draw(); return; }

    // Only animate while the hero is on screen and the tab is visible.
    var onScreen = true;
    function sync() {
      var should = onScreen && !doc.hidden;
      if (should && !running) { running = true; loop(); }
      else if (!should) { running = false; }
    }
    if (hasIO) {
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting; sync();
      }, { threshold: 0 }).observe(box);
    }
    doc.addEventListener('visibilitychange', sync);
    sync();
  })();
})();
