# -*- coding: utf-8 -*-
"""業務用エアコン /ac/（2026-09-16 第3版）

   並びを「替える理由 → 選ぶ → 払う → 流れ → 質問」にした。
   読む人が決める順番に合わせてある。事実は会社の情報のまま。
   リースの注意点と Q&A の答えは契約にかかわるので、言い回しも変えていない。
"""
from common import head, header, phero, footer, jsonld, sh, TEL, TEL_RAW

TITLE = "業務用エアコンの販売・設置工事とリース｜株式会社パーソンライト"
DESC = "業務用エアコンを5メーカー・12の形から選び、自社の工事部が設置。リースなら初期費用0円。最新の省エネ機種なら消費電力を最大70%削減。福島県郡山市の株式会社パーソンライト。"

TYPES = [
    ("01", "S-ラウンドフロー", "天井カセット形（4方向）"),
    ("02", "スタイリッシュフロー", "天井カセット形（4方向）"),
    ("03", "エコ・ダブルフロー", "天井カセット形（2方向）"),
    ("04", "ワンダ風流", "天井カセット形（4方向）"),
    ("05", "シングルフロー", "天井カセット形（1方向）"),
    ("06", "天井吊形", "天井に吊り下げて設置"),
    ("07", "壁掛形", "壁に掛けて設置"),
    ("08", "ビルトインHiタイプ", "天井に埋め込んで設置"),
    ("09", "天井埋込ダクト形", "ダクトで送風"),
    ("10", "マルチフロータイプ", "天井カセット形"),
    ("11", "床置形", "床に据え置いて設置"),
    ("12", "厨房用エアコン", "厨房の熱と油に対応"),
]

CASES = ["事務所", "飲食店", "店舗", "工場", "理美容室", "倉庫", "病院", "学校", "宿泊施設", "住宅"]

MERITS = [
    ("初期費用がかからない", "買うときのような、まとまった資金を用意しなくて済みます。"),
    ("借入枠を使わない", "リースは、銀行から借りられる枠を減らしません。"),
    ("経費にできる", "税務上認められたリース期間なら、支払いを全額経費にできます。"),
    ("事務の手間が少ない", "面倒な事務の手続きは、リース会社が引き受けます。"),
    ("動産総合保険つき", "思わぬ事故で損害が出たときも補償されます。"),
    ("無料修理つきのプランも", "修理が無料になるプランもあります。"),
    ("電気代が下がる", "15年前の機種から替えると、消費電力が65%下がります。"),
    ("再リースは安い", "期間が終わったあとの再リースは、10分の1ほどの料金で使えます。<small>※動産保険はつきません。</small>"),
]

CAUTIONS = [
    ("途中でやめることはできません",
     "リース期間中の解約は、原則としてできません。お客様のご都合でどうしても解約したい場合は、途中解約金や、契約したリース金額をお支払いいただくことで、解約に応じることもあります。"),
    ("エアコンの持ち主はリース会社です",
     "エアコンの所有権はリース会社にあるので、契約が終わったら返していただく必要があります。続けて使いたいときは、年間リース額の10分の1で再契約することもできます。契約の内容によっては、買い取ることもできます。"),
    ("支払いの合計は、一括で買うより高くなります",
     "リースでは、販売価格に加えて料率がかかります。そのぶん、支払いの合計は一括で買うより高くなります。"),
]

FLOW = [
    ("見積りのご依頼", "お電話かフォームで、気軽にご連絡ください。お見積りは無料です。"),
    ("現地を見てお見積り", "スタッフがうかがって取り付ける場所を実際に見てから、機種と工事のやり方を決めます。"),
    ("リースの審査の申し込み", "必要な書類は当社で用意して、リース会社へ出すところまで行います。"),
    ("リースのご契約", "内容を確かめていただいてから、ご契約になります。"),
    ("取り付け工事", "自社の工事部が取り付けます。引き渡しのあとは、7年保証と年間メンテナンスが始まります。"),
]

FAQ = [
    ("途中で解約できますか？",
     "<p>リースや延払いの契約期間中は、途中で解約できません。お客様のご都合でどうしても解約することになった場合は、お客様の費用でエアコンをリース会社へ返したうえで、残っているリース料・割賦金の全額を、損害金としてすぐに現金でリース会社へお支払いいただくことになります。（動産保険が使える場合は、この限りではありません。）</p>"),
    ("リースの期間が終わったら、どうなりますか？",
     "<p><b>そのまま使い続ける（再リース）</b><br>ご希望があれば再リース契約を結んで、同じエアコンを使い続けられます。再リース料は月額リース料の2倍＋消費税で、1年ごとの契約です。（「安心保証リース」で契約したエアコンを再リースする場合、安心保証はつきません。）</p><p><b>新しい機種に替える（レベルアップ更新）</b><br>期間が終わるときに新しい機種へ入れ替えて、改めてリース契約を結ぶこともできます。それまでとあまり変わらないリース料で、最新の高性能なエアコンが使えます。</p><p>このほか、買い取りや撤去もできます。（注）撤去の費用と、リース会社へ返すための費用は、お客様のご負担になります。</p>"),
    ("故障したときの修理は、保証されますか？",
     "<p>買った場合と同じように、メーカー保証の範囲で修理を受けられます。「安心保証リース」でご契約いただくと、リース期間中は突然の故障の修理費がかかりません。</p>"),
    ("動産保険とは、どんな保険ですか？",
     "<p>リースや延払いで入れたエアコンには、動産総合保険がついています。火事、水害、雪害、落雷、爆発、車がぶつかる事故、盗難など、思いがけない事故による損害を補償する保険です。</p>"),
    ("現金での購入や、クレジットの分割払いもできますか？",
     "<p>はい、できます。お支払いの方法はいくつかご用意していますので、気軽にお尋ねください。</p>"),
]

GEN = [
    ("R22", "指定フロン", "2001年以前", 100),
    ("R407・R410", "代替フロン", "2001年〜2013年", 60),
    ("R32", "代替えフロン", "2014年以降", 20),
]


def build():
    types = "\n".join(f"""      <figure class="ty rise">
        <img src="../assets/img/ac-type{n}.jpg" alt="{name}（{d}）" width="720" height="511" loading="lazy">
        <figcaption><span class="mono">{n}</span><b>{name}</b><small>{d}</small></figcaption>
      </figure>""" for n, name, d in TYPES)

    cases = "\n".join(f"""      <li class="rise"><img src="../assets/img/ac-case{i+1:02d}.jpg" alt="{c}への業務用エアコン設置例" width="352" height="352" loading="lazy"><span>{c}</span></li>"""
                      for i, c in enumerate(CASES))

    merits = "\n".join(f"""      <li class="rise"><span class="mono">{i+1:02d}</span><b>{t}</b><p>{d}</p></li>"""
                       for i, (t, d) in enumerate(MERITS))

    cautions = "\n".join(f"""      <li><b>{t}</b><p>{d}</p></li>""" for t, d in CAUTIONS)

    flow = "\n".join(f"""      <li class="rise"><span class="mono">{i+1}</span><b>{t}</b><p>{d}</p></li>""" for i, (t, d) in enumerate(FLOW))

    faq = "\n".join(f"""    <details{' open' if i == 0 else ''}>
      <summary><span class="mono">Q{i+1}</span>{q}</summary>
      <div class="qa__a">{a}</div>
    </details>""" for i, (q, a) in enumerate(FAQ))

    gen = "\n".join(f"""        <li style="--w:{w}"><span class="mono">{r}</span><small>{k}・{y}</small><i><em></em></i><b class="mono">{w}%</b></li>"""
                    for r, k, y, w in GEN)

    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a.replace("<p>", "").replace("</p>", " ").replace("<br>", " ").replace("<b>", "").replace("</b>", "").strip()}}
                       for q, a in FAQ],
    }

    return head(TITLE, DESC, "ac", 1, extra=jsonld(1, [faq_ld])) + header("ac", 1) + f"""
<main id="main">
""" + phero("01", "AIR CONDITIONER", "業務用エアコン",
            "機種を選ぶところから、支払い方、取り付け、付けたあとのことまで、まとめてお任せください。5社のメーカー・12種類から選べて、リースなら初期費用はかかりません。工事は自社の工事部が行い、7年保証と年間メンテナンスもご用意しています。",
            "case-shop.jpg", "店舗の天井に設置した天井カセット形エアコン",
            [("業務用エアコン", "")], 1, 780, 611) + f"""
<nav class="toc" aria-label="このページの目次">
  <ol class="mono">
    <li><a href="#eco">01 替える理由</a></li>
    <li><a href="#lineup">02 選ぶ</a></li>
    <li><a href="#lease">03 払う</a></li>
    <li><a href="#flow">04 流れ</a></li>
    <li><a href="#faq">05 質問</a></li>
  </ol>
</nav>

<section class="sec" id="eco">
  <div class="wrap">
    {sh("01", "替える理由", "替えどきを決めるのは、<br>電気代とガスです。", "2011年3月の東日本大震災のあと、電気代は上がり続けてきました。そのあいだに業務用エアコンの省エネは大きく進み、いまでは昔の機種の5分の1ほどの電気代で済むものもあります。")}
    <div class="nums">
      <div class="rise"><small>最新の省エネ機種に替えると</small><p><b class="count mono" data-to="70">70</b><span>%</span></p><span>消費電力が最大でこれだけ減ります</span></div>
      <div class="rise"><small>15年前の機種と比べると</small><p><b class="count mono" data-to="65">65</b><span>%</span></p><span>消費電力がこれだけ減ります</span></div>
      <div class="rise"><small>18年前の機種と比べると</small><p><b class="count mono" data-to="80">80</b><span>%</span></p><span>消費電力がこれだけ減ります</span></div>
    </div>
  </div>
</section>

<section class="sec sec--ink" id="refrigerant">
  <div class="wrap duo">
    <div class="rise">
      <p class="sh__no mono"><span>冷媒のこと</span></p>
      <h2 class="big">R22の機種は、<br>ガスがあるうちに<br>入れ替えを。</h2>
      <p class="lede">2001年より前の機種に使われているR22（指定フロン）は、もう生産も輸入もされていません。壊れたときに修理用のガスが手に入らない、ということになる前に、早めの入れ替えをおすすめします。</p>
    </div>
    <figure class="gen rise" aria-labelledby="genC" data-k="enter">
      <ul>
{gen}
      </ul>
      <figcaption id="genC">冷媒ごとの消費電力（R22を100%としたとき）</figcaption>
    </figure>
  </div>
</section>

<section class="sec" id="lineup">
  <div class="wrap">
    {sh("02", "選ぶ", "12種類の中から、<br>部屋に合う一台を選びます。", "天井に埋め込む形、吊るす形、壁掛け、床置き、厨房用まであります。置く場所や広さ、天井のつくりを見てお選びします。")}
    <div class="brand rise">
      <p>取り扱いメーカー</p>
      <img src="../assets/img/makers.png" alt="ダイキン、三菱電機、日立、東芝、パナソニック" width="634" height="29" loading="lazy">
    </div>
    <div class="tys">
{types}
    </div>
  </div>
</section>

<section class="sec sec--p2" id="case">
  <div class="wrap">
    {sh("", "業種", "お店や会社によって、<br>合う形は変わります。", "同じ業務用エアコンでも、使う場所によって向いている形が違います。業種に合わせてご提案します。")}
    <ul class="biz">
{cases}
    </ul>
  </div>
</section>

<section class="sec" id="lease">
  <div class="wrap">
    {sh("03", "払う", "リースなら、<br>初期費用はかかりません。", "まとまった資金を用意しなくても、最新の省エネ機種を入れられます。もちろん、現金での購入やクレジットの分割払いもできます。")}
    <ol class="merits" data-k="through" data-steps>
{merits}
    </ol>
    <div class="caution rise">
      <h3>ご契約の前に、ここは必ず確かめてください</h3>
      <ul>
{cautions}
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--p2" id="flow">
  <div class="wrap">
    {sh("04", "流れ", "ご相談から工事まで、<br>5つの手順です。", "リースの審査や契約の手続きも、当社とリース会社でお手伝いします。")}
    <ol class="flow" data-k="through" data-steps>
{flow}
    </ol>
  </div>
</section>

<section class="sec" id="faq">
  <div class="wrap duo duo--top">
    {sh("05", "質問", "リースについて、<br>よくいただく質問です。", f'ほかにもわからないことがあれば、<a class="mono" href="tel:{TEL_RAW}">{TEL}</a> までお電話ください。')}
    <div class="qa rise">
{faq}
    </div>
  </div>
</section>

</main>
""" + footer(1)
