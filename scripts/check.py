#!/usr/bin/env python3
"""Structural checks for this repo. Deliberately dumb — it cannot tell you whether a rule is good.

Checks:
  1. skill/SKILL.md has the required frontmatter keys and a semver version
  2. every relative markdown link resolves to a file that exists
  3. every scenario pack has the 8 contract fields
  4. no stale project codename remains outside the changelog
  5. required root files exist

Prints what it actually inspected, so a pass cannot be mistaken for a check of
some other copy of the repo.

    python scripts/check.py
    python scripts/check.py --quiet
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED_ROOT = [
    "README.md", "README.zh-CN.md", "LICENSE", ".gitignore", "CHANGELOG.md",
    "CONTRIBUTING.md", "GETTING_STARTED.md",
]
REQUIRED_SKILL = [
    "skill/SKILL.md",
    "skill/references/modes.md",
    "skill/references/difficulty.md",
    "skill/references/thoughts.md",
    "skill/references/scenario-map.md",
    "skill/references/prompt-templates.md",
    "skill/references/special-directions.md",
    "skill/references/packs/_contract.md",
]
LINK = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)")
IMG = re.compile(r"""<img[^>]+src=["']([^"']+)["']""", re.IGNORECASE)
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
STALE = re.compile(r"\bpromat\b", re.IGNORECASE)

errors: list[str] = []
checked: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def check_root() -> None:
    for rel in REQUIRED_ROOT:
        p = ROOT / rel
        if not p.exists():
            fail(f"missing required file: {rel}")
        else:
            checked.append(rel)


def check_skill() -> None:
    for rel in REQUIRED_SKILL:
        p = ROOT / rel
        if not p.exists():
            fail(f"missing required skill file: {rel}")
        else:
            checked.append(rel)

    skill = ROOT / "skill/SKILL.md"
    if not skill.exists():
        return
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("skill/SKILL.md must start with a --- frontmatter block")
        return
    end = text.find("\n---", 4)
    if end == -1:
        fail("skill/SKILL.md frontmatter block is not closed")
        return
    front = text[4:end]
    for key in ("name:", "description:", "version:"):
        if key not in front:
            fail(f"skill/SKILL.md frontmatter missing {key}")
    m = re.search(r"^version:\s*(\S+)", front, re.MULTILINE)
    if m and not SEMVER.match(m.group(1).strip().strip('"')):
        fail(f"skill/SKILL.md version is not semver: {m.group(1)}")
    name = re.search(r"^name:\s*(\S+)", front, re.MULTILINE)
    if name and name.group(1).strip() != "thought-kernel":
        fail(f"skill/SKILL.md name is {name.group(1)!r}, expected 'thought-kernel'")


def check_packs() -> None:
    packs = sorted((ROOT / "skill/references/packs").glob("*.md"))
    if not packs:
        fail("no scenario packs found")
        return
    for p in packs:
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8")
        headings = re.findall(r"^##\s+(\d+)[.\s]", text, re.MULTILINE)
        missing = [n for n in "12345678" if n not in headings]
        if missing:
            fail(f"{p.relative_to(ROOT)} missing contract field(s): {', '.join(missing)}")
        else:
            checked.append(str(p.relative_to(ROOT)))


def check_links() -> None:
    for md in ROOT.rglob("*.md"):
        if any(part in {".git", "node_modules", "bench"} for part in md.parts):
            continue
        text = md.read_text(encoding="utf-8")
        # strip fenced code blocks so examples are not treated as links
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        targets = LINK.findall(text) + IMG.findall(text)
        for target in targets:
            target = target.split(" ")[0].strip()
            if target.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                fail(f"broken link in {md.relative_to(ROOT)}: {target}")


def check_stale_name() -> None:
    for md in ROOT.rglob("*.md"):
        if any(part in {".git", "node_modules"} for part in md.parts):
            continue
        if md.name == "CHANGELOG.md":
            continue
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if STALE.search(line):
                fail(f"stale codename in {md.relative_to(ROOT)}:{i}: {line.strip()[:70]}")


def main() -> None:
    quiet = "--quiet" in sys.argv
    check_root()
    check_skill()
    check_packs()
    check_links()
    check_stale_name()

    if not quiet:
        print(f"[guard] repo: {ROOT}")
        print(f"[guard] files inspected: {len(checked)}")
        for rel in checked:
            print(f"  ok  {rel}")

    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print(f"  FAIL  {e}")
        sys.exit(1)
    print(f"\nPASS — {len(checked)} structural checks, {len(errors)} problems.")
    print("This checks structure only. It cannot tell you whether a rule is good.")


if __name__ == "__main__":
    main()
