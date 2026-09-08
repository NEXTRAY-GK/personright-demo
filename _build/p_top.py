# -*- coding: utf-8 -*-
"""トップページ"""
from common import head, header, cta, footer, jsonld, TEL, TEL_RAW, INSTA

TITLE = "株式会社パーソンライト｜業務用エアコン・環境商材・通信機器（福島県郡山市）"
DESC = "郡山市を拠点に、業務用エアコンの販売・設置工事、LED照明、防犯カメラ、複合機の導入までを一貫して承ります。見積りは無料。株式会社パーソンライト。"

BIZ = [
    ("01", "環境事業", "ENVIRONMENT",
     ["業務用エアコン", "家庭用エアコン", "空気清浄機", "LED照明", "分解・洗浄クリーニング",
      "エコキュート", "高機能換気設備", "業務用冷蔵庫・冷凍庫", "各種厨房機器"],
     "業務用エアコンには <b>7年保証サービス</b>と年間メンテナンスサービスをご用意しています。"),
    ("02", "通信事業", "COMMUNICATION",
     ["ビジネスフォン", "複合機", "セキュリティ商材", "PC周辺設備", "防犯カメラ", "UTM", "サーバー"],
     "機器の選定から設置、その後の保守まで一括で承ります。"),
    ("03", "工事部", "CONSTRUCTION",
     ["各種工事", "電気工事", "水回り工事"],
     "自社の工事部が施工します。空調に付随する工事もまとめてお任せください。"),
    ("04", "テレマーケティング事業", "TELEMARKETING",
     ["アポイント"],
     "福島県内の事業所へ、お電話でご案内しています。"),
]

WORKS = [
    ("work-ceiling.jpg", "天井カセット形エアコンを分解して点検する当社の工事スタッフ", "分解・点検"),
    ("case-install01.jpg", "天井カセット形エアコンの入れ替え工事の様子", "入れ替え工事"),
    ("work-outdoor.jpg", "建物の外壁で室外機を据え付ける工事の様子", "室外機の据付"),
    ("work-filter.jpg", "天井カセット形エアコンのフィルターを清掃する様子", "フィルター清掃"),
    ("case-install02.jpg", "設置を終えた天井カセット形エアコン", "設置完了"),
    ("work-attic.jpg", "天井裏で配管と配線を通す作業の様子", "天井裏の配管"),
]

VOICE = [
    ("最適な提案と確かな技術で大満足です。", "田村市　N様", "98",
     "会社のエアコン設置をお願いしました。こちらの要望をしっかりヒアリングしていただき、最適な機種や設置方法を提案してもらえました。コスト面も含めて納得のいく内容で、仕上がりも大満足です。またお願いしたいと思います。"),
    ("業務への影響を最小限に、スムーズな設置でした。", "郡山市　M様", "96",
     "オフィスのエアコンを新しく設置していただきました。作業が迅速かつ丁寧で、業務の妨げにならないよう配慮いただき助かりました。社内が快適になり、社員からも好評です。プロの仕事に感謝しています。"),
]


def build():
    biz = "\n".join(f"""    <div class="biz__i rise">
      <span class="biz__n">{n}</span>
      <h3 class="biz__t">{ja}<small>{en}</small></h3>
      <ul class="biz__l">{''.join(f'<li>{x}</li>' for x in items)}</ul>
      <p class="biz__d">{d}</p>
    </div>""" for n, ja, en, items, d in BIZ)

    works = "\n".join(f"""      <figure class="tile rise">
        <img src="./assets/img/{f}" alt="{a}" width="760" height="507" loading="lazy">
        <figcaption class="tile__n">{c}</figcaption>
      </figure>""" for f, a, c in WORKS)

    voice = "\n".join(f"""      <article class="voice rise">
        <p class="voice__mark" aria-hidden="true">“</p>
        <h3 class="voice__t">{t}</h3>
        <p class="voice__d">{d}</p>
        <p class="voice__who"><b>{who}</b></p>
        <p class="card__more"><a class="tlink" href="./reviews/{i}/">この声を読む</a></p>
      </article>""" for t, who, i, d in VOICE)

    return head(TITLE, DESC, "", 0, extra=jsonld(0, [{
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "株式会社パーソンライト", "url": "https://nextrayjp.github.io/personright-demo/",
    }])) + header("", 0) + f"""
<main id="main">

<section class="hero">
  <div class="hero__bg"><img src="./assets/img/office-front.jpg" alt="福島県郡山市安積町にある株式会社パーソンライトの本社社屋" width="1600" height="1096" fetchpriority="high"></div>
  <div class="hero__veil"></div>
  <canvas class="hero__air" id="air" aria-hidden="true"></canvas>
  <div class="wrap hero__inner">
    <h1 class="hero__en"><i>Service</i><i><span class="amp">&amp;</span> Contribution</i></h1>
    <p class="hero__ja">笑顔や喜びにあふれた<br>顧客作りを目指して</p>
    <p class="hero__sub">業務用エアコンから通信機器まで。福島県郡山市を拠点に、選ぶところから工事、その後の保守までを自社で受け持ちます。</p>
    <div class="hero__acts">
      <a class="btn btn--onDark" href="./ac/">業務用エアコンを見る</a>
      <a class="btn btn--onDark" href="./contact/">無料で見積りを頼む</a>
    </div>
  </div>
  <span class="hero__scroll" aria-hidden="true">SCROLL</span>
</section>

<section class="sec" id="business">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Business Information</span>
      <h2 class="lead__ja">事業案内</h2>
      <div class="rule"></div>
      <p class="lead__note">郡山市を拠点に、業務用エアコンから家庭用エアコン、ビル用マルチエアコン、業務用冷凍機・冷蔵庫、換気扇、全熱交換器、除湿器、暖房機、また通信機器などの販売や各種設置工事を行っております。</p>
    </div>
    <div class="biz">
{biz}
    </div>
  </div>
</section>

<section class="band sec" id="aircon">
  <div class="band__bg"><img src="./assets/img/case-house.jpg" alt="" width="1200" height="801" loading="lazy"></div>
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Air Conditioner</span>
      <h2 class="lead__ja">空調機器の各種販売、設置工事</h2>
      <div class="rule"></div>
      <p class="lead__note">業務用エアコンの入れ替え・取り付け工事はパーソンライトにお任せください。ダイキン・三菱電機・日立・東芝・パナソニックの5メーカーから、お使いの場所に合う一台をお選びします。</p>
    </div>
    <div class="figs rise">
      <div class="figs__i">
        <span class="figs__l">最新の省エネ機種に替えると</span>
        <p class="figs__v num">70<small>%</small></p>
        <span class="figs__d">消費電力を最大で削減できます</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">取り扱いメーカー</span>
        <p class="figs__v num">5<small>社</small></p>
        <span class="figs__d">ダイキン・三菱電機・日立<br>東芝・パナソニック</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">業務用エアコン</span>
        <p class="figs__v num">7<small>年</small></p>
        <span class="figs__d">保証サービス。<br>年間メンテナンスも承ります</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">初期費用</span>
        <p class="figs__v num">0<small>円</small></p>
        <span class="figs__d">リースなら、まとまった資金を<br>用意せずに導入できます</span>
      </div>
    </div>
    <p style="margin-top:44px"><a class="btn btn--onDark" href="./ac/">業務用エアコンのご案内</a></p>
  </div>
</section>

<section class="sec" id="works">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Works</span>
      <h2 class="lead__ja">施工実例</h2>
      <div class="rule"></div>
      <p class="lead__note">事務所・店舗・工場・倉庫。天井カセット形の入れ替えから、外壁の室外機据付、天井裏の配管まで。現場の写真は Instagram でも随時ご紹介しています。</p>
    </div>
    <div class="tiles tiles--w">
{works}
    </div>
    <p style="margin-top:40px"><a class="tlink" href="{INSTA}" target="_blank" rel="noopener">Instagram（@personright501）で施工実例を見る</a></p>
  </div>
</section>

<section class="sec" id="voice" style="background:var(--paper-2)">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Customer Reviews</span>
      <h2 class="lead__ja">お客様の声</h2>
      <div class="rule"></div>
      <p class="lead__note">パーソンライトでは、設備機器の工事を終えた後からが本当のお付き合いの始まりであると考えております。皆様からのご意見をお伺いし、今後のアフターフォローに活かしていきます。</p>
    </div>
    <div class="grid grid--2">
{voice}
    </div>
    <p style="margin-top:40px"><a class="btn" href="./reviews/">お客様の声の一覧</a></p>
  </div>
</section>

<section class="sec" id="recruit">
  <div class="wrap">
    <div class="duo">
      <figure class="duo__fig rise">
        <img src="./assets/img/recruit03.jpg" alt="天井カセット形エアコンを点検する当社の工事スタッフ" width="1000" height="717" loading="lazy">
        <figcaption>RECRUIT</figcaption>
      </figure>
      <div class="rise">
        <div class="lead">
          <span class="lead__en">Recruit</span>
          <h2 class="lead__ja">一緒に働く人を<br>探しています</h2>
          <div class="rule"></div>
        </div>
        <p>自ら行動する意欲や姿勢を持ち、常にチャレンジ精神旺盛な人物を求めています。営業職・工事スタッフ・テレフォンアポインター・管理職責任者の4職種で募集中です。</p>
        <p style="margin-top:26px"><a class="btn" href="./recruit/">採用情報を見る</a></p>
      </div>
    </div>
  </div>
</section>

</main>
""" + cta(0) + footer(0)
