#!/usr/bin/env python3
"""Generate a reader-focused README.md populated with all published articles.

Extracts metadata (title, date, description, URL) from docs/writing/**/index.md,
sorts reverse-chronologically by publication date, and renders a clean,
reader-first index for visitors on GitHub.
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
README = ROOT / "README.md"
SITE_BASE = "https://msampathkumar.github.io"

_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def get_all_posts() -> list[dict]:
    posts: list[dict] = []
    for md_path in sorted(DOCS.glob("writing/**/index.md")):
        if md_path.as_posix() == (DOCS / "writing" / "index.md").as_posix():
            continue
        text = md_path.read_text(encoding="utf-8")
        match = _FRONT_MATTER.match(text)
        if not match:
            continue
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except Exception:
            continue

        date = meta.get("date")
        if isinstance(date, dict):
            date = date.get("created")
        if isinstance(date, _dt.datetime):
            date = date.date()
        if not isinstance(date, _dt.date):
            continue

        section = md_path.parent.parent.name
        slug = md_path.parent.name
        title = meta.get("title") or slug.replace("-", " ").title()
        desc = (meta.get("description") or "").strip()
        url = f"{SITE_BASE}/writing/{section}/{slug}/"

        posts.append({
            "title": str(title).strip('"'),
            "date": date,
            "description": desc,
            "url": url,
            "section": section,
        })

    # Sort reverse-chronologically (newest first)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_readme(posts: list[dict]) -> str:
    parts = [
        "# Sampath Kumar — Digital Garden & Engineering Reference",
        "",
        f"> Welcome! This repository is the source for **[msampathkumar.github.io]({SITE_BASE}/)**, a digital garden dedicated to **Google Cloud**, **Gemini AI**, **Agentic Workflows (A2A, ADK)**, and modern cloud architecture.",
        "",
        "---",
        "",
        "## 📚 Published Articles & Technical Guides",
        "",
        f"Below is a list of all {len(posts)} articles published on the site, ordered newest first:",
        "",
    ]

    for p in posts:
        date_str = p["date"].strftime("%b %d, %Y")
        parts.append(f"- **`{date_str}`** — [{p['title']}]({p['url']})")

    parts.extend([
        "",
        "---",
        "",
        "## 📖 Key Initiatives",
        "",
        f"- **[Google Cloud Gemini Cookbook]({SITE_BASE}/cookbook/)**: Practical tutorials for building production AI applications with Gemini and Vertex AI.",
        f"- **[Agent-to-Agent (A2A) Protocols]({SITE_BASE}/writing/)**: Architectural guides and whitepapers on the Linux Foundation A2A protocol.",
        f"- **[AI-Ready Reading (llms.txt)]({SITE_BASE}/llms.txt)**: Curated context streams optimized for LLM agents and AI assistants.",
        "",
        "---",
        "",
        "## 🌐 Connect & Explore",
        "",
        f"- **Website**: [msampathkumar.github.io]({SITE_BASE}/)",
        "- **LinkedIn**: [msampathkumar](https://www.linkedin.com/in/msampathkumar/)",
        "- **GitHub**: [@msampathkumar](https://github.com/msampathkumar)",
        "",
        "---",
        "",
        "## 💬 Feedback & Issues",
        "",
        "If you spot a typo, broken link, or technical bug in any article or cookbook lesson, please feel free to [open an issue](https://github.com/msampathkumar/msampathkumar.github.io/issues) or submit a feature request. Your feedback helps improve the resources for everyone!",
        "",
        "---",
        "",
        "## ❤️ Built for the Community",
        "",
        "This site and its engineering resources are created with deep love and respect for the developer community — especially the **Python** and **Data Science** communities whose creativity, openness, and passion continue to inspire me every single day.",
        "",
        "---",
        "",
        "## 📄 License",
        "",
        "Content and code samples are open source and available under the [Apache 2.0 License](LICENSE).",
        "",
    ])

    return "\n".join(parts)


def main() -> int:
    posts = get_all_posts()
    readme_content = render_readme(posts)
    README.write_text(readme_content, encoding="utf-8")
    print(f"Generated {README.name} with {len(posts)} published articles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
