#!/usr/bin/env python3
"""Download remote images referenced by Markdown posts into the repo.

Makes the site self-contained: fetches remote images (e.g. Medium CDN) into
``docs/blog/posts/images/<subdir>/`` with clean, predictable filenames
(``<post-stem>_<n>.<ext>``) and rewrites the Markdown to point at the local
copies. Article/source links (medium.com/... article URLs) are left alone —
only image references are localized.

Usage:
    python scripts/localize_images.py docs/blog/posts/a2a_intro.md ...
    python scripts/localize_images.py --subdir a2a docs/blog/posts/a2a_*.md
"""

from __future__ import annotations

import argparse
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<url>https?://[^)\s]+)\)")
CT_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}


def download(url: str, dest_base: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": "img-localize/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = resp.read()
        ext = Path(url.split("?")[0]).suffix.lower()
        if ext not in CT_EXT.values():
            ext = CT_EXT.get(resp.headers.get("Content-Type", "").split(";")[0], ".png")
    dest = dest_base.with_suffix(ext)
    dest.write_bytes(data)
    return dest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--subdir", default="imported", help="images/<subdir>/")
    args = ap.parse_args()

    img_root = ROOT / "docs" / "blog" / "posts" / "images" / args.subdir
    img_root.mkdir(parents=True, exist_ok=True)
    total = 0

    for f in args.files:
        path = Path(f)
        text = path.read_text(encoding="utf-8")
        matches = list(IMG_RE.finditer(text))
        remote = [m for m in matches if m["url"].startswith("http")]
        if not remote:
            continue
        for i, m in enumerate(remote, 1):
            base = img_root / f"{path.stem}_{i}"
            try:
                dest = download(m["url"], base)
            except Exception as e:  # noqa: BLE001
                print(f"  FAIL {m['url']}: {e}")
                continue
            rel = Path(os.path.relpath(dest, path.resolve().parent)).as_posix()
            text = text.replace(f"({m['url']})", f"({rel})")
            total += 1
            print(f"  {path.name}: {m['url'].split('/')[-1]} -> {rel}")
        path.write_text(text, encoding="utf-8")

    print(f"\nLocalized {total} images into {img_root.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
