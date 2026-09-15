"""Original pixel-art sprites and scenes in the ryanlenk.com brand palette. Stdlib + Pillow."""
import math
from pathlib import Path

from PIL import Image

PAL = {
    "K": (0, 0, 0), "W": (255, 255, 255), "C": (245, 240, 230), "Y": (255, 235, 59),
    "P": (255, 64, 129), "B": (33, 150, 243), "G": (76, 175, 80), "O": (255, 152, 0),
    "U": (156, 39, 176), "R": (255, 82, 82),
}


class Canvas:
    def __init__(self, w, h, bg=None):
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0) if bg is None else PAL[bg] + (255,))
        self.w, self.h = w, h

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((int(x), int(y)), PAL[c] + (255,))

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r + r * 0.6:
                    self.px(cx + x, cy + y, c)

    def ring(self, cx, cy, r, c):
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                d = x * x + y * y
                if r * r - r <= d <= r * r + r * 0.6:
                    self.px(cx + x, cy + y, c)

    def stamp(self, other, ox, oy):
        self.img.alpha_composite(other.img, (ox, oy))

    def save(self, path, scale=1):
        im = self.img if scale == 1 else self.img.resize((self.w * scale, self.h * scale), Image.NEAREST)
        im.save(path)


def wheel(cv, cx, cy, r, frame=0):
    cv.disc(cx, cy, r, "C")
    cv.ring(cx, cy, r, "K")
    angles = [0, 45, 90, 135] if frame % 2 == 0 else [22, 67, 112, 157]
    for a in angles:
        ra = math.radians(a)
        dx, dy = round(math.cos(ra) * (r - 1)), round(math.sin(ra) * (r - 1))
        cv.line(cx - dx, cy - dy, cx + dx, cy + dy, "K")
    cv.rect(cx - 1, cy - 1, 2, 2, "O")


def wagon(frame=0):
    cv = Canvas(40, 24)
    top, bw, bh, bx = 1, 24, 11, 7
    for dy in range(bh):
        t = (bh - 1 - dy) / (bh - 1)
        half = round((bw / 2) * math.sqrt(max(0.0, 1 - t * t)) + 1.5)
        mid = bx + bw // 2
        for x in range(mid - half, mid + half + 1):
            cv.px(x, top + dy, "C")
        cv.px(mid - half - 1, top + dy, "K")
        cv.px(mid + half + 1, top + dy, "K")
    for x in range(cv.w):  # outline the top edge of the bonnet
        if cv.img.getpixel((x, top))[:3] == PAL["C"] and cv.img.getpixel((x, top))[3]:
            cv.px(x, top - 1, "K")
    for hx in (bx + 6, bx + 12, bx + 18):
        for y in range(top, top + bh):
            if cv.img.getpixel((hx, y))[:3] == PAL["C"]:
                cv.px(hx, y, "K")
    cv.rect(bx - 3, top + bh, bw + 7, 1, "K")
    cv.rect(bx - 3, top + bh + 1, bw + 7, 3, "O")
    cv.rect(bx - 3, top + bh + 1, 1, 3, "K")
    cv.rect(bx + bw + 3, top + bh + 1, 1, 3, "K")
    cv.rect(bx - 3, top + bh + 4, bw + 7, 1, "K")
    for x in range(bx - 1, bx + bw + 2, 4):
        cv.px(x, top + bh + 2, "K")
    cv.line(bx + bw + 4, top + bh + 3, cv.w - 1, top + bh + 3, "K")
    wheel(cv, bx + 2, 19, 4, frame)
    wheel(cv, bx + bw - 1, 20, 3, frame)
    return cv


OX_BODY = [
    ".................W..W.",
    ".................KWWK.",
    "..KKKKKKKKKKKKKKKKOOK.",
    ".KOOOOOOOOOOOOOOOKOOOK",
    "KOOOOCCOOOOOOOOOOKOKOK",
    "KOOOCCCCOOOOOOOOOOOOOK",
    "KOOOOCCOOOOOOOOOOKKKK.",
    ".KOOOOOOOOOOOOOOK.....",
    ".KKKKKKKKKKKKKKKK.....",
]
OX_LEGS = [
    ["..K.K........K.K......", "..K.K........K.K......", ".KK.KK......KK.KK....."],
    ["...K.K......K.K.......", "...K.K......K.K.......", "..KK.KK....KK.KK......"],
]


def from_map(rows):
    cv = Canvas(len(rows[0]), len(rows))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                cv.px(x, y, ch)
    return cv


def ox(frame=0):
    return from_map(OX_BODY + OX_LEGS[frame % 2])


def team(frame=0):
    cv = Canvas(64, 24)
    cv.stamp(wagon(frame), 0, 0)
    cv.stamp(ox(frame), 41, 12)
    return cv


def mountain(cv, x, base, h, c="U"):
    for dy in range(h):
        half = dy
        for xx in range(x - half, x + half + 1):
            cv.px(xx, base - h + dy, c)
    for dy in range(max(1, h // 4)):
        for xx in range(x - dy, x + dy + 1):
            cv.px(xx, base - h + dy, "W")


def cloud(cv, x, y):
    cv.rect(x + 2, y, 6, 2, "W")
    cv.rect(x, y + 2, 12, 2, "W")


def flag(cv, x, y, c="P"):
    cv.rect(x, y, 1, 10, "K")
    cv.rect(x + 1, y, 5, 4, c)
    cv.rect(x + 1, y + 4, 1, 0, c)


def prairie(w, h, horizon, trail_y, sun_x=None, clouds=(), mountains=()):
    cv = Canvas(w, h, "B")
    if sun_x is not None:
        cv.disc(sun_x, horizon - 16, 5, "Y")
    for cx, cy in clouds:
        cloud(cv, cx, cy)
    for mx, mh in mountains:
        mountain(cv, mx, horizon, mh)
    cv.rect(0, horizon, w, h - horizon, "G")
    for x in range(3, w, 11):
        cv.px(x, horizon + 3 + (x * 7) % 5, "Y")
    cv.rect(0, trail_y, w, 5, "C")
    cv.rect(0, trail_y + 1, w, 1, "O")
    cv.rect(0, trail_y + 3, w, 1, "O")
    return cv


def tombstone():
    cv = Canvas(40, 44)
    cv.rect(0, 36, 40, 8, "G")
    for y in range(4, 38):
        top = 10
        if y < top:
            t = (top - y) / top
            half = round(13 * math.sqrt(max(0.0, 1 - t * t)))
        else:
            half = 13
        for x in range(20 - half, 20 + half + 1):
            cv.px(x, y, "W")
        cv.px(20 - half - 1, y, "K")
        cv.px(20 + half + 1, y, "K")
    for x in range(cv.w):
        for y in range(cv.h):
            if cv.img.getpixel((x, y))[:3] == PAL["W"] and cv.img.getpixel((x, y))[3]:
                if y == 0 or cv.img.getpixel((x, y - 1))[3] == 0:
                    cv.px(x, y - 1, "K")
                break
    glyph = {
        "R": ["KKK", "K.K", "KK.", "K.K", "K.K"],
        "I": ["KKK", ".K.", ".K.", ".K.", "KKK"],
        "P": ["KKK", "K.K", "KKK", "K..", "K.."],
    }
    x0 = 9
    for ch in "RIP":
        for gy, row in enumerate(glyph[ch]):
            for gx, v in enumerate(row):
                if v == "K":
                    cv.rect(x0 + gx * 2, 13 + gy * 2, 2, 2, "K")
        x0 += 8
    cv.rect(5, 37, 31, 1, "K")
    return cv


def icon(kind):
    cv = Canvas(16, 16)
    if kind == "crate":
        cv.rect(1, 3, 14, 12, "K"); cv.rect(2, 4, 12, 10, "O")
        cv.rect(2, 8, 12, 1, "K"); cv.line(2, 4, 13, 13, "K")
    elif kind == "book":
        cv.rect(2, 1, 12, 14, "K"); cv.rect(3, 2, 10, 12, "B"); cv.rect(4, 2, 1, 12, "K")
        cv.rect(12, 3, 2, 11, "C"); cv.rect(6, 5, 5, 1, "Y"); cv.rect(6, 7, 5, 1, "Y")
    elif kind == "note":
        cv.rect(2, 2, 12, 13, "K"); cv.rect(3, 3, 10, 11, "C")
        for y in (6, 8, 10):
            cv.rect(5, y, 7, 1, "K")
        cv.rect(11, 3, 2, 2, "K")
    elif kind == "never":
        cv.rect(3, 2, 10, 12, "K"); cv.rect(4, 3, 8, 10, "O")
        for i in range(12):
            cv.rect(2 + i, 2 + i, 2, 2, "R"); cv.rect(13 - i, 2 + i, 2, 2, "R")
    return cv


def scene_banner():
    cv = prairie(112, 76, 44, 56, sun_x=92, clouds=((10, 8), (60, 14)), mountains=((18, 16), (40, 22), (70, 12)))
    cv.stamp(team(0), 22, 36)
    flag(cv, 100, 44)
    return cv


def scene_social(frame=0, w=248, h=44, team_x=150):
    cv = prairie(w, h, 20, 33, sun_x=w - 26, clouds=((20, 2), (120, 5), (180, 1)), mountains=((40, 10), (70, 14), (160, 12), (200, 8)))
    cv.stamp(team(frame), team_x, 13)
    flag(cv, w - 12, 23)
    return cv


def scene_trail(flag_xs):
    cv = prairie(276, 40, 14, 28, sun_x=None, clouds=((30, 1), (140, 3), (220, 2)), mountains=((50, 8), (190, 10)))
    for i, x in enumerate(flag_xs):
        flag(cv, x, 18, "P" if i < len(flag_xs) - 1 else "Y")
    return cv


def logo():
    cv = Canvas(48, 48)
    cv.stamp(wagon(0), 5, 12)
    return cv


def build_all(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    scene_banner().save(out / "scene-banner.png")
    scene_social().save(out / "scene-social.png")
    col, gap = (1392 - 5 * 18) / 6, 18
    flag_xs = [round((i * (col + gap) + col / 2 - 6) / 5) for i in range(6)]
    scene_trail(flag_xs).save(out / "scene-trail.png")
    logo().save(out / "logo-wagon.png")
    tombstone().save(out / "tombstone.png")
    for k in ("crate", "book", "note", "never"):
        icon(k).save(out / f"icon-{k}.png")
    for f in range(2):
        scene_social(f, w=240, h=40, team_x=40 + f * 70).save(out / f"strip-{f}.png")
        scene_social(f, w=240, h=40, team_x=150 + f * 4).save(out / f"strip-arrive-{f}.png")


if __name__ == "__main__":
    import sys
    build_all(sys.argv[1])
    print("ok")
