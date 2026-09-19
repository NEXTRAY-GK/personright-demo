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

ENV = ["業務用エアコン", "家庭用エアコン", "ビル用マルチエアコン", "空気清浄機", "LED照明", "分解・洗浄クリーニング", "エコキュート",
       "高機能換気設備", "全熱交換器", "除湿器", "暖房機", "業務用冷蔵庫・冷凍庫", "各種厨房機器"]
TEL_BIZ = ["ビジネスフォン", "複合機", "セキュリティ商材", "PC周辺設備", "防犯カメラ", "UTM", "サーバー"]
KOJI = ["各種工事", "電気工事", "水回り工事"]


def fmt(d):
    return f"{d[:4]}.{d[4:6]}.{d[6:]}"


# 声ごとに「何を頼んだか」。本文に書いてあることだけから付けた
WHAT = {"98": "会社のエアコン設置", "96": "オフィスのエアコン設置", "53": "工場の空調更新・リース", "56": "エアコンの工事"}


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
            <p class="card__who">{v['who']}<span class="tag">{WHAT[v['id']]}</span></p>
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
    {sec_head("SIMULATION", "電気代の比べ方", "替えると、電気代はいくら下がるか。", "いまのエアコンの時期と、毎月の電気代を動かしてみてください。結果はその場で変わります。")}
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
        <p class="sim__note">冷媒ごとの消費電力の比（R22を100%としたとき、R407・R410は60%、R32は20%）から出した目安です。電気の単価や使い方の違い、本体・工事・リースの費用は入っていません。</p>
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
      <p class="en">福島県郡山市　会社・お店・工場の設備</p>
      <h1><span class="nw">業務用エアコンも、</span><span class="nw">防犯カメラも複合機も。</span><span class="nw">付けるのは自社の工事部です。</span></h1>
      <p class="lead">会社・お店・工場の業務用エアコンの入れ替えとリース、防犯カメラ・複合機・ビジネスフォン、電気と水回りの工事をお受けしています。エアコンは、付けたあと7年間保証します。</p>
      <ul class="proof">
        <li><b>初期費用0円</b><span>エアコンをリースで入れる場合</span></li>
        <li><b>自社の工事部</b><span>電気・水回りの工事も</span></li>
        <li><b>7年保証</b><span>エアコンの年間メンテナンスも</span></li>
      </ul>
      {cta_pair(d)}
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







<section class="sec" id="why">
  <div class="wrap narrow">
    {sec_head("", "パーソンライトの考え", "工事を終えたあとからが、<br>本当のお付き合いの始まりです。")}
    <p class="big-text">2020年に須賀川市で、業務用エアコンの取り付けと保守の会社として始まりました。取り付けは自社の工事部が行い、付けたあとは7年保証と年間メンテナンスがつきます。</p>
    <p class="note">企業理念は「サービス＆貢献」。「パーソンライトに相談して良かった！」と心の底からお喜び頂けることを目指しています。 <a class="more" href="{r}company/#philosophy">会社案内で読む</a></p>
  </div>
</section>

<section class="sec sec--tint" id="service">
  <div class="wrap">
    {sec_head("", "事業紹介", "ご用件に合わせて、<br>それぞれのページで詳しくご案内しています。", "空調と通信の機器を売るところから、取り付けの工事まで。4つの事業があります。")}
    <div class="svc">
      <div class="svc__group">
        <p class="svc__label"><b>01</b>環境事業</p>
        <a class="svc__main" href="{r}ac/">
          <img src="{r}assets/img/case-shop.jpg" alt="店舗の天井に設置した業務用エアコン" width="780" height="611" loading="lazy">
          <div>
            <small>5メーカー・12種類から選べます</small>
            <b>業務用エアコン</b>
            <p>機種選びから取り付け、リース、7年保証と年間メンテナンスまで。</p>
            <p class="svc__hook">電気代が月3万円なら、2001年より前の機種（R22）からいまの機種（R32）に替えると、<b>年に約29万円</b>下がる計算です。</p>
            <span class="more">詳しく見る・自分の電気代で計算する</span>
          </div>
        </a>
        <p class="svc__also">ほかに扱っている物</p>
        <ul class="taglist">{"".join(f"<li>{x}</li>" for x in ENV[1:])}</ul>
        {tbd("「年に約29万円」は、旧サイトの冷媒ごとの消費電力の比（R22を100としたとき、R32は20）から出した計算。比の出どころ（メーカー資料か、自社の実測か）")}
      </div>
      <div class="svc__group">
        <p class="svc__label"><b>02</b>通信事業</p>
        <a class="svc__main" href="{r}office-tech/">
          <img src="{r}assets/img/cam-hero.jpg" alt="防犯カメラ" width="1600" height="587" loading="lazy">
          <div>
            <small>いまの印刷代と比べられます</small>
            <b>通信機器</b>
            <p>夜でも色まで写る防犯カメラ、富士フイルムの複合機、ビジネスフォン。</p>
            <p class="svc__hook">複合機は、いまの請求書の単価を入れると、印刷代の差額をその場で比べられます。</p>
            <span class="more">詳しく見る・印刷代を比べる</span>
          </div>
        </a>
        <ul class="taglist">{"".join(f"<li>{x}</li>" for x in TEL_BIZ)}</ul>
      </div>
      <div class="svc__group">
        <p class="svc__label"><b>03</b>工事部</p>
        <div class="svc__sub">
          <b>各種工事・電気工事・水回り工事</b>
          <p>エアコンを付けるときの電気の工事も、水回りの工事も、自社の工事部でお受けします。</p>
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

<section class="sec" id="how">
  <div class="wrap">
    {sec_head("", "頼んだあと", "現地を見てから決めて、<br>自社の工事部が取り付けます。")}
    <ol class="how">
      <li>
        <p class="how__no">1</p>
        <div class="how__t"><b>現地を見てから、機種を決めます</b><p>スタッフがうかがって、取り付ける場所を見てから、機種と工事のやり方をご提案します。お見積りは無料です。</p></div>
        <blockquote class="how__q"><p>こちらの要望をしっかりヒアリングしていただき、最適な機種や設置方法を提案してもらえました。</p><cite><a href="{r}reviews/98/">田村市　N様</a></cite></blockquote>
      </li>
      <li>
        <p class="how__no">2</p>
        <div class="how__t"><b>取り付けは、自社の工事部が行います</b><p>エアコンの取り付けのほか、電気工事や水回りの工事も、同じ工事部でお受けします。</p></div>
        <blockquote class="how__q"><p>変電設備を増やす工事に伴っては、工場内を計画的に停電させる必要がありましたが、こちらもスケジュール通り安全に進めていただき、業務もストップすることなく完了しました。</p><cite><a href="{r}reviews/53/">須賀川市内　某社 様</a></cite></blockquote>
      </li>
      <li>
        <p class="how__no">3</p>
        <div class="how__t"><b>付けたあとは、7年間保証します</b><p>引き渡しのあとは、7年保証と年間メンテナンスが始まります。「安心保証リース」でご契約いただくと、リース期間中の突然の故障も修理費がかかりません。</p></div>
        <blockquote class="how__q how__q--us"><p>設備機器の工事を終えた後からが、本当のお付き合いの始まりであると考えております。</p><cite>パーソンライト</cite></blockquote>
      </li>
    </ol>
    {cta_pair(d, "業務用エアコン")}
  </div>
</section>

<section class="sec sec--tint" id="voice">
  <div class="wrap">
    {sec_head("", "お客様の声", "工事のあとに、いただいた声です。")}
    {voice_cards(d, ids=["96", "56", "98"])}
    <p class="more-line"><a class="more" href="{r}reviews/">お客様の声をすべて読む（{len(VOICES)}件）</a></p>
    {tbd("施工件数・年間の施工本数・お取引先の名前（載せてよい物）。数字があれば、この節の頭に置く。いちばん効く場所")}
  </div>
</section>

<section class="photostrip" aria-label="現場の写真"><ul>{strip}</ul></section>

<section class="sec" id="about">
  <div class="wrap">
    {sec_head("", "パーソンライトについて", "どんな会社から、どんな人がうかがうのか。")}
    <ul class="cards cards--2">
      <li class="card card--big"><a href="{r}company/">
        <img src="{r}assets/img/office-front.jpg" alt="本社の外観" width="810" height="555" loading="lazy">
        <div class="card__b"><p class="card__t">会社案内</p><p>2020年に須賀川市で、業務用エアコンの取り付けと保守の会社として始まりました。いまは郡山市に本社があります。スタッフの顔と、ひとことも載せています。</p><span class="more">会社案内を見る</span></div>
      </a></li>
      <li class="card card--big"><a href="{r}recruit/">
        <img src="{r}assets/img/recruit03.jpg" alt="天井のエアコンを点検する工事スタッフ" width="720" height="516" loading="lazy">
        <div class="card__b"><p class="card__t">採用情報</p><p>工事スタッフ・営業職・テレフォンアポインター・管理職責任者の4職種を募集しています。</p><span class="more">採用情報を見る</span></div>
      </a></li>
    </ul>
  </div>
</section>

<section class="sec sec--tint" id="media">
  <div class="wrap">
    {sec_head("", "現場の記録", "工事の現場を、写真で見ていただけます。")}
    <ul class="cards cards--2">
      <li class="card card--row"><a href="{r}works/">
        <img src="{r}assets/img/works-20251204.jpg" alt="入れ替えた天井吊形エアコン" width="640" height="800" loading="lazy">
        <div class="card__b"><p class="card__t">施工実績</p><p>入れ替え工事と高圧分解洗浄の現場です。分解して洗ったときの、にごった水の写真もあります。</p><span class="more">施工実績を見る</span></div>
      </a></li>
      <li class="card card--row"><a href="{INSTA}" target="_blank" rel="noopener">
        <img src="{r}assets/img/works-20251211.jpg" alt="分解して洗った天井カセット形エアコン" width="640" height="800" loading="lazy">
        <div class="card__b"><p class="card__t">Instagram</p><p>新しい現場は @personright501 に載せています。</p><span class="more">Instagram を開く</span></div>
      </a></li>
    </ul>
  </div>
</section>
"""
    return page("株式会社パーソンライト｜業務用エアコンの入れ替え・リース（福島県郡山市）",
                "古い業務用エアコンを今の機種に替えると、消費電力は15年前の機種より65%下がります。リースなら初期費用0円、取り付けは自社の工事部、付けたあとは7年保証。福島県郡山市の株式会社パーソンライト。",
                d, "top", body, band_topic="業務用エアコン", ld=jsonld())


# ================================================================= 事業のページ（LP の型）
# 2026-09-18、代表の指示「エアコンと通信機器の強みを最大限引き出す。優秀なLPのノウハウでコンバージョンを」。
# 型は `NEXTRAY関連/調査_HPの成約構成_2026-09/` の結論に合わせた。訪問者の問いの順に節を置く。
#   ① 自分に関係あるか … 何屋×誰向け×地域の一言、実物の写真、主の一歩と電話、事実だけの安心の1行
#   ② すぐ知りたい3つ … 料金・誰がやるか・実例を最初の2画面に
#   困りごとの入口 … 人は解決策ではなく困りごとで探す（NN/g 2014）
#   ③ 強みごとに、確かめられる証拠（声の原文・写真・数字）を添える
#   ④ 料金と条件は、強い言葉と同じ塊に置く（消費者庁 打消し表示の留意点 2018）
#   ⑤ はじめ方は、誰が何をするかを書く。フォームは必須3つ
# ⚠️ No.1 の表示は使わない。旧サイトの「J.D.パワー 9年連続1位」は、2023年の調査で2部門ともキヤノンが1位で、いまは言えない（2026-09-18 に原典で確かめた）。

def lp_hero(depth, crumbs, label, h1, lead, proof, safe, img, alt, w, h, topic=None):
    items = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in proof)
    return f"""{crumb(depth, crumbs)}
<section class="lph" id="top">
  <div class="wrap lph__in">
    <div class="lph__t">
      <p class="en">{label}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <ul class="proof">{items}</ul>
      <div class="cta-pair"><a class="btn btn--main" href="#form">無料で見積りを頼む</a><a class="btn btn--line" href="tel:{TEL_RAW}">電話で相談する　{TEL}</a></div>
      <p class="safe">{safe}</p>
    </div>
    <figure class="lph__fig"><img src="{R(depth)}assets/img/{img}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high"></figure>
  </div>
</section>
"""


def answers(items):
    """すぐ知りたい3つ … (問い, 答え, 補足, 飛び先)"""
    return '<section class="ans" aria-label="すぐ知りたいこと"><div class="wrap"><ul>' + "".join(
        f'<li><a href="#{a}"><small>{q}</small><b>{b}</b><span>{c}</span></a></li>' for q, b, c, a in items) + "</ul></div></section>"


def needs(title, items):
    """困りごとの入口 … (お客様の言葉, 答えの一言, 飛び先)"""
    return f"""<section class="sec sec--tight" id="needs">
  <div class="wrap">
    {sec_head("", "こんなとき", title)}
    <ul class="needs">{"".join(f'<li><a href="#{a}"><b>{t}</b><span>{x}</span></a></li>' for t, x, a in items)}</ul>
  </div>
</section>"""


def staff_row(depth, ids, title):
    r = R(depth)
    pick = [s for s in STAFF if s[0] in ids]
    return f"""<div class="crew">
      <p class="crew__t">{title}</p>
      <ul>{"".join(f'<li><img src="{r}assets/img/{f}.jpg" alt="{role}　{n}" width="320" height="320" loading="lazy"><div><small>{role}　{n}</small><p>「{m}」</p></div></li>' for f, role, n, m in pick)}</ul>
    </div>"""


VOICE_NOTE = "いただいた声を、手を加えずに載せています。"


# ================================================================= 業務用エアコン
def build_ac():
    d = 1
    r = R(d)
    hero = lp_hero(d, [("業務用エアコン", None)],
                   "福島県郡山市　会社・お店・工場の業務用エアコン",
                   '<span class="nw">業務用エアコンの入れ替えを、</span><span class="nw">初期費用0円のリースで。</span>',
                   "15年前の機種から替えると、消費電力は65%下がります。機種はダイキン・三菱電機・日立・東芝・パナソニックの12種類から。取り付けは自社の工事部が行い、付けたあとは7年保証と年間メンテナンスがつきます。",
                   [("初期費用0円", "リースの場合"), ("7年保証", "年間メンテナンスも"), ("自社の工事部", "電気工事もまとめて")],
                   "お見積りは無料です。スタッフがうかがって、取り付ける場所を見てから機種を決めます。",
                   "case-shop.jpg", "店舗の天井に取り付けた天井カセット形の業務用エアコン", 780, 611)
    ans = answers([
        ("いくらかかる？", "リースなら初期費用0円", "月々のリース料で入れられます。現金・分割払いも", "pay"),
        ("誰が付ける？", "自社の工事部", "電気の工事や水回りの工事も同じ部署で", "work"),
        ("実際は？", "工場を止めずに更新", "須賀川市内の工場で、停電の段取りまで", "voice"),
    ])
    nd = needs("気になっていることから、読んでください。", [
        ("電気代が、年々高くなってきた", "替えるといくら下がるか、計算できます", "sim"),
        ("古いエアコンで、壊れたら直せるか不安", "R22の機種は、修理のガスが手に入りにくくなっています", "r22"),
        ("まとまったお金を出したくない", "リースなら初期費用はかかりません", "pay"),
        ("お店や工場を止めずに替えたい", "工場を止めずに更新したお客様の声があります", "voice"),
        ("厨房が暑い・部屋の形が変わっている", "12種類から、部屋に合う形を選べます", "types"),
        ("効きが悪い・においが気になる", "入れ替えの前に、分解・洗浄で済むこともあります", "after"),
    ])
    gen = "".join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td><td><span class="bar" style="--w:{p}%"></span>{p}%</td></tr>' for a, b, c, p in GEN)
    types = "".join(f"""<li class="type"><img src="{r}assets/img/ac-type{no}.jpg" alt="{name}（{kind}）" width="720" height="511" loading="lazy"><b>{name}</b><span>{kind}</span></li>""" for no, name, kind in TYPES)
    cases = "".join(f'<li><a href="{r}contact/{q("業務用エアコン")}"><img src="{r}assets/img/ac-case{i+1:02d}.jpg" alt="{c}の業務用エアコン" width="352" height="352" loading="lazy"><span>{c}</span></a></li>' for i, c in enumerate(CASES))
    merits = "".join(f"<li><b>{t}</b><p>{x}</p></li>" for t, x in MERITS[:6])
    cautions = "".join(f"<li><b>{t}</b><p>{x}</p></li>" for t, x in CAUTIONS)
    swaps = [w for w in WORKS if w["kind"] == "swap"][:3]
    v53 = next(v for v in VOICES if v["id"] == "53")
    faq_groups = [
        ("リースのこと", [AC_FAQ[0], AC_FAQ[1], AC_FAQ[3]]),
        ("修理と保証のこと", [AC_FAQ[2]]),
        ("お支払いのこと", [AC_FAQ[4]]),
    ]
    faq_html = "".join(f'<h3 class="qa-h">{g}</h3>{acc(ps)}' for g, ps in faq_groups)

    body = f"""{hero}
{ans}
{nd}


<section class="sec" id="voice">
  <div class="wrap">
    {sec_head("", "お客様の声", "頼んだ会社の方が、工事のあとに書いてくださった声です。", VOICE_NOTE)}
    {voice_cards(d, ids=["98", "96", "56"])}
    <p class="more-line"><a class="more" href="{r}reviews/">お客様の声をすべて読む（{len(VOICES)}件）</a></p>
  </div>
</section>

<section class="sec sec--tint" id="reason">
  <div class="wrap">
    {sec_head("", "強み 1　電気代", "替えるだけで、エアコンの電気は大きく減ります。", "2011年3月の東日本大震災のあと、電気代は上がり続けてきました。そのあいだに、業務用エアコンの省エネは大きく進んでいます。")}
    <div class="nums">
      <div><small>最新の省エネ機種に替えると</small><b>最大70<span>%</span></b><p>消費電力が減ります</p></div>
      <div><small>15年前の機種と比べると</small><b>65<span>%</span></b><p>消費電力が減ります</p></div>
      <div><small>18年前の機種と比べると</small><b>80<span>%</span></b><p>消費電力が減ります</p></div>
    </div>
    <table class="tbl"><caption>冷媒ごとの消費電力（R22を100%としたとき）</caption><thead><tr><th>冷媒</th><th>種類</th><th>使われた時期</th><th>消費電力</th></tr></thead><tbody>{gen}</tbody></table>
  </div>
</section>

{sim_ac(d)}

{mid_cta(d, "いまお使いの一台を、見せてください。", "入れ替えか、クリーニングで済むか。現地を見てからお答えします。お見積りは無料です。", "業務用エアコン")}

<section class="sec" id="types">
  <div class="wrap">
    {sec_head("", "強み 2　選べる", "5社のメーカー・12種類から、部屋に合う形を選びます。", "天井に埋め込む形、吊るす形、壁掛け、床置き、ダクトで送る形、熱と油に強い厨房用まであります。置く場所や広さ、天井のつくりを見てお選びします。")}
    <p class="makers"><b>取り扱いメーカー</b>ダイキン／三菱電機／日立／東芝／パナソニック</p>
    <ul class="types">{types}</ul>
    <h3 class="h3">お店や会社の種類から、相談できます。</h3>
    <ul class="cases">{cases}</ul>
  </div>
</section>

<section class="sec sec--tint" id="work">
  <div class="wrap">
    {sec_head("", "強み 3　工事", "取り付けは、自社の工事部が行います。", "エアコンの取り付けのほか、電気の工事も水回りの工事も、同じ工事部でお受けします。電気の容量が足りない建物でも、話が一度で済みます。")}
    <ul class="thumbs">
      <li><img src="{r}assets/img/work-ceiling.jpg" alt="天井カセット形を取り付ける工事スタッフ" width="276" height="200" loading="lazy"></li>
      <li><img src="{r}assets/img/work-attic.jpg" alt="天井の中で配管を確かめる工事スタッフ" width="276" height="200" loading="lazy"></li>
      <li><img src="{r}assets/img/work-outdoor.jpg" alt="建物の外で室外機まわりを作業する工事スタッフ" width="276" height="200" loading="lazy"></li>
      <li><img src="{r}assets/img/work-filter.jpg" alt="天井のエアコンのパネルを外す工事スタッフ" width="276" height="200" loading="lazy"></li>
    </ul>
    <blockquote class="bigq"><p>{v53['body'][0]}</p><cite><a href="{r}reviews/53/">{v53['who']}</a>（工場の空調更新・リース）</cite></blockquote>
    {staff_row(d, ["staff10", "staff11", "staff16"], "うかがうのは、この工事部です")}
  </div>
</section>

<section class="sec" id="after">
  <div class="wrap">
    {sec_head("", "強み 4　付けたあと", "工事が終わってからが、<br>本当のお付き合いの始まりです。")}
    <div class="after2">
      <ul class="grid2">
        <li><b>7年保証</b><p>引き渡しのあとから、7年間の保証が始まります。</p></li>
        <li><b>年間メンテナンス</b><p>付けたあとの点検のために、年間メンテナンスをご用意しています。</p></li>
      </ul>
      <figure class="after2__fig"><img src="{r}assets/img/works-20251203.jpg" alt="分解して洗ったあと、カップにたまった茶色い水" width="640" height="800" loading="lazy"><figcaption><b>分解・洗浄クリーニング</b>部品を外して、水の勢いで奥まで洗い流します。カップの水の色が、中にたまっていた汚れです。効きが悪いときは、入れ替えの前に一度ご相談ください。 <a href="{r}works/#wash">洗浄の現場を見る</a></figcaption></figure>
    </div>
    {tbd("年間メンテナンスの中身と料金、7年保証の範囲（何が無料で、何が有料か）")}
  </div>
</section>

<section class="sec sec--tint" id="works">
  <div class="wrap">
    {sec_head("", "施工事例", "入れ替え工事の現場です。")}
    {work_cards(d, swaps)}
    <p class="more-line"><a class="more" href="{r}works/">施工実績をすべて見る</a></p>
  </div>
</section>

<section class="sec" id="pay">
  <div class="wrap">
    {sec_head("", "払い方", "リースなら、初期費用はかかりません。", "毎月のリース料で、いまの省エネ機種を入れられます。審査に出す書類は当社で用意して、リース会社へ出すところまで行います。現金での購入や、クレジットの分割払いもできます。")}
    <div class="lease3">
      <div><b>故障しても、修理費がかからない</b><p>「安心保証リース」でご契約いただくと、リース期間中の突然の故障の修理費がかかりません。</p></div>
      <div><b>火事や雪の被害も、保険で</b><p>リースで入れたエアコンには動産総合保険がつきます。火事・水害・雪害・落雷・盗難などの損害を補償します。</p></div>
      <div><b>期間が終わったら、新しい機種へ</b><p>「レベルアップ更新」で、それまでとあまり変わらないリース料のまま、最新の機種に入れ替えられます。</p></div>
    </div>
    <h3 class="h3">リースの良いところ</h3>
    <ul class="grid3">{merits}</ul>
    <h3 class="h3">ご契約の前に、ここは必ず確かめてください</h3>
    <ul class="grid3 grid3--warn">{cautions}</ul>
    {tbd("機種ごと・部屋の広さごとのリース月額の目安（例：事務所30坪・天井カセット形2台で月◯円）。典型例の料金が一つあると、見積りの前に離れる人が減る。再リースの料金が2か所で合わない（注意「年間リース額の10分の1」／よくある質問「月額リース料の2倍」）")}
  </div>
</section>

<section class="sec sec--tint" id="r22">
  <div class="wrap narrow">
    {sec_head("", "いま替える理由", "R22の機種は、壊れたら直せないことがあります。")}
    <p>2001年より前の機種に使われているR22（指定フロン）は、もう生産も輸入もされていません。修理に使うガスが手に入らないことがあります。室外機の銘板に「R22」と書いてあれば、この時期の機種です。夏の盛りに止まる前に、入れ替えを考えてみてください。</p>
    <p class="more-line"><a class="btn btn--main" href="#form">銘板を見に来てもらう（無料）</a></p>
  </div>
</section>

<section class="sec" id="flow">
  <div class="wrap">
    {sec_head("", "はじめ方", "お客様にしていただくのは、最初の連絡と、中身の確認だけです。", "リースの審査や契約の書類は、当社とリース会社でお手伝いします。現金で購入する場合は、3と4はありません。")}
    <ol class="flow">{"".join(f'<li><p class="flow__who flow__who--{"you" if w == "お客様" else "us"}">{w}</p><p class="flow__no">{i+1}</p><b>{t}</b><p>{x}</p></li>' for i, ((t, x), w) in enumerate(zip(FLOW, ["お客様", "パーソンライト", "パーソンライト", "お客様", "パーソンライト"])))}</ol>
    {tbd("ご相談から取り付けまでの日数の目安、工事にかかる時間（1台あたり）。見積りのあとお断りいただいても費用はかからない、と書けるなら、フォームの横にも置く")}
  </div>
</section>

<section class="sec sec--tint" id="faq">
  <div class="wrap narrow">
    {sec_head("", "よくある質問", "業務用エアコンの、よくいただく質問です。")}
    {faq_html}
    <p class="more-line"><a class="more" href="{r}faq/">ほかの質問を見る</a></p>
  </div>
</section>

<section class="sec" id="form">
  <div class="wrap">
    {inquiry_form(d, "業務用エアコン")}
  </div>
</section>

<section class="sec" id="options">
  <div class="wrap">
    {sec_head("", "一緒に頼めること", "エアコンと一緒に、まとめてご相談ください。")}
    <ul class="grid4 grid4--link">
      <li><a href="{r}contact/{q('クリーニング')}"><b>分解・洗浄クリーニング</b><p>効きが悪い・においが気になるとき</p></a></li>
      <li><a href="{r}contact/{q('工事')}"><b>電気工事・水回り工事</b><p>自社の工事部でお受けします</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>LED照明・換気設備</b><p>全熱交換器・除湿器も</p></a></li>
      <li><a href="{r}office-tech/"><b>防犯カメラ・複合機・電話</b><p>通信機器のページへ</p></a></li>
    </ul>
  </div>
</section>
"""
    return page("業務用エアコンの入れ替え・リース（初期費用0円）｜福島県郡山市｜株式会社パーソンライト",
                "郡山市の業務用エアコンの入れ替え・リース。初期費用0円、15年前の機種から替えると消費電力65%減。5メーカー・12種類から選び、自社の工事部が取り付け、7年保証。お見積りは無料です。",
                d, "ac", body, band=False, ld=jsonld([faq_ld(AC_FAQ)]))


# ================================================================= 通信機器
def build_office():
    d = 1
    r = R(d)
    hero = lp_hero(d, [("通信機器", None)],
                   "福島県郡山市　会社・お店の防犯カメラ・複合機・ビジネスフォン",
                   '<span class="nw">防犯カメラは、夜も色まで。</span><span class="nw">複合機は、印刷代から見直します。</span>',
                   "夜でもカラーで撮れる防犯カメラと、富士フイルムの複合機を中心に、ビジネスフォン・UTM・サーバーまで扱っています。エアコンと同じ会社なので、電気の工事が要るときも、自社の工事部でお受けします。",
                   [("夜もカラー", "防犯カメラ"), ("富士フイルム", "複合機"), ("自社の工事部", "電気工事も")],
                   "お見積りは無料です。取り付ける場所と、何のために付けたいかをうかがってからご提案します。",
                   "cam-hero.jpg", "建物の外壁に取り付けた防犯カメラ", 1600, 587)
    ans = answers([
        ("夜は写る？", "色まで残ります", "暗い中でも、服や車の色が見分けられます", "camera"),
        ("印刷代は？", "いまの単価と比べられます", "枚数と単価を入れると、差額が出ます", "sim"),
        ("誰に頼む？", "エアコンと同じ会社", "電気の工事も自社の工事部で", "flow"),
    ])
    nd = needs("気になっていることから、読んでください。", [
        ("夜の駐車場や倉庫が、映像で真っ暗", "夜もカラーで撮れるカメラがあります", "camera"),
        ("前に見積りを取って、高くて見送った", "もう一度、当社の条件と比べてみてください", "price"),
        ("印刷代が高い気がする", "いまの単価で、差額を計算できます", "sim"),
        ("電話機やネットの機器が古い", "ビジネスフォン・UTM・サーバーも扱っています", "items"),
    ])
    cams = "".join(f"""<li class="card"><img src="{r}assets/img/{f}" alt="{t}で夜に撮った映像" width="{w}" height="{h}" loading="lazy"><div class="card__b"><p class="tag{' tag--on' if i == 2 else ''}">{'当社で扱っているカメラ' if i == 2 else '比べる物'}</p><p class="card__t">{t}</p><p>{x}</p></div></li>""" for i, (f, w, h, t, x) in enumerate(CAM))
    fuji = "".join(f"<li><b>{t}</b><p>{x}</p></li>" for t, x in FUJI)
    body = f"""{hero}
{ans}
{nd}

<section class="sec sec--tint" id="camera">
  <div class="wrap">
    {sec_head("", "強み 1　防犯カメラ", "夜の映像で、比べてみてください。", "同じ場所を、夜に3種類のカメラで撮った映像です。当社で扱っているのは、3つ目の、夜でもカラーで撮れるカメラです。")}
    <ul class="cards cards--3">{cams}</ul>
    <div class="camfeat">
      <ul class="camfeat__img">
        <li><img src="{r}assets/img/cam-01.png" alt="壁に取り付ける筒形の防犯カメラ" width="252" height="138" loading="lazy"></li>
        <li><img src="{r}assets/img/cam-02.png" alt="天井に取り付けるドーム形の防犯カメラ" width="175" height="159" loading="lazy"></li>
      </ul>
      <ul class="grid3">
        <li><b>夜もカラーで撮れる</b><p>服や車の色まで残るので、いざというときの手がかりになります。</p></li>
        <li><b>動くものを見つけて知らせる</b><p>動くものを見つけると、知らせてくれます。</p></li>
        <li><b>離れた場所から操作できる</b><p>その場にいなくても、カメラを操作できます。</p></li>
      </ul>
    </div>
    <div class="price-note" id="price">
      <h3 class="h3">値段で見送った方にも、もう一度見てほしい。</h3>
      <p>以前に防犯カメラを考えたものの、値段を見て見送った方もいらっしゃると思います。一度、当社の条件と比べてみてください。お仕事の内容や取り付ける場所、何のために付けたいのかをうかがってから、台数と付け方をご提案します。</p>
    </div>
    {tbd("台数ごとの金額の目安（例：カメラ4台・録画機1台で◯円〜、リースなら月◯円）。スマホで映像を見る仕組みの名前")}
  </div>
</section>

{mid_cta(d, "付けたい場所と、困っていることを聞かせてください。", "お見積りは無料です。現地を見てから、台数と付け方をご提案します。", "防犯カメラ")}

<section class="sec" id="copier">
  <div class="wrap">
    {sec_head("", "強み 2　複合機", "複合機は、富士フイルムを扱っています。", "入れるときの費用も印刷の費用も、地域でいちばん安くすることを目指しています。")}
    <div class="copier">
      <figure><img src="{r}assets/img/printer.png" alt="富士フイルムの複合機" width="491" height="397" loading="lazy"></figure>
      <ul class="grid2">{fuji}</ul>
    </div>
  </div>
</section>

{sim_copier(d)}

<section class="sec sec--tint" id="items">
  <div class="wrap">
    {sec_head("", "そのほかの機器", "電話やネットの機器も、まとめて見直せます。")}
    <ul class="grid4 grid4--link">
      <li><a href="{r}contact/{q('ビジネスフォン')}"><b>ビジネスフォン</b><p>事務所の電話機</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>UTM・セキュリティ商材</b><p>社内のネットを外から守る機器</p></a></li>
      <li><a href="{r}contact/{q('その他')}"><b>サーバー・PC周辺設備</b><p>社内のデータの置き場など</p></a></li>
      <li><a href="{r}ac/"><b>業務用エアコン</b><p>同じ会社で、空調のことも</p></a></li>
    </ul>
    {tbd("ビジネスフォン・UTM・サーバーの扱いメーカーと中身（旧サイトは名前だけ）。中身があれば、防犯カメラ・複合機と同じ形で節を足す")}
  </div>
</section>

<section class="sec" id="flow">
  <div class="wrap">
    {sec_head("", "はじめ方", "お客様にしていただくのは、最初の連絡と、中身の確認だけです。")}
    <ol class="flow">
      <li><p class="flow__who flow__who--you">お客様</p><p class="flow__no">1</p><b>ご連絡</b><p>お電話かフォームでご連絡ください。お見積りは無料です。</p></li>
      <li><p class="flow__who flow__who--us">パーソンライト</p><p class="flow__no">2</p><b>お話をうかがう</b><p>お仕事の内容や取り付ける場所、何のために付けたいのかをうかがいます。</p></li>
      <li><p class="flow__who flow__who--you">お客様</p><p class="flow__no">3</p><b>ご提案の確認</b><p>機種と取り付け方、金額をご確認ください。</p></li>
      <li><p class="flow__who flow__who--us">パーソンライト</p><p class="flow__no">4</p><b>取り付け</b><p>ご提案した機種を取り付けます。電気の工事が要るときは、自社の工事部がお受けします。</p></li>
    </ol>
    {staff_row(d, ["staff14", "staff15", "staff19"], "ご相談を受けるのは、通信機器部です")}
  </div>
</section>

<section class="sec" id="form">
  <div class="wrap">
    {inquiry_form(d)}
  </div>
</section>
"""
    return page("防犯カメラ・複合機・ビジネスフォン（福島県郡山市）｜株式会社パーソンライト",
                "郡山市の防犯カメラ・複合機・ビジネスフォン。夜もカラーで撮れる防犯カメラ、富士フイルムの複合機（いまの印刷代と比べられます）、UTM・サーバーまで。配線や電気の工事も自社の工事部で。お見積りは無料です。",
                d, "office-tech", body, band=False, ld=jsonld())


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
{mid_cta(d, "同じような入れ替えを考えていたら、一度見に伺います。", "現地を見てからお見積りします。お見積りは無料です。", "業務用エアコン")}
<section class="sec sec--tint" id="wash">
  <div class="wrap">
    {sec_head("CLEANING", "高圧分解洗浄", f"高圧分解洗浄　{len(wash)}件", "エアコンは使っているうちに、中のフィンやファンにほこりや汚れがたまっていきます。部品を外して、水の勢いで奥まで洗い流します。")}
    {work_cards(d, wash)}
    <p class="more-line"><a class="btn btn--line" href="{r}contact/{q('クリーニング')}">クリーニングの相談をする</a></p>
  </div>
</section>
<section class="sec" id="insta">
  <div class="wrap narrow center">
    {sec_head("INSTAGRAM", "新しい現場", "このほかの現場は、Instagramに載せています。", center=True)}
    <p><a class="btn btn--line" href="{INSTA}" target="_blank" rel="noopener">Instagram を開く（@personright501）</a></p>
    {tbd("業種・地域・工事の中身が分かる事例を、写真と一緒に数件（手本は業種ごとに事例を並べている）")}
  </div>
</section>
"""
    return page("施工実績｜株式会社パーソンライト", p_works.DESC, d, "works", body, ld=jsonld())


# ================================================================= お客様の声
def build_reviews():
    d = 1
    body = f"""{page_hero(d, "VOICE", "お客様の声", f"設備の工事を終えたあとからが、本当のお付き合いの始まりだと考えています。いただいた声（{len(VOICES)}件）は、そのあとのフォローに活かしています。", [("お客様の声", None)])}
<section class="sec">
  <div class="wrap">
    {voice_cards(d)}
    {tbd("新しい声と、写真付きの声。業種と、何を頼んだか（入れ替え・リース・クリーニングなど）が分かると、読む人が自分と重ねやすい")}
  </div>
</section>
{mid_cta(d, "まずは、いまお使いのエアコンを見せてください。", "現地を見てからお見積りします。お見積りは無料です。", "業務用エアコン")}
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
    {sec_head("PROFILE", "会社概要", "会社の概要です。")}
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
<section class="sec" id="next">
  <div class="wrap">
    {sec_head("", "ここまで読んでくださった方へ", "頼みたい方も、働きたい方も、ここから。")}
    <ul class="cards cards--2">
      <li class="card card--big"><a href="{r}contact/">
        <img src="{r}assets/img/case-shop.jpg" alt="店舗の天井に設置した業務用エアコン" width="780" height="611" loading="lazy">
        <div class="card__b"><p class="card__t">お見積り・ご相談</p><p>エアコン・防犯カメラ・複合機・工事のご相談。現地を見てからお見積りします。お見積りは無料です。</p><span class="more">無料で見積りを頼む</span></div>
      </a></li>
      <li class="card card--big"><a href="{r}recruit/">
        <img src="{r}assets/img/recruit03.jpg" alt="天井のエアコンを点検する工事スタッフ" width="720" height="516" loading="lazy">
        <div class="card__b"><p class="card__t">採用情報</p><p>工事スタッフ・営業職・テレフォンアポインター・管理職責任者の4職種を募集しています。</p><span class="more">募集中の仕事を見る</span></div>
      </a></li>
    </ul>
    <p class="more-line center">お電話でも受け付けています　<a href="tel:{TEL_RAW}">{TEL}</a>（FAX {FAX}）</p>
  </div>
</section>
"""
    return page("会社案内｜株式会社パーソンライト", p_company.DESC, d, "company", body, band=False, ld=jsonld())


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
  <div class="wrap phero__split">
    <div>
      <p class="en">RECRUIT</p>
      <h1>天井に上がる人も、電話をかける人も、募集しています。</h1>
      <p class="lead">自分から動ける人、新しいことに挑戦したい人を探しています。正社員は土日祝休み、年間休日120日です。</p>
      <div class="cta-pair"><a class="btn btn--main" href="#jobs">募集中の仕事を見る</a><a class="btn btn--line" href="tel:{TEL_RAW}">電話で応募する　{TEL}</a></div>
    </div>
    <figure class="phero__fig"><img src="{r}assets/img/recruit03.jpg" alt="天井のエアコンを点検する工事スタッフ" width="720" height="516" fetchpriority="high"></figure>
  </div>
  <div class="wrap">
    <nav class="chips" aria-label="このページの目次"><ul>
      <li><a href="#philosophy">理念</a></li><li><a href="#work">仕事を知る</a></li><li><a href="#people">人を知る</a></li>
      <li><a href="#fit">来てほしい人</a></li><li><a href="#numbers">数字で見る</a></li><li><a href="#jobs">募集職種</a></li><li><a href="#faq">応募について</a></li>
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
<section class="sec sec--tint" id="work">
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
<section class="sec" id="people">
  <div class="wrap">
    {sec_head("PEOPLE", "人を知る", "一緒に働いている人の、ひとことです。")}
    <ul class="staff">{people}</ul>
    <p class="more-line"><a class="more" href="{r}company/#members">スタッフ全員を見る</a></p>
    {tbd("社員インタビュー（入った理由・一日の流れ）。手本はここを一番厚くしている")}
  </div>
</section>
<section class="sec sec--tint" id="fit">
  <div class="wrap">
    {sec_head("", "来てほしい人", "経験より、自分から動けるかを見ています。")}
    <ul class="grid2">
      <li><b>自分から動ける人</b><p>言われるのを待たずに、現場やお客様のために次の手を考えられる人。</p></li>
      <li><b>新しいことに挑戦したい人</b><p>空調から通信機器まで、扱う物が広い会社です。知らない仕事を覚えていくのを楽しめる人。</p></li>
    </ul>
    <h3 class="h3">職種ごとに要ること</h3>
    <dl class="dl">{"".join(f"<div><dt>{j['name']}</dt><dd>{j['req']}</dd></div>" for j in JOBS)}</dl>
    {tbd("合わない人（例：決まった作業だけをしたい人）を会社として言えるか。手本は「合わない人」まで書いて、応募の質と定着を上げている。上の2つの説明文も、代表の言葉で確かめる")}
  </div>
</section>
<section class="sec" id="numbers">
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
<section class="sec sec--tint" id="jobs">
  <div class="wrap">
    {sec_head("POSITIONS", "募集職種", f"いま、{len(JOBS)}つの職種で募集しています。")}
    {job_cards(d)}
  </div>
</section>
<section class="sec" id="faq">
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
    {sec_head("REQUIREMENTS", "募集要項", f"{j['name']}の募集要項です。")}
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
    {sec_head("OTHER POSITIONS", "ほかの募集", "ほかの職種も募集しています。")}
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
                d, "faq", body, band_title="ここに無いことは、電話で聞いてください。", ld=jsonld([faq_ld(all_pairs)]))


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
