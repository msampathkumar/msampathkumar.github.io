# msampathkumar.github.io

> **Digital Garden & Engineering Reference**: Modern Cloud Architecture, Gemini AI, Agentic Workflows (A2A, ADK), and Developer Tooling.

Published live at **[msampathkumar.github.io](https://msampathkumar.github.io/)** via GitHub Pages.

______________________________________________________________________

## 10,000-Foot Architecture Overview

This repository hosts a content-first static website and engineering cookbook built with **MkDocs Material**. It is authored with an **"agents-first, human-delight"** philosophy — structured with machine-readable metadata, deterministic heading hierarchies, and curated indexing for LLM agents, alongside a fast, responsive interface for developers.

```text
[Content Markdown & Notebooks] ➔ [MkDocs Material Build Hooks] ➔ [GitHub Actions CI/CD] ➔ [GitHub Pages]
```

______________________________________________________________________

## Key Initiatives & Content Hubs

- **[Google Cloud Gemini Cookbook](https://msampathkumar.github.io/cookbook/)**: Practical, runnable tutorials and lessons for building and deploying production AI applications with Gemini and Vertex AI.
- **[Agent-to-Agent (A2A) Protocols](https://msampathkumar.github.io/writing/)**: Architecture deep dives on the Linux Foundation A2A protocol, multi-tenancy, and autonomous agent orchestration.
- **[Technical Deep Dives](https://msampathkumar.github.io/writing/)**: Cloud workstations, headless session automation (`tmux`), documentation-driven development, and cloud-native systems.
- **[Agent-Ready Indexes](https://msampathkumar.github.io/llms.txt)**: Hand-curated `llms.txt` and machine-generated `llms-full.txt` context streams optimized for AI assistants and crawler ingestion.

______________________________________________________________________

## Quick Reference

| Command | Description |
| :--- | :--- |
| `make run` | Start local preview server at `http://localhost:8099` |
| `make new-post TITLE="..." SECTION="..."` | Scaffold a new folder-per-post markdown document |
| `make llms` | Compile full inlined text into `docs/llms-full.txt` |
| `mkdocs build` | Test build compilation, navigation integrity, and links |

______________________________________________________________________

## Technical Documentation & Guides

- **[`DESIGN.md`](DESIGN.md)**: System architecture, directory routing, hero image design specifications, and automated build hook mechanics.
- **[`AGENTS.md`](AGENTS.md)**: Agent operating manual, content workflows, quality checklists, and publishing standards.

______________________________________________________________________

## License

Content and code samples are open source under the [Apache 2.0 License](LICENSE).
