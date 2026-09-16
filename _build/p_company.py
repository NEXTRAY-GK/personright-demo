# -*- coding: utf-8 -*-
"""会社案内 /company/（2026-09-16 第3版）

   並びを「概要と歩み → 代表から → 理念 → 人 → 場所」にした。
   スタッフの一言は本人の言葉なので、そのまま。
"""
from common import head, header, phero, footer, jsonld, sh, TEL, TEL_RAW, FAX, ZIP, ADDR

TITLE = "会社案内｜株式会社パーソンライト"
DESC = "企業理念は「サービス＆貢献」。福島県郡山市で空調・通信機器の販売と各種設備工事を行う株式会社パーソンライトの会社概要・沿革・スタッフ・アクセス。"

OUTLINE = [
    ("社名", "株式会社パーソンライト"),
    ("代表者", "代表取締役社長　増子 佑"),
    ("本社", f'{ZIP}　{ADDR}<br>TEL <a class="mono" href="tel:{TEL_RAW}">{TEL}</a>　FAX <span class="mono">{FAX}</span>'),
    ("事業内容", '空調・通信機器販売、各種設備工事、テレマーケティング事業<br><a class="tl" href="../#madoguchi">事業の一覧を見る</a>'),
    ("設立", "令和4年12月28日"),
    ("資本金", "300万円"),
    ("従業員数", "15名"),
]

HIST = [
    ("2020.05", "福島県須賀川市に、業務用空調機の取付・保守・メンテナンス会社として創業"),
    ("2022.12", "株式会社 Person right を設立"),
    ("2025.03", "郡山営業所を設立"),
    ("2025.03", "新潟県新潟市に合同会社 Ambit を設立"),
    ("2025.05", "本社を郡山市へ移転"),
]

STAFF = [
    ("staff01", "代表取締役", "Y.M", "人生はチャレンジ！失敗の連続！目線高く共に前に進み続けよう！"),
    ("staff02", "広報部長", "K.M", "全員が楽しく取り組めるように 元気いっぱい♪笑顔いっぱい♪"),
    ("staff03", "総務部長", "Y.J", "楽しいと思える職場を創る為に 常に全力で自分が楽しむ〜♬"),
    ("staff13", "社員", "M.O", "おいしい物を食べる為、全力で頑張ります。"),
    ("staff04", "環境部 営業部長", "K.H", "明るく元気が取り柄です。ゆっくりじっくり笑顔で対応させて頂きます。"),
    ("staff09", "環境部 営業主任", "J.I", "お客様に喜んでいただけるような仕事をします。"),
    ("staff14", "通信機器部 営業部長", "H.M", "お困り事がございましたらお気軽にご相談ください。"),
    ("staff15", "通信機器部 営業課長", "S.Y", "みんなと共に成長します！お客様目線に立った提案をします！"),
    ("staff19", "通信機器部 営業社員", "J.M", "お客様の立場になって考え、納得いただけるご提案を心がけています。"),
    ("staff10", "工事部 部長", "Y.S", "安心・安全・元気な施工を心がけます。"),
    ("staff11", "工事部 係長", "D.K", "確実・丁寧な施工対応を致します。日々精進!!"),
    ("staff16", "工事部 主任", "Y.S", "清く、正しく、泥臭く！"),
    ("staff06", "パートリーダー", "M.Y", "糖分とみんなの笑顔が大好物です。常に楽しく取り組みます(笑)"),
    ("staff12", "パートサブリーダー", "C.O", "いつも笑顔をモットーにがんばります。みんなで毎日HAPPYに!!"),
    ("staff17", "パート", "T.M", "筋トレが大好きな美容オタクです!! 健康第一!!"),
    ("staff08", "広報", "まめ", "きゃんきゃんきゃん♬"),
    ("staff20", "広報", "むぎ", "むぎ♪むぎ♫むぎ♬"),
    ("staff07", "広報", "イブ（永眠）", "ぶぅ〜ぶぅ〜ぶぅ〜♪"),
]

MAP = "https://www.google.com/maps/search/?api=1&query=" + "福島県郡山市安積町日出山2-43"


def build():
    outline = "\n".join(f"""      <div><dt>{k}</dt><dd>{v}</dd></div>""" for k, v in OUTLINE)
    hist = "\n".join(f"""      <li><span class="mono">{y}</span><p>{d}</p></li>""" for y, d in HIST)
    staff = "\n".join(f"""      <figure class="st rise">
        <img src="../assets/img/{f}.jpg" alt="{r}　{n}" width="320" height="320" loading="lazy">
        <figcaption>
          <small>{r}</small>
          <b class="mono">{n}</b>
          <span>{c}</span>
        </figcaption>
      </figure>""" for f, r, n, c in STAFF)

    return head(TITLE, DESC, "company", 1, extra=jsonld(1)) + header("company", 1) + f"""
<main id="main">
""" + phero("04", "COMPANY", "会社案内",
            "2020年に須賀川市で、業務用空調機の取付・保守・メンテナンス会社として始まりました。いまは郡山市に本社を置いています。",
            "office-side.jpg", "Person right の看板を掲げた本社の外観", [("会社案内", "")], 1, 1023, 655) + f"""

<section class="sec" id="outline">
  <div class="wrap duo duo--top">
    <div>
      {sh("01", "概要", "会社の概要")}
      <dl class="spec rise">
{outline}
      </dl>
    </div>
    <div>
      {sh("02", "沿革", "歩み")}
      <ol class="hist rise">
{hist}
      </ol>
      <figure class="clip rise">
        <img src="../assets/img/media.jpg" alt="地元紙に掲載された「私たち創業しました！」の記事" width="700" height="990" loading="lazy">
        <figcaption>創業時に地元紙でご紹介いただきました。</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="sec sec--ink" id="message">
  <div class="wrap">
    <figure class="ceo rise">
      <img src="../assets/img/ceo-bg.jpg" alt="社内のソファに腰かけた代表取締役社長 増子佑" width="1600" height="431" loading="lazy">
    </figure>
    <div class="duo">
      <p class="sh__no mono rise"><b>03</b><span>代表から</span></p>
      <div class="rise">
        <h2 class="big">お客様も、社員も、<br>関わる全員と前へ。</h2>
        <p class="lede">お客様はもちろん、当社の社員含め、パーソンライトに関わる全ての皆様と共に輝かしい未来へ。創造と挑戦の歩みを止めず、日々成長してまいります。</p>
        <p class="sign">代表取締役社長　<b>増子　佑</b></p>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="philosophy">
  <div class="wrap duo duo--top">
    <div class="rise">
      <p class="sh__no mono"><b>04</b><span>企業理念</span></p>
      <h2 class="creed">サービス＆貢献</h2>
      <p class="lede">「パーソンライトに相談して良かった！」と心の底からお喜び頂けるよう、お客様が求めているサービスを展開し、笑顔や喜びにあふれた社会づくりを目指しています。</p>
    </div>
    <div class="posters rise">
      <img src="../assets/img/philosophy01.jpg" alt="社内に掲げた経営理念「顧客作り創造企業 〜全ては結果と報連相〜」の掲示物" width="546" height="772" loading="lazy">
      <img src="../assets/img/philosophy02.jpg" alt="社内に掲げた行動指針「全ては結果と報連相」の掲示物" width="546" height="772" loading="lazy">
    </div>
  </div>
</section>

<section class="sec sec--p2" id="staff">
  <div class="wrap">
    {sh("05", "人", "一緒に働いている顔ぶれ。", "環境部・通信機器部・工事部・総務。広報の3匹も含めて。")}
    <div class="sts">
{staff}
    </div>
  </div>
</section>

<section class="sec" id="access">
  <div class="wrap duo">
    <figure class="scan-wrap rise">
      <div class="scan" data-scan>
        <img class="scan__real" src="../assets/img/office-front.jpg" alt="福島県郡山市安積町日出山にある本社の外観" width="810" height="555" loading="lazy">
        <img class="scan__heat" src="../assets/img/office-front.jpg" alt="" width="810" height="555" loading="lazy" aria-hidden="true">
        <i class="scan__line" aria-hidden="true"></i>
      </div>
    </figure>
    <div class="rise">
      <p class="sh__no mono"><b>06</b><span>アクセス</span></p>
      <h2 class="big">本社</h2>
      <address class="addr">{ZIP}<br>{ADDR}<br>TEL <a class="mono" href="tel:{TEL_RAW}">{TEL}</a>　FAX <span class="mono">{FAX}</span></address>
      <p class="more"><a class="btn" href="{MAP}" target="_blank" rel="noopener">Google マップで開く</a></p>
    </div>
  </div>
</section>

</main>
""" + footer(1)
