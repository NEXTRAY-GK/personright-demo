# -*- coding: utf-8 -*-
"""パーソンライト — 共通部品。build.py から読む。"""

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

NAV = [
    ("",            "/",             "HOME",             "ホーム"),
    ("ac",          "/ac/",          "AIR CONDITIONER",  "エアコン"),
    ("office-tech", "/office-tech/", "OFFICE TECH",      "通信機器"),
    ("works",       "/#works",       "WORKS",            "施工実例"),
    ("reviews",     "/reviews/",     "CUSTOMER REVIEWS", "お客様の声"),
    ("company",     "/company/",     "COMPANY",          "会社案内"),
    ("recruit",     "/recruit/",     "RECRUIT",          "採用情報"),
    ("contact",     "/contact/",     "CONTACT US",       "お問い合わせ"),
]
FOOT_NAV = NAV + [("privacy", "/privacy/", "PRIVACY POLICY", "プライバシーポリシー")]


def head(title, desc, here, depth, og="og.jpg", extra=""):
    """depth … ルートからの階層数（/ac/ なら 1、/recruit/46/ なら 2）"""
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
<meta name="theme-color" content="#1a6969">
<link rel="icon" href="{r}assets/img/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{r}assets/img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{r}assets/css/style.css?v={CSS_V}">
{extra}</head>
<body>
<a class="sr" href="#main">本文へ移動</a>
<div class="gauge" aria-hidden="true"><i></i></div>
"""


def header(here, depth):
    r = "../" * depth if depth else "./"
    items = []
    for key, href, en, ja in NAV:
        h = (r + href.lstrip("/")) if href.startswith("/") else href
        if href == "/":
            h = r
        elif href.startswith("/#"):
            h = r + href[1:]
        cur = ' aria-current="page"' if key == here else ""
        items.append(
            f'<li><a href="{h}"{cur}><span class="en">{en}</span><span>{ja}</span></a></li>'
        )
    lis = "\n      ".join(items)
    return f"""<header class="head">
  <a class="head__logo" href="{r}"><img src="{r}assets/img/logo.svg" alt="{SITE}" width="370" height="46"></a>
  <nav class="head__nav" id="gnav" aria-label="主なメニュー">
    <div class="head__inner">
      <ul class="head__list">
        {lis}
      </ul>
      <div class="navtel">
        <small>TEL</small>
        <a class="num" href="tel:{TEL_RAW}">{TEL}</a>
      </div>
    </div>
  </nav>
  <div class="head__tel">
    <small>TEL</small>
    <b><a href="tel:{TEL_RAW}">{TEL}</a></b>
  </div>
  <a class="btn head__cta" href="{r}contact/">お問い合わせ</a>
  <button class="burger" type="button" aria-controls="gnav" aria-expanded="false" aria-label="メニューを開く"><span></span><span></span><span></span></button>
</header>
"""


def phero(en, ja, note, img, alt, crumbs, depth):
    """下層ページの見出し。crumbs … [(名前, href), …] 最後はリンク無し"""
    r = "../" * depth if depth else "./"
    c = [f'<a href="{r}">ホーム</a>']
    for name, href in crumbs:
        c.append('<span aria-hidden="true">/</span>')
        c.append(f'<a href="{r}{href}">{name}</a>' if href else f"<span>{name}</span>")
    note_html = f'<p class="phero__note">{note}</p>' if note else ""
    return f"""<div class="phero" style="--c1:#041f1e;--c2:#0f423f">
  <div class="phero__ph"><img src="{r}assets/img/{img}" alt="{alt}" width="1600" height="900" fetchpriority="high"></div>
  <div class="wrap phero__in">
    <div class="phero__t">
      <span class="phero__en">{en}</span>
      <h1>{ja}</h1>
      {note_html}
    </div>
    <nav class="crumb" aria-label="現在地">{''.join(c)}</nav>
  </div>
</div>
"""


def cta(depth, bg="office-front.jpg"):
    r = "../" * depth if depth else "./"
    return f"""<section class="cta" style="--c1:#f4efdf;--c2:#e6d5ab">
  <div class="cta__ph"><img src="{r}assets/img/{bg}" alt="" width="1600" height="900" loading="lazy"></div>
  <div class="wrap cta__in">
    <div class="cta__l">
      <span class="cta__en">CONTACT</span>
      <h2 class="cta__t">まずは、いまの一台を<br>見せてください</h2>
      <p class="cta__d">いまお使いの機種の型番と、部屋の広さが分かれば見積りが出ます。無料です。電気代が気になる、古い機種を入れ替えたい、防犯カメラを検討している ── どれでも構いません。</p>
    </div>
    <div class="cta__r">
      <div class="cta__way">
        <small>BY PHONE</small>
        <a class="tel num" href="tel:{TEL_RAW}">{TEL}</a>
        <p>FAX {FAX}</p>
      </div>
      <div class="cta__way">
        <small>BY FORM</small>
        <p>24時間受け付けています。後日、担当よりご連絡します。</p>
        <a class="btn btn--dark" href="{r}contact/">お問い合わせフォーム</a>
      </div>
    </div>
  </div>
</section>
"""


def footer(depth):
    r = "../" * depth if depth else "./"
    items = []
    for key, href, en, ja in FOOT_NAV:
        h = r if href == "/" else (r + href[1:] if href.startswith("/#") else r + href.lstrip("/"))
        items.append(f'<a href="{h}"><span class="en">{en}</span><span>{ja}</span></a>')
    nav = "\n      ".join(items)
    return f"""<div class="dusk" aria-hidden="true"></div>
<footer class="foot" style="--c1:#0a3a37;--c2:#04211f">
  <div class="wrap">
    <div class="foot__top">
      <div>
        <img class="foot__logo" src="{r}assets/img/logo-white.svg" alt="{SITE}" width="370" height="46">
        <address class="foot__addr">
          <b>株式会社 パーソンライト</b>
          本社 ／ {ZIP}　{ADDR}<br>
          TEL <a class="num" href="tel:{TEL_RAW}">{TEL}</a>　FAX <span class="num">{FAX}</span>
        </address>
        <div class="foot__sns">
          <a href="{INSTA}" target="_blank" rel="noopener">INSTAGRAM</a>
        </div>
      </div>
      <nav class="foot__nav" aria-label="サイト内のご案内">
      {nav}
      </nav>
    </div>
    <div class="foot__sub">
      <p>このホームページは須賀川市中小企業ホームページ開設等支援事業補助金を活用して作成しました</p>
      <p class="foot__cr">© 2023 Person right All Rights Reserved.</p>
    </div>
  </div>
</footer>

<button class="toTop" type="button" aria-label="ページの先頭へ戻る">
  <svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
</button>

<button class="demo" type="button" popovertarget="demoNote">デモサイトについて</button>
<div id="demoNote" popover>
  <h2>これはデモサイトです</h2>
  <p>株式会社パーソンライト様の現行サイト（personright.com）の内容をもとに、NextRay がデザイン案として制作したものです。<strong>ご発注をいただいたものではありません。</strong></p>
  <p>掲載の社名・住所・電話番号・写真は現行サイトから引き継いだ実在のものです。お問い合わせフォームは形だけで、送信はできません。検索には出ないようにしてあります。</p>
  <button class="btn" type="button" popovertarget="demoNote" popovertargetaction="hide">閉じる</button>
</div>

<script src="{r}assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""


def jsonld(depth, extra=None):
    """組織の構造化データ。手元にある事実だけ。"""
    import json
    r = "../" * depth if depth else "./"
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
