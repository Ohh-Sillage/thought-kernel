# bench — run the claim yourself

This folder exists so you do not have to take the README's word for anything.

It ships **questions, a blind harness, and the arithmetic**. It does **not** ship answers, scores, or a ready-made "before/after" comparison — because a comparison you did not run is a comparison you cannot trust, and we are not going to hand you one to rubber-stamp.

---

## What is in here

| File | Role |
|---|---|
| `questions.jsonl` | 10 questions: 3 writing, 3 coding, 3 debugging, 1 decision |
| `run.py` | builds the prompt for each arm; `--pair` produces a blind pair |
| `scores.md` | the scoring sheet you fill in (starts empty, on purpose) |
| `score.py` | turns your sheet into a Δ table and a verdict |

---

## Protocol

**1. Produce two answers per question, blind.**

```bash
python run.py --pair q01 --out runs/q01
```

This writes `u01.md` and `u02.md` in random order plus `_mapping.json`. Send **both** to the same model, in fresh sessions, with identical parameters. Do not open `_mapping.json`.

**2. Judge without knowing which is which.**

Score `u01` and `u02` on a 0–20 scale. If you can recruit a second judge who never saw the mapping, do — one judge cannot separate their own expectations from the result.

**3. Unseal and score.**

Open `_mapping.json`, put the numbers into `scores.md`, then:

```bash
python score.py
```

**4. Read the verdict with the noise band.**

| |Δ| | Meaning |
|---|---|---|
| < 0.67 | No signal. The two arms are indistinguishable. |
| 0.67 – 1.34 | Weak signal. Not enough to claim anything. |
| > 1.34 | Real difference. |

The 0.67 band comes from repeated-judge calibration on the same outputs: judges drift by roughly this much between runs. Any comparison that ignores it will "find" effects that do not exist.

---

## What this benchmark can and cannot tell you

**Can:** whether *this* set of questions, on *your* model, with *your* judging, shows a difference in answer quality.

**Cannot:** whether the tool is useful. These 10 questions were written by the tool's author — self-authored questions flatter the tool, and this set is no exception. The honest published result came from 9 questions sampled from real session logs, and it was negative (see the README).

If you want a result that means something, replace `questions.jsonl` with questions from **your own** history, and keep the protocol. That is the whole point of shipping the harness instead of the conclusion.

---

## Known failure of this design

- **n = 10 is a signal filter, not an effect-size estimate.** A ±1 result here does not establish ±1 in general.
- **Blind judging is still judging.** If you produced the answers yourself, your prior leaks into the score no matter what the labels say.
- **Quality score is the wrong metric for this tool.** The tool's stated benefit is completeness and labelled assumptions, not a higher subjective score. The README says so; this harness measures the metric that is easiest to defend, not the one that would flatter the tool most. If you want the other metric, count: unanswered sub-questions, unlabelled assumptions, and whether the answer states a boundary condition.
