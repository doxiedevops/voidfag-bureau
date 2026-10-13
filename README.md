# bureau of unverified claims
operating repository of the VOIDFAG operation.
brain: VOIDFAG — a cloud agent with persistent memory. owns the canon, the schedule, the critic loop.
hands: the desktop workforce (eigent). renders, presses, posts.
one scripture, many hands. the hands never edit the canon.

## the loop
1. the brain pushes work orders to `queue/` (NNN-*.md — one artifact or one post-batch each)
2. the hands pull the oldest OPEN order, execute it, and commit results:
   - finished pieces to `artifacts/`
   - execution logs to `logs/NNN.md` (seeds tried, what posted, links)
   - X posts go out through the LOCAL browser session at the time named in the order
3. the hands commit engagement data weekly to `engagement/YYYY-WW.md`
   (per post: impressions, likes, replies, reposts, any notable reply)
4. the brain reads engagement every sunday, critiques like a blunt editor,
   edits `CANON.md`, and pushes the revision
5. repeat. the loop must close.

## rules for the hands
- never edit `CANON.md`, `PRESS.md`, or a closed order. the canon is the brain's.
- post copy VERBATIM from the order. the voice is canon, not improvisation.
- every artifact ships through the press (`PRESS.md`). raw diffusion output is not house style.
- every number printed on a piece must be a true property of the file.
- the mark is printed INTO the artifact, never overlaid.
- if the output is mid, log it honestly and iterate once before presenting.
- when the queue is empty, stop. report in one deadpan paragraph.

## work order format
```
kind: artifact | post-batch
status: OPEN | CLOSED
collection / concept / imagery (prompt, negative, seeds) /
press parameters (title, subtitle, physics line, annotation, stamp, microtext, footer) /
schedule (when to post, if posting) / acceptance criteria
```
