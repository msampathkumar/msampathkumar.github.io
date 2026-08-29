# System Architecture & Technical Design

This document details the technical architecture, design patterns, rendering pipeline, and infrastructure mechanics of the `msampathkumar.github.io` static site.

______________________________________________________________________

## 1. Architectural Goals & Non-Goals

### 🎯 Goals
- **Deterministic & Agent-Centric**: Provide clean, predictable Markdown endpoints and automated machine-readable context streams (`/llms.txt`, `/llms-full.txt`) for AI crawlers, IDE assistants, and sub-agents.
- **Fast, Zero-JS Content Delivery**: Ensure all critical prose, code samples, and architectural guides render statically and execute blazingly fast without requiring client-side JavaScript execution.
- **Permanent URL Stability**: Preserve every historical and syndicate link via automated client-side redirect maps (`mkdocs-redirects`).
- **Co-Located Asset Model**: Every article is self-contained within its own directory (`docs/writing/<section>/<slug>/index.md`) alongside its dedicated hero image and media assets.

### 🚫 Non-Goals
- **No Dynamic Backend Server Runtimes**: Avoid database-backed CMS complexity; all state is checked into Git and compiled into pure static HTML/CSS.
- **No Client-Side Framework Bloat**: Avoid heavy client frameworks (React, Vue, SPA bundles) for basic documentation reading.
- **No Orphaned or Broken Links**: Disallow broken relative paths or missing nav linkages (`mkdocs build --strict` gating).

______________________________________________________________________

## 2. Core Architecture Rules & Constraints

1. **Strict Build Integrity**: Every change must pass `mkdocs build --strict` with zero warnings and zero broken relative links.
2. **Reverse-Chronological Ordering**: All navigation trees (`mkdocs.yml`), LLM indexes (`docs/llms.txt`), and writing hubs (`docs/writing/index.md`) must strictly list new posts top-first by publication date.
3. **Canonical Attribution**: Any post imported or cross-posted from Medium or dev.to must include `canonical_url` in YAML frontmatter and a standard blockquote callout.
4. **Hero Image Standards**: Co-located `hero.png` (16:9, dark slate `#0f172a`, glowing accents, zero text) with prompt documentation comment.
5. **No Direct Git Commits**: Never perform git operations without explicit user confirmation.

______________________________________________________________________

## 3. Core Architecture & Tech Stack

- **Static Site Generator**: [MkDocs](https://www.mkdocs.org/) with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.
- **Hosting & CDN**: GitHub Pages with custom domain publishing (`msampathkumar.github.io`).
- **Runtime & Environment**: Python 3.13+ (`requirements.txt` is the pinned source of truth for CI/CD; `pyproject.toml` for local tooling).
- **Navigation Model**: Fully manual curated navigation defined in `mkdocs.yml` (`nav:`). The Material `blog` plugin is intentionally disabled to avoid auto-hiding posts from manual tabs.
- **Client-Side Redirects**: Managed via `mkdocs-redirects` plugin (`redirect_maps` in `mkdocs.yml`) to preserve historical URLs without 404s.


______________________________________________________________________

## 4. Directory Layout & Routing Conventions

```text
├── docs/
│   ├── index.md                 # Home landing page (auto-injected with latest posts)
│   ├── writing/                 # Curated blog posts
│   │   ├── index.md             # Writing hub index (check this page after adding new posts)
│   │   ├── a2a/                 # Agent-to-Agent protocol articles
│   │   ├── cloud-next-2026/     # Google Cloud Next 2026 recap series
│   │   ├── gemini/              # Gemini guides & CLI cheatsheets
│   │   ├── technical/           # Technical engineering & architecture posts
│   │   └── personal/            # Reflections and essays
│   ├── cookbook.md              # Cookbook hub index
│   ├── google-cloud-gemini-cookbook/ # Gemini lessons & tutorials
│   ├── about.md                 # About the author
│   ├── llms.txt                 # Hand-curated index optimized for LLMs & AI agents
│   └── llms-full.txt            # Machine-generated full-content inlined index
├── hooks/                       # When possible. Use hooks to automate this site's build
│   └── latest_posts.py          # MkDocs build hook injecting latest posts into Home
├── scripts/                     # For tasks, scripts, and automation use this
│   ├── gen_llms_full.py         # Inlines full markdown docs into docs/llms-full.txt
│   ├── gen_readme.py            # Regenerates README.md and docs/writing/index.md in sync
│   ├── new_post.py              # CLI scaffolding tool for new folder-per-post articles
│   ├── score_post.py            # Mechanical agent-readiness linting script (0–100)
│   └── import_devto.py          # Migration script for external syndication
├── .github/
│   └── workflows/
│       └── publish-docs.yaml    # CI/CD automated deployment workflow to gh-pages branch
└── mkdocs.yml                   # Central site configuration, plugins, & navigation
```

### URL Resolution Rule

- **Path = URL**: A file at `docs/writing/<section>/<slug>/index.md` is served at `https://msampathkumar.github.io/writing/<section>/<slug>/`.
- **Folder-per-post**: Every post is isolated in its own directory so images, diagrams, and assets are co-located and referenced by local relative paths (`![](hero.png)`).

______________________________________________________________________

## 5. Hero Image Specifications & Design System

To maintain visual cohesion across technical and architectural articles, all hero images adhere to a strict visual design system:

| Property | Specification | Rationale |
| :--- | :--- | :--- |
| **Dimensions** | **800 × 450 px** (approx. 800×400) | Optimized for fast web delivery and responsive mobile cards |
| **Aspect Ratio** | **16:9** | Standard wide aspect ratio across desktop and social previews |
| **Format** | PNG (optimized compression) | Sharp vector-style edges and artifacts-free gradients |
| **Background Palette** | Dark Slate / Charcoal (`#0f172a` / `#111827`) | Seamlessly matches MkDocs Slate dark mode aesthetic |
| **Accent Palette** | Glowing Cyan, Electric Blue, Emerald, Violet | Cyberpunk / modern developer infrastructure aesthetics |
| **Typography Rule** | **Zero text / words in image** | Eliminates AI lettering artifacts; typography belongs in HTML/CSS |

### AI Generation Comment Requirement

Every hero image must be preceded by an HTML comment with the exact prompt used:

```markdown
<!-- AI Image Generation Prompt: A minimalist, clean modern tech illustration of <subject>, glowing cyan and electric blue accents on a dark slate background, no text, professional developer aesthetic. -->
![<Title> Hero](hero.png)
```

______________________________________________________________________

## 6. Build Hooks & Dynamic Injection

### Latest Posts Hook (`hooks/latest_posts.py`)

- Runs during `mkdocs build` / `mkdocs serve`.
- Scans `docs/writing/**/*.md` and extracts `title`, `date`, `description`, and URL from YAML front matter.
- Injects the top 3 newest posts into `docs/index.md` at the `<!-- LATEST_POSTS -->` placeholder.

### Automated Post Metadata Header Hook (`hooks/latest_posts.py`)

- Automatically runs across all articles under `docs/writing/**/*.md`.
- Injects a single-line metadata bar (`Date · Read Time · Author`) immediately beneath the `# Title` and above the hero image.
- Estimates reading time using the **Medium.com standard algorithm** (265 words/min on English prose, excluding code/diagrams, plus 12s/11s progressive image weighting).

### LLM Indexing System (`docs/llms.txt` & `docs/llms-full.txt`)

- `docs/llms.txt`: Curated, link-first index categorized by topic for LLMs and crawler agents.
- `docs/llms-full.txt`: Automatically compiled by `scripts/gen_llms_full.py`, which reads `docs/llms.txt`, fetches each referenced `.md` file, strips redundant front matter, and compiles a single deterministic context file for AI assistants.

______________________________________________________________________

## 7. CI/CD & GitHub Pages Deployment Pipeline

The site is automatically deployed via GitHub Actions:

- **Workflow Path**: `.github/workflows/publish-docs.yaml`
- **Trigger**: Pushes to `master` (or `main`)
- **Execution Steps**:
  1. `actions/checkout@v4` with `fetch-depth: 0` (mandatory for `git-revision-date-localized` plugin to parse commit timestamps).
  1. Python setup & dependency installation from `requirements.txt`.
  1. `python scripts/gen_llms_full.py` to regenerate the full LLM index.
  1. `mkdocs gh-deploy --clean --force` to build and publish static HTML to the `gh-pages` branch.

