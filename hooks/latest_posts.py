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


def _calculate_read_time(text: str) -> int:
    """Estimate read time in minutes using the Medium.com standard algorithm.

    Medium formula:
      - 265 words per minute for English prose.
      - 12 seconds for the 1st image, 11s for the 2nd, down to 3s for the 10th+ image.
      - Code snippets & diagrams are excluded from prose word count.
    """
    # 1. Count images before stripping
    images = re.findall(r"!\[.*?\]\(.*?\)|<img\b[^>]*>", text)
    image_seconds = 0
    for i in range(len(images)):
        if i < 10:
            image_seconds += max(3, 12 - i)
        else:
            image_seconds += 3

    # 2. Strip HTML comments
    clean = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    # 3. Strip fenced code blocks (```...```) and Mermaid diagrams
    clean = re.sub(r"```[\s\S]*?```", " ", clean)
    # 4. Strip inline code
    clean = re.sub(r"`[^`]+`", " ", clean)
    # 5. Strip HTML tags
    clean = re.sub(r"<[^>]+>", " ", clean)
    # 6. Strip markdown image tags
    clean = re.sub(r"!\[.*?\]\(.*?\)", " ", clean)
    # 7. Extract link text from markdown links [text](url) -> text
    clean = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", clean)

    # 8. Extract English prose words
    words = re.findall(r"\b[A-Za-z0-9'-]{2,}\b", clean)
    word_count = len(words)

    # Total reading time in seconds: (words / 265 * 60) + image_seconds
    total_seconds = (word_count / 265.0 * 60.0) + image_seconds

    # Round to nearest minute (minimum 1 minute)
    return max(1, round(total_seconds / 60.0))


def _inject_post_metadata(markdown: str, page) -> str:
    """Inject Date · Read Time · Author immediately after the first # Title."""
    src_uri = page.file.src_uri
    # Only target blog posts under writing/ (exclude writing/index.md hub)
    if not src_uri.startswith("writing/") or src_uri == "writing/index.md":
        return markdown

    meta = getattr(page, "meta", {}) or {}
    date = meta.get("date")
    if isinstance(date, dict):
        date = date.get("created")
    if isinstance(date, _dt.datetime):
        date = date.date()

    if not isinstance(date, _dt.date):
        return markdown

    # Format Date
    formatted_date = date.strftime("%B %d, %Y")

    # Author
    author = "Sampath Kumar"
    authors = meta.get("authors")
    if authors and isinstance(authors, list) and authors[0] != "sampathm":
        author = str(authors[0])

    # Read Time
    read_time = _calculate_read_time(markdown)

    meta_html = (
        f'<div class="post-metadata-header">\n'
        f'  <span class="post-metadata-item"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 19H5V8h14m-3-7v2H8V1H6v2H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-1V1m-1 11h-5v5h5v-5Z"/></svg></span> {formatted_date}</span>\n'
        f'  <span class="post-metadata-divider">·</span>\n'
        f'  <span class="post-metadata-item"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 20a8 8 0 0 0 8-8a8 8 0 0 0-8-8a8 8 0 0 0-8 8a8 8 0 0 0 8 8m0-18a10 10 0 0 1 10 10a10 10 0 0 1-10 10C6.47 22 2 17.5 2 12A10 10 0 0 1 12 2m.5 5v5.25l4.5 2.67l-.75 1.23L11 13V7h1.5Z"/></svg></span> {read_time} min read</span>\n'
        f'  <span class="post-metadata-divider">·</span>\n'
        f'  <span class="post-metadata-item"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 4a4 4 0 0 1 4 4a4 4 0 0 1-4 4a4 4 0 0 1-4-4a4 4 0 0 1 4-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4Z"/></svg></span> {author}</span>\n'
        f'</div>\n'
    )

    # If markdown starts with '# Title' (H1 at top), place metadata right below it
    h1_match = re.match(r"^(#\s+[^\n]+)\n*", markdown)
    if h1_match:
        insert_pos = h1_match.end()
        return markdown[:insert_pos] + "\n" + meta_html + "\n\n" + markdown[insert_pos:]

    # Otherwise (e.g. custom div header or title from front-matter), place metadata at the very top
    return meta_html + "\n\n" + markdown


def on_page_markdown(markdown: str, *, page, config, files):
    # Handle Home page latest posts injection
    if page.file.src_uri == "index.md" and MARKER in markdown:
        docs_dir = Path(config["docs_dir"])
        files = sorted(docs_dir.glob("writing/**/index.md"))
        files += sorted((docs_dir / "blog" / "posts").glob("*.md"))
        posts = [p for f in files if (p := _parse_post(f, docs_dir))]
        posts.sort(key=lambda p: p["date"], reverse=True)
        markdown = markdown.replace(MARKER, _render(posts[:MAX_POSTS]))

    # Handle Post Metadata header injection for writing/ articles
    return _inject_post_metadata(markdown, page)
