# -*- coding: utf-8 -*-
"""お問い合わせ・完了・プライバシーポリシー（2026-09-16 第3版）"""
from common import head, header, phero, footer, jsonld, sh, TEL, TEL_RAW, FAX, ZIP, ADDR

FORM_NOTE = """<ul class="form__note">
<li>docomo・au・softbankなど、携帯会社のメールアドレスをお使いの場合、こちらからの返信が届かないことがあります。困ったときはお電話ください。</li>
<li>半角カナは文字化けすることがあるので、全角でご入力ください。</li>
</ul>"""

TOPICS = ["業務用エアコン", "リース", "クリーニング", "防犯カメラ", "複合機", "ビジネスフォン", "その他"]


def _field(label, req, fid, html):
    r = '<i>必須</i>' if req else ''
    return f"""      <div class="form__row">
        <label class="form__l" for="{fid}">{label}{r}</label>
        <div class="form__f">{html}</div>
      </div>"""


def contact():
    title = "お問い合わせ｜株式会社パーソンライト"
    desc = f"業務用エアコン・防犯カメラ・複合機のご相談、お見積りの依頼はこちらから。お電話（{TEL}）でも受け付けています。福島県郡山市の株式会社パーソンライト。"
    topics = "".join(f'<label class="pill"><input type="checkbox" name="topic" value="{t}"><span>{t}</span></label>' for t in TOPICS)
    fields = "\n".join([
        f"""      <fieldset class="form__row">
        <legend class="form__l">何についてのご相談ですか</legend>
        <div class="form__f pills">{topics}</div>
      </fieldset>""",
        _field("お名前", True, "f-name", '<input type="text" name="name" id="f-name" autocomplete="name" required>'),
        _field("フリガナ", True, "f-kana", '<input type="text" name="kana" id="f-kana" required>'),
        _field("電話番号（携帯可）", True, "f-tel", '<input type="tel" name="tel" id="f-tel" autocomplete="tel" required>'),
        _field("メールアドレス", True, "f-mail", '<input type="email" name="mail" id="f-mail" autocomplete="email" required>'),
        _field("メールアドレス（確認用）", True, "f-mail2", '<input type="email" name="mail2" id="f-mail2" required>'),
        _field("ご相談の内容", True, "f-body", '<textarea name="body" id="f-body" rows="8" required placeholder="考えている機器や取り付ける場所、台数など、わかる範囲で書いてください。"></textarea>'),
        _field("送信確認", True, "f-ok", '<label class="form__check"><input type="checkbox" name="ok" id="f-ok" required><span>「<a href="../privacy/">プライバシーポリシー</a>」を読んで、同意します。</span></label>'),
    ])
    return head(title, desc, "contact", 1, extra=jsonld(1)) + header("contact", 1) + f"""
<main id="main">
""" + phero("06", "CONTACT", "お問い合わせ",
            "お見積りは無料です。お電話でもフォームでも、どちらでも構いません。フォームは24時間受け付けていて、内容を確かめてから担当者がご連絡します。",
            None, None, [("お問い合わせ", "")], 1) + f"""

<section class="sec sec--flush">
  <div class="wrap duo duo--top">
    <div class="ways rise">
      <p class="sh__no mono"><span>お電話で</span></p>
      <a class="ways__tel mono" href="tel:{TEL_RAW}">{TEL}</a>
      <p>FAX <span class="mono">{FAX}</span></p>
    </div>
    <div class="rise">
      <p class="sh__no mono"><span>フォームで</span></p>
      {FORM_NOTE}
      <form class="form" method="post" action="./thanks/" data-demo="1" aria-describedby="formDemo">
{fields}
        <p class="form__demo" id="formDemo">これはデモサイトです。<b>送信はできません。</b>お急ぎの用件は <a class="mono" href="tel:{TEL_RAW}">{TEL}</a> へお願いします。</p>
      </form>
    </div>
  </div>
</section>

</main>
""" + footer(1, cta_on=False)


def thanks():
    title = "送信ありがとうございました｜株式会社パーソンライト"
    desc = "お問い合わせを受け付けました。株式会社パーソンライト。"
    return head(title, desc, "contact", 2, extra=jsonld(2)) + header("contact", 2) + f"""
<main id="main">
""" + phero("06-2", "THANK YOU", "送信ありがとうございました",
            "内容を確かめて、担当者から折り返しご連絡します。",
            None, None, [("お問い合わせ", "contact/"), ("送信完了", "")], 2) + f"""

<section class="sec sec--flush">
  <div class="wrap">
    <p class="lede rise">3日たっても連絡がないときは、お手数ですが <a class="mono" href="tel:{TEL_RAW}">{TEL}</a> までお電話ください。</p>
    <p class="more rise"><a class="btn" href="../../">トップへ戻る</a></p>
  </div>
</section>

</main>
""" + footer(2, cta_on=False)


PRIVACY = [
    ("1", "個人情報を受け取るとき、使うとき、渡すとき",
     "仕事の中で個人情報をお預かりするときは、何に使うのかをはっきりさせ、その目的に必要な範囲でだけ使います。目的以外には使わないよう、社内で手立てを取ります。また、ご本人の同意がある場合や正当な理由がある場合を除いて、お預かりした個人情報を第三者に見せたり渡したりしません。"),
    ("2", "法律や決まりを守ります",
     "個人情報の扱いについては、関係する法律や国の指針などの決まりを守ります。"),
    ("3", "しっかり管理して守ります",
     "個人情報は厳しく管理します。外に漏れたり、なくなったり、壊れたりしないよう、防ぐための対策と、起きたときに正すための対策を取ります。"),
    ("4", "ご相談や苦情には、すぐに対応します",
     "個人情報の扱いについてご相談や苦情をいただいたときは、すぐに対応します。"),
    ("5", "管理の体制を整え、よくしていきます",
     "個人情報を正しく扱うための責任者と体制を決めます。社内の決まりを作って全員に伝え、定期的に点検と見直しを行い、個人情報を守る仕組みをよくし続けます。"),
]


def privacy():
    title = "プライバシーポリシー｜株式会社パーソンライト"
    desc = "株式会社パーソンライトの個人情報保護方針です。"
    items = "\n".join(f"""      <section class="pp__i rise">
        <h2><span class="mono">{n}</span>{t}</h2>
        <p>{d}</p>
      </section>""" for n, t, d in PRIVACY)
    return head(title, desc, "privacy", 1, extra=jsonld(1)) + header("privacy", 1) + f"""
<main id="main">
""" + phero("07", "PRIVACY POLICY", "プライバシーポリシー",
            "パーソンライト（以下、当社）は、みなさまからお預かりする個人情報を、細心の注意を払って扱います。",
            None, None, [("プライバシーポリシー", "")], 1) + f"""

<section class="sec sec--flush">
  <div class="wrap duo duo--top">
    <p class="sh__no mono"><span>方針</span></p>
    <div>
      <div class="pp">
{items}
      </div>
      <div class="pp__box rise">
        <h2>お問い合わせ窓口</h2>
        <p>この方針についてご質問があれば、下の連絡先までお問い合わせください。</p>
        <address class="addr">
          パーソンライト<br>
          {ZIP}　{ADDR}<br>
          TEL <a class="mono" href="tel:{TEL_RAW}">{TEL}</a> ／ FAX <span class="mono">{FAX}</span>
        </address>
      </div>
    </div>
  </div>
</section>

</main>
""" + footer(1, cta_on=False)
