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
    ("初期費用は0円", "購入時にかかる多額の資金を用意する必要はありません。"),
    ("借入枠の節約", "リースは銀行の借入枠を圧迫しません。"),
    ("経費処理OK", "税務上認められたリース期間であれば、全額を経費として処理できます。"),
    ("事務処理が簡単", "面倒な事務処理はリース会社が行いますので安心です。"),
    ("動産総合保険付", "偶然な事故による損害のときにも保証されます。"),
    ("無料修理付き", "無料修理の付いたプランもあります。"),
    ("最新機種は省エネ", "15年前の機種から替えると、消費電力が65%下がります。"),
    ("再リースがお得", "再リースなら1/10程度の低価格で利用できます。<small>※動産保険はつきません。</small>"),
]

CAUTIONS = [
    ("途中解約はできません",
     "原則的にリース期間中の解約は認められません。お客様のご都合により解約の申し出があった場合には、途中解約金や、契約したリース金額をお支払いいただいて解約に応じる場合もあります。"),
    ("契約終了後の所有権はリース会社",
     "エアコンの所有権はリース会社が保有しているので、契約満了時に業務用エアコンを返す必要があります。契約満了後は年間リース額の1/10で再契約を結ぶこともできます。※リース契約によってエアコンの買い取りをすることも可能です。"),
    ("一括購入より割高です",
     "リース契約を行う場合は、販売価格の他に料率が発生いたしますので、一般購入より総額は割高になります。"),
]

FLOW = [
    ("無料見積依頼", "お電話またはフォームからご連絡ください。"),
    ("現地調査・お見積", "当社スタッフが伺い、設置場所を実際に見て機種と工法を決めます。"),
    ("リース審査申込み", "必要書類は当社が用意し、リース会社へ出すところまでやります。"),
    ("リース契約", "内容をご確認のうえ、ご契約いただきます。"),
    ("エアコン設置工事", "当社の工事部が施工します。引き渡しの後は7年保証と年間メンテナンスに移ります。"),
]

FAQ = [
    ("中途解約はできるの？",
     "<p>リース・延払契約期間中での中途解約は認められません。万一、ユーザー様のご都合で中途解約になった場合は、ユーザー様の費用負担で物件をリース会社に返却したうえで、リース・割賦金残高の全額を損害額として即時現金でユーザー様がリース会社に支払わなければなりません。（動産保険適用時は、この限りではありません。）</p>"),
    ("期間満了後はどうなる？",
     "<p><b>◎再リース</b><br>リース期間満了後は、希望すれば再リース契約を結ぶことで、物件を引き続き使用できます。再リース料は月額リース料に2を乗じた額＋消費税で、再リース契約は1年ごとの年間契約となります。（「安心保証リース」契約物件の再リースには、安心保証はつきません。）</p><p><b>◎レベルアップ更新</b><br>リース満了時に新製品に入替えて新たにリース契約を結べば、それまでと大差ないリース料で、最新高性能エアコンがご利用いただけます。</p><p>「買い取り」「撤去」することもできます。（注）リース契約物件の撤去費用およびリース会社への返還費用はユーザー様のご負担となります。</p>"),
    ("修理保証はどうなる？",
     "<p>購入した場合と同じように、メーカー保証範囲内での修理保証が受けられます。なお「安心保証リース」でご契約いただければ、リース期間内は突発的な故障による修理費が無償となります。</p>"),
    ("動産保険って何？",
     "<p>リース・延払物件には、火災・水害・雪害・落雷・爆発、車両の衝突や接触事故、盗難など偶発的な事故による損害を補償するために動産総合保険が付与されています。</p>"),
    ("現金購入や、クレジット分割払いは出来るの？",
     "<p>はい、大丈夫です。複数のお支払方法をご準備しております。お気軽にお問い合わせください。</p>"),
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

    flow = "\n".join(f"""      <li class="rise"><span class="mono">STEP {i+1}</span><b>{t}</b><p>{d}</p></li>""" for i, (t, d) in enumerate(FLOW))

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
            "選ぶ、払う、取り付ける、見続ける。5メーカー・12の形から選び、リースなら初期費用0円。工事は自社の工事部、引き渡しのあとは7年保証と年間メンテナンスです。",
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
    {sh("01", "替える理由", "替える理由は、<br>電気代とガスの2つ。", "2011年3月の東日本大震災のあと、電気代の値上がりが続くなかで、業務用エアコンの省電力化は大きく進みました。いまの機種は、従来の機種に比べて電気代を1/5まで削減できるほどです。")}
    <div class="nums">
      <div class="rise"><small>省エネ最新エアコンに交換すると</small><p><b class="count mono" data-to="70">70</b><span>%</span></p><span>消費電力を最大で削減</span></div>
      <div class="rise"><small>15年前の機種より</small><p><b class="count mono" data-to="65">65</b><span>%</span></p><span>消費電力を削減</span></div>
      <div class="rise"><small>18年前の機種より</small><p><b class="count mono" data-to="80">80</b><span>%</span></p><span>消費電力を削減</span></div>
    </div>
  </div>
</section>

<section class="sec sec--ink" id="refrigerant">
  <div class="wrap duo">
    <div class="rise">
      <p class="sh__no mono"><b>01-b</b><span>冷媒</span></p>
      <h2 class="big">R22 の機種は、<br>ガスが手に入るうちに。</h2>
      <p class="lede">2001年以前の機種に使われている R22（指定フロン）は、生産・輸入が終了しています。故障しても修理用のガスが手に入らなくなる前に、早めの更新をおすすめします。</p>
    </div>
    <figure class="gen rise" aria-labelledby="genC">
      <ul>
{gen}
      </ul>
      <figcaption id="genC">冷媒別の消費電力の比較（R22＝100%）</figcaption>
    </figure>
  </div>
</section>

<section class="sec" id="lineup">
  <div class="wrap">
    {sh("02", "選ぶ", "12の形から、<br>部屋に合う一台を。", "天井カセット形から天井吊形、壁掛形、床置形、厨房用まで。設置する場所と広さ、天井の構造に合わせてお選びします。")}
    <div class="brand rise">
      <p class="mono">取り扱いメーカー</p>
      <img src="../assets/img/makers.png" alt="ダイキン、三菱電機、日立、東芝、パナソニック" width="634" height="29" loading="lazy">
    </div>
    <div class="tys">
{types}
    </div>
  </div>
</section>

<section class="sec sec--p2" id="case">
  <div class="wrap">
    {sh("02-b", "業態", "業態ごとに、<br>合う形がある。", "業務用エアコン・空調設備は、使う場所によって適した形が違います。業態に合わせてご提案します。")}
    <ul class="biz">
{cases}
    </ul>
  </div>
</section>

<section class="sec" id="lease">
  <div class="wrap">
    {sh("03", "払う", "リースなら、<br>初期費用は0円。", "まとまった資金を用意せずに、最新の省エネ機種を入れられます。現金購入やクレジットの分割払いもできます。")}
    <ol class="merits">
{merits}
    </ol>
    <div class="caution rise">
      <h3>ご契約の前に、ここだけはご確認ください</h3>
      <ul>
{cautions}
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--p2" id="flow">
  <div class="wrap">
    {sh("04", "流れ", "ご相談から工事まで、<br>5つの段。", "リース審査・本契約は、当社とリース会社とでお手伝いします。")}
    <ol class="flow">
{flow}
    </ol>
  </div>
</section>

<section class="sec" id="faq">
  <div class="wrap duo duo--top">
    {sh("05", "質問", "リースについて、<br>よく聞かれること。", f'ほかに分からないことがあれば、<a class="mono" href="tel:{TEL_RAW}">{TEL}</a> へ。')}
    <div class="qa rise">
{faq}
    </div>
  </div>
</section>

</main>
""" + footer(1)
