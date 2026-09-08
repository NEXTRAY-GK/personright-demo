#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""パーソンライト デモサイト — 組み立て。
   $ python3 _build/build.py     （リポジトリの直下でも _build の中でも動く）
   現行サイトの URL の形（拡張子なしのディレクトリ）をそのまま保つ。
"""
import os, sys, io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import p_top, p_ac, p_office, p_company, p_recruit, p_reviews, p_misc


def put(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return rel, len(html.encode("utf-8"))


def main():
    made = []
    made.append(put("index.html", p_top.build()))
    made.append(put("ac/index.html", p_ac.build()))
    made.append(put("office-tech/index.html", p_office.build()))
    made.append(put("company/index.html", p_company.build()))
    made.append(put("recruit/index.html", p_recruit.build_index()))
    for j in p_recruit.JOBS:
        made.append(put(f"recruit/{j['id']}/index.html", p_recruit.build_job(j)))
    made.append(put("reviews/index.html", p_reviews.build_index()))
    for v in p_reviews.VOICES:
        made.append(put(f"reviews/{v['id']}/index.html", p_reviews.build_one(v)))
    made.append(put("contact/index.html", p_misc.contact()))
    made.append(put("contact/thanks/index.html", p_misc.thanks()))
    made.append(put("privacy/index.html", p_misc.privacy()))

    # robots / sitemap（デモなので、検索には出さない）
    made.append(put("robots.txt", "User-agent: *\nDisallow: /\n"))
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    tot = sum(m[1] for m in made)
    print(f"{len(made)} 本 / 合計 {tot/1024:.0f}KB")
    for rel, n in made:
        print(f"  {n/1024:7.1f}KB  {rel}")


if __name__ == "__main__":
    main()
