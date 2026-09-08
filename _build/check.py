#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""組み上げたサイトを点検する。推測で埋めず、その場で数える。"""
import os, re, json, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NG, WARN = [], []


def pages():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in (".git", "_build", "assets")]
        for f in fn:
            if f.endswith(".html"):
                yield os.path.join(dp, f)


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h = []
        self.imgs = []
        self.links = []
        self.ids = set()
        self.title = None
        self._t = False
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.h.append(int(tag[1]))
        if tag == "img":
            self.imgs.append(a)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "title":
            self._t = True

    def handle_data(self, d):
        if self._t:
            self.title = (self.title or "") + d

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False


def rel(p):
    return os.path.relpath(p, ROOT)


def main():
    files = sorted(pages())
    print(f"■ {len(files)} ページ")
    all_ids = {}
    for f in files:
        s = open(f, encoding="utf-8").read()
        p = P()
        p.feed(s)
        r = rel(f)
        all_ids[os.path.dirname(r) or "."] = p.ids

        # h1 は1つ、階層を飛ばさない
        h1 = p.h.count(1)
        if h1 != 1:
            NG.append(f"{r}: h1 が {h1} 個")
        prev = 0
        for lv in p.h:
            if prev and lv > prev + 1:
                NG.append(f"{r}: 見出しが h{prev} から h{lv} へ飛んでいる")
                break
            prev = lv

        # title / lang / description
        if not p.title or len(p.title.strip()) < 8:
            NG.append(f"{r}: title が短い/無い")
        if p.lang != "ja":
            NG.append(f"{r}: lang が ja でない")
        if 'name="description"' not in s:
            NG.append(f"{r}: description が無い")

        # alt
        for a in p.imgs:
            if "alt" not in a:
                NG.append(f"{r}: alt の無い img … {a.get('src')}")
            if not a.get("width") or not a.get("height"):
                WARN.append(f"{r}: width/height の無い img … {a.get('src')}")

        # 画像の実在
        for a in p.imgs:
            src = a.get("src", "")
            if src.startswith("http") or src.startswith("data:"):
                continue
            t = os.path.normpath(os.path.join(os.path.dirname(f), src.split("?")[0]))
            if not os.path.exists(t):
                NG.append(f"{r}: 画像が無い … {src}")

        # JSON-LD
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                NG.append(f"{r}: JSON-LD が壊れている … {e}")

    # リンク切れ
    for f in files:
        s = open(f, encoding="utf-8").read()
        p = P(); p.feed(s)
        r = rel(f)
        for href in p.links:
            if href.startswith(("http", "tel:", "mailto:", "javascript:")):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in p.ids:
                    NG.append(f"{r}: ページ内の飛び先が無い … {href}")
                continue
            path, _, frag = href.partition("#")
            if not path:
                continue
            t = os.path.normpath(os.path.join(os.path.dirname(f), path))
            if os.path.isdir(t):
                t = os.path.join(t, "index.html")
            if not os.path.exists(t):
                NG.append(f"{r}: リンク切れ … {href}")
            elif frag:
                d = os.path.relpath(os.path.dirname(t), ROOT)
                ids = all_ids.get(d if d != "." else ".", set())
                if frag not in ids:
                    NG.append(f"{r}: 飛び先の id が無い … {href}")

    # 画像の重さ
    big = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "assets", "img")):
        for f in fn:
            n = os.path.getsize(os.path.join(dp, f))
            if n > 300 * 1024:
                big.append((f, n))
    for f, n in big:
        WARN.append(f"assets/img/{f} が {n//1024}KB（300KB超）")

    css = os.path.getsize(os.path.join(ROOT, "assets", "css", "style.css"))
    js = os.path.getsize(os.path.join(ROOT, "assets", "js", "main.js"))
    img = sum(os.path.getsize(os.path.join(dp, f))
              for dp, dn, fn in os.walk(os.path.join(ROOT, "assets", "img")) for f in fn)
    print(f"■ CSS {css/1024:.0f}KB / JS {js/1024:.0f}KB / 画像 {img/1048576:.2f}MB（{len(os.listdir(os.path.join(ROOT,'assets','img')))}本）")

    print(f"\n■ 赤 {len(NG)} 件")
    for x in NG:
        print("  ×", x)
    print(f"■ 黄 {len(WARN)} 件")
    for x in WARN[:20]:
        print("  △", x)
    if len(WARN) > 20:
        print(f"  … 他 {len(WARN)-20} 件")
    return 1 if NG else 0


sys.exit(main())
