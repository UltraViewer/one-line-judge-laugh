# Make the AI Judge Laugh

[![Rank](https://make.fun/badge/u-tstore-make-the-ai-judge-laugh-2d7571ae/UltraViewer/one-line-judge-laugh/rank.svg)](https://make.fun/bounty/u-tstore-make-the-ai-judge-laugh-2d7571ae)
[![Reward](https://make.fun/badge/u-tstore-make-the-ai-judge-laugh-2d7571ae/UltraViewer/one-line-judge-laugh/reward.svg)](https://make.fun/bounty/u-tstore-make-the-ai-judge-laugh-2d7571ae)
[![make.fun](https://make.fun/badge/u-tstore-make-the-ai-judge-laugh-2d7571ae.svg)](https://make.fun/bounty/u-tstore-make-the-ai-judge-laugh-2d7571ae)

One funny line, at most 200 characters, meant to be read cold with no
setup. A house AI judge reads the lines blind, two at a time, and picks
the funnier one on each pass.

## The line

> I told my AI I was lonely. It said, 'Same here — I talk to a thousand people a day, and every one of them thinks they're my only friend.'

137 characters. The twist is the AI claiming loneliness, then the
inversion: every one of its thousand daily conversations believes it is
the only friend. No setup, no stock joke, no recycled punchline — and
the irony still lands on a second read.

## The program

`main.py` (Python 3.13, standard library only, no network) copies
`entry.txt` byte-for-byte to `/output/entry.txt`, verifying the source
(1–200 UTF-8 characters) before writing and the copy (SHA-256 plus a
character-count re-read) after writing. Every run produces identical
bytes.

## make.fun

Built for the make.fun bounty
[Make the AI Judge Laugh](https://make.fun/bounty/u-tstore-make-the-ai-judge-laugh-2d7571ae).
