#!/usr/bin/env python3
"""NI23 v7 build tool: renders entry.png (1024x1024) for Monday 23 November 2026.

21 stories: 3 larges + 10 mediums + 8 briefs (briefs cut 17 -> 8 for r1 legibility).

Fixed pixel grid (bands + columns). Text that does not fit is a recorded
warning and the build exits non-zero -- text is shortened, bands never move.
Scenes are painted on their own sub-image and pasted, so nothing can leak.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

import data

FD = "/usr/share/fonts/truetype/dejavu/"
W = H = 1024
PAGE = (247, 242, 232)
INK = (24, 30, 48)
NAVY = (22, 38, 74)
GREY = (96, 96, 104)
LINE = (201, 195, 181)
RED = (176, 32, 40)
YELLOW = (255, 214, 110)
REGION_COL = {"ASIA": (46, 109, 164), "EUROPE": (74, 124, 89), "AMERICAS": (138, 109, 28),
              "MIDDLE EAST": (123, 74, 142), "AFRICA": (192, 96, 58), "OCEANIA": (42, 138, 138),
              "GLOBAL": (102, 102, 102)}
TAG_COL = {"OFFICIAL": (31, 63, 168), "CONFIRMED": (14, 122, 106), "REPORTED": (181, 83, 10)}

_fonts = {}


def F(kind, size):
    key = (kind, size)
    if key not in _fonts:
        name = {"sb": "DejaVuSans-Bold.ttf", "s": "DejaVuSans.ttf",
                "rb": "DejaVuSerif-Bold.ttf", "r": "DejaVuSerif.ttf"}[kind]
        _fonts[key] = ImageFont.truetype(FD + name, size)
    return _fonts[key]


class Reg:
    def __init__(self):
        self.items, self.warnings, self.meta, self.texts = [], [], {}, []

    def add(self, band, kind, bbox, text=""):
        self.items.append(dict(band=band, kind=kind, bbox=tuple(int(v) for v in bbox), text=text))
        if text:
            self.texts.append(text)

    def warn(self, msg):
        self.warnings.append(msg)


def T(d, reg, band, xy, s, font, fill, anchor="la", maxw=None):
    bb = d.textbbox(xy, s, font=font, anchor=anchor)
    if maxw is not None and bb[2] - bb[0] > maxw:
        reg.warn(f"text too wide ({bb[2]-bb[0]}>{maxw}): {s!r}")
    d.text(xy, s, font=font, fill=fill, anchor=anchor)
    reg.add(band, "text", bb, s)
    return bb


def wrap(reg, font, text, maxw, maxlines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if font.getlength(w) > maxw:
                reg.warn(f"word too wide: {w!r}")
    if cur:
        lines.append(cur)
    if len(lines) > maxlines:
        reg.warn(f"{len(lines)} lines > {maxlines}: {text!r}")
        lines = lines[:maxlines]
    return lines


def rect(d, reg, band, box, fill=None, outline=None, kind="rect"):
    d.rectangle(box, fill=fill, outline=outline)
    reg.add(band, kind, (box[0], box[1], box[2] + 1, box[3] + 1))


def chip(d, reg, band, x, y, s, fill, size=9, pad=4, h=12):
    f = F("sb", size)
    w = int(f.getlength(s)) + 2 * pad
    rect(d, reg, band, (x, y, x + w - 1, y + h - 1), fill=fill, kind="chip")
    T(d, reg, band, (x + w / 2, y + h / 2 + 0.5), s, f, (255, 255, 255), anchor="mm")
    return w


def num_dot(d, reg, band, cx, cy, n, r=8, size=10, fill=RED):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=(255, 255, 255))
    reg.add(band, "dot", (cx - r, cy - r, cx + r + 1, cy + r + 1))
    T(d, reg, band, (cx, cy + 0.5), str(n), F("sb", size), (255, 255, 255), anchor="mm")


# ------------------------------------------------------------------ scenes
# Every scene paints on its own (w, h) image, so nothing can leave the box.

def sc_belgium(d, w, h):
    d.rectangle((0, 0, w, h), fill=(120, 170, 220))
    d.rectangle((0, int(h * .78), w, h), fill=(86, 90, 100))
    for i in range(0, w, 22):
        d.rectangle((i, int(h * .88), i + 10, int(h * .9)), fill=(235, 235, 235))
    d.ellipse((w * .55, h * .1, w * .55 + h * .3, h * .1 + h * .3), fill=YELLOW)
    d.ellipse((w * .58, h * .38, w * .84, h * .56), fill=(250, 250, 250))
    d.polygon([(w * .80, h * .40), (w * .88, h * .22), (w * .90, h * .22), (w * .86, h * .50)], fill=(200, 50, 50))
    d.polygon([(w * .62, h * .5), (w * .70, h * .5), (w * .66, h * .68)], fill=(215, 215, 220))
    d.rectangle((w * .92, h * .35, w * .96, h * .78), fill=(70, 70, 80))
    d.rectangle((w * .90, h * .28, w * .98, h * .38), fill=(235, 190, 70))


def sc_nvidia(d, w, h):
    d.rectangle((0, 0, w, h), fill=(16, 28, 16))
    s = h * .46
    cx, cy = w * .72, h * .52
    for k in range(-2, 3):
        d.line((cx + k * s * .3, cy - s * .8, cx + k * s * .3, cy - s * .55), fill=(150, 150, 150), width=2)
        d.line((cx + k * s * .3, cy + s * .55, cx + k * s * .3, cy + s * .8), fill=(150, 150, 150), width=2)
    d.rectangle((cx - s * .6, cy - s * .55, cx + s * .6, cy + s * .55), fill=(118, 185, 0))
    d.rectangle((cx - s * .35, cy - s * .3, cx + s * .35, cy + s * .3), fill=(24, 40, 12))
    d.polygon([(cx, cy - s * .22), (cx + s * .22, cy + s * .1), (cx - s * .22, cy + s * .1)], fill=(118, 185, 0))
    d.rectangle((cx + s * .85, cy - s * .7, cx + s * .95, cy + s * .7), fill=(118, 185, 0))


def sc_wallst(d, w, h):
    d.rectangle((0, 0, w, h), fill=(20, 36, 70))
    base = h * .92
    for i, (hh, x) in enumerate([(.30, .50), (.42, .56), (.34, .62), (.58, .68), (.74, .74), (.88, .80)]):
        c = (60, 190, 110)
        d.rectangle((w * x, base - h * hh, w * x + w * .035, base), fill=c)
        d.line((w * x + w * .0175, base - h * hh - h * .1, w * x + w * .0175, base + 0), fill=c)
    d.polygon([(w * .88, h * .3), (w * .94, h * .3), (w * .91, h * .12)], fill=(60, 190, 110))
    d.rectangle((w * .88, h * .3, w * .94, h * .6), fill=(60, 190, 110))
    d.rectangle((0, base, w, h), fill=(40, 60, 100))


def sc_kospi(d, w, h):
    d.rectangle((0, 0, w, h), fill=(34, 36, 44))
    pts = [(.45, .15), (.55, .30), (.63, .26), (.72, .52), (.80, .48), (.90, .85)]
    for i, (x, y) in enumerate(pts):
        d.rectangle((w * x - 3, h * y, w * x + 3, h * (y + .22)), fill=(210, 70, 60))
    d.line([(w * x, h * y) for x, y in pts], fill=(255, 120, 100), width=2)
    d.polygon([(w * .95, h * .95), (w * .89, h * .78), (w * 1.0, h * .8)], fill=(255, 120, 100))


def sc_benghazi(d, w, h):
    d.rectangle((0, 0, w, h), fill=(150, 200, 235))
    d.rectangle((0, int(h * .62), w, h), fill=(40, 90, 160))
    d.ellipse((w * .1, h * .1, w * .1 + h * .22, h * .1 + h * .22), fill=YELLOW)
    d.polygon([(w * .52, h * .62), (w * .92, h * .62), (w * .86, h * .80), (w * .58, h * .80)], fill=(60, 60, 70))
    d.rectangle((w * .62, h * .46, w * .80, h * .62), fill=(210, 210, 215))
    d.rectangle((w * .70, h * .30, w * .72, h * .46), fill=(80, 80, 80))
    d.rectangle((w * .74, h * .22, w * .94, h * .38), fill=(90, 170, 230))
    d.ellipse((w * .80, h * .26, w * .88, h * .34), outline=(255, 255, 255))
    d.line((w * .43, h * .62, w * .43, h * .2), fill=(70, 70, 70), width=2)
    d.line((w * .43, h * .2, w * .53, h * .2), fill=(70, 70, 70), width=2)


def sc_cop(d, w, h):
    d.rectangle((0, 0, w, h), fill=(20, 100, 110))
    cx = w * .78
    d.rectangle((cx - 4, h * .12, cx + 4, h * .70), fill=(235, 235, 235))
    d.ellipse((cx - 11, h * .62, cx + 11, h * .92), fill=(220, 50, 50))
    d.rectangle((cx - 3, h * .30, cx + 3, h * .75), fill=(220, 50, 50))
    for k in range(5):
        d.line((cx + 7, h * (.18 + k * .1), cx + 14, h * (.18 + k * .1)), fill=(235, 235, 235))
    d.ellipse((w * .88, h * .12, w * .88 + h * .3, h * .12 + h * .3), fill=YELLOW)


def sc_train(d, w, h):
    d.rectangle((0, 0, w, h), fill=(140, 190, 230))
    d.rectangle((0, h * .78, w, h), fill=(90, 70, 50))
    d.line((0, h * .78, w, h * .78), fill=(60, 60, 60), width=2)
    d.rectangle((w * .50, h * .32, w * .98, h * .72), fill=(40, 70, 150))
    d.rectangle((w * .50, h * .52, w * .98, h * .58), fill=(235, 235, 235))
    d.rectangle((w * .84, h * .20, w * .98, h * .34), fill=(40, 70, 150))
    for x in (.58, .70, .84):
        d.ellipse((w * x - 4, h * .66, w * x + 6, h * .84), fill=(30, 30, 30))
    d.rectangle((w * .54, h * .38, w * .60, h * .48), fill=(250, 240, 180))


def sc_gaza(d, w, h):
    d.rectangle((0, 0, w, h), fill=(58, 48, 82))
    d.ellipse((w * .1, h * .12, w * .1 + h * .22, h * .12 + h * .22), fill=(240, 235, 200))
    for i, (x, hh) in enumerate([(.52, .45), (.60, .60), (.70, .38), (.80, .52), (.90, .34)]):
        d.rectangle((w * x, h * (1 - hh), w * x + w * .075, h), fill=(40, 40, 54))
        d.rectangle((w * x + 3, h * (1 - hh) + 4, w * x + 6, h * (1 - hh) + 8), fill=(250, 210, 90))
    d.ellipse((w * .66, h * .02, w * .82, h * .30), fill=(120, 120, 128))
    d.polygon([(w * .74, h * .30), (w * .70, h * .5), (w * .78, h * .5)], fill=(240, 130, 40))


def sc_cricket(d, w, h):
    d.rectangle((0, 0, w, h), fill=(86, 150, 80))
    d.rectangle((0, h * .55, w, h * .8), fill=(214, 190, 130))
    for x in (.70, .76, .82):
        d.rectangle((w * x, h * .18, w * x + 3, h * .66), fill=(250, 230, 150))
    d.line((w * .70, h * .18, w * .85, h * .18), fill=(250, 230, 150), width=2)
    d.polygon([(w * .92, h * .15), (w * .96, h * .15), (w * .90, h * .75), (w * .86, h * .75)], fill=(180, 120, 60))
    d.ellipse((w * .58, h * .68, w * .58 + 8, h * .68 + 8), fill=(200, 40, 40))


def sc_oil(d, w, h):
    d.rectangle((0, 0, w, h), fill=(44, 46, 56))
    d.rectangle((w * .64, h * .35, w * .78, h * .90), fill=(130, 134, 144))
    d.rectangle((w * .60, h * .30, w * .82, h * .38), fill=(160, 164, 172))
    d.rectangle((w * .86, h * .55, w * .98, h * .90), fill=(190, 194, 202))
    d.ellipse((w * .86, h * .50, w * .98, h * .62), fill=(214, 218, 226))
    d.polygon([(w * .71, h * .02), (w * .66, h * .28), (w * .76, h * .28)], fill=(245, 140, 40))
    d.polygon([(w * .71, h * .10), (w * .68, h * .28), (w * .74, h * .28)], fill=(255, 220, 90))
    d.rectangle((0, h * .9, w, h), fill=(30, 30, 36))


def sc_fire(d, w, h):
    d.rectangle((0, 0, w, h), fill=(48, 40, 48))
    d.rectangle((w * .50, h * .52, w * .94, h), fill=(110, 112, 124))
    for x in (.54, .66, .78):
        d.polygon([(w * x, h * .52), (w * x + w * .06, h * .30), (w * x + w * .12, h * .52)], fill=(130, 132, 144))
    d.rectangle((w * .88, h * .22, w * .93, h * .52), fill=(90, 90, 100))
    for x, s in ((.56, .30), (.70, .40), (.82, .26)):
        d.polygon([(w * x, h * .6), (w * x + w * .05, h * (.6 - s) - 2), (w * x + w * .10, h * .6)], fill=(245, 140, 40))
        d.polygon([(w * x + w * .02, h * .6), (w * x + w * .05, h * (.6 - s * .5)), (w * x + w * .08, h * .6)], fill=(255, 225, 100))


def sc_seoul(d, w, h):
    d.rectangle((0, 0, w, h), fill=(190, 215, 240))
    d.polygon([(w * .52, h), (w * .60, h * .40), (w * .64, h * .40), (w * .72, h)], fill=(70, 80, 100))
    d.ellipse((w * .55, h * .18, w * .69, h * .46), fill=(70, 80, 100))
    d.line((w * .62, 0, w * .62, h * .2), fill=(70, 80, 100), width=2)
    fx0, fy0, fx1, fy1 = w * .78, h * .12, w * .96, h * .58
    d.rectangle((fx0, fy0, fx1, fy1), fill=(250, 250, 250), outline=(120, 120, 120))
    cx, cy, r = (fx0 + fx1) / 2, (fy0 + fy1) / 2, h * .13
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(200, 40, 50))
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 0, 180, fill=(40, 70, 160))


def sc_europe(d, w, h):
    d.rectangle((0, 0, w, h), fill=(30, 60, 130))
    cx, cy, r = w * .84, h * .42, h * .30
    import math
    for k in range(12):
        a = k * math.pi / 6
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=YELLOW)
    for i, hh in enumerate((.25, .35, .30, .50, .62)):
        d.rectangle((w * (.50 + i * .06), h * (.95 - hh), w * (.50 + i * .06) + w * .04, h * .95), fill=(80, 200, 130))


SCENES = {1: sc_belgium, 2: sc_nvidia, 3: sc_wallst, 4: sc_kospi, 5: sc_benghazi, 6: sc_cop,
          7: sc_train, 8: sc_gaza, 9: sc_cricket, 10: sc_oil, 11: sc_fire, 12: sc_seoul, 13: sc_europe}


def scene(img, reg, band, n, x, y, w, h):
    sub = Image.new("RGB", (w, h))
    SCENES[n](ImageDraw.Draw(sub), w, h)
    img.paste(sub, (x, y))
    reg.add(band, "scene", (x, y, x + w, y + h))


def badge(d, reg, band, x, y, num, unit, nsz, usz, pad):
    fn, fu = F("sb", nsz), F("sb", usz)
    capn, capu = round(.73 * nsz), round(.73 * usz)
    wd = int(max(fn.getlength(num), fu.getlength(unit))) + 2 * pad
    ht = pad + capn + 4 + capu + pad
    rect(d, reg, band, (x, y, x + wd - 1, y + ht - 1), fill=(18, 20, 30), kind="badge")
    T(d, reg, band, (x + pad, y + pad + capn), num, fn, (255, 255, 255), anchor="ls")
    T(d, reg, band, (x + pad, y + pad + capn + 4 + capu), unit, fu, YELLOW, anchor="ls")
    return wd, ht


# ------------------------------------------------------------------ panels
def large(img, d, reg, s, x, y):
    band, w, h = "larges", 246, 182
    rect(d, reg, band, (x, y, x + w - 1, y + h - 1), fill=(255, 255, 255), outline=LINE, kind="panel")
    scene(img, reg, band, s["n"], x + 1, y + 1, w - 2, 84)
    badge(d, reg, band, x + 7, y + 7, s["num"], s["unit"], 30, 9, 5)
    num_dot(d, reg, band, x + w - 16, y + 16, s["n"], r=10, size=12)
    T(d, reg, band, (x + 6, y + 88), s["head"], F("sb", 20), INK, maxw=w - 12)
    for i, ln in enumerate(wrap(reg, F("s", 12), s["deck"], w - 12, 2)):
        T(d, reg, band, (x + 6, y + 120 + i * 16), ln, F("s", 12), (50, 52, 60))
    cw = chip(d, reg, band, x + 6, y + 166, s["tag"], TAG_COL[s["tag"]])
    T(d, reg, band, (x + 12 + cw, y + 167), s["src"], F("s", 10), GREY, maxw=w - 24 - cw - 60)
    T(d, reg, band, (x + w - 6, y + 167), s["region"], F("sb", 9), REGION_COL[s["region"]], anchor="ra")


def medium(img, d, reg, s, x, y, band):
    w, h = 192, 136
    rect(d, reg, band, (x, y, x + w - 1, y + h - 1), fill=(255, 255, 255), outline=LINE, kind="panel")
    scene(img, reg, band, s["n"], x + 1, y + 1, w - 2, 52)
    badge(d, reg, band, x + 4, y + 4, s["num"], s["unit"], 26, 9, 4)
    num_dot(d, reg, band, x + w - 12, y + 13, s["n"], r=9, size=10)
    for i, ln in enumerate(wrap(reg, F("sb", 14), s["head"], w - 10, 2)):
        T(d, reg, band, (x + 5, y + 55 + i * 17), ln, F("sb", 14), INK)
    for i, ln in enumerate(wrap(reg, F("s", 10), s["deck"], w - 10, 2)):
        T(d, reg, band, (x + 5, y + 92 + i * 13), ln, F("s", 10), (50, 52, 60))
    cw = chip(d, reg, band, x + 5, y + 122, s["tag"], TAG_COL[s["tag"]], size=8, pad=3, h=11)
    T(d, reg, band, (x + 9 + cw, y + 123), s["src"], F("s", 9), GREY, maxw=w - 14 - cw)


def brief(d, reg, s, x, y, w=346, h=70):
    band = "bottom"
    rect(d, reg, band, (x, y, x + w - 1, y + h - 1), fill=(255, 255, 255), outline=LINE, kind="panel")
    rect(d, reg, band, (x + 1, y + 1, x + 5, y + h - 2), fill=REGION_COL[s["region"]], kind="flag")
    # Headline and detail run full width (number chip sits bottom-right), so both can be larger.
    T(d, reg, band, (x + 13, y + 11), s["head"], F("sb", 15), INK, maxw=w - 54)
    T(d, reg, band, (x + 13, y + 38), s["det"], F("s", 11), GREY, maxw=w - 54)
    chip(d, reg, band, x + w - 24, y + h - 20, str(s["n"]), REGION_COL[s["region"]],
         size=10, pad=2, h=14)


# ------------------------------------------------------------------ map
LAND = [
    [(-168, 66), (-140, 70), (-125, 70), (-95, 72), (-80, 70), (-62, 60), (-56, 52), (-66, 45), (-70, 42), (-76, 35),
     (-81, 30), (-80, 25), (-84, 30), (-90, 29), (-97, 26), (-97, 20), (-87, 21), (-83, 10), (-78, 8), (-86, 12),
     (-92, 15), (-105, 20), (-110, 24), (-114, 31), (-118, 34), (-124, 40), (-124, 48), (-130, 55), (-140, 60),
     (-152, 59), (-165, 55), (-168, 60)],
    [(-80, 8), (-72, 12), (-62, 10), (-50, 0), (-35, -6), (-39, -15), (-48, -26), (-58, -38), (-66, -46), (-70, -54),
     (-75, -48), (-73, -38), (-70, -20), (-76, -14), (-81, -5)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (2, 51), (8, 54), (10, 57), (5, 62), (15, 69), (30, 71), (60, 69),
     (80, 73), (110, 77), (140, 72), (170, 70), (180, 66), (160, 60), (155, 52), (142, 52), (140, 45), (130, 42),
     (127, 38), (126, 35), (122, 40), (120, 30), (110, 20), (108, 12), (105, 9), (100, 13), (103, 2), (98, 8),
     (94, 16), (88, 22), (80, 15), (77, 8), (72, 20), (67, 25), (57, 26), (48, 30), (40, 36), (36, 36), (28, 36),
     (26, 40), (22, 37), (19, 41), (13, 45), (16, 41), (8, 44), (3, 43), (-5, 36)],
    [(35, 30), (43, 13), (52, 16), (59, 22), (56, 26), (48, 30)],
    [(-17, 21), (-10, 30), (-5, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 12), (40, -3), (40, -15),
     (35, -25), (27, -34), (18, -34), (12, -17), (9, -1), (9, 5), (-8, 4), (-17, 14)],
    [(114, -22), (122, -18), (131, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37), (140, -38),
     (132, -32), (115, -34)],
    [(166, -47), (178, -37), (176, -41), (172, -47)],
    [(130, 31), (135, 34), (140, 36), (142, 40), (141, 45), (138, 38), (132, 34)],
    [(95, 5), (106, -6), (104, -6), (95, 2)],
    [(109, -1), (117, 7), (119, 0), (115, -4)],
    [(105, -5.5), (115, -6.5), (115, -9), (105, -8)],
    [(-5, 50), (1, 51), (2, 53), (-2, 57), (-5, 58), (-6, 55)],
]
LON0, LON1, LAT0, LAT1 = -135.0, 180.0, 70.0, -50.0


def project(lon, lat, w, h):
    return ((lon - LON0) / (LON1 - LON0) * w, (LAT0 - lat) / (LAT0 - LAT1) * h)


def world_map(img, d, reg, x0, y0, w, h):
    band = "bottom"
    rect(d, reg, band, (x0, y0, x0 + w - 1, y0 + h - 1), fill=NAVY, kind="map")
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for poly in LAND:
        md.polygon([project(lo, la, w, h) for lo, la in poly], fill=255)
    for gy in range(3, h, 4):
        for gx in range(3, w, 4):
            if mask.getpixel((gx, gy)):
                d.ellipse((x0 + gx - 1.3, y0 + gy - 1.3, x0 + gx + 1.3, y0 + gy + 1.3), fill=(122, 160, 214))
    pins = []
    for label, lon, lat, city, (dx, dy) in data.PINS:
        px, py = project(lon, lat, w, h)
        cx, cy = x0 + px + dx, y0 + py + dy
        if dx or dy:
            d.line((x0 + px, y0 + py, cx, cy), fill=(255, 255, 255), width=1)
        pins.append((cx, cy))
        if not (x0 + 8 <= cx <= x0 + w - 8 and y0 + 8 <= cy <= y0 + h - 8):
            reg.warn(f"pin {label} outside map: {cx:.0f},{cy:.0f}")
        num_dot(d, reg, band, int(round(cx)), int(round(cy)), label, r=7, size=9)
    reg.meta["pin_xy"] = pins
    # key under the map
    ky = y0 + h + 8
    for i, (label, lon, lat, city, _) in enumerate(data.PINS):
        col, row = divmod(i, 7)
        kx, kyy = x0 + 4 + col * 140, ky + row * 17
        num_dot(d, reg, band, kx + 8, kyy + 8, label, r=8, size=9, fill=RED)
        T(d, reg, band, (kx + 21, kyy + 8.5), city, F("s", 10), INK, anchor="lm", maxw=112)


# ------------------------------------------------------------------ frame
def italic(img, reg, band, cx, y, s, font, fill, maxw):
    tw = int(font.getlength(s)) + 24
    th = font.size + 12
    tmp = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(tmp).text((8, 4), s, font=font, fill=255)
    sh = .2
    tmp = tmp.transform((tw, th), Image.AFFINE, (1, sh, -sh * th, 0, 1, 0), resample=Image.BICUBIC)
    bb = tmp.getbbox()
    ink = bb[2] - bb[0]
    if ink > maxw:
        reg.warn(f"kicker too wide {ink}>{maxw}")
    px = int(cx - ink / 2) - bb[0]
    layer = Image.new("RGB", (tw, th), fill)
    img.paste(layer, (px, y), tmp)
    reg.add(band, "text", (px + bb[0], y + bb[1], px + bb[2], y + bb[3]), s)


def region_widths(counts):
    gap, total = 2, 992
    avail = total - gap * (len(counts) - 1)
    floor = 92
    ws = [max(floor, round(avail * c / sum(counts))) for c in counts]
    while sum(ws) != avail:
        i = ws.index(max(ws))
        ws[i] += avail - sum(ws)
    return ws, gap


def build():
    img = Image.new("RGB", (W, H), PAGE)
    d = ImageDraw.Draw(img)
    reg = Reg()
    stories = data.all_stories()
    tally = {r: sum(1 for s in stories if s["region"] == r) for r in data.REGIONS}

    # top bar 0-18
    rect(d, reg, "topbar", (0, 0, W - 1, 17), fill=NAVY, kind="rect")
    T(d, reg, "topbar", (16, 9), "THE WORLD IN ONE DAY", F("sb", 11), (255, 255, 255), anchor="lm")
    T(d, reg, "topbar", (W / 2, 9), "PRESS TIME 21:00 UTC · US CLOSE", F("s", 11), YELLOW, anchor="mm")
    right = "21 STORIES · 7 REGIONS"
    reg.meta["topbar_right"] = right
    T(d, reg, "topbar", (W - 16, 9), right, F("sb", 11), (255, 255, 255), anchor="rm")

    # masthead 20-80
    T(d, reg, "masthead", (W / 2, 52), "MONDAY 23 NOVEMBER 2026", F("rb", 48), NAVY, anchor="mm", maxw=992)

    # kicker 80-100
    italic(img, reg, "kicker", W / 2, 76, data.KICKER, F("r", 15), RED, 992)

    # region bar 102-122
    ws, gap = region_widths([tally[r] for r in data.REGIONS])
    x = 16
    for r, wd in zip(data.REGIONS, ws):
        rect(d, reg, "regionbar", (x, 102, x + wd - 1, 121), fill=REGION_COL[r], kind="chip")
        T(d, reg, "regionbar", (x + wd / 2, 112), f"{r} {tally[r]}", F("sb", 10), (255, 255, 255), anchor="mm", maxw=wd - 4)
        x += wd + gap
    reg.meta["region_counts"] = tally
    reg.meta["region_bar_w"] = x - gap - 16

    # timeline 124-150
    rect(d, reg, "timeline", (16, 124, 1007, 149), fill=NAVY, kind="rect")
    T(d, reg, "timeline", (24, 137), "UTC", F("sb", 10), (150, 170, 210), anchor="lm")
    cw = (992 - 40) / 6
    for i, (t, lab) in enumerate(data.TIMELINE):
        cx = 16 + 40 + i * cw
        tb = T(d, reg, "timeline", (cx, 137), t, F("sb", 11), YELLOW, anchor="lm")
        T(d, reg, "timeline", (tb[2] + 5, 137), lab, F("s", 10), (255, 255, 255), anchor="lm", maxw=cw - (tb[2] - cx) - 10)

    # larges 156-340 + rail
    for i, s in enumerate(data.LARGES):
        large(img, d, reg, s, (16, 270, 524)[i], 156)
    rx, ry, rw = 778, 156, 230
    rect(d, reg, "larges", (rx, ry, rx + rw - 1, 156 + 181), fill=(255, 255, 255), outline=NAVY, kind="rail")
    T(d, reg, "larges", (rx + 8, ry + 10), "THE DAY IN NUMBERS", F("sb", 12), NAVY, anchor="lm")
    for i, (num, lab, n, token) in enumerate(data.RAIL):
        yy = ry + 24 + i * 26
        d.line((rx + 6, yy, rx + rw - 7, yy), fill=LINE)
        T(d, reg, "larges", (rx + 8, yy + 13), num, F("sb", 20), NAVY, anchor="lm", maxw=96)
        T(d, reg, "larges", (rx + 108, yy + 13), lab, F("s", 10), (50, 52, 60), anchor="lm", maxw=rw - 116)

    # mediums
    for i, s in enumerate(data.MEDIUMS):
        row, col = divmod(i, 5)
        medium(img, d, reg, s, (16, 216, 416, 616, 816)[col], 346 if row == 0 else 490, "med1" if row == 0 else "med2")

    # bottom band: 2 columns x 4 rows = 8 briefs, every cell filled (no dead cell);
    # reading order runs left-to-right, row by row.
    for i, s in enumerate(data.BRIEFS):
        row, col = divmod(i, 2)
        brief(d, reg, s, (16, 370)[col], 634 + row * 76)
    T(d, reg, "bottom", (728, 640), "WHERE IT HAPPENED", F("sb", 12), NAVY, anchor="lm")
    T(d, reg, "bottom", (1008, 640), "pins = story numbers", F("s", 9), GREY, anchor="rm")
    world_map(img, d, reg, 728, 650, 280, 150)

    # DATE CHECK 942-978
    rect(d, reg, "datecheck", (16, 942, 1007, 977), fill=(255, 247, 246), outline=RED, kind="rect")
    d.rectangle((17, 943, 1006, 976), outline=RED)
    lb = T(d, reg, "datecheck", (24, 952), "DATE CHECK", F("sb", 10), RED, anchor="lm")
    T(d, reg, "datecheck", (lb[2] + 6, 952), data.DC_LINE1, F("s", 10), INK, anchor="lm", maxw=1000 - lb[2] - 6 - 16)
    T(d, reg, "datecheck", (24, 968), data.DC_LINE2, F("s", 10), INK, anchor="lm", maxw=960)

    # legend 980-1002
    for i, ln in enumerate(wrap(reg, F("s", 9), data.LEGEND, 992, 2)):
        T(d, reg, "legend", (W / 2, 987 + i * 11), ln, F("s", 9), GREY, anchor="mm")

    reg.meta["all_text"] = " | ".join(reg.texts)
    return img, reg


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    img, reg = build()
    out = os.path.join(here, "entry.png")
    img.save(out, "PNG", optimize=True)
    for w in reg.warnings:
        print("FIT WARNING:", w)
    print(f"wrote {out} ({os.path.getsize(out)} bytes), {len(reg.warnings)} fit warnings")
    return 1 if reg.warnings else 0


if __name__ == "__main__":
    sys.exit(main())
