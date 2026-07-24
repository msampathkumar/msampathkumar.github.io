#!/usr/bin/env python3
"""Scaffold a new blog post — fast-forward blogging.

Creates ``docs/writing/<section>/<slug>/index.md`` (folder-per-post, so images
and other assets live right next to the post) with valid front matter and a
starter skeleton, then prints the nav line to paste under the relevant
"Writing" section in mkdocs.yml. The post shows up on the Home page
automatically (via hooks/latest_posts.py) as soon as it has a title and date.

Usage:
    python scripts/new_post.py "My Great Title" --section a2a
    python scripts/new_post.py "My Great Title" --section technical \
        --category "AI" --description "..."
    make new-post TITLE="My Great Title" SECTION="a2a"

Sections map to /writing/<section>/: a2a, cloud-next-2026, gemini, technical,
personal (add a new one deliberately — it becomes part of the public URL).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITING = ROOT / "docs" / "writing"
SECTIONS = ["a2a", "cloud-next-2026", "gemini", "technical", "personal"]


def slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    return re.sub(r"[\s_-]+", "-", slug).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new blog post.")
    parser.add_argument("title", help="Post title")
    parser.add_argument(
        "--section",
        default="technical",
        help=f"Writing section (URL segment). Common: {', '.join(SECTIONS)}",
    )
    parser.add_argument("--slug", help="Override the auto-generated slug")
    parser.add_argument(
        "--category", action="append", default=[], help="Category (repeatable)"
    )
    parser.add_argument("--description", default="", help="SEO/agent description")
    args = parser.parse_args()

    section = slugify(args.section)
    slug = args.slug or slugify(args.title)
    path = WRITING / section / slug / "index.md"
    if path.exists():
        parser.error(f"{path.relative_to(ROOT)} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)

    today = _dt.date.today().isoformat()
    categories = args.category or ["AI"]
    cat_yaml = "\n".join(f"  - {c}" for c in categories)

    path.write_text(
        f"""---
title: "{args.title}"
description: "{args.description}"
date: {today}
authors:
  - sampathm
categories:
{cat_yaml}
---

# {args.title}

<!-- Agents-first: lead with the answer, then the reasoning. Keep headings
     descriptive, prefer runnable code, and state prerequisites explicitly. -->

## TL;DR

_One-paragraph summary an agent (or a busy human) can act on._

## Details

Write here.
""",
        encoding="utf-8",
    )

    print(f"Created {path.relative_to(ROOT)}")
    print("Put any images for this post right in that folder and reference them")
    print("by bare filename, e.g. ![](diagram.png).")
    print("\nAdd this line under the right section in mkdocs.yml (nav > Writing):")
    print(f'          - "{args.title}": writing/{section}/{slug}/index.md')
    print("\nIt will also appear on the Home page automatically after a rebuild.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
