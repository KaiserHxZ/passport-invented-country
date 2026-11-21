#!/usr/bin/env python3
"""Draw the make.fun entry for the-passport-page-of-a-countr-2-20261121-0318:
one uncaptioned open passport spread for the Republic of Thalvor, an
invented Arctic research republic. All text and imagery are drawn in
code with DejaVu fonts (no AI-generated or downloaded imagery, so
nothing can garble). Output is a deterministic 1024x1024 PNG.

Country: Republic of Thalvor — a polar research state in the far north.
Capital Vinterhavn. Holder Elin Marja Korvola, glaciologist, born
14 JUN 1996 in Vinterhavn. Passport issued 12 MAR 2024, expires
11 MAR 2034. Travel history: Mirell 04-18 MAY 2024, Ostara
03 SEP 2025 - 21 FEB 2026, back in Vinterhavn 22 FEB 2026. Telling
paperwork detail: a winter-over permit for Station Nordlys that bans
travel outside the station during the polar night (15 NOV - 15 FEB).
Every stamp date falls after the issue date and before expiry.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 245, 238)
INK = (30, 38, 52)
GREY = (110, 108, 98)
RULE = (70, 72, 80)
TEAL = (32, 88, 110)      # stamp ink 1
PURPLE = (86, 70, 120)    # stamp ink 2
RED = (150, 52, 44)       # permit / paid ink
PHOTO_BG = (163, 178, 190)
PARKA = (38, 74, 92)
SKIN = (226, 188, 152)
HAIR = (58, 42, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

LX0, LX1 = 26, 500      # left (data) page
RX0, RX1 = 524, 998     # right (visa) page


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.18)


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def fit_font(draw, text, path, size, max_w):
    """Largest size <= `size` that fits max_w, never below 11."""
    while size > 11 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# ------------------------------------------------------------------ MRZ
def check_digit(s):
    vals = {}
    for i in range(10):
        vals[str(i)] = i
    for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[ch] = 10 + i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    doc = "TV4829137"
    dob, exp = "960614", "340311"
    pers = "TV4829137<<<<<"
    c1, c2, c3, c4 = (check_digit(doc), check_digit(dob),
                     check_digit(exp), check_digit(pers))
    composite_src = doc + c1 + dob + c2 + exp + c3 + pers + c4
    c5 = check_digit(composite_src)
    line2 = doc + c1 + "THV" + dob + c2 + "F" + exp + c3 + pers + c4 + c5
    name = "KORVOLA<<ELIN<MARJA"
    line1 = "P<THV" + name + "<" * (39 - len(name))
    assert len(line1) == 44 and len(line2) == 44, (line1, line2)
    return line1, line2


def draw_mrz(d, x, y, line, size=16, advance=10.0):
    fnt = font(SANS, size)
    for i, ch in enumerate(line):
        d.text((x + i * advance, y), ch, font=fnt, fill=INK)


# ------------------------------------------------------------------ emblem
def emblem(d, cx, cy, r, color=INK):
    """Circular seal: ring, five-point star over three waves."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
              outline=color, width=1)
    d.polygon(star_points(cx, cy - r * 0.18, r * 0.42, r * 0.17), fill=color)
    for k, wy in enumerate((0.28, 0.44, 0.60)):
        yy = cy + r * wy
        pts = []
        for t in range(0, 25):
            px = cx - r * 0.62 + t * (r * 1.24 / 24)
            py = yy + 3 * math.sin(t * math.pi * 2 / 8 + k)
            pts.append((px, py))
        d.line(pts, fill=color, width=2)


# ------------------------------------------------------------------ portrait
def portrait(d, x, y, w, h):
    """Stylised glaciologist in a fur-trimmed parka hood. Flat shapes."""
    d.rectangle([x, y, x + w, y + h], fill=PHOTO_BG)
    # soft light behind the head
    d.ellipse([x + w * 0.18, y + h * 0.02, x + w * 0.82, y + h * 0.62],
              fill=(178, 192, 203))
    cx = x + w / 2
    # parka shoulders
    d.polygon([(x + w * 0.06, y + h), (x + w * 0.16, y + h * 0.74),
               (cx - w * 0.20, y + h * 0.66), (cx + w * 0.20, y + h * 0.66),
               (x + w * 0.84, y + h * 0.74), (x + w * 0.94, y + h)],
              fill=PARKA)
    # parka zipper + collar
    d.line([(cx, y + h * 0.70), (cx, y + h)], fill=(22, 48, 62), width=4)
    d.polygon([(cx - w * 0.20, y + h * 0.66), (cx - w * 0.13, y + h * 0.76),
               (cx - w * 0.10, y + h), (cx - w * 0.24, y + h)],
              fill=(30, 60, 76))
    d.polygon([(cx + w * 0.20, y + h * 0.66), (cx + w * 0.13, y + h * 0.76),
               (cx + w * 0.10, y + h), (cx + w * 0.24, y + h)],
              fill=(30, 60, 76))
    # hood behind head
    d.ellipse([cx - w * 0.34, y + h * 0.10, cx + w * 0.34, y + h * 0.66],
              fill=(30, 60, 76))
    # fur trim: scalloped ring around the hood opening
    fur = (203, 194, 176)
    for i in range(13):
        ang = math.radians(200 + i * (140 / 12))
        fx = cx + math.cos(ang) * w * 0.315
        fy = y + h * 0.38 + math.sin(ang) * h * 0.26
        d.ellipse([fx - 9, fy - 9, fx + 9, fy + 9], fill=fur)
    # hair (dark, framing the face, braid over the right shoulder)
    d.ellipse([cx - w * 0.24, y + h * 0.12, cx + w * 0.24, y + h * 0.52],
              fill=HAIR)
    for i, (bx, by, br) in enumerate(((0.30, 0.60, 15), (0.315, 0.68, 14),
                                      (0.295, 0.76, 13), (0.31, 0.84, 12),
                                      (0.295, 0.92, 11))):
        d.ellipse([cx + w * bx - br, y + h * by - br,
                   cx + w * bx + br, y + h * by + br],
                  fill=HAIR if i % 2 == 0 else (70, 52, 40))
    # face
    fx0, fy0 = cx - w * 0.185, y + h * 0.17
    fx1, fy1 = cx + w * 0.185, y + h * 0.47
    d.ellipse([fx0, fy0, fx1, fy1], fill=SKIN)
    # soft cheek shading
    d.ellipse([fx0 + 6, fy0 + h * 0.16, fx0 + 34, fy0 + h * 0.26],
              fill=(218, 178, 142))
    d.ellipse([fx1 - 34, fy0 + h * 0.16, fx1 - 6, fy0 + h * 0.26],
              fill=(218, 178, 142))
    # hairline sweep over the forehead
    d.pieslice([cx - w * 0.20, y + h * 0.10, cx + w * 0.20, y + h * 0.30],
               start=180, end=360, fill=HAIR)
    # ears
    d.ellipse([fx0 - 7, y + h * 0.30, fx0 + 4, y + h * 0.38], fill=SKIN)
    d.ellipse([fx1 - 4, y + h * 0.30, fx1 + 7, y + h * 0.38], fill=SKIN)
    # brows, eyes, nose, lips — small, symmetric, neutral
    ey = y + h * 0.315
    for s in (-1, 1):
        ex = cx + s * w * 0.088
        d.arc([ex - 13, ey - 14, ex + 13, ey - 2], start=200, end=340,
              fill=(70, 50, 36), width=3)
        d.ellipse([ex - 5, ey - 3, ex + 5, ey + 3], fill=(38, 30, 26))
        d.ellipse([ex + 2, ey - 3, ex + 4, ey - 1], fill=(240, 240, 235))
    d.line([(cx, y + h * 0.33), (cx - 2, y + h * 0.40)], fill=(196, 158, 124),
           width=3)
    d.line([(cx - 12, y + h * 0.435), (cx + 12, y + h * 0.435)],
           fill=(172, 104, 96), width=3)
    d.arc([cx - 12, y + h * 0.435, cx + 12, y + h * 0.455], start=0, end=180,
          fill=(172, 104, 96), width=2)


# ------------------------------------------------------------------ stamps
def round_stamp(img, cx, cy, r, color, lines, angle=0, size=15):
    """A round border stamp, drawn on its own tile so it can be tilted."""
    tile = Image.new("RGBA", (r * 2 + 24, r * 2 + 24), (0, 0, 0, 0))
    t = ImageDraw.Draw(tile)
    c = r + 12
    col = color + (215,)
    t.ellipse([c - r, c - r, c + r, c + r], outline=col, width=4)
    t.ellipse([c - r + 9, c - r + 9, c + r - 9, c + r - 9], outline=col,
              width=2)
    t.polygon(star_points(c, c - r + 26, 9, 4), fill=col)
    fnt = font(SANS_B, size)
    total = len(lines) * int(size * 1.35)
    yy = c - total / 2 + 8
    for ln in lines:
        w = t.textlength(ln, font=fnt)
        t.text((c - w / 2, yy), ln, font=fnt, fill=col)
        yy += int(size * 1.35)
    tile = tile.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(tile, (cx - r - 12, cy - r - 12), tile)


def rect_stamp(img, x, y, w, h, color, lines, angle=0):
    """A rectangular border stamp, drawn on its own tile so it can tilt."""
    tile = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    t = ImageDraw.Draw(tile)
    col = color + (215,)
    t.rectangle([12, 12, 12 + w, 12 + h], outline=col, width=4)
    t.rectangle([18, 18, 12 + w - 6, 12 + h - 6], outline=col, width=2)
    fnt = font(SANS_B, 17)
    fnt2 = font(SANS_B, 15)
    yy = 12 + 16
    for i, ln in enumerate(lines):
        f = fnt if i != 1 else fnt2
        lw = t.textlength(ln, font=f)
        t.text((12 + (w - lw) / 2, yy), ln, font=f, fill=col)
        yy += 24 if i == 0 else 22
    tile = tile.rotate(angle, resample=Image.BICUBIC, expand=False)
    img.paste(tile, (x - 12, y - 12), tile)


# ------------------------------------------------------------------ layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # faint watermark: large ring + star behind the data page
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    wd.ellipse([60, 560, 470, 970], outline=(30, 38, 52, 14), width=10)
    wd.polygon(star_points(265, 765, 70, 28), fill=(30, 38, 52, 12))
    img.paste(wm, (0, 0), wm)
    d = ImageDraw.Draw(img)

    # centre gutter
    d.rectangle([508, 20, 516, 1004], fill=(228, 225, 214))
    d.line([(508, 20), (508, 1004)], fill=(200, 196, 184), width=1)
    d.line([(516, 20), (516, 1004)], fill=(200, 196, 184), width=1)

    # ============================================================ LEFT PAGE
    # header
    emblem(d, 263, 62, 26)
    centred(d, 263, 100, "REPUBLIC OF THALVOR", font(SERIF, 24), INK)
    centred(d, 263, 130, "PASSPORT", font(SERIF, 17), INK)
    hrule(d, LX0, LX1, 158, 2)
    hrule(d, LX0, LX1, 162, 1)

    # type / code / number row
    y = 176
    for (lab, val, fx) in (("TYPE", "P", LX0),
                           ("CODE", "THV", 190),
                           ("PASSPORT NO.", "TV4829137", 300)):
        d.text((fx, y), lab, font=font(SANS, 10), fill=GREY)
        d.text((fx, y + 14), val, font=font(SANS_B, 16), fill=INK)
    hrule(d, LX0, LX1, 218, 1)

    # portrait
    portrait(d, 44, 232, 190, 250)
    d.rectangle([44, 232, 234, 482], outline=RULE, width=2)
    # authority seal overlapping the photo's lower right corner
    round_stamp(img, 216, 448, 28, TEAL, ["THALVOR", "PASSPORT"], angle=-8,
                size=8)
    d = ImageDraw.Draw(img)

    # signature under the photo
    d.text((44, 498), "Elin Korvola", font=font(SERIF_R, 17), fill=INK)
    hrule(d, 44, 234, 524, 1)
    d.text((44, 530), "HOLDER'S SIGNATURE", font=font(SANS, 9), fill=GREY)

    # data fields, bilingual labels (English / Thalvoric)
    fields = [
        ("SURNAME — SLEKTSNAVN", "KORVOLA"),
        ("GIVEN NAMES — FORNAVN", "ELIN MARJA"),
        ("NATIONALITY — NASJONALITET", "THALVORIC"),
        ("DATE OF BIRTH — FØDSELSDATO", "14 JUN 1996"),
        ("PLACE OF BIRTH — FØDESTED", "VINTERHAVN, THALVOR"),
        ("SEX — KJØNN", "F"),
        ("DATE OF ISSUE — UTSTEDT", "12 MAR 2024"),
        ("DATE OF EXPIRY — GYLDIG TIL", "11 MAR 2034"),
        ("AUTHORITY — MYNDIGHET", "PASSPORT OFFICE"),
    ]
    fy = 232
    for lab, val in fields:
        d.text((252, fy), lab, font=font(SANS, 10), fill=GREY)
        fnt = fit_font(d, val, SANS_B, 16, LX1 - 252)
        d.text((252, fy + 14), val, font=fnt, fill=INK)
        fy += 48

    # observations box
    oy = 690
    d.rectangle([44, oy, LX1, oy + 108], outline=RULE, width=1)
    d.text((58, oy + 10), "OBSERVATIONS — MERKNADER",
           font=font(SANS_B, 11), fill=INK)
    obs = ("Holder is authorised for winter-over duty at Station "
           "Nordlys. See permit, page 4.")
    text_block(d, 58, oy + 34, wrap(d, obs, font(SANS, 13), LX1 - 72),
               font(SANS, 13), leading=18)

    hrule(d, LX0, LX1, 830, 1)
    centred(d, 263, 844,
            "THIS PASSPORT REMAINS THE PROPERTY OF THE REPUBLIC OF THALVOR",
            font(SANS, 10), GREY)

    # machine-readable zone
    line1, line2 = mrz_lines()
    draw_mrz(d, 44, 896, line1)
    draw_mrz(d, 44, 922, line2)

    d.text((LX0, 972), "Form THV-11 · 2023", font=font(SANS, 10), fill=GREY)
    d.text((LX1 - 8, 972), "3", font=font(SANS, 10), fill=GREY)

    # =========================================================== RIGHT PAGE
    cxr = (RX0 + RX1) // 2
    centred(d, cxr, 40, "VISAS", font(SERIF, 22), INK)
    centred(d, cxr, 70, "VISUM", font(SANS, 11), GREY)
    hrule(d, RX0, RX1, 96, 2)

    # winter-over permit (the telling paperwork detail)
    px0, py0, px1, py1 = 540, 112, 982, 322
    d.rectangle([px0, py0, px1, py1], outline=RED, width=2)
    d.rectangle([px0 + 6, py0 + 6, px1 - 6, py1 - 6], outline=RED, width=1)
    d.text((px0 + 18, py0 + 14), "WINTER-OVER PERMIT",
           font=font(SANS_B, 19), fill=RED)
    d.text((px0 + 18, py0 + 42), "No. WN-2025-114  ·  STATION NORDLYS",
           font=font(SANS_B, 13), fill=RED)
    hrule(d, px0 + 18, px1 - 18, py0 + 70, 1, fill=RED)
    permit = [
        "Issued 15 AUG 2025 at Vinterhavn.",
        "Holder may reside at Station Nordlys",
        "from 01 OCT 2025 to 30 APR 2026.",
        "No travel outside the station",
        "15 NOV – 15 FEB (polar night).",
    ]
    text_block(d, px0 + 18, py0 + 82, permit, font(SANS, 13.5), fill=INK,
               leading=19)
    d.text((px0 + 18, py1 - 30), "Fee: AURORA LEVY 40 KR — PAID",
           font=font(SANS_B, 13), fill=RED)
    # PAID stamp, tilted, overlapping the permit box
    rect_stamp(img, 836, 218, 128, 52, RED, ["PAID"], angle=-10)
    d = ImageDraw.Draw(img)

    # arrival / departure stamps: two trips, all dates after issue
    stamps = [
        (640, 448, 92, TEAL, ["ARRIVAL", "MIRELL", "04 MAY 2024"], -5),
        (880, 448, 92, TEAL, ["DEPARTURE", "MIRELL", "18 MAY 2024"], 6),
        (640, 648, 92, PURPLE, ["ARRIVAL", "OSTARA", "03 SEP 2025"], 4),
        (880, 648, 92, PURPLE, ["DEPARTURE", "OSTARA", "21 FEB 2026"], -6),
    ]
    for (sx, sy, sr, col, lines, ang) in stamps:
        round_stamp(img, sx, sy, sr, col, lines, angle=ang, size=14)
    d = ImageDraw.Draw(img)

    # Thalvor arrival stamp on return from Ostara
    rect_stamp(img, 596, 800, 330, 92, (150, 52, 44),
               ["ARRIVAL", "VINTERHAVN · THALVOR", "22 FEB 2026"], angle=-2)
    d = ImageDraw.Draw(img)

    d.text((RX0, 972), "PAGE 4", font=font(SANS, 10), fill=GREY)
    d.text((RX1 - 8, 972), "4", font=font(SANS, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)
    print("MRZ1:", line1)
    print("MRZ2:", line2)


if __name__ == "__main__":
    main()
