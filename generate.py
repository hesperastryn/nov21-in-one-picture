#!/usr/bin/env python3
"""Draw the front page for the make.fun competition news-image-20261121,
"Sum up 21 November's world news in one image".

A newspaper-style front page drawn procedurally with PIL: a huge date
header over six captioned panels covering the defining stories of
Saturday 21 November 2026, plus an "also today" ticker along the bottom.

Stories (reported 21 Nov 2026; One Turn News, AP, NYT, SCMP):
  1. Russia's biggest barrage of the war: 400+ drones and 110 missiles
     hit Ukraine overnight, killing at least eight in Kyiv; two Russian
     missiles and a suspected drone came down in Poland, which PM Tusk
     called a deliberate provocation; NATO condemned the violation.
  2. An AI and chip sell-off sends US stocks down 3.7% on Friday,
     pushing the S&P 500 and the Dow into correction territory.
  3. A trial of the pill daraxonrasib makes pancreatic-cancer tumours
     undetectable on scans in one in twelve patients.
  4. PM Andy Burnham and EU leaders sign the biggest post-Brexit
     agreements in Brussels: food exports, carbon markets, youth
     mobility.
  5. COP31 in Antalya runs past its deadline into overtime as nearly
     200 nations stay deadlocked over fossil fuels.
  6. An Anthropic researcher says Claude has solved the Riemann
     hypothesis, the 160-year-old Millennium riddle of mathematics.
Ticker: Gen Z protests spread across 25 European countries; Iran says
it downed a US MQ-9 over the Strait of Hormuz; Lewis Pugh swims the
Strait of Hormuz for war-hit wildlife; Spain heads to a 29 November
election; Mongolia's president resigns.

Writes entry.png (1024x1024) beside this file. Deterministic.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

NAVY = (13, 21, 43)
GOLD = (233, 186, 82)
PAPER = (243, 239, 229)
INK = (17, 19, 25)
CAP_BG = (9, 13, 26)
CAP_SUB = (198, 207, 226)
WHITE = (250, 250, 248)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_w):
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, f, fill, tracking=10):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- panels

def panel_barrage(d, x, y, w, h):
    """Night sky, skyline, a storm of trails; Poland flag at the border."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    rng = [(37 * i + 11) % 97 / 97.0 for i in range(60)]
    for i in range(28):  # stars
        sx = x + 8 + rng[i] * (w - 16)
        sy = y + 6 + rng[i + 20] * h * 0.4
        d.point((sx, sy), fill=(200, 208, 235))
    # incoming trails
    for i in range(16):
        fx = x + 14 + rng[i + 5] * (w - 40)
        fy = y + h * 0.52 + rng[i + 30] * h * 0.22
        txp = fx - 26 - rng[i + 40] * 30
        d.line([txp, y + 8, fx, fy], fill=(255, 176, 92), width=2)
        d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 214, 130))
    for i in range(7):  # drone silhouettes
        dx = x + 20 + rng[i + 12] * (w - 50)
        dy = y + 16 + rng[i + 44] * h * 0.2
        d.line([dx - 9, dy, dx + 9, dy], fill=(160, 170, 200), width=2)
        d.line([dx, dy - 4, dx, dy + 4], fill=(160, 170, 200), width=2)
    # skyline
    base = y + h
    heights = [0.30, 0.42, 0.24, 0.5, 0.34, 0.44, 0.27, 0.38, 0.31]
    bx = x
    for i, hf in enumerate(heights):
        bw = w / len(heights)
        bh = h * hf
        d.rectangle([bx, base - bh, bx + bw - 2, base], fill=(4, 6, 14))
        for wy in range(int(base - bh) + 8, int(base) - 8, 14):
            if (i * 7 + wy) % 3:
                d.point((bx + 5 + (wy % 11), wy), fill=(240, 205, 110))
        bx += bw
    # explosions
    for cx, cy, r in [(x + w * 0.24, y + h * 0.66, 15),
                      (x + w * 0.58, y + h * 0.6, 11),
                      (x + w * 0.8, y + h * 0.7, 13)]:
        star(d, cx, cy, r, (255, 140, 60))
        star(d, cx, cy, r * 0.55, (255, 214, 130))
    # Poland flag marker, right edge
    fx, fy = x + w - 52, y + 12
    d.line([fx, fy, fx, fy + 44], fill=(220, 224, 235), width=2)
    d.rectangle([fx + 2, fy, fx + 38, fy + 11], fill=(245, 245, 245))
    d.rectangle([fx + 2, fy + 11, fx + 38, fy + 22], fill=(214, 40, 57))


def panel_rout(d, x, y, w, h):
    """Falling red chart and a cracked chip."""
    d.rectangle([x, y, x + w, y + h], fill=(26, 10, 14))
    for gx in range(x + 20, x + w - 10, 34):  # grid
        d.line([gx, y + 12, gx, y + h - 46], fill=(64, 30, 36), width=1)
    for gy in range(y + 16, y + h - 40, 30):
        d.line([x + 12, gy, x + w - 12, gy], fill=(64, 30, 36), width=1)
    pts = [(x + 16, y + h * 0.2), (x + w * 0.3, y + h * 0.3),
           (x + w * 0.44, y + h * 0.26), (x + w * 0.6, y + h * 0.48),
           (x + w * 0.74, y + h * 0.44), (x + w * 0.94, y + h * 0.72)]
    d.line(pts, fill=(255, 84, 84), width=5, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - 20, ay - 4), (ax - 6, ay - 18)],
              fill=(255, 84, 84))
    f = fit_font(d, "-3.7%", BOLD, 54, w * 0.52)
    d.text((x + 16, y + h - 52), "-3.7%", font=f, fill=(255, 120, 120))
    # cracked chip
    cx, cy, s = x + w - 74, y + 26, 56
    d.rounded_rectangle([cx, cy, cx + s, cy + s], 8, outline=(140, 200, 255),
                        width=3)
    for px in range(cx + 8, cx + s, 12):
        d.line([px, cy - 7, px, cy], fill=(140, 200, 255), width=2)
        d.line([px, cy + s, px, cy + s + 7], fill=(140, 200, 255), width=2)
    crack = [(cx + 10, cy + 6), (cx + 26, cy + 22), (cx + 20, cy + 34),
             (cx + 36, cy + 50)]
    d.line(crack, fill=(255, 84, 84), width=3)
    f2 = fit_font(d, "AI", BOLD, 20, 30)
    d.text((cx + s / 2 - d.textlength("AI", font=f2) / 2, cy + s + 12),
           "AI", font=f2, fill=(140, 200, 255))


def panel_pill(img, d, x, y, w, h):
    """A capsule, a fading tumour scan, and the 1-in-12 figure."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 44, 48))
    # capsule, tilted
    cap = Image.new("RGBA", (170, 74), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cap)
    cd.rounded_rectangle([2, 2, 168, 72], 34, fill=(238, 242, 245),
                         outline=(20, 30, 34), width=3)
    cd.rounded_rectangle([86, 2, 168, 72], 34, fill=(64, 190, 178))
    cd.rectangle([86, 4, 120, 70], fill=(64, 190, 178))
    cap = cap.rotate(24, expand=True, resample=Image.BILINEAR)
    img.paste(cap, (int(x + 12), int(y + 16)), cap)
    # scan box with a fading tumour
    sx, sy, ss = x + w - 118, y + 20, 96
    d.rectangle([sx, sy, sx + ss, sy + ss], outline=(150, 230, 220), width=2)
    for r, col in [(30, (70, 90, 92)), (21, (96, 116, 118)),
                   (13, (128, 148, 150))]:
        d.ellipse([sx + ss / 2 - r, sy + ss / 2 - r,
                   sx + ss / 2 + r, sy + ss / 2 + r], outline=col, width=2)
    d.line([sx + 14, sy + 14, sx + ss - 14, sy + ss - 14],
           fill=(120, 235, 220), width=2)
    f = fit_font(d, "1 in 12", BOLD, 52, w * 0.6)
    d.text((x + 16, y + h - 58), "1 in 12", font=f, fill=(150, 240, 228))
    f2 = fit_font(d, "tumours gone", REG, 19, w * 0.4)
    d.text((sx - 16, sy + ss + 10), "tumours gone", font=f2,
           fill=(190, 235, 230))


def panel_ukeu(d, x, y, w, h):
    """Union Jack and EU flag side by side over a signing line."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 52))
    fw, fh = (w - 48) // 2, int(h * 0.52)
    ux, uy = x + 16, y + 18
    # Union Jack (simplified)
    d.rectangle([ux, uy, ux + fw, uy + fh], fill=(28, 52, 128))
    d.line([ux, uy, ux + fw, uy + fh], fill=WHITE, width=13)
    d.line([ux + fw, uy, ux, uy + fh], fill=WHITE, width=13)
    d.line([ux, uy, ux + fw, uy + fh], fill=(200, 30, 50), width=5)
    d.line([ux + fw, uy, ux, uy + fh], fill=(200, 30, 50), width=5)
    d.rectangle([ux + fw / 2 - 13, uy, ux + fw / 2 + 13, uy + fh], fill=WHITE)
    d.rectangle([ux, uy + fh / 2 - 13, ux + fw, uy + fh / 2 + 13], fill=WHITE)
    d.rectangle([ux + fw / 2 - 8, uy, ux + fw / 2 + 8, uy + fh],
                fill=(200, 30, 50))
    d.rectangle([ux, uy + fh / 2 - 8, ux + fw, uy + fh / 2 + 8],
                fill=(200, 30, 50))
    # EU flag
    ex, ey = ux + fw + 16, uy
    d.rectangle([ex, ey, ex + fw, ey + fh], fill=(20, 44, 140))
    ccx, ccy, rr = ex + fw / 2, ey + fh / 2, fh * 0.32
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        star(d, ccx + rr * math.cos(ang), ccy + rr * math.sin(ang), 7,
             (255, 205, 40))
    # signing line + pen
    ly = y + h - 40
    d.line([x + 24, ly, x + w - 24, ly], fill=(210, 216, 230), width=2)
    d.line([x + 30, ly - 2, x + 74, ly - 14], fill=GOLD, width=3)
    d.line([x + 74, ly - 14, x + 96, ly - 3], fill=GOLD, width=3)
    px, py = x + w - 92, ly - 34
    d.line([px, py + 26, px + 34, py], fill=(235, 238, 245), width=5)
    d.polygon([(px + 34, py), (px + 44, py + 2), (px + 36, py + 10)],
              fill=GOLD)


def panel_cop(d, x, y, w, h):
    """Globe, thermometer, factory smoke and an overtime clock."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 20))
    gx, gy, gr = x + w * 0.34, y + h * 0.44, h * 0.3
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 110, 160))
    for dx, dy, rw, rh in [(-0.45, -0.4, 0.5, 0.34), (0.1, -0.55, 0.42, 0.3),
                           (-0.2, 0.12, 0.55, 0.4), (0.42, 0.3, 0.3, 0.3)]:
        d.ellipse([gx + dx * gr, gy + dy * gr, gx + (dx + rw) * gr,
                   gy + (dy + rh) * gr], fill=(74, 148, 84))
    # thermometer
    tx = x + w - 52
    d.rounded_rectangle([tx, y + 18, tx + 16, y + h - 56], 8,
                        outline=(235, 238, 240), width=3)
    d.rectangle([tx + 4, y + 44, tx + 12, y + h - 62], fill=(232, 70, 60))
    d.ellipse([tx - 6, y + h - 62, tx + 22, y + h - 34], fill=(232, 70, 60))
    # factory + smoke
    fx, fy = x + 18, y + h - 52
    d.rectangle([fx, fy - 26, fx + 84, fy], fill=(24, 26, 30))
    d.polygon([(fx + 8, fy - 26), (fx + 22, fy - 62), (fx + 36, fy - 26)],
              fill=(24, 26, 30))
    d.polygon([(fx + 44, fy - 26), (fx + 58, fy - 62), (fx + 72, fy - 26)],
              fill=(24, 26, 30))
    for i, (sx, sy, sr) in enumerate([(fx + 22, fy - 74, 11),
                                      (fx + 34, fy - 92, 15),
                                      (fx + 58, fy - 76, 12)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                  fill=(150, 152, 150))
    # clock past twelve
    kx, ky, kr = x + w - 116, y + 46, 24
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], outline=(245, 240, 220),
              width=3)
    d.line([kx, ky, kx, ky - kr + 6], fill=(245, 240, 220), width=3)
    d.line([kx, ky, kx + 12, ky + 8], fill=(245, 240, 220), width=3)


def panel_riemann(d, x, y, w, h):
    """Chalkboard: the critical line, its zeros, and a gold tick."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 34, 28))
    f = fit_font(d, "ζ(s) = 0", SERIF, 40, w * 0.62)
    d.text((x + 16, y + 12), "ζ(s) = 0", font=f, fill=(238, 244, 238))
    # critical line with zeros
    lx = x + w * 0.3
    d.line([lx, y + 66, lx, y + h - 18], fill=(240, 240, 230), width=2)
    d.line([x + 16, y + h - 18, x + w - 16, y + h - 18],
           fill=(240, 240, 230), width=2)
    for i, fy_ in enumerate([0.16, 0.38, 0.55, 0.74, 0.88]):
        zy = y + 66 + fy_ * (h - 92)
        d.ellipse([lx - 5, zy - 5, lx + 5, zy + 5], fill=GOLD)
    f2 = fit_font(d, "Re(s) = 1/2", REG, 19, w * 0.4)
    d.text((lx + 12, y + h - 40), "Re(s) = 1/2", font=f2,
           fill=(210, 226, 214))
    f3 = fit_font(d, "160", BOLD, 58, w * 0.34)
    d.text((x + w - 108, y + 74), "160", font=f3, fill=(238, 244, 238))
    f4 = fit_font(d, "years", REG, 22, w * 0.3)
    d.text((x + w - 104, y + 134), "years", font=f4, fill=(210, 226, 214))
    # gold tick
    tx, ty = x + w - 96, y + h - 78
    d.line([tx, ty + 16, tx + 16, ty + 32], fill=GOLD, width=7)
    d.line([tx + 16, ty + 32, tx + 46, ty], fill=GOLD, width=7)


PANELS = [
    (panel_barrage, "RUSSIA'S BIGGEST BARRAGE",
     "400+ drones & 110 missiles hit Ukraine; two land in Poland"),
    (panel_rout, "AI ROUT: STOCKS IN CORRECTION",
     "S&P 500 falls 3.7% as the AI & chip sell-off deepens"),
    (panel_pill, "CANCER PILL BREAKTHROUGH",
     "Trial pill leaves tumours undetectable in 1 in 12 patients"),
    (panel_ukeu, "UK & EU SIGN POST-BREXIT RESET",
     "Biggest deals since Brexit: food, carbon, youth mobility"),
    (panel_cop, "COP31 RUNS INTO OVERTIME",
     "Nearly 200 nations deadlocked over fossil fuels in Antalya"),
    (panel_riemann, "CLAUDE 'SOLVES' MATHS' RIDDLE",
     "Anthropic researcher claims Riemann hypothesis is proved"),
]

TICKER = ("ALSO TODAY:  Gen Z protests in 25 European countries  •  "
          "Iran says it downed a US MQ-9 over Hormuz  •  Lewis Pugh "
          "swims the Strait of Hormuz  •  Spain heads to a 29 Nov "
          "election  •  Mongolia's president resigns")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 158], fill=NAVY)
    f_kick = font(BOLD, 21)
    tracked(d, (30, 20), "THE DAY IN ONE PICTURE", f_kick, GOLD, 8)
    f_day = fit_font(d, "SATURDAY", BOLD, 30, 260)
    tw = d.textlength("SATURDAY", font=f_day)
    d.text((W - 30 - tw, 16), "SATURDAY", font=f_day, fill=WHITE)
    f_date = fit_font(d, "21 NOVEMBER 2026", SERIF, 84, W - 60)
    d.text((28, 52), "21 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.rectangle([0, 152, W, 158], fill=GOLD)

    # panel grid
    mx, gap = 26, 14
    pw = (W - 2 * mx - 2 * gap) // 3
    ph = 368
    top = 172
    for i, (draw_fn, head, sub) in enumerate(PANELS):
        col, row = i % 3, i // 3
        px = mx + col * (pw + gap)
        py = top + row * (ph + gap)
        cap_h = 96
        d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255))
        if draw_fn is panel_pill:
            draw_fn(img, d, px, py, pw, ph - cap_h)
        else:
            draw_fn(d, px, py, pw, ph - cap_h)
        cy = py + ph - cap_h
        d.rectangle([px, cy, px + pw, py + ph], fill=CAP_BG)
        fh = fit_font(d, head, BOLD, 25, pw - 20)
        lines = wrap(d, head, fh, pw - 20)
        if len(lines) > 1:
            fh = fit_font(d, head, BOLD, 21, pw - 20)
            lines = wrap(d, head, fh, pw - 20)
        ly = cy + 9
        for ln in lines[:2]:
            d.text((px + 10, ly), ln, font=fh, fill=WHITE)
            ly += fh.size + 3
        fs = font(REG, 17)
        for ln in wrap(d, sub, fs, pw - 20)[:2]:
            d.text((px + 10, ly), ln, font=fs, fill=CAP_SUB)
            ly += 21

    # ticker (shrink the font until the whole ticker fits on two lines)
    ty = top + 2 * ph + gap + 12
    d.rectangle([0, ty, W, H], fill=NAVY)
    tsize = 20
    while tsize > 12:
        ft = font(REG, tsize)
        lines = wrap(d, TICKER, ft, W - 52)
        if len(lines) <= 2:
            break
        tsize -= 1
    ly = ty + 12
    for ln in lines[:2]:
        d.text((26, ly), ln, font=ft, fill=(226, 231, 242))
        ly += tsize + 6

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
