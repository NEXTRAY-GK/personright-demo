# -*- coding: utf-8 -*-
"""通信機器 /office-tech/（2026-09-16 第3版）

   並びを「取り扱い → 夜の映像の見比べ（スクロールで切り替わる）→ 複合機」にした。
"""
from common import head, header, phero, footer, jsonld, sh

TITLE = "防犯カメラ・複合機・ビジネスフォン｜株式会社パーソンライト"
DESC = "夜間もカラーで撮れる防犯カメラ、富士フイルムの複合機、ビジネスフォン、UTM、サーバーまで。機種選びから取り付けまで、福島県郡山市の株式会社パーソンライトにご相談ください。"

CAM = [
    ("cam-dark.jpg", 520, 242, "夜の撮影に対応していないカメラ",
     "暗くなると、ほとんど何も見分けられません。"),
    ("cam-mono.jpg", 520, 242, "夜のカラー撮影に対応していないカメラ",
     "写ってはいますが白黒なので、色まではわかりません。"),
    ("cam-color.jpg", 1080, 504, "夜のカラー撮影に対応したカメラ",
     "暗い中でも形と色が残ります。服や車の色まで見分けられるので、いざというときの手がかりになります。"),
]

FUJI = [
    ("印刷の費用",
     "いまのプリンターで印刷代が高いと感じているなら、一度ご相談ください。入れるときの費用も印刷の費用も、地域でいちばんの安さを目指しています。"),
    ("きれいな印刷",
     "富士フイルムの複合機は、色がきれいに出ることで評判の製品です。"),
    ("丈夫さ",
     "全国のセブン-イレブンにも、富士フイルムの複合機が置かれています。大勢の人が使い、置き場所の環境もさまざまなコンビニでも、安定して動いています。"),
    ("困ったときのサポート",
     "富士フイルムビジネスイノベーションは全国にメンテナンスの拠点が多くあるので、仕事中に調子が悪くなっても、すぐに対応してもらえます。"),
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
            "電話機や複合機、防犯カメラ、UTM、サーバーも扱っています。どれを選べばいいかの相談から取り付けまで、まとめてお任せください。",
            "cam-hero.jpg", "建物の外壁に設置された防犯カメラ", [("通信機器", "")], 1, 1600, 587) + f"""

<section class="sec" id="lineup">
  <div class="wrap">
    {sh("", "取り扱っている機器", "事務所の機器のことも、<br>まとめてご相談ください。")}
    <ul class="chips rise" data-k="through" data-steps>{items}</ul>
  </div>
</section>

<section class="nv" id="camera" aria-labelledby="nvH">
  <div class="nv__stage">
    <div class="wrap nv__in">
      <div class="nv__l">
        <p class="sh__no mono"><span>防犯カメラ</span></p>
        <h2 class="big" id="nvH">夜の映像で、<br>比べてみてください。</h2>
        <p class="lede">同じ場所を、夜に3種類のカメラで撮った映像です。スクロールすると切り替わります。当社で扱っているのは、夜でもカラーで撮れるカメラです。</p>
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
      <p class="sh__no mono"><span>お見積り</span></p>
      <h2 class="big">値段で<br>あきらめた方にも、<br>もう一度見てほしい。</h2>
    </div>
    <div class="rise">
      <p class="lede">以前に防犯カメラを考えたものの、値段を見て見送った方もいらっしゃると思います。一度、当社の条件と比べてみてください。夜のカラー撮影のほか、動くものを見つけて知らせる機能や、離れた場所からの操作にも対応しています。</p>
      <p class="lede">お仕事の内容や取り付ける場所、何のために付けたいのかをうかがってから、機種と取り付け方をご提案します。</p>
      <p class="more"><a class="btn" href="../contact/">防犯カメラの相談をする</a></p>
    </div>
  </div>
</section>

<section class="sec sec--p2" id="printer">
  <div class="wrap">
    {sh("", "複合機", "複合機は、<br>富士フイルムを扱っています。", "J.D.パワーの顧客満足度調査で、9年連続1位になった複合機です。")}
    <div class="duo duo--top">
      <figure class="pr rise" data-k="through">
        <div class="pr__paper" aria-hidden="true"><b></b><i style="--i:1"></i><i style="--i:2"></i><i style="--i:3"></i><i style="--i:4"></i><i style="--i:5"></i><i style="--i:6"></i></div>
        <img src="../assets/img/printer.png" alt="富士フイルムの複合機" width="491" height="397" loading="lazy">
      </figure>
      <ol class="merits merits--1" data-k="through" data-steps>
{fuji}
      </ol>
    </div>
  </div>
</section>

</main>
""" + footer(1)
