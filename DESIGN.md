# System Architecture & Technical Design

This document details the technical architecture, design patterns, rendering pipeline, and infrastructure mechanics of the `msampathkumar.github.io` static site.

______________________________________________________________________

## 1. Core Architecture & Tech Stack

- **Static Site Generator**: [MkDocs](https://www.mkdocs.org/) with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.
- **Hosting & CDN**: GitHub Pages with custom domain publishing (`msampathkumar.github.io`).
- **Runtime & Environment**: Python 3.13+ (`requirements.txt` is the pinned source of truth for CI/CD; `pyproject.toml` for local tooling).
- **Navigation Model**: Fully manual curated navigation defined in `mkdocs.yml` (`nav:`). The Material `blog` plugin is intentionally disabled to avoid auto-hiding posts from manual tabs.
- **Client-Side Redirects**: Managed via `mkdocs-redirects` plugin (`redirect_maps` in `mkdocs.yml`) to preserve historical URLs without 404s.

______________________________________________________________________

## 2. Directory Layout & Routing Conventions

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

## 3. Hero Image Specifications & Design System

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

## 4. Build Hooks & Dynamic Injection

### Latest Posts Hook (`hooks/latest_posts.py`)

- Runs during `mkdocs build` / `mkdocs serve`.
- Scans `docs/writing/**/*.md` and extracts `title`, `date`, `description`, and URL from YAML front matter.
- Injects the top 3 newest posts into `docs/index.md` at the `<!-- LATEST_POSTS -->` placeholder.

### LLM Indexing System (`docs/llms.txt` & `docs/llms-full.txt`)

- `docs/llms.txt`: Curated, link-first index categorized by topic for LLMs and crawler agents.
- `docs/llms-full.txt`: Automatically compiled by `scripts/gen_llms_full.py`, which reads `docs/llms.txt`, fetches each referenced `.md` file, strips redundant front matter, and compiles a single deterministic context file for AI assistants.

______________________________________________________________________

## 5. CI/CD & GitHub Pages Deployment Pipeline

The site is automatically deployed via GitHub Actions:

- **Workflow Path**: `.github/workflows/publish-docs.yaml`
- **Trigger**: Pushes to `master` (or `main`)
- **Execution Steps**:
  1. `actions/checkout@v4` with `fetch-depth: 0` (mandatory for `git-revision-date-localized` plugin to parse commit timestamps).
  1. Python setup & dependency installation from `requirements.txt`.
  1. `python scripts/gen_llms_full.py` to regenerate the full LLM index.
  1. `mkdocs gh-deploy --clean --force` to build and publish static HTML to the `gh-pages` branch.
