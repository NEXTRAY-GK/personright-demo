# -*- coding: utf-8 -*-
"""会社案内 /company/"""
from common import head, header, phero, cta, footer, jsonld, TEL, TEL_RAW, FAX, ZIP, ADDR

TITLE = "会社案内｜株式会社パーソンライト"
DESC = "「サービス＆貢献」を企業理念に、福島県郡山市で空調・通信機器の販売と各種設備工事を行う株式会社パーソンライトの会社概要・沿革・スタッフのご紹介。"

OUTLINE = [
    ("社名", "株式会社パーソンライト"),
    ("代表者", "代表取締役社長　増子 佑"),
    ("本社", f'{ZIP}　{ADDR}<br>TEL <a class="num" href="tel:{TEL_RAW}">{TEL}</a>　FAX <span class="num">{FAX}</span>'),
    ("事業内容", '空調・通信機器販売、各種設備工事、テレマーケティング事業<br><a class="tlink" href="../#works" style="margin-top:10px">事業内容の詳細を見る</a>'),
    ("設立", "令和4年12月28日"),
    ("資本金", "300万円"),
    ("従業員数", "15名"),
]

HIST = [
    ("2020年5月", "福島県須賀川市に、業務用空調機の取付・保守・メンテナンス会社として創業"),
    ("2022年12月", "株式会社 Person right を設立"),
    ("2025年3月", "郡山営業所を設立"),
    ("2025年3月", "新潟県新潟市に合同会社 Ambit を設立"),
    ("2025年5月", "本社を郡山市へ移転"),
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

SLIDER = [
    ("work-desk.jpg", "事務所で電話を受ける社員"),
    ("work-ceiling.jpg", "天井カセット形エアコンの分解作業"),
    ("work-outdoor.jpg", "外壁での室外機の据付工事"),
    ("work-filter.jpg", "天井カセット形エアコンのフィルター清掃"),
    ("work-attic.jpg", "天井裏の配管・配線作業"),
    ("dog-mame.jpg", "事務所にいる広報のまめ"),
]

MAP = "https://www.google.com/maps/search/?api=1&query=" + "福島県郡山市安積町日出山2-43".replace(" ", "+")


def build():
    outline = "\n".join(f"""    <div><dt><span>{k}</span></dt><dd>{v}</dd></div>""" for k, v in OUTLINE)
    hist = "\n".join(f"""      <li><span class="hist__y num">{y}</span><p class="hist__d">{d}</p></li>""" for y, d in HIST)
    staff = "\n".join(f"""      <figure class="stf rise">
        <img src="../assets/img/{f}.jpg" alt="{r}　{n}" width="520" height="520" loading="lazy">
        <figcaption>
          <span class="stf__r">{r}</span>
          <b class="stf__n">{n}</b>
          <span class="stf__c">{c}</span>
        </figcaption>
      </figure>""" for f, r, n, c in STAFF)
    slider = "\n".join(f"""      <img src="../assets/img/{f}" alt="{a}" width="1200" height="1200" loading="lazy">""" for f, a in SLIDER)

    return head(TITLE, DESC, "company", 1, extra=jsonld(1)) + header("company", 1) + f"""
<main id="main">
""" + phero("Company", "会社案内", None, "office-side.jpg",
            "Person right の看板を掲げた本社の外観", [("会社案内", "")], 1) + f"""

<section class="sec" id="message">
  <div class="wrap">
    <div class="duo">
      <figure class="duo__fig rise">
        <img src="../assets/img/ceo-bg.jpg" alt="社内のソファに腰かけた代表取締役社長 増子佑" width="1600" height="442" loading="lazy" style="object-position:74% center">
        <figcaption>MESSAGE</figcaption>
      </figure>
      <div class="rise">
        <div class="lead">
          <span class="lead__en">Message</span>
          <h2 class="lead__ja">代表あいさつ</h2>
        </div>
        <p class="msg">お客様はもちろん、当社の社員含め、パーソンライトに関わる全ての皆様と共に輝かしい未来へ。<br>創造と挑戦の歩みを止めず、日々成長してまいります。</p>
        <p class="sign">代表取締役社長　<b>増子　佑</b></p>
      </div>
    </div>
  </div>
</section>

<section class="band band--sub sec on-dark" id="philosophy">
  <div class="band__ph"><img src="../assets/img/work-desk.jpg" alt="" width="1200" height="900" loading="lazy"></div>
  <div class="narrow">
    <div class="lead lead--c rise">
      <span class="lead__en">Philosophy</span>
      <h2 class="lead__ja">企業理念</h2>
    </div>
    <p class="creed rise">サービス＆貢献</p>
    <p class="rise" style="text-align:center;color:rgba(255,255,255,.86);max-width:56ch;margin-inline:auto">「パーソンライトに相談して良かった！」と心の底からお喜び頂けるよう、お客様が求めているサービスを展開し、笑顔や喜びにあふれた社会づくりを目指しています。</p>
    <div class="grid grid--2 rise" style="margin-top:clamp(40px,5vw,64px)">
      <figure class="pcard"><img src="../assets/img/philosophy01.jpg" alt="社内に掲げた経営理念「顧客作り創造企業 〜全ては結果と報連相〜」の掲示物" width="1000" height="1414" loading="lazy"></figure>
      <figure class="pcard"><img src="../assets/img/philosophy02.jpg" alt="社内に掲げた行動指針「全ては結果と報連相」の掲示物" width="1000" height="1414" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="sec" id="outline">
  <div class="narrow">
    <div class="lead rise">
      <span class="lead__en">Outline</span>
      <h2 class="lead__ja">会社概要</h2>
    </div>
    <dl class="deft rise">
{outline}
    </dl>
  </div>
</section>

<section class="sec--tight" id="history" style="padding-bottom:var(--sec);background:var(--paper-2)">
  <div class="narrow">
    <div class="lead rise">
      <span class="lead__en">History</span>
      <h2 class="lead__ja">沿革</h2>
    </div>
    <ol class="hist rise">
{hist}
    </ol>
    <figure class="media rise">
      <img src="../assets/img/media.jpg" alt="地元紙に掲載された「私たち創業しました！」の記事" width="1000" height="1414" loading="lazy">
      <figcaption>創業時に地元紙でご紹介いただきました。</figcaption>
    </figure>
  </div>
</section>

<section class="sec" id="access">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Access</span>
      <h2 class="lead__ja">アクセス</h2>
    </div>
    <div class="duo">
      <figure class="duo__fig rise">
        <img src="../assets/img/office-front.jpg" alt="福島県郡山市安積町日出山にある本社の外観" width="1600" height="1096" loading="lazy">
        <figcaption>本社</figcaption>
      </figure>
      <div class="rise">
        <p class="acc__t">本社</p>
        <address class="acc__a">{ZIP}<br>{ADDR}<br>TEL <a class="num" href="tel:{TEL_RAW}">{TEL}</a>　FAX <span class="num">{FAX}</span></address>
        <p style="margin-top:26px"><a class="btn" href="{MAP}" target="_blank" rel="noopener">Google マップで見る</a></p>
      </div>
    </div>
  </div>
</section>

<section class="sec--tight" id="staff" style="padding-bottom:var(--sec)">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Staff</span>
      <h2 class="lead__ja">スタッフ紹介</h2>
      <p class="lead__note">環境部・通信機器部・工事部・総務の4部門です。</p>
    </div>
    <div class="stfs">
{staff}
    </div>
  </div>
</section>

<section class="sec--tight" style="padding-top:0">
  <div class="strip rise">
{slider}
  </div>
</section>

</main>
""" + cta(1, "office-side.jpg") + footer(1)
