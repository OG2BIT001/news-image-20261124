#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE -- Tuesday 24 November 2026.

Draws a newspaper front page summing up 24 November 2026 world news
and writes it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Round 1, early edition: built in the first hours of 24 November 2026 UTC,
so the page leads with what Tuesday morning's papers lead with. A stronger
round 2 with the full day's news may follow before the deadline.

Everything is drawn with the Python standard library only: a hand-authored
5x7 bitmap typeface, geometric icons, and a hand-encoded PNG (zlib + struct).
Output is byte-identical across runs: no timestamps, no randomness, no
dict-order dependence.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (176, 32, 32)
BLUE = (28, 62, 118)
GREEN = (32, 116, 58)
GOLD = (196, 138, 30)
GREY = (222, 216, 202)
LIGHT = (238, 233, 220)
WHITE = (255, 255, 255)
DARKRED = (140, 20, 20)

# ---------------------------------------------------------------- font ----
# 5x7 bitmap glyphs, rows top to bottom, "#" = on, "." = off.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def wrap_text(text, max_w, scale):
    """Greedy word wrap; returns a list of lines, each <= max_w px."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# -------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = color[0]
                self.px[i + 1] = color[1]
                self.px[i + 2] = color[2]

    def hline(self, x, y, w, color, thick=1):
        self.fill_rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill_rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill_rect(x0 - thick // 2, y0 - thick // 2, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, filled=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if filled:
                    if d <= r * r:
                        self.set(xx, yy, color)
                else:
                    if abs(d - r * r) <= r:
                        self.set(xx, yy, color)

    def triangle(self, p0, p1, p2, color):
        # scanline fill of a triangle
        pts = sorted([p0, p1, p2], key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts
        for y in range(y0, y2 + 1):
            xa = x0 + (x2 - x0) * (y - y0) / max(1, (y2 - y0))
            if y <= y1 and y1 > y0:
                xb = x0 + (x1 - x0) * (y - y0) / (y1 - y0)
            elif y > y1 and y2 > y1:
                xb = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            else:
                xb = xa
            lo, hi = sorted([int(xa), int(xb)])
            for x in range(lo, hi + 1):
                self.set(x, y, color)

    def draw_char(self, x, y, ch, scale, color):
        glyph = FONT.get(ch)
        if glyph is None:
            return
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    self.fill_rect(x + col * scale, y + row * scale,
                                   scale, scale, color)

    def draw_text(self, x, y, text, scale, color, align="left"):
        tw = text_width(text, scale)
        if align == "center":
            x = x - tw // 2
        elif align == "right":
            x = x - tw
        cx = x
        for ch in text:
            self.draw_char(cx, y, ch, scale, color)
            cx += 6 * scale
        return tw

    def draw_block(self, x, y, lines, scale, color, line_h=None):
        if line_h is None:
            line_h = 7 * scale + 4
        cy = y
        for ln in lines:
            self.draw_text(x, cy, ln, scale, color)
            cy += line_h
        return cy


# --------------------------------------------------------------- icons ----
def icon_chip(c, x, y, s):
    # computer chip: dark square, inner die, pins, rising arrow
    c.fill_rect(x, y, s, s, BLUE)
    c.fill_rect(x + s // 6, y + s // 6, s * 2 // 3, s * 2 // 3, WHITE)
    c.fill_rect(x + s // 3, y + s // 3, s // 3, s // 3, GREEN)
    for i in range(4):
        t = s // 8 + i * s // 4
        c.fill_rect(x + t, y - 6, 5, 6, INK)
        c.fill_rect(x + t, y + s, 5, 6, INK)
        c.fill_rect(x - 6, y + t, 6, 5, INK)
        c.fill_rect(x + s, y + t, 6, 5, INK)


def icon_flame(c, x, y, s):
    c.fill_rect(x, y, s, s, DARKRED)
    c.triangle((x + s // 2, y + 6), (x + 8, y + s - 8), (x + s - 8, y + s - 8), (255, 120, 30))
    c.triangle((x + s // 2, y + s // 2 - 4), (x + s // 4, y + s - 8), (x + s * 3 // 4, y + s - 8), (255, 200, 40))
    c.circle(x + s // 2, y + s - 16, 7, (255, 240, 120))


def icon_ship(c, x, y, s):
    c.fill_rect(x, y, s, s, BLUE)
    # hull
    c.triangle((x + 6, y + s - 22), (x + s - 6, y + s - 22), (x + s - 14, y + s - 8), (255, 255, 255))
    c.fill_rect(x + 8, y + s - 22, s - 22, 8, WHITE)
    # mast + flag
    c.fill_rect(x + s // 2 - 2, y + 8, 4, s - 30, WHITE)
    c.triangle((x + s // 2 + 2, y + 8), (x + s // 2 + 2, y + 20), (x + s - 12, y + 14), RED)
    # waves
    for i in range(3):
        c.fill_rect(x + 6 + i * 16, y + s - 5, 12, 3, (120, 180, 230))


def icon_building(c, x, y, s):
    c.fill_rect(x, y, s, s, (90, 90, 96))
    c.fill_rect(x + 10, y + 22, s - 20, s - 30, (210, 205, 190))
    for r in range(3):
        for col in range(3):
            c.fill_rect(x + 16 + col * 14, y + 28 + r * 12, 8, 7, (60, 60, 70))
    # smoke
    c.circle(x + s // 2 - 8, y + 8, 6, (120, 120, 120))
    c.circle(x + s // 2 + 4, y + 4, 8, (150, 150, 150))
    c.circle(x + s // 2 + 12, y + 10, 5, (120, 120, 120))


def icon_talks(c, x, y, s):
    c.fill_rect(x, y, s, s, GREEN)
    # two speech bubbles
    c.fill_rect(x + 8, y + 10, s // 2, s // 3, WHITE)
    c.triangle((x + 12, y + 10 + s // 3), (x + 22, y + 10 + s // 3), (x + 12, y + 10 + s // 3 + 10), WHITE)
    c.fill_rect(x + s // 2 - 2, y + s // 2, s // 2, s // 3, (20, 20, 20))
    c.triangle((x + s - 14, y + s // 2 + s // 3), (x + s - 24, y + s // 2 + s // 3), (x + s - 14, y + s // 2 + s // 3 + 10), (20, 20, 20))
    c.fill_rect(x + 14, y + 18, s // 2 - 12, 3, GREEN)
    c.fill_rect(x + 14, y + 26, s // 2 - 22, 3, GREEN)


def icon_train(c, x, y, s):
    c.fill_rect(x, y, s, s, (120, 60, 30))
    # locomotive body
    c.fill_rect(x + 8, y + 12, s - 16, s // 2, (250, 240, 210))
    c.fill_rect(x + 8, y + 12, s // 3, s // 2, RED)
    for i in range(3):
        c.fill_rect(x + 16 + i * 16, y + 20, 10, 10, BLUE)
    # wheels + track
    c.circle(x + 18, y + s - 14, 7, INK)
    c.circle(x + s - 18, y + s - 14, 7, INK)
    c.hline(x + 4, y + s - 6, s - 8, INK, 3)


def icon_crowd(c, x, y, s):
    c.fill_rect(x, y, s, s, GOLD)
    # placard
    c.fill_rect(x + s // 2 - 4, y + 8, 4, 22, INK)
    c.fill_rect(x + s // 2 - 18, y + 4, 36, 16, WHITE)
    c.fill_rect(x + s // 2 - 13, y + 9, 26, 3, RED)
    # heads
    for i in range(4):
        cx = x + 10 + i * 14
        c.circle(cx, y + s - 18, 7, (40, 40, 44))
        c.fill_rect(cx - 8, y + s - 11, 16, 11, (40, 40, 44))


def icon_ball(c, x, y, s):
    c.fill_rect(x, y, s, s, GREEN)
    c.circle(x + s // 2, y + s // 2, s // 2 - 4, WHITE)
    # pentagon
    cx, cy = x + s // 2, y + s // 2
    c.fill_rect(cx - 7, cy - 7, 14, 14, INK)
    c.line(cx, cy - 7, cx, y + 6, INK, 2)
    c.line(cx - 7, cy + 5, x + 8, y + s - 8, INK, 2)
    c.line(cx + 7, cy + 5, x + s - 8, y + s - 8, INK, 2)


# ---------------------------------------------------------------- png ------
def chunk(ctype, data):
    out = struct.pack(">I", len(data)) + ctype + data
    out += struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return out


def encode_png(c):
    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(c.h):
        raw.append(0)
        base = yy * c.w * 3
        raw += c.px[base:base + c.w * 3]
    idat = zlib.compress(bytes(raw), 9)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", idat) + chunk(b"IEND", b""))


# -------------------------------------------------------------- layout ----
def story_box(c, x, y, w, h, kicker, headline, deck, icon, hscale=3,
              icon_size=46, deck_lh=17, icon_right=False):
    """A boxed story: icon top-left (or top-right), kicker, headline, deck."""
    c.fill_rect(x, y, w, h, WHITE)
    c.hline(x, y, w, INK, 2)
    ix, iy = x + 10, y + 10
    if icon is not None and icon_right:
        icon(c, x + w - 10 - icon_size, y + 10, icon_size)
        kx = x + 10
        hy = y + 34
    elif icon is not None:
        icon(c, ix, iy, icon_size)
        kx = x + 10 + icon_size + 10
        hy = y + 10 + icon_size + 6
    else:
        kx = x + 10
        hy = y + 34
    c.draw_text(kx, y + 12, kicker, 2, RED)
    hlines = wrap_text(headline, w - 20, hscale)
    cy = c.draw_block(x + 10, hy, hlines, hscale, INK, 7 * hscale + 5)
    dlines = wrap_text(deck, w - 20, 2)
    c.draw_block(x + 10, cy + 6, dlines, 2, (40, 40, 40), deck_lh)


def draw_page():
    c = Canvas(W, H, PAPER)
    # outer border
    c.fill_rect(8, 8, W - 16, 3, INK)
    c.fill_rect(8, H - 11, W - 16, 3, INK)
    c.fill_rect(8, 8, 3, H - 16, INK)
    c.fill_rect(W - 11, 8, 3, H - 16, INK)

    # ---- masthead ----
    c.fill_rect(16, 16, W - 32, 88, INK)
    c.draw_text(512, 34, "THE WORLD IN ONE PAGE", 5, WHITE, align="center")
    c.draw_text(512, 78, "THE DAY IN ONE IMAGE", 2, (200, 200, 200), align="center")

    # ---- date band ----
    c.draw_text(24, 118, "EARLY EDITION", 2, RED)
    c.draw_text(1000, 118, "ROUND 1", 2, RED, align="right")
    c.draw_text(512, 112, "TUESDAY 24 NOVEMBER 2026", 4, INK, align="center")
    c.fill_rect(24, 152, 976, 4, RED)

    # ---- lead story (row A) ----
    lx, ly, lw, lh = 24, 168, 636, 236
    c.fill_rect(lx, ly, lw, lh, WHITE)
    c.hline(lx, ly, lw, INK, 2)
    c.draw_text(lx + 12, ly + 12, "LEAD STORY  -  TECHNOLOGY", 2, RED)
    c.draw_text(lx + 12, ly + 36, "HUANG IS BACK", 6, INK)
    lead_deck = ("NVIDIA REINSTATES JENSEN HUANG AS CEO, PRESIDENT AND "
                 "BOARD MEMBER, EFFECTIVE IMMEDIATELY, 11 DAYS AFTER HE "
                 "RESIGNED. THE BOARD VOTED UNANIMOUSLY. SHARES ROSE 31%, "
                 "THE BEST DAY SINCE 2003, ADDING ABOUT $950BN. "
                 "PRESIDENT TRUMP CLAIMS HE ENGINEERED THE RETURN.")
    c.draw_block(lx + 12, ly + 88, wrap_text(lead_deck, lw - 24, 2), 2,
                 (40, 40, 40), 18)
    # market chart strip at the bottom of the lead
    cy0 = ly + lh - 46
    c.hline(lx + 12, cy0 - 6, lw - 24, GREY, 2)
    bars = [10, 16, 22, 30, 40]
    bx = lx + 16
    for i, bh in enumerate(bars):
        c.fill_rect(bx + i * 26, cy0 + 44 - bh, 18, bh, GREEN)
    c.draw_text(lx + 156, cy0 + 2, "SHARES +31% - NASDAQ +6.5%", 2, GREEN)
    c.draw_text(lx + 156, cy0 + 24, "S+P 500 +4.7%  -  DOW +1,448", 2, INK)
    icon_chip(c, lx + lw - 66, ly + 12, 54)

    # ---- Indonesia (row A, right) ----
    story_box(c, 676, 168, 324, 236, "INDONESIA",
              "FACTORY FIRE KILLS 24",
              "24 KILLED, ABOUT 30 MISSING, AFTER A FIRE AT A "
              "CONFECTIONERY FACTORY IN CIKANDE. THE TOLL WAS "
              "CONFIRMED ON MONDAY. THE CAUSE IS BEING PROBED.",
              icon_flame)

    # ---- row B: three stories ----
    story_box(c, 24, 416, 324, 228, "UKRAINE WAR",
              "UKRAINE SINKS RUSSIAN SHIP",
              "UKRAINE SAYS IT SANK THE CORVETTE MERKURY OFF LIBYA WITH "
              "SEVEN NAVAL DRONES AND HIT THE MV ANGARA. THE SPARTA II "
              "CAUGHT FIRE AND IS BEING TOWED BACK.",
              icon_ship, deck_lh=15)
    story_box(c, 360, 416, 324, 228, "KYIV",
              "KYIV REGION UNDER FIRE",
              "RUSSIAN DRONE AND MISSILE ATTACKS ON THE KYIV REGION KILL "
              "SEVERAL PEOPLE AND LEAVE OTHERS MISSING. A HOME WAS HIT IN "
              "THE VILLAGE OF DYMER.",
              icon_building, deck_lh=15)
    story_box(c, 696, 416, 304, 228, "DIPLOMACY",
              "ZELENSKY SEEKS TALKS",
              "PRESIDENT ZELENSKY CALLS FOR FOUR-WAY TALKS WITH RUSSIA AS "
              "SOON AS POSSIBLE.",
              icon_talks, deck_lh=15)

    # ---- row C: India-Nepal + Lisbon (left), Sport (right) ----
    story_box(c, 24, 656, 476, 116, "SOUTH ASIA",
              "INDIA AND NEPAL LINK UP",
              "PM MODI AND NEPAL PM BALENDRA SHAH HOLD TALKS IN DELHI. "
              "THE SARYU-KAMALA EXPRESS LINKS AYODHYA AND JANAKPUR.",
              icon_train, icon_size=32, deck_lh=16, icon_right=True)
    story_box(c, 24, 780, 476, 104, "PORTUGAL",
              "LISBON MARCHES",
              "THOUSANDS MARCH IN LISBON AGAINST RISING LIVING COSTS.",
              icon_crowd, icon_size=36, deck_lh=16, icon_right=True)

    # sport box
    sx, sy, sw, sh = 512, 656, 488, 228
    c.fill_rect(sx, sy, sw, sh, WHITE)
    c.hline(sx, sy, sw, INK, 2)
    icon_ball(c, sx + 10, sy + 10, 52)
    c.draw_text(sx + 72, sy + 12, "SPORT", 2, RED)
    c.draw_text(sx + 72, sy + 34, "SPORT IN BRIEF", 3, INK)
    bullets = [
        "CRICKET: INDIA V NZ FIRST TEST DRAWN AT WELLINGTON. PANT 128.",
        "TENNIS: ALCARAZ WINS MAIDEN ATP FINALS TITLE, BEATING ZVEREV.",
        "F1: VERSTAPPEN WINS THE LAS VEGAS GRAND PRIX.",
        "CHESS: GUKESH V SINDAROV WORLD TITLE MATCH BEGINS IN GENEVA.",
    ]
    by = sy + 72
    for b in bullets:
        blines = wrap_text(b, sw - 20, 2)
        by = c.draw_block(sx + 10, by, blines, 2, (40, 40, 40), 17)
        by += 3

    # ---- footer strip ----
    fy = 896
    c.fill_rect(16, fy, W - 32, 112, INK)
    c.draw_text(24, fy + 12, "BUSINESS", 2, GOLD)
    c.draw_block(24, fy + 34,
                 wrap_text("FERRARI UNVEILS TWO NEW 296 MODELS AT FINALI "
                           "MONDIALI IN SPAIN. INDIA'S SENSEX FALLS 1,484 "
                           "POINTS.", 470, 2), 2, WHITE, 18)
    c.draw_text(512, fy + 12, "WASHINGTON", 2, GOLD)
    c.draw_block(512, fy + 34,
                 wrap_text("REP. JIMMY GOMEZ TO RESIGN FROM CONGRESS FROM "
                           "1 DECEMBER AFTER A HOUSE ETHICS COMMITTEE "
                           "FINDING OF SEXUAL MISCONDUCT.", 470, 2), 2,
                 WHITE, 18)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(draw_page())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
