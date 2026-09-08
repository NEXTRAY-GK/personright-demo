# -*- coding: utf-8 -*-
"""お客様の声 /reviews/ と個票4本"""
from common import head, header, phero, cta, footer, jsonld

INTRO = ("ご利用いただいたお客様のさまざまなお声を掲載しております。"
         "パーソンライトでは設備機器の工事を終えた後からが本当のお付き合いの始まりであると考えております。"
         "皆様からのご意見をお伺いし、今後のアフターフォローに活かしていきます。")

VOICES = [
    {"id": "98", "title": "最適な提案と確かな技術で大満足です。", "who": "田村市　N様",
     "img": "case-install01.jpg", "alt": "天井カセット形エアコンの入れ替え工事の様子",
     "body": ["会社のエアコン設置をお願いしました。こちらの要望をしっかりヒアリングしていただき、最適な機種や設置方法を提案してもらえました。",
              "コスト面も含めて納得のいく内容で、仕上がりも大満足です。またお願いしたいと思います。"]},
    {"id": "96", "title": "業務への影響を最小限に、スムーズな設置でした。", "who": "郡山市　M様",
     "img": "case-install02.jpg", "alt": "設置を終えた天井カセット形エアコン",
     "body": ["オフィスのエアコンを新しく設置していただきました。作業が迅速かつ丁寧で、業務の妨げにならないよう配慮いただき助かりました。",
              "社内が快適になり、社員からも好評です。プロの仕事に感謝しています。"]},
    {"id": "53", "title": "通常業務もストップすることなく完了しました。", "who": "須賀川市内　某社 様",
     "img": "case-shop.jpg", "alt": "店舗の天井に設置した業務用エアコン",
     "body": ["空調設備の老朽化に伴い、空調更新工事をお願いしました。変電設備を増やす工事に伴っては、工場内を計画的に停電させる必要がありましたが、こちらもスケジュール通り安全に進めていただき、業務もストップすることなく完了しました。",
              "リースの内容も詳しく説明していただき、とても助かりました。"]},
    {"id": "56", "title": "とても作業が丁寧で、安心して見ていました。", "who": "郡山市　S.T 様",
     "img": "case-house.jpg", "alt": "工場の外壁に並べて設置した業務用エアコンの室外機",
     "body": ["丁寧なご説明とご提案をいただきました。タイミングもよく、翌日には対応いただき大変助かりました。元気のある青年で良かったです。",
              "エアコンのカバーも綺麗にやっていただき満足しています。"]},
]


def build_index():
    title = "お客様の声｜株式会社パーソンライト"
    desc = "業務用エアコンの設置・更新工事をご利用いただいたお客様からいただいたお声を掲載しています。福島県郡山市の株式会社パーソンライト。"
    cards = "\n".join(f"""      <article class="card rise">
        <a class="card__fig" href="./{v['id']}/"><img src="../assets/img/{v['img']}" alt="{v['alt']}" width="1200" height="900" loading="lazy"></a>
        <div class="card__body">
          <p class="voice__mark" aria-hidden="true">“</p>
          <h2 class="card__t">{v['title']}</h2>
          <p class="card__d">{v['body'][0]}</p>
          <p class="voice__who"><b>{v['who']}</b></p>
          <p class="card__more"><a class="tlink" href="./{v['id']}/">この声を読む</a></p>
        </div>
      </article>""" for v in VOICES)

    return head(title, desc, "reviews", 1, extra=jsonld(1)) + header("reviews", 1) + f"""
<main id="main">
""" + phero("Customer Reviews", "お客様の声", INTRO, "case-install01.jpg",
            "天井カセット形エアコンの入れ替え工事の様子", [("お客様の声", "")], 1) + f"""

<section class="sec">
  <div class="wrap">
    <div class="grid grid--2">
{cards}
    </div>
  </div>
</section>

</main>
""" + cta(1, "case-shop.jpg") + footer(1)


def build_one(v):
    i = [x["id"] for x in VOICES].index(v["id"])
    prev = VOICES[i - 1] if i > 0 else None
    nxt = VOICES[i + 1] if i < len(VOICES) - 1 else None
    title = f"{v['title']}｜お客様の声｜株式会社パーソンライト"
    desc = v["body"][0][:110]
    body = "\n".join(f"<p>{b}</p>" for b in v["body"])
    nav = []
    if prev:
        nav.append(f'<a class="pn__p" href="../{prev["id"]}/"><span class="en">PREV</span><span>{prev["title"]}</span></a>')
    if nxt:
        nav.append(f'<a class="pn__n" href="../{nxt["id"]}/"><span class="en">NEXT</span><span>{nxt["title"]}</span></a>')

    return head(title, desc, "reviews", 2, og=v["img"], extra=jsonld(2)) + header("reviews", 2) + f"""
<main id="main">
""" + phero("Customer Reviews", "お客様の声", None, v["img"], v["alt"],
            [("お客様の声", "reviews/"), (v["title"], "")], 2) + f"""

<section class="sec--tight" style="padding-bottom:var(--sec)">
  <div class="narrow">
    <article class="one rise">
      <p class="voice__mark" aria-hidden="true">“</p>
      <h2 class="one__t">{v['title']}</h2>
      <p class="one__who">{v['who']}</p>
      <figure class="one__fig">
        <img src="../../assets/img/{v['img']}" alt="{v['alt']}" width="1200" height="900" loading="lazy">
      </figure>
      <div class="one__b">
{body}
      </div>
    </article>
    <nav class="pn rise" aria-label="ほかのお客様の声">
      {''.join(nav)}
    </nav>
    <p style="margin-top:44px;text-align:center"><a class="btn" href="../">お客様の声の一覧へ</a></p>
  </div>
</section>

</main>
""" + cta(2, "work-outdoor.jpg") + footer(2)
