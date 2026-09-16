# -*- coding: utf-8 -*-
"""お問い合わせ・完了・プライバシーポリシー（2026-09-16 第3版）"""
from common import head, header, phero, footer, jsonld, sh, TEL, TEL_RAW, FAX, ZIP, ADDR

FORM_NOTE = """<ul class="form__note">
<li>docomo、au、softbank等のキャリアメールをご利用の方には、返信メールが届かない場合がございます。不明な点があれば下記までご連絡ください。</li>
<li>半角カナ入力は文字化けの原因となりますのでご注意ください。</li>
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
    desc = f"業務用エアコン・防犯カメラ・複合機のご相談、お見積りの依頼はこちらから。お電話（{TEL}）でも承ります。福島県郡山市の株式会社パーソンライト。"
    topics = "".join(f'<label class="pill"><input type="checkbox" name="topic" value="{t}"><span>{t}</span></label>' for t in TOPICS)
    fields = "\n".join([
        f"""      <fieldset class="form__row">
        <legend class="form__l">ご相談の種類</legend>
        <div class="form__f pills">{topics}</div>
      </fieldset>""",
        _field("お名前", True, "f-name", '<input type="text" name="name" id="f-name" autocomplete="name" required>'),
        _field("フリガナ", True, "f-kana", '<input type="text" name="kana" id="f-kana" required>'),
        _field("電話番号（携帯可）", True, "f-tel", '<input type="tel" name="tel" id="f-tel" autocomplete="tel" required>'),
        _field("メールアドレス", True, "f-mail", '<input type="email" name="mail" id="f-mail" autocomplete="email" required>'),
        _field("メールアドレス（確認用）", True, "f-mail2", '<input type="email" name="mail2" id="f-mail2" required>'),
        _field("お問い合わせ内容", True, "f-body", '<textarea name="body" id="f-body" rows="8" required placeholder="ご検討中の機器、設置場所、台数など、分かる範囲でお書きください。"></textarea>'),
        _field("送信確認", True, "f-ok", '<label class="form__check"><input type="checkbox" name="ok" id="f-ok" required><span>「<a href="../privacy/">プライバシーポリシー</a>」を確認し、同意します。</span></label>'),
    ])
    return head(title, desc, "contact", 1, extra=jsonld(1)) + header("contact", 1) + f"""
<main id="main">
""" + phero("06", "CONTACT", "お問い合わせ",
            "お見積りは無料です。お電話でも、下のフォームからでも。フォームは24時間受け付け、内容を確認して後日担当からご連絡します。",
            None, None, [("お問い合わせ", "")], 1) + f"""

<section class="sec sec--flush">
  <div class="wrap duo duo--top">
    <div class="ways rise">
      <p class="sh__no mono"><b>TEL</b><span>お電話</span></p>
      <a class="ways__tel mono" href="tel:{TEL_RAW}">{TEL}</a>
      <p>FAX <span class="mono">{FAX}</span></p>
    </div>
    <div class="rise">
      <p class="sh__no mono"><b>FORM</b><span>フォーム</span></p>
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
            "内容を確認のうえ、担当より折り返しご連絡いたします。",
            None, None, [("お問い合わせ", "contact/"), ("送信完了", "")], 2) + f"""

<section class="sec sec--flush">
  <div class="wrap">
    <p class="lede rise">3日たっても連絡が届かないときは、お手数ですが <a class="mono" href="tel:{TEL_RAW}">{TEL}</a> までお電話ください。</p>
    <p class="more rise"><a class="btn" href="../../">トップへ戻る</a></p>
  </div>
</section>

</main>
""" + footer(2, cta_on=False)


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
        <h2><span class="mono">{n}</span>{t}</h2>
        <p>{d}</p>
      </section>""" for n, t, d in PRIVACY)
    return head(title, desc, "privacy", 1, extra=jsonld(1)) + header("privacy", 1) + f"""
<main id="main">
""" + phero("07", "PRIVACY POLICY", "プライバシーポリシー",
            "パーソンライト（以下、当社という）は、皆様からお預かりする個人情報の管理に細心の注意を払い、これを取り扱うものとします。",
            None, None, [("プライバシーポリシー", "")], 1) + f"""

<section class="sec sec--flush">
  <div class="wrap duo duo--top">
    <p class="sh__no mono"><b>07</b><span>方針</span></p>
    <div>
      <div class="pp">
{items}
      </div>
      <div class="pp__box rise">
        <h2>お問い合わせ窓口</h2>
        <p>上記内容に関してご質問などがございましたら、下記連絡先にご連絡ください。</p>
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
