# -*- coding: utf-8 -*-
"""通信機器 /office-tech/（2026-09-16 第3版）

   並びを「取り扱い → 夜の映像の見比べ（スクロールで切り替わる）→ 複合機」にした。
"""
from common import head, header, phero, footer, jsonld, sh

TITLE = "防犯カメラ・複合機・ビジネスフォン｜株式会社パーソンライト"
DESC = "夜間もカラーで撮れる防犯カメラ、富士フイルムの複合機、ビジネスフォン、UTM、サーバーまで。福島県郡山市の株式会社パーソンライトがご提案から設置まで承ります。"

CAM = [
    ("cam-dark.jpg", 520, 242, "夜間の撮影に対応していないカメラ",
     "暗くなると、ほとんど何も判別できません。"),
    ("cam-mono.jpg", 520, 242, "夜間のカラー撮影に対応していないカメラ",
     "写ってはいますが白黒のため、色の手がかりは残りません。"),
    ("cam-color.jpg", 1080, 504, "夜間カラー撮影に対応したカメラ",
     "暗いなかでも輪郭と色が残ります。服装や車の色まで判別でき、証拠として役に立ちます。"),
]

FUJI = [
    ("コストパフォーマンス",
     "いまお使いのプリンターの印刷コストが高いと感じていれば、一度ご相談ください。導入コスト・印刷コストで地域ナンバーワンの低価格を目指しています。"),
    ("高品質な印刷",
     "富士フイルムの複合機は、色の再現性に優れた製品として市場から高い評価を得ています。"),
    ("高い耐久性",
     "全国のセブン-イレブンに富士フイルムの複合機が設置されています。利用客が多く、環境が安定しないコンビニでも安定して動いています。"),
    ("サポート体制",
     "富士フイルムビジネスイノベーションは全国にメンテナンス拠点を多く設けており、業務中に不具合が出ても迅速に対応できる体制があります。"),
]

ITEMS = ["ビジネスフォン", "複合機", "セキュリティ商材", "PC周辺設備", "防犯カメラ", "UTM", "サーバー"]


def build():
    layers = "\n".join(f"""        <figure class="nv__i" data-nv="{i}">
          <img src="../assets/img/{f}" alt="{t}の夜間の映像" width="{w}" height="{h}" loading="lazy">
        </figure>""" for i, (f, w, h, t, d) in enumerate(CAM))
    caps = "\n".join(f"""        <li data-nv="{i}"><span class="mono">{i+1:02d}</span><b>{t}</b><p>{d}</p></li>""" for i, (f, w, h, t, d) in enumerate(CAM))

    fuji = "\n".join(f"""      <li class="rise"><span class="mono">{i+1:02d}</span><b>{t}</b><p>{d}</p></li>"""
                     for i, (t, d) in enumerate(FUJI))

    items = "".join(f"<li>{i}</li>" for i in ITEMS)

    return head(TITLE, DESC, "office-tech", 1, extra=jsonld(1)) + header("office-tech", 1) + f"""
<main id="main">
""" + phero("02", "OFFICE TECH", "通信機器",
            "電話機、複合機、防犯カメラ、UTM、サーバー。事務所の機器を選ぶところから設置まで、まとめてご相談ください。",
            "cam-hero.jpg", "建物の外壁に設置された防犯カメラ", [("通信機器", "")], 1, 1600, 587) + f"""

<section class="sec" id="lineup">
  <div class="wrap">
    {sh("01", "取り扱い", "事務所の機器を、<br>ひとつの窓口で。")}
    <ul class="chips rise">{items}</ul>
  </div>
</section>

<section class="nv" id="camera" aria-labelledby="nvH">
  <div class="nv__stage">
    <div class="wrap nv__in">
      <div class="nv__l">
        <p class="sh__no mono"><b>02</b><span>防犯カメラ</span></p>
        <h2 class="big" id="nvH">夜の映像で、<br>比べてください。</h2>
        <p class="lede">同じ夜間の撮影を、3種類のカメラで並べました。スクロールすると切り替わります。当社が扱うのは、夜間もカラーで撮れるカメラです。</p>
        <ol class="nv__caps">
{caps}
        </ol>
      </div>
      <div class="nv__r">
        <div class="nv__view">
{layers}
          <p class="nv__osd mono" aria-hidden="true"><span class="nv__rec"><i></i>REC</span><span>CAM 01　NIGHT</span></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="compare">
  <div class="wrap duo">
    <div class="rise">
      <p class="sh__no mono"><b>02-b</b><span>見積り</span></p>
      <h2 class="big">金額で見送った方こそ、<br>もう一度。</h2>
    </div>
    <div class="rise">
      <p class="lede">以前、防犯カメラを検討して、金額で導入を見送った方もいらっしゃるかと思います。当社の条件と比べてみてください。夜間のカラー撮影のほか、動体検知や遠隔操作にも対応しています。</p>
      <p class="lede">業種や設置環境、目的に応じて、機種と設置方法をご提案します。</p>
      <p class="more"><a class="btn" href="../contact/">防犯カメラの相談をする</a></p>
    </div>
  </div>
</section>

<section class="sec sec--p2" id="printer">
  <div class="wrap">
    {sh("03", "複合機", "複合機は、<br>富士フイルム。", "顧客満足度は、J.D.パワーの調査で9年連続1位。導入コスト・印刷コストで地域No.1を目指します。")}
    <div class="duo duo--top">
      <figure class="pr rise">
        <img src="../assets/img/printer.png" alt="富士フイルムの複合機" width="491" height="397" loading="lazy">
      </figure>
      <ol class="merits merits--1">
{fuji}
      </ol>
    </div>
  </div>
</section>

</main>
""" + footer(1)
