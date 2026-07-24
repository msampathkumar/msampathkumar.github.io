#!/usr/bin/env python3
"""One-time migration: /blog/posts/<slug>/ -> /writing/<section>/<slug>/.

For each post in MAPPING:
  * move docs/blog/posts/<stem>.md -> docs/writing/<section>/<slug>/index.md
  * move every image it references into that same folder (co-located) and
    rewrite the ref from ``images/.../foo.png`` to bare ``foo.png``
Then update the site wiring in one pass:
  * mkdocs.yml nav paths + docs/index.md + docs/about.md internal links
  * mkdocs.yml redirect_maps (old source path -> new source path)
  * docs/llms.txt public URLs

The MAPPING below is the durable record of the old->new mapping. Re-running is
safe: posts already moved are skipped. Run: ``python scripts/migrate_urls.py``.
Then: ``git add -A`` (renames auto-detected) and ``make llms``.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
POSTS = DOCS / "blog" / "posts"

# old stem (docs/blog/posts/<stem>.md) -> (section, new-slug)
# a2a_multi_tenancy was migrated by hand as the pilot and is intentionally omitted.
MAPPING: dict[str, tuple[str, str]] = {
    # Agent-to-Agent (A2A)
    "a2a_intro": ("a2a", "intro"),
    "a2a_v1_release": ("a2a", "v1-release"),
    "a2a_test_kit": ("a2a", "test-kit"),
    "a2a_security_whitepaper": ("a2a", "security-whitepaper"),
    # Google Cloud Next 2026
    "google-cloud-next-2026-agentic-cloud-infrastructure": (
        "cloud-next-2026",
        "infrastructure",
    ),
    "google-cloud-next-2026-gap-foundational-models": (
        "cloud-next-2026",
        "foundational-models",
    ),
    "google-cloud-next-2026-dev-tools-mcp-servers": (
        "cloud-next-2026",
        "dev-tools-mcp-servers",
    ),
    "google-cloud-next-2026-agentic-data-protocols-security": (
        "cloud-next-2026",
        "data-protocols-security",
    ),
    "google-cloud-next-2026-workspace-ai-agents": (
        "cloud-next-2026",
        "workspace-ai-agents",
    ),
    # Gemini Guides
    "gemini-cli-cheatsheet-printouts": ("gemini", "cli-cheatsheets"),
    "gemini-cli-top-commands": ("gemini", "cli-top-commands"),
    "gemini-2.5-flash-image-preview": ("gemini", "flash-image-preview"),
    "gemini-as-your-culinary-guide": ("gemini", "culinary-guide"),
    # Technical Articles
    "the-six-essential-protocols-powering-the-ai-agent-ecosystem": (
        "technical",
        "six-essential-protocols",
    ),
    "the-role-of-python-in-google-cloud": ("technical", "python-in-google-cloud"),
    "advanced-memory-management-agentic-ai": (
        "technical",
        "memory-management-agentic-ai",
    ),
    "gke_magic_quadrant": ("technical", "gke-magic-quadrant"),
    "vibe-coding-intro": ("technical", "vibe-coding-intro"),
    "vibe-coding-dos-donts": ("technical", "vibe-coding-dos-donts"),
    # Personal
    "miyamoto-musashi-10-principles": ("personal", "miyamoto-musashi"),
    "poem-sky-sea-truth": ("personal", "sky-sea-truth"),
    "spot-fakes-leaders": ("personal", "spot-fake-leaders"),
    "two-lenses-of-leadership": ("personal", "two-lenses-of-leadership"),
}

IMG_RE = re.compile(r"images/[A-Za-z0-9._/-]+\.(?:png|jpe?g|gif|svg|webp)", re.I)

# The pilot's redirect entry; new entries are inserted right after it.
ANCHOR = "        blog/posts/a2a_multi_tenancy.md: writing/a2a/multi-tenancy/index.md\n"


def migrate() -> None:
    moved: list[tuple[str, str]] = []  # (stem, "writing/<section>/<slug>")
    for stem, (section, slug) in MAPPING.items():
        src_md = POSTS / f"{stem}.md"
        if not src_md.exists():
            print(f"SKIP (already moved / missing): {stem}")
            continue
        new_dir = DOCS / "writing" / section / slug
        new_dir.mkdir(parents=True, exist_ok=True)
        content = src_md.read_text(encoding="utf-8")

        for ref in sorted(set(IMG_RE.findall(content)), key=len, reverse=True):
            img_src = POSTS / ref
            base = Path(ref).name
            if img_src.exists():
                # Local image: co-locate it and rewrite the ref to the basename.
                shutil.move(str(img_src), str(new_dir / base))
                content = content.replace(ref, base)
            else:
                # Not a local file (e.g. an ``images/...`` substring inside a
                # remote CDN URL). Leave it completely untouched.
                print(f"  skip (not a local image): {ref}")

        (new_dir / "index.md").write_text(content, encoding="utf-8")
        src_md.unlink()
        moved.append((stem, f"writing/{section}/{slug}"))
        print(f"moved {stem} -> writing/{section}/{slug}")

    if not moved:
        print("\nNothing to migrate.")
        return

    # 1) nav paths + internal doc links (same string form in all three files)
    for f in (ROOT / "mkdocs.yml", DOCS / "index.md", DOCS / "about.md"):
        text = f.read_text(encoding="utf-8")
        for stem, (section, slug) in MAPPING.items():
            text = text.replace(
                f"blog/posts/{stem}.md", f"writing/{section}/{slug}/index.md"
            )
        f.write_text(text, encoding="utf-8")

    # 2) redirect_maps: insert after the pilot anchor (added last, so the nav
    #    pass above never rewrites these keys)
    mk = ROOT / "mkdocs.yml"
    text = mk.read_text(encoding="utf-8")
    block = "".join(
        f"        blog/posts/{stem}.md: {dst}/index.md\n" for stem, dst in moved
    )
    assert ANCHOR in text, "redirect_maps anchor not found in mkdocs.yml"
    mk.write_text(text.replace(ANCHOR, ANCHOR + block), encoding="utf-8")

    # 3) llms.txt public URLs
    lf = DOCS / "llms.txt"
    text = lf.read_text(encoding="utf-8")
    for stem, (section, slug) in MAPPING.items():
        text = text.replace(f"/blog/posts/{stem}/", f"/writing/{section}/{slug}/")
    lf.write_text(text, encoding="utf-8")

    print(f"\nMigrated {len(moved)} posts; updated nav, redirects, links, llms.txt.")


if __name__ == "__main__":
    migrate()
