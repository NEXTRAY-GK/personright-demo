# -*- coding: utf-8 -*-
"""等温線の地（assets/img/field.svg）を書き出す。

   空調は 目に見えない空気の温度を設計する仕事。
   その「温度の場」を1枚の等温線にして、節の地に敷く。
   写真の上には重ねない（2026-09-09、代表の「波が不自然」はそれで出た）。

   CSS 側は これを mask に使う。だから線は白で描く。
   色は敷く節のほうが持つので、暗い地でも明るい地でも同じ1枚で足りる。

   $ python3 _build/mk_field.py
"""
import io, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "img", "field.svg")

# ⚠️ 縦長にしてある。CSS は mask-size:cover で敷くので、
#    横幅で合わせたときに 背の高い節でも縦が足りるだけの高さが要る。
#    1600x1200 だと 背の高い節で拡大されすぎ、線が1〜2本しか見えなくなった（2026-09-10 実測）。
W, H = 1600, 2200          # viewBox
NX, NY = 120, 165          # 格子（細かくすると線は滑らかになるがファイルが太る）
LEVELS = 19                # 等温線の本数

# 熱源 … (x, y, 強さ, 広がり)。手で置いた。乱数を使わないので毎回同じ絵になる。
SOURCES = [
    (0.14, 0.09,  1.00, 0.17),
    (0.62, 0.04,  0.72, 0.13),
    (0.88, 0.17,  0.94, 0.15),
    (0.26, 0.29, -0.86, 0.14),
    (0.72, 0.36,  0.82, 0.16),
    (0.06, 0.44, -0.66, 0.12),
    (0.48, 0.52,  0.90, 0.15),
    (0.92, 0.58, -0.58, 0.12),
    (0.20, 0.66,  0.76, 0.14),
    (0.66, 0.74, -0.80, 0.13),
    (0.10, 0.82,  0.68, 0.12),
    (0.84, 0.88,  0.88, 0.15),
    (0.40, 0.94, -0.62, 0.13),
]


def temp(u, v):
    """0..1 の座標から温度を返す。ガウス山の重ね合わせ＋ゆるい大きな傾き。"""
    t = 0.42 * (1.0 - v) + 0.20 * math.sin(u * 2.3 + 0.7) + 0.10 * math.sin(v * 7.1)
    for sx, sy, amp, sig in SOURCES:
        d2 = (u - sx) ** 2 + (v - sy) ** 2
        t += amp * math.exp(-d2 / (2 * sig * sig))
    return t


def build_grid():
    g = []
    for j in range(NY + 1):
        row = []
        v = j / NY
        for i in range(NX + 1):
            row.append(temp(i / NX, v))
        g.append(row)
    return g


def march(g, lv):
    """marching squares。1本の等温線を、線分の集まりとして返す。"""
    segs = []
    dx, dy = W / NX, H / NY

    def ip(a, b, pa, pb):
        """a→b の間で lv を横切る点"""
        d = b - a
        t = 0.5 if abs(d) < 1e-9 else (lv - a) / d
        t = min(1.0, max(0.0, t))
        return (pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t)

    for j in range(NY):
        for i in range(NX):
            a, b = g[j][i], g[j][i + 1]
            c, d = g[j + 1][i + 1], g[j + 1][i]
            pa = (i * dx, j * dy)
            pb = ((i + 1) * dx, j * dy)
            pc = ((i + 1) * dx, (j + 1) * dy)
            pd = (i * dx, (j + 1) * dy)
            idx = (1 if a > lv else 0) | (2 if b > lv else 0) | (4 if c > lv else 0) | (8 if d > lv else 0)
            if idx in (0, 15):
                continue
            top = ip(a, b, pa, pb)
            right = ip(b, c, pb, pc)
            bottom = ip(d, c, pd, pc)
            left = ip(a, d, pa, pd)
            if idx in (1, 14):
                segs.append((left, top))
            elif idx in (2, 13):
                segs.append((top, right))
            elif idx in (3, 12):
                segs.append((left, right))
            elif idx in (4, 11):
                segs.append((right, bottom))
            elif idx in (6, 9):
                segs.append((top, bottom))
            elif idx in (7, 8):
                segs.append((left, bottom))
            elif idx == 5:
                segs.append((left, top)); segs.append((right, bottom))
            elif idx == 10:
                segs.append((top, right)); segs.append((left, bottom))
    return segs


def stitch(segs):
    """線分をつないで折れ線にする。つなげるほど d 属性が短くなる。
       ⚠️ 端点の照合は番号でやる。線分そのものを探すと本数の2乗で遅くなる。"""
    def key(p):
        return (round(p[0], 1), round(p[1], 1))

    ends = {}
    for i, s in enumerate(segs):
        ends.setdefault(key(s[0]), []).append(i)
        ends.setdefault(key(s[1]), []).append(i)

    used = [False] * len(segs)
    lines = []
    for i in range(len(segs)):
        if used[i]:
            continue
        used[i] = True
        line = [segs[i][0], segs[i][1]]
        for direction in (0, 1):
            while True:
                tip = line[-1] if direction == 0 else line[0]
                nxt = other = None
                for k in ends.get(key(tip), ()):
                    if used[k]:
                        continue
                    if key(segs[k][0]) == key(tip):
                        nxt, other = k, segs[k][1]
                    elif key(segs[k][1]) == key(tip):
                        nxt, other = k, segs[k][0]
                    else:
                        continue
                    break
                if nxt is None:
                    break
                used[nxt] = True
                if direction == 0:
                    line.append(other)
                else:
                    line.insert(0, other)
        if len(line) > 3:      # 短すぎる切れ端は捨てる
            lines.append(line)
    return lines


def thin(line, tol=1.1):
    """ほぼ一直線に並んだ点を間引く。marching squares は升ごとに点を置くので、
       そのまま書くと同じ形のまま ファイルだけが3倍太る。"""
    if len(line) < 3:
        return line
    out = [line[0]]
    for i in range(1, len(line) - 1):
        ax, ay = out[-1]
        bx, by = line[i]
        cx, cy = line[i + 1]
        # a→c から b までの距離
        dx, dy = cx - ax, cy - ay
        n = math.hypot(dx, dy)
        d = abs(dx * (ay - by) - (ax - bx) * dy) / n if n > 1e-9 else 0.0
        if d > tol:
            out.append(line[i])
    out.append(line[-1])
    return out


def d_of(line):
    line = thin(line)
    out = ["M%.0f %.0f" % (line[0][0], line[0][1])]
    last = (round(line[0][0]), round(line[0][1]))
    for p in line[1:]:
        q = (round(p[0]), round(p[1]))
        if q == last:
            continue
        out.append("L%d %d" % q)
        last = q
    return "".join(out)


def main():
    g = build_grid()
    flat = [x for row in g for x in row]
    lo, hi = min(flat), max(flat)
    body = []
    n_paths = 0
    for k in range(LEVELS):
        lv = lo + (hi - lo) * (k + 0.5) / LEVELS
        lines = stitch(march(g, lv))
        if not lines:
            continue
        # 4本に1本を太くする（地形図の主曲線と同じ考え）
        主 = (k % 4 == 0)
        sw = 2.4 if 主 else 1.2
        op = 0.92 if 主 else 0.5
        ds = " ".join(d_of(l) for l in lines)
        n_paths += len(lines)
        body.append(
            '<path d="%s" stroke-width="%s" opacity="%s"/>' % (ds, sw, op)
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'preserveAspectRatio="xMidYMid slice">'
        '<g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round">'
        "%s</g></svg>\n" % (W, H, "".join(body))
    )
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("%s / %.1fKB / 等温線 %d本（線 %d本）" % (
        os.path.relpath(OUT, ROOT), len(svg.encode("utf-8")) / 1024, len(body), n_paths))


if __name__ == "__main__":
    main()
