"""the house press.

every image leaves here looking printed, not rendered: xerox decay, duotone inks,
misregistration, halftone, brutal condensed type, stamps. the nous method,
the voidfag palette. four inks only: black, cream, the impossible magenta,
signal orange.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1500
INK_BLACK = (10, 5, 16)
INK_CREAM = (242, 237, 228)
INK_MAGENTA = (255, 0, 212)
INK_ORANGE = (255, 77, 0)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def mono(size, bold=False):
    name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def ink_grade(img):
    """xerox levels + duotone ramp; anything magenta-ish snaps to the pure ink."""
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    L = a @ np.array([0.299, 0.587, 0.114], np.float32)
    Lc = np.clip((L - 18.0) / (236.0 - 18.0), 0, 1) ** 0.9
    t = Lc[..., None]
    out = (1 - t) * np.array(INK_BLACK, np.float32) + t * np.array(INK_CREAM, np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = (r > 110) & (g < 110) & (b > 60) & (r - g > 70)
    out[mag] = np.array(INK_MAGENTA, np.float32)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), mag


def misregistration(img, mag):
    """the magenta plate prints slightly off. the ghost of a second feed."""
    a = np.asarray(img).astype(np.float32)
    m = mag.astype(np.float32)[..., None]
    shifted = np.roll(np.roll(a, 4, axis=1), -3, axis=0)
    a = a * (1 - 0.8 * m) + shifted * (0.8 * m)
    ghost = np.roll(a, (3, -2), axis=(0, 1))
    a = np.clip(a * 0.88 + ghost * 0.12, 0, 255)
    return Image.fromarray(a.astype(np.uint8))


def xerox_decay(img, rng):
    """toner grain, dropout streaks, worn edges. never a clean digital block."""
    a = np.asarray(img).astype(np.float32)
    a += rng.normal(0, 5.5, a.shape)
    for _ in range(10):
        y = int(rng.integers(20, a.shape[0] - 20))
        h = int(rng.integers(1, 3))
        x0 = int(rng.integers(0, a.shape[1] // 2))
        x1 = int(rng.integers(a.shape[1] // 2, a.shape[1]))
        a[y:y + h, x0:x1] *= float(rng.uniform(0.35, 0.6))
    hh, ww = a.shape[:2]
    yy, xx = np.mgrid[0:hh, 0:ww]
    d = np.minimum(np.minimum(xx, ww - xx), np.minimum(yy, hh - yy)).astype(np.float32)
    noise = rng.normal(0, 7, d.shape).astype(np.float32)
    edge = np.clip((26 - d - noise) / 26, 0, 1) * 0.55
    a *= (1 - edge)[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def condensed_text(img, xy, text, size, fill, squeeze=0.62, tracking=3):
    """no condensed font on this machine. render wide, squeeze horizontally."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), size)
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    bbox = layer.getbbox()
    if not bbox:
        return
    crop = layer.crop(bbox)
    crop = crop.resize((max(1, int(crop.width * squeeze)), crop.height))
    img.paste(crop, (bbox[0], bbox[1]), crop)


def stamp(img, text, xy, angle, color, scale=1.0, seed=11):
    w = int(len(text) * 34 * scale) + 60
    h = int(104 * scale)
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    sd.rectangle([3, 3, w - 4, h - 4], outline=color + (255,), width=4)
    sd.rectangle([12, 12, w - 13, h - 13], outline=color + (170,), width=1)
    f = mono(int(48 * scale), bold=True)
    total = sum(sd.textlength(c, font=f) + 7 for c in text) - 7
    x = (w - total) / 2
    for c in text:
        sd.text((x, (h - 48 * scale) / 2), c, font=f, fill=color + (255,))
        x += sd.textlength(c, font=f) + 7
    arr = np.asarray(s).astype(np.float32)
    keep = (np.random.default_rng(seed).random(arr.shape[:2]) > 0.18).astype(np.float32) * 0.72 + 0.28
    arr[..., 3] *= keep
    s = Image.fromarray(arr.astype(np.uint8)).rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(s, xy, s)


def press(base_path, out_path, title, subtitle, annotation, stamp_text,
          microtext, footer, seed=137):
    img = Image.open(base_path).convert("RGB").resize((W, H), Image.LANCZOS)
    rng = np.random.default_rng(seed)
    img, mag = ink_grade(img)
    img = misregistration(img, mag)
    img = xerox_decay(img, rng)
    a = np.asarray(img).astype(np.float32)
    a[::3] *= 0.95
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    d = ImageDraw.Draw(img)
    d.rectangle([24, 24, W - 24, H - 24], outline=(120, 118, 112), width=2)
    d.rectangle([32, 32, W - 32, H - 32], outline=(70, 68, 64), width=1)
    condensed_text(img, (60, 52), title, 74, INK_CREAM + (255,))
    d = ImageDraw.Draw(img)
    d.text((62, 148), subtitle, font=mono(15), fill=(150, 146, 138))
    d.line([(60, 176), (W - 60, 176)], fill=(70, 68, 64), width=1)

    # annotation: the press measures the piece itself — centroid of the divine ink
    ys, xs = np.where(mag)
    if len(xs) > 200:
        cx, cy = int(xs.mean()), int(ys.mean())
        d.line([(cx - 10, cy), (cx + 10, cy)], fill=INK_ORANGE, width=1)
        d.line([(cx, cy - 10), (cx, cy + 10)], fill=INK_ORANGE, width=1)
        right = cx < W // 2
        lx = (cx + 110) if right else (cx - 430)
        lx = max(60, min(lx, W - 440))
        ly = (cy - 64) if cy > 300 else (cy + 44)
        d.line([(cx + (14 if right else -14), cy - 14), (lx - 10, ly + 18)],
               fill=INK_ORANGE, width=1)
        d.text((lx, ly), annotation, font=mono(13), fill=INK_ORANGE)

    stamp(img, stamp_text, (640, 1150), -9, INK_MAGENTA, scale=0.9)

    mf = mono(7)
    reps = (W - 120) // max(1, int(len(microtext) * 4.2)) + 1
    d.text((60, H - 74), (microtext * reps)[:(W - 120) // 4], font=mf, fill=(90, 88, 84))
    d.text((60, H - 52), footer, font=mono(13), fill=(130, 126, 120))

    a = np.asarray(img).astype(np.float32)
    a += np.random.default_rng(seed + 1).normal(0, 1.4, a.shape)
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / (math.hypot(W, H) / 2)
    a *= (1.0 - 0.12 * np.clip(r - 0.55, 0, 1))[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(out_path)
    print("pressed:", out_path)
