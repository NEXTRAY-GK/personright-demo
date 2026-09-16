/* ==========================================================================
   株式会社パーソンライト — 動き（第3版 2026-09-16）
   スクロールに連動する物は、1本の rAF でまとめて更新する。
     ・冷えていく部屋（トップの冒頭。canvas にサーモ画像を描く）
     ・冷媒の電気代メーター（トップ）
     ・横に流れる現場の写真（トップ）
     ・サーモ画像 → 実写（[data-scan]）
     ・夜間カメラの見比べ（通信機器）
     ・頭の読み出し（室温）と足の帯
   ⚠️ 動きを減らす設定でも、スクロールに連動する変化は残す（読む人の手で動くため）。
      止めるのは、勝手に動き続ける物（陽炎のゆらぎ・気流の粒の自走）だけ。
   ========================================================================== */
(function () {
  'use strict';
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var doc = document.documentElement;
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var ease = function (t) { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); };
  var band = function (p, a, b) { return clamp((p - a) / (b - a), 0, 1); };
  var vh = window.innerHeight, vw = window.innerWidth;

  /* 区間の進み具合（要素の頭が画面の頭に来たら0、尻が画面の尻に来たら1） */
  function pinProgress(el) {
    var r = el.getBoundingClientRect();
    var run = r.height - vh;
    return run > 0 ? clamp(-r.top / run, 0, 1) : (r.top < 0 ? 1 : 0);
  }

  /* ------------------------------------------------ 温度 → 色（ironbow） */
  var STOPS = [
    [0, 10, 12, 38], [.16, 26, 31, 110], [.34, 91, 26, 143], [.5, 179, 25, 92],
    [.66, 239, 90, 43], [.84, 251, 177, 60], [1, 255, 241, 191]
  ];
  var LUT = new Uint8ClampedArray(256 * 3);
  (function () {
    for (var i = 0; i < 256; i++) {
      var t = i / 255, k = 0;
      while (k < STOPS.length - 2 && t > STOPS[k + 1][0]) k++;
      var a = STOPS[k], b = STOPS[k + 1], u = (t - a[0]) / (b[0] - a[0]);
      LUT[i * 3] = lerp(a[1], b[1], u); LUT[i * 3 + 1] = lerp(a[2], b[2], u); LUT[i * 3 + 2] = lerp(a[3], b[3], u);
    }
  })();
  var T_MIN = 22, T_MAX = 36;
  function tColor(T) {
    var i = Math.round(clamp((T - T_MIN) / (T_MAX - T_MIN), 0, 1) * 255) * 3;
    return 'rgb(' + LUT[i] + ',' + LUT[i + 1] + ',' + LUT[i + 2] + ')';
  }

  /* ================================================================ 頭 */
  var head = document.querySelector('.head');
  var rdV = document.querySelector('.rd__v');
  var rdDot = document.querySelector('.rd__dot');
  var bar = document.querySelector('.bar');
  var darkSecs = [].slice.call(document.querySelectorAll('.tm, .mt, .reel, .nv, .sec--ink, .cta, .foot'));
  var roomTemp = null; /* トップの冒頭が温度を持っているあいだは、そちらを出す */
  var shownTemp = -1;

  function updHead(y) {
    if (!head) return;
    head.classList.toggle('is-min', y > 40);
    var probe = (head.offsetHeight || 64) / 2, dark = false;
    for (var i = 0; i < darkSecs.length; i++) {
      var r = darkSecs[i].getBoundingClientRect();
      if (r.top <= probe && r.bottom > probe) { dark = true; break; }
    }
    head.classList.toggle('is-dark', dark);

    var max = Math.max(1, doc.scrollHeight - vh);
    var p = clamp(y / max, 0, 1);
    if (bar) bar.style.setProperty('--p', p.toFixed(4));
    /* トップは冒頭で冷えきった温度から、ほかのページは読み始めの暑さから下げる */
    var T = roomTemp != null ? roomTemp : (tm ? lerp(24.6, 23.8, ease(p)) : lerp(31.6, 24.2, ease(p)));
    T = Math.round(T * 10) / 10;
    if (rdV && T !== shownTemp) {
      shownTemp = T;
      rdV.textContent = T.toFixed(1);
      if (rdDot) rdDot.style.setProperty('--rd-c', tColor(T));
    }
  }

  /* ======================================================== 引き出し */
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');
  if (burger && drawer) {
    var setNav = function (open) {
      drawer.hidden = !open;
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      doc.classList.toggle('is-nav', open);
      document.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', function () { setNav(drawer.hidden); });
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !drawer.hidden) { setNav(false); burger.focus(); }
    });
    var wide = window.matchMedia('(min-width:1181px)');
    var onWide = function (e) { if (e.matches && !drawer.hidden) setNav(false); };
    if (wide.addEventListener) wide.addEventListener('change', onWide); else if (wide.addListener) wide.addListener(onWide);
  }

  /* ========================================================== 現れる */
  var rises = document.querySelectorAll('.rise, .gen');
  if (!('IntersectionObserver' in window)) {
    for (var i = 0; i < rises.length; i++) rises[i].classList.add('is-in');
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); countUp(e.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
    rises.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh && r.bottom > 0) { el.classList.add('is-in', 'is-now'); }
      else io.observe(el);
    });
  }

  /* 数字が読み上がる（動きを減らす設定なら、最後の数字をそのまま出す） */
  function countUp(root) {
    if (still) return;
    var els = root.querySelectorAll('.count');
    [].forEach.call(els, function (el) {
      var to = +el.getAttribute('data-to'), t0 = null;
      var step = function (ts) {
        if (t0 == null) t0 = ts;
        var k = clamp((ts - t0) / 1400, 0, 1);
        el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      };
      el.textContent = '0';
      requestAnimationFrame(step);
    });
  }

  /* ============================================ サーモ画像 → 実写（スクロール） */
  var scans = [].slice.call(document.querySelectorAll('[data-scan]')).filter(function (el) { return !el.closest('.reel'); });
  function updScans() {
    for (var i = 0; i < scans.length; i++) {
      var r = scans[i].getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) continue;
      /* 写真の頭が画面の下から入って、真ん中を過ぎるまでに戻しきる */
      var k = clamp((vh * 0.92 - r.top) / (vh * 0.62), 0, 1);
      scans[i].style.setProperty('--k', ease(k).toFixed(3));
    }
  }

  /* ================================================== 冷媒のメーター */
  var mt = document.querySelector('.mt');
  var mtParts = mt && {
    v: mt.querySelector('.mt__v'), bar: mt.querySelector('.mt__bar i'),
    gen: mt.querySelector('.mt__gen'), era: mt.querySelector('.mt__era'),
    steps: mt.querySelectorAll('.mt__steps li')
  };
  var GENS = [['R22（指定フロン）', '2001年以前'], ['R407・R410（代替フロン）', '2001年〜2013年'], ['R32（代替えフロン）', '2014年以降']];
  var mtLast = -1;
  function updMeter() {
    if (!mt) return;
    var r = mt.getBoundingClientRect();
    if (r.bottom < 0 || r.top > vh) return;
    var p = pinProgress(mt);
    /* 0–.16 止まる／.16–.4 100→60／.4–.58 止まる／.58–.82 60→20／.82– 止まる */
    var v = 100 - 40 * ease(band(p, .16, .4)) - 40 * ease(band(p, .58, .82));
    var g = p < .28 ? 0 : p < .7 ? 1 : 2;
    var vi = Math.round(v);
    if (vi === mtLast) return;
    mtLast = vi;
    mtParts.v.textContent = vi;
    mtParts.bar.style.setProperty('--w', v.toFixed(1));
    var c = tColor(lerp(24, 34.5, (v - 20) / 80));
    mtParts.bar.style.setProperty('--bar-c', c);
    mtParts.gen.textContent = GENS[g][0];
    mtParts.era.textContent = GENS[g][1];
    for (var i = 0; i < mtParts.steps.length; i++) mtParts.steps[i].classList.toggle('is-on', i === g);
  }

  /* ================================================== 横に流れる現場 */
  var reel = document.querySelector('.reel');
  var reelTrack = reel && reel.querySelector('.reel__track');
  var reelScans = reel ? [].slice.call(reel.querySelectorAll('[data-scan]')) : [];
  var reelRun = 0;
  function sizeReel() {
    if (!reel) return;
    reelTrack.style.transform = '';
    reelRun = Math.max(0, reelTrack.scrollWidth - vw);
    reel.style.height = (reelRun + vh) + 'px';
  }
  function updReel() {
    if (!reel) return;
    var r = reel.getBoundingClientRect();
    if (r.bottom < 0 || r.top > vh) return;
    var p = pinProgress(reel);
    reelTrack.style.transform = 'translate3d(' + (-reelRun * p).toFixed(1) + 'px,0,0)';
    for (var i = 0; i < reelScans.length; i++) {
      var q = reelScans[i].getBoundingClientRect();
      var k = clamp((vw * 0.96 - q.left) / (Math.min(q.width, vw) * 1.1), 0, 1);
      reelScans[i].style.setProperty('--k', ease(k).toFixed(3));
    }
  }

  /* ================================================== 夜間カメラの見比べ */
  var nv = document.querySelector('.nv');
  var nvLast = -1;
  function updNv() {
    if (!nv) return;
    var r = nv.getBoundingClientRect();
    if (r.bottom < 0 || r.top > vh) return;
    var p = pinProgress(nv);
    var g = p < .33 ? 0 : p < .66 ? 1 : 2;
    if (g === nvLast) return;
    nvLast = g;
    [].forEach.call(nv.querySelectorAll('[data-nv]'), function (el) {
      el.classList.toggle('is-on', +el.getAttribute('data-nv') === g);
    });
  }

  /* ================================================ 冷えていく部屋（冒頭） */
  var tm = document.querySelector('.tm');
  var room = null;
  if (tm) room = makeRoom(tm);

  function makeRoom(sec) {
    var cv = sec.querySelector('.tm__cv');
    var ctx = cv.getContext('2d');
    if (!ctx) return null;
    var steps = [].slice.call(sec.querySelectorAll('.tm__s'));
    var vEl = sec.querySelector('.tm__v');
    var mark = sec.querySelector('.tm__scale em');
    var sps = [].slice.call(sec.querySelectorAll('.tm__sp b'));
    var off = document.createElement('canvas');
    var octx = off.getContext('2d');
    var img = null, gw = 0, gh = 0, field = null;
    var W = 0, H = 0, dpr = 1, rx = 0, ry = 0, rw = 0, rh = 0, narrow = false;
    var P = 0, time = 0, running = false, visible = true;

    /* 気流の粒 … 左右の吹き出し（j）と、中央を上がる戻り（r） */
    var parts = [];
    for (var i = 0; i < 150; i++) {
      var kind = i < 110 ? (i % 2 ? 'L' : 'R') : 'U';
      parts.push({ k: kind, s: Math.random(), o: (Math.random() - .5), sp: .7 + Math.random() * .6 });
    }

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 1.75);
      W = cv.clientWidth || window.innerWidth; H = cv.clientHeight || window.innerHeight;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      narrow = W < 900;
      if (narrow) {
        rx = W * 0.05; rw = W * 0.9;
        ry = H * 0.53; rh = H * 0.33;
      } else {
        rx = W * 0.45; rw = W * 0.52;
        ry = H * 0.14; rh = H * 0.58;
      }
      gw = 110; gh = Math.max(40, Math.min(150, (Math.round(gw * rh / rw) || 70)));
      off.width = gw; off.height = gh;
      img = octx.createImageData(gw, gh);
      field = new Float32Array(gw * gh);
    }

    var g2 = function (x, y, sx, sy) { return Math.exp(-(x * x) / (2 * sx * sx) - (y * y) / (2 * sy * sy)); };
    var CEIL = 0.2, CX = 0.5;

    /* 点と2次ベジエの近さ（粗く10分割） */
    function jetDist(u, v, side) {
      var x0 = CX + side * 0.07, y0 = CEIL + 0.03, x1 = CX + side * 0.22, y1 = CEIL + 0.08, x2 = CX + side * 0.4, y2 = 0.88;
      var best = 9, bt = 0;
      for (var i = 0; i <= 32; i++) {
        var t = i / 32, a = (1 - t) * (1 - t), b = 2 * (1 - t) * t, c = t * t;
        var px = a * x0 + b * x1 + c * x2, py = a * y0 + b * y1 + c * y2;
        var d = (u - px) * (u - px) + (v - py) * (v - py);
        if (d < best) { best = d; bt = t; }
      }
      return [best, bt];
    }

    function temp(u, v, p, t) {
      var hot = 30.4 + 4.2 * (1 - v);
      if (v < CEIL) hot += 1.6;
      hot += 4.2 * g2(u - 1, v - 0.52, 0.07, 0.17);                         // 窓
      hot += 2.4 * (g2(u - 0.2, v - 0.8, 0.06, 0.04) + g2(u - 0.8, v - 0.8, 0.06, 0.04)); // 机の上の機器
      var ppl = g2(u - 0.3, v - 0.68, 0.03, 0.11) + g2(u - 0.68, v - 0.68, 0.03, 0.11);
      hot += 3 * ppl;                                                          // 人
      if (t) hot += 0.45 * Math.sin(u * 14 + t * 1.1) * Math.sin(v * 10 - t * 0.7);
      if (v < CEIL) return hot;                                                // 天井裏は冷えない

      var on = band(p, 0.22, 0.34);
      var reach = ease(band(p, 0.46, 0.9));
      var dx = (u - CX) / 1.05, dy = (v - CEIL) / 0.8;
      var d = Math.sqrt(dx * dx + dy * dy);
      var c = clamp((reach * 1.25 - d) / 0.28, 0, 1);
      c = c * c * (3 - 2 * c);
      var cool = 24.1 + 0.9 * v + 0.9 * ppl + 0.6 * g2(u - 1, v - 0.52, 0.07, 0.17);
      var T = lerp(hot, cool, c);

      T -= 5.5 * on * (1 - c * 0.7) * g2(u - CX, v - CEIL - 0.03, 0.09, 0.035);   // 吹き出し口
      var jp = band(p, 0.34, 0.5) * (1 - band(p, 0.82, 1) * 0.6);
      if (jp > 0) {
        for (var s = -1; s <= 1; s += 2) {
          var jd = jetDist(u, v, s);
          T -= 7.5 * jp * Math.exp(-jd[0] / 0.0022) * (1 - jd[1] * 0.55) * (1 - c * 0.6);
        }
      }
      var rp = band(p, 0.5, 0.66) * (1 - band(p, 0.9, 1) * 0.5);
      if (rp > 0 && v > CEIL + 0.06) T += 2.2 * rp * Math.exp(-((u - CX) * (u - CX)) / 0.0016) * ((v - CEIL) / 0.8) * (1 - c * 0.45);
      return T;
    }

    function computeField(p, t) {
      var data = img.data, sum = 0, n = 0;
      for (var j = 0; j < gh; j++) {
        var v = j / (gh - 1);
        for (var i = 0; i < gw; i++) {
          var u = i / (gw - 1);
          var T = temp(u, v, p, t);
          field[j * gw + i] = T;
          if (v > 0.45) { sum += T; n++; }
          var li = Math.round(clamp((T - T_MIN) / (T_MAX - T_MIN), 0, 1) * 255) * 3, o = (j * gw + i) * 4;
          data[o] = LUT[li]; data[o + 1] = LUT[li + 1]; data[o + 2] = LUT[li + 2]; data[o + 3] = 255;
        }
      }
      octx.putImageData(img, 0, 0);
      return sum / n;
    }
    function at(u, v) {
      var i = Math.round(clamp(u, 0, 1) * (gw - 1)), j = Math.round(clamp(v, 0, 1) * (gh - 1));
      return field[j * gw + i];
    }

    /* 図の中の札 … 明るい色の上でも読めるよう、暗い下敷きを敷く */
    function tag(s, x, y) {
      var w = ctx.measureText(s).width;
      ctx.fillStyle = 'rgba(11,14,16,.74)';
      ctx.fillRect(x - 5, y - 9, w + 10, 18);
      ctx.fillStyle = '#fff';
      ctx.fillText(s, x, y + 1);
    }
    function X(u) { return rx + u * rw; }
    function Y(v) { return ry + v * rh; }

    function draw() {
      var p = P, t = still ? 0 : time;
      var avg = computeField(p, t);

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      /* 地の方眼 */
      ctx.strokeStyle = 'rgba(236,234,228,.045)'; ctx.lineWidth = 1;
      var step = 48;
      ctx.beginPath();
      for (var gx = (W % step) / 2; gx < W; gx += step) { ctx.moveTo(gx + .5, 0); ctx.lineTo(gx + .5, H); }
      for (var gy = 0; gy < H; gy += step) { ctx.moveTo(0, gy + .5); ctx.lineTo(W, gy + .5); }
      ctx.stroke();

      /* サーモ画像 */
      ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(off, rx, ry, rw, rh);

      /* 走査線 */
      ctx.fillStyle = 'rgba(0,0,0,.08)';
      for (var sl = ry; sl < ry + rh; sl += 3) ctx.fillRect(rx, sl, rw, 1);

      ctx.lineWidth = 1;
      ctx.strokeStyle = 'rgba(255,255,255,.55)';
      ctx.strokeRect(rx + .5, ry + .5, rw - 1, rh - 1);
      /* 天井 */
      ctx.setLineDash([4, 5]);
      ctx.beginPath(); ctx.moveTo(rx, Y(CEIL)); ctx.lineTo(rx + rw, Y(CEIL)); ctx.stroke();
      ctx.setLineDash([]);

      ctx.font = '500 11px "JetBrains Mono", "Zen Kaku Gothic New", monospace';
      ctx.textBaseline = 'middle';
      tag('天井裏', X(0.012), Y(CEIL / 2));
      tag('室内', X(0.012), Y(CEIL) + 16);

      /* 窓 */
      ctx.strokeStyle = 'rgba(255,255,255,.6)';
      ctx.strokeRect(X(0.985), Y(0.36), rw * 0.015, rh * 0.32);

      /* 机と人 */
      ctx.strokeStyle = 'rgba(255,255,255,.62)'; ctx.lineWidth = 1.2;
      [[0.12, 0.28], [0.72, 0.88]].forEach(function (d) {
        ctx.beginPath(); ctx.moveTo(X(d[0]), Y(0.84)); ctx.lineTo(X(d[1]), Y(0.84));
        ctx.moveTo(X(d[0] + 0.01), Y(0.84)); ctx.lineTo(X(d[0] + 0.01), Y(1));
        ctx.moveTo(X(d[1] - 0.01), Y(0.84)); ctx.lineTo(X(d[1] - 0.01), Y(1)); ctx.stroke();
        ctx.strokeRect(X((d[0] + d[1]) / 2 - 0.03), Y(0.76), rw * 0.06, rh * 0.065);
      });
      [0.3, 0.68].forEach(function (pu) {
        var hr = Math.max(5, rh * 0.03);
        ctx.beginPath(); ctx.arc(X(pu), Y(0.53), hr, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(X(pu) - hr * 1.5, Y(0.84)); ctx.lineTo(X(pu) - hr * 1.3, Y(0.6));
        ctx.quadraticCurveTo(X(pu), Y(0.57), X(pu) + hr * 1.3, Y(0.6)); ctx.lineTo(X(pu) + hr * 1.5, Y(0.84));
        ctx.stroke();
      });

      /* 室内機と配管（選ぶ段から現れる） */
      var a1 = ease(band(p, 0.18, 0.3));
      if (a1 > 0) {
        ctx.globalAlpha = a1;
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.6;
        var uw = rw * 0.17, uh = Math.max(8, rh * 0.035);
        ctx.strokeRect(X(CX) - uw / 2, Y(CEIL) - 1, uw, uh);
        ctx.beginPath();
        ctx.moveTo(X(CX) - uw / 2 + 6, Y(CEIL) + uh + 4); ctx.lineTo(X(CX) - uw / 2 + uw * 0.3, Y(CEIL) + uh + 4);
        ctx.moveTo(X(CX) + uw / 2 - 6, Y(CEIL) + uh + 4); ctx.lineTo(X(CX) + uw / 2 - uw * 0.3, Y(CEIL) + uh + 4);
        ctx.stroke();
        ctx.lineWidth = 1.2; ctx.setLineDash([2, 3]);
        ctx.beginPath(); ctx.moveTo(X(CX) + uw / 2, Y(CEIL * 0.55)); ctx.lineTo(X(1), Y(CEIL * 0.55)); ctx.stroke();
        ctx.setLineDash([]);
        tag('冷媒配管 → 室外機', X(CX) + uw / 2 + 10, Y(CEIL * 0.55) - 12);
        tag('天井カセット形', X(CX) - uw / 2, Y(CEIL) + uh + 22);
        ctx.globalAlpha = 1;
      }

      /* 気流の粒 */
      var jv = band(p, 0.32, 0.46) * (1 - band(p, 0.94, 1) * 0.5);
      var rv = band(p, 0.5, 0.64) * (1 - band(p, 0.94, 1) * 0.5);
      if (jv > 0 || rv > 0) {
        ctx.lineCap = 'round';
        for (var q = 0; q < parts.length; q++) {
          var pt = parts[q];
          var vis = pt.k === 'U' ? rv : jv;
          if (vis <= 0) continue;
          var s = (pt.s + p * 2.4 * pt.sp + t * 0.06 * pt.sp) % 1;
          var fade = Math.sin(Math.PI * s);
          var x, y, x2, y2;
          if (pt.k === 'U') {
            var vv = 0.95 - s * 0.68;
            x = X(CX + pt.o * 0.05 + Math.sin(s * 6 + pt.o * 9) * 0.01); y = Y(vv);
            x2 = x; y2 = y + rh * 0.03;
            ctx.strokeStyle = 'rgba(255,214,140,' + (0.75 * fade * vis) + ')';
          } else {
            var sd = pt.k === 'L' ? -1 : 1;
            var bez = function (tt) {
              var o = pt.o * 0.08 * tt;
              var x0 = CX + sd * 0.07, y0 = CEIL + 0.03, xa = CX + sd * 0.22, ya = CEIL + 0.08, xb = CX + sd * (0.4 + o), yb = 0.88;
              var a = (1 - tt) * (1 - tt), b = 2 * (1 - tt) * tt, c = tt * tt;
              return [X(a * x0 + b * xa + c * xb), Y(a * y0 + b * ya + c * yb)];
            };
            var p1 = bez(s), p0 = bez(Math.max(0, s - 0.04));
            x = p1[0]; y = p1[1]; x2 = p0[0]; y2 = p0[1];
            ctx.strokeStyle = 'rgba(190,235,255,' + (0.85 * fade * vis) + ')';
          }
          ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x2, y2); ctx.stroke();
        }
      }

      /* 計測点 */
      var SP = [[0.93, 0.5], [0.5, 0.8], [0.08, 0.96]];
      ctx.lineWidth = 1; ctx.strokeStyle = '#fff'; ctx.fillStyle = '#fff';
      for (var k = 0; k < SP.length; k++) {
        var cx = X(SP[k][0]), cy = Y(SP[k][1]), T = at(SP[k][0], SP[k][1]);
        ctx.beginPath();
        ctx.moveTo(cx - 9, cy); ctx.lineTo(cx - 3, cy); ctx.moveTo(cx + 3, cy); ctx.lineTo(cx + 9, cy);
        ctx.moveTo(cx, cy - 9); ctx.lineTo(cx, cy - 3); ctx.moveTo(cx, cy + 3); ctx.lineTo(cx, cy + 9);
        ctx.stroke();
        var lab = 'SP' + (k + 1) + ' ' + T.toFixed(1) + '°';
        var lx = SP[k][0] > 0.7 ? cx - 20 - ctx.measureText(lab).width : cx + 14;
        tag(lab, lx, cy - 14);
        ctx.strokeStyle = '#fff';
        if (sps[k]) sps[k].textContent = T.toFixed(1);
      }

      /* 読み出し */
      var shown = Math.round(avg * 10) / 10;
      if (vEl) vEl.textContent = shown.toFixed(1);
      if (mark) mark.style.setProperty('--t', (clamp((avg - T_MIN) / (T_MAX - T_MIN), 0, 1) * 100).toFixed(1) + '%');
      return shown;
    }

    function stepsUpdate(p) {
      /* 段の境目 */
      var B = [[-1, 0, 0.16, 0.22], [0.2, 0.26, 0.42, 0.48], [0.46, 0.52, 0.66, 0.72], [0.7, 0.76, 2, 2]];
      for (var i = 0; i < steps.length; i++) {
        var b = B[i];
        var o = p < b[1] ? band(p, b[0], b[1]) : 1 - band(p, b[2], b[3]);
        var y = p < b[1] ? (1 - o) * 24 : -(1 - o) * 24;
        steps[i].style.opacity = o.toFixed(3);
        steps[i].style.transform = (narrow ? 'translateY(' : 'translateY(calc(-50% + ') + y.toFixed(1) + 'px' + (narrow ? ')' : '))');
        steps[i].classList.toggle('is-on', o > 0.02);
      }
      sec.classList.toggle('is-past-0', p > 0.04);
    }

    function frame(ts) {
      running = false;
      time = ts / 1000;
      var T = draw();
      stepsUpdate(P);
      var r = sec.getBoundingClientRect();
      roomTemp = r.bottom > vh * 0.5 ? T : null;
      updHead(window.scrollY || window.pageYOffset);
      if (visible && !still) loop();
    }
    function loop() { if (!running) { running = true; requestAnimationFrame(frame); } }

    var api = {
      resize: function () { size(); api.scroll(); },
      scroll: function () {
        var r = sec.getBoundingClientRect();
        visible = r.bottom > 0 && r.top < vh;
        if (!visible) { roomTemp = null; return; }
        P = pinProgress(sec);
        loop();
      }
    };
    size();
    return api;
  }

  /* 目次の今いる所（業務用エアコン） */
  var tocLinks = [].slice.call(document.querySelectorAll('.toc a'));
  function updToc() {
    if (!tocLinks.length) return;
    var cur = null;
    for (var i = 0; i < tocLinks.length; i++) {
      var t = document.querySelector(tocLinks[i].getAttribute('href'));
      if (t && t.getBoundingClientRect().top < vh * 0.4) cur = tocLinks[i];
    }
    tocLinks.forEach(function (a) { a.classList.toggle('is-on', a === cur); });
  }

  /* ====================================================== まとめて回す */
  var ticking = false;
  function tick() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    if (room) room.scroll();
    updMeter(); updReel(); updScans(); updNv(); updToc();
    updHead(y);
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(tick); } }
  function onResize() {
    vh = window.innerHeight; vw = window.innerWidth;
    sizeReel(); if (room) room.resize(); mtLast = -1; nvLast = -1;
    tick();
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  var rzT;
  window.addEventListener('resize', function () {
    /* スマホで上下の帯が出入りするたびに組み直さない（幅が変わったときだけ） */
    if (window.innerWidth === vw && Math.abs(window.innerHeight - vh) < 120) return;
    clearTimeout(rzT); rzT = setTimeout(onResize, 120);
  });
  sizeReel();
  tick();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { sizeReel(); tick(); });
  window.addEventListener('load', function () { sizeReel(); tick(); });

  /* --------------------------------------------- デモの断り書き（保険） */
  var demoBtn = document.querySelector('.demo');
  var demoNote = document.getElementById('demoNote');
  if (demoBtn && demoNote && !HTMLElement.prototype.hasOwnProperty('popover')) {
    demoNote.style.display = 'none';
    demoBtn.addEventListener('click', function () {
      var open = demoNote.style.display === 'none';
      demoNote.style.display = open ? 'block' : 'none';
      demoNote.style.position = 'fixed';
      demoNote.style.left = '50%';
      demoNote.style.top = '50%';
      demoNote.style.transform = 'translate(-50%,-50%)';
      demoNote.style.zIndex = '90';
    });
  }
})();
