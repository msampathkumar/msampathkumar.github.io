# Building Agentic AI: How to Provision a Google Cloud VM for Gemini & Model Garden

Building Agentic applications requires more than just code; it requires a secure, high-performance environment that can seamlessly talk to Large Language Models (LLMs) like [Gemini](https://cloud.google.com/vertex-ai) and [Claude](https://cloud.google.com/vertex-ai).

In this post, we’ll walk through how to create a Google Compute Engine VM specifically configured for AI development, focusing on the critical identity and permission steps often missed.

## Pre-requisites

1. You need to have a Google Cloud project
2. You need to run all the following commands from Google Cloud Project's Web Cloud Shell (https://shell.cloud.google.com/)
3. You can use you personal mac or linux, to run ssh commands provided

## Step 1: Enable the AI Infrastructure APIs

> **Note:** Run these commands from Google Cloud Project - Cloud Shell.

Before creating resources, you must tell Google Cloud to turn on the necessary “brains” for your project. We need the Vertex AI API (for Gemini/Model Garden) and the Discovery Engine API (for agentic search).

```bash
# Enable Vertex AI and Discovery Engine (Vertex AI Search & Conversation)
gcloud services enable \
  aiplatform.googleapis.com \
  discoveryengine.googleapis.com \
  compute.googleapis.com

```

## Step 2: Create a Dedicated Service Account

> **Note:** Run these commands from Google Cloud Project - Cloud Shell.

Never use the default “Compute Engine default service account” for AI apps. Instead, create a dedicated identity following the principle of least privilege.

```bash
# Create the service account
gcloud iam service-accounts create ai-agent-sa \
  --display-name="AI Agent Service Account"

# Store the email in a variable for easy use
SA_EMAIL="ai-agent-sa@$(gcloud config get-value project).iam.gserviceaccount.com"
```

## Step 3: Grant IAM Permissions

> **Note:** Run these commands from Google Cloud Project - Cloud Shell.

To build an “agentic” app, your VM needs to find models, call them, and potentially deploy them.

```bash
# 1. Access Gemini and Model Garden
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"

# 2. Access Vertex AI Search (Discovery Engine) for RAG capabilities
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/discoveryengine.viewer"

# 3. Allow the SA to use itself (required for deploying models like Claude)
gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser"

```

## Step 4: Create the VM with Correct Scopes

> **Note:** Run these commands from my personal pc.

To make it easy to reuse, I am defining the variables in the following manner.

```bash
GCP_PROJECT_ID=gemini-demo-project-4242
GCP_PROJECT_ZONE=us-central1-a
VM_NAME=ai-development-vm
```

This is the most critical step. Even with IAM roles, a VM cannot call APIs unless its Access Scopes are set to `cloud-platform`.

```bash
gcloud compute instances create $VM_NAME \
  --project=$GCP_PROJECT_ID \
  --zone=$GCP_PROJECT_ZONE \
  --machine-type=e2-standard-4 \
  --service-account=$SA_EMAIL \
  --scopes=[https://www.googleapis.com/auth/cloud-platform](https://www.googleapis.com/auth/cloud-platform) \
  --image-family=debian-11 \
  --image-project=debian-cloud

```

## Step 5: How login to VM ?

> **Note:** Run these commands from my personal pc.

To login to the above created VM, use the following command:

```bash
gcloud compute ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME"
```

### (Optiona) Other helpful command

> **Note:** Run these commands from my personal pc.

To check VM instance in your project

```bash
gcloud compute instances list --project $GCP_PROJECT_ID
```

To simplify the login command, you can use the following command to update the SSH config:

```bash
gcloud compute config-ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME"
```

To open port-forwarding using cloud-shell, use `-L <local-port>:<local-host>:<remote-port>` option. You can use multiple `-L` options to forward multiple ports.

```bash
gcloud compute ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME" -- -L 8888:127.0.0.1:8888 -L 9595:127.0.0.1:9595
```

### (Optional) Install necessary developer utilities

> **Note:** Run these commands from my new VM.

As a developer, you would neeed utilities to work in a VM. For example, git, vim, python and etc.

```bash
sudo apt update
sudo apt upgrade
sudo apt-get install -y git vim gedit tree
```

```bash
echo "# Set default editor" >> ~/.bashrc
echo "export VISUAL=vim" >> ~/.bashrc
echo "export EDITOR=\$VISUAL" >> ~/.bashrc
source ~/.bashrc
```

```bash
sudo apt install -y python3-pip

# Verify python and pip are installed
python3 --version
pip3 --version
```

## Conclusion

In this post, you learned how to setup a VM in Google Cloud Platform for agentic AI experiments using Gemini and Model Garden. You can now use this VM to run your agentic AI experiments.
