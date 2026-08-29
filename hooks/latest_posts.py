"""MkDocs hook: inject the latest blog posts into the Home page.

Replaces the marker ``<!-- LATEST_POSTS -->`` in ``index.md`` with a list of
the most recent posts, newest first. Post metadata (title, date, description)
is read from each file's YAML front matter, so the Home page stays current
automatically — just drop a new post in and rebuild.

Posts are discovered in two locations so the site can migrate incrementally:
``docs/writing/<section>/<slug>/index.md`` (current convention) and the legacy
``docs/blog/posts/<slug>.md``. The public URL is derived from the file's path
relative to ``docs_dir`` (mirroring MkDocs' own ``use_directory_urls`` rules),
so it stays correct wherever a post lives.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

import yaml

# How many recent posts to surface on the Home page.
MAX_POSTS = 3
MARKER = "<!-- LATEST_POSTS -->"
_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _post_url(path: Path, docs_dir: Path) -> str:
    """Source-relative link target for a post (docs_dir-relative ``.md`` path).

    Returning the source path (e.g. ``writing/a2a/multi-tenancy/index.md``)
    rather than the directory URL lets MkDocs recognise and rewrite the link to
    the final page URL — which avoids the "unrecognized relative link" INFO
    messages MkDocs emits for bare-directory links.
    """
    return path.relative_to(docs_dir).as_posix()


def _parse_post(path: Path, docs_dir: Path) -> dict | None:
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

    # For folder-per-post the slug is the parent dir, not the "index" stem.
    slug = path.parent.name if path.stem == "index" else path.stem
    title = meta.get("title") or slug.replace("-", " ").title()
    return {
        "title": str(title).strip('"'),
        "date": date,
        "description": (meta.get("description") or "").strip(),
        "url": _post_url(path, docs_dir),
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

    docs_dir = Path(config["docs_dir"])
    # Current convention (folder-per-post) + legacy flat location.
    files = sorted(docs_dir.glob("writing/**/index.md"))
    files += sorted((docs_dir / "blog" / "posts").glob("*.md"))
    posts = [p for f in files if (p := _parse_post(f, docs_dir))]
    posts.sort(key=lambda p: p["date"], reverse=True)
    return markdown.replace(MARKER, _render(posts[:MAX_POSTS]))
