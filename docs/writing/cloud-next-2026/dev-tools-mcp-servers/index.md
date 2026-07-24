---
title: "Google Cloud Next 2026 (3/5) - Developer Tools, Guides, and MCP Servers"
date: 2026-05-02
authors: [sampathm] 
categories:
- "Google Cloud Next 2026"
---
![Google Cloud Next 2026](https://storage.googleapis.com/gweb-cloudblog-publish/images/GCN26_102_BlogHeader_2436x1200_Opt_4_Dark.max-2500x2500.jpg)

# Google Cloud Next 2026 (3/5) - Developer Tools, Guides, and MCP Servers

> This is from my personal collection/notes. Hope you find it informative :)

In my first post, we reviewed hardware updates like 8th-Gen TPUs, Axion
processors, and Virgo Networks. In my second, we peeked into Google Cloud's
Gemini Enterprise Agent Platform and its underlying models. For this third
part, let's shift our focus to the Developer Tools that Google Cloud makes
available to users.

______________________________________________________________________

## 👨🏻‍💻 Developer Tools, Guides, and MCP Servers

- [**Google ADK**](https://adk.dev/): The open-source agent development
  framework that lets you build, debug, and deploy reliable AI agents at
  enterprise scale. Available in Python, TypeScript, Go, and Java.
- [**Agent CLI**](https://github.com/google/agents-cli): Serves as both a CLI
  tool and a **Skill package** for your agentic developer environments
  (including Gemini CLI, Antigravity, Codex, Claude Code, and others).
- [**Agent Skills**](https://github.com/google/skills/tree/main): Pre-packaged
  agent skills tailored for Google products and technologies, including Google
  Cloud integrations.
- [**Google Antigravity**](https://antigravity.google/): An advanced agentic
  development platform that evolves the traditional IDE into an autonomous,
  multi-surface "mission control" where AI agents plan, execute, and verify
  complex software tasks.
- [**Google Cloud Data Agent Kit**](https://docs.cloud.google.com/data-cloud-extension/vs-code/install):
  A rich Visual Studio Code extension designed for data engineers, scientists,
  and app developers to efficiently manage data assets, run queries, and deploy
  data pipelines.

## 🔌 MCP Servers

- [**Google Workspace MCP Servers**](https://docs.cloud.google.com/mcp/supported-products#google-workspace-mcp-servers):
  A collection of MCP server your agents can use to interact with Google
  Workspace products(Calendar, Gmail, Drive, etc).
- [**Google Cloud MCP Servers**](https://docs.cloud.google.com/mcp/supported-products#google-cloud-mcp-servers):
  A collection of MCP server your agents can use to interact with Google Cloud
  products(Agent Registry, BigQuery, Cloud Run, Cloud Sql, Firestore,
  Memorystore, Pub/Sub, etc).

## 📚 Free Learning Resources & References

- **Professional Certification**:
  [Google AI Professional Certificate](https://www.coursera.org/professional-certificates/google-ai)
  (8 hrs)
- **Hands-on Labs**: Over 75 free codelabs available at
  [Google Cloud Next 2026 Codelabs](https://codelabs.developers.google.com/?event=googlecloudnext2026)
- **Sub-Agents Deep Dive**: Read "Mastering Gemini CLI Subagents" on Medium
  ([Part 1](https://medium.com/google-cloud/mastering-gemini-cli-subagents-part-1-a4666091c154)
  &
  [Part 2](https://medium.com/google-cloud/mastering-gemini-cli-subagents-part-2-tool-isolation-advanced-governance-af4cbb287204))
- **White Paper**: Dive into enterprise security with
  [Agent Security Overview](https://services.google.com/fh/files/events/agent_security.pdf)
- **Atlas Agents (WIP)**: Check out the work-in-progress book by A. Gulli on
  [GitHub](https://github.com/agulli/atlas-agents)

______________________________________________________________________

*In my fourth post, I will unpack the "Agentic Data Cloud"—from Spanner Omni to
the standardized Iceberg data layer, along with the newly governing A2A & MCP
protocols. Stay tuned!*
