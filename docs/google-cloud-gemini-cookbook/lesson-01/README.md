# Lesson 01: Deploying a Streamlit App to Google Cloud Run

In this lesson, you'll learn how to deploy a Streamlit web app to Google Cloud Run with ease.

## What you'll learn

*   What Streamlit is and why you should use it.
*   How to build a simple Streamlit application.
*   What Cloud Run is and why it's a great choice for deploying serverless applications.
*   How to deploy a Streamlit application directly to Cloud Run from your source code.

## Prerequisites

*   A Google Cloud Project with billing enabled.
*   The `gcloud` CLI installed and configured.
*   Python 3.8 or later.

For development, we recommend using the Google Cloud Shell, which comes pre-installed with the necessary tools.

## What is Streamlit?

[Streamlit](https://streamlit.io/) is an open-source Python framework that makes it easy to create and share beautiful, custom web apps for machine learning and data science. In just a few lines of code, you can build and deploy powerful data apps.

While Streamlit is not as feature-rich as full-fledged web frameworks like Django or Flask, its strength lies in its simplicity and ability to create highly interactive applications quickly. This makes it an excellent choice for building demos and prototypes.

## What is Google Cloud Run?

[Cloud Run](https://cloud.google.com/run) is a fully managed serverless platform that enables you to run stateless containers that are invocable via web requests or Pub/Sub events. You can deploy your code to Cloud Run, and it will automatically scale up or down based on traffic.

Here are some of the benefits of using Cloud Run:

*   **Easy to use:** Deploy your application with a single command.
*   **Serverless:** No infrastructure to manage.
*   **Scalable:** Automatically scales to meet demand.
*   **Cost-effective:** Pay only for the resources you use.

## Let's get started!

### 1. Set up your environment

Create a virtual environment and install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a simple Streamlit app

Create a file named `streamlit_app.py` with the following content:

```python
import streamlit as st

st.title("Sample AI App")

st.text("This is a sample app.")
```

### 3. Run the app locally

To run the app locally, use the following command:

```bash
streamlit run streamlit_app.py --server.port 8080
```

You can now view your app by opening your browser and navigating to `http://localhost:8080`.

### 4. Deploy to Cloud Run

To deploy your app to Cloud Run, you'll need to create a `Procfile` and a `deploy.sh` script.

**Procfile**

Create a file named `Procfile` with the following content:

```
web: streamlit run streamlit_app.py --server.port=8080 --server.address=0.0.0.0 --server.enableCORS=false --browser.gatherUsageStats=false
```

This file tells Cloud Run how to start your application.

**deploy.sh**

Create a file named `deploy.sh` with the following content:

```bash
#!/bin/bash
# Purpose: To deploy the App to Cloud Run.

# Google Cloud Project ID
PROJECT="your-gcp-project-id"

# Google Cloud Region
LOCATION="us-central1"

# Deploy app from source code
gcloud run deploy simple-app --source . --region=$LOCATION --project=$PROJECT --allow-unauthenticated
```

**Important:** Replace `"your-gcp-project-id"` with your actual Google Cloud Project ID.

Now, run the deployment script:

```bash
bash deploy.sh
```

This command will build a container image from your source code, push it to the container registry, and deploy it to Cloud Run. Once the deployment is complete, you'll see a service URL in the output.

Congratulations 🎉! You have successfully deployed your Streamlit app to Cloud Run.

## Cleanup

To avoid incurring future charges, delete the resources you created:

*   Go to the [Cloud Run console](https://console.cloud.google.com/run) and delete your application.
*   Go to the [Container Registry](https://console.cloud.google.com/gcr) and delete the container image.

## Learn More

*   [Cloud Run Documentation](https://cloud.google.com/run/docs)
*   [Streamlit Documentation](https://docs.streamlit.io/)
*   [Authenticating to Cloud Run](https://cloud.google.com/run/docs/authenticating/overview)
