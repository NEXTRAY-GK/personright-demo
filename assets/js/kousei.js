/* パーソンライト 第4版（構成案）の動き。見た目の演出は入れていない。
   - スマホのメニュー
   - 頭の「事業紹介」の開け閉め
   - フォームの相談の種類を ?type= から選んでおく
   - デモなので、フォームは送らずに完了ページへ移る */
(function () {
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      burger.setAttribute('aria-label', open ? 'メニューを開く' : 'メニューを閉じる');
      drawer.hidden = open;
      document.documentElement.classList.toggle('is-locked', !open);
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) { burger.click(); }
    });
  }

  document.querySelectorAll('.hd__btn').forEach(function (btn) {
    var li = btn.closest('li');
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      li.classList.toggle('is-open', !open);
    });
    document.addEventListener('click', function (e) {
      if (!li.contains(e.target)) { btn.setAttribute('aria-expanded', 'false'); li.classList.remove('is-open'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { btn.setAttribute('aria-expanded', 'false'); li.classList.remove('is-open'); }
    });
  });

  document.querySelectorAll('form[data-demo]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault(); // 入れた内容は URL にも外にも出さない
      location.href = f.getAttribute('action');
    });
  });

  var type = new URLSearchParams(location.search).get('type');
  if (type) {
    document.querySelectorAll('input[name="type"]').forEach(function (r) { if (r.value === type) { r.checked = true; } });
  }
})();
