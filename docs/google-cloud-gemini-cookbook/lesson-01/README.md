![img.png](img.png)
# Cookbook Lesson 01: 🚀 Build a `Hello World` app with Gemini, Streamlit & Google Cloud Run

Welcome to the **Google Cloud Gemini Cookbook**! In this very first lesson,
we're going to embark on an exciting journey: taking your Python code from a
simple idea to a live web application in minutes. Forget complex setups; with
Streamlit and Google Cloud Run, deploying your first web app is incredibly fast
and fun! ✨

> This lesson is part of the
[Google Cloud - Gemini Cookbook (GitHub Link)](https://github.com/msampathkumar/msampathkumar.github.io/tree/master/docs/google-cloud-gemini-cookbook/).

______________________________________________________________________

## What You'll Learn 🎓

This lesson focuses on the essentials of getting a web application up and
running quickly:

1. **Build a "Hello World" with Streamlit:** Discover how effortlessly you can
   create interactive web apps using just Python. Streamlit handles all the
   front-end magic for you! 🐍
1. **Deploy to Google Cloud Run:** Learn to take your Streamlit app and deploy
   it as a scalable, serverless container on Google Cloud Run. This means your
   app can handle traffic effortlessly, and you only pay for what you use! ☁️💸

By the end of this lesson, you'll have a fully functional web application
accessible via a URL, demonstrating the incredible speed of modern cloud
development. 🚀

______________________________________________________________________

## Prerequisites 🛠️

Before we begin, ensure you have the following:

- A Google Cloud Project with billing enabled.
- The `gcloud` CLI installed and configured.
- Python 3.8+ installed on your local machine.
- `pip` (Python package installer).

For development, we recommend using the Google Cloud Shell, which comes
pre-installed with the necessary tools.

## What is Streamlit?

[Streamlit](https://streamlit.io/) is an open-source Python framework that
makes it easy to create and share beautiful, custom web apps for machine
learning and data science. In just a few lines of code, you can build and
deploy powerful data apps.

While Streamlit is not as feature-rich as full-fledged web frameworks like
Django or Flask, its strength lies in its simplicity and ability to create
highly interactive applications quickly. This makes it an excellent choice for
building demos and prototypes.

## What is Google Cloud Run?

[Cloud Run](https://cloud.google.com/run) is a fully managed serverless
platform that enables you to run stateless containers that are invocable via
web requests or Pub/Sub events. You can deploy your code to Cloud Run, and it
will automatically scale up or down based on traffic.

Here are some of the benefits of using Cloud Run:

- **Easy to use:** Deploy your application with a single command.
- **Serverless:** No infrastructure to manage.
- **Scalable:** Automatically scales to meet demand.
- **Cost-effective:** Pay only for the resources you use.

## 💻 Local Development: Your Streamlit "Hello World"

Let's start by creating a simple Streamlit application locally. Here's how you
can do it:

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

You should see your Streamlit app open in your browser and navigating to
`http://localhost:8080`. Interact with it! This is your app running locally. 🚀

### 4. Deploy to Cloud Run

To deploy your app to Cloud Run, you'll need to create a `Procfile` and a
`deploy.sh` script.

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

**Important:** Replace `"your-gcp-project-id"` with your actual Google Cloud
Project ID.

Now, run the deployment script:

```bash
bash deploy.sh
```

This command will build a container image from your source code, push it to the
container registry, and deploy it to Cloud Run. Once the deployment is
complete, you'll see a service URL in the output.

Congratulations 🎉! You have successfully deployed your Streamlit app to Cloud
Run.

## Cleanup

To avoid incurring future charges, delete the resources you created:

- Go to the [Cloud Run console](https://console.cloud.google.com/run) and
  delete your application.
- Go to the [Container Registry](https://console.cloud.google.com/gcr) and
  delete the container image.

## Learn More

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Authenticating to Cloud Run](https://cloud.google.com/run/docs/authenticating/overview)
