/* ==========================================================================
   株式会社パーソンライト — 動き
   ⚠️ 動かすのは 頭・引き出し・現れ方 の3つだけ。ほかは CSS に持たせる。
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
      burger.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        burger.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'メニューを開く');
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
