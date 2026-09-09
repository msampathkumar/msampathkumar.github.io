# Part 2: Complete SCION Setup, Architecture & Troubleshooting Guide

> **Series Navigation:**
> **[Overview](README.md)** | **[Part 1: The Case for Containerized Agents](01-case-for-containerized-agents.md)** | **[Part 2: Setup, Architecture & Troubleshooting](02-setup-architecture-troubleshooting.md)** (Current) | **[Part 3: Practical User Guide & Workflows](03-user-guide-workflows.md)**

---

> A comprehensive, production-ready manual for setting up, configuring, and maintaining [SCION (Source-Code Inference & Orchestration Node)](https://github.com/GoogleCloudPlatform/scion) on macOS and Linux.

---

## 1. System Architecture

**SCION** runs autonomous AI coding agents concurrently inside isolated containers.

Instead of sharing your global filesystem and Git branch, SCION provisions an isolated container (Podman or Docker) and a dedicated Git worktree for each agent.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SCION Server (Hub)                            │
│  - Web UI: http://127.0.0.1:8080                                        │
│  - Runtime Broker API: http://127.0.0.1:9800                            │
│  - Central State DB: SQLite (~/.scion/hub.db)                           │
│  - Auth & Policy Engine (RBAC, Token Management)                        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                    Container Engine (Podman / Docker)
                                     │
   ┌─────────────────────────────────┴─────────────────────────────────┐
   │                                                                   │
┌──▼───────────────────────────────┐ ┌──▼───────────────────────────────┐
│     Agent Container A (Claude)   │ │  Agent Container B (Gemini-CLI)  │
│  - Git Worktree (Branch: ag-01)  │ │  - Git Worktree (Branch: ag-02)  │
│  - Isolated dependencies/tools   │ │  - Isolated dependencies/tools   │
│  - Mounted Workspace: /workspace │ │  - Mounted Workspace: /workspace │
│  - Tmux session + Scion Harness  │ │  - Tmux session + Scion Harness  │
└──────────────────────────────────┘ └──────────────────────────────────┘
```

### Core Architecture Components
1. **SCION Server (`scion server`)**:
   - Hosts the **Web Frontend** (port `8080`) for browser monitoring.
   - Hosts the **Runtime Broker** (port `9800`) for container operations.
   - Persists session state and metadata in SQLite (`~/.scion/hub.db`).
2. **Runtime Broker**: Manages the Podman/Docker container lifecycle (create, stop, inspect, remove).
3. **Agent Harnesses**: Pre-packaged images for LLM interfaces (`gemini-cli`, `claude`, `codex`, `copilot`, `hermes`, `opencode`, `antigravity`).
4. **Git Worktree Isolation**: Gives each agent a dedicated Git branch and working directory, enabling concurrent edits without conflicts.

---

## 2. System Requirements & Prerequisites

| Requirement | Details |
| :--- | :--- |
| **Operating System** | macOS (Apple Silicon / Intel) or Linux (Ubuntu, Debian, Fedora, Arch) |
| **Container Engine** | **Podman** (v4.5+ / recommended) or **Docker** (v24+) |
| **Git** | Git 2.30+ installed and initialized in target project directories |
| **Go** | Go 1.22+ (if compiling from source) |
| **Terminal Tools** | `curl`, `tmux` (included inside agent containers) |

---

## 3. Step-by-Step Installation & Setup

### Step 1: Install SCION
Install via Homebrew or build from source:

```bash
# Via Homebrew
brew tap GoogleCloudPlatform/scion https://github.com/GoogleCloudPlatform/scion
brew install scion

# Verify installation
scion version
```

### Step 2: Initialize and Start Container Runtime (Podman on macOS)
On macOS, Podman runs inside an optimized lightweight Linux VM.

```bash
# 1. Check if Podman machine exists
podman machine list

# 2. If no machine exists, initialize one
podman machine init --cpus 4 --memory 4096 --disk-size 50

# 3. Start the Podman machine
podman machine start

# 4. Verify socket connectivity
podman ps
```

> 💡 *Linux Users*: Ensure rootless Podman or the Docker daemon service is enabled: `systemctl --user enable --now podman.socket` or `sudo systemctl enable --now docker`.

### Step 3: Configure Default Harness
SCION ships with multiple harness configurations in `~/.scion/harness-configs/`. Ensure your default harness matches an installed configuration (such as `gemini-cli` or `claude`):

```bash
# Check available harness configurations
scion harness-config list

# Set default harness
scion config set default_harness_config gemini-cli
```

### Step 4: Configure LLM Authentication
SCION supports multiple authentication strategies depending on your model provider:

#### A. Google Gemini (Google AI Studio API Key)
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

#### B. Google Cloud Vertex AI
```bash
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI="true"
# Ensure Application Default Credentials (ADC) are configured
gcloud auth application-default login
```

#### C. Anthropic Claude / OpenAI Codex
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### Step 5: Launch the SCION Server
Start the background server daemon:

```bash
# Start the server
scion server start

# Check status and developer token
cat ~/.scion/server.log | grep -E "Developer token|Starting Web Frontend"
```

Set your developer token in your shell environment:
```bash
export SCION_DEV_TOKEN="your-developer-token-from-log"
```

Access the Web UI in your browser:
👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

## 4. Troubleshooting & Known Error Resolutions

### ❌ Issue 1: `runtime broker returned error 500: ... exit status 125`
- **Error Log**: `unable to connect to Podman socket: failed to connect: dial tcp 127.0.0.1:60279: connect: connection refused`
- **Root Cause**: The Podman virtual machine on macOS is stopped or paused.
- **Solution**:
  ```bash
  podman machine start
  podman ps
  ```

---

### ❌ Issue 2: `failed to find harness-config "gemini": harness-config "gemini" not found`
- **Error Log**: `API Error: code: not_found, failed to find harness-config "gemini"`
- **Root Cause**: `settings.yaml` specified `gemini` instead of the built-in package name `gemini-cli`.
- **Solution**:
  ```bash
  scion config set default_harness_config gemini-cli
  ```

---

### ❌ Issue 3: `401 UNAUTHENTICATED: ACCESS_TOKEN_TYPE_UNSUPPORTED`
- **Error Log**: `google.ai.generativelanguage.v1beta.GenerativeService.StreamGenerateContent returned 401 UNAUTHENTICATED`
- **Root Cause**: The container attempted to contact the AI Studio developer endpoint with incompatible credentials.
- **Solution**: Explicitly set the auth method when launching the agent:
  ```bash
  # Option 1: API Key
  export GEMINI_API_KEY="your-key"
  scion start my-agent "task" --harness-auth api-key

  # Option 2: OAuth Credentials File
  scion start my-agent "task" --harness-auth auth-file

  # Option 3: Vertex AI on Google Cloud
  scion start my-agent "task" --harness-auth vertex-ai
  ```

---

### ❌ Issue 4: Agents Not Appearing in the Web UI
- **Symptom**: Agent created via CLI appears in `scion list --all` but not on the Web dashboard.
- **Root Cause**: SCION scopes agents by project directory. The Web UI might currently be viewing the `Global` project.
- **Solution**: In the Web UI top/sidebar navigation, switch the project selector to match your directory name (e.g. `a2a-cli`).

---

## 5. Health Check & Verification Checklist

Run this quick checklist anytime to confirm your SCION environment is healthy:

```bash
# 1. Check system prerequisites
scion doctor

# 2. Verify Podman is answering commands
podman info

# 3. Check active agents across all projects
scion list --all

# 4. Verify server logs for errors
tail -n 30 ~/.scion/server.log
```

---

## 6. Next in This Series

- **Part 1**: [**The Case for Containerized Agents (Overview & Deep Dive)**](01-case-for-containerized-agents.md)
- **Part 3**: [**SCION User Guide, Workflows & Practical Cheatsheet**](03-user-guide-workflows.md) — Master day-to-day commands, multi-tasking workflows, and repository reviews.
