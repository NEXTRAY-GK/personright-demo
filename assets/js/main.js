/* ==========================================================================
   株式会社パーソンライト — 動き
   足すのは1画面に1つまで。止める設定のときは、静止した1枚として成立させる。
   ========================================================================== */
(function () {
  'use strict';
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- 頭 */
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

  /* ------------------------------------------------------- ハンバーガー */
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
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) burger.click();
    });
  }

  /* -------------------------------------------------------------- 現れる
     ⚠️ 読み込んだ時点で画面に入っている物は動かさずに出す。
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

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' });
    });
  }

  /* ==========================================================================
     等温線 — このサイトの署名

     空調は、目に見えない空気を設計する仕事。
     だから冒頭には、部屋の温度分布そのものを描く。

     やっていること：
       1. ゆっくり動く熱源をいくつか置いて、格子の各点の「温度」を出す
       2. marching squares で、同じ温度の点をつないだ線（等温線）を引く
       3. 冷たい線は青緑、温かい線は銅色。温度そのものが色になる
     粒子を飛ばすのではなく線を引くのは、止めた1枚で成立させるため。
     ========================================================================== */
  var cv = document.getElementById('air');
  if (cv && cv.getContext) {
    var cx = cv.getContext('2d');
    var W = 0, H = 0, cols = 0, rows = 0, cw = 0, ch = 0;
    var grid = null, srcs = [], raf = 0, t0 = 0, lastDraw = 0;

    /* 等温線の高さ。細かく刻んで、地形図のように読ませる */
    var LEVELS = [0.10, 0.16, 0.22, 0.28, 0.35, 0.42, 0.49, 0.57, 0.65, 0.73, 0.82, 0.91, 1.00];

    /* 冷 #2f7275 → 温 #b8663a。値をそのまま色にする */
    function tint(v, a) {
      var c1 = [58, 122, 124], c2 = [216, 152, 96];
      var k = Math.pow(Math.min(Math.max(v, 0), 1), 0.85);
      return 'rgba(' +
        Math.round(c1[0] + (c2[0] - c1[0]) * k) + ',' +
        Math.round(c1[1] + (c2[1] - c1[1]) * k) + ',' +
        Math.round(c1[2] + (c2[2] - c1[2]) * k) + ',' + a + ')';
    }

    function build() {
      var r = cv.getBoundingClientRect();
      if (!r.width || !r.height) return false;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      cv.width = Math.round(W * dpr);
      cv.height = Math.round(H * dpr);
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);

      /* 格子は粗くてよい。線は補間で滑らかになる */
      var step = W < 700 ? 15 : 19;
      cols = Math.max(12, Math.ceil(W / step));
      rows = Math.max(10, Math.ceil(H / step));
      cw = W / cols; ch = H / rows;
      grid = new Float32Array((cols + 1) * (rows + 1));

      /* 熱源。1つは冷たい吹き出し（負）にして、流れの向きを作る */
      srcs = [
        { x: .22, y: .40, r: .40, w:  1.00, ax: .085, ay: .050, sx: .000041, sy: .000063, px: 0.0, py: 1.9 },
        { x: .68, y: .30, r: .34, w:  0.78, ax: .105, ay: .075, sx: .000029, sy: .000047, px: 2.1, py: 0.4 },
        { x: .50, y: .78, r: .46, w:  0.62, ax: .130, ay: .045, sx: .000023, sy: .000071, px: 4.0, py: 3.1 },
        { x: .88, y: .66, r: .30, w: -0.52, ax: .070, ay: .090, sx: .000037, sy: .000031, px: 1.2, py: 5.2 }
      ];
      return true;
    }

    function field(now) {
      var ar = W / (H || 1), i, j, k = 0;
      /* 熱源の今の位置 */
      var sx = [], sy = [], sr = [], sw = [];
      for (i = 0; i < srcs.length; i++) {
        var s = srcs[i];
        sx.push(s.x + Math.sin(now * s.sx + s.px) * s.ax);
        sy.push(s.y + Math.cos(now * s.sy + s.py) * s.ay);
        sr.push(s.r * s.r);
        sw.push(s.w);
      }
      for (j = 0; j <= rows; j++) {
        var v = j / rows;
        for (i = 0; i <= cols; i++) {
          var u = i / cols, sum = 0;
          for (var m = 0; m < sx.length; m++) {
            var dx = (u - sx[m]) * ar, dy = v - sy[m];
            sum += sw[m] * Math.exp(-(dx * dx + dy * dy) / sr[m]);
          }
          /* 下ほど暖かい（暖気は上へ、という当たり前を絵にする） */
          grid[k++] = sum + v * 0.30;
        }
      }
    }

    function at(i, j) { return grid[j * (cols + 1) + i]; }
    /* 2点の間で、ちょうど閾値になる位置を求める */
    function ip(a, b, lv) { var d = b - a; return d === 0 ? 0.5 : (lv - a) / d; }

    function contour(lv) {
      cx.beginPath();
      for (var j = 0; j < rows; j++) {
        for (var i = 0; i < cols; i++) {
          var tl = at(i, j), tr = at(i + 1, j), br = at(i + 1, j + 1), bl = at(i, j + 1);
          var idx = (tl > lv ? 8 : 0) | (tr > lv ? 4 : 0) | (br > lv ? 2 : 0) | (bl > lv ? 1 : 0);
          if (idx === 0 || idx === 15) continue;
          var x = i * cw, y = j * ch;
          var T = { x: x + cw * ip(tl, tr, lv), y: y };
          var R = { x: x + cw,                  y: y + ch * ip(tr, br, lv) };
          var B = { x: x + cw * ip(bl, br, lv), y: y + ch };
          var L = { x: x,                       y: y + ch * ip(tl, bl, lv) };
          var seg = null;
          switch (idx) {
            case 1: case 14: seg = [L, B]; break;
            case 2: case 13: seg = [B, R]; break;
            case 3: case 12: seg = [L, R]; break;
            case 4: case 11: seg = [T, R]; break;
            case 6: case  9: seg = [T, B]; break;
            case 7: case  8: seg = [L, T]; break;
            case 5: cx.moveTo(L.x, L.y); cx.lineTo(T.x, T.y);
                    cx.moveTo(B.x, B.y); cx.lineTo(R.x, R.y); break;
            case 10: cx.moveTo(L.x, L.y); cx.lineTo(B.x, B.y);
                     cx.moveTo(T.x, T.y); cx.lineTo(R.x, R.y); break;
          }
          if (seg) { cx.moveTo(seg[0].x, seg[0].y); cx.lineTo(seg[1].x, seg[1].y); }
        }
      }
      cx.stroke();
    }

    function draw(now) {
      if (!grid) return;
      field(now);
      cx.clearRect(0, 0, W, H);
      cx.lineCap = 'round';
      for (var n = 0; n < LEVELS.length; n++) {
        var lv = LEVELS[n];
        var v = n / (LEVELS.length - 1);
        /* 内側（温かい側）ほど濃く、太く */
        cx.lineWidth = 0.6 + v * 0.7;
        cx.strokeStyle = tint(v, 0.10 + v * 0.26);
        contour(lv);
      }
    }

    function loop(now) {
      raf = requestAnimationFrame(loop);
      if (now - lastDraw < 33) return;   /* 30fps で足りる。線はゆっくり動く */
      lastDraw = now;
      draw(t0 + now);
    }

    function start() {
      if (!build()) return;
      if (still) { draw(9000); }         /* 止める設定 … 良い一枚を描いて終わり */
      else if (!raf) { raf = requestAnimationFrame(loop); }
    }

    t0 = 9000;                            /* 最初から絵になっている位相から始める */
    start();

    var rt;
    function rebuild() {
      clearTimeout(rt);
      rt = setTimeout(function () { if (build() && still) draw(9000); }, 180);
    }
    window.addEventListener('resize', rebuild);
    window.addEventListener('load', rebuild);
    if ('ResizeObserver' in window) { new ResizeObserver(rebuild).observe(cv); }
    document.addEventListener('visibilitychange', function () {
      if (still) return;
      if (document.hidden) { cancelAnimationFrame(raf); raf = 0; }
      else if (!raf) { raf = requestAnimationFrame(loop); }
    });
  }

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
