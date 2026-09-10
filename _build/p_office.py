# -*- coding: utf-8 -*-
"""通信機器 /office-tech/"""
from common import head, header, phero, cta, footer, jsonld

TITLE = "通信機器｜株式会社パーソンライト"
DESC = "夜間もカラーで撮れる防犯カメラ、富士フイルムの複合機、ビジネスフォン、UTM、サーバーまで。ビジネス現場に最適な機器を一括でご提案・導入します。福島県郡山市の株式会社パーソンライト。"

CAM = [
    ("cam-color.jpg", "夜間カラー撮影に対応したカメラ",
     "暗いなかでも輪郭と色が残ります。服装や車の色まで判別でき、証拠として役に立ちます。"),
    ("cam-dark.jpg", "夜間の撮影に対応していないカメラ",
     "暗くなると、ほとんど何も判別できません。"),
    ("cam-mono.jpg", "夜間のカラー撮影に対応していないカメラ",
     "写ってはいますが白黒のため、色の手がかりは残りません。"),
]

FUJI = [
    ("圧倒的なコストパフォーマンス",
     "現在お使いのプリンターで印刷コストが高いと感じている企業様、ぜひ一度お問合せください。弊社は常にお客様のニーズに応えるため、地域ナンバーワンの低価格を目指しています。"),
    ("高品質な印刷",
     "富士フイルムの複合機は色彩の再現性に優れた製品として市場から高い評価を得ています。高精細な印刷品質で、鮮やかな色彩とシャープなテキストを実現します。"),
    ("高い耐久性",
     "全国のセブン-イレブンに富士フイルムの複合機が設置されています。利用客も多く、環境が不安定なコンビニでも安定して運用されており、その耐久性が高く評価されています。"),
    ("質の高いサポート体制",
     "富士フイルムビジネスイノベーションは全国にメンテナンス拠点を多く設けております。不具合が生じたときも迅速に対応できる体制を整えているため、業務中に機器が不具合を生じたとしても安心してご利用いただけます。"),
]

ITEMS = ["ビジネスフォン", "複合機", "セキュリティ商材", "PC周辺設備", "防犯カメラ", "UTM", "サーバー"]


def build():
    cam = "\n".join(f"""      <figure class="card rise">
        <div class="card__fig"><img src="../assets/img/{f}" alt="{t}" width="1200" height="675" loading="lazy"></div>
        <div class="card__body"><h3 class="card__t">{t}</h3><p class="card__d">{d}</p></div>
      </figure>""" for f, t, d in CAM)

    fuji = "\n".join(f"""      <li class="rise"><h3 class="merit__t"><i>{i+1:02d}</i>{t}</h3><p class="merit__d">{d}</p></li>"""
                     for i, (t, d) in enumerate(FUJI))

    items = "".join(f"<li>{i}</li>" for i in ITEMS)

    return head(TITLE, DESC, "office-tech", 1, extra=jsonld(1)) + header("office-tech", 1) + f"""
<main id="main">
""" + phero("Office Tech", "通信機器",
            "防犯カメラをはじめ、電話機、コピー機、IT・通信機器まで。ビジネス現場に最適な機器を一括でご提案・導入いたします。",
            "cam-hero.jpg", "建物の外壁に設置された防犯カメラ",
            [("通信機器", "")], 1) + f"""

<section class="sec" id="camera">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Security Camera</span>
      <h2 class="lead__ja">安心・安全な職場や店舗づくりを、<br>私たちがサポートします</h2>
      <p class="lead__note">弊社では、夜間でもカラー撮影が可能な防犯カメラを取り扱っております。暗闇でも鮮明なカラー映像を提供し、犯罪の抑止や証拠収集に非常に効果的です。</p>
    </div>
    <div class="grid grid--3">
{cam}
    </div>
    <p class="note rise" style="margin-top:26px">いずれも夜間の映像です。同じ場所を、対応機と非対応機で撮り比べています。</p>
  </div>
</section>

<section class="band band--sub sec on-dark" id="compare">
  <div class="band__ph"><img src="../assets/img/cam-color.jpg" alt="" width="1200" height="675" loading="lazy"></div>
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Comparison</span>
      <h2 class="lead__ja">金額で見送った方こそ、<br>もう一度比べてください</h2>
      <p class="lead__note">以前、防犯カメラを検討されていたお客様の中には、金額が高くて導入を見送った方もいらっしゃるかと思います。ぜひ一度、弊社の条件と比較してみてください。夜間のカラー撮影はもちろん、動体検知や遠隔操作など、最新の技術を搭載しています。これにより、より安心で効率的な監視が可能です。</p>
      <p class="lead__note">業種や設置環境、目的に応じて、最適な機種と設置方法をご提案いたします。設置工事からサポート体制まで、すべて弊社にお任せください。</p>
    </div>
    <p style="margin-top:40px"><a class="btn btn--onDark" href="../contact/">防犯カメラの相談をする</a></p>
  </div>
</section>

<section class="sec" id="printer">
  <div class="wrap">
    <div class="duo duo--rev">
      <figure class="duo__fig rise">
        <img src="../assets/img/printer.png" alt="富士フイルムの複合機" width="800" height="600" loading="lazy" style="background:#fff;object-fit:contain">
      </figure>
      <div class="rise">
        <div class="lead">
          <span class="lead__en">Multifunction Printer</span>
          <h2 class="lead__ja">富士フイルム複合機</h2>
        </div>
        <p>導入コスト、印刷コストで<b class="num" style="font-size:1.5em;color:var(--teal)">地域No.1</b>を目指します。</p>
        <p>顧客満足度は、J.D.パワーの調査で9年連続1位。高品質な製品とサービスでお客様をサポートし、貴社の業務に貢献いたします。</p>
      </div>
    </div>
    <ul class="merit rise" style="margin-top:clamp(40px,5vw,68px)">
{fuji}
    </ul>
  </div>
</section>

<section class="sec--tight" id="lineup" style="padding-bottom:var(--sec);background:var(--paper-2)">
  <div class="narrow">
    <div class="lead lead--c rise">
      <span class="lead__en">Line Up</span>
      <h2 class="lead__ja">通信事業の取り扱い</h2>
    </div>
    <ul class="chips rise">{items}</ul>
  </div>
</section>

</main>
""" + cta(1, "cam-hero.jpg") + footer(1)
