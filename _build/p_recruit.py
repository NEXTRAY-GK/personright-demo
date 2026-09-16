# -*- coding: utf-8 -*-
"""採用情報 /recruit/ と求人4本（2026-09-16 第3版）"""
from common import head, header, phero, footer, jsonld, sh, TEL, TEL_RAW

COMMON_OTHER_NEW = "2022年12月に法人化した会社です。営業も工事も、これから形を作る人を探しています。"
COMMON_OTHER_R4 = "令和4年12月に法人化した会社です。営業も工事も、これから形を作る人を探しています。"

SALES_WORK = """<p>空調設備機器、LED照明等の環境商材の販売を行っていただきます。</p>
<ul class="dots">
<li>当社は、福島県内の中小企業様向けをメインとしてご提案営業を行っております。</li>
<li>基礎知識の研修制度や先輩社員と共に同行営業をして、自分に合ったペースで取り組むことが可能です。</li>
<li>自分に合ったやりがいを探すお仕事です。</li>
</ul>"""

JOBS = [
    {
        "id": "49", "name": "エアコン設備工事スタッフ", "img": "recruit03.jpg",
        "alt": "天井のエアコンを点検する工事スタッフ",
        "summary": "業務用・一般家庭のエアコン取付工事",
        "type": "正社員", "pay": "月給：220,000〜450,000円",
        "work": """<p>経験者優遇で、道具や材料のノウハウに優れている方を募集します。1人親方として最前線で働けるスタッフとし、子方共々2人1組で行う形が基本となります。</p>
<p>事務所に出勤し、当日の現地へ向かっていただきます。場合によっては、現場からの直行直帰は可能となります。自車両も可能で、特段の報告業務などもありません。自分のスケジュールで仕事ができる環境で働けます。</p>""",
        "req": "一通りの施工業務が行える知識・技術が必須となります。",
        "hours": "8:00〜18:00（休憩2時間）　※現場によって就業時間が多少変動することがあります。",
        "welfare": "賞与有、退職金制度有、交通費支給（上限：月額3,000円）",
        "holiday": "週休2日制（土・日・祝、会社カレンダーによる）、年間休日120日",
        "other": COMMON_OTHER_NEW,
    },
    {
        "id": "46", "name": "営業職", "img": "recruit01.jpg",
        "alt": "お客様と商談する営業社員",
        "summary": "空調設備機器、LED照明等の環境商材の販売を行っていただきます。",
        "type": "正社員", "pay": "月給：220,000〜650,000円",
        "work": SALES_WORK,
        "req": "エクセル・ワードの入力程度",
        "hours": "9:00〜18:00（休憩1時間）、又は10:00〜19:00の間の8時間程度",
        "welfare": "賞与有、退職金制度有、交通費支給（上限：月額5,000円）",
        "holiday": "土・日・祝日（完全週休2日制）、年間休日120日、年末年始・夏季休暇有",
        "other": COMMON_OTHER_NEW,
    },
    {
        "id": "48", "name": "テレフォンアポインター", "img": "recruit02.jpg",
        "alt": "電話をかけるスタッフ",
        "summary": "福島県内の事業所へテレフォンアポイントを取っていただくお仕事になります。",
        "type": "パート・アルバイト", "pay": "時給：1,100〜1,500円",
        "work": """<p>福島県内の事業所へテレフォンアポイントを取っていただくお仕事になります。電話対応のマニュアルがあり、先輩のサポートがあるので、安心してお仕事をしていただけます。</p>
<p class="note">※取り扱う商品は、空調設備機、LED照明等の環境商材です。</p>""",
        "req": "エクセル・ワードの入力",
        "hours": "9:00〜16:00（休憩90分）、週所定労働日数：週3日程度",
        "welfare": "昇給有、交通費支給（上限：月額3,000円）",
        "holiday": "土・日・祝日（完全週休2日制）、年末年始・夏季休暇有",
        "other": COMMON_OTHER_NEW,
    },
    {
        "id": "77", "name": "管理職責任者", "img": "recruit04.jpg",
        "alt": "パソコンに向かう社員",
        "summary": "空調設備機器、LED照明等の環境商材の販売を行っていただきます。",
        "type": "正社員", "pay": "月給：350,000〜650,000円",
        "work": SALES_WORK,
        "req": "エクセル・ワードの入力程度",
        "hours": "9:00〜18:00（休憩1時間）、又は10:00〜19:00の間の8時間程度",
        "welfare": "賞与有、退職金制度有、交通費支給（上限：月額3,000円）",
        "holiday": "土・日・祝日（完全週休2日制）、年間休日120日、年末年始・夏季休暇有",
        "other": COMMON_OTHER_R4,
    },
]

FORM_NOTE = """<ul class="form__note">
<li><b>*</b> は入力必須項目ですので、必ずご記入ください。</li>
<li>メールアドレスは正しくご入力ください。（誤りがあると弊社より返信メールが届きません。）</li>
<li>半角カナ入力は文字化けの原因となりますのでご注意ください。</li>
<li>問い合わせから1週間しても連絡が来ない場合は、送信エラーの可能性も考えられますので、再度ご連絡ください。</li>
</ul>"""


def _field(label, req, fid, html):
    r = '<i>必須</i>' if req else ''
    return f"""      <div class="form__row">
        <label class="form__l" for="{fid}">{label}{r}</label>
        <div class="form__f">{html}</div>
      </div>"""


def apply_form(jid):
    f = [
        _field("お名前", True, f"n{jid}", f'<input type="text" name="name" id="n{jid}" autocomplete="name" required>'),
        _field("フリガナ", True, f"k{jid}", f'<input type="text" name="kana" id="k{jid}" required>'),
        _field("電話番号（携帯可）", True, f"t{jid}", f'<input type="tel" name="tel" id="t{jid}" autocomplete="tel" required>'),
        _field("メールアドレス", True, f"m{jid}", f'<input type="email" name="mail" id="m{jid}" autocomplete="email" required>'),
        _field("メールアドレス（確認用）", True, f"m2{jid}", f'<input type="email" name="mail2" id="m2{jid}" required>'),
        _field("生年月日", True, f"b{jid}", f'<input type="date" name="birth" id="b{jid}" required>'),
        _field("連絡方法の補足事項", False, f"no{jid}", f'<textarea name="note" id="no{jid}" rows="4" placeholder="ご連絡がつきやすい時間帯など"></textarea>'),
        _field("現在の就業状況", True, f"s{jid}", f'<textarea name="status" id="s{jid}" rows="3" required></textarea>'),
        _field("送信確認", True, f"c{jid}", f'<label class="form__check"><input type="checkbox" name="ok" id="c{jid}" required><span>上記の送信内容を確認しました。</span></label>'),
    ]
    return f"""{FORM_NOTE}
    <form class="form" method="post" action="#" data-demo="1" aria-describedby="formDemo">
{chr(10).join(f)}
      <p class="form__demo" id="formDemo">これはデモサイトです。<b>送信はできません。</b>ご応募は <a class="mono" href="tel:{TEL_RAW}">{TEL}</a>（担当：増子）へお願いします。</p>
    </form>"""


def build_index():
    title = "採用情報｜株式会社パーソンライト"
    desc = "エアコン設備工事スタッフ・営業職・テレフォンアポインター・管理職責任者を募集しています。福島県郡山市の株式会社パーソンライト採用情報。"
    cards = "\n".join(f"""      <article class="job rise">
        <a href="./{j['id']}/">
          <div class="job__fig"><img src="../assets/img/{j['img']}" alt="{j['alt']}" width="720" height="516" loading="lazy"></div>
          <div class="job__b">
            <p class="mono">JOB {i+1:02d}　{j['type']}</p>
            <h2 class="job__t">{j['name']}</h2>
            <p class="job__s">{j['summary']}</p>
            <p class="job__pay mono">{j['pay']}</p>
            <span class="job__go">募集要項を見る →</span>
          </div>
        </a>
      </article>""" for i, j in enumerate(JOBS))

    ld = [{
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": j["name"],
                             "url": f"https://nextray-gk.github.io/personright-demo/recruit/{j['id']}/"}
                            for i, j in enumerate(JOBS)],
    }]
    return head(title, desc, "recruit", 1, extra=jsonld(1, ld)) + header("recruit", 1) + f"""
<main id="main">
""" + phero("05", "RECRUIT", "採用情報",
            "自ら行動する意欲や姿勢を持ち、チャレンジ精神のある人を求めています。天井に上がる工事の仕事から、事業所へ電話をかける仕事まで、4つの職種で募集中です。",
            "recruit01.jpg", "お客様と商談する営業社員", [("採用情報", "")], 1, 720, 516) + f"""

<section class="sec" id="openings">
  <div class="wrap">
    {sh("01", "募集中", "4つの職種で、<br>募集しています。")}
    <div class="jobs">
{cards}
    </div>
  </div>
</section>

</main>
""" + footer(1)


def build_job(j):
    title = f"{j['name']}の募集要項｜採用情報｜株式会社パーソンライト"
    desc = f"{j['name']}（{j['type']}・{j['pay']}）を募集しています。{j['summary']}福島県郡山市の株式会社パーソンライト。"
    rows = [
        ("仕事内容", j["work"]),
        ("応募資格", f"<p>{j['req']}</p>"),
        ("勤務時間", f"<p>{j['hours']}</p>"),
        ("給与", f'<p class="mono">{j["pay"]}</p>'),
        ("待遇", f"<p>{j['welfare']}</p>"),
        ("休日・休暇", f"<p>{j['holiday']}</p>"),
        ("その他", f"<p>{j['other']}</p>"),
    ]
    tbl = "\n".join(f"""      <div><dt>{k}</dt><dd>{v}</dd></div>""" for k, v in rows)

    others = "\n".join(f"""      <li><a href="../{o['id']}/"><b>{o['name']}</b><span>{o['type']}</span><span class="mono">{o['pay']}</span><i aria-hidden="true">→</i></a></li>"""
                       for o in JOBS if o["id"] != j["id"])

    ld = [{
        "@context": "https://schema.org", "@type": "JobPosting",
        "title": j["name"],
        "description": j["summary"],
        "employmentType": "FULL_TIME" if j["type"] == "正社員" else "PART_TIME",
        "hiringOrganization": {"@type": "Organization", "name": "株式会社パーソンライト"},
        "jobLocation": {"@type": "Place", "address": {
            "@type": "PostalAddress", "addressCountry": "JP", "addressRegion": "福島県",
            "addressLocality": "郡山市", "streetAddress": "安積町日出山2-43", "postalCode": "963-0101"}},
    }]

    return head(title, desc, "recruit", 2, extra=jsonld(2, ld)) + header("recruit", 2) + f"""
<main id="main">
""" + phero("05", "RECRUIT", j["name"], f'{j["summary"]}<br><span class="mono">{j["type"]}　{j["pay"]}</span>', j["img"], j["alt"],
            [("採用情報", "recruit/"), (j["name"], "")], 2, 720, 516) + f"""

<section class="sec">
  <div class="wrap duo duo--top">
    {sh("01", "募集要項", "募集要項")}
    <dl class="spec rise">
{tbl}
    </dl>
  </div>
</section>

<section class="sec sec--p2">
  <div class="wrap duo duo--top">
    {sh("02", "応募", "応募は、電話か<br>フォームで。")}
    <div class="rise">
      <div class="apply">
        <div><small>お電話</small><a class="mono" href="tel:{TEL_RAW}">{TEL}</a><p>株式会社パーソンライト（担当：増子）</p></div>
        <div><small>フォーム</small><a class="tl" href="#applyForm">応募フォームへ</a></div>
      </div>
      <h3 class="form__h" id="applyForm">応募フォーム</h3>
      {apply_form(j['id'])}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap duo duo--top">
    {sh("03", "ほかの職種", "ほかの募集")}
    <ul class="rows rise">
{others}
    </ul>
  </div>
</section>

</main>
""" + footer(2)
