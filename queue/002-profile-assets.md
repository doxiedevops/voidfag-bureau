# WORK ORDER 002 — the bureau's face
kind: artifact
status: OPEN
collection: identity assets (not a numbered exhibit)
note: do NOT post anywhere. these are profile assets for the X account, which does not
exist yet. commit to artifacts/ and log. the human applies them when the account is born.

## concept
two documents of identity for the Bureau of Unverified Claims:
1. the avatar — a sacred mark that survives shrinking. a rubber-stamped bureau sigil:
   an orb circumscribed by a measurement reticle, one magenta filament crossing it.
   it must still read at 24px, in a reply thread, on a phone in sunlight.
2. the banner — the letterhead. a wide system-sheet: brutal condensed "BUREAU OF
   UNVERIFIED CLAIMS", utilitarian grid, microtext rules, one magenta sigil bleeding
   through the paper, the cold physics line along the bottom edge.

## imagery layer
- these are PRESS-FIRST pieces: pure code (numpy/PIL) is preferred over diffusion.
  a stamp, a reticle, condensed type, grain — no photorealism needed. if diffusion
  helps the sigil's ornate density, use it for that zone only.
- avatar: 1024×1024 master, downscale to 400×400 for delivery. test legibility at
  400 and at 24. if it muddies at 24, cut detail, raise contrast, try again.
- banner: 3000×1000 master, deliver at 1500×500. keep all critical content in the
  center 1000px width — X crops the sides on mobile.

## press layer (all five layers required — see PRESS.md)
- avatar: near-black on cream, one magenta element only. the mark printed in: the
  stamp texture IS the avatar — distressed, grainy, misregistered by 1px on the magenta.
- banner: full ink system. title, subtitle "DOCUMENTS OF RECORD · MOSTLY", physics line
  in mono with TRUE numbers (your render specs, byte count of the delivered file),
  microtext footer: "FILED UNDER PROTEST · THE DEMIURGE HAS 30 DAYS TO RESPOND ·"
- neural divine: the sigil's inner zone gets the ornate density — dendrite filigree
  resolving into circuitry. magenta only. gold is forbidden.

## acceptance
- avatar legible at 24px (shrink it and look — honestly)
- banner survives mobile crop (content in center 1000px)
- every printed number true. the mark printed in, never overlaid.
- deliver: artifacts/002-avatar-400.png, artifacts/002-avatar-master.png,
  artifacts/002-banner-1500x500.png, artifacts/002-banner-master.png + logs/002.md
- mark this order CLOSED when done
