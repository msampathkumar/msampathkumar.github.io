#!/usr/bin/env python3
"""Import dev.to posts into a local staging area for review.

dev.to cross-posts to/from Medium, so pulling from dev.to covers both. This
fetches your published articles' full Markdown into ``_internal/devto_import/``
(git-ignored — nothing is published until you move a file into
``docs/blog/posts/`` and wire it into mkdocs.yml).

- Skips any article whose title already exists on the site (dedupe).
- Adds ``canonical_url`` front matter pointing at the original, to avoid
  duplicate-content SEO penalties.

Usage:
    python scripts/import_devto.py --username sampathm
    python scripts/import_devto.py --username sampathm --force   # include dupes
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "docs" / "blog" / "posts"
STAGE = ROOT / "_internal" / "devto_import"
API = "https://dev.to/api"
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "devto-import/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    return re.sub(r"[\s_-]+", "-", slug).strip("-")


def existing_titles() -> set[str]:
    titles = set()
    for md in POSTS.glob("*.md"):
        m = FRONT_MATTER_RE.match(md.read_text(encoding="utf-8"))
        if not m:
            continue
        tm = re.search(r'^title:\s*"?(.+?)"?\s*$', m.group(1), re.MULTILINE)
        if tm:
            titles.add(_norm(tm.group(1)))
    return titles


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def main() -> int:
    parser = argparse.ArgumentParser(description="Import dev.to posts (staged).")
    parser.add_argument("--username", required=True)
    parser.add_argument("--force", action="store_true", help="include duplicates")
    args = parser.parse_args()

    STAGE.mkdir(parents=True, exist_ok=True)
    have = existing_titles()
    listing = _get(f"{API}/articles?username={args.username}&per_page=1000")
    print(f"Found {len(listing)} articles on dev.to for @{args.username}\n")

    imported = skipped = 0
    for stub in listing:
        title = stub["title"]
        if not args.force and _norm(title) in have:
            print(f"  skip (exists): {title}")
            skipped += 1
            continue

        article = _get(f"{API}/articles/{stub['id']}")
        time.sleep(0.3)  # be polite to the API
        body = article.get("body_markdown") or ""
        body = FRONT_MATTER_RE.sub("", body, count=1).strip()  # drop dev.to fm

        canonical = stub.get("canonical_url") or stub["url"]
        date = (stub.get("published_at") or "")[:10]
        tags = [t.strip() for t in (stub.get("tags") or "").split(",") if t.strip()]
        cats = "\n".join(f"  - {t}" for t in tags) or "  - AI"
        desc = (stub.get("description") or "").replace('"', "'").strip()
        slug = slugify(title)

        out = STAGE / f"{slug}.md"
        out.write_text(
            f"""---
title: "{title}"
description: "{desc}"
date: {date}
authors:
  - sampathm
categories:
{cats}
canonical_url: "{canonical}"
---

> Originally published on [dev.to]({stub["url"]}) / [Medium]({canonical}).

{body}
""",
            encoding="utf-8",
        )
        print(f"  imported: {out.relative_to(ROOT)}")
        imported += 1

    print(f"\nDone. {imported} imported, {skipped} skipped.")
    print(f"Review in {STAGE.relative_to(ROOT)}/ then move keepers into")
    print("docs/blog/posts/ and add them to mkdocs.yml (nav > Writing).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
