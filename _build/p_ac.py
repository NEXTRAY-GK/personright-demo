# -*- coding: utf-8 -*-
"""業務用エアコン /ac/"""
from common import head, header, phero, cta, footer, jsonld, TEL, TEL_RAW

TITLE = "業務用エアコン｜株式会社パーソンライト"
DESC = "オフィス・飲食店・工場の業務用エアコンならリースがおすすめ。初期費用0円で導入でき、最新の省エネ機種なら消費電力を最大70%削減。福島県郡山市の株式会社パーソンライト。"

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
    ("再リースがお得", "再リースなら1/10程度の低価格で利用できます。<br><small>※動産保険はつきません。</small>"),
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

# 冷媒別の消費電力（旧サイトのグラフを SVG で描き直した）
GRAPH = """<figure class="graph rise">
  <svg viewBox="0 0 720 300" role="img" aria-labelledby="gT gD">
    <title id="gT">冷媒別の消費電力の比較</title>
    <desc id="gD">2001年以前のR22（指定フロン）を100%としたとき、2001年から2013年のR407・R410（代替フロン）は60%、2014年以降のR32（代替えフロン）は20%。</desc>
    <line x1="46" y1="248" x2="700" y2="248" stroke="rgba(26,105,105,.3)" stroke-width="1"/>
    <g font-family="Jost, sans-serif" font-size="11" fill="#7c8481" text-anchor="end">
      <text x="38" y="56">100</text><text x="38" y="152">50</text><text x="38" y="252">0</text>
    </g>
    <g stroke="rgba(26,105,105,.1)" stroke-width="1">
      <line x1="46" y1="52" x2="700" y2="52"/><line x1="46" y1="148" x2="700" y2="148"/>
    </g>
    <!-- R22 100% -->
    <rect x="96" y="52" width="128" height="196" fill="#1a6969" opacity=".14"/>
    <rect x="96" y="52" width="128" height="196" fill="none" stroke="#1a6969" stroke-width="1"/>
    <text x="160" y="146" text-anchor="middle" font-family="Jost, sans-serif" font-size="27" fill="#0e4444">100<tspan font-size="14">%</tspan></text>
    <text x="160" y="168" text-anchor="middle" font-size="11" fill="#4a5350">消費</text>
    <!-- R407/R410 60% -->
    <rect x="296" y="130" width="128" height="118" fill="#1a6969" opacity=".14"/>
    <rect x="296" y="130" width="128" height="118" fill="none" stroke="#1a6969" stroke-width="1"/>
    <text x="360" y="190" text-anchor="middle" font-family="Jost, sans-serif" font-size="27" fill="#0e4444">60<tspan font-size="14">%</tspan></text>
    <text x="360" y="212" text-anchor="middle" font-size="11" fill="#4a5350">消費</text>
    <text x="360" y="112" text-anchor="middle" font-family="Jost, sans-serif" font-size="17" fill="#ab8f4e">40% 削減</text>
    <!-- R32 20% -->
    <rect x="496" y="209" width="128" height="39" fill="#1a6969" opacity=".14"/>
    <rect x="496" y="209" width="128" height="39" fill="none" stroke="#1a6969" stroke-width="1"/>
    <text x="560" y="238" text-anchor="middle" font-family="Jost, sans-serif" font-size="19" fill="#0e4444">20<tspan font-size="11">%</tspan></text>
    <text x="560" y="191" text-anchor="middle" font-family="Jost, sans-serif" font-size="17" fill="#ab8f4e">80% 削減</text>
    <!-- 削減の線 -->
    <path d="M224 52 L296 130" stroke="#ab8f4e" stroke-width="1" stroke-dasharray="3 3"/>
    <path d="M424 130 L496 209" stroke="#ab8f4e" stroke-width="1" stroke-dasharray="3 3"/>
    <g font-size="11.5" fill="#4a5350" text-anchor="middle">
      <text x="160" y="270">R22（指定フロン）</text><text x="160" y="288">2001年以前</text>
      <text x="360" y="270">R407・R410（代替フロン）</text><text x="360" y="288">2001年〜2013年</text>
      <text x="560" y="270">R32（代替えフロン）</text><text x="560" y="288">2014年以降</text>
    </g>
  </svg>
  <figcaption>冷媒別の消費電力の比較。R22 は入手が難しくなっていくため、早めの更新をおすすめします。</figcaption>
</figure>"""


def build():
    types = "\n".join(f"""      <figure class="tile tile--flat rise">
        <img src="../assets/img/ac-type{n}.jpg" alt="{name}（{d}）" width="720" height="511" loading="lazy">
        <figcaption class="tile__n">{name}</figcaption>
      </figure>""" for n, name, d in TYPES)

    cases = "\n".join(f"""      <figure class="tile rise">
        <img src="../assets/img/ac-case{i+1:02d}.jpg" alt="{c}への業務用エアコン設置例" width="760" height="507" loading="lazy">
        <figcaption class="tile__n">{c}</figcaption>
      </figure>""" for i, c in enumerate(CASES))

    merits = "\n".join(f"""      <li class="rise"><h3 class="merit__t"><i>{i+1:02d}</i>{t}</h3><p class="merit__d">{d}</p></li>"""
                       for i, (t, d) in enumerate(MERITS))

    cautions = "\n".join(f"""      <li><b>{t}</b><p>{d}</p></li>""" for t, d in CAUTIONS)

    flow = "\n".join(f"""      <li class="rise"><h3 class="flow__t">{t}</h3><p class="flow__d">{d}</p></li>""" for t, d in FLOW)

    faq = "\n".join(f"""    <details{' open' if i == 0 else ''}>
      <summary><i>Q</i><span>{q}</span></summary>
      <div class="qa__a"><i>A</i><div>{a}</div></div>
    </details>""" for i, (q, a) in enumerate(FAQ))

    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a.replace("<p>", "").replace("</p>", " ").replace("<br>", " ").replace("<b>", "").replace("</b>", "").strip()}}
                       for q, a in FAQ],
    }

    return head(TITLE, DESC, "ac", 1, extra=jsonld(1, [faq_ld])) + header("ac", 1) + f"""
<main id="main">
""" + phero("Air Conditioner", "業務用エアコン",
            "オフィスや工場、飲食店の業務用エアコンなら、リースで初期費用0円。月々の支払いは全額を経費にできます。",
            "case-house.jpg", "工場の外壁に並べて設置した業務用エアコンの室外機",
            [("業務用エアコン", "")], 1) + f"""

<section class="sec" id="strength">
  <div class="wrap">
    <div class="lead lead--c rise">
      <span class="lead__en">Strength</span>
      <h2 class="lead__ja">当社の業務用エアコン<br>提供サービスの強み</h2>
      <div class="rule"></div>
      <p class="lead__note">様々なニーズに応じてお選びいただけるよう、メーカー・製品ともに種類豊富に業務用エアコンを取り扱っています。お客様のご希望にあったエアコン選びと、当社の充実・安心サービスで、快適な省エネ空間をご提供いたします。</p>
    </div>
    <figure class="makers rise">
      <img src="../assets/img/makers.png" alt="取り扱いメーカー：ダイキン、三菱電機、日立、東芝、パナソニック" width="1200" height="60" loading="lazy">
      <figcaption>取り扱いメーカー</figcaption>
    </figure>
  </div>
</section>

<section class="sec--tight" id="lineup" style="padding-bottom:var(--sec)">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Line Up</span>
      <h2 class="lead__ja">種類豊富なパッケージエアコン</h2>
      <div class="rule"></div>
      <p class="lead__note">天井カセット形から天井吊形、壁掛形、床置形、厨房用まで。設置する場所と広さ、天井の構造に合わせてお選びします。</p>
    </div>
    <div class="tiles tiles--t">
{types}
    </div>
  </div>
</section>

<section class="band sec" id="eco">
  <div class="band__bg"><img src="../assets/img/case-install01.jpg" alt="" width="1200" height="900" loading="lazy"></div>
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Energy Saving</span>
      <h2 class="lead__ja">今のエアコンを替えるだけで、<br>電気代は下がります</h2>
      <div class="rule"></div>
      <p class="lead__note">2011年3月の東日本大震災以降、電気代の値上がり傾向が進むなかで、業務用エアコンの機能も「環境面」「省エネ面」「機能面」と進化してきました。現在では空調機の省電力化の技術が進み、従来の機種に比べ1/5の電気代を削減できるほどになっています。</p>
    </div>
    <div class="figs rise">
      <div class="figs__i">
        <span class="figs__l">省エネ最新エアコンに交換すると</span>
        <p class="figs__v num"><span class="tick" style="--to:70"><i>70</i></span><small>%</small></p>
        <span class="figs__d">消費電力を最大で削減</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">15年前の機種より</span>
        <p class="figs__v num"><span class="tick" style="--to:65"><i>65</i></span><small>%</small></p>
        <span class="figs__d">消費電力を削減</span>
      </div>
      <div class="figs__i">
        <span class="figs__l">18年前の機種より</span>
        <p class="figs__v num"><span class="tick" style="--to:80"><i>80</i></span><small>%</small></p>
        <span class="figs__d">消費電力を削減</span>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="refrigerant">
  <div class="narrow">
    <div class="lead lead--c rise">
      <span class="lead__en">Refrigerant</span>
      <h2 class="lead__ja">R22冷媒が入手困難になる前に</h2>
      <div class="rule"></div>
      <p class="lead__note">2001年以前の機種に使われている R22（指定フロン）は、生産・輸入が終了しています。故障しても修理用のガスが手に入らなくなる前に、早めの更新をおすすめします。</p>
    </div>
{GRAPH}
  </div>
</section>

<section class="sec" id="case" style="background:var(--paper-2)">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Case</span>
      <h2 class="lead__ja">実績多数。<br>様々なケースに最適なご提案を</h2>
      <div class="rule"></div>
      <p class="lead__note">業務用エアコン・空調設備は利用場所により適した形があり、業態に合わせた商品をご提案させていただきます。</p>
    </div>
    <div class="tiles tiles--c">
{cases}
    </div>
  </div>
</section>

<section class="sec" id="lease">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Lease</span>
      <h2 class="lead__ja">リースには、<br>メリットがいっぱい</h2>
      <div class="rule"></div>
      <p class="lead__note">まとまった資金を用意せずに、最新の省エネ機種を導入できます。月々の支払いは全額を経費として処理できます。</p>
    </div>
    <ul class="merit">
{merits}
    </ul>
    <div class="caution rise" style="margin-top:clamp(34px,4vw,54px)">
      <h3 class="caution__t">ご契約の前に、ここだけはご確認ください</h3>
      <ul>
{cautions}
      </ul>
    </div>
  </div>
</section>

<section class="sec--tight" id="flow" style="padding-bottom:var(--sec)">
  <div class="wrap">
    <div class="lead rise">
      <span class="lead__en">Flow</span>
      <h2 class="lead__ja">ご依頼から設置工事までの流れ</h2>
      <div class="rule"></div>
      <p class="lead__note">当社スタッフがお見積りから工事完了まで一貫して対応します。リース審査・本契約につきましては、弊社とリース会社とで丁寧にサポートいたしますので、安心してご利用ください。</p>
    </div>
    <ol class="flow flow--5">
{flow}
    </ol>
  </div>
</section>

<section class="sec" id="faq" style="background:var(--paper-2)">
  <div class="narrow">
    <div class="lead lead--c rise">
      <span class="lead__en">Q &amp; A</span>
      <h2 class="lead__ja">よくあるご質問</h2>
      <div class="rule"></div>
    </div>
    <div class="qa">
{faq}
    </div>
  </div>
</section>

</main>
""" + cta(1, "work-outdoor.jpg") + footer(1)
