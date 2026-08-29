# Building Agentic AI: How to Provision a Google Cloud VM for Gemini & Model Garden

Building Agentic applications requires more than just code; it requires a secure, high-performance environment that can seamlessly talk to Large Language Models (LLMs) like [Gemini](https://cloud.google.com/vertex-ai) and [Claude](https://cloud.google.com/vertex-ai).

In this post, we’ll walk through how to create a Google Compute Engine VM specifically configured for AI development, focusing on the critical identity and permission steps often missed.

## Prerequisites

1. A Google Cloud project with billing enabled.
2. Access to Google Cloud Shell (https://shell.cloud.google.com/) or the Google Cloud CLI installed locally.
3. A local computer (Mac, Linux, or Windows) to run SSH commands.

## Step 1: Enable the AI Infrastructure APIs

> **Note:** Run these commands from Google Cloud Shell.

Before creating resources, enable the required Google Cloud APIs for Vertex AI (for Gemini and Model Garden), Discovery Engine (for agentic search), and Compute Engine.

```bash
# Enable Vertex AI and Discovery Engine (Vertex AI Search & Conversation)
gcloud services enable \
  aiplatform.googleapis.com \
  discoveryengine.googleapis.com \
  compute.googleapis.com
```

## Step 2: Create a Dedicated Service Account

> **Note:** Run these commands from Google Cloud Shell.

Avoid using the default Compute Engine service account for AI applications. Instead, create a dedicated identity following the principle of least privilege:

```bash
# Create the service account
gcloud iam service-accounts create ai-agent-sa \
  --display-name="AI Agent Service Account"

# Store the email in a variable for easy use
SA_EMAIL="ai-agent-sa@$(gcloud config get-value project).iam.gserviceaccount.com"
```

## Step 3: Grant IAM Permissions

> **Note:** Run these commands from Google Cloud Shell.

Grant the dedicated service account the necessary permissions to access models and search capabilities:

```bash
# 1. Access Gemini and Model Garden
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"

# 2. Access Vertex AI Search (Discovery Engine) for RAG capabilities
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/discoveryengine.viewer"

# 3. Allow the service account to use itself (required for deploying certain models)
gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser"
```

## Step 4: Create the VM with Correct Scopes

> **Note:** Run these commands from your local computer or Cloud Shell.

Define the environment variables below for easy reuse:

```bash
GCP_PROJECT_ID=YOUR_GOOGLE_CLOUD_PROJECT_ID_HERE
GCP_PROJECT_ZONE=us-central1-a
VM_NAME=ai-development-vm
```

This is the most critical step: even with IAM roles, a VM cannot invoke GCP APIs unless its access scopes include `cloud-platform`.

```bash
gcloud compute instances create $VM_NAME \
  --project=$GCP_PROJECT_ID \
  --zone=$GCP_PROJECT_ZONE \
  --machine-type=e2-standard-4 \
  --service-account=$SA_EMAIL \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

## Step 5: Log In to the VM

> **Note:** Run these commands from your local computer.

To log in to the newly created VM:

```bash
gcloud compute ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME"
```

### (Optional) Other Helpful Commands

> **Note:** Run these commands from your local computer.

To list VM instances in your project:

```bash
gcloud compute instances list --project $GCP_PROJECT_ID
```

To configure SSH aliases for simpler login:

```bash
gcloud compute config-ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME"
```

To forward ports from the VM to your local computer, use the `-L <local-port>:<local-host>:<remote-port>` option (you can pass multiple `-L` flags simultaneously):

```bash
gcloud compute ssh --project $GCP_PROJECT_ID --zone $GCP_PROJECT_ZONE "$VM_NAME" -- -L 8888:127.0.0.1:8888 -L 9595:127.0.0.1:9595
```

### (Optional) Install Developer Utilities

> **Note:** Run these commands inside the VM.

Install common development utilities (such as Git, Vim, and Python):

```bash
sudo apt update
sudo apt upgrade -y
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

In this guide, you learned how to provision and configure a Google Cloud VM for agentic AI experiments using Gemini and Model Garden. You can now use this VM as a reliable environment to develop and test agentic workflows.
