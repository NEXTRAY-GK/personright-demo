# -*- coding: utf-8 -*-
"""トップページ（2026-09-16 第3版）

   組み立ての考え：
     会社の事業一覧から入らない。読む人の困りごとから入る。
     冒頭は写真ではなく、スクロールで冷えていく部屋の断面（サーモ画像）。
       冷える部屋 → 困りごと6つ → 冷媒で変わる電気代 → 現場の写真 → 窓口は1本 → 声 → 採用
   事実（メーカー・保証・数字・声・求人）はすべて会社の情報から。足していない。
   断面図の温度はイメージで、画面にもそう書く。
"""
from common import head, header, footer, jsonld, sh, TEL, TEL_RAW, INSTA

TITLE = "株式会社パーソンライト｜業務用エアコンの販売・設置工事（福島県郡山市）"
DESC = "福島県郡山市の株式会社パーソンライト。ダイキンをはじめ5社のメーカーから業務用エアコンを選び、自社の工事部で取り付けます。7年保証と年間メンテナンスもご用意しています。リースなら初期費用0円。防犯カメラ・複合機・ビジネスフォンも。"

# 困りごと → 行き先
CASES = [
    ("夏になると、どうも効きが悪い。",
     "分解クリーニングで済むのか、入れ替えたほうがいいのか。まずは今お使いの一台を見せてください。",
     "ac/", "業務用エアコン"),
    ("毎月の電気代が重い。",
     "15年前の機種を最新の省エネ機種に替えると、消費電力は65%下がります。機種によっては最大70%です。",
     "ac/#eco", "替える理由"),
    ("2001年より前のエアコンを、まだ使っている。",
     "その頃の機種に使われている冷媒R22は、もう生産も輸入もされていません。修理用のガスが手に入らなくなる前に、入れ替えを考えてみませんか。",
     "ac/#refrigerant", "R22 のこと"),
    ("開業や入れ替えで、まとまったお金を出すのは厳しい。",
     "リースなら初期費用はかかりません。税務上認められたリース期間なら、支払いを全額経費にできます。",
     "ac/#lease", "リース"),
    ("電話も複合機も、防犯カメラも古くなってきた。",
     "ビジネスフォンや富士フイルムの複合機、夜でもカラーで撮れる防犯カメラ、UTM、サーバーも扱っています。",
     "office-tech/", "通信機器"),
    ("エアコンと一緒に、電気や水回りの工事も頼みたい。",
     "電気工事も水回りの工事も、自社の工事部でお受けします。",
     "company/", "会社案内"),
]

REEL = [
    ("case-install01.jpg", 640, 800, "天井を開け、天井裏で作業する当社の工事スタッフ", "天井を開けての工事", "事務所"),
    ("case-shop.jpg", 780, 611, "店舗の天井に設置した天井カセット形エアコン", "店舗の天井", "店舗"),
    ("case-install02.jpg", 640, 480, "建物の外壁に据え付けた業務用エアコンの室外機", "室外機の据付", "外壁"),
    ("case-house.jpg", 640, 427, "工場の外壁に並べて設置した業務用エアコンの室外機7台", "室外機7台", "工場"),
]

HUB = [
    ("環境事業", ["業務用エアコン", "家庭用エアコン", "空気清浄機", "LED照明", "分解・洗浄クリーニング",
               "エコキュート", "高機能換気設備", "業務用冷蔵庫・冷凍庫", "各種厨房機器"]),
    ("通信事業", ["ビジネスフォン", "複合機", "セキュリティ商材", "PC周辺設備", "防犯カメラ", "UTM", "サーバー"]),
    ("工事部", ["各種工事", "電気工事", "水回り工事"]),
    ("テレマーケティング事業", ["アポイント"]),
]

VOICE = [
    ("最適な提案と確かな技術で大満足です。", "田村市　N様", "98",
     "こちらの要望をしっかりヒアリングしていただき、最適な機種や設置方法を提案してもらえました。コスト面も含めて納得のいく内容で、仕上がりも大満足です。"),
    ("業務への影響を最小限に、スムーズな設置でした。", "郡山市　M様", "96",
     "作業が迅速かつ丁寧で、業務の妨げにならないよう配慮いただき助かりました。社内が快適になり、社員からも好評です。"),
]

JOBS = [
    ("49", "エアコン設備工事スタッフ", "正社員", "月給 220,000〜450,000円"),
    ("46", "営業職", "正社員", "月給 220,000〜650,000円"),
    ("48", "テレフォンアポインター", "パート・アルバイト", "時給 1,100〜1,500円"),
    ("77", "管理職責任者", "正社員", "月給 350,000〜650,000円"),
]


def build():
    cases = "\n".join(f"""      <li class="case rise">
        <a href="./{href}">
          <span class="case__n mono">{i+1:02d}</span>
          <b class="case__t">{t}</b>
          <span class="case__d">{d}</span>
          <span class="case__go mono">{go} →</span>
        </a>
      </li>""" for i, (t, d, href, go) in enumerate(CASES))

    reel = "\n".join(f"""      <figure class="reel__i" style="--ar:{w}/{h}">
        <div class="scan" data-scan>
          <img class="scan__real" src="./assets/img/{f}" alt="{a}" width="{w}" height="{h}" loading="lazy">
          <img class="scan__heat" src="./assets/img/{f}" alt="" width="{w}" height="{h}" loading="lazy" aria-hidden="true">
          <i class="scan__line" aria-hidden="true"></i>
        </div>
        <figcaption><span>{place}</span>{c}</figcaption>
      </figure>""" for i, (f, w, h, a, c, place) in enumerate(REEL))

    hub = "\n".join(f"""      <div class="hub__i rise">
        <h3 class="hub__t"><span class="mono">{i+1:02d}</span>{t}</h3>
        <ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>
      </div>""" for i, (t, items) in enumerate(HUB))

    voice = "\n".join(f"""      <article class="q rise" data-k="read">
        <p class="q__no">{who}</p>
        <h3 class="q__t"><span class="mk">「{t}」</span></h3>
        <p class="q__d">{d}</p>
        <a class="tl" href="./reviews/{vid}/">続きを読む</a>
      </article>""" for i, (t, who, vid, d) in enumerate(VOICE))

    jobs = "\n".join(f"""      <li><a href="./recruit/{jid}/"><b>{n}</b><span>{ty}</span><span class="mono">{pay}</span><i aria-hidden="true">→</i></a></li>"""
                     for jid, n, ty, pay in JOBS)

    return head(TITLE, DESC, "", 0, page="is-top", extra=jsonld(0, [{
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "株式会社パーソンライト", "url": "https://nextray-gk.github.io/personright-demo/",
    }])) + header("", 0) + f"""
<main id="main">

<!-- ================================================ 冒頭 ── 冷えていく部屋 -->
<section class="tm" id="top" aria-labelledby="tmH">
  <div class="tm__stage">
    <canvas class="tm__cv" aria-hidden="true"></canvas>
    <div class="tm__hud mono" aria-hidden="true">
      <span class="tm__rec"><i></i>サーモ画像で見た部屋の断面（温度はイメージです）</span>
      <span class="tm__sp" data-sp="0">SP1 窓際　<b>--.-</b>℃</span>
      <span class="tm__sp" data-sp="1">SP2 机の上　<b>--.-</b>℃</span>
      <span class="tm__sp" data-sp="2">SP3 床の隅　<b>--.-</b>℃</span>
    </div>

    <div class="tm__txt">
      <div class="tm__s" data-s="0">
        <p class="tm__eye">福島県郡山市　業務用エアコンの販売と取り付け</p>
        <h1 class="tm__h" id="tmH">暑い部屋は、<br>天井から冷やす。</h1>
        <p class="tm__p">ダイキンをはじめ5社のメーカーから部屋に合う機種を選び、自社の工事部で取り付けます。付けたあとの7年保証と年間メンテナンスもご用意しています。</p>
        <p class="tm__acts">
          <a class="btn btn--light" href="./contact/">無料で見積りを頼む</a>
          <a class="tl tl--light" href="tel:{TEL_RAW}"><span class="mono">{TEL}</span></a>
        </p>
      </div>
      <div class="tm__s" data-s="1">
        <p class="tm__eye">まず、選ぶ</p>
        <p class="tm__h2">ダイキン、三菱電機、<br>日立、東芝、<br>パナソニック。</p>
        <p class="tm__p">天井に埋め込む形、吊るす形、壁掛け、床置き、厨房用まで12種類あります。部屋の広さや天井のつくりを見て、合うものをご提案します。</p>
      </div>
      <div class="tm__s" data-s="2">
        <p class="tm__eye">次に、取り付ける</p>
        <p class="tm__h2">冷たい空気は下へ、<br>暖まった空気は上へ。</p>
        <p class="tm__p">この流れをじゃましない場所に室内機を置き、配管や排水の傾きをきちんと取ります。同じ機種でも、取り付け方で効き具合は変わります。工事は自社の工事部が行います。</p>
      </div>
      <div class="tm__s" data-s="3">
        <p class="tm__eye">そのあとも、見守る</p>
        <p class="tm__h2">付けたあとも、<br>7年間は保証します。</p>
        <p class="tm__p">年間メンテナンスもご用意しています。古い機種を最新の省エネ機種に替えると、消費電力は最大で70%下がります。</p>
        <p class="tm__acts"><a class="btn btn--light" href="./ac/">業務用エアコンを見る</a></p>
      </div>
    </div>

    <div class="tm__temp" aria-hidden="true">
      <p class="tm__deg"><b class="tm__v">33.8</b><span>℃</span></p>
      <div class="tm__scale mono"><span>22</span><i><em></em></i><span>36℃</span></div>
      <p class="tm__hint"><i></i>スクロールすると、部屋が冷えていきます</p>
    </div>
  </div>
</section>

<!-- ======================================================== メーカー -->
<div class="makers">
  <p>取り扱いメーカー</p>
  <ul><li>ダイキン</li><li>三菱電機</li><li>日立</li><li>東芝</li><li>パナソニック</li></ul>
</div>

<!-- ======================================================== 困りごと -->
<section class="sec" id="cases">
  <div class="wrap">
    {sh("", "ご相談の入り口", "何から聞けばいいか、<br>わからなくても大丈夫です。", "よくいただくご相談を6つにまとめました。近いものから読んでみてください。どれにも当てはまらなければ、そのままお電話ください。")}
    <ol class="cases">
{cases}
    </ol>
  </div>
</section>

<!-- ============================================ 冷媒で変わる電気代（止まって読む） -->
<section class="mt" id="meter" aria-labelledby="mtH">
  <div class="mt__stage">
    <div class="wrap mt__in">
      <div class="mt__l">
        <p class="sh__no mono"><span>電気代</span></p>
        <h2 class="mt__h" id="mtH">同じ部屋を冷やす電気が、<br>いまの冷媒なら5分の1です。</h2>
        <p class="mt__p">R22という冷媒を使った古い機種を100として比べています。2001年より前の機種をお使いなら、気にしていただきたいのは電気代だけではありません。R22はもう生産も輸入もされていないので、修理用のガスが手に入りにくくなっていきます。</p>
        <p><a class="tl" href="./ac/#refrigerant">冷媒と入れ替えについて読む</a></p>
      </div>
      <div class="mt__r">
        <p class="mt__yr mono"><span class="mt__gen">R22（指定フロン）</span><span class="mt__era">2001年以前</span></p>
        <p class="mt__big"><b class="mt__v">100</b><span>%</span></p>
        <div class="mt__bar"><i></i></div>
        <ol class="mt__steps mono">
          <li data-m="0"><b>100</b>R22<small>〜2001</small></li>
          <li data-m="1"><b>60</b>R407・R410<small>2001〜2013</small></li>
          <li data-m="2"><b>20</b>R32<small>2014〜</small></li>
        </ol>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================== 現場（横に流れる） -->
<section class="reel" id="works" aria-labelledby="reelH">
  <div class="reel__stage">
    <div class="wrap reel__hd">
      <p class="sh__no mono"><span>現場</span></p>
      <h2 class="reel__h" id="reelH">天井の中も、壁の外も。</h2>
      <p class="reel__p">事務所や店舗の天井、工場の外壁など、実際に取り付けた現場の写真です。</p>
    </div>
    <div class="reel__track">
{reel}
      <div class="reel__end">
        <p>ほかの現場は、<br>施工実績のページに。</p>
        <a class="tl tl--light" href="./works/">施工実績を見る</a>
      </div>
    </div>
  </div>
</section>

<!-- ======================================================== 窓口は1本 -->
<section class="sec hub" id="madoguchi">
  <div class="wrap">
    {sh("", "窓口", "お電話は、<br>この番号ひとつで。", "空調、通信機器、工事、テレマーケティングの4つを1つの会社でやっています。エアコンの相談のついでに、電話機や複合機のことを聞いていただいても構いません。")}
    <p class="hub__tel rise"><small>お電話</small><a class="mono" href="tel:{TEL_RAW}">{TEL}</a></p>
    <div class="hub__g">
{hub}
    </div>
  </div>
</section>

<!-- ======================================================== 声 -->
<section class="sec sec--p2" id="voice">
  <div class="wrap">
    {sh("", "お客様の声", "工事のあとに、<br>いただいた声です。")}
    <div class="qs">
{voice}
    </div>
    <p class="more rise"><a class="btn" href="./reviews/">お客様の声をすべて読む（4件）</a></p>
  </div>
</section>

<!-- ======================================================== 採用 -->
<section class="sec" id="recruit">
  <div class="wrap rc">
    {sh("", "採用", "天井に上がる人も、<br>電話をかける人も<br>募集しています。", "いま、4つの職種で募集しています。")}
    <ul class="rows rise">
{jobs}
    </ul>
  </div>
</section>

</main>
""" + footer(0)
