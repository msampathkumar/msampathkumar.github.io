# Part 3: SCION User Guide & Workflow Manual

> **Series Navigation:**
> **[Overview](README.md)** | **[Part 1: The Case for Containerized Agents](01-case-for-containerized-agents.md)** | **[Part 2: Setup, Architecture & Troubleshooting](02-setup-architecture-troubleshooting.md)** | **[Part 3: Practical User Guide & Workflows](03-user-guide-workflows.md)** (Current)

---

> A practical step-by-step guide for developers, team leads, and architects on operating [SCION](https://github.com/GoogleCloudPlatform/scion) agents for daily engineering workflows.

---

## 1. Quick Reference: Basic Command Cheatsheet

| Purpose | Command | Description |
| :--- | :--- | :--- |
| **Launch Agent (Background)** | `scion start <name> "<task>"` | Creates and starts agent asynchronously |
| **Launch Agent (Interactive)** | `scion start <name> "<task>" --attach` | Starts agent and connects terminal directly |
| **Select Model/Harness** | `scion start <name> "<task>" --harness claude` | Uses specific harness (`claude`, `gemini-cli`, `codex`, `copilot`, etc.) |
| **Send Task / Follow-up** | `scion message <name> "<task>"` | Dispatches a new task or query to a running agent |
| **Interrupt & Steer** | `scion message <name> "<task>" --interrupt` | Interrupts current agent loop and redirects it |
| **Attach to Terminal** | `scion attach <name>` | Connects to live tmux session *(Detach: `Ctrl+B`, `D`)* |
| **Inspect Screen (Read-Only)** | `scion look <name>` | Takes a non-intrusive snapshot of agent screen |
| **View Full History** | `scion look <name> --full` | Dumps complete terminal scrollback history |
| **View Container Logs** | `scion logs <name>` | Fetches stdout/stderr container logs |
| **List Current Project Agents** | `scion list` | Lists active agents for current repo |
| **List All Agents** | `scion list --all` | Lists agents across all projects |
| **Filter Active Agents** | `scion list --running` | Shows only actively executing agents |
| **Suspend Agent** | `scion suspend <name>` | Pauses container to free CPU/RAM (preserves state) |
| **Resume Agent** | `scion resume <name>` | Restores a suspended or stopped agent |
| **Stop Agent** | `scion stop <name>` | Gracefully halts agent execution |
| **Delete Agent** | `scion delete <name> -y` | Destroys container, worktree, and temp branch |
| **Switch to Agent Workspace** | `scion cdw <name>` | Navigates host shell into the agent's git worktree |
| **Web Dashboard** | [http://127.0.0.1:8080](http://127.0.0.1:8080) | Full browser GUI for agent monitoring & chat |

---

## 2. Core Concepts: Multi-Tasking vs Agent Deletion

### Treat Agents as Stateful Workers, Not Single-Turn Scripts
Do not destroy an agent after a single prompt.

**SCION agents are persistent, stateful workers:**
1. **Memory & Context**: The agent retains prior tool outputs, file inspections, and reasoning steps across prompts.
2. **Git Worktree Isolation**: Edits stay in the agent's dedicated Git branch until you merge or delete them.
3. **Sequential Execution**: Send iterative prompts, review requests, and bug fixes to the same running agent with `scion message`.

```
┌──────────────────────────────────────────────────────────────────┐
│                   Agent Lifecycle Workflow                       │
│                                                                  │
│  1. scion start agent-01 "Task 1"                                │
│       │                                                          │
│       ▼                                                          │
│  2. Agent executes Task 1 in background                          │
│       │                                                          │
│       ▼                                                          │
│  3. scion message agent-01 "Follow-up Task 2" (Reuses context!)  │
│       │                                                          │
│       ▼                                                          │
│  4. scion message agent-01 "Refine tests Task 3"                 │
│       │                                                          │
│       ▼                                                          │
│  5. Work completed? ───► scion delete agent-01 -y (Cleanup)      │
└──────────────────────────────────────────────────────────────────┘
```

- **Keep Running**: Keep the agent active while iterating on a feature, bug investigation, or review pass.
- **Suspend**: Run `scion suspend` to pause work and free resources without losing context.
- **Delete**: Run `scion delete` only after merging or discarding the work.

---

## 3. Step-by-Step Operations Guide

### 3.1 Creating & Starting Agents

```bash
# Standard background start (recommended)
scion start reviewer "Audit internal/runner for error handling"

# Start with an explicit LLM harness
scion start doc-writer "Update README.md" --harness claude

# Pre-create configuration without launching immediately
scion create benchmarker "Run benchmarks on parser"
# Launch later:
scion resume benchmarker
```

---

### 3.2 Interacting, Messaging & Steering Tasks

#### Sending Follow-up Instructions
```bash
# Dispatch next prompt to the same active agent
scion message reviewer "Great, now write unit tests covering the edge cases you found"

# Attach a document or spec file with the message
scion message reviewer "Verify implementation against this spec" --attach specification/a2a.json
```

#### Interrupting a Running Agent
Redirect an agent that is off-track:
```bash
scion message reviewer "Stop running benchmarks; focus only on code readability" --interrupt
```

---

### 3.3 Terminal Monitoring & The Attach/Detach Rule

#### Non-intrusive Snapshot (`scion look`)
```bash
# View instant snapshot of the agent terminal
scion look reviewer

# View complete scrollback history
scion look reviewer --full
```

#### Interactive Terminal (`scion attach`)
Directly interact with the agent harness:
```bash
scion attach reviewer
```

> ⚠️ **CRITICAL: How to exit an attached session:**
> - ❌ **NEVER** type `exit` or close the terminal (this kills the agent container).
> - ✅ **PRESS `Ctrl + B`**, release both keys, then press **`D`** (*Detach*).
> - You return to your host shell while the agent continues running in the background.

---

### 3.4 Stopping, Suspending & Deleting

```bash
# Suspend container to save host memory/CPU (preserves state)
scion suspend reviewer

# Resume container execution
scion resume reviewer

# Stop agent gracefully
scion stop reviewer

# Delete agent, container, and temporary worktree
scion delete reviewer -y
```

---

## 4. Practical Workflows on `a2a-cli` (Example Repository)

The following workflows show how to use SCION safely on a real Go CLI codebase ([`a2a-cli`](https://github.com/GoogleCloudPlatform/scion)).

### Workflow 1: Read-Only Architectural Exploration & Onboarding
**Scenario**: Survey a repository structure without manual file exploration.

```bash
cd /path/to/a2a-cli

# 1. Start exploration agent
scion start explorer "Perform a read-only survey of this codebase. Explain the role of main.go, the internal/ directory structure, and command routing."

# 2. Check output non-intrusively
scion look explorer

# 3. Ask follow-up question to the SAME agent
scion message explorer "Which third-party libraries in go.mod handle CLI argument parsing and HTTP communication?"

# 4. Read the answer
scion look explorer --full

# 5. Clean up when finished
scion delete explorer -y
```

---

### Workflow 2: Documentation & README Quality Audit
**Scenario**: Audit documentation against actual CLI flags.

```bash
cd /path/to/a2a-cli

# 1. Launch doc reviewer
scion start doc-auditor "Compare README.md against flags in internal/commands/. Highlight outdated flags or missing prerequisites. Do not modify files yet."

# 2. Inspect findings
scion look doc-auditor

# 3. Instruct the same agent to draft improvements
scion message doc-auditor "Draft an updated 'Usage Examples' section in Markdown format based on your review."

# 4. View suggested draft
scion look doc-auditor --full

# 5. Review isolated branch workspace if needed
scion cdw doc-auditor

# 6. Clean up
scion delete doc-auditor -y
```

---

### Workflow 3: Code Readability & Idiomatic Go Review
**Scenario**: Audit code for Go best practices and error wrapping.

```bash
cd /path/to/a2a-cli

# 1. Launch auditor with Claude harness
scion start go-reviewer "Review internal/ for idiomatic Go patterns, fmt.Errorf wrapping with %w, and mutex safety. Generate a bulleted report prioritized by severity." --harness claude

# 2. Check the review report
scion look go-reviewer

# 3. Clean up
scion delete go-reviewer -y
```

---

## 5. Summary & Best Practices for Teams

1. **Parallel Execution**: Launch multiple specialized agents concurrently (e.g., `test-writer`, `doc-reviewer`, `security-scanner`) without them interfering with each other.
2. **Preserve Context**: Send sequential messages to the same agent rather than constantly recreating new ones.
3. **Always Detach Cleanly**: Use `Ctrl + B`, then `D` when using `scion attach`.
4. **Use Web UI for Team Visibility**: Open `http://127.0.0.1:8080` for team demos, live logs, and project-level overview.

---

## 6. Series Navigation

- **Part 1**: [**The Case for Containerized Agents (Overview & Deep Dive)**](01-case-for-containerized-agents.md) — The rationale and architectural benefits of container-isolated agent orchestration.
- **Part 2**: [**Complete SCION Setup, Architecture & Troubleshooting Guide**](02-setup-architecture-troubleshooting.md) — Prerequisites, runtime installation, and resolving real-world errors.
