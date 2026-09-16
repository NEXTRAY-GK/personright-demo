# -*- coding: utf-8 -*-
"""お客様の声 /reviews/ と個票4本（2026-09-16 第3版）
   声の本文はお客様の言葉なので、そのまま。"""
from common import head, header, phero, footer, jsonld, sh

VOICES = [
    {"id": "98", "title": "最適な提案と確かな技術で大満足です。", "who": "田村市　N様",
     "img": "case-install01.jpg", "w": 640, "h": 800, "alt": "天井を開け、天井裏で作業する工事の様子",
     "body": ["会社のエアコン設置をお願いしました。こちらの要望をしっかりヒアリングしていただき、最適な機種や設置方法を提案してもらえました。",
              "コスト面も含めて納得のいく内容で、仕上がりも大満足です。またお願いしたいと思います。"]},
    {"id": "96", "title": "業務への影響を最小限に、スムーズな設置でした。", "who": "郡山市　M様",
     "img": "case-install02.jpg", "w": 640, "h": 480, "alt": "建物の外壁に据え付けた業務用エアコンの室外機",
     "body": ["オフィスのエアコンを新しく設置していただきました。作業が迅速かつ丁寧で、業務の妨げにならないよう配慮いただき助かりました。",
              "社内が快適になり、社員からも好評です。プロの仕事に感謝しています。"]},
    {"id": "53", "title": "通常業務もストップすることなく完了しました。", "who": "須賀川市内　某社 様",
     "img": "case-shop.jpg", "w": 780, "h": 611, "alt": "店舗の天井に設置した天井カセット形エアコン",
     "body": ["空調設備の老朽化に伴い、空調更新工事をお願いしました。変電設備を増やす工事に伴っては、工場内を計画的に停電させる必要がありましたが、こちらもスケジュール通り安全に進めていただき、業務もストップすることなく完了しました。",
              "リースの内容も詳しく説明していただき、とても助かりました。"]},
    {"id": "56", "title": "とても作業が丁寧で、安心して見ていました。", "who": "郡山市　S.T 様",
     "img": "case-house.jpg", "w": 640, "h": 427, "alt": "工場の外壁に並べて設置した業務用エアコンの室外機",
     "body": ["丁寧なご説明とご提案をいただきました。タイミングもよく、翌日には対応いただき大変助かりました。元気のある青年で良かったです。",
              "エアコンのカバーも綺麗にやっていただき満足しています。"]},
]


def build_index():
    title = "お客様の声｜株式会社パーソンライト"
    desc = "業務用エアコンの設置・更新工事をご利用いただいたお客様からのお声を掲載しています。福島県郡山市の株式会社パーソンライト。"
    cards = "\n".join(f"""      <article class="vc rise">
        <a href="./{v['id']}/">
          <p class="vc__who">{v['who']}</p>
          <h2 class="vc__t">「{v['title']}」</h2>
          <p class="vc__d">{v['body'][0]}</p>
          <span class="vc__go">続きを読む →</span>
        </a>
      </article>""" for i, v in enumerate(VOICES))

    return head(title, desc, "reviews", 1, extra=jsonld(1)) + header("reviews", 1) + f"""
<main id="main">
""" + phero("03", "VOICES", "お客様の声",
            "工事が終わってからが、本当のお付き合いの始まりだと考えています。いただいた声は、そのあとのフォローに活かしています。",
            None, None, [("お客様の声", "")], 1) + f"""

<section class="sec sec--flush">
  <div class="wrap">
    <div class="vcs">
{cards}
    </div>
  </div>
</section>

</main>
""" + footer(1)


def build_one(v):
    i = [x["id"] for x in VOICES].index(v["id"])
    prev = VOICES[i - 1] if i > 0 else None
    nxt = VOICES[i + 1] if i < len(VOICES) - 1 else None
    title = f"{v['title']}｜お客様の声｜株式会社パーソンライト"
    desc = v["body"][0][:110]
    body = "\n".join(f"<p>{b}</p>" for b in v["body"])
    nav = []
    if prev:
        nav.append(f'<a class="pn__p" href="../{prev["id"]}/"><small>← 前の声</small><span>{prev["title"]}</span></a>')
    if nxt:
        nav.append(f'<a class="pn__n" href="../{nxt["id"]}/"><small>次の声 →</small><span>{nxt["title"]}</span></a>')

    return head(title, desc, "reviews", 2, og=v["img"], extra=jsonld(2)) + header("reviews", 2) + f"""
<main id="main">
""" + phero(f"03-{i+1}", "VOICE", f"「{v['title']}」", v["who"], v["img"], v["alt"],
            [("お客様の声", "reviews/"), (v["title"], "")], 2, v["w"], v["h"]) + f"""

<section class="sec">
  <div class="wrap duo duo--top">
    <p class="sh__no mono"><span>いただいた声</span></p>
    <div>
      <div class="one rise">
{body}
      </div>
      <nav class="pn rise" aria-label="ほかのお客様の声">
        {''.join(nav)}
      </nav>
      <p class="more"><a class="btn" href="../">お客様の声の一覧へ</a></p>
    </div>
  </div>
</section>

</main>
""" + footer(2)
