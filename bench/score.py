#!/usr/bin/env python3
"""Compute the per-judge delta from a filled-in scores.md.

`score.py` reads the markdown table in scores.md, ignores empty cells, and
reports:

    Δ = mean(kernel) - mean(bare)

separately for each judge, then averaged across judges. It prints the noise
band so a small delta cannot be mistaken for a result.

Stdlib only. No network. No model calls.
"""

from __future__ import annotations

import pathlib
import re
import sys

SCORES = pathlib.Path(__file__).resolve().parent / "scores.md"
NOISE = 0.67          # single-judge noise band, from repeated-judge calibration
DECISION = 2 * NOISE  # 1.34 — only beyond this is a real difference claimed

ROW = re.compile(r"^\|\s*(q\d{2})\s*\|(.*)\|\s*$")


def parse_scores() -> dict[str, dict[str, float]]:
    if not SCORES.exists():
        sys.exit(f"missing {SCORES}")
    text = SCORES.read_text(encoding="utf-8")
    header = None
    data: dict[str, dict[str, float]] = {}
    for line in text.splitlines():
        if line.startswith("|") and "id" in line.lower() and header is None:
            header = [c.strip() for c in line.strip("|").split("|")]
            continue
        m = ROW.match(line.strip())
        if not m or header is None:
            continue
        qid = m.group(1)
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) != len(header) - 1:
            sys.exit(f"{qid}: expected {len(header) - 1} score cells, found {len(cells)}")
        row: dict[str, float] = {}
        for col, cell in zip(header[1:], cells):
            if cell == "":
                continue
            try:
                row[col] = float(cell)
            except ValueError:
                sys.exit(f"{qid}/{col}: not a number: {cell!r}")
        if row:
            data[qid] = row
    return data


def main() -> None:
    data = parse_scores()
    if not data:
        print("No scores yet. Fill in scores.md, then run this again.")
        return

    cols = sorted({c for row in data.values() for c in row})
    judges = sorted({c.split(":")[-1] for c in cols if ":" in c})
    if not judges:
        print("Column names must look like 'bare:A' and 'kernel:A'. Found:", ", ".join(cols))
        return

    print(f"{'id':<5}" + "".join(f"{j:>9}" for j in judges))
    print("-" * (5 + 9 * len(judges)))
    per_judge: dict[str, list[float]] = {j: [] for j in judges}
    for qid in sorted(data):
        cells = []
        for j in judges:
            bare = data[qid].get(f"bare:{j}")
            kernel = data[qid].get(f"kernel:{j}")
            if bare is None or kernel is None:
                cells.append("     --")
                continue
            d = kernel - bare
            per_judge[j].append(d)
            cells.append(f"{d:>+9.2f}")
        print(f"{qid:<5}" + "".join(cells))

    print()
    means = []
    for j in judges:
        vals = per_judge[j]
        if not vals:
            print(f"judge {j}: no complete pairs")
            continue
        m = sum(vals) / len(vals)
        means.append(m)
        print(f"judge {j}: n={len(vals):<3} Δ = {m:+.2f}")
    if not means:
        return
    total = sum(means) / len(means)
    print(f"mean Δ (kernel − bare) = {total:+.2f}   [{len(means)} judge(s)]")
    print()
    if abs(total) < NOISE:
        verdict = "no signal — inside the ±0.67 noise band. Do not claim an effect."
    elif abs(total) < DECISION:
        verdict = "weak signal — between noise and the 1.34 decision threshold. Do not claim an effect."
    else:
        verdict = f"real difference — |Δ| > {DECISION}, direction {'better' if total > 0 else 'worse'} with kernel."
    print(verdict)
    print("Reminder: this measures answer quality on 10 self-authored questions.")
    print("It is not a general claim about the tool's value, and self-authored questions flatter the tool.")


if __name__ == "__main__":
    main()
