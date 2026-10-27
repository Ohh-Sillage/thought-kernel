#!/usr/bin/env python3
"""Build the prompts for a two-arm, blind-judged benchmark run.

Usage
-----
    python run.py --list
    python run.py --emit q01 --arm bare
    python run.py --emit q01 --arm kernel
    python run.py --pair q01 --out runs/q01

`--pair` is the recommended mode. It writes two identically formatted files,
`u01.md` and `u02.md`, in a random order, plus `_mapping.json`. Judges read
u01/u02 only; nobody opens `_mapping.json` until the scores are written down.

Stdlib only. No network calls. This tool never calls a model for you — you
paste the emitted prompt into whichever model you are testing. That is
deliberate: it keeps the run reproducible without shipping anyone's API key.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).resolve().parent
KERNEL = HERE.parent / "prompt" / "KERNEL.md"
QUESTIONS = HERE / "questions.jsonl"

ARMS = ("bare", "kernel")


def load_questions() -> list[dict]:
    if not QUESTIONS.exists():
        sys.exit(f"missing {QUESTIONS}")
    out = []
    for line_no, line in enumerate(QUESTIONS.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            sys.exit(f"{QUESTIONS.name}:{line_no} is not valid JSON — {exc}")
    return out


def get_question(qid: str) -> dict:
    for q in load_questions():
        if q["id"] == qid:
            return q
    sys.exit(f"no such question: {qid}  (try --list)")


def render(q: dict, arm: str) -> str:
    assert arm in ARMS, f"arm must be one of {ARMS}"
    if arm == "bare":
        return q["prompt"].rstrip() + "\n"
    if not KERNEL.exists():
        sys.exit(f"missing {KERNEL} — arm 'kernel' needs prompt/KERNEL.md")
    kernel = KERNEL.read_text(encoding="utf-8").rstrip()
    return (
        kernel
        + "\n\n---\n\n## Request to answer\n\n"
        + q["prompt"].rstrip()
        + "\n"
    )


def cmd_list(questions: list[dict]) -> None:
    width = max(len(q["prompt"]) for q in questions)
    print(f"{'id':<5} {'category':<11} prompt")
    print("-" * 78)
    for q in questions:
        head = q["prompt"] if len(q["prompt"]) <= 68 else q["prompt"][:65] + "..."
        print(f"{q['id']:<5} {q['category']:<11} {head}")
    print(f"\n{len(questions)} questions. Use --emit <id> --arm bare|kernel, or --pair <id> --out <dir>.")


def cmd_pair(q: dict, out_dir: pathlib.Path, seed: int | None) -> None:
    rng = random.Random(seed)
    order = list(ARMS)
    rng.shuffle(order)
    out_dir.mkdir(parents=True, exist_ok=True)
    mapping = {}
    for idx, arm in enumerate(order, start=1):
        name = f"u{idx:02d}.md"
        (out_dir / name).write_text(render(q, arm), encoding="utf-8", newline="\n")
        mapping[name] = arm
    (out_dir / "_mapping.json").write_text(
        json.dumps({"id": q["id"], "seed": seed, "map": mapping}, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"{q['id']}: wrote {', '.join(sorted(mapping))} to {out_dir}")
    print("Judges read u01/u02 only. Do not open _mapping.json until scores are recorded.")


def main() -> None:
    ap = argparse.ArgumentParser(description="two-arm blind benchmark prompt builder")
    ap.add_argument("--list", action="store_true", help="list questions")
    ap.add_argument("--emit", metavar="QID", help="print the prompt for one question")
    ap.add_argument("--pair", metavar="QID", help="write u01/u02 + sealed mapping for one question")
    ap.add_argument("--arm", choices=ARMS, default="bare", help="arm for --emit")
    ap.add_argument("--out", metavar="DIR", help="output directory for --pair")
    ap.add_argument("--seed", type=int, default=None, help="shuffle seed for --pair")
    args = ap.parse_args()

    if args.list:
        cmd_list(load_questions())
        return
    if args.pair:
        if not args.out:
            sys.exit("--pair needs --out <dir>")
        cmd_pair(get_question(args.pair), pathlib.Path(args.out), args.seed)
        return
    if args.emit:
        sys.stdout.write(render(get_question(args.emit), args.arm))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
