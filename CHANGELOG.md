# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is semantic-ish: the third number changes when the kernel's judgement rules change, because that is what breaks behaviour.

## [1.6.0] — 2026-10-27

First public release. Internally this project was codenamed **Promat**; the public name is ThoughtKernel, the package id is `thought-kernel`.

### Added
- Kernel reduced to ~3,000 Chinese characters (from ~8,500). Judgement rules kept, narrative moved out.
- Five scenario packs: `coding`, `debugging`, `planning`, `refactor`, `writing` — 8 fixed fields each, boundaries drawn by mutual non-applicability signals rather than ordering.
- Portable build: `prompt/KERNEL.md`, self-contained, no relative links, for hosts without a skills mechanism.
- Blind bench harness: `bench/run.py --pair` produces anonymised `u01`/`u02` plus a sealed mapping; `bench/score.py` computes Δ against the 0.67 noise band.
- Two hard prohibitions added after observed failures: never cite a file path you have not verified; never route around security software or system services.

### Changed
- Placeholders may occupy a *value*, never a *section*. Deliverables must be usable after replacing values only — this reverses the earlier behaviour that handed back blank forms.
- A small operational fault no longer receives a delivery contract. Structured-but-unhelpful was measurably worse than direct.

### Known issues
- **No benchmark run at 1.6.0.** The published measurement (−1.39) is from the 1.5.x line. Do not attribute it to this version.
- `demo/index.html` is Chinese-first; English templates are not done.
- The decision scenario has no expanded pack — it falls back to the generic kernel.
- `profile` layer (terminology, example domain, tone) is specified but not implemented.

---

## Measurement history

The numbers below are why this project's claims are shaped the way they are. They are listed here rather than buried, because a reader deciding whether to install this should see them before the install instructions.

| Measurement | n | Result |
|---|---|---|
| Real session questions, 2 arms, 2 blind judges | 9 | **−1.39** (judge A −1.33, B −1.44); 7/9 worse by both |
| Same, after fixing both mechanisms | 9 | **±0** — stopped losing, did not start winning |
| Self-authored questions, coding/debugging | — | +3.83 — **not** cited in the README; self-authored sets flatter the tool |

Two failure mechanisms were diagnosed by reading outputs, not scores: "don't fabricate" degrading into "hand back a skeleton", and a delivery contract applied to a one-line operational question.
