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

  /* 料金の比べ方。条件を動かすと、結果がその場で変わる */
  var yen = function (n) { return Math.round(n).toLocaleString('ja-JP') + '円'; };
  document.querySelectorAll('[data-sim]').forEach(function (sim) {
    var kind = sim.getAttribute('data-sim');
    var o = function (k) { return sim.querySelector('[data-o="' + k + '"]'); };
    var num = function (n) { var el = sim.querySelector('[name="' + n + '"]'); return el ? parseFloat(el.value) : 0; };
    var text = '';

    function paint(now, after, years) {
      var save = now - after;
      o('now').textContent = yen(now) + '/月';
      o('after').textContent = yen(after) + '/月';
      o('afterW').style.setProperty('--w', (now > 0 ? Math.max(2, after / now * 100) : 0) + '%');
      var sign = function (n) { return (Math.round(n) === 0 ? '' : n > 0 ? '−' : '＋') + yen(Math.abs(n)); };
      o('m').textContent = sign(save);
      o('y').textContent = sign(save * 12);
      o('t').textContent = sign(save * 12 * years);
      sim.classList.toggle('is-up', save < 0);
      return save;
    }

    function calc() {
      sim.querySelectorAll('.sim__range').forEach(function (r) {
        var p = (r.value - r.min) / (r.max - r.min) * 100;
        r.style.setProperty('--p', p + '%');
        var out = sim.querySelector('[data-out="' + r.name + '"]');
        if (out) { out.textContent = Number(r.value).toLocaleString('ja-JP', { maximumFractionDigits: 1, minimumFractionDigits: r.step.indexOf('.') >= 0 ? 1 : 0 }); }
      });
      if (kind === 'ac') {
        var gen = sim.querySelector('input[name="gen"]:checked');
        var ratio = 20 / parseFloat(gen.value);          // いまの冷媒 → R32（20%）
        var bill = num('bill'), years = num('years');
        o('yl').textContent = years + '年';
        var save = paint(bill, bill * ratio, years);
        o('msg').textContent = save > 0
          ? '電気代が、およそ' + Math.round((1 - ratio) * 100) + '%下がる目安です。'
          : 'いまの機種と同じ世代です。電気代はほとんど変わりません。効きが悪いときは、入れ替えの前に分解・洗浄をご相談ください。';
        text = '【電気代の比べ方で入れた条件】いまの機種：' + gen.parentNode.textContent.trim() + '／電気代：月' + yen(bill) + '／使う年数：' + years + '年';
      } else {
        var m = num('mono'), c = num('color');
        var ourM = parseFloat(sim.getAttribute('data-our-mono')), ourC = parseFloat(sim.getAttribute('data-our-color'));
        var now = m * num('pmono') + c * num('pcolor');
        var s = paint(now, m * ourM + c * ourC, 5);
        o('msg').textContent = s > 0 ? '印刷代が、これだけ下がる目安です（仮の単価で計算）。'
          : s < 0 ? 'いまの単価のほうが安い目安です。基本料金まで含めて比べるので、一度ご相談ください。' : '';
        text = '【印刷代の比べ方で入れた条件】月の枚数：モノクロ' + m.toLocaleString('ja-JP') + '枚・カラー' + c.toLocaleString('ja-JP') + '枚／いまの単価：モノクロ' + num('pmono') + '円・カラー' + num('pcolor') + '円';
      }
    }
    sim.addEventListener('input', calc);
    sim.addEventListener('change', calc);
    calc();

    /* 「この条件で見積りを頼む」… フォームに相談の種類と条件を入れておく */
    sim.querySelectorAll('[data-type]').forEach(function (go) {
      go.addEventListener('click', function () {
        var t = go.getAttribute('data-type');
        document.querySelectorAll('input[name="type"]').forEach(function (r) { r.checked = r.value === t; });
        var body = document.querySelector('.form textarea[name="body"]');
        if (!body) { return; }
        // 前に入れた条件の行だけを差し替え、ご本人が書いた文は残す
        body.value = body.value.indexOf('【') === 0 ? text + body.value.replace(/^【[^\n]*/, '') : text + (body.value ? '\n' + body.value : '');
      });
    });
  });

  var type = new URLSearchParams(location.search).get('type');
  if (type) {
    document.querySelectorAll('input[name="type"]').forEach(function (r) { if (r.value === type) { r.checked = true; } });
  }
})();
