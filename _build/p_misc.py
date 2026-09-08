# -*- coding: utf-8 -*-
"""お問い合わせ・完了・プライバシーポリシー"""
from common import head, header, phero, footer, jsonld, TEL, TEL_RAW, FAX, ZIP, ADDR

FORM_NOTE = """<ul class="form__note">
<li>docomo、au、softbank等のキャリアメールをご利用の方には、返信メールが届かない場合がございます。不明な点があれば下記までご連絡ください。</li>
<li>半角カナ入力は文字化けの原因となりますのでご注意ください。</li>
<li>データを送信される際の情報はSSL暗号通信により保護されますので、安心してご利用ください。</li>
</ul>"""


def _field(label, req, html):
    r = '<i>必須</i>' if req else ''
    return f"""      <div class="form__row">
        <div class="form__l">{label}{r}</div>
        <div class="form__f">{html}</div>
      </div>"""


def contact():
    title = "お問い合わせ｜株式会社パーソンライト"
    desc = f"業務用エアコン・防犯カメラ・複合機のご相談、資料請求はこちらから。お電話（{TEL}）でも承ります。福島県郡山市の株式会社パーソンライト。"
    fields = "\n".join([
        _field("お名前", True, '<input type="text" name="name" id="f-name" autocomplete="name" required>'),
        _field("フリガナ", True, '<input type="text" name="kana" id="f-kana" required>'),
        _field("電話番号（携帯可）", True, '<input type="tel" name="tel" id="f-tel" autocomplete="tel" required>'),
        _field("メールアドレス", True, '<input type="email" name="mail" id="f-mail" autocomplete="email" required>'),
        _field("メールアドレス（確認用）", True, '<input type="email" name="mail2" id="f-mail2" required>'),
        _field("お問い合わせ内容", True, '<textarea name="body" id="f-body" rows="8" required placeholder="ご検討中の機器、設置場所、台数など、分かる範囲でお書きください。"></textarea>'),
        _field("送信確認", True, '<label class="form__check"><input type="checkbox" name="ok" id="f-ok" required><span>「<a href="../privacy/">プライバシーポリシー</a>」を確認し、同意します。</span></label>'),
    ])
    return head(title, desc, "contact", 1, extra=jsonld(1)) + header("contact", 1) + f"""
<main id="main">
""" + phero("Contact Us", "お問い合わせ",
            "ご質問や資料請求等ございましたら、下記メールフォームよりご連絡ください。後日、担当よりご連絡させていただきます。",
            "office-front.jpg", "福島県郡山市安積町日出山にある本社の外観", [("お問い合わせ", "")], 1) + f"""

<section class="sec--tight">
  <div class="narrow">
    <div class="ways rise">
      <div class="ways__i">
        <small>BY PHONE</small>
        <a class="tel num" href="tel:{TEL_RAW}">{TEL}</a>
        <p>FAX <span class="num">{FAX}</span></p>
      </div>
      <div class="ways__i">
        <small>BY FORM</small>
        <p>24時間受け付けています。<br>内容を確認のうえ、後日担当よりご連絡します。</p>
      </div>
    </div>
  </div>
</section>

<section class="sec--tight" style="padding-top:0;padding-bottom:var(--sec)">
  <div class="narrow">
    <div class="lead rise">
      <span class="lead__en">Mail Form</span>
      <h2 class="lead__ja">メールフォーム</h2>
      <div class="rule"></div>
    </div>
    {FORM_NOTE}
    <form class="form rise" method="post" action="./thanks/" data-demo="1" aria-describedby="formDemo">
{fields}
      <p class="form__demo" id="formDemo">これはデモサイトです。<b>送信はできません。</b>お急ぎの用件は <a class="num" href="tel:{TEL_RAW}">{TEL}</a> へお願いします。</p>
    </form>
  </div>
</section>

</main>
""" + footer(1)


def thanks():
    title = "送信ありがとうございました｜株式会社パーソンライト"
    desc = "お問い合わせを受け付けました。株式会社パーソンライト。"
    return head(title, desc, "contact", 2, extra=jsonld(2)) + header("contact", 2) + f"""
<main id="main">
""" + phero("Thank You", "送信ありがとうございました", None, "office-front.jpg",
            "福島県郡山市安積町日出山にある本社の外観",
            [("お問い合わせ", "contact/"), ("送信完了", "")], 2) + f"""

<section class="sec">
  <div class="narrow" style="text-align:center">
    <p class="rise">お問い合わせいただき、ありがとうございました。<br>内容を確認のうえ、担当より折り返しご連絡いたします。</p>
    <p class="rise" style="margin-top:26px;color:var(--ink-2);font-size:13.5px">3日たっても連絡が届かないときは、お手数ですが <a class="num" href="tel:{TEL_RAW}">{TEL}</a> までお電話ください。</p>
    <p class="rise" style="margin-top:40px"><a class="btn" href="../../">ホームへ戻る</a></p>
  </div>
</section>

</main>
""" + footer(2)


PRIVACY = [
    ("1", "個人情報の取得、利用及び提供",
     "当社は、業務上個人情報を取得する場合には利用目的を特定し、その利用目的の達成に必要な限度で取扱い、目的外利用を行わないための措置を講じます。また、当社はご提供いただいた個人情報を、ご本人様の同意がある場合または正当な理由がある場合を除き、第三者に開示または提供いたしません。"),
    ("2", "法令及びその他の規範の順守",
     "当社は、保有する個人情報の取扱いに関し、適用される法令及び国が定める指針その他の規範を順守します。"),
    ("3", "個人情報の管理と保護",
     "当社は、個人情報の管理を厳重に行ない、個人情報の漏えい、滅失又はき損を防ぐため、適切な防止及び是正処置を行います。"),
    ("4", "お問い合わせ・苦情への対応",
     "当社は、保有する個人情報の取り扱いに対するご相談や苦情について、速やかに対応致します。"),
    ("5", "個人情報保護管理体制の確立及び仕組みの継続的改善",
     "当社は、業務上の個人情報を適正に取扱うための責任体制を確立し、また個人情報保護を実践するため、内部規程を整備して全従業者に周知し、定期的な監査と見直しを行い、個人情報保護マネジメントシステムの継続的改善に努めます。"),
]


def privacy():
    title = "プライバシーポリシー｜株式会社パーソンライト"
    desc = "株式会社パーソンライトの個人情報保護方針です。"
    items = "\n".join(f"""      <section class="pp__i rise">
        <h2 class="pp__t"><span class="num">{n}</span>{t}</h2>
        <p>{d}</p>
      </section>""" for n, t, d in PRIVACY)
    return head(title, desc, "privacy", 1, extra=jsonld(1)) + header("privacy", 1) + f"""
<main id="main">
""" + phero("Privacy Policy", "プライバシーポリシー", None, "office-side.jpg",
            "Person right の看板を掲げた本社の外観", [("プライバシーポリシー", "")], 1) + f"""

<section class="sec">
  <div class="narrow">
    <p class="rise">パーソンライト（以下、当社という）は、皆様からお預かりする個人情報の管理に細心の注意を払い、これを取り扱うものとします。</p>
    <div class="pp">
{items}
    </div>
    <div class="pp__box rise">
      <h2 class="pp__t">お問い合わせ窓口</h2>
      <p>上記内容に関してご質問などがございましたら、下記連絡先にご連絡ください。</p>
      <address class="acc__a">
        パーソンライト<br>
        {ZIP}　{ADDR}<br>
        TEL <a class="num" href="tel:{TEL_RAW}">{TEL}</a> ／ FAX <span class="num">{FAX}</span>
      </address>
    </div>
  </div>
</section>

</main>
""" + footer(1)
