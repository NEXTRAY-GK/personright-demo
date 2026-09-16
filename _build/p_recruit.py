# -*- coding: utf-8 -*-
"""採用情報 /recruit/ と求人4本（2026-09-16 第3版）"""
from common import head, header, phero, footer, jsonld, sh, TEL, TEL_RAW

COMMON_OTHER_NEW = "2022年12月に株式会社になった、まだ若い会社です。営業も工事も、これから一緒に形を作っていける人を探しています。"
COMMON_OTHER_R4 = "令和4年12月に株式会社になった、まだ若い会社です。営業も工事も、これから一緒に形を作っていける人を探しています。"

SALES_WORK = """<p>空調設備やLED照明など、省エネにつながる商品の販売をお任せします。</p>
<ul class="dots">
<li>お客様は、主に福島県内の中小企業です。</li>
<li>基礎を学ぶ研修があり、はじめは先輩と一緒に営業へ回るので、自分のペースで慣れていけます。</li>
<li>自分なりのやりがいを見つけていける仕事です。</li>
</ul>"""

JOBS = [
    {
        "id": "49", "name": "エアコン設備工事スタッフ", "img": "recruit03.jpg",
        "alt": "天井のエアコンを点検する工事スタッフ",
        "summary": "お店や会社、ご家庭のエアコンを取り付ける仕事です。",
        "type": "正社員", "pay": "月給：220,000〜450,000円",
        "work": """<p>経験のある方を優遇します。道具や材料にくわしい方を探しています。親方として現場の最前線に立ち、子方と2人1組で動くのが基本です。</p>
<p>朝は事務所に出勤して、その日の現場へ向かいます。場合によっては、現場への直行・直帰もできます。自分の車を使ってもよく、細かい報告の仕事もありません。自分のスケジュールで動ける職場です。</p>""",
        "req": "ひととおりの施工ができる知識と技術が必要です。",
        "hours": "8:00〜18:00（休憩2時間）　※現場によって就業時間が多少変動することがあります。",
        "welfare": "賞与有、退職金制度有、交通費支給（上限：月額3,000円）",
        "holiday": "週休2日制（土・日・祝、会社カレンダーによる）、年間休日120日",
        "other": COMMON_OTHER_NEW,
    },
    {
        "id": "46", "name": "営業職", "img": "recruit01.jpg",
        "alt": "お客様と商談する営業社員",
        "summary": "空調設備やLED照明など、省エネにつながる商品を提案して販売する仕事です。",
        "type": "正社員", "pay": "月給：220,000〜650,000円",
        "work": SALES_WORK,
        "req": "エクセルやワードで入力ができれば大丈夫です",
        "hours": "9:00〜18:00（休憩1時間）、又は10:00〜19:00の間の8時間程度",
        "welfare": "賞与有、退職金制度有、交通費支給（上限：月額5,000円）",
        "holiday": "土・日・祝日（完全週休2日制）、年間休日120日、年末年始・夏季休暇有",
        "other": COMMON_OTHER_NEW,
    },
    {
        "id": "48", "name": "テレフォンアポインター", "img": "recruit02.jpg",
        "alt": "電話をかけるスタッフ",
        "summary": "福島県内の会社やお店に電話をかけて、訪問の約束をいただく仕事です。",
        "type": "パート・アルバイト", "pay": "時給：1,100〜1,500円",
        "work": """<p>福島県内の会社やお店に電話をかけて、営業にうかがう約束をいただく仕事です。電話で話す内容のマニュアルがあり、先輩もついているので、はじめてでも安心して始められます。</p>
<p class="note">※扱う商品は、空調設備やLED照明などです。</p>""",
        "req": "エクセルやワードで入力ができること",
        "hours": "9:00〜16:00（休憩90分）、週所定労働日数：週3日程度",
        "welfare": "昇給有、交通費支給（上限：月額3,000円）",
        "holiday": "土・日・祝日（完全週休2日制）、年末年始・夏季休暇有",
        "other": COMMON_OTHER_NEW,
    },
    {
        "id": "77", "name": "管理職責任者", "img": "recruit04.jpg",
        "alt": "パソコンに向かう社員",
        "summary": "空調設備やLED照明などの販売をまとめる、管理職の仕事です。",
        "type": "正社員", "pay": "月給：350,000〜650,000円",
        "work": SALES_WORK,
        "req": "エクセルやワードで入力ができれば大丈夫です",
        "hours": "9:00〜18:00（休憩1時間）、又は10:00〜19:00の間の8時間程度",
        "welfare": "賞与有、退職金制度有、交通費支給（上限：月額3,000円）",
        "holiday": "土・日・祝日（完全週休2日制）、年間休日120日、年末年始・夏季休暇有",
        "other": COMMON_OTHER_R4,
    },
]

FORM_NOTE = """<ul class="form__note">
<li>「必須」のついた項目は、必ずご記入ください。</li>
<li>メールアドレスが間違っていると、こちらからの返信が届きません。</li>
<li>半角カナは文字化けすることがあるので、全角でご入力ください。</li>
<li>1週間たっても連絡がない場合は、うまく送れていないかもしれません。お手数ですが、もう一度ご連絡ください。</li>
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
        _field("連絡についての補足", False, f"no{jid}", f'<textarea name="note" id="no{jid}" rows="4" placeholder="ご連絡がつきやすい時間帯など"></textarea>'),
        _field("現在の就業状況", True, f"s{jid}", f'<textarea name="status" id="s{jid}" rows="3" required></textarea>'),
        _field("送信確認", True, f"c{jid}", f'<label class="form__check"><input type="checkbox" name="ok" id="c{jid}" required><span>入力した内容を確かめました。</span></label>'),
    ]
    return f"""{FORM_NOTE}
    <form class="form" method="post" action="#" data-demo="1" aria-describedby="formDemo">
{chr(10).join(f)}
      <p class="form__demo" id="formDemo">これはデモサイトです。<b>送信はできません。</b>ご応募は <a class="mono" href="tel:{TEL_RAW}">{TEL}</a>（担当：増子）へお願いします。</p>
    </form>"""


def paybar(j):
    """月給の幅を、65万円までの目盛りで見せる（時給の仕事は出さない）"""
    import re
    if not j["pay"].startswith("月給"):
        return ""
    a, b = [int(x.replace(",", "")) for x in re.findall(r"[\d,]+", j["pay"])[:2]]
    return (f'<div class="pay" data-k="enter" aria-hidden="true">'
            f'<i style="--a:{a/650000:.3f};--b:{b/650000:.3f}"></i>'
            f'<span class="pay__s mono">0</span><span class="pay__e mono">65万円</span></div>')


def build_index():
    title = "採用情報｜株式会社パーソンライト"
    desc = "エアコン設備工事スタッフ・営業職・テレフォンアポインター・管理職責任者を募集しています。福島県郡山市の株式会社パーソンライト採用情報。"
    cards = "\n".join(f"""      <article class="job rise">
        <a href="./{j['id']}/">
          <div class="job__fig"><img src="../assets/img/{j['img']}" alt="{j['alt']}" width="720" height="516" loading="lazy"></div>
          <div class="job__b">
            <p class="job__ty">{j['type']}</p>
            <h2 class="job__t">{j['name']}</h2>
            <p class="job__s">{j['summary']}</p>
            <p class="job__pay mono">{j['pay']}</p>
            {paybar(j)}
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
            "自分から動ける人、新しいことに挑戦したい人を探しています。天井に上がる工事の仕事から、会社やお店に電話をかける仕事まで、4つの職種で募集中です。",
            "recruit01.jpg", "お客様と商談する営業社員", [("採用情報", "")], 1, 720, 516) + f"""

<section class="sec" id="openings">
  <div class="wrap">
    {sh("", "募集している仕事", "いま、4つの職種で<br>募集しています。")}
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
    {sh("", "募集要項", "募集要項")}
    <div>
    {paybar(j)}
    <dl class="spec rise" data-k="through" data-steps>
{tbl}
    </dl>
    </div>
  </div>
</section>

<section class="sec sec--p2">
  <div class="wrap duo duo--top">
    {sh("", "応募", "応募は、お電話か<br>フォームでどうぞ。")}
    <div class="rise">
      <div class="apply">
        <div><small>お電話で</small><a class="mono" href="tel:{TEL_RAW}">{TEL}</a><p>株式会社パーソンライト（担当：増子）</p></div>
        <div><small>フォームで</small><a class="tl" href="#applyForm">応募フォームへ</a></div>
      </div>
      <h3 class="form__h" id="applyForm">応募フォーム</h3>
      {apply_form(j['id'])}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap duo duo--top">
    {sh("", "ほかの職種", "ほかの募集")}
    <ul class="rows rise">
{others}
    </ul>
  </div>
</section>

</main>
""" + footer(2)
