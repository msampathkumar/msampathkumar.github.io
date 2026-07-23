# How I configured Hemes Agents to run using Google Cloud Gemini Models

## Initial setup

> **Note:** Run these commands from my personal pc.

To make it easy to reuse, I am defining the variables in the following manner.

```bash
GCP_PROJECT_ID=...            # Update this line ---------------------
GCP_PROJECT_ZONE=us-central1-a
VM_NAME=ai-development-vm
```

SSH to the VM

```bash
gcloud compute ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME" -- -L 8888:127.0.0.1:8888 -L 9595:127.0.0.1:9595
```

# Hermes Agent Setup

> **Note:** Run these commands from the VM.

To install [Hermes-agent](https://github.com/NousResearch/hermes-agent), use the following command:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

## Setup options

**Caution:** Once you the installation command was run be-careful and do not accidently press `ENTER` key as you man accidently select options you were not aware of. (In my case, I accidently selecting Quick setup and it took me a while figure out what was happending.)

Logs

```
How would you like to set up Hermes?
  ↑↓ navigate  ENTER/SPACE select  ESC cancel

 → (●) Quick Setup (Nous Portal) — free OAuth login, no API keys, model + tools (recommended)
   (○) Full setup — configure every provider, tool & option yourself (bring your own keys)
   (○) Blank Slate — everything off except the bare minimum; opt in to each capability
```

Once the installation is done, I was immediately prompted to go to [https://portal.nousresearch.com/manage-subscription](https://portal.nousresearch.com/manage-subscription)
and complete the subscription process. But you can safe press `ctrl+c` to exit that step and you will be prompted as below. You can find what I have selected.

Here are my selection logs

```
Select terminal backend:
  ↑↓ navigate  ENTER/SPACE select  ESC cancel

   (○) Local - run directly on this machine (default)
   (○) Docker - isolated container with configurable resources
   (○) Modal - serverless cloud sandbox
   (○) SSH - run on a remote machine
   (○) Daytona - persistent cloud development environment
   (○) Singularity/Apptainer - HPC-friendly container
 → (●) Keep current (local)

Connect a messaging platform? (Telegram, Discord, etc.)
  ↑↓ navigate  ENTER/SPACE select  ESC cancel

   (●) Set up messaging now (recommended)
 → (○) Skip — set up later with 'hermes setup gateway'

```

After installation, you need to reload the shell and then you can start the hermes agent.

```bash
source ~/.bashrc

# back-up copy
cp -p ~/.hermes/config.yaml ~/.hermes/config.yaml.backup

# edit config
vi ~/.hermes/config.yaml # or use "hermes config edit"
```

## Know about what has to be done

Depending on how you intial setup option goes, you need to ensure to have 3 section in the `~/.hermes/config.yaml` file. In my case, I had to edit the `config.yaml` file to add vertexai details.

The first section contain information about model:

```yaml
model:
  default: google/gemini-3.1-flash-lite
  provider: vertex
```

The second section contain information about the Project ID

```yaml
vertex:
  project_id: GCP_PROJECT_ID
```

(Optional) The third section is about auxiliary section.

```yaml
auxiliary:
  title_generation:
    provider: vertex
    model: google/gemini-3.1-flash-lite
```

### Model config file updation

If you followed the same path as I did them, you can edit the config file directly or just check that above section are present in your config file.

Update the model details in Line 1-3 of `~/.hermes/config.yaml`

```bash
$ head ~/.hermes/config.yaml
model:
  default: google/gemini-3.1-flash-lite
  provider: vertex
vertex:
  project_id: GCP_PROJECT_ID # Update this line ---------------------
auxiliary:
  title_generation:
    provider: vertex
    model: google/gemini-3.1-flash-lite
agent:
```

Here is the latest difference

```
$ diff ~/.hermes/config.yaml ~/.hermes/config.yaml.backup
2,9c2,4
<   default: google/gemini-3.1-flash-lite
<   provider: vertex
< vertex:
<   project_id: GCP_PROJECT_ID
< auxiliary:
<   title_generation:
<     provider: vertex
<     model: google/gemini-3.1-flash-lite
---
>   default: anthropic/claude-opus-4.6
>   provider: auto
>   base_url: https://openrouter.ai/api/v1
```

## Model Selection

There could a few formatting issues or other, so I ran `hermes model` to select the model. During the selection, you will be prompted to select provider, project name and model

```
hermes model
```

Logs

```
sampathm@ai-development-vm:~$ hermes model
Warning: Unknown provider 'vertex'. Check 'hermes model' for available providers, or run 'hermes doctor' to diagnose config issues. Falling back to auto provider detection.

  Current model:    google/gemini-3.1-flash-lite
  Active provider:  none


  Vertex credentials: Application Default Credentials (ADC)
    Vertex uses OAuth2, not a static API key. Either:
      • run 'gcloud auth application-default login', or
      • set VERTEX_CREDENTIALS_PATH in ~/.hermes/.env to a service account JSON

  GCP project ID [GOOGLE_CLOUD_PROJECT=.....]:
  Vertex region [global]:

Enter model name: google/gemini-3.1-flash-lite
  Default model set to: google/gemini-3.1-flash-lite (via Google Vertex AI, global)
```

```
   (○) Nous Portal (Everything your agent needs, 300+ models with bundled tool use)
   (○) OpenRouter (Pay-per-use API aggregator)
   (○) Mixture of Agents (named presets; aggregator acts after reference models)
   (○) NovitaAI (Cloud: Model API, Agent Sandbox, GPU Cloud)
   (○) LM Studio (Local desktop app with built-in model server)
   (○) Anthropic (Claude models via API key or Claude Code)
   (○) OpenAI ▸ (Codex CLI or direct OpenAI API)
   (○) Qwen Cloud / DashScope (Qwen + multi-provider)
   (○) xAI Grok ▸ (Direct API or SuperGrok / Premium+ OAuth)
   (○) Xiaomi MiMo (MiMo-V2.5 and V2 models: pro, omni, flash)
   (○) Tencent TokenHub (Hy3 Preview via tokenhub.tencentmaas.com)
   (○) NVIDIA NIM (Nemotron models via build.nvidia.com or local NIM)
   (○) GitHub Copilot ▸ (GitHub token API or copilot --acp process)
   (○) Hugging Face Inference Providers
 → (●) Google AI Studio (Native Gemini API)
   (○) Google Vertex AI (Gemini via GCP; OAuth2 service account or ADC, GCP billing/quotas)
   (○) DeepSeek (V3, R1, coder, direct API)
   (○) Z.AI / GLM (Zhipu direct API)
   (○) Kimi / Moonshot ▸ (Coding Plan, Moonshot global & China endpoints)
   (○) StepFun Step Plan (Agent / coding models via Step Plan API)
   (○) MiniMax ▸ (Global, OAuth Coding Plan & China endpoints)
   (○) Ollama Cloud (Cloud-hosted open models, ollama.com)
   (○) Arcee AI (Trinity models, direct API)
   (○) GMI Cloud (Multi-model direct API)
   (○) Kilo Code (Kilo Gateway API)
   (○) OpenCode ▸ (Zen pay-as-you-go or Go subscription)
   (○) AWS Bedrock (Claude, Nova, Llama, DeepSeek; IAM or API key)
   (○) Azure Foundry (OpenAI-style or Anthropic-style endpoint, your Azure AI deployment)
   (○) Qwen OAuth (Reuses local Qwen CLI login)
```

Logs

```
Select default model:
  ↑↓ navigate  ENTER/SPACE select  / search  ESC cancel

   (○) google/gemini-3-pro-preview
   (○) google/gemini-3-flash-preview
 → (●) Enter custom model name
   (○) Skip (keep current)
```

Since we are already in Google Cloud VM with proper service account access, we can select `Google Cloud` as the provider.

### Test Run

To start a quick session as below and prompt the model for question

```bash
hermes
```

**Note:** There were warning like `Vertex` is not recognised and Model may not work. But I ignored them for now.

Here is the final config.yaml file.

```bash
$ diff ~/.hermes/config.yaml ~/.hermes/config.yaml.backup
2,3c2,4
<   default: google/gemini-3.1-flash-lite
<   provider: vertex
---
>   default: anthropic/claude-opus-4.6
>   provider: auto
>   base_url: https://openrouter.ai/api/v1
79,82d79
< auxiliary:
<   title_generation:
<     provider: vertex
<     model: google/gemini-3.1-flash-lite
122,123d118
< vertex:
<   project_id: GCP_PROJECT_ID
```

# Uninstall

If you wish to uninstall hermes agent, you can use the following command:

```bash
# Uninstall using hermes CLI
hermes uninstall
# Or you can manually remove the hermes directory
# rm -rf~/.hermes/
```
