# -*- coding: utf-8 -*-
"""施工実績 /works/（2026-09-16 足した）

   旧サイトの「施工実績」は、トップに埋め込んだ Instagram の6件（2025年12月2日〜12日）だった。
   投稿の本文は6件とも同じ定型文なので、各現場の説明は写真に写っている物だけから書いた。
   写真は旧サイトが WordPress の中に控えていた物（素材/旧サイト画像/instagram_2025-12/）。

   仕掛け … 散らばった写真が並ぶ冒頭／12月の暦が点く／現場の記録（サーモ→実写・写っている物に印）
            ／絞り込み（並び替えの動き）／汚れが流れていく洗浄の図／入れ替えで新しくなる所の図
            ／Instagram の名前が流れる帯
"""
from common import head, header, footer, jsonld, sh, INSTA

TITLE = "施工実績｜株式会社パーソンライト"
DESC = "業務用エアコンの入れ替え工事と高圧分解洗浄の現場写真です。天井カセット形・天井吊形・室外機・リモコンまで、写真に写っている物を一件ずつご紹介します。福島県郡山市の株式会社パーソンライト。"

KIND = {"swap": "エアコンの入れ替え工事", "wash": "高圧分解洗浄"}
PARTS = {"cassette": "天井カセット形", "hang": "天井吊形", "outdoor": "室外機", "remote": "リモコン", "washing": "分解して洗う様子"}

# 日付は Instagram に載せた日（工事の日とは限らない）
WORKS = [
    {"d": "20251212", "post": "https://www.instagram.com/p/DSI3cGmE03J/", "kind": "swap", "h": 800,
     "parts": ["hang", "remote", "outdoor"],
     "title": "天井から吊るすエアコンに、入れ替えました。",
     "text": "天井吊形の室内機を入れ替えた現場です。壁のリモコンと、外に置いたダイキンの室外機も写っています。"},
    {"d": "20251211", "post": "https://www.instagram.com/p/DSGWgvukyzq/", "kind": "wash", "h": 800,
     "parts": ["cassette", "washing"],
     "title": "木の天井の部屋で、分解して洗いました。",
     "text": "天井カセット形を天井から外し、部品を分けて洗いました。カップにたまった水の色が、中にたまっていた汚れです。"},
    {"d": "20251205", "post": "https://www.instagram.com/p/DR21pkfE39k/", "kind": "swap", "h": 749,
     "parts": ["hang", "remote", "outdoor"],
     "title": "室内機から、壁のリモコン、外の室外機まで。",
     "text": "天井吊形への入れ替えです。壁のリモコンと、建物の外に置いたダイキンの室外機も写真に収めています。"},
    {"d": "20251204", "post": "https://www.instagram.com/p/DR0TQe-Ey1O/", "kind": "swap", "h": 800,
     "parts": ["hang", "outdoor"],
     "title": "室外機は、2台を縦に重ねて。",
     "text": "天井吊形の室内機を入れ替えた現場です。外には、室外機が2台、上下に重ねて置かれています。"},
    {"d": "20251203", "post": "https://www.instagram.com/p/DRxtOnwk21q/", "kind": "wash", "h": 800,
     "parts": ["cassette", "washing"],
     "title": "分解してみると、中はこれだけ汚れていました。",
     "text": "天井カセット形を分解し、高い水圧で中まで洗いました。茶色くにごった水と、洗ったあとのフィンを並べて載せています。"},
    {"d": "20251202", "post": "https://www.instagram.com/p/DRvEqV1k1P7/", "kind": "swap", "h": 800,
     "parts": ["cassette", "remote", "outdoor"],
     "title": "天井に埋め込むエアコンを、入れ替えました。",
     "text": "天井カセット形を入れ替えた現場です。天井に埋め込んだ新しい室内機と、壁のリモコン、外の室外機が写っています。"},
]

LOAD = {True: 'fetchpriority="high"', False: 'loading="lazy"'}

# 散らばったときの位置（vw・vh の割合と、傾き）
SCATTER = [(10, 24, -14), (12, -24, 9), (26, 20, 16), (6, -20, 11), (8, 30, -7), (22, -6, -18)]


def fmt(d):
    return f"{d[:4]}.{d[4:6]}.{d[6:]}"


def build():
    n = len(WORKS)
    n_swap = sum(1 for w in WORKS if w["kind"] == "swap")
    n_wash = n - n_swap

    # 冒頭の散らばる写真（古い順ではなく、新しい順）
    cards = "\n".join(f"""        <a class="wk__c" href="#w{w['d']}" style="--sx:{SCATTER[i][0]};--sy:{SCATTER[i][1]};--sr:{SCATTER[i][2]}">
          <img class="wk__real" src="../assets/img/works-{w['d']}.jpg" alt="{fmt(w['d'])}の{KIND[w['kind']]}の写真" width="640" height="{w['h']}" {LOAD[i < 3]}>
          <img class="wk__heat" src="../assets/img/works-{w['d']}.jpg" alt="" width="640" height="{w['h']}" aria-hidden="true">
          <span class="wk__d mono">{w['d'][4:6]}/{w['d'][6:]}</span>
        </a>""" for i, w in enumerate(WORKS))

    # 12月の暦（2025年12月1日は月曜）
    posted = {int(w["d"][6:]): w["d"] for w in WORKS}
    days = []
    for day in range(1, 32):
        if day in posted:
            days.append(f'<li class="on"><a href="#w{posted[day]}"><b class="mono">{day}</b></a></li>')
        else:
            days.append(f'<li><span class="mono">{day}</span></li>')
    week = "".join(f"<li class=\"cal__w\">{x}</li>" for x in "月火水木金土日")
    cal_on = "".join(f'<li>{int(w["d"][6:])}日　{KIND[w["kind"]]}</li>' for w in reversed(WORKS))

    # 現場の記録
    recs = []
    for i, w in enumerate(WORKS):
        ticks = "".join(
            f'<li class="{"has" if k in w["parts"] else "no"}"><i aria-hidden="true"></i>{v}<span class="sr">{"：写っている" if k in w["parts"] else "：写っていない"}</span></li>'
            for k, v in PARTS.items())
        recs.append(f"""      <article class="rec" id="w{w['d']}" data-kind="{w['kind']}" data-parts="{' '.join(w['parts'])}">
        <figure class="rec__fig">
          <div class="scan" data-scan>
            <img class="scan__real" src="../assets/img/works-{w['d']}.jpg" alt="{fmt(w['d'])}にInstagramへ載せた{KIND[w['kind']]}の写真。{'・'.join(PARTS[p] for p in w['parts'])}が写っている" width="640" height="{w['h']}" loading="lazy">
            <img class="scan__heat" src="../assets/img/works-{w['d']}.jpg" alt="" width="640" height="{w['h']}" loading="lazy" aria-hidden="true">
            <i class="scan__line" aria-hidden="true"></i>
          </div>
        </figure>
        <div class="rec__b">
          <p class="rec__no"><span class="mono">{n - i:02d}</span>{KIND[w['kind']]}</p>
          <h3 class="rec__t">{w['title']}</h3>
          <p class="rec__p">{w['text']}</p>
          <div class="rec__sheet">
            <p class="rec__l">写っている物</p>
            <ul class="rec__ticks" data-k="read" data-steps>{ticks}</ul>
          </div>
          <p class="rec__meta"><span class="mono">{fmt(w['d'])}</span>にInstagramへ載せた写真です</p>
          <a class="tl" href="{w['post']}" target="_blank" rel="noopener">この投稿をInstagramで見る</a>
        </div>
      </article>""")
    recs = "\n".join(recs)

    parts_btn = "".join(
        f'<button type="button" class="chip" data-f="part:{k}" aria-pressed="false">{v}<span class="mono">{sum(1 for w in WORKS if k in w["parts"])}</span></button>'
        for k, v in PARTS.items() if k != "washing")

    # 洗浄の図（フィンと汚れ）
    fins = "".join(f'<line x1="{60 + i*18}" y1="40" x2="{60 + i*18}" y2="250"/>' for i in range(19))
    dirt = "".join(
        f'<ellipse cx="{72 + (i*53) % 296}" cy="{62 + (i*37) % 170}" rx="{10 + (i*7) % 18}" ry="{7 + (i*5) % 12}"/>'
        for i in range(26))

    return head(TITLE, DESC, "works", 1, extra=jsonld(1)) + header("works", 1) + f"""
<main id="main">

<!-- ============================================ 冒頭 ── 散らばった写真が並ぶ -->
<section class="wk" aria-labelledby="wkH">
  <div class="wk__stage">
    <div class="wk__txt">
      <nav class="crumb crumb--light" aria-label="現在地"><a href="../">トップ</a><span aria-hidden="true">/</span><span aria-current="page">施工実績</span></nav>
      <h1 class="wk__h1" id="wkH">施工実績</h1>
      <div class="wk__s wk__s--a">
        <p class="wk__big">現場の写真を、<br>机に広げてみました。</p>
        <p class="wk__p">2025年12月にInstagramへ載せた、6つの現場です。スクロールすると、写真がそろっていきます。</p>
      </div>
      <div class="wk__s wk__s--b">
        <p class="wk__big">入れ替え工事が{n_swap}件、<br>高圧分解洗浄が{n_wash}件。</p>
        <p class="wk__p">気になる写真を押すと、その現場の記録まで飛びます。</p>
      </div>
    </div>
    <div class="wk__grid">
{cards}
    </div>
  </div>
</section>

<!-- ======================================================== 12月の暦 -->
<section class="sec" id="calendar">
  <div class="wrap duo duo--top">
    {sh("", "2025年12月", "12月2日から12日までに、<br>6つの現場を載せました。", "暦の中の数字は、Instagramに載せた日です。工事をした日とは限りません。押すと、その日の記録へ移ります。")}
    <div class="cal rise">
      <p class="cal__m"><b class="mono">12</b><span>2025年 12月</span></p>
      <ol class="cal__g" data-k="through" data-steps>
        {week}{''.join(days)}
      </ol>
      <ul class="cal__on">{cal_on}</ul>
    </div>
  </div>
</section>

<!-- ======================================================== 現場の記録 -->
<section class="sec sec--p2" id="records">
  <div class="wrap">
    {sh("", "現場の記録", "一件ずつ、<br>写っている物を見ていきます。", "写真にカーソルを当てると、その場所だけサーモ画像になります。下のボタンで、見たい現場だけに絞り込めます。")}
    <div class="filt rise" role="group" aria-label="現場の絞り込み">
      <div class="filt__row">
        <button type="button" class="chip is-on" data-f="all" aria-pressed="true">すべて<span class="mono">{n}</span></button>
        <button type="button" class="chip" data-f="kind:swap" aria-pressed="false">入れ替え工事<span class="mono">{n_swap}</span></button>
        <button type="button" class="chip" data-f="kind:wash" aria-pressed="false">高圧分解洗浄<span class="mono">{n_wash}</span></button>
      </div>
      <div class="filt__row"><span class="filt__l">写っている物で</span>{parts_btn}</div>
      <p class="filt__n" aria-live="polite"><b class="mono">{n}</b>件を表示しています</p>
    </div>
    <div class="recs">
{recs}
    </div>
  </div>
</section>

<!-- ======================================================== 洗浄の図 -->
<section class="wash" id="wash" aria-labelledby="washH">
  <div class="wash__stage">
    <div class="wrap wash__in">
      <div>
        <p class="sh__no mono"><span>高圧分解洗浄</span></p>
        <h2 class="big" id="washH">流れ出た水の色が、<br>汚れの量です。</h2>
        <p class="lede">エアコンは使っているうちに、中のフィンやファンにほこりや汚れがたまっていきます。高圧分解洗浄では、部品を外して、水の勢いで奥まで洗い流します。</p>
        <p class="lede wash__hint">スクロールすると、汚れが流れていきます。</p>
        <p class="more"><button type="button" class="btn btn--light" data-jump="kind:wash">洗浄の現場だけを見る</button></p>
      </div>
      <figure class="wash__fig" aria-hidden="true">
        <svg viewBox="0 0 440 420" fill="none">
          <defs>
            <mask id="washMask"><rect x="0" y="0" width="440" height="420" fill="#fff"/><rect class="wash__clean2" x="40" y="30" width="360" height="0" fill="#000"/></mask>
          </defs>
          <rect x="40" y="30" width="360" height="230" stroke="rgba(236,234,228,.35)"/>
          <g stroke="rgba(236,234,228,.7)" stroke-width="2">{fins}</g>
          <g fill="#6b4a2a" opacity=".85" mask="url(#washMask)">{dirt}</g>
          <g class="wash__nozzle">
            <rect x="196" y="0" width="48" height="16" rx="3" fill="#eceae4"/>
            <g stroke="#8fd8ff" stroke-width="2" stroke-linecap="round">
              <path d="M205 20 L180 60"/><path d="M220 20 L220 64"/><path d="M235 20 L260 60"/>
            </g>
          </g>
          <!-- カップ -->
          <path d="M150 300 L166 410 L274 410 L290 300" stroke="rgba(236,234,228,.8)" stroke-width="2"/>
          <clipPath id="cupClip"><path d="M150 300 L166 410 L274 410 L290 300 Z"/></clipPath>
          <g clip-path="url(#cupClip)"><rect class="wash__water" x="140" y="410" width="160" height="0" fill="#3a2a1a"/></g>
          <text x="310" y="400" fill="rgba(236,234,228,.7)" font-size="12" font-family="Zen Kaku Gothic New, sans-serif">流れ出た水</text>
        </svg>
      </figure>
    </div>
  </div>
</section>

<!-- ======================================================== 入れ替えで新しくなる所 -->
<section class="sec" id="parts">
  <div class="wrap">
    {sh("", "入れ替え工事", "入れ替えで新しくなるのは、<br>部屋の中と外の両方です。", "写真に出てくる機械を、場所ごとに分けてみました。押すと、それが写っている現場だけを表示します。")}
    <div class="ex rise" data-k="enter">
      <svg class="ex__bg" viewBox="0 0 1000 460" fill="none" aria-hidden="true">
        <path d="M40 60 H640 V420 H40 Z" stroke="rgba(15,19,20,.3)"/>
        <path d="M40 120 H640" stroke="rgba(15,19,20,.3)" stroke-dasharray="4 5"/>
        <path d="M640 420 H960" stroke="rgba(15,19,20,.3)"/>
        <path class="ex__pipe" pathLength="1" d="M330 100 H700 V300 H780" stroke="#e2572b" stroke-width="2" stroke-dasharray="1" />
        <text x="54" y="100" fill="#636a6b" font-size="14" font-family="Zen Kaku Gothic New, sans-serif">部屋の中</text>
        <text x="700" y="100" fill="#636a6b" font-size="14" font-family="Zen Kaku Gothic New, sans-serif">建物の外</text>
      </svg>
      <button type="button" style="--fx:120;--fy:90" class="ex__p ex__p--cassette" data-jump="part:cassette">
        <svg viewBox="0 0 160 50" aria-hidden="true"><rect x="10" y="4" width="140" height="30" stroke="currentColor" stroke-width="2" fill="none"/><path d="M30 42 H60 M100 42 H130" stroke="currentColor" stroke-width="2"/></svg>
        <b>天井カセット形</b><small>天井に埋め込む室内機</small>
      </button>
      <button type="button" style="--fx:40;--fy:-60" class="ex__p ex__p--hang" data-jump="part:hang">
        <svg viewBox="0 0 160 60" aria-hidden="true"><path d="M40 2 V14 M120 2 V14" stroke="currentColor" stroke-width="2"/><rect x="10" y="14" width="140" height="36" rx="6" stroke="currentColor" stroke-width="2" fill="none"/><path d="M24 42 H136" stroke="currentColor" stroke-width="2"/></svg>
        <b>天井吊形</b><small>天井から吊るす室内機</small>
      </button>
      <button type="button" style="--fx:220;--fy:-20" class="ex__p ex__p--remote" data-jump="part:remote">
        <svg viewBox="0 0 60 80" aria-hidden="true"><rect x="8" y="4" width="44" height="72" rx="4" stroke="currentColor" stroke-width="2" fill="none"/><rect x="16" y="14" width="28" height="22" stroke="currentColor" stroke-width="2" fill="none"/></svg>
        <b>リモコン</b><small>壁に付ける操作盤</small>
      </button>
      <button type="button" style="--fx:-240;--fy:-60" class="ex__p ex__p--outdoor" data-jump="part:outdoor">
        <svg viewBox="0 0 120 110" aria-hidden="true"><rect x="6" y="6" width="108" height="96" stroke="currentColor" stroke-width="2" fill="none"/><circle cx="56" cy="54" r="32" stroke="currentColor" stroke-width="2" fill="none"/><path class="ex__fan" d="M56 54 C70 44 80 44 84 52 M56 54 C56 70 50 80 42 80 M56 54 C42 48 36 38 40 30" stroke="currentColor" stroke-width="2"/></svg>
        <b>室外機</b><small>建物の外で熱を逃がす</small>
      </button>
    </div>
  </div>
</section>

<!-- ======================================================== Instagram -->
<section class="ig" aria-labelledby="igH">
  <div class="ig__band" aria-hidden="true"><p class="ig__run mono" data-k="through">@personright501　@personright501　@personright501　@personright501　@personright501　@personright501</p></div>
  <div class="wrap duo">
    <h2 class="big" id="igH">新しい現場は、<br>Instagramで。</h2>
    <div>
      <p class="lede">このページで紹介した6件のほかの現場は、Instagramでご覧ください。</p>
      <p class="more"><a class="btn" href="{INSTA}" target="_blank" rel="noopener">Instagramを開く</a></p>
    </div>
  </div>
</section>

</main>
""" + footer(1)
