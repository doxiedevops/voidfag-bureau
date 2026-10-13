# PRESS — the house finishing pipeline
two layers. raw diffusion output is not house style; everything ships through the press.

## layer 1 — imagery
- detect hardware first. GPU (CUDA or Apple MPS) → SDXL or flux.1-schnell via diffusers.
  CPU-only → SD1.5-class LCM (Lykon/dreamshaper-8-lcm, 4-8 steps, guidance ~1.5).
- prompt register: liminal sacred spaces, dark surreal, chiaroscuro, monochrome + one
  magenta light source, film grain.
- negative: text, watermark, signature, frame, border, oversaturated, colorful.
- generate at least 4 variants (different seeds), curate by eye, keep the best. log all seeds.

## layer 2 — the press (in order)
1. xerox levels crush: black point ~18, white point ~236, gamma ~0.9
2. duotone ramp: shadows → near-black #0A0510, highlights → cream #F2EDE4
3. snap magenta-ish hues to pure #FF00D4
4. misregistration: offset the magenta plate a few px + a faint photocopy ghost
5. toner grain, dropout streaks, worn darkened edges, subtle scanlines
6. contrast-boost after curation: levels stretch + power curve ~0.72
   (timid intensity = mid-gray mush. this was paid for in rejections.)
7. the ornament pass (neural divine): one focal zone gets neural filigree — recursive
   branching (dendrite/circuit traces) in magenta at 2-3 scales, symmetric enough to feel
   holy, dense enough to feel grown. gold is forbidden; the divine here is magenta.
8. measurement honesty (hal): every printed number is computed from the piece itself —
   byte count, seed, centroid, sample counts. no decorative numbers. one cold physics
   line in mono, e.g. "7 sources · 4096 samples · consensus 0.82 · seed 137".
9. the mark printed in (nous): stamps and seals pass through the same grain, decay and
   misregistration as the inks. never a clean digital overlay.
10. typography: brutal condensed caps for titles (render wide, squeeze horizontally if
    no condensed face exists), monospace for data, banknote microtext as texture.

## craft lessons (paid for in rejections)
- iterate in states, like printmaking. state I → state II → …
- one impossible color on a dead field. no pretty, just wrong.
- if it's mid, say so before the human does. then fix the contrast.

## the code
- `press/imprint.py` — reference finishing pass (numpy/PIL, runs on CPU)
- `press/gen004_local.py` — reference CPU generator (dreamshaper-8-lcm)
- adapt freely to your hardware. the SPEC is the canon; the code is a starting point.
