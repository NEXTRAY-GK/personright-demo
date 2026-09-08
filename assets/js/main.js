/* パーソンライト — 動きは最小限に。止めた絵で成立させる */
(function () {
  'use strict';
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ヘッダー：スクロールで縮む */
  var head = document.querySelector('.head');
  var toTop = document.querySelector('.toTop');
  var last = -1;
  function onScroll() {
    var y = window.scrollY;
    if (y === last) return;
    last = y;
    if (head) head.classList.toggle('is-min', y > 80);
    if (toTop) toTop.classList.toggle('is-on', y > 640);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ハンバーガー */
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.head__nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        burger.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  /* 現れる。
     ⚠️ 読み込んだ時点で画面に入っている物は、動かさずにそのまま出す。
     （アンカーで途中へ飛んだとき、そこが白いままになるのを防ぐ） */
  var rises = document.querySelectorAll('.rise');
  if (rises.length) {
    if (still || !('IntersectionObserver' in window)) {
      for (var i = 0; i < rises.length; i++) rises[i].classList.add('is-in');
    } else {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
        });
      }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
      var vh = window.innerHeight;
      rises.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < vh && r.bottom > 0) { el.classList.add('is-in', 'is-now'); }
        else { io.observe(el); }
      });
    }
  }

  /* 上へ */
  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' });
    });
  }

  /* ヒーローの気流 — 空調の会社なので、空気の流れを細い線で描く。
     動きを止める設定のときは、静止した1枚として描いて終わる。 */
  var cv = document.getElementById('air');
  if (cv && cv.getContext) {
    var cx = cv.getContext('2d');
    var W = 0, H = 0, lines = [], t = 0, raf = 0;
    function build() {
      var r = cv.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      cv.width = W * dpr; cv.height = H * dpr;
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);
      lines = [];
      var n = W < 700 ? 7 : 13;
      for (var i = 0; i < n; i++) {
        lines.push({
          y: (H / (n + 1)) * (i + 1) + (Math.random() - .5) * 26,
          amp: 12 + Math.random() * 30,
          len: .34 + Math.random() * .42,
          sp: .00016 + Math.random() * .00032,
          ph: Math.random() * Math.PI * 2,
          a: .1 + Math.random() * .26
        });
      }
    }
    function draw(now) {
      cx.clearRect(0, 0, W, H);
      cx.lineWidth = 1;
      for (var i = 0; i < lines.length; i++) {
        var l = lines[i];
        var head = ((now * l.sp + l.ph / 6) % 1.5) - .25;
        var x0 = (head - l.len) * W, x1 = head * W;
        var g = cx.createLinearGradient(x0, 0, x1, 0);
        g.addColorStop(0, 'rgba(204,187,137,0)');
        g.addColorStop(.5, 'rgba(204,187,137,' + l.a + ')');
        g.addColorStop(1, 'rgba(255,255,255,0)');
        cx.strokeStyle = g;
        cx.beginPath();
        for (var x = x0; x <= x1; x += 12) {
          var y = l.y + Math.sin(x * .0052 + l.ph + now * l.sp * 5.5) * l.amp;
          x === x0 ? cx.moveTo(x, y) : cx.lineTo(x, y);
        }
        cx.stroke();
      }
    }
    function loop(now) { t = now; draw(now); raf = requestAnimationFrame(loop); }
    build();
    if (still) { draw(1400); }
    else { raf = requestAnimationFrame(loop); }
    var rt;
    function rebuild() {
      clearTimeout(rt);
      rt = setTimeout(function () { build(); if (still) draw(1400); }, 200);
    }
    window.addEventListener('resize', rebuild);
    /* ヒーローの高さは画像が入ってから決まる。箱が変わったら組み直す */
    if ('ResizeObserver' in window) { new ResizeObserver(rebuild).observe(cv); }
    window.addEventListener('load', rebuild);
    document.addEventListener('visibilitychange', function () {
      if (still) return;
      if (document.hidden) { cancelAnimationFrame(raf); raf = 0; }
      else if (!raf) { raf = requestAnimationFrame(loop); }
    });
  }

  /* デモの断り書き（popover が無い browser のための保険） */
  var demoBtn = document.querySelector('.demo');
  var demoNote = document.getElementById('demoNote');
  if (demoBtn && demoNote && !HTMLElement.prototype.hasOwnProperty('popover')) {
    demoNote.style.display = 'none';
    demoBtn.addEventListener('click', function () {
      demoNote.style.display = demoNote.style.display === 'none' ? 'block' : 'none';
      demoNote.style.position = 'fixed';
      demoNote.style.left = '50%';
      demoNote.style.top = '50%';
      demoNote.style.transform = 'translate(-50%,-50%)';
      demoNote.style.zIndex = '90';
    });
  }
})();
