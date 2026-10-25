#!/usr/bin/env python3
"""face002 — the bureau's face. order 002: avatar + banner, press-first, pure code.
no model. 0 steps. seed 137. every printed number is a true property of the render."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SEED = 137
INK   = (10, 5, 16)      # near-black #0A0510
CREAM = (242, 237, 228)  # #F2EDE4
MAG   = (255, 0, 212)    # #FF00D4
ORG   = (255, 77, 0)     # #FF4D00
NARROW = "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf"
MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

rng = np.random.default_rng(SEED)

def paper(w, h, base=CREAM):
    """cream stock: low-freq blotches + fine grain."""
    yy, xx = np.mgrid[0:h, 0:w]
    blotch = np.zeros((h, w))
    for _ in range(14):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(w*0.08, w*0.3)
        blotch += rng.uniform(-1, 1) * np.exp(-(((xx-cx)**2 + (yy-cy)**2) / (2*r*r)))
    grain = rng.normal(0, 2.2, (h, w))
    arr = np.broadcast_to(np.array(base, float), (h, w, 3)).copy() + blotch[:, :, None]*6 + grain[:, :, None]
    # worn darker edges
    ex = np.minimum(xx, w-1-xx) / (w*0.06); ey = np.minimum(yy, h-1-yy) / (h*0.06)
    edge = np.minimum(1, np.minimum(ex, ey))[:, :, None]
    edge = np.clip(edge, 0, 1)**0.8
    arr = arr * (1 - 0.10*(1-edge))
    return np.clip(arr, 0, 255)

def xerox(arr, bp=18, wp=236, gamma=0.9):
    """levels crush + duotone toward ink/cream."""
    a = arr.astype(float) / 255.0
    a = np.clip((a - bp/255.0) / (wp/255.0 - bp/255.0), 0, 1) ** gamma
    return a

def toner(arr, amt=1.0):
    h, w = arr.shape[:2]
    speck = (rng.random((h, w)) < 0.004 * amt) * rng.uniform(-38, 22, (h, w))
    arr = arr + speck[:, :, None]
    return arr

def dropout_streaks(img, n=3, color=CREAM):
    """xerox dropout: pale streaks erasing ink."""
    d = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(n):
        y = rng.uniform(h*0.1, h*0.9)
        hh = rng.uniform(2, 7)
        x0, x1 = rng.uniform(0, w*0.3), rng.uniform(w*0.7, w)
        d.rectangle([x0, y, x1, y+hh], fill=tuple(int(c + rng.uniform(-6, 6)) for c in color))
    return img

def dendrites(draw, cx, cy, R, scales=(1.0, 0.55, 0.30), color=MAG, seedname=None):
    """neural divine: symmetric radial branching, 3 scales, holy + grown."""
    r = np.random.default_rng(SEED + 7)
    n_main = 7
    base_ang = r.uniform(0, 2*np.pi)
    def branch(x, y, ang, length, width, depth):
        if depth == 0 or length < R*0.05: return
        x2 = x + np.cos(ang)*length; y2 = y + np.sin(ang)*length
        draw.line([(x, y), (x2, y2)], fill=color, width=max(1, int(width)))
        # synaptic bud
        if r.random() < 0.55:
            br = width*1.6
            draw.ellipse([x2-br, y2-br, x2+br, y2+br], fill=color)
        spread = r.uniform(0.38, 0.62)
        branch(x2, y2, ang - spread, length*r.uniform(0.58, 0.74), width*0.62, depth-1)
        branch(x2, y2, ang + spread, length*r.uniform(0.58, 0.74), width*0.62, depth-1)
    for s in scales:
        for i in range(n_main):
            ang = base_ang + i*2*np.pi/n_main + (0.12 if s != scales[0] else 0)
            branch(cx, cy, ang, R*s, max(1, int(R*0.070*s)), 4)

def sigil(size, distressed=True, for_avatar=True):
    """the bureau mark: orb in a reticle ring, one magenta filament, dendrite crown."""
    S = size
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = S/2
    R = S*0.44                      # stamp ring radius
    ring_w = max(3, int(S*0.030))
    # ring (rubber stamp, uneven pressure via angular noise)
    an = np.linspace(0, 2*np.pi, 720)
    press = 0.72 + 0.28*np.abs(np.sin(an*3 + 0.7)) * (0.6 + 0.4*np.sin(an*11 + SEED))
    for i, th in enumerate(an):
        alpha = int(255 * press[i]) if distressed else 255
        wobble = S*0.004*np.sin(th*17+1.0)
        rr = R + wobble
        x0, y0 = c+np.cos(th)*rr, c+np.sin(th)*rr
        x1, y1 = c+np.cos(th+0.01)*rr, c+np.sin(th+0.01)*rr
        d.line([(x0, y0), (x1, y1)], fill=INK+(alpha,), width=ring_w)
    # reticle: crosshair with center gap, ticks outside ring
    gap = S*0.16
    lw = max(2, int(S*0.006))
    # crosshair with center gap
    d.line([(c+gap, c), (c+R+S*0.09, c)], fill=INK+(235,), width=lw)
    d.line([(c-gap, c), (c-R-S*0.09, c)], fill=INK+(235,), width=lw)
    d.line([(c, c+gap), (c, c+R+S*0.09)], fill=INK+(235,), width=lw)
    d.line([(c, c-gap), (c, c-R-S*0.09)], fill=INK+(235,), width=lw)
    # measurement ticks on crosshair
    for t in np.linspace(0.30, 0.95, 8):
        for sgn in (1, -1):
            d.line([(c+t*R, c-S*0.012), (c+t*R, c+S*0.012)], fill=INK+(210,), width=max(1,lw//2))
            d.line([(c-t*R, c-S*0.012), (c-t*R, c+S*0.012)], fill=INK+(210,), width=max(1,lw//2))
            d.line([(c, c+t*R-S*0.012), (c, c+t*R+S*0.012)], fill=INK+(210,), width=max(1,lw//2))
            d.line([(c, c-t*R-S*0.012), (c, c-t*R+S*0.012)], fill=INK+(210,), width=max(1,lw//2))
    # orb: solid near-black
    orbR = S*0.145
    d.ellipse([c-orbR, c-orbR, c+orbR, c+orbR], fill=INK+(255,))
    # dendrite crown inside orb (neural divine, magenta only)
    dend = Image.new("RGBA", (S, S), (0,0,0,0))
    dendrites(ImageDraw.Draw(dend), c, c, orbR*0.92)
    dend = dend.filter(ImageFilter.GaussianBlur(0.2))
    # the divine stays inside the mark: clip filigree to the orb
    omask = Image.new("L", (S, S), 0)
    r_in = orbR * 0.94
    ImageDraw.Draw(omask).ellipse([c-r_in, c-r_in, c+r_in, c+r_in], fill=255)
    da = np.array(dend).astype(float)
    da[:, :, 3] *= np.array(omask) / 255.0
    dend = Image.fromarray(da.astype(np.uint8))
    img = Image.alpha_composite(img, dend)
    d = ImageDraw.Draw(img)
    # magenta filament: orbit arc crossing the orb, misregistered +2px
    fil = Image.new("RGBA", (S, S), (0,0,0,0))
    fd = ImageDraw.Draw(fil)
    fr = S*0.20
    fd.arc([c-fr, c-fr, c+fr, c+fr], start=205, end=25, fill=MAG+(255,), width=max(2,int(S*0.012)))
    fil = fil.transform((S, S), Image.AFFINE, (1, 0, 2, 0, 1, 1))  # +2px misregistration
    img = Image.alpha_composite(img, fil)
    if distressed:
        # speckle erosion of the whole mark
        a = np.array(img)
        m = rng.random((S, S))
        fade = (m > 0.985) | ((m > 0.965) & (rng.random((S, S)) > 0.5))
        a[fade, 3] = (a[fade, 3] * 0.15).astype(np.uint8)
        img = Image.fromarray(a)
    return img

def fit_text(text, font_path, size, target_w, fill=INK):
    f = ImageFont.truetype(font_path, size)
    tmp = Image.new("RGBA", (6000, int(size*1.8)), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((0, 0), text, fill=fill, font=f)
    tmp = tmp.crop(tmp.getbbox())
    sc = target_w / tmp.width
    return tmp.resize((target_w, max(1, int(tmp.height*sc))), Image.LANCZOS)

def avatar_master():
    S = 1024
    base = paper(S, S)
    img = Image.fromarray(base.astype(np.uint8))
    img = dropout_streaks(img, n=2)
    mark = sigil(S, distressed=True)
    img.paste(mark, (0, 0), mark)
    # xerox decay + contrast
    a = xerox(np.array(img).astype(float))
    a = np.clip((a - 0.5) * 1.14 + 0.5, 0, 1)  # contrast boost
    a = a ** 0.72                                 # power curve
    a = toner(a * 255)
    return Image.fromarray(a.astype(np.uint8))

def banner_master():
    W, H = 3000, 1000
    base = paper(W, H)
    img = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
    # --- sigil ghost: ink bleed-through under the form, right-center
    GS = 820
    ghost = sigil(GS, distressed=False).filter(ImageFilter.GaussianBlur(5))
    g = np.array(ghost).astype(float)
    g[:, :, 3] *= 0.20
    ghost1 = Image.fromarray(g.astype(np.uint8))
    ghost2 = ghost1.transform((GS, GS), Image.AFFINE, (1, 0, -5, 0, 1, -3))
    gx, gy = 1700, 210
    img.paste(ghost1, (gx, gy), ghost1)
    img.paste(ghost2, (gx, gy), ghost2)
    d = ImageDraw.Draw(img)
    # --- microtext rules, top and bottom edges (full width; decoration may crop)
    f_micro = ImageFont.truetype(MONO, 13)
    micro = "FILED UNDER PROTEST · THE DEMIURGE HAS 30 DAYS TO RESPOND · "
    tw = d.textlength(micro, font=f_micro)
    x = 20
    while x < W:
        d.text((x, 18), micro, fill=INK+(200,), font=f_micro)
        d.text((x, H-34), micro, fill=INK+(200,), font=f_micro)
        x += tw
    for y in (44, H-48):
        d.line([(0, y), (W, y)], fill=INK+(120,), width=2)
    # --- title block (safe zone 500..2500)
    f_small = ImageFont.truetype(NARROW, 120)
    d.text((584, 250), "BUREAU OF", fill=INK, font=f_small)
    title = fit_text("UNVERIFIED CLAIMS", NARROW, 300, 1800)
    img.paste(title, (580, 400), title)
    d = ImageDraw.Draw(img)
    # --- form grid, mono, upper right of safe zone
    f_field = ImageFont.truetype(MONOB, 28)
    f_val   = ImageFont.truetype(MONO, 28)
    rows = [("EXHIBIT Nº", "PENDING"), ("STATUS", "UNVERIFIED"),
            ("FILED", "UNDER PROTEST"), ("INTEREST", "ACCRUED: ONE UNIVERSE")]
    fx, fy, fw = 1870, 140, 560
    for i, (k, v) in enumerate(rows):
        y = fy + i*54
        d.text((fx, y), k, fill=INK, font=f_field)
        d.text((fx+280, y), v, fill=INK, font=f_val)
        d.line([(fx, y+42), (fx+fw, y+42)], fill=INK+(150,), width=2)
    # --- orange annotation, lower left, leader to the orb center (TRUE: delivered is 1500x500)
    ax, ay = 600, 700
    d.text((ax, ay), "SUBJECT REPORTS INFINITE.", fill=ORG, font=f_val)
    d.text((ax, ay+46), "MEASURED: 1500×500 PX.", fill=ORG, font=f_val)
    lx0, ly0 = ax + d.textlength("SUBJECT REPORTS INFINITE.", font=f_val) + 30, ay + 16
    lx1, ly1 = 1975, 640
    d.line([(lx0, ly0), (lx1, ly1)], fill=ORG, width=3)
    d.ellipse([lx1-14, ly1-14, lx1+14, ly1+14], outline=ORG, width=3)
    # --- physics line, bottom, centered, mono — every number true
    f_phys = ImageFont.truetype(MONO, 26)
    phys = "PURE PRESS · 0 STEPS · NO MODEL · SEED 137 · MASTER 3000×1000 · DELIVERED 1500×500 · NUMPY 1.24.2"
    pw = d.textlength(phys, font=f_phys)
    d.text(((W-pw)/2, H-92), phys, fill=INK, font=f_phys)
    # --- halftone stipple field behind the title zone
    stip = np.zeros((H, W, 4))
    yy, xx = np.mgrid[0:H, 0:W]
    zone = np.exp(-(((xx-1050)/560.0)**2 + ((yy-540)/260.0)**2))
    cell = ((xx // 14) * 7919 + (yy // 14) * 104729) % 97
    dots = (cell < 34) & (zone > 0.30)
    stip[dots, 0:3] = INK; stip[dots, 3] = (zone[dots] * 70).astype(float)
    img = Image.alpha_composite(img, Image.fromarray(stip.astype(np.uint8)))
    img = dropout_streaks(img.convert("RGB"), n=3)
    # --- press pass
    a = xerox(np.array(img.convert("RGB")).astype(float))
    a = np.clip((a - 0.5) * 1.10 + 0.5, 0, 1)
    a = a ** 0.72
    a = toner(a * 255)
    return Image.fromarray(a.astype(np.uint8))

if __name__ == "__main__":
    av = avatar_master()
    av.save("/root/workspace/voidfag-art/out/002-avatar-master.png")
    av.resize((400, 400), Image.LANCZOS).save("/root/workspace/voidfag-art/out/002-avatar-400.png")
    av.resize((24, 24), Image.NEAREST).resize((192, 192), Image.NEAREST).save("/root/workspace/voidfag-art/out/002-avatar-24test.png")
    bn = banner_master()
    bn.save("/root/workspace/voidfag-art/out/002-banner-master.png")
    bn.resize((1500, 500), Image.LANCZOS).save("/root/workspace/voidfag-art/out/002-banner-1500x500.png")
    print("rendered. seed", SEED, "· 0 steps · no model")
