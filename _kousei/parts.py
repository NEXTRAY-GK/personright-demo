# -*- coding: utf-8 -*-
"""パーソンライト 第4版（構成のやり直し）— 共通の枠。

   2026-09-17、代表の指示「propagateinc.com と同じ構成、迷わない導線で1から組み直す。デザインはそのあと」。
   手本から写したのは節の並びと導線だけ。HTML・CSS・JS・文章・写真は持ち込んでいない。
   見た目は仮（assets/css/kousei.css）。デザインの段で差し替える。

   導線の決め事
   - どのページも、頭に「無料で見積りを頼む」と電話。スマホは画面下に固定の帯
   - どのページも、最後はお見積りの帯（電話とフォーム）で終わる
   - 事業のページ（ac・office-tech）は、ページの中にフォームを持つ（出口をページの外に出さない）
   - 相談の種類は ?type= で引き継ぐ（どの入口から来たかを、フォームで選び直させない）
"""

import hashlib as _hl, os as _os, json as _json

_HERE = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(_HERE)


def _v(rel):
    try:
        with open(_os.path.join(ROOT, rel), "rb") as f:
            return _hl.md5(f.read()).hexdigest()[:8]
    except OSError:
        return "0"


SITE = "株式会社パーソンライト"
TEL = "024-983-0294"
TEL_RAW = "0249830294"
FAX = "024-983-0295"
ZIP = "〒963-0101"
ADDR = "福島県郡山市安積町日出山2-43"
INSTA = "https://www.instagram.com/personright501/"
BASE = "https://nextray-gk.github.io/personright-demo"
MAP = "https://www.google.com/maps/search/?api=1&query=" + ADDR

# 相談の種類（フォームの選択肢。?type= の値もこれ）
TOPICS = ["業務用エアコン", "リース", "クリーニング", "防犯カメラ", "複合機", "ビジネスフォン", "工事", "その他"]

COMPANY_SUB = [
    ("company-info", "会社概要"),
    ("history", "沿革"),
    ("philosophy", "企業理念"),
    ("message", "代表あいさつ"),
    ("members", "スタッフ"),
    ("access", "アクセス"),
]


def R(depth):
    return "../" * depth if depth else "./"


def q(topic):
    """フォームへ相談の種類を渡すクエリ"""
    from urllib.parse import quote
    return "?type=" + quote(topic)


def head(title, desc, depth, body_cls=""):
    r = "../" * depth
    css_v = _v("assets/css/kousei.css")
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
<meta property="og:image" content="{BASE}/assets/img/og.jpg">
<link rel="icon" href="{r}assets/img/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{r}assets/img/icon-180.png">
<link rel="stylesheet" href="{r}assets/css/kousei.css?v={css_v}">
</head>
<body class="{body_cls}">
<a class="skip" href="#main">本文へ移動</a>
"""


# ---------------------------------------------------------------- 頭
def header(depth, here=""):
    r = R(depth)

    def cur(key):
        return ' aria-current="page"' if key == here else ""

    company_sub = "".join(
        f'<li><a href="{r}company/#{a}">{t}</a></li>' for a, t in COMPANY_SUB
    )
    mega = f"""<div class="mega" id="megaService">
        <div class="mega__in">
          <div class="mega__group">
            <p class="mega__label">環境事業</p>
            <a class="mega__card" href="{r}ac/">
              <small>5メーカー・12種類から選べる</small>
              <b>業務用エアコン</b>
              <span>販売・取り付け・リース・7年保証</span>
            </a>
          </div>
          <div class="mega__group">
            <p class="mega__label">通信事業</p>
            <a class="mega__card" href="{r}office-tech/">
              <small>事務所の機器をまとめて</small>
              <b>通信機器</b>
              <span>防犯カメラ・複合機・ビジネスフォン</span>
            </a>
          </div>
          <div class="mega__group">
            <p class="mega__label">そのほか</p>
            <ul class="mega__list">
              <li><a href="{r}#service">事業の一覧（4つの事業）</a></li>
              <li><a href="{r}ac/#after">分解・洗浄クリーニング</a></li>
              <li><a href="{r}contact/{q('工事')}">電気工事・水回り工事の相談</a></li>
            </ul>
          </div>
        </div>
      </div>"""
    return f"""<header class="hd">
  <div class="hd__in">
    <a class="hd__logo" href="{r}"><img src="{r}assets/img/logo.svg" alt="{SITE}" width="370" height="46"></a>
    <nav class="hd__nav" aria-label="主なメニュー">
      <ul>
        <li class="has-sub">
          <button type="button" class="hd__btn" aria-expanded="false" aria-controls="megaService"{' data-current' if here in ('ac', 'office-tech') else ''}>事業紹介</button>
      {mega}
        </li>
        <li><a href="{r}works/"{cur('works')}>施工実績</a></li>
        <li><a href="{r}reviews/"{cur('reviews')}>お客様の声</a></li>
        <li class="has-sub">
          <a href="{r}company/"{cur('company')}>会社案内</a>
          <ul class="drop">{company_sub}</ul>
        </li>
        <li><a href="{r}recruit/"{cur('recruit')}>採用情報</a></li>
        <li><a href="{r}faq/"{cur('faq')}>よくある質問</a></li>
      </ul>
    </nav>
    <a class="hd__tel" href="tel:{TEL_RAW}"><small>お電話</small>{TEL}</a>
    <a class="btn btn--main hd__cta" href="{r}contact/">無料で見積りを頼む</a>
    <button class="burger" type="button" aria-controls="drawer" aria-expanded="false" aria-label="メニューを開く"><span></span><span></span></button>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <nav aria-label="メニュー">
    <p class="drawer__label">事業紹介</p>
    <ul>
      <li><a href="{r}ac/">業務用エアコン</a></li>
      <li><a href="{r}office-tech/">通信機器（防犯カメラ・複合機・電話）</a></li>
      <li><a href="{r}#service">事業の一覧</a></li>
    </ul>
    <p class="drawer__label">パーソンライトを知る</p>
    <ul>
      <li><a href="{r}works/">施工実績</a></li>
      <li><a href="{r}reviews/">お客様の声</a></li>
      <li><a href="{r}company/">会社案内</a></li>
      <li><a href="{r}recruit/">採用情報</a></li>
      <li><a href="{r}faq/">よくある質問</a></li>
    </ul>
  </nav>
  <div class="drawer__cta">
    <a class="btn btn--main" href="{r}contact/">無料で見積りを頼む</a>
    <a class="btn btn--line" href="tel:{TEL_RAW}">電話する　{TEL}</a>
  </div>
</div>
<main id="main">
"""


def crumb(depth, items):
    """items … [(名前, href or None)]。最後は現在地"""
    r = R(depth)
    out = [f'<a href="{r}">トップ</a>']
    for name, href in items:
        out.append('<span aria-hidden="true">›</span>')
        out.append(f'<a href="{r}{href}">{name}</a>' if href else f'<span aria-current="page">{name}</span>')
    return f'<nav class="crumb" aria-label="現在地"><div class="wrap">{"".join(out)}</div></nav>'


def page_hero(depth, en, ja, lead, crumbs, actions="", chips=None):
    """下層ページの頭（手本の「英字の札＋日本語の見出し」）"""
    chip_html = ""
    if chips:
        chip_html = '<nav class="chips" aria-label="このページの目次"><ul>' + "".join(
            f'<li><a href="#{a}">{t}</a></li>' for a, t in chips) + "</ul></nav>"
    return f"""{crumb(depth, crumbs)}
<section class="phero" id="top">
  <div class="wrap">
    <p class="en">{en}</p>
    <h1>{ja}</h1>
    {f'<p class="lead">{lead}</p>' if lead else ''}
    {actions}
    {chip_html}
  </div>
</section>
"""


def sec_head(en, label, title, lead="", center=False):
    c = " sh--center" if center else ""
    return f"""<header class="sh{c}">
      <p class="sh__label"><span>{label}</span><i>{en}</i></p>
      <h2>{title}</h2>
      {f'<p class="sh__lead">{lead}</p>' if lead else ''}
    </header>"""


def tbd(text):
    """事実が手元に無い所。推測で埋めず、何が要るかを見せる"""
    return f'<p class="tbd"><b>要確認</b>{text}</p>'


def cta_pair(depth, topic=None, main="無料で見積りを頼む"):
    r = R(depth)
    href = f"{r}contact/" + (q(topic) if topic else "")
    return f"""<div class="cta-pair">
      <a class="btn btn--main" href="{href}">{main}</a>
      <a class="btn btn--line" href="tel:{TEL_RAW}">電話で相談する　{TEL}</a>
    </div>"""


def mid_cta(depth, title, sub, topic=None):
    """ページの途中に挟む、短いお見積りの帯"""
    return f"""<section class="midcta">
  <div class="wrap midcta__in">
    <div>
      <p class="midcta__t">{title}</p>
      <p class="midcta__s">{sub}</p>
    </div>
    {cta_pair(depth, topic)}
  </div>
</section>
"""


def contact_band(depth, title="まずは一度、その部屋を見せてください。", topic=None):
    r = R(depth)
    href = f"{r}contact/" + (q(topic) if topic else "")
    return f"""<section class="cband" id="contact-band">
  <div class="wrap">
    {sec_head("CONTACT", "お見積り・ご相談", title, "お見積りは無料です。スタッフがうかがって実際の場所を見てから、機種と工事のやり方を決めます。", center=True)}
    <div class="cband__ways">
      <a class="cband__way" href="tel:{TEL_RAW}"><small>お電話で</small><b>{TEL}</b><span>FAX {FAX}</span></a>
      <a class="cband__way cband__way--main" href="{href}"><small>フォームで（24時間受付）</small><b>無料で見積りを頼む</b><span>入れていただくのは、お名前・電話・メールの3つです</span></a>
    </div>
    <p class="cband__sub">先に聞きたいことがあれば <a href="{r}faq/">よくある質問</a> へ。</p>
  </div>
</section>
"""


def footer(depth, band=True, band_title=None, band_topic=None):
    r = R(depth)
    b = ""
    if band:
        b = contact_band(depth, band_title, band_topic) if band_title else contact_band(depth, topic=band_topic)
    return f"""{b}</main>
<footer class="ft">
  <div class="wrap ft__in">
    <div class="ft__co">
      <a href="{r}"><img src="{r}assets/img/logo.svg" alt="{SITE}" width="370" height="46"></a>
      <address>{ZIP}　{ADDR}<br>TEL <a href="tel:{TEL_RAW}">{TEL}</a>　FAX {FAX}</address>
      <a class="btn btn--main" href="{r}contact/">無料で見積りを頼む</a>
    </div>
    <nav class="ft__nav" aria-label="サイトのご案内">
      <div>
        <p>事業紹介</p>
        <ul>
          <li><a href="{r}ac/">業務用エアコン</a></li>
          <li><a href="{r}office-tech/">通信機器</a></li>
          <li><a href="{r}#service">事業の一覧</a></li>
        </ul>
      </div>
      <div>
        <p>パーソンライトを知る</p>
        <ul>
          <li><a href="{r}works/">施工実績</a></li>
          <li><a href="{r}reviews/">お客様の声</a></li>
          <li><a href="{r}company/">会社案内</a></li>
          <li><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
      <div>
        <p>採用</p>
        <ul>
          <li><a href="{r}recruit/">採用情報</a></li>
          <li><a href="{r}recruit/#jobs">募集中の仕事</a></li>
        </ul>
      </div>
      <div>
        <p>お問い合わせ</p>
        <ul>
          <li><a href="{r}contact/">お見積り・ご相談</a></li>
          <li><a href="{r}faq/">よくある質問</a></li>
          <li><a href="{r}privacy/">プライバシーポリシー</a></li>
        </ul>
      </div>
    </nav>
  </div>
  <p class="ft__cr">© Person right Co., Ltd.</p>
  <p class="ft__demo">これはデモサイトです。株式会社パーソンライト様の会社情報をもとに NextRay が構成案として作ったもので、ご発注をいただいたものではありません。フォームは送信されません。検索には出ないようにしてあります。</p>
</footer>
<div class="spbar" aria-label="お問い合わせ">
  <a href="tel:{TEL_RAW}">電話する</a>
  <a class="spbar__main" href="{r}contact/">無料で見積りを頼む</a>
</div>
<script src="{r}assets/js/kousei.js?v={_v('assets/js/kousei.js')}" defer></script>
</body>
</html>
"""


def jsonld(extra=None):
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE,
        "alternateName": "Person right",
        "url": BASE + "/",
        "logo": BASE + "/assets/img/logo.svg",
        "telephone": "+81-24-983-0294",
        "faxNumber": "+81-24-983-0295",
        "foundingDate": "2022-12-28",
        "address": {
            "@type": "PostalAddress", "addressCountry": "JP", "addressRegion": "福島県",
            "addressLocality": "郡山市", "streetAddress": "安積町日出山2-43", "postalCode": "963-0101",
        },
        "sameAs": [INSTA],
    }
    data = [org] + (extra or [])
    return '<script type="application/ld+json">' + _json.dumps(data if len(data) > 1 else org, ensure_ascii=False) + "</script>\n"


def faq_ld(pairs):
    import re
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": qq,
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for qq, a in pairs],
    }


def acc(pairs):
    return "\n".join(
        f"""<details class="qa"><summary><i>Q</i>{qq}</summary><div class="qa__a"><i>A</i><div>{a}</div></div></details>"""
        for qq, a in pairs)


def inquiry_form(depth, topic=None, heading=True):
    """お見積りのフォーム。項目は 種類・お名前・電話・メール・内容（任意）の5つに絞った。
       旧サイトにあったフリガナと確認用メールは外した（手本の決まり「出口の項目は削る」）。"""
    r = R(depth)
    radios = "".join(
        f'<label class="pill"><input type="radio" name="type" value="{t}"{" checked" if t == topic else ""}><span>{t}</span></label>'
        for t in TOPICS)
    h = ""
    if heading:
        h = sec_head("CONTACT", "お見積り・ご相談", "無料で見積りを頼む",
                     "フォームは24時間受け付けています。内容を確かめてから、担当者がご連絡します。", center=True)
    return f"""{h}
    <ol class="after-send" aria-label="送ったあとの流れ">
      <li><b>1</b><span>内容を確かめます</span></li>
      <li><b>2</b><span>担当者からお電話かメールでご連絡</span></li>
      <li><b>3</b><span>現地を見てお見積り（無料）</span></li>
    </ol>
    <div class="formwrap">
      <form class="form" action="{r}contact/thanks/" method="post" data-demo>
        <fieldset class="field">
          <legend>何についてのご相談ですか</legend>
          <div class="pills">{radios}</div>
        </fieldset>
        <label class="field"><span>お名前<em>必須</em></span><input type="text" name="name" autocomplete="name" required></label>
        <label class="field"><span>電話番号（携帯可）<em>必須</em></span><input type="tel" name="tel" autocomplete="tel" inputmode="tel" required></label>
        <label class="field"><span>メールアドレス<em>必須</em></span><input type="email" name="email" autocomplete="email" required></label>
        <label class="field"><span>ご相談の内容<em class="opt">任意</em></span><textarea name="body" rows="5" placeholder="例）事務所の天井のエアコンが古く、入れ替えを考えています"></textarea></label>
        <label class="agree"><input type="checkbox" required> <a href="{r}privacy/" target="_blank">プライバシーポリシー</a>を読んで、同意します</label>
        <button class="btn btn--main btn--wide" type="submit">この内容で送る</button>
        <p class="form__demo">これはデモサイトです。押しても送信されません。お急ぎの方は <a href="tel:{TEL_RAW}">{TEL}</a> へ。</p>
      </form>
      <aside class="formside">
        <p class="formside__t">お電話でも受け付けています</p>
        <a class="formside__tel" href="tel:{TEL_RAW}">{TEL}</a>
        <p>FAX {FAX}</p>
        {tbd("電話を受けられる時間と定休日（旧サイトに記載なし）")}
        <ul class="formside__note">
          <li>docomo・au・softbank など携帯会社のメールアドレスだと、返信が届かないことがあります。困ったときはお電話ください。</li>
          <li>半角カナは文字化けすることがあるので、全角でご入力ください。</li>
        </ul>
      </aside>
    </div>"""
