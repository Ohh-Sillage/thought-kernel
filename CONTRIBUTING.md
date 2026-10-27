# Contributing

The most useful contribution is not code. It is a **failure report**.

## Highest value: gate failures

The kernel's whole thesis is *"decide whether to do anything before doing it"*. So the worst bug it can have is doing the wrong amount:

- added a framework to a one-line question → should have been `skip`
- handed back a skeleton when a draft was asked for → should have been a draft
- stayed silent on something irreversible → should have forced `accuracy`

Open an issue with **the exact message you sent** and **what it did instead**. Redact anything private; the judgement usually survives redaction. These reports go straight into the gate rules, and the reporter is credited in `CHANGELOG.md` unless they ask not to be.

## Adding a thinking model

A thinking model is only accepted if it brings its **failure boundary** with it. A model without a stated "when this makes things worse" is not added — that column is the entire value of the library.

To propose one, open the *New thinking model* issue and fill in:

| Field | Why it is required |
|---|---|
| Name and origin | If it is not yours, cite it. Attribution is checked. |
| Side | `H` (changes how the user asks) or `M` (shapes how the model reasons) |
| Mode | `wrap` / `inject` / `interactive` |
| One-line principle | Mechanism, not marketing. "Explaining exposes gaps" — yes. "Unlock your potential" — no. |
| Trigger | The observable signal that should select it |
| **Failure boundary** | When using it is worse than not using it |
| Overlap check | Which existing model does something similar, and why both should exist |

## Adding a scenario pack

Packs live in `skill/references/packs/`. Each has 8 fixed fields and is validated by the contract in `_contract.md`. Two rules that are not negotiable:

1. **Boundaries by non-applicability, not priority.** If your pack can only be selected by being listed earlier, it is not a pack.
2. **Deleting your pack must not break anything.** The kernel falls back to the generic shape.

## Local checks

```bash
# every reference resolves, no placeholder text left, frontmatter valid
python scripts/check.py

# bench still runs
cd bench && python run.py --list && python score.py
```

`scripts/check.py` is intentionally dumb: it checks structure, not judgement. Nothing in this repo can check whether a rule is *good* — that only comes from someone reporting it misfired.

## Style

- English in `README.md`, Chinese in `README.zh-CN.md`. They are not translations of each other; each is written for its own readers. Keep it that way.
- Rules are written as decisions with a test, not as advice. `"Answer is one thing (a number, a command, a link) → zero gap"` is a rule. `"Be concise"` is not.
- If you cannot say what would falsify a rule, it does not belong in the kernel.

## Licence

By contributing you agree your contribution is licensed under [MIT](LICENSE). No CLA.
