#!/usr/bin/env python3
"""Score a blog post for agent-readiness (mechanical checks).

Usage:
    python scripts/score_post.py docs/blog/posts/my-post.md

Prints a 0-100 score plus per-check PASS/WARN/FAIL. This covers the
*mechanical* signals only — structure, front matter, headings, TL;DR,
code, links. Editorial quality (accuracy, novelty, clarity) still needs
human/agent judgement; see the agent-ready-blog skill for the full rubric.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(?P<fm>.*?)\n---\s*\n(?P<body>.*)$", re.DOTALL)


def headings(body: str) -> list[tuple[int, str]]:
    out, fence = [], False
    for line in body.splitlines():
        if re.match(r"^\s*```", line):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6}) (.+)", line)
        if m:
            out.append((len(m.group(1)), m.group(2)))
    return out


def score(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    checks: list[tuple[str, str, int, str]] = []  # name, status, pts, note

    fm = m.group("fm") if m else ""
    body = m.group("body") if m else text

    def add(name, ok, pts, note=""):
        checks.append((name, "PASS" if ok else "FAIL", pts if ok else 0, note))

    # Front matter (25)
    add("front matter present", bool(m), 5)
    add("has title", bool(re.search(r"^title:", fm, re.M)), 5)
    add("has date", bool(re.search(r"^date:", fm, re.M)), 5)
    has_desc = bool(re.search(r"^description:\s*\S", fm, re.M))
    add("has description (agent summary)", has_desc, 5)
    add("has categories/tags", bool(re.search(r"^categories:", fm, re.M)), 5)

    # Structure (35)
    hs = headings(body)
    subs = [h for h in hs if h[0] in (2, 3)]
    add("has >=2 section headings (TOC)", len(subs) >= 2, 20, f"found {len(subs)}")
    single_h1 = sum(1 for h in hs if h[0] == 1) <= 1
    add("at most one H1", single_h1, 5)
    has_tldr = bool(re.search(r"tl;?dr|in short|summary", body, re.I))
    add("has TL;DR / summary", has_tldr, 10)

    # Depth & code (25)
    words = len(re.findall(r"\w+", body))
    add("substantial (>=300 words)", words >= 300, 10, f"{words} words")
    add("has code or diagram", "```" in body, 10)
    add("has outbound links", bool(re.search(r"\]\(https?://", body)), 5)

    # Agent hygiene (15)
    add(
        "canonical_url if imported",
        "canonical_url" in fm or "Originally published" not in body,
        5,
    )
    lead = "\n".join(body.strip().splitlines()[:6])
    add(
        "leads with the answer (early payload)",
        bool(re.search(r"tl;?dr|^\s*[-*]|\b(is|are|means)\b", lead, re.I)),
        10,
    )

    total = sum(c[2] for c in checks)
    print(f"\n=== {path.name} — agent-readiness: {total}/100 ===")
    for name, status, pts, note in checks:
        mark = "OK " if status == "PASS" else "XX "
        extra = f"  ({note})" if note else ""
        print(f"  {mark}{name}{extra}")
    if total < 70:
        print("\nVERDICT: not agent-ready yet — address the XX items above.")
    elif total < 85:
        print("\nVERDICT: decent — a few improvements would help agents.")
    else:
        print("\nVERDICT: agent-ready.")
    return total


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    score(Path(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
