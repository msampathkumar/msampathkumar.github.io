# Agent Instructions & Operating Manual

This document defines the agent operating principles, user goals, content workflows, and quality standards for `msampathkumar.github.io`.

For full technical architecture, site layout, CI/CD pipeline, and design specifications, see [**`DESIGN.md`**](DESIGN.md).

______________________________________________________________________

## 1. User Profile & Strategic Ambitions

- **Site Owner**: Sampath Kumar (`sampathm`)
- **Focus Areas**: Google Cloud, Gemini AI, Agentic Workflows (A2A, ADK), Modern Cloud Architecture, and Developer Tooling.
- **Audience & Tone**: Professional cloud architects, AI engineers, and technical leaders. Clean, direct, highly structured, and actionable ("agents-first, human-delight").

______________________________________________________________________

## 2. Goals & Non-Goals

### 🎯 Goals
- **Global Reach**: Reach 50 million viewers and 20 million subscribers across technical distribution channels (YouTube, Medium, LinkedIn, Blog) by end of 2026.
- **Flagship References**: Establish the "Google Cloud Gemini Cookbook" and "A2A / Agentic Systems" as premier industry reference hubs.
- **Agent-First Architecture**: Deliver fully machine-readable, deterministic context (`/llms.txt`, `/llms-full.txt`) alongside human-delightful UI.
- **High Technical Rigor**: Maintain 100% runnable code samples, rigorous architectural diagrams, and verified documentation across all guides.

### 🚫 Non-Goals
- **No Unvetted Demos**: Avoid publishing unrunnable snippets, incomplete toys, or hallucinated APIs.
- **No Aggressive Marketing Jargon**: Avoid vague buzzwords or hype; keep content technical, direct, and architecture-focused.
- **No Ad-Hoc URL Changes Without Redirects**: Never break existing URLs or search engine inbound links; preserve backward compatibility.
- **No Unpermissioned Commits**: Never perform autonomous git commits or pushes without explicit approval.

______________________________________________________________________

## 3. Mandatory Agent Rules

1. **Explicit Permission Required**: **Never execute `git commit` or `git push` without explicit user permission.**
2. **Requirements Clarity**: Ensure at least 80% clarity on requirements before executing large changes. Proactively seek clarification when uncertain.
3. **Sequential & Minimal Execution**: Plan sequentially, execute task-by-task, and apply minimal necessary code modifications.
4. **Preserve Legacy & History**: Comment out deprecated code/logic with clear rationale rather than deleting unprompted. Always configure client-side redirect maps (`redirect_maps` in `mkdocs.yml`) when moving published URLs.
5. **Always Land Cleanly**: When completing a task, verify the build (`mkdocs build --strict`), format touched Markdown (`mdformat`), and ensure no loose ends or broken links remain.

______________________________________________________________________

## 4. Blog Post Lifecycle & Mandatory Workflow

When creating, updating, or moving a blog post, follow this end-to-end workflow:

```text
[Draft / Scaffold] ➔ [Refine & Visuals] ➔ [Mandatory 7-Point Linkage] ➔ [Quality Gate / Build]
```

### Mandatory 7-Point Update Checklist

Whenever adding, renaming, or moving a blog post, update all 7 locations:

1. **Post Document**: `docs/writing/<section>/<slug>/index.md` with valid YAML front matter (`title`, `date`, `authors: [sampathm]`, `categories:`, `description:`).
1. **Left Navigation**: Add entry under `nav > Writing > <Section>` in `mkdocs.yml` (**ordered reverse-chronologically with newest posts at the top**).
1. **LLM Link-First Index**: Add URL and description under the section in `docs/llms.txt`.
1. **Generate Full LLM Text**: Run `python scripts/gen_llms_full.py` (or `make llms`).
1. **Writing Hub & README Index**: Run `python scripts/gen_readme.py` (or `make readme`) to synchronize both `docs/writing/index.md` and `README.md` with grouped reverse-chronological listings.
1. **Redirect Maps**: If moving/renaming an existing post, add `old/path.md: new/path/index.md` in `mkdocs.yml` (`redirect_maps`).
1. **Verification**: Run `python scripts/score_post.py <path>` (target score ≥ 85) and `mkdocs build`.


______________________________________________________________________

## 5. Visuals & Content Patterns

- **Standard Article Structure**:
  - `[# Title]` ➔ `[Metadata Bar (Date · Read time · Author)]` (auto-injected by build hook) ➔ `[Hero Image]` ➔ `[TL;DR / Body]`.
- **Hero Image Requirement**:
  - Every post includes a co-located hero image placed below the `# Title` and metadata bar.
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

## 6. Technical Overview & Link to Design

This repository is a static site built with **MkDocs Material** and deployed via GitHub Actions to GitHub Pages.

For the high-level system architecture, routing principles, build hooks, CI/CD deployment mechanics, and hero image design system specifications, refer to:
👉 [**`DESIGN.md`**](DESIGN.md)

______________________________________________________________________

## 7. Common Commands

| Command | Purpose |
| :--- | :--- |
| `make run` | Start local live preview server on `http://localhost:8099` |
| `make new-post TITLE="..." SECTION="..."` | Scaffold a new folder-per-post markdown file |
| `make llms` | Regenerate `docs/llms-full.txt` from `docs/llms.txt` |
| `mkdocs build` | One-shot build to test site compilation and nav links |
| `python scripts/score_post.py <path>` | Score draft for agent-readiness (0–100) |
| `mdformat <file>` | Format markdown cleanly (requires `mdformat-frontmatter`) |
