"""MkDocs hook: inject the latest blog posts into the Home page.

Replaces the marker ``<!-- LATEST_POSTS -->`` in ``index.md`` with a list of
the most recent posts under ``docs/blog/posts/``, newest first. Post metadata
(title, date, description) is read from each file's YAML front matter, so the
Home page stays current automatically — just drop a new post in and rebuild.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

import yaml

# How many recent posts to surface on the Home page.
MAX_POSTS = 6
MARKER = "<!-- LATEST_POSTS -->"
_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_post(path: Path) -> dict | None:
    """Return {title, date, description, url} for a post, or None to skip."""
    text = path.read_text(encoding="utf-8")
    match = _FRONT_MATTER.match(text)
    if not match:
        return None
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(meta, dict) or "date" not in meta:
        return None

    date = meta["date"]
    if isinstance(date, dict):  # blog plugin supports {created: ...}
        date = date.get("created")
    if isinstance(date, _dt.datetime):
        date = date.date()
    if not isinstance(date, _dt.date):
        return None

    title = meta.get("title") or path.stem.replace("-", " ").title()
    return {
        "title": str(title).strip('"'),
        "date": date,
        "description": (meta.get("description") or "").strip(),
        "url": f"blog/posts/{path.stem}/",
    }


def _render(posts: list[dict]) -> str:
    lines: list[str] = []
    for post in posts:
        line = f"- **[{post['title']}]({post['url']})** "
        line += f"<small>· {post['date'].strftime('%b %d, %Y')}</small>"
        if post["description"]:
            line += f"<br><small>{post['description']}</small>"
        lines.append(line)
    return "\n".join(lines)


def on_page_markdown(markdown: str, *, page, config, files):
    if page.file.src_uri != "index.md" or MARKER not in markdown:
        return markdown

    posts_dir = Path(config["docs_dir"]) / "blog" / "posts"
    posts = [p for f in posts_dir.glob("*.md") if (p := _parse_post(f))]
    posts.sort(key=lambda p: p["date"], reverse=True)
    return markdown.replace(MARKER, _render(posts[:MAX_POSTS]))
