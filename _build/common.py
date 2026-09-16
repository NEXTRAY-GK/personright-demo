# -*- coding: utf-8 -*-
"""パーソンライト — 共通部品。build.py から読む。

   2026-09-16 第3版。考えは1つ。
     「空調の仕事は、目に見えない温度を扱う。だからサイトはサーモカメラのように見せる」
   写真はサーモ画像から実写へ戻り、頭の読み出しは読み進めるほど室温が下がる。
"""

import hashlib as _hl, os as _os

_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)


def _v(rel):
    """資産の中身から短い版番号を作る（キャッシュが古いまま残らないように）"""
    try:
        with open(_os.path.join(_ROOT, rel), "rb") as f:
            return _hl.md5(f.read()).hexdigest()[:8]
    except OSError:
        return "0"


CSS_V = _v("assets/css/style.css")
JS_V = _v("assets/js/main.js")

SITE = "株式会社パーソンライト"
TEL = "024-983-0294"
TEL_RAW = "0249830294"
FAX = "024-983-0295"
ZIP = "〒963-0101"
ADDR = "福島県郡山市安積町日出山2-43"
INSTA = "https://www.instagram.com/personright501/"
BASE = "https://nextray-gk.github.io/personright-demo"

# 頭の並び。施工の写真はトップの中にあるので、足にだけ出す
NAV = [
    ("ac",          "ac/",          "業務用エアコン"),
    ("office-tech", "office-tech/", "通信機器"),
    ("works",       "works/",       "施工実績"),
    ("reviews",     "reviews/",     "お客様の声"),
    ("company",     "company/",     "会社案内"),
    ("recruit",     "recruit/",     "採用情報"),
]
FOOT_NAV = [
    ("", "", "トップ"),
    ("ac", "ac/", "業務用エアコン"),
    ("office-tech", "office-tech/", "通信機器"),
    ("works", "works/", "施工実績"),
    ("reviews", "reviews/", "お客様の声"),
    ("company", "company/", "会社案内"),
    ("recruit", "recruit/", "採用情報"),
    ("contact", "contact/", "お問い合わせ"),
    ("privacy", "privacy/", "プライバシーポリシー"),
]


def R(depth):
    return "../" * depth if depth else "./"


def head(title, desc, here, depth, og="og.jpg", extra="", page=""):
    r = "../" * depth if depth else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}/assets/img/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0e10">
<link rel="icon" href="{r}assets/img/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{r}assets/img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Space+Grotesk:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{r}assets/css/style.css?v={CSS_V}">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>
<body class="{page}">
<a class="sr" href="#main">本文へ移動</a>
"""


def header(here, depth):
    r = R(depth)
    cur = ' aria-current="page"'
    items = "\n      ".join(
        f'<li><a href="{r}{href}"{cur if key == here else ""}>{ja}</a></li>'
        for key, href, ja in NAV
    )
    return f"""<header class="head">
  <a class="head__logo" href="{r}">
    <img class="lg-d" src="{r}assets/img/logo.svg" alt="{SITE}" width="370" height="46">
    <img class="lg-l" src="{r}assets/img/logo-white.svg" alt="" width="370" height="46" aria-hidden="true">
  </a>
  <nav class="head__nav" aria-label="主なメニュー">
    <ul>
      {items}
    </ul>
  </nav>
  <p class="rd" aria-hidden="true" title="読み進めるほど、室温が下がります">
    <i class="rd__dot"></i><span class="rd__m">冷房</span><b class="rd__v">--.-</b><span class="rd__u">℃</span>
  </p>
  <a class="head__cta" href="{r}contact/">見積りを頼む</a>
  <button class="burger" type="button" aria-controls="drawer" aria-expanded="false" aria-label="メニューを開く"><span></span><span></span></button>
</header>
<div class="drawer" id="drawer" hidden>
  <nav aria-label="メニュー">
    <ol>
      <li><a href="{r}"><i>00</i>トップ</a></li>
      {"".join(f'<li><a href="{r}{href}"><i>{i+1:02d}</i>{ja}</a></li>' for i, (key, href, ja) in enumerate(NAV))}
      <li><a href="{r}contact/"><i>{len(NAV)+1:02d}</i>お問い合わせ</a></li>
    </ol>
  </nav>
  <div class="drawer__tel">
    <small>お電話</small>
    <a class="mono" href="tel:{TEL_RAW}">{TEL}</a>
  </div>
</div>
"""


def phero(no, en, ja, note, img, alt, crumbs, depth, w=1200, h=800):
    """下層ページの頭。左に言葉、右にサーモ画像から実写へ戻る写真。
       crumbs … [(名前, href), …] 最後はリンク無し"""
    r = R(depth)
    c = [f'<a href="{r}">トップ</a>']
    for name, href in crumbs:
        c.append('<span aria-hidden="true">/</span>')
        c.append(f'<a href="{r}{href}">{name}</a>' if href else f'<span aria-current="page">{name}</span>')
    note_html = f'<p class="ph__note">{note}</p>' if note else ""
    fig = ""
    if img:
        fig = f"""  <figure class="ph__fig scan scan--auto">
    <img class="scan__real" src="{r}assets/img/{img}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high">
    <img class="scan__heat" src="{r}assets/img/{img}" alt="" width="{w}" height="{h}" aria-hidden="true">
    <i class="scan__line" aria-hidden="true"></i>
  </figure>
"""
    long = " ph--long" if len(ja) > 12 else ""
    return f"""<div class="ph{'' if img else ' ph--text'}{long}">
  <div class="ph__t">
    <nav class="crumb" aria-label="現在地">{''.join(c)}</nav>
    <h1 class="ph__h">{ja}</h1>
    {note_html}
  </div>
{fig}</div>
"""


def sh(no, tag, title, note="", cls="", hid=""):
    """節の見出し。左に番号と札、右に見出しと添え書き"""
    n = f'<p class="sh__p">{note}</p>' if note else ""
    i = f' id="{hid}"' if hid else ""
    return f"""<header class="sh rise {cls}" data-k="enter">
      <p class="sh__no mono">{f"<b>{no}</b>" if no else ""}<span>{tag}</span></p>
      <div class="sh__b">
        <h2 class="sh__t"{i}>{title}</h2>
        {n}
      </div>
    </header>"""


def cta(depth):
    r = R(depth)
    return f"""<section class="cta" aria-labelledby="ctaT">
  <div class="wrap cta__in">
    <p class="cta__no">ご相談・お見積り</p>
    <h2 class="cta__t" id="ctaT">まずは一度、<br>その部屋を見せてください。</h2>
    <p class="cta__d">お見積りは無料です。スタッフがうかがって実際の場所を見てから、機種と工事のやり方を決めます。エアコンに限らず、防犯カメラや複合機のご相談でも構いません。</p>
    <div class="cta__ways">
      <a class="cta__tel" href="tel:{TEL_RAW}"><small>お電話で</small><b class="mono">{TEL}</b></a>
      <a class="cta__form" href="{r}contact/"><small>フォームから（24時間受付）</small><b>お問い合わせフォーム</b><i aria-hidden="true">→</i></a>
    </div>
  </div>
</section>
"""


THERMAL_FILTER = """<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false">
  <filter id="thermal" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values=".33 .5 .17 0 0  .33 .5 .17 0 0  .33 .5 .17 0 0  0 0 0 1 0"/>
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.03 0.10 0.42 0.76 0.94 0.98 1"/>
      <feFuncG type="table" tableValues="0.04 0.12 0.11 0.09 0.35 0.69 0.96"/>
      <feFuncB type="table" tableValues="0.12 0.43 0.60 0.36 0.17 0.24 0.76"/>
    </feComponentTransfer>
  </filter>
</svg>"""


def footer(depth, cta_on=True):
    r = R(depth)
    nav = "\n      ".join(
        f'<a href="{r}{href}">{ja}</a>' for key, href, ja in FOOT_NAV
    )
    return (cta(depth) if cta_on else "") + f"""<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div>
        <img class="foot__logo" src="{r}assets/img/logo-white.svg" alt="{SITE}" width="370" height="46">
        <address class="foot__addr">
          本社　{ZIP}　{ADDR}<br>
          TEL <a class="mono" href="tel:{TEL_RAW}">{TEL}</a>　FAX <span class="mono">{FAX}</span>
        </address>
        <p class="foot__sns"><a href="{INSTA}" target="_blank" rel="noopener">Instagram　@personright501</a></p>
      </div>
      <nav class="foot__nav" aria-label="サイトのご案内">
      {nav}
      </nav>
    </div>
    <p class="foot__cr mono">© Person right Co., Ltd.</p>
  </div>
</footer>

<p class="bar" aria-hidden="true"><i></i></p>

<button class="demo" type="button" popovertarget="demoNote">デモサイトについて</button>
<div id="demoNote" popover>
  <h2>これはデモサイトです</h2>
  <p>株式会社パーソンライト様の会社情報をもとに、NextRay がデザイン案として制作したものです。<strong>ご発注をいただいたものではありません。</strong></p>
  <p>社名・住所・電話番号・写真は実在のものです。断面図の温度はイメージです。お問い合わせフォームは形だけで、送信はできません。検索には出ないようにしてあります。</p>
  <button class="btn" type="button" popovertarget="demoNote" popovertargetaction="hide">閉じる</button>
</div>
{THERMAL_FILTER}
<script src="{r}assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""


def jsonld(depth, extra=None):
    """組織の構造化データ。手元にある事実だけ。"""
    import json
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "株式会社パーソンライト",
        "alternateName": "Person right",
        "url": BASE + "/",
        "logo": BASE + "/assets/img/logo.svg",
        "telephone": "+81-24-983-0294",
        "faxNumber": "+81-24-983-0295",
        "foundingDate": "2022-12-28",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "JP",
            "addressRegion": "福島県",
            "addressLocality": "郡山市",
            "streetAddress": "安積町日出山2-43",
            "postalCode": "963-0101",
        },
        "sameAs": [INSTA],
    }
    out = [org] if extra is None else [org] + extra
    return (
        '<script type="application/ld+json">'
        + json.dumps(out if len(out) > 1 else out[0], ensure_ascii=False)
        + "</script>\n"
    )
