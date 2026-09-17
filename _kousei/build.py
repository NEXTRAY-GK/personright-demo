#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""パーソンライト 第4版（構成のやり直し）— 全ページを書き出す。

   $ python _kousei/build.py
   事実（機種・リース・求人・お客様の声・施工実績）は _build/ の第3版のデータをそのまま読む。
   ここで足したのは並びと導線だけ。事実が手元に無い所は tbd() で「要確認」と出す。

   手本 propagateinc.com との対応
     トップ        … ヒーロー → 理念 → 写真の帯 → 事業（まとまりごと）→ 体制3点 → 声と実績 → 会社と採用 → 発信 → お問い合わせ
     事業のページ  … ヒーロー＋CTA → 目次 → 中身 → 途中のCTA → 選ぶ → 払う → 流れ（誰が何をするか）→ 付けたあと
                     → 声 → 事例 → 一緒に頼めること → よくある質問 → 運営会社 → ページの中のフォーム
     会社案内      … 概要 → 沿革 → 理念 → 代表 → メンバー → アクセス → お問い合わせ
     採用          … ヒーロー（求人を見る／人を知る）→ 理念 → 数字 → 仕事を知る → 人を知る → 職種 → よくある質問 → エントリー
     よくある質問  … テーマから探す → すべての質問 → 解決しない場合は
"""
import io, os, re, sys, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(ROOT, "_build"))

from parts import (head, header, footer, page_hero, sec_head, tbd, cta_pair, mid_cta, jsonld, faq_ld, acc,
                   inquiry_form, crumb, R, q, SITE, TEL, TEL_RAW, FAX, ZIP, ADDR, INSTA, MAP, COMPANY_SUB)
import p_ac, p_office, p_company, p_recruit, p_reviews, p_works  # 第3版のデータだけを使う

TYPES, CASES, MERITS, CAUTIONS, FLOW, AC_FAQ, GEN = p_ac.TYPES, p_ac.CASES, p_ac.MERITS, p_ac.CAUTIONS, p_ac.FLOW, p_ac.FAQ, p_ac.GEN
CAM, FUJI, ITEMS = p_office.CAM, p_office.FUJI, p_office.ITEMS
OUTLINE_HIST, STAFF = p_company.HIST, p_company.STAFF
JOBS, VOICES, WORKS, KIND, PARTS = p_recruit.JOBS, p_reviews.VOICES, p_works.WORKS, p_works.KIND, p_works.PARTS

ENV = ["業務用エアコン", "家庭用エアコン", "空気清浄機", "LED照明", "分解・洗浄クリーニング", "エコキュート",
       "高機能換気設備", "業務用冷蔵庫・冷凍庫", "各種厨房機器"]
TEL_BIZ = ["ビジネスフォン", "複合機", "セキュリティ商材", "PC周辺設備", "防犯カメラ", "UTM", "サーバー"]
KOJI = ["各種工事", "電気工事", "水回り工事"]


def fmt(d):
    return f"{d[:4]}.{d[4:6]}.{d[6:]}"


def voice_cards(depth, ids=None, n=None):
    r = R(depth)
    vs = [v for v in VOICES if ids is None or v["id"] in ids]
    if n:
        vs = vs[:n]
    return '<ul class="cards cards--3">' + "".join(f"""
      <li class="card card--voice">
        <a href="{r}reviews/{v['id']}/">
          <img src="{r}assets/img/{v['img']}" alt="{v['alt']}" width="{v['w']}" height="{v['h']}" loading="lazy">
          <div class="card__b">
            <p class="card__who">{v['who']}</p>
            <p class="card__t">「{v['title']}」</p>
            <span class="more">お客様の声を読む</span>
          </div>
        </a>
      </li>""" for v in vs) + "</ul>"


def work_cards(depth, items):
    r = R(depth)
    return '<ul class="cards cards--3">' + "".join(f"""
      <li class="card" id="w{w['d']}">
        <img src="{r}assets/img/works-{w['d']}.jpg" alt="{KIND[w['kind']]}の現場写真（{fmt(w['d'])} にInstagramへ載せた物）" width="640" height="{w['h']}" loading="lazy">
        <div class="card__b">
          <p class="tag">{KIND[w['kind']]}</p>
          <p class="card__t">{w['title']}</p>
          <p>{w['text']}</p>
          <p class="card__meta">写っている物：{"・".join(PARTS[p] for p in w['parts'])}</p>
          <p class="card__meta">{fmt(w['d'])} にInstagramへ載せた写真 ／ <a href="{w['post']}" target="_blank" rel="noopener">投稿を見る</a></p>
        </div>
      </li>""" for w in items) + "</ul>"


def job_cards(depth, exclude=None):
    r = R(depth)
    return '<ul class="cards cards--2">' + "".join(f"""
      <li class="card card--job">
        <a href="{r}recruit/{j['id']}/">
          <img src="{r}assets/img/{j['img']}" alt="{j['alt']}" width="720" height="516" loading="lazy">
          <div class="card__b">
            <p class="tag">{j['type']}</p>
            <p class="card__t">{j['name']}</p>
            <p>{j['summary']}</p>
            <p class="card__pay">{j['pay']}</p>
            <span class="more">募集要項を見る</span>
          </div>
        </a>
      </li>""" for j in JOBS if j["id"] != exclude) + "</ul>"


def company_mini(depth):
    r = R(depth)
    return f"""<section class="sec sec--tint" id="company">
  <div class="wrap">
    {sec_head("COMPANY", "運営会社", "株式会社パーソンライト")}
    <dl class="dl">
      <div><dt>社名</dt><dd>株式会社パーソンライト</dd></div>
      <div><dt>代表者</dt><dd>代表取締役社長　増子 佑</dd></div>
      <div><dt>設立</dt><dd>令和4年12月28日（創業 2020年5月）</dd></div>
      <div><dt>本社</dt><dd>{ZIP}　{ADDR}</dd></div>
      <div><dt>事業内容</dt><dd>空調・通信機器販売、各種設備工事、テレマーケティング事業</dd></div>
    </dl>
    <p class="more-line"><a class="more" href="{r}company/">会社案内を見る</a></p>
  </div>
</section>"""


def page(title, desc, depth, here, body, band=True, band_title=None, band_topic=None, ld=None, cls=""):
    return (head(title, desc, depth, cls or "p-" + here) + (ld or "") + header(depth, here) + body
            + footer(depth, band, band_title, band_topic))


# ================================================================= 料金の比べ方（スライダー）
# 2026-09-17、代表の指示「スライダーで簡単な料金比較。複合機とエアコン両方。ワイモバイルのページに近い感じ」。
# 条件を動かすと、右（スマホは上）の結果がその場で変わる。計算は assets/js/kousei.js の sim。
# エアコン … 旧サイトの「冷媒ごとの消費電力（R22を100%）」だけで出す。単価の仮置きは無い。
# 複合機   … 当社の単価が手元に無い。COPIER_OURS は仮の数字。画面にも「仮」と出す。先方の単価が来たらここだけ直す。
COPIER_OURS = {"mono": 1.0, "color": 10.0}   # ⚠️ 仮。根拠なし。要確認


def sim_range(name, label, unit, mn, mx, step, val, hint=""):
    return f"""<div class="sim__row">
        <label class="sim__label" for="{name}">{label}<output class="sim__val" for="{name}" data-out="{name}">{val:,}</output><small>{unit}</small></label>
        <input class="sim__range" type="range" id="{name}" name="{name}" min="{mn}" max="{mx}" step="{step}" value="{val}">
        <p class="sim__scale"><span>{mn:,}{unit}</span><span>{mx:,}{unit}</span></p>
        {f'<p class="sim__hint">{hint}</p>' if hint else ''}
      </div>"""


def sim_ac(depth):
    r = R(depth)
    gens = "".join(f'<label class="seg"><input type="radio" name="gen" value="{p}"{" checked" if i == 0 else ""}><span><b>{c}</b><small>{a}</small></span></label>'
                   for i, (a, b, c, p) in enumerate(GEN))
    return f"""<section class="sec sim-sec" id="sim">
  <div class="wrap">
    {sec_head("SIMULATION", "電気代の比べ方", "替えると、電気代はいくら変わるか。", "いまのエアコンの時期と、毎月の電気代を動かしてみてください。結果はその場で変わります。")}
    <div class="sim" data-sim="ac">
      <div class="sim__in">
        <fieldset class="sim__row">
          <legend class="sim__label">いまのエアコンは、いつ頃の機種ですか</legend>
          <div class="segs">{gens}</div>
          <p class="sim__hint">室外機の銘板に書いてある製造年か、冷媒の名前で選んでください。</p>
        </fieldset>
        {sim_range("bill", "エアコンにかかる電気代（月の平均）", "円", 5000, 150000, 1000, 30000)}
        {sim_range("years", "このあと使う年数", "年", 1, 15, 1, 7, "7年は、取り付けたあとの保証の年数です。")}
        <a class="btn btn--main btn--wide sim-foot" href="#form" data-type="業務用エアコン">この条件で見積りを頼む</a>
      </div>
      <div class="sim__out" aria-live="polite">
        <p class="sim__out-t">替えた場合の目安</p>
        <div class="sim__bars">
          <div class="sim__bar"><span>いま</span><i style="--w:100%"></i><b data-o="now">30,000円</b></div>
          <div class="sim__bar sim__bar--after"><span>替えたあと</span><i data-o="afterW" style="--w:20%"></i><b data-o="after">6,000円</b></div>
        </div>
        <dl class="sim__sum">
          <div><dt>1か月</dt><dd data-o="m">24,000円</dd></div>
          <div><dt>1年</dt><dd data-o="y">288,000円</dd></div>
          <div class="sim__sum-big"><dt data-o="yl">7年</dt><dd data-o="t">2,016,000円</dd></div>
        </dl>
        <p class="sim__msg" data-o="msg">電気代が、これだけ下がる目安です。</p>
        <a class="btn btn--main btn--wide" href="#form" data-type="業務用エアコン">この条件で見積りを頼む</a>
        <p class="sim__note">旧サイトの「冷媒ごとの消費電力（R22を100%としたとき、R407・R410は60%、R32は20%）」から出した目安です。電気の単価や使い方の違い、本体・工事・リースの費用は入っていません。</p>
      </div>
    </div>
    {tbd("機種ごとのリース月額が分かれば、「電気代の差額 − リース月額」まで出せる。冷媒の比率の出どころ（メーカー資料か自社の実測か）も確かめる")}
  </div>
</section>
"""


def sim_copier(depth):
    o = COPIER_OURS
    return f"""<section class="sec sim-sec" id="sim">
  <div class="wrap">
    {sec_head("SIMULATION", "印刷代の比べ方", "いまの印刷代と、比べてみてください。", "毎月の枚数と、いまの請求書に書いてある1枚あたりの単価を動かすと、結果がその場で変わります。")}
    <div class="sim" data-sim="copier" data-our-mono="{o['mono']}" data-our-color="{o['color']}">
      <div class="sim__in">
        <p class="sim__group">毎月、何枚刷っていますか</p>
        {sim_range("mono", "モノクロ", "枚", 0, 20000, 100, 3000)}
        {sim_range("color", "カラー", "枚", 0, 10000, 100, 500)}
        <p class="sim__group">いまの1枚あたりの単価（カウンター料金）</p>
        {sim_range("pmono", "モノクロ", "円", 0.5, 10, 0.1, 3.0)}
        {sim_range("pcolor", "カラー", "円", 3, 60, 1, 20, "請求書の「カウンター料金」「保守料金」の欄に、1枚あたりの単価が書いてあります。")}
        <a class="btn btn--main btn--wide sim-foot" href="#form" data-type="複合機">この条件で見積りを頼む</a>
      </div>
      <div class="sim__out" aria-live="polite">
        <p class="sim__out-t">パーソンライトに替えた場合の目安（当社の単価は仮）</p>
        <div class="sim__bars">
          <div class="sim__bar"><span>いま</span><i style="--w:100%"></i><b data-o="now">0円</b></div>
          <div class="sim__bar sim__bar--after"><span>替えたあと</span><i data-o="afterW" style="--w:50%"></i><b data-o="after">0円</b></div>
        </div>
        <dl class="sim__sum">
          <div><dt>1か月</dt><dd data-o="m">0円</dd></div>
          <div><dt>1年</dt><dd data-o="y">0円</dd></div>
          <div class="sim__sum-big"><dt>5年</dt><dd data-o="t">0円</dd></div>
        </dl>
        <p class="sim__msg" data-o="msg"></p>
        <a class="btn btn--main btn--wide" href="#form" data-type="複合機">この条件で見積りを頼む</a>
        <p class="sim__note sim__note--warn">当社の単価（モノクロ {o['mono']:.1f}円・カラー {o['color']:.1f}円）は<b>仮の数字</b>です。本体・リース・基本料金は入っていません。</p>
      </div>
    </div>
    {tbd("当社の1枚あたりの単価（モノクロ・カラー）と、月額の基本料金・リース料。いまは仮の数字で動かしている")}
  </div>
</section>
"""


# ================================================================= トップ
def build_top():
    d = 0
    r = R(d)
    strip = "".join(
        f'<li><img src="{r}assets/img/{f}" alt="{a}" width="{w}" height="{h}" loading="lazy"></li>'
        for f, w, h, a in [
            ("case-install01.jpg", 640, 800, "天井を開けて作業する工事スタッフ"),
            ("works-20251202.jpg", 640, 800, "入れ替えた天井カセット形エアコン"),
            ("case-shop.jpg", 780, 611, "店舗の天井に設置した天井カセット形エアコン"),
            ("works-20251203.jpg", 640, 800, "分解して洗った天井カセット形エアコン"),
            ("case-install02.jpg", 640, 480, "外壁に据え付けた室外機"),
            ("works-20251212.jpg", 640, 800, "入れ替えた天井吊形エアコン"),
            ("case-house.jpg", 640, 427, "工場の外壁に並べた室外機7台"),
        ])

    body = f"""
<section class="hero" id="top">
  <div class="wrap hero__in">
    <div class="hero__t">
      <p class="en">福島県郡山市　業務用エアコンの販売・取り付け・リース</p>
      <h1><span class="nw">業務用エアコンの入れ替えを、</span><span class="nw">選ぶところから、</span><span class="nw">付けたあとまで。</span></h1>
      <p class="lead">5社のメーカー・12種類から部屋に合う一台を選び、自社の工事部が取り付けます。付けたあとは7年保証と年間メンテナンス。リースなら初期費用はかかりません。</p>
      {cta_pair(d, "業務用エアコン")}
    </div>
    <figure class="hero__fig"><img src="{r}assets/img/hero.jpg" alt="業務用エアコンを取り付けた部屋" width="1600" height="771" fetchpriority="high"></figure>
  </div>
  <nav class="quick wrap" aria-label="ご用件から探す">
    <p class="quick__t">ご用件から探す</p>
    <ul>
      <li><a href="{r}ac/"><b>エアコンを入れ替えたい・新しく付けたい</b><span>業務用エアコン</span></a></li>
      <li><a href="{r}ac/#pay"><b>まとまったお金を出さずに入れたい</b><span>リース</span></a></li>
      <li><a href="{r}ac/#after"><b>効きが悪い・中を洗いたい</b><span>分解・洗浄クリーニング</span></a></li>
      <li><a href="{r}office-tech/"><b>防犯カメラ・複合機・電話を替えたい</b><span>通信機器</span></a></li>
    </ul>
  </nav>
</section>

<section class="sec" id="mission">
  <div class="wrap narrow">
    {sec_head("PHILOSOPHY", "企業理念", "サービス＆貢献", center=True)}
    <p class="big-text">「パーソンライトに相談して良かった！」と心の底からお喜び頂けるよう、お客様が求めているサービスを展開し、笑顔や喜びにあふれた社会づくりを目指しています。</p>
    <p class="more-line center"><a class="more" href="{r}company/#philosophy">会社案内で読む</a></p>
  </div>
</section>

<section class="photostrip" aria-label="現場の写真"><ul>{strip}</ul></section>

<section class="sec sec--tint" id="service">
  <div class="wrap">
    {sec_head("SERVICE", "事業紹介", "4つの事業を、1つの会社でやっています。", "エアコンの相談のついでに、電話機や複合機、電気や水回りの工事のことを聞いていただいても構いません。")}
    <div class="svc">
      <div class="svc__group">
        <p class="svc__label"><b>01</b>環境事業</p>
        <a class="svc__main" href="{r}ac/">
          <img src="{r}assets/img/case-shop.jpg" alt="店舗の天井に設置した業務用エアコン" width="780" height="611" loading="lazy">
          <div>
            <small>5メーカー・12種類から選べる</small>
            <b>業務用エアコン</b>
            <p>機種選びから取り付け、リース、7年保証と年間メンテナンスまで。</p>
            <span class="more">詳しく見る</span>
          </div>
        </a>
        <p class="svc__also">ほかに扱っている物</p>
        <ul class="taglist">{"".join(f"<li>{x}</li>" for x in ENV[1:])}</ul>
      </div>
      <div class="svc__group">
        <p class="svc__label"><b>02</b>通信事業</p>
        <a class="svc__main" href="{r}office-tech/">
          <img src="{r}assets/img/cam-hero.jpg" alt="防犯カメラ" width="1600" height="587" loading="lazy">
          <div>
            <small>事務所の機器をまとめて</small>
            <b>通信機器</b>
            <p>夜もカラーで撮れる防犯カメラ、富士フイルムの複合機、ビジネスフォン。</p>
            <span class="more">詳しく見る</span>
          </div>
        </a>
        <ul class="taglist">{"".join(f"<li>{x}</li>" for x in TEL_BIZ)}</ul>
      </div>
      <div class="svc__group">
        <p class="svc__label"><b>03</b>工事部</p>
        <div class="svc__sub">
          <b>各種工事・電気工事・水回り工事</b>
          <p>エアコンの取り付けも、電気や水回りの工事も、自社の工事部でお受けします。</p>
          <a class="more" href="{r}contact/{q('工事')}">工事の相談をする</a>
        </div>
      </div>
      <div class="svc__group">
        <p class="svc__label"><b>04</b>テレマーケティング事業</p>
        <div class="svc__sub">
          <b>アポイント</b>
          {tbd("何をお受けしている事業か（旧サイトは項目名だけ）。社外から頼める物でなければ、ここから外す")}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="support">
  <div class="wrap">
    {sec_head("SUPPORT", "パーソンライトの体制", "選ぶ・付ける・見守るを、自社で。")}
    <ol class="points">
      <li><p class="points__no">POINT 01</p><b>現地を見てから<br>無料でお見積り</b><p>スタッフがうかがって取り付ける場所を見てから、機種と工事のやり方を決めます。</p></li>
      <li><p class="points__no">POINT 02</p><b>取り付けは<br>自社の工事部</b><p>ダイキンをはじめ5社のメーカーの機種を、自社の工事部が取り付けます。</p></li>
      <li><p class="points__no">POINT 03</p><b>付けたあとも<br>7年保証</b><p>引き渡しのあとは、7年保証と年間メンテナンスが始まります。</p></li>
    </ol>
  </div>
</section>

<section class="sec sec--tint" id="voice">
  <div class="wrap">
    {sec_head("VOICE", "お客様の声", "工事のあとに、いただいた声です。")}
    {voice_cards(d, n=3)}
    <p class="more-line"><a class="more" href="{r}reviews/">お客様の声をすべて読む（{len(VOICES)}件）</a></p>
    <div class="nums">
      <div><small>取り扱いメーカー</small><b>5<span>社</span></b><p>ダイキン・三菱電機・日立・東芝・パナソニック</p></div>
      <div><small>選べる機種の形</small><b>12<span>種類</span></b><p>天井カセット形から厨房用まで</p></div>
      <div><small>保証</small><b>7<span>年</span></b><p>年間メンテナンスもご用意</p></div>
    </div>
    {tbd("施工件数・年間の施工本数・お取引先の名前（載せてよい物）。手本はここに累計の件数と取引先の一覧を置いている。数字が一番効く場所")}
  </div>
</section>

<section class="sec" id="about">
  <div class="wrap">
    {sec_head("ABOUT", "パーソンライトについて", "会社を知る。一緒に働く人を知る。")}
    <ul class="cards cards--2">
      <li class="card card--big"><a href="{r}company/">
        <img src="{r}assets/img/office-front.jpg" alt="本社の外観" width="810" height="555" loading="lazy">
        <div class="card__b"><p class="en">COMPANY</p><p class="card__t">会社案内</p><p>会社概要・沿革・企業理念・代表あいさつ・スタッフ・アクセス。</p><span class="more">詳しく見る</span></div>
      </a></li>
      <li class="card card--big"><a href="{r}recruit/">
        <img src="{r}assets/img/recruit03.jpg" alt="天井のエアコンを点検する工事スタッフ" width="720" height="516" loading="lazy">
        <div class="card__b"><p class="en">RECRUIT</p><p class="card__t">採用情報</p><p>工事スタッフ・営業職・テレフォンアポインター・管理職責任者の4職種を募集しています。</p><span class="more">詳しく見る</span></div>
      </a></li>
    </ul>
  </div>
</section>

<section class="sec sec--tint" id="media">
  <div class="wrap">
    {sec_head("MEDIA", "現場の記録", "どんな現場を、どう仕上げているか。")}
    <ul class="cards cards--2">
      <li class="card card--row"><a href="{r}works/">
        <img src="{r}assets/img/works-20251204.jpg" alt="入れ替えた天井吊形エアコン" width="640" height="800" loading="lazy">
        <div class="card__b"><p class="card__t">施工実績</p><p>入れ替え工事と高圧分解洗浄の現場を、写真で紹介しています。</p><span class="more">施工実績を見る</span></div>
      </a></li>
      <li class="card card--row"><a href="{INSTA}" target="_blank" rel="noopener">
        <img src="{r}assets/img/works-20251211.jpg" alt="分解して洗った天井カセット形エアコン" width="640" height="800" loading="lazy">
        <div class="card__b"><p class="card__t">Instagram</p><p>新しい現場は @personright501 で載せています。</p><span class="more">Instagram を開く</span></div>
      </a></li>
    </ul>
  </div>
</section>
"""
    return page("株式会社パーソンライト｜業務用エアコンの販売・取り付け・リース（福島県郡山市）",
                "福島県郡山市の株式会社パーソンライト。5社のメーカー・12種類から業務用エアコンを選び、自社の工事部が取り付けます。7年保証と年間メンテナンス、リースなら初期費用0円。防犯カメラ・複合機・ビジネスフォンも。",
                d, "top", body, band_topic="業務用エアコン", ld=jsonld())


# ================================================================= 業務用エアコン
def build_ac():
    d = 1
    r = R(d)
    chips = [("reason", "替えどき"), ("sim", "電気代の比べ方"), ("types", "機種を選ぶ"), ("pay", "お支払い"), ("flow", "流れ"),
             ("after", "付けたあと"), ("voice", "お客様の声"), ("works", "施工事例"), ("faq", "よくある質問"),
             ("form", "お見積り")]
    hero = page_hero(d, "AIR CONDITIONER", "業務用エアコンの販売・取り付け・リース",
                     "機種を選ぶところから、支払い方、取り付け、付けたあとのことまで、まとめてお任せください。",
                     [("業務用エアコン", None)],
                     actions=f"""<ul class="badges"><li><b>5メーカー・12種類</b>から選べる</li><li><b>自社の工事部</b>が取り付け</li><li><b>7年保証</b>と年間メンテナンス</li><li>リースなら<b>初期費用0円</b></li></ul>
    <div class="cta-pair"><a class="btn btn--main" href="#form">無料で見積りを頼む</a><a class="btn btn--line" href="tel:{TEL_RAW}">電話で相談する　{TEL}</a></div>""",
                     chips=chips)
    gen = "".join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td><td><span class="bar" style="--w:{p}%"></span>{p}%</td></tr>' for a, b, c, p in GEN)
    types = "".join(f"""<li class="type"><img src="{r}assets/img/ac-type{no}.jpg" alt="{name}（{kind}）" width="720" height="511" loading="lazy"><b>{name}</b><span>{kind}</span></li>""" for no, name, kind in TYPES)
    cases = "".join(f"<li>{c}</li>" for c in CASES)
    merits = "".join(f"<li><b>{t}</b><p>{x}</p></li>" for t, x in MERITS)
    cautions = "".join(f"<li><b>{t}</b><p>{x}</p></li>" for t, x in CAUTIONS)
    who = ["お客様", "パーソンライト", "パーソンライト", "お客様", "パーソンライト"]
    flow = "".join(f"""<li><p class="flow__who flow__who--{'you' if w == 'お客様' else 'us'}">{w}</p><p class="flow__no">STEP {i+1}</p><b>{t}</b><p>{x}</p></li>""" for i, ((t, x), w) in enumerate(zip(FLOW, who)))
    swaps = [w for w in WORKS if w["kind"] == "swap"][:3]
    faq_groups = [
        ("リースのこと", [AC_FAQ[0], AC_FAQ[1], AC_FAQ[3]]),
        ("修理と保証のこと", [AC_FAQ[2]]),
        ("お支払いのこと", [AC_FAQ[4]]),
    ]
    faq_html = "".join(f'<h3 class="qa-h">{g}</h3>{acc(ps)}' for g, ps in faq_groups)

    body = f"""{hero}
<section class="sec" id="reason">
  <div class="wrap">
    {sec_head("REASON", "替えどき", "替えどきを決めるのは、電気代とガスです。", "2011年3月の東日本大震災のあと、電気代は上がり続けてきました。そのあいだに業務用エアコンの省エネは大きく進んでいます。")}
    <div class="nums">
      <div><small>最新の省エネ機種に替えると</small><b>最大70<span>%</span></b><p>消費電力が減ります</p></div>
      <div><small>15年前の機種と比べると</small><b>65<span>%</span></b><p>消費電力が減ります</p></div>
      <div><small>18年前の機種と比べると</small><b>80<span>%</span></b><p>消費電力が減ります</p></div>
    </div>
    <h3 class="h3">R22の機種は、ガスがあるうちに入れ替えを。</h3>
    <p>2001年より前の機種に使われているR22（指定フロン）は、もう生産も輸入もされていません。壊れたときに修理用のガスが手に入らない、ということになる前に、早めの入れ替えをおすすめします。</p>
    <table class="tbl"><caption>冷媒ごとの消費電力（R22を100%としたとき）</caption><thead><tr><th>冷媒</th><th>種類</th><th>使われた時期</th><th>消費電力</th></tr></thead><tbody>{gen}</tbody></table>
  </div>
</section>

{sim_ac(d)}

{mid_cta(d, "いまお使いの一台を、見せてください。", "入れ替えか、クリーニングで済むか。現地を見てからお答えします。お見積りは無料です。", "業務用エアコン")}

<section class="sec sec--tint" id="types">
  <div class="wrap">
    {sec_head("LINEUP", "機種を選ぶ", "12種類の中から、部屋に合う一台を。", "天井に埋め込む形、吊るす形、壁掛け、床置き、厨房用まであります。置く場所や広さ、天井のつくりを見てお選びします。")}
    <p class="makers"><b>取り扱いメーカー</b>ダイキン／三菱電機／日立／東芝／パナソニック</p>
    <ul class="types">{types}</ul>
    <h3 class="h3">お店や会社によって、合う形は変わります。</h3>
    <ul class="taglist taglist--lg">{cases}</ul>
  </div>
</section>

<section class="sec" id="pay">
  <div class="wrap">
    {sec_head("PAYMENT", "お支払い", "リースなら、初期費用はかかりません。", "現金での購入や、クレジットの分割払いもできます。")}
    {tbd("機種ごと・部屋の広さごとの金額の目安（リースの月額と、買う場合の総額）。手本はここに料金表を置いている。金額の目安が見えると、見積りの前に離れる人が減る")}
    <h3 class="h3">リースの良いところ</h3>
    <ul class="grid4">{merits}</ul>
    <h3 class="h3">ご契約の前に、ここは必ず確かめてください</h3>
    <ul class="grid3 grid3--warn">{cautions}</ul>
    {tbd("再リースの料金が2か所で合わない（上の注意「年間リース額の10分の1」／よくある質問「月額リース料の2倍」＝年額の6分の1）。旧サイトの数字のまま")}
  </div>
</section>

<section class="sec sec--tint" id="flow">
  <div class="wrap">
    {sec_head("PROCESS", "流れ", "ご相談から取り付けまで、5つの手順です。", "リースの審査や契約の手続きも、当社とリース会社でお手伝いします。現金で購入する場合は、STEP 3・4 はありません。")}
    <ol class="flow">{flow}</ol>
    {tbd("ご相談から取り付けまでの日数の目安")}
  </div>
</section>

<section class="sec" id="after">
  <div class="wrap">
    {sec_head("AFTER", "付けたあと", "付けて終わりにしません。")}
    <ul class="grid3">
      <li><b>7年保証</b><p>引き渡しのあとから、7年間の保証が始まります。</p></li>
      <li><b>年間メンテナンス</b><p>付けたあとの点検のために、年間メンテナンスをご用意しています。</p></li>
      <li><b>分解・洗浄クリーニング</b><p>部品を外して、水の勢いで奥まで洗い流します。効きが悪いときは、入れ替えの前に一度ご相談ください。 <a href="{r}works/#wash">洗浄の現場を見る</a></p></li>
    </ul>
    {tbd("年間メンテナンスの中身と料金、保証の範囲")}
  </div>
</section>

<section class="sec sec--tint" id="voice">
  <div class="wrap">
    {sec_head("VOICE", "お客様の声", "工事のあとに、いただいた声です。")}
    {voice_cards(d, ids=["98", "96", "53"])}
    <p class="more-line"><a class="more" href="{r}reviews/">お客様の声をすべて読む</a></p>
  </div>
</section>

<section class="sec" id="works">
  <div class="wrap">
    {sec_head("WORKS", "施工事例", "入れ替え工事の現場です。")}
    {work_cards(d, swaps)}
    <p class="more-line"><a class="more" href="{r}works/">施工実績をすべて見る</a></p>
  </div>
</section>

<section class="sec sec--tint" id="options">
  <div class="wrap">
    {sec_head("OPTIONS", "一緒に頼めること", "エアコンと一緒に、まとめてご相談ください。")}
    <ul class="grid4 grid4--link">
      <li><a href="{r}contact/{q('クリーニング')}"><b>分解・洗浄クリーニング</b><p>効きが悪い・においが気になるとき</p></a></li>
      <li><a href="{r}contact/{q('工事')}"><b>電気工事・水回り工事</b><p>自社の工事部でお受けします</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>LED照明・換気設備</b><p>高機能換気設備も扱っています</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>業務用冷蔵庫・厨房機器</b><p>冷凍庫・各種厨房機器も</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>家庭用エアコン・エコキュート</b><p>ご自宅のことも</p></a></li>
      <li><a href="{r}office-tech/"><b>防犯カメラ・複合機・電話</b><p>通信機器のページへ</p></a></li>
    </ul>
  </div>
</section>

<section class="sec" id="faq">
  <div class="wrap narrow">
    {sec_head("FAQ", "よくある質問", "業務用エアコンの、よくいただく質問です。")}
    {faq_html}
    <p class="more-line"><a class="more" href="{r}faq/">ほかの質問を見る</a></p>
  </div>
</section>

{company_mini(d)}

<section class="sec" id="form">
  <div class="wrap">
    {inquiry_form(d, "業務用エアコン")}
  </div>
</section>
"""
    return page("業務用エアコンの販売・取り付け・リース｜株式会社パーソンライト",
                p_ac.DESC, d, "ac", body, band=False, ld=jsonld([faq_ld(AC_FAQ)]))


# ================================================================= 通信機器
def build_office():
    d = 1
    r = R(d)
    chips = [("items", "取り扱い機器"), ("camera", "防犯カメラ"), ("copier", "複合機"), ("sim", "印刷代の比べ方"), ("flow", "流れ"),
             ("options", "一緒に頼めること"), ("form", "お見積り")]
    hero = page_hero(d, "OFFICE TECH", "防犯カメラ・複合機・ビジネスフォン",
                     "電話機や複合機、防犯カメラ、UTM、サーバーも扱っています。どれを選べばいいかの相談から取り付けまで、まとめてお任せください。",
                     [("通信機器", None)],
                     actions=f"""<div class="cta-pair"><a class="btn btn--main" href="#form">無料で見積りを頼む</a><a class="btn btn--line" href="tel:{TEL_RAW}">電話で相談する　{TEL}</a></div>""",
                     chips=chips)
    cams = "".join(f"""<li class="card"><img src="{r}assets/img/{f}" alt="{t}で夜に撮った映像" width="{w}" height="{h}" loading="lazy"><div class="card__b"><p class="tag">{'当社で扱っているカメラ' if i == 2 else '比べる物'}</p><p class="card__t">{t}</p><p>{x}</p></div></li>""" for i, (f, w, h, t, x) in enumerate(CAM))
    fuji = "".join(f"<li><b>{t}</b><p>{x}</p></li>" for t, x in FUJI)
    body = f"""{hero}
<section class="sec" id="items">
  <div class="wrap">
    {sec_head("LINEUP", "取り扱い機器", "事務所の機器のことも、まとめてご相談ください。")}
    <ul class="grid4 grid4--link">
      <li><a href="#camera"><b>防犯カメラ</b><p>夜もカラーで撮れるカメラ</p></a></li>
      <li><a href="#copier"><b>複合機</b><p>富士フイルム。印刷代の比べ方も</p></a></li>
      <li><a href="{r}contact/{q('ビジネスフォン')}"><b>ビジネスフォン</b><p>相談する</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>セキュリティ商材・UTM</b><p>相談する</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>PC周辺設備・サーバー</b><p>相談する</p></a></li>
    </ul>
    {tbd("ビジネスフォン・UTM・サーバーの扱いメーカーと中身（旧サイトは名前だけ）。中身があれば、防犯カメラ・複合機と同じ形で節を足す")}
  </div>
</section>

<section class="sec sec--tint" id="camera">
  <div class="wrap">
    {sec_head("SECURITY CAMERA", "防犯カメラ", "夜の映像で、比べてみてください。", "同じ場所を、夜に3種類のカメラで撮った映像です。当社で扱っているのは、夜でもカラーで撮れるカメラです。")}
    <ul class="cards cards--3">{cams}</ul>
    <h3 class="h3">値段であきらめた方にも、もう一度見てほしい。</h3>
    <p>以前に防犯カメラを考えたものの、値段を見て見送った方もいらっしゃると思います。一度、当社の条件と比べてみてください。夜のカラー撮影のほか、動くものを見つけて知らせる機能や、離れた場所からの操作にも対応しています。</p>
    {tbd("台数ごとの金額の目安")}
  </div>
</section>

{mid_cta(d, "付けたい場所と、困っていることを聞かせてください。", "お仕事の内容や取り付ける場所をうかがってから、機種と取り付け方をご提案します。", "防犯カメラ")}

<section class="sec" id="copier">
  <div class="wrap">
    {sec_head("COPIER", "複合機", "複合機は、富士フイルムを扱っています。", "J.D.パワーの顧客満足度調査で、9年連続1位になった複合機です。")}
    {tbd("「9年連続1位」の調査名と年（年が変わると書き換えが要る）")}
    <ul class="grid4">{fuji}</ul>
  </div>
</section>

{sim_copier(d)}

<section class="sec sec--tint" id="flow">
  <div class="wrap">
    {sec_head("PROCESS", "流れ", "ご相談から取り付けまで。")}
    <ol class="flow">
      <li><p class="flow__who flow__who--you">お客様</p><p class="flow__no">STEP 1</p><b>ご相談</b><p>お電話かフォームで、気軽にご連絡ください。お見積りは無料です。</p></li>
      <li><p class="flow__who flow__who--us">パーソンライト</p><p class="flow__no">STEP 2</p><b>お話をうかがう</b><p>お仕事の内容や取り付ける場所、何のために付けたいのかをうかがいます。</p></li>
      <li><p class="flow__who flow__who--us">パーソンライト</p><p class="flow__no">STEP 3</p><b>ご提案</b><p>機種と取り付け方をご提案します。</p></li>
      <li><p class="flow__who flow__who--us">パーソンライト</p><p class="flow__no">STEP 4</p><b>取り付け</b><p>取り付けまで、まとめてお任せください。</p></li>
    </ol>
  </div>
</section>

<section class="sec" id="options">
  <div class="wrap">
    {sec_head("OPTIONS", "一緒に頼めること", "事務所のことは、まとめてご相談ください。")}
    <ul class="grid4 grid4--link">
      <li><a href="{r}ac/"><b>業務用エアコン</b><p>5メーカー・12種類から</p></a></li>
      <li><a href="{r}contact/{q('工事')}"><b>電気工事</b><p>自社の工事部で</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>LED照明</b><p>省エネの相談も</p></a></li>
    </ul>
  </div>
</section>

{company_mini(d)}

<section class="sec" id="form">
  <div class="wrap">
    {inquiry_form(d)}
  </div>
</section>
"""
    return page("防犯カメラ・複合機・ビジネスフォン｜株式会社パーソンライト", p_office.DESC, d, "office-tech", body,
                band=False, ld=jsonld())


# ================================================================= 施工実績
def build_works():
    d = 1
    r = R(d)
    swap = [w for w in WORKS if w["kind"] == "swap"]
    wash = [w for w in WORKS if w["kind"] == "wash"]
    body = f"""{page_hero(d, "WORKS", "施工実績", "業務用エアコンの入れ替え工事と、高圧分解洗浄の現場です。写真は2025年12月にInstagramへ載せた物です。", [("施工実績", None)],
                      chips=[("swap", f"入れ替え工事（{len(swap)}件）"), ("wash", f"高圧分解洗浄（{len(wash)}件）")])}
<section class="sec" id="swap">
  <div class="wrap">
    {sec_head("REPLACEMENT", "入れ替え工事", f"エアコンの入れ替え工事　{len(swap)}件")}
    {work_cards(d, swap)}
  </div>
</section>
{mid_cta(d, "同じような入れ替えを考えている方へ。", "現地を見てからお見積りします。無料です。", "業務用エアコン")}
<section class="sec sec--tint" id="wash">
  <div class="wrap">
    {sec_head("CLEANING", "高圧分解洗浄", f"高圧分解洗浄　{len(wash)}件", "エアコンは使っているうちに、中のフィンやファンにほこりや汚れがたまっていきます。部品を外して、水の勢いで奥まで洗い流します。")}
    {work_cards(d, wash)}
    <p class="more-line"><a class="btn btn--line" href="{r}contact/{q('クリーニング')}">クリーニングの相談をする</a></p>
  </div>
</section>
<section class="sec" id="insta">
  <div class="wrap narrow center">
    {sec_head("INSTAGRAM", "新しい現場", "このほかの現場は、Instagramで。", center=True)}
    <p><a class="btn btn--line" href="{INSTA}" target="_blank" rel="noopener">Instagram を開く（@personright501）</a></p>
    {tbd("業種・地域・工事の中身が分かる事例を、写真と一緒に数件（手本は業種ごとに事例を並べている）")}
  </div>
</section>
"""
    return page("施工実績｜株式会社パーソンライト", p_works.DESC, d, "works", body, ld=jsonld())


# ================================================================= お客様の声
def build_reviews():
    d = 1
    body = f"""{page_hero(d, "VOICE", "お客様の声", f"工事のあとに、お客様からいただいた声です（{len(VOICES)}件）。", [("お客様の声", None)])}
<section class="sec">
  <div class="wrap">
    {voice_cards(d)}
    {tbd("新しい声と、写真付きの声。業種と、何を頼んだか（入れ替え・リース・クリーニングなど）が分かると、読む人が自分と重ねやすい")}
  </div>
</section>
{mid_cta(d, "同じように相談してみませんか。", "お見積りは無料です。", "業務用エアコン")}
"""
    return page("お客様の声｜株式会社パーソンライト",
                "株式会社パーソンライトで業務用エアコンの設置・入れ替えをされたお客様の声です。福島県郡山市・田村市・須賀川市。",
                d, "reviews", body, ld=jsonld())


def build_review(i, v):
    d = 2
    r = R(d)
    prev_v = VOICES[i - 1] if i > 0 else None
    next_v = VOICES[i + 1] if i + 1 < len(VOICES) else None
    pn = '<nav class="pn" aria-label="前後の声">'
    pn += f'<a class="pn__prev" href="{r}reviews/{prev_v["id"]}/"><small>前の声</small>{prev_v["title"]}</a>' if prev_v else "<span></span>"
    pn += f'<a class="pn__next" href="{r}reviews/{next_v["id"]}/"><small>次の声</small>{next_v["title"]}</a>' if next_v else "<span></span>"
    pn += "</nav>"
    body = f"""{crumb(d, [("お客様の声", "reviews/"), (v["title"], None)])}
<article class="sec">
  <div class="wrap narrow">
    <p class="en">VOICE</p>
    <h1 class="h1">「{v['title']}」</h1>
    <p class="card__who">{v['who']}</p>
    <figure class="fig"><img src="{r}assets/img/{v['img']}" alt="{v['alt']}" width="{v['w']}" height="{v['h']}"></figure>
    {"".join(f"<p>{p}</p>" for p in v['body'])}
    <div class="related">
      <p>この声に関わる事業</p>
      <a class="more" href="{r}ac/">業務用エアコン</a>
    </div>
    {pn}
    <p class="more-line center"><a class="more" href="{r}reviews/">お客様の声の一覧へ</a></p>
  </div>
</article>
"""
    return page(f"{v['title']}｜お客様の声｜株式会社パーソンライト", f"{v['who']}の声。" + v["body"][0][:80], d, "reviews", body)


# ================================================================= 会社案内
def build_company():
    d = 1
    r = R(d)
    hist = "".join(f"<li><time>{y}</time><p>{x}</p></li>" for y, x in OUTLINE_HIST)
    staff = "".join(f"""<li><img src="{r}assets/img/{f}.jpg" alt="{role}　{n}" width="320" height="320" loading="lazy"><small>{role}</small><b>{n}</b><p>{m}</p></li>""" for f, role, n, m in STAFF)
    body = f"""{page_hero(d, "COMPANY", "会社案内", "2020年に須賀川市で、業務用エアコンの取り付けと保守の会社として始まりました。いまは郡山市に本社があります。", [("会社案内", None)], chips=COMPANY_SUB)}
<section class="sec" id="company-info">
  <div class="wrap">
    {sec_head("PROFILE", "会社概要", "会社のこと")}
    <dl class="dl">
      <div><dt>社名</dt><dd>株式会社パーソンライト</dd></div>
      <div><dt>代表者</dt><dd>代表取締役社長　増子 佑</dd></div>
      <div><dt>本社</dt><dd>{ZIP}　{ADDR}<br>TEL <a href="tel:{TEL_RAW}">{TEL}</a>　FAX {FAX}</dd></div>
      <div><dt>事業内容</dt><dd>空調・通信機器販売、各種設備工事、テレマーケティング事業<br><a class="more" href="{r}#service">事業の一覧を見る</a></dd></div>
      <div><dt>設立</dt><dd>令和4年12月28日</dd></div>
      <div><dt>資本金</dt><dd>300万円</dd></div>
      <div><dt>従業員数</dt><dd>15名</dd></div>
    </dl>
    {tbd("営業時間・定休日／従業員15名とスタッフ紹介18名（広報3匹を含む）の数の違い")}
  </div>
</section>
<section class="sec sec--tint" id="history">
  <div class="wrap">
    {sec_head("HISTORY", "沿革", "これまでの歩み")}
    <ol class="hist">{hist}</ol>
  </div>
</section>
<section class="sec" id="philosophy">
  <div class="wrap narrow">
    {sec_head("PHILOSOPHY", "企業理念", "サービス＆貢献")}
    <p class="big-text">「パーソンライトに相談して良かった！」と心の底からお喜び頂けるよう、お客様が求めているサービスを展開し、笑顔や喜びにあふれた社会づくりを目指しています。</p>
  </div>
</section>
<section class="sec sec--tint" id="message">
  <div class="wrap narrow">
    {sec_head("MESSAGE", "代表あいさつ", "お客様とも、社員とも、一緒に前へ進みたい。")}
    <p>お客様はもちろん、当社の社員含め、パーソンライトに関わる全ての皆様と共に輝かしい未来へ。創造と挑戦の歩みを止めず、日々成長してまいります。</p>
    <p class="sign">代表取締役社長　増子 佑</p>
    {tbd("代表の写真と、創業のきっかけ（手本は代表の経歴と「創業の想い」を別の節で持っている）")}
  </div>
</section>
<section class="sec" id="members">
  <div class="wrap">
    {sec_head("MEMBER", "スタッフ", "一緒に働いているメンバーです。", "環境部、通信機器部、工事部、総務のみんなと、広報を担当している3匹です。")}
    <ul class="staff">{staff}</ul>
    <p class="more-line"><a class="more" href="{r}recruit/">一緒に働く仲間を募集しています</a></p>
  </div>
</section>
<section class="sec sec--tint" id="access">
  <div class="wrap">
    {sec_head("ACCESS", "アクセス", "本社")}
    <dl class="dl">
      <div><dt>住所</dt><dd>{ZIP}　{ADDR}</dd></div>
      <div><dt>電話</dt><dd><a href="tel:{TEL_RAW}">{TEL}</a>　FAX {FAX}</dd></div>
    </dl>
    <p class="more-line"><a class="btn btn--line" href="{MAP}" target="_blank" rel="noopener">Google マップで見る</a></p>
  </div>
</section>
"""
    return page("会社案内｜株式会社パーソンライト", p_company.DESC, d, "company", body, ld=jsonld())


# ================================================================= 採用
RECRUIT_FAQ = [
    ("応募はどうすればいいですか？",
     f"<p>お電話（<a href=\"tel:{TEL_RAW}\">{TEL}</a>、担当：増子）か、各職種のページの応募フォームからどうぞ。</p>"),
    ("応募フォームを送ったのに、連絡がありません。",
     "<p>1週間たっても連絡がない場合は、うまく送れていないかもしれません。お手数ですが、もう一度ご連絡ください。</p>"),
    ("パソコンは、どのくらい使えればいいですか？",
     "<p>営業職・テレフォンアポインター・管理職責任者は、エクセルやワードで入力ができれば大丈夫です。</p>"),
]


def build_recruit():
    d = 1
    r = R(d)
    people = "".join(f"""<li><img src="{r}assets/img/{f}.jpg" alt="{role}　{n}" width="320" height="320" loading="lazy"><small>{role}</small><b>{n}</b><p>{m}</p></li>""" for f, role, n, m in STAFF[:12:2])
    body = f"""{crumb(d, [("採用情報", None)])}
<section class="phero phero--recruit" id="top">
  <div class="wrap">
    <p class="en">RECRUIT</p>
    <h1>天井に上がる人も、電話をかける人も、募集しています。</h1>
    <p class="lead">自分から動ける人、新しいことに挑戦したい人を探しています。</p>
    <div class="cta-pair"><a class="btn btn--main" href="#jobs">募集中の仕事を見る</a><a class="btn btn--line" href="#people">一緒に働く人を見る</a></div>
    <nav class="chips" aria-label="このページの目次"><ul>
      <li><a href="#philosophy">理念</a></li><li><a href="#numbers">数字で見る</a></li><li><a href="#work">仕事を知る</a></li>
      <li><a href="#people">人を知る</a></li><li><a href="#jobs">募集職種</a></li><li><a href="#faq">応募について</a></li>
    </ul></nav>
  </div>
</section>
<section class="sec" id="philosophy">
  <div class="wrap narrow">
    {sec_head("PHILOSOPHY", "理念", "サービス＆貢献")}
    <p class="big-text">お客様はもちろん、当社の社員含め、パーソンライトに関わる全ての皆様と共に輝かしい未来へ。創造と挑戦の歩みを止めず、日々成長してまいります。</p>
    <p class="sign">代表取締役社長　増子 佑</p>
  </div>
</section>
<section class="sec sec--tint" id="numbers">
  <div class="wrap">
    {sec_head("NUMBERS", "数字で見る", "パーソンライトを数字で見る")}
    <div class="nums nums--4">
      <div><small>株式会社の設立</small><b>2022<span>年</span></b><p>創業は2020年5月</p></div>
      <div><small>従業員</small><b>15<span>名</span></b><p>会社概要の数</p></div>
      <div><small>年間休日（正社員）</small><b>120<span>日</span></b><p>土日祝休み</p></div>
      <div><small>募集している職種</small><b>{len(JOBS)}<span>職種</span></b><p>正社員とパート</p></div>
    </div>
    <p class="more-line"><a class="more" href="{r}company/#history">これまでの歩みを見る</a></p>
    {tbd("平均年齢・男女の割合・未経験から入った人の数など、手本が「数字で見る」に置いている物で出せる数")}
  </div>
</section>
<section class="sec" id="work">
  <div class="wrap">
    {sec_head("OUR WORK", "仕事を知る", "4つの部署で、仕事を分けています。")}
    <ul class="grid4">
      <li><b>環境部</b><p>空調設備やLED照明など、省エネにつながる商品を提案して販売します。</p></li>
      <li><b>通信機器部</b><p>—</p></li>
      <li><b>工事部</b><p>お店や会社、ご家庭のエアコンを取り付けます。電気工事・水回り工事も自社で行います。</p></li>
      <li><b>総務</b><p>—</p></li>
    </ul>
    {tbd("通信機器部と総務の仕事の中身、テレフォンアポインターがどの部署か（旧サイトは部署名だけ）")}
  </div>
</section>
<section class="sec sec--tint" id="people">
  <div class="wrap">
    {sec_head("PEOPLE", "人を知る", "一緒に働いている人の、ひとことです。")}
    <ul class="staff">{people}</ul>
    <p class="more-line"><a class="more" href="{r}company/#members">スタッフ全員を見る</a></p>
    {tbd("社員インタビュー（入った理由・一日の流れ）。手本はここを一番厚くしている")}
  </div>
</section>
<section class="sec" id="jobs">
  <div class="wrap">
    {sec_head("POSITIONS", "募集職種", f"いま、{len(JOBS)}つの職種で募集しています。")}
    {job_cards(d)}
  </div>
</section>
<section class="sec sec--tint" id="faq">
  <div class="wrap narrow">
    {sec_head("FAQ", "応募について", "応募の前に、よくいただく質問です。")}
    {acc(RECRUIT_FAQ)}
  </div>
</section>
<section class="sec entry" id="entry">
  <div class="wrap narrow center">
    <p class="en">ENTRY</p>
    <h2 class="h2">まずは、話を聞きに来てください。</h2>
    <p>お電話（担当：増子）か、各職種の応募フォームからどうぞ。</p>
    <div class="cta-pair cta-pair--center"><a class="btn btn--main" href="#jobs">募集中の仕事を見る</a><a class="btn btn--line" href="tel:{TEL_RAW}">電話で応募する　{TEL}</a></div>
  </div>
</section>
"""
    return page("採用情報｜株式会社パーソンライト",
                "福島県郡山市の株式会社パーソンライトの採用情報。エアコン設備工事スタッフ・営業職・テレフォンアポインター・管理職責任者を募集しています。",
                d, "recruit", body, band=False, ld=jsonld([faq_ld(RECRUIT_FAQ)]))


def build_job(j):
    d = 2
    r = R(d)
    rows = [("職種", j["name"]), ("雇用形態", j["type"]), ("仕事内容", j["work"]), ("応募資格", j["req"]),
            ("勤務時間", j["hours"]), ("給与", j["pay"]), ("待遇", j["welfare"]), ("休日・休暇", j["holiday"]),
            ("勤務地", f"本社（{ADDR}）"), ("その他", j["other"])]
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    body = f"""{crumb(d, [("採用情報", "recruit/"), (j["name"], None)])}
<section class="phero" id="top">
  <div class="wrap">
    <p class="en">POSITION</p>
    <h1>{j['name']}</h1>
    <p class="lead">{j['summary']}</p>
    <ul class="badges"><li><b>{j['type']}</b></li><li><b>{j['pay']}</b></li></ul>
    <div class="cta-pair"><a class="btn btn--main" href="#apply">応募する</a><a class="btn btn--line" href="tel:{TEL_RAW}">電話で応募する　{TEL}</a></div>
  </div>
</section>
<section class="sec" id="detail">
  <div class="wrap narrow">
    {sec_head("REQUIREMENTS", "募集要項", "募集要項")}
    <dl class="dl dl--job">{dl}</dl>
    {tbd("勤務地は本社として仮に置いた（旧サイトに記載なし）。郡山営業所の勤務もあるか")}
  </div>
</section>
<section class="sec sec--tint" id="apply">
  <div class="wrap narrow">
    {sec_head("ENTRY", "応募", "応募は、お電話かフォームでどうぞ。")}
    <div class="apply">
      <a class="cband__way" href="tel:{TEL_RAW}"><small>お電話で（担当：増子）</small><b>{TEL}</b></a>
    </div>
    <form class="form" action="{r}contact/thanks/" method="post" data-demo>
      <input type="hidden" name="job" value="{j['name']}">
      <label class="field"><span>お名前<em>必須</em></span><input type="text" name="name" autocomplete="name" required></label>
      <label class="field"><span>電話番号（携帯可）<em>必須</em></span><input type="tel" name="tel" autocomplete="tel" required></label>
      <label class="field"><span>メールアドレス<em>必須</em></span><input type="email" name="email" autocomplete="email" required></label>
      <label class="field"><span>生年月日<em>必須</em></span><input type="date" name="birth" required></label>
      <label class="field"><span>現在の就業状況<em>必須</em></span><select name="status" required><option value="">選んでください</option><option>就業中</option><option>離職中</option><option>学生</option><option>その他</option></select></label>
      <label class="field"><span>連絡についての補足<em class="opt">任意</em></span><textarea name="note" rows="3" placeholder="例）平日の18時以降なら電話に出られます"></textarea></label>
      <label class="agree"><input type="checkbox" required> <a href="{r}privacy/" target="_blank">プライバシーポリシー</a>を読んで、同意します</label>
      <button class="btn btn--main btn--wide" type="submit">この内容で応募する</button>
      <p class="form__demo">これはデモサイトです。押しても送信されません。ご応募は <a href="tel:{TEL_RAW}">{TEL}</a>（担当：増子）へ。</p>
    </form>
    <p class="note">1週間たっても連絡がない場合は、うまく送れていないかもしれません。お手数ですが、もう一度ご連絡ください。</p>
  </div>
</section>
<section class="sec" id="others">
  <div class="wrap">
    {sec_head("OTHER POSITIONS", "ほかの募集", "ほかの職種も見てみる")}
    {job_cards(d, exclude=j["id"])}
    <p class="more-line"><a class="more" href="{r}recruit/">採用情報のトップへ</a></p>
  </div>
</section>
"""
    return page(f"{j['name']}の募集要項｜採用情報｜株式会社パーソンライト", f"{j['name']}（{j['type']}・{j['pay']}）。{j['summary']}",
                d, "recruit", body, band=False)


# ================================================================= よくある質問
def faq_themes():
    lease = [AC_FAQ[0], AC_FAQ[1], AC_FAQ[3], AC_FAQ[4]]
    return [
        ("consult", "ご相談・お見積り", "相談できること、見積りの受け方", [
            ("見積りに、お金はかかりますか？",
             "<p>お見積りは無料です。スタッフがうかがって取り付ける場所を実際に見てから、機種と工事のやり方を決めます。</p>"),
            ("エアコンのほかに、どんなことを相談できますか？",
             "<p>家庭用エアコン、空気清浄機、LED照明、分解・洗浄クリーニング、エコキュート、高機能換気設備、業務用冷蔵庫・冷凍庫、各種厨房機器。ビジネスフォン、複合機、防犯カメラ、UTM、サーバー。電気工事や水回りの工事も、自社の工事部でお受けします。</p>"),
            ("どうやって申し込めばいいですか？",
             f"<p>お電話（<a href=\"tel:{TEL_RAW}\">{TEL}</a>）か、<a href=\"../contact/\">お問い合わせフォーム</a>からどうぞ。フォームは24時間受け付けています。</p>"),
            ("フォームを送ったのに、返事が届きません。",
             "<p>docomo・au・softbank など携帯会社のメールアドレスだと、こちらからの返信が届かないことがあります。困ったときはお電話ください。</p>"),
        ]),
        ("lease", "リース・お支払い", "リースの仕組み、途中解約、期間が終わったあと", [
            ("リースにすると、何が良いのですか？",
             "<p>初期費用がかからず、銀行から借りられる枠を減らしません。税務上認められたリース期間なら、支払いを全額経費にできます。動産総合保険もついています。</p><p><a href=\"../ac/#pay\">リースの良いところと、ご契約前に確かめてほしいこと</a></p>"),
        ] + lease),
        ("support", "保証・修理", "故障したとき、付けたあとのこと", [
            ("取り付けたあとの保証はありますか？",
             "<p>引き渡しのあとは、7年保証と年間メンテナンスが始まります。</p>"),
            AC_FAQ[2],
            ("古いエアコンが壊れたら、修理できますか？",
             "<p>2001年より前の機種に使われているR22（指定フロン）は、もう生産も輸入もされていません。修理用のガスが手に入らなくなる前に、入れ替えを考えてみてください。</p>"),
        ]),
        ("recruit", "採用", "応募の方法", RECRUIT_FAQ[:2]),
    ]


def build_faq():
    d = 1
    r = R(d)
    themes = faq_themes()
    all_pairs = [p for _, _, _, ps in themes for p in ps]
    directory = "".join(f"""<li><a href="#{k}"><i>{i+1:02d}</i><b>{t}</b><span>{s}</span><em>{len(ps)}件</em></a></li>""" for i, (k, t, s, ps) in enumerate(themes))
    groups = "".join(f"""<section class="faqg" id="{k}"><h2 class="h3"><i>{i+1:02d}</i>{t}</h2>{acc(ps)}</section>""" for i, (k, t, s, ps) in enumerate(themes))
    body = f"""{page_hero(d, "FAQ", "よくある質問", f"ご相談・リース・保証・採用について、よくいただく質問に答えています（{len(all_pairs)}件）。", [("よくある質問", None)])}
<section class="sec" id="themes">
  <div class="wrap">
    {sec_head("FIND BY THEME", "テーマから探す", "知りたいことに近いテーマを選んでください。")}
    <ul class="faqdir">{directory}</ul>
  </div>
</section>
<section class="sec sec--tint" id="all">
  <div class="wrap narrow">
    {sec_head("ALL QUESTIONS", "すべての質問", "すべての質問と回答")}
    {groups}
  </div>
</section>
"""
    return page("よくある質問｜株式会社パーソンライト",
                "株式会社パーソンライトへのよくある質問。見積りの費用、相談できること、リースの途中解約と期間終了後、保証と修理、採用の応募について。",
                d, "faq", body, band_title="解決しない場合は、お気軽にご相談ください。", ld=jsonld([faq_ld(all_pairs)]))


# ================================================================= お問い合わせ
def build_contact():
    d = 1
    r = R(d)
    body = f"""{crumb(d, [("お見積り・ご相談", None)])}
<section class="sec sec--form" id="top">
  <div class="wrap">
    <div class="ctop">
      <p class="en">CONTACT</p>
      <h1 class="h1">お見積り・ご相談</h1>
      <p class="lead">お見積りは無料です。お電話でもフォームでも、どちらでも構いません。</p>
      <ul class="badges"><li><b>5メーカー・12種類</b>から選べる</li><li><b>自社の工事部</b>が取り付け</li><li><b>7年保証</b></li></ul>
    </div>
    {inquiry_form(d, heading=False)}
    <p class="more-line center">先に聞きたいことがあれば <a href="{r}faq/">よくある質問</a> へ。</p>
  </div>
</section>
"""
    return page("お見積り・ご相談｜株式会社パーソンライト",
                "業務用エアコン・リース・クリーニング・防犯カメラ・複合機・ビジネスフォンのお見積りとご相談。お見積りは無料です。株式会社パーソンライト（福島県郡山市）。",
                d, "contact", body, band=False)


def build_thanks():
    d = 2
    r = R(d)
    body = f"""{crumb(d, [("お見積り・ご相談", "contact/"), ("送信完了", None)])}
<section class="sec">
  <div class="wrap narrow center">
    <p class="en">THANK YOU</p>
    <h1 class="h1">送信ありがとうございました</h1>
    <p>内容を確かめて、担当者から折り返しご連絡します。</p>
    <p class="note">これはデモサイトです。実際には何も送信されていません。</p>
    <p>3日たっても連絡がないときは、お手数ですが <a href="tel:{TEL_RAW}">{TEL}</a> までお電話ください。</p>
    <h2 class="h3">お待ちのあいだに</h2>
    <ul class="grid3 grid4--link">
      <li><a href="{r}works/"><b>施工実績</b><p>現場の写真を見る</p></a></li>
      <li><a href="{r}reviews/"><b>お客様の声</b><p>工事のあとの声を読む</p></a></li>
      <li><a href="{r}faq/"><b>よくある質問</b><p>リースや保証のこと</p></a></li>
    </ul>
    <p class="more-line center"><a class="btn btn--line" href="{r}">トップへ戻る</a></p>
  </div>
</section>
"""
    return page("送信ありがとうございました｜株式会社パーソンライト", "お問い合わせを受け付けました。", d, "contact", body, band=False)


def build_privacy():
    import p_misc
    d = 1
    items = "".join(f"<section class=\"pp\"><h2 class=\"h3\">{n}　{t}</h2><p>{x}</p></section>" for n, t, x in p_misc.PRIVACY)
    body = f"""{page_hero(d, "PRIVACY POLICY", "プライバシーポリシー", "パーソンライト（以下、当社）は、みなさまからお預かりする個人情報を、細心の注意を払って扱います。", [("プライバシーポリシー", None)])}
<section class="sec">
  <div class="wrap narrow">
    {items}
    <section class="pp"><h2 class="h3">お問い合わせ窓口</h2><p>この方針についてご質問があれば、下の連絡先までお問い合わせください。</p>
    <p>パーソンライト<br>{ZIP}　{ADDR}<br>TEL <a href="tel:{TEL_RAW}">{TEL}</a> ／ FAX {FAX}</p></section>
  </div>
</section>
"""
    return page("プライバシーポリシー｜株式会社パーソンライト", "株式会社パーソンライトのプライバシーポリシー。", d, "privacy", body, band=False)


# ================================================================= 書き出しと点検
def put(rel, text, made):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    made.append((rel, text))


def check(made):
    """内部リンク（ページとアンカー）と画像の実在、h1 の数を数える"""
    ids = {}
    for rel, t in made:
        ids[rel.replace("\\", "/")] = set(re.findall(r'\sid="([^"]+)"', t))
    bad = []
    for rel, t in made:
        base = os.path.dirname(rel)
        h1 = len(re.findall(r"<h1[\s>]", t))
        if h1 != 1:
            bad.append(f"{rel}: h1 が {h1} 個")
        for attr, url in re.findall(r'(href|src)="([^"]+)"', t):
            if url.startswith(("http", "tel:", "mailto:")):
                continue
            path, _, frag = url.partition("#")
            path = path.split("?")[0]
            if not path:
                target = rel.replace("\\", "/")
            else:
                target = os.path.normpath(os.path.join(base, path)).replace("\\", "/")
                if path.endswith("/") or target == "." or os.path.isdir(os.path.join(ROOT, target)):
                    target = (target + "/index.html").replace("./", "") if target != "." else "index.html"
                if not os.path.exists(os.path.join(ROOT, target)):
                    bad.append(f"{rel}: 無い {url}")
                    continue
            if frag and target in ids and frag not in ids[target]:
                bad.append(f"{rel}: アンカーが無い {url}")
    return bad


def main():
    made = []
    put("index.html", build_top(), made)
    put("ac/index.html", build_ac(), made)
    put("office-tech/index.html", build_office(), made)
    put("works/index.html", build_works(), made)
    put("reviews/index.html", build_reviews(), made)
    for i, v in enumerate(VOICES):
        put(f"reviews/{v['id']}/index.html", build_review(i, v), made)
    put("company/index.html", build_company(), made)
    put("recruit/index.html", build_recruit(), made)
    for j in JOBS:
        put(f"recruit/{j['id']}/index.html", build_job(j), made)
    put("faq/index.html", build_faq(), made)
    put("contact/index.html", build_contact(), made)
    put("contact/thanks/index.html", build_thanks(), made)
    put("privacy/index.html", build_privacy(), made)
    bad = check(made)
    tbds = sum(t.count('class="tbd"') for _, t in made)
    print(f"{len(made)} ページ / 要確認 {tbds} か所 / 点検の赤 {len(bad)}")
    for b in bad:
        print("  ✗", b)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
