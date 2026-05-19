# Agent Instructions

Personal MkDocs-Material site published to GitHub Pages (`msampathkumar.github.io`). Content-only repo — no application code.

## Repo Layout

- `docs/` — published site content (blog posts, cookbook, events, services). Entry: `docs/index.md`.
- `mkdocs.yml` — site config and navigation. New pages must be wired into `nav:` here or they will not appear.
- `_internal/`, `archive/`, `docs/blog/ProjectMgmt/`, anything matching `internal*` or `*personal*` — gitignored drafts. Don't commit.

## Commands

```bash
make run        # mkdocs serve on http://localhost:8099
make deploy     # mkdocs gh-deploy --clean --force  (manual publish)
make check-ga   # build site/ and grep for Google Analytics injection
mkdocs build    # one-shot build into site/
```

Install deps with `pip install -r requirements.txt` (pinned, used by CI). `pyproject.toml` exists for uv but versions there are looser — `requirements.txt` is the source of truth.

Python 3.13+ required (see `.python-version`, `pyproject.toml`).

## CI / Deploy Quirks

- Auto-deploy workflow: `.github/workflow/publish-docs.yaml` (note: **`workflow/` singular**, not the standard `workflows/`). `.gitignore` excludes `.github/workflows`, so creating a `workflows/` directory will not be tracked. Edit the existing file in place; do not rename the directory.
- Pushes to `main` trigger `mkdocs gh-deploy --force` on the `gh-pages` branch.
- `GOOGLE_ANALYTICS_KEY` is provided via GitHub Actions secret; locally it reads `GOOGLE_ANALYTICS_KEY_GITHUB_IO_BLOG` (see `check-ga`).

## Markdown Formatting

`.mdformat.toml` enforces `wrap=79`, LF endings, and runs `python` + `json` code-block formatters (via `mdformat-black`, `mdformat-config`). Run `mdformat <file>` before committing markdown changes if formatting may have drifted.

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
