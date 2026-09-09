# -*- coding: utf-8 -*-
"""トップページ

   組み立ての考え：
     空調は、目に見えない空気を設計する仕事。
     だから冒頭は写真ではなく「温度の分布」から入り、
     そこから 4つの事業 → 数字 → 仕組みの断面 → 現場の写真 → 声 と降りる。
   事実はすべて現行サイト（personright.com）から引き継いだもの。足していない。
"""
from common import head, header, cta, footer, jsonld, TEL, TEL_RAW, INSTA

TITLE = "株式会社パーソンライト｜業務用エアコン・環境商材・通信機器（福島県郡山市）"
DESC = "郡山市を拠点に、業務用エアコンの販売・設置工事、LED照明、防犯カメラ、複合機の導入までを一貫して承ります。見積りは無料。株式会社パーソンライト。"

# 温度の目盛りの上に、4つの事業を置く（冷 → 温）
SCALE = [
    ("01", "環境事業", "空調・冷熱・照明"),
    ("02", "通信事業", "電話・複合機・防犯"),
    ("03", "工事部", "電気・水回り・各種"),
    ("04", "テレマーケティング事業", "県内へのご案内"),
]

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

# 断面図に添える説明（図と一対）
ROOM = [
    ("01", "室内機", "天井に埋め込む「天井カセット形」が主流です。四方向から吹き出すので、部屋の隅まで温度のむらが出にくくなります。"),
    ("02", "冷媒配管", "天井裏を通して、外の室外機へつなぎます。露出させないぶん、天井裏での取り回しが仕上がりを分けます。"),
    ("03", "室外機", "室内から集めた熱を、外へ捨てます。据付の向きと風の抜けで、効きと電気代が変わります。"),
    ("04", "ドレン", "冷房中に出る水を、外へ流します。勾配が甘いと、天井に染みが出ます。"),
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


def room_svg():
    """室内機から室外機までの断面。写真では撮れないので自分で描く。
       冷たい空気は青緑、暖かい空気は銅色。色がそのまま温度を指す。"""
    return """<svg viewBox="0 0 660 420" role="img" aria-labelledby="roomT roomD" fill="none">
  <title id="roomT">業務用エアコンの断面図</title>
  <desc id="roomD">天井カセット形の室内機から冷たい空気が四方に降り、室内で暖まった空気が中央を上がって室内機へ戻る。熱は天井裏の冷媒配管を通って屋外の室外機から捨てられる。</desc>

  <!-- 建物 -->
  <g stroke="#3f5354" stroke-width="1">
    <path d="M40 44 H470 V376 H40 Z"/>
    <path d="M40 92 H470" stroke-dasharray="3 4" opacity=".75"/>
    <path d="M40 376 H620"/>
    <path d="M470 44 V376"/>
  </g>
  <text x="52" y="72" fill="#6f7d7d" font-size="10.5" letter-spacing="2.4">天井裏</text>
  <text x="486" y="72" fill="#6f7d7d" font-size="10.5" letter-spacing="2.4">屋外</text>

  <!-- 室内機（天井カセット形） -->
  <g stroke="#d9975f" stroke-width="1.4">
    <path d="M212 92 H298 V116 H212 Z"/>
    <path d="M226 116 V124 M255 116 V126 M284 116 V124"/>
  </g>
  <circle cx="255" cy="104" r="2.2" fill="#d9975f"/>

  <!-- 冷たい空気：室内機から四方へ降りる -->
  <g stroke="#79b1ae" stroke-width="1.2" stroke-linecap="round">
    <path d="M212 118 C170 138 140 190 136 262" opacity=".9"/>
    <path d="M212 118 C182 148 162 200 160 268" opacity=".55"/>
    <path d="M298 118 C340 138 370 190 374 262" opacity=".9"/>
    <path d="M298 118 C328 148 348 200 350 268" opacity=".55"/>
  </g>
  <g fill="#79b1ae">
    <path d="M136 268 l4.6 -9 h-9.2 Z"/>
    <path d="M374 268 l4.6 -9 h-9.2 Z"/>
  </g>

  <!-- 暖かい空気：中央を上がって戻る -->
  <g stroke="#d9975f" stroke-width="1.2" stroke-linecap="round">
    <path d="M232 330 C238 268 244 200 248 130" opacity=".85"/>
    <path d="M278 330 C274 268 268 200 262 130" opacity=".85"/>
    <path d="M255 336 C255 300 255 280 255 258" opacity=".4"/>
  </g>
  <g fill="#d9975f">
    <path d="M248 130 l-4.6 9 h9.2 Z" transform="rotate(180 248 134)"/>
    <path d="M262 130 l-4.6 9 h9.2 Z" transform="rotate(180 262 134)"/>
  </g>

  <!-- 人がいる高さ -->
  <g stroke="#3f5354" stroke-width="1" stroke-dasharray="2 5">
    <path d="M60 300 H450"/>
  </g>
  <text x="60" y="292" fill="#6f7d7d" font-size="10" letter-spacing="2">人のいる高さ</text>

  <!-- 冷媒配管：天井裏 → 壁 → 室外機 -->
  <g stroke="#79b1ae" stroke-width="1.6">
    <path d="M298 100 H438 C452 100 458 106 458 120 V244"/>
  </g>
  <g stroke="#d9975f" stroke-width="1.6">
    <path d="M458 244 H520"/>
  </g>

  <!-- ドレン -->
  <g stroke="#5f8f8f" stroke-width="1.1" stroke-dasharray="4 3">
    <path d="M212 104 H120 C108 104 104 110 104 122 V352 H470"/>
  </g>

  <!-- 室外機 -->
  <g stroke="#d9975f" stroke-width="1.4">
    <path d="M520 224 H612 V320 H520 Z"/>
    <path d="M520 300 H612"/>
  </g>
  <g stroke="#d9975f" stroke-width="1.1" opacity=".9">
    <circle cx="566" cy="262" r="24"/>
    <path d="M566 238 A24 24 0 0 1 585 274"/>
    <path d="M566 286 A24 24 0 0 1 547 250"/>
  </g>
  <!-- 捨てられる熱 -->
  <g stroke="#d9975f" stroke-width="1.1" stroke-linecap="round" opacity=".7">
    <path d="M622 250 C636 246 640 240 636 232"/>
    <path d="M622 266 C640 262 646 254 640 244"/>
  </g>

  <!-- 番号 -->
  <g font-size="10.5" letter-spacing="1.6" fill="#d9975f" font-family="Jost, sans-serif">
    <text x="304" y="88">01</text>
    <text x="400" y="116">02</text>
    <text x="524" y="216">03</text>
    <text x="110" y="366">04</text>
  </g>
</svg>"""


def build():
    scale = "\n".join(f"""      <div class="scale__i">
        <span class="scale__n">{n}</span>
        <p class="scale__t">{ja}</p>
        <p class="scale__d">{d}</p>
      </div>""" for n, ja, d in SCALE)

    biz = "\n".join(f"""      <div class="biz__i rise">
        <span class="biz__n">{n}</span>
        <h3 class="biz__t">{ja}<small>{en}</small></h3>
        <div>
          <ul class="biz__l">{''.join(f'<li>{x}</li>' for x in items)}</ul>
          <p class="biz__d">{d}</p>
        </div>
      </div>""" for n, ja, en, items, d in BIZ)

    steps = "\n".join(f"""        <div class="room__s">
          <b>{n}</b>
          <p><i>{t}</i>{d}</p>
        </div>""" for n, t, d in ROOM)

    works = "\n".join(f"""        <figure class="tile rise">
          <img src="./assets/img/{f}" alt="{a}" width="760" height="507" loading="lazy">
          <figcaption class="tile__n">{c}</figcaption>
        </figure>""" for f, a, c in WORKS)

    voice = "\n".join(f"""        <article class="voice rise">
          <p class="voice__mark" aria-hidden="true">“</p>
          <h3 class="voice__t">{t}</h3>
          <p class="voice__d">{d}</p>
          <p class="voice__who"><b>{who}</b></p>
          <p class="card__more"><a class="tlink" href="./reviews/{i}/">この声を読む</a></p>
        </article>""" for t, who, i, d in VOICE)

    ticks = "".join(f'<i style="--i:{k}"></i>' for k in range(13))

    return head(TITLE, DESC, "", 0, extra=jsonld(0, [{
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "株式会社パーソンライト", "url": "https://nextrayjp.github.io/personright-demo/",
    }])) + header("", 0) + f"""
<main id="main">

<!-- ============================================================ 静 -->
<section class="still">
  <canvas class="still__field" id="air" aria-hidden="true"></canvas>
  <div class="still__vig" aria-hidden="true"></div>
  <div class="wrap still__in">
    <span class="still__lab">Service &amp; Contribution — Koriyama, Fukushima</span>
    <h1 class="still__h">
      <i>空気は、目に見えない。</i>
      <i>だから、最後まで見る。</i>
    </h1>
    <p class="still__sub">業務用エアコンから通信機器まで。福島県郡山市を拠点に、選ぶところから工事、その後の保守までを自社で受け持ちます。笑顔や喜びにあふれた顧客作りを目指して。</p>
    <div class="still__acts">
      <a class="btn btn--onDark" href="./ac/">業務用エアコンを見る</a>
      <a class="btn btn--onDark" href="./contact/">無料で見積りを頼む</a>
    </div>
  </div>
  <span class="still__scroll" aria-hidden="true">SCROLL</span>
  <div class="still__scale" aria-hidden="true">{ticks}</div>
</section>

<!-- ==================================================== 温度帯（事業） -->
<section class="scale" aria-label="事業の一覧">
  <div class="scale__bar" aria-hidden="true"></div>
  <div class="wrap">
    <div class="scale__row">
{scale}
    </div>
  </div>
</section>

<!-- ======================================================== 事業案内 -->
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

<!-- ==================================================== 空調（数字） -->
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
        <p class="figs__v num"><span class="tick" style="--to:70"><i>70</i></span><small>%</small></p>
        <span class="figs__d">消費電力を最大で削減できます</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">取り扱いメーカー</span>
        <p class="figs__v num"><span class="tick" style="--to:5"><i>5</i></span><small>社</small></p>
        <span class="figs__d">ダイキン・三菱電機・日立<br>東芝・パナソニック</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">業務用エアコン</span>
        <p class="figs__v num"><span class="tick" style="--to:7"><i>7</i></span><small>年</small></p>
        <span class="figs__d">保証サービス。<br>年間メンテナンスも承ります</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">初期費用</span>
        <p class="figs__v num"><span class="tick" style="--to:0"><i>0</i></span><small>円</small></p>
        <span class="figs__d">リースなら、まとまった資金を<br>用意せずに導入できます</span>
      </div>
    </div>
    <p style="margin-top:clamp(38px,4.6vw,60px)"><a class="btn btn--onDark" href="./ac/">業務用エアコンのご案内</a></p>
  </div>
</section>

<!-- ============================================ 仕組み（断面図） -->
<section class="sec dark" id="how" style="background:var(--sumi-2)">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">How it works</span>
      <h2 class="lead__ja">一台のエアコンが、<br>部屋の空気を変えるまで</h2>
      <div class="rule"></div>
      <p class="lead__note">写真には写らないところに、仕事の差が出ます。冷たい空気は下へ、暖まった空気は上へ。その循環を邪魔しない位置に室内機を置き、天井裏の配管とドレンの勾配を取る。そこまでが工事です。</p>
    </div>
    <div class="room rise">
      <figure class="room__fig">
        {room_svg()}
        <figcaption class="room__cap">断面図 ── 天井カセット形の場合</figcaption>
      </figure>
      <div class="room__steps">
{steps}
      </div>
    </div>
  </div>
</section>

<!-- ======================================================== 施工実例 -->
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
    <p style="margin-top:clamp(32px,4vw,52px)"><a class="tlink" href="{INSTA}" target="_blank" rel="noopener">Instagram（@personright501）で施工実例を見る</a></p>
  </div>
</section>

<!-- ======================================================== お客様の声 -->
<section class="sec dark" id="voice">
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
    <p style="margin-top:clamp(32px,4vw,52px)"><a class="btn btn--onDark" href="./reviews/">お客様の声の一覧</a></p>
  </div>
</section>

<!-- ========================================================== 採用 -->
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
        <p style="margin-top:30px"><a class="btn" href="./recruit/">採用情報を見る</a></p>
      </div>
    </div>
  </div>
</section>

</main>
""" + cta(0) + footer(0)
