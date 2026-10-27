<div align="center">

# ThoughtKernel
### 思想内核 — a portable kernel of thinking for LLMs

**Most prompt tools sell you technique. This one ships a kernel — and tells you exactly where the kernel loses.**

[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)](CHANGELOG.md)
[![No telemetry](https://img.shields.io/badge/telemetry-none-brightgreen.svg)](#privacy)

[Demo](demo/index.html) · [Install](#install-in-30-seconds) · [What we measured](#what-we-measured-and-where-it-fails) · [中文说明](README.zh-CN.md)

</div>

---

## The problem is not that you don't know Feynman

Everyone has heard of Feynman technique, pre-mortems, and red-teaming. Three things still go wrong in practice:

1. **You don't think of the right one at the right moment.**
2. **Knowing it isn't the same as writing it correctly** — every time you hand-write the role, the flow, the constraints.
3. **Strength is never tuned.** The same method used for a career decision and for a typo fix should not carry the same force.

ThoughtKernel turns "which scenario → which thinking models → how much pressure" into a lookup, and shrinks the whole thing to a **kernel you can port to any host**: a Claude Skill, a Cursor rule, a system prompt, a browser panel.

---

## Three principles (the part that transfers)

The techniques are disposable. These three are not — they apply to agent orchestration, RAG pipelines, and workflow engines just as well.

**1. Gate before technique.**
Doing nothing is a valid, correct output. Most prompt-enhancement tools fail because they do *something* to every message. ThoughtKernel runs a **gap test** first: after the shortest correct answer, would the user still ask *why / how / which / anything else*? If no → `skip`, no framework, no closing tip.

**2. Subtractability — if you can't delete it, it isn't architecture.**
Three layers: kernel → scenario packs → profile. Delete any pack and the kernel still degrades gracefully into a generic fallback. Boundaries are drawn by mutual *non-applicability signals*, not by priority ordering — so no pack can "win" by being listed earlier.

**3. Inject constraints, don't rewrite content.**
Three injection forms — `wrap` (rewrite the prompt's constraints), `inject` (silent, shapes reasoning only), `interactive` (turn it into a dialogue). None of them replace what the user actually asked for. The user's intent is the invariant; only the pressure around it changes.

> Derived from (1): **strength follows stakes.** Same method, different force — an irreversible decision gets full pressure, a throwaway query gets one sentence.

---

## What's inside

| | Count | What |
|---|---|---|
| 🧠 **Thinking models** | 25 | 13 human-side (H1–H13, reshape how you ask) + 12 machine-side (M1–M12, shape how the model reasons) |
| 🎯 **Scenarios** | 9 + fallback | learning, planning, decision, debugging, writing, coding, refactor, research, review |
| 🎚️ **Modes** | 3 | `efficiency` / `balanced` / `accuracy` — the only knob most users ever touch |
| 📦 **Scenario packs** | 5 | coding, debugging, planning, refactor, writing — 8 fixed fields each |

Machine-side models are algorithms borrowed from CS — divide & conquer, pruning, memoization, state abstraction, feedback control, Occam's razor. They are *injected silently*: the model follows them, it does not narrate them.

---

## Install in 30 seconds

### A. Claude Code / Claude Skills / WorkBuddy

```bash
git clone https://github.com/<your-handle>/thought-kernel.git
cp -r thought-kernel/skill ~/.claude/skills/thought-kernel
```

Then just talk:

```
Learn Transformer positional encoding with me using Feynman technique
Plan this project — but don't give me a plan yet
Should I take this offer? Argue both sides
Use efficiency mode from now on
```

### B. Cursor / Windsurf / rule-based hosts

Copy `prompt/KERNEL.md` into your rules file (`.cursor/rules/thought-kernel.mdc`). It is self-contained — no relative links, no host-specific syntax.

### C. Any model, zero install

Open [`demo/index.html`](demo/index.html) in a browser, or paste `prompt/KERNEL.md` as a system prompt. Both produce the same constraints.

See [`GETTING_STARTED.md`](GETTING_STARTED.md) for host-by-host details and failure modes.

---

## Architecture

```
kernel     gate · modes · assembly · output protocol · fallback · honesty
  │        (knows no scenario content — only pack ids)
  ▼
packs      5 scenarios × 8 fixed fields
  │        (id / applies-when / not-applicable / deliverable / injects /
  ▼         hard constraints / failure boundary / self-checks)
profile    terminology, example domain, tone — not enabled yet
```

The split exists because an earlier version scattered one scenario's knowledge across five files: change one, miss two, and they eventually contradicted each other. Now scenarios can only be separated by *not-applicable* signals, never by ordering.

---

## What we measured (and where it fails)

We benchmarked this. The result was not flattering, so it is the first thing on the page.

**Setup.** 9 real questions sampled from agent-session logs (*writing / coding / debugging*, 3 each) × 2 arms (bare model vs. model + skill) × 2 independent blind judges. The two answers to the same question were shuffled into U01/U02; judges never knew which arm produced which. 20-point scale. Noise band ±0.67; only |Δ| > 1.34 counts as a real difference.

**Result.**

| Judge | Δ (skill − bare) |
|---|---|
| A | −1.33 |
| B | −1.44 |
| **mean** | **−1.39** |

**7 of 9 tasks were judged worse by both judges.** The skill did not make answers better. It made them worse.

**Why — reading the outputs, not the scores:**

- **"Don't fabricate" became "hand back a blank form."** Asked to fill in resume project entries, the bare model wrote a finished draft (with two invented numbers, correctly penalised). The skill wrote a *skeleton* of placeholders and taught the user how to fill it. Fabrication dropped; usability dropped further.
- **A delivery contract applied to a small glitch became overhead.** Asked about flickering tray icons on Windows, the bare model gave a 3-step fix. The skill opened with "stop touching the registry, first do loss-control → evidence → localisation" — structurally better, practically worse, because the user wanted their icons back.

**What happened next.** Both failure modes were patched: placeholders may occupy *values*, never *whole sections*; a small operational glitch does not get a delivery contract. On the same benchmark the skill then **tied** the bare model — it stopped losing, it did not start winning. Two new failure shapes appeared (inventing file paths, routing around security tooling); both are now hard prohibitions in the kernel.

**What we have not done.** We have not re-run the 9-task benchmark at v1.6.0. Until we do, treat every claim above as the v1.5.x measurement, not a v1.6.0 result. The numbers live in this repo's [`bench/`](bench/) so you can disagree with them.

---

## So what does it actually buy you

Not a higher score. **A different shape.**

- Questions you didn't ask get surfaced as a ranked list instead of being silently dropped.
- Assumptions are labelled as assumptions, so you can veto them.
- Trivial requests stay trivial — the gate keeps the framework out of the way.
- Outputs come with a stated boundary: *this holds under X, flips under Y.*

If you want "answers get better, period", do not install this. If you want "fewer things I forgot to consider, and I can see what was assumed", it does that reliably. That is a smaller claim than the one most prompt packs make, and it is the one that survived measurement.

---

## Run the benchmark yourself

```bash
cd bench
python run.py --list                 # 10 questions, 3 categories
python run.py --emit 01 --arm bare   # prints the prompt to run
python score.py                      # Δ table once you fill in scores.md
```

`bench/` ships the questions, an empty scoring sheet, and the Δ arithmetic. It ships **no answers** — we are not going to hand you outputs to rubber-stamp. See [`bench/README.md`](bench/README.md).

---

## What is *not* here

- **No telemetry, no network calls, no key handling.** Plain text in, plain text out.
- **No "25 techniques will 10x your output".** See the measurement section.
- **No prompt-injection defence.** If your host is compromised, a text kernel will not save you.
- **No non-English templates in `demo/` yet.** The scenario packs are bilingual-ready, the panel is Chinese-first. Tracked in [CHANGELOG](CHANGELOG.md).

---

## Attribution

The 25 thinking models are **not original**. Feynman technique, Socratic questioning, pre-mortems, red-teaming, divide-and-conquer, pruning, memoization — all public, long predating this repo. What is claimed here is only the **selection, the boundaries where each one fails, and the assembly** (gate → scenario → strength → injection).

If you find an attribution missing, open an issue; it will be added.

---

## License

[MIT](LICENSE). Copy it, fork it, sell it, rename it. Stars are nice but not required.
