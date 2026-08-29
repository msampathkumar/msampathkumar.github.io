# Agent Instructions & Operating Manual

This document defines the agent operating principles, user goals, content workflows, and quality standards for `msampathkumar.github.io`.

For full technical architecture, site layout, CI/CD pipeline, and design specifications, see [**`DESIGN.md`**](DESIGN.md).

______________________________________________________________________

## 1. User Profile & Strategic Ambitions

- **Site Owner**: Sampath Kumar (`sampathm`)
- **Focus Areas**: Google Cloud, Gemini AI, Agentic Workflows (A2A, ADK), Modern Cloud Architecture, and Developer Tooling.
- **Audience & Tone**: Professional cloud architects, AI engineers, and technical leaders. Clean, direct, highly structured, and actionable ("agents-first, human-delight").
- **Strategic Goals (by end of 2026)**:
  - Reach 50 million viewers and 20 million subscribers across technical distribution channels (YouTube, Medium, LinkedIn, Blog).
  - Establish the "Google Cloud Gemini Cookbook" and "A2A / Agentic Systems" as premier reference resources.

______________________________________________________________________

## 2. Core Operating Principles & Communication

1. **Clarity & Trust**: Ensure at least 80% clarity on requirements before executing large changes. Proactively ask clarifying questions instead of guessing.
1. **Explicit Permissions**: **Never execute git commits or pushes without explicit user permission.**
1. **Sequential & Minimal**: Plan sequentially, execute task-by-task, and apply minimal necessary changes.
1. **Preserve History & Legacy**: Comment out deprecated code/logic with clear rationale rather than deleting unprompted. Always wire redirects when moving published URLs.
1. **Always Land Cleanly**: When completing a task, verify the build (`mkdocs build`), format touched Markdown (`mdformat`), and ensure no loose ends or broken links remain.

______________________________________________________________________

## 3. Blog Post Lifecycle & Mandatory Workflow

When creating, updating, or moving a blog post, follow this end-to-end workflow:

```text
[Draft / Scaffold] ➔ [Refine & Visuals] ➔ [Mandatory 7-Point Linkage] ➔ [Quality Gate / Build]
```

### Mandatory 7-Point Update Checklist

Whenever adding, renaming, or moving a blog post, update all 7 locations:

1. **Post Document**: `docs/writing/<section>/<slug>/index.md` with valid YAML front matter (`title`, `date`, `authors: [sampathm]`, `categories:`, `description:`).
1. **Left Navigation**: Add entry under `nav > Writing > <Section>` in `mkdocs.yml`.
1. **Writing Hub Index**: Add link and 1-line summary to `docs/writing/index.md`.
1. **LLM Link-First Index**: Add URL and description under the section in `docs/llms.txt`.
1. **Generate Full LLM Text**: Run `python scripts/gen_llms_full.py` (or `make llms`).
1. **Redirect Maps**: If moving/renaming an existing post, add `old/path.md: new/path/index.md` in `mkdocs.yml` (`redirect_maps`).
1. **Verification**: Run `python scripts/score_post.py <path>` (target score ≥ 85) and `mkdocs build`.

______________________________________________________________________

## 4. Visuals & Content Patterns

- **Hero Image Requirement**:
  - Every post includes a co-located hero image placed immediately below the `# Title`.
  - Visual Style: Minimalist technical illustration, dark slate canvas, glowing neon accents, **zero embedded text/words**.
  - Must include generation prompt comment directly above the image tag:
    ```markdown
    <!-- AI Image Generation Prompt: A minimalist, clean modern tech illustration of <subject>, glowing cyan accents on a dark slate background, no text. -->
    ![<Title> Hero](hero.png)
    ```
- **Structure Pattern**:
  - Lead with a clear **TL;DR** or summary in the first section.
  - Use descriptive `##` and `###` headers so the right-hand table of contents renders cleanly.
  - Include 1–2 inline diagrams (Mermaid or screenshots/visuals) in technical deep dives.
  - Define all domain acronyms on first use.

______________________________________________________________________

## 5. Technical Overview & Link to Design

This repository is a static site built with **MkDocs Material** and deployed via GitHub Actions to GitHub Pages.

For the high-level system architecture, routing principles, build hooks, CI/CD deployment mechanics, and hero image design system specifications, refer to:
👉 [**`DESIGN.md`**](DESIGN.md)

______________________________________________________________________

## 6. Common Commands

| Command | Purpose |
| :--- | :--- |
| `make run` | Start local live preview server on `http://localhost:8099` |
| `make new-post TITLE="..." SECTION="..."` | Scaffold a new folder-per-post markdown file |
| `make llms` | Regenerate `docs/llms-full.txt` from `docs/llms.txt` |
| `mkdocs build` | One-shot build to test site compilation and nav links |
| `python scripts/score_post.py <path>` | Score draft for agent-readiness (0–100) |
| `mdformat <file>` | Format markdown cleanly (requires `mdformat-frontmatter`) |
