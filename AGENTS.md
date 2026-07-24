# Agent Instructions

Personal MkDocs-Material site published to GitHub Pages (`msampathkumar.github.io`). Content-only repo — no application code.

## Repo Layout

- `docs/` — published site content. Entry: `docs/index.md` (Home).
  - `docs/writing/<section>/<slug>/index.md` — blog posts (folder-per-post, images/assets co-located; front matter required, see below). Sections map to `/writing/<section>/`: `a2a`, `cloud-next-2026`, `gemini`, `technical`, `personal`. `docs/blog/posts/` retains a few unlisted drafts; `docs/blog/notes/` — unlisted notes (built but not in nav). Old `/blog/posts/<slug>/` URLs are preserved via `mkdocs-redirects` (see `redirect_maps` in `mkdocs.yml`).
  - `docs/cookbook.md` — Cookbook **hub** at `/cookbook/` (Gemini live; A2A slot commented in nav for later). `docs/google-cloud-gemini-cookbook/` — the Gemini cookbook + lessons.
  - `docs/about.md` — About page (last nav item). `docs/blog/.authors.yml` — author profiles (id `sampathm`).
  - `docs/llms.txt` — hand-curated, link-first index for LLMs/agents. `docs/llms-full.txt` — **generated**, full inlined content (do not hand-edit; run `make llms`).
- `mkdocs.yml` — site config + navigation. New pages must be wired into `nav:` or they won't appear. The Material **`blog` plugin is intentionally disabled** (it excludes `blog/posts` from the manual nav and breaks the curated Writing tab).
- `hooks/latest_posts.py` — build hook that injects newest posts into Home at the `<!-- LATEST_POSTS -->` marker (reads each post's front-matter `date`).
- `scripts/` — `gen_llms_full.py` (llms-full), `new_post.py` (scaffold), `import_devto.py` (import), `score_post.py` (agent-readiness score).
- `.cloudcode/skills/agent-ready-blog/` — skill to scope a post for agents-first quality.
- `_internal/`, `archive/`, `docs/blog/ProjectMgmt/`, anything matching `internal*` or `*personal*` — gitignored drafts. Don't commit. (Note: the pattern is `internal*` **and** `_internal/` — the leading underscore needs its own rule.)

## Content conventions

- **Every blog post needs valid YAML front matter**: `title`, `date` (YYYY-MM-DD), `authors: [sampathm]`, `categories:`, and ideally `description:`. The Home "Latest posts" list and dates depend on it.
- **Agents-first**: posts should have `##`/`###` sections (so the right-hand TOC renders), lead with a TL;DR, and define acronyms. Score a draft with `python scripts/score_post.py <file>` or the `agent-ready-blog` skill.
- Imported/cross-posted content should set `canonical_url` to the original (avoids duplicate-content SEO).

### Naming & URL conventions (foundational — keep it simple)

- **Paths = URLs.** A post at `docs/writing/<section>/<slug>/index.md` is served at `/writing/<section>/<slug>/`. Choose the section + slug deliberately; together they are the public URL. Scaffold with `make new-post TITLE="…" SECTION="a2a"` (or `python scripts/new_post.py`), which prints the nav line to paste into `mkdocs.yml`.
- **Lowercase-kebab slugs, folder-per-post.** Each post is its own folder (`.../<slug>/index.md`) so images and assets live beside it. Lowercase, hyphen-separated; keep slugs short and topical (`/writing/a2a/multi-tenancy/`, not a long dev.to title). Drop the redundant section prefix from the slug (under `/writing/a2a/`, use `intro`, not `a2a-intro`).
- **Sections** are the first URL segment and group related posts: `a2a`, `cloud-next-2026`, `gemini`, `technical`, `personal`. Add a new section deliberately — it becomes a public URL segment. (Note: `.gitignore`'s `*personal*` rule is explicitly un-ignored for `docs/writing/personal/` — keep that negation.)
- **Don't rename or move an established post** without adding a `redirect_maps` entry in `mkdocs.yml` (`old/path.md: new/path/index.md`) — it breaks live URLs, inbound links, and SEO. On GitHub Pages these are client-side meta-refresh stubs, not 301s.
- **Images** are co-located in the post's own folder and referenced by bare filename (`![](diagram.png)`). Keep names descriptive (`<topic>_<n>.<ext>`). Remote CDN images may be left as absolute URLs; only localize when you want the site self-contained.
- **Buttons**: author Material buttons on a single short line (`[Text](url){ .md-button }`) that fits under 79 cols — mdformat's `wrap=79` will otherwise split the `{ .md-button }` attr-list across lines and it renders as literal text.

## Commands

```bash
make run                       # mkdocs serve on http://localhost:8099
make deploy                    # runs `make llms` then gh-deploy (manual publish)
make check-ga                  # build site/ and grep for Google Analytics injection
make llms                      # regenerate docs/llms-full.txt from docs/llms.txt
make new-post TITLE="My Title" SECTION="a2a"  # scaffold docs/writing/<section>/<slug>/index.md
make import-devto              # pull dev.to/Medium posts to _internal/devto_import/ (review-first)
mkdocs build                   # one-shot build into site/
```

Install deps with `pip install -r requirements.txt` (pinned, used by CI). `pyproject.toml` exists for uv but versions there are looser — `requirements.txt` is the source of truth.

Python 3.13+ required (see `.python-version`, `pyproject.toml`).

## CI / Deploy Quirks

- Auto-deploy workflow: `.github/workflow/publish-docs.yaml` (note: **`workflow/` singular**, not the standard `workflows/`). `.gitignore` excludes `.github/workflows`, so creating a `workflows/` directory will not be tracked. Edit the existing file in place; do not rename the directory.
- Pushes to `master` (or `main`) trigger `mkdocs gh-deploy --force` on the `gh-pages` branch. The default branch is `master`.
- The checkout uses `fetch-depth: 0` — required so the `git-revision-date-localized` plugin can read commit history for last-updated dates.
- `GOOGLE_ANALYTICS_KEY` is provided via GitHub Actions secret; locally it reads `GOOGLE_ANALYTICS_KEY_GITHUB_IO_BLOG` (see `check-ga`).

## Markdown Formatting

`.mdformat.toml` enforces `wrap=79`, LF endings, and runs `python` + `json` code-block formatters (via `mdformat-black`, `mdformat-config`). Run `mdformat <file>` before committing markdown changes if formatting may have drifted.

> **CRITICAL:** `mdformat-frontmatter` **must** be installed (it is pinned in `requirements.txt`). Without it, mdformat rewrites the leading `---` YAML front-matter fences into horizontal rules and reflows the metadata into a paragraph — silently breaking the Home page and dropping post `title`/`date`. After running mdformat, sanity-check that touched files still start with `---`.

## Landing the Plane (Session Completion)

Work is NOT complete until `git push` succeeds. Required sequence at session end:

1. Run quality gates if content changed (`mkdocs build` to catch broken nav/links; `mdformat` on touched markdown).
2. **Push:**
   ```bash
   git pull --rebase
   git push
   git status   # must show "up to date with origin"
   ```
3. Clear stashes, prune remote branches, hand off context.

Never stop before `git push` succeeds. If it fails, resolve and retry.
