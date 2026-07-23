---
name: "agent-ready-blog"
description: "Score and improve a blog post/page for agent-readiness (agents-first content) on the msampathkumar.github.io MkDocs site. Use when scoping a draft post before publishing, asking \"is this good for agents/LLMs?\", or preparing content in docs/blog/posts. Checks structure, TOC-worthy headings, TL;DR, canonical/front matter, runnable code, and llms.txt inclusion."
---

# agent-ready-blog

## Overview

This site is **agents-first**: content should be easy for an AI agent (and an
LLM crawler) to parse, extract, and act on — then also pleasant for humans. This
skill scores a post against that bar and drives concrete fixes. It pairs a
mechanical scorer (`scripts/score_post.py`) with an editorial rubric you apply
with judgement.

## When to use this

- Before publishing a new post in `docs/blog/posts/`.
- When asked "is this good for agents?", "make this agent-ready", or to review a
  draft's structure.
- After importing posts (e.g. via `make import-devto`) and before promoting them
  from `_internal/devto_import/` into `docs/blog/posts/`.

## When NOT to use this

- General prose editing unrelated to this site.
- Non-blog pages where structure is dictated elsewhere (e.g. cookbook lessons).

## Steps

1. **Run the mechanical scorer** on the target file:
   `python scripts/score_post.py docs/blog/posts/<slug>.md`
   It prints a 0-100 score and per-check PASS/FAIL. Treat <70 as "not ready".
2. **Fix the mechanical gaps** it flags (see rubric). Re-run until >=85.
3. **Apply the editorial rubric** (judgement, not scriptable) below.
4. **Verify parity**: the post is listed in `mkdocs.yml` nav and (if canonical)
   in `docs/llms.txt`; then run `make llms` so `llms-full.txt` stays in sync.
5. **Build**: `mkdocs build` must be warning-clean; `mdformat <file>` the post
   (the `mdformat-frontmatter` plugin must be installed — it is in
   requirements.txt — or mdformat will corrupt the `---` front matter).

## Rubric — what "agent-ready" means

**Structure (parseability)**
- Exactly one H1 (or rely on front-matter title); sections at `##`/`###` so a
  right-hand TOC renders. At least two section headings.
- Lead with the answer: a **TL;DR** or summary in the first screenful. Agents
  extract the top of the document first.
- Descriptive headings (a heading should make sense out of context).

**Front matter (machine metadata)**
- `title`, `date`, `authors`, `categories` present and valid YAML.
- `description`: a one-sentence summary written for a machine — this is what
  feeds `llms.txt` and search snippets.
- `canonical_url` if the post was published elsewhere first (dev.to/Medium), to
  avoid duplicate-content penalties.

**Substance (actionability)**
- Runnable code, commands, or a diagram where relevant — agents reuse these.
- Concrete, checkable claims over vague assertions. Link primary sources.
- Define acronyms on first use (A2A, ADK, MCP, RAG).

**Site integration**
- Wired into `mkdocs.yml` nav (curated) so it isn't orphaned.
- Appears on the Home page automatically (via `hooks/latest_posts.py`) once it
  has a title + date.
- Included in `docs/llms.txt` if it's canonical content, then `make llms`.

## Notes

- The scorer is heuristic: a poem or micro-post may legitimately score low —
  use judgement, don't force structure onto content that has none.
- Agents-first does not mean human-hostile: keep it readable for both.
