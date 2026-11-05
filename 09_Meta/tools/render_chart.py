#!/usr/bin/env python3
"""Рендер свечи + уровни -> PNG (практика разметки, REPLIKA_*).

Источник — публичные спотовые данные Bybit (v5 kline), только чтение.
Уровни — горизонтальные линии с подписями; якоря 0/1 — пунктир.

Запуск:
    python3 render_chart.py SYMBOL ИНТЕРВАЛ КОЛИЧЕСТВО --out FILE.png \
        [--level ЦЕНА:ПОДПИСЬ ...] [--anchor ЦЕНА:ПОДПИСЬ ...]
Пример:
    python3 render_chart.py TRUMPUSDT D 300 --out /tmp/opencode/trump.png \
        --level 16432:хай_26.04 --anchor 1253:0_дно
"""
import json
import sys
import urllib.request
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
M_L, M_R, M_T, M_B = 40, 150, 60, 40
UP, DN, BG, FG = "#26a69a", "#ef5350", "#131722", "#b2b5be"


def fetch(symbol, interval, limit):
    url = (f"https://api.bybit.com/v5/market/kline?category=spot"
           f"&symbol={symbol}&interval={interval}&limit={min(limit, 1000)}")
    with urllib.request.urlopen(url, timeout=20) as r:
        d = json.load(r)
    rows = d["result"]["list"]  # newest first
    rows = list(reversed(rows))
    return [(int(t), float(o), float(h), float(l), float(c))
            for t, o, h, l, c, *_ in rows]


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    args = sys.argv[1:]
    out = args[args.index("--out") + 1] if "--out" in args else "/tmp/opencode/chart.png"
    levels = [a for a in args if a.startswith("--level")]
    lvl = [args[args.index(l) + 1] for l in levels]
    anchors = [a for a in args if a.startswith("--anchor")]
    anc = [args[args.index(a) + 1] for a in anchors]
    pos = [a for a in args if not a.startswith("--")]
    symbol, interval, limit = pos[0], pos[1], int(pos[2])
    kl = fetch(symbol, interval, limit)
    if not kl:
        sys.exit("нет данных")
    lo = min(k[3] for k in kl)
    hi = max(k[2] for k in kl)
    pad = (hi - lo) * 0.05 or hi * 0.01
    lo, hi = lo - pad, hi + pad
    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)
    f = font(20)
    fb = font(24)

    def y(p):
        return M_T + (hi - p) / (hi - lo) * (H - M_T - M_B)

    cw = (W - M_L - M_R) / len(kl)
    dr.text((M_L, 14), f"{symbol} {interval} Bybit spot  {len(kl)} баров"
            f"  {kl[0][0]}..{kl[-1][0]}", fill=FG, font=fb)
    for i, (t, o, h, l, c) in enumerate(kl):
        x = M_L + i * cw
        col = UP if c >= o else DN
        xc = x + cw / 2
        dr.line([(xc, y(h)), (xc, y(l))], fill=col, width=1)
        top, bot = y(max(o, c)), y(min(o, c))
        dr.rectangle([x + 1, top, x + max(1, cw - 2), max(bot, top + 1)],
                     fill=col)
    for spec in lvl:
        p, _, lab = spec.partition(":")
        p = float(p)
        if lo <= p <= hi:
            dr.line([(M_L, y(p)), (W - M_R + 40, y(p))], fill="#f0b90b", width=2)
            dr.text((W - M_R + 45, y(p) - 10), lab or str(p), fill="#f0b90b", font=f)
    for spec in anc:
        p, _, lab = spec.partition(":")
        p = float(p)
        if lo <= p <= hi:
            for xx in range(M_L, W - M_R, 8):
                dr.line([(xx, y(p)), (min(xx + 4, W - M_R), y(p))],
                        fill="#5b9cf6", width=2)
            dr.text((W - M_R + 45, y(p) - 10), lab or str(p), fill="#5b9cf6", font=f)
    for frac in (4, 2):  # сетка-ориентир по средней
        p = lo + (hi - lo) * frac / 8
        dr.line([(M_L, y(p)), (W - M_R, y(p))], fill="#2a2e39", width=1)
    img.save(out)
    print(out, f"bars={len(kl)} lo={lo:.6g} hi={hi:.6g} last_close={kl[-1][4]}")


main()
