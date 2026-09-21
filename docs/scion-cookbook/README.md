# 🚀 SCION Cookbook: Containerized Multi-Agent AI Engineering

Welcome to the **SCION (Source-Code Inference & Orchestration Node) Cookbook**! This hands-on series explores how to run, orchestrate, and supervise concurrent autonomous AI coding agents inside isolated containers.

---

## 💡 Why SCION?

Autonomous AI coding agents can inspect codebases, execute shell commands, create branches, and run tests. Running them directly on your host machine introduces serious risks:

- **Host Pollution & Safety**: Autonomous commands can alter global state, overwrite dependencies, or run destructive scripts.
- **Sequential Bottlenecks**: Developers must wait for one agent to finish before starting another.
- **Git Branch Collisions**: Multiple agents on the same branch clash over uncommitted edits and index locks.
- **Credential Exposure**: Unrestricted host execution risks exposing environment variables, tokens, and SSH keys.

**SCION** packages each agent into an ephemeral container (Podman or Docker) with a **dedicated Git worktree, isolated filesystem, and scoped runtime credentials**.

---

## 📚 Cookbook Sections

This cookbook is structured into four practical parts:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             SCION Cookbook Series                                │
│                                                                                  │
│   Part 1: The Case for Containerized Agents                                      │
│   ├── Architecture breakdown: Hub, Runtime Broker, and Harnesses                 │
│   └── Why container isolation unlocks true multi-agent parallelism               │
│                                                                                  │
│   Part 2: Setup, Architecture & Troubleshooting                                  │
│   ├── Podman & Docker runtime initialization (macOS & Linux)                     │
│   ├── Multi-provider auth setup (Gemini, Vertex AI, Claude, OpenAI)              │
│   └── Battle-tested solutions for common error codes & socket issues             │
│                                                                                  │
│   Part 3: Practical User Guide & Workflows                                       │
│   ├── Master the CLI cheatsheet (start, message, look, attach, suspend, resume) │
│   ├── Non-intrusive monitoring vs interactive tmux steering (Ctrl+B, D)          │
│   └── Real-world multi-agent workflows on a Go repository                        │
│                                                                                  │
│   Part 4: Developer Workflow: Skills, Rules & Templates                          │
│   ├── Skill-oriented architecture and Hub Skill Bank resolution                 │
│   ├── Guardrail enforcement with repository-level AGENTS.md                      │
│   ├── Curating reusable agent templates and role specialization                  │
│   └── Multi-day intermittent lifecycles (suspend/resume/cdw) & Kanban model      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

1. **[Part 1: The Case for Containerized Agents](01-case-for-containerized-agents.md)**  
   *Deep dive into the architecture of container-isolated agent orchestration and why it changes software engineering for developers, leads, and CTOs.*

2. **[Part 2: Setup, Architecture & Troubleshooting](02-setup-architecture-troubleshooting.md)**  
   *Step-by-step setup guide for macOS and Linux, configuring Podman/Docker, setting up harness credentials (Gemini, Claude, Vertex AI), and resolving runtime errors.*

3. **[Part 3: Practical User Guide & Workflows](03-user-guide-workflows.md)**  
   *Comprehensive operational manual, command cheatsheets, session lifecycle management, and real-world multi-agent repository audits.*

4. **[Part 4: Developer Workflow: Skills, Rules & Templates](04-developer-workflow-skills-templates.md)**  
   *Designing skill-oriented agent systems, enforcing project-level rules with AGENTS.md, authoring templates, and mastering multi-day intermittent workflows.*

---

## 🛠️ Prerequisites

To follow the recipes in this cookbook, ensure you have:
- **Operating System**: macOS (Apple Silicon or Intel) or Linux (Ubuntu, Debian, Fedora, Arch).
- **Container Engine**: [Podman](https://podman.io/) (recommended on macOS) or [Docker](https://www.docker.com/).
- **Git**: Git 2.30+ installed.
- **API Access**: Access to Google Gemini (`GEMINI_API_KEY` or Vertex AI credentials), Anthropic Claude, or OpenAI Codex.

---

[Start Part 1: The Case for Containerized Agents →](01-case-for-containerized-agents.md){ .md-button .md-button--primary }
