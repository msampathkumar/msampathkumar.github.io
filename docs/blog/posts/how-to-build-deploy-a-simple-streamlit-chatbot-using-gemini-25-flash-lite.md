---
title: "How to build & deploy a simple Streamlit chatbot using Gemini 2.5 Flash Lite"
description: "In this blog post, I will show you how to use the Gemini Flash model to build a chatbot using..."
date: 2025-07-09
authors:
  - sampathm
categories:
  - gemini
  - streamlit
  - googlecloud
canonical_url: "https://dev.to/sampathm/how-to-build-deploy-a-simple-streamlit-chatbot-using-gemini-25-flash-lite-14ki"
---

> Originally published on
> [dev.to](https://dev.to/sampathm/how-to-build-deploy-a-simple-streamlit-chatbot-using-gemini-25-flash-lite-14ki)
> /
> [Medium](https://dev.to/sampathm/how-to-build-deploy-a-simple-streamlit-chatbot-using-gemini-25-flash-lite-14ki).

> In this blog post, I will show you how to use the Gemini Flash model to build
> a chatbot using Streamlit. Compared to my previous post in Medium.com, here I
> use the latest version of Streamlit and also the new Google GenAI SDK.

Google has offered Gemini Models services in 2 -3 different ways. For those who
are following regular updates, these are easy to grasp, but for the general
crowd this has become a slight challenge due to the rapid changes and updates
in AI/LLM topics.

Personally, I have felt that AI updates are like unexpected storms 🌪️. So here
is the short version. From a programmer’s lens 🧐, Google offered Gemini Models
access in 3️⃣ ways: (1) Google AI Studio API Keys (2) Google Cloud Project —
Application Default Credentials (ADC) (3) Google Cloud Gemini API keys.

(Off-topic: I have used all these 3️⃣ ways and I find using Google Cloud ADC is
my preferred option. This is because it is easy to use and feels more secure
than others. In production environments, I prefer to use Terraform code to
update my service accounts to have the required credentials.)

The [Google-GenAI SDK](https://pypi.org/project/google-genai) acts as a
standalone SDK for all these 3️⃣ ways of accessing Gemini Models. Also
switching the access methods takes only a 2–3 lines of code. If you like to use
ENVIRONMENT variables, or a .env file then your code becomes more portable. To
learn more about, check https://github.com/googleapis/python-genai/

Now lets start with build Streamlit chatbot with Gemini 2.5. I have already
written the necessary code in Github.

**Download the code** Source:
https://github.com/GoogleCloudPlatform/devrel-demos/tree/main/ai-ml/gemini-chatbot-app/lesson03

```
git clone git@github.com:GoogleCloudPlatform/devrel-demos.git
cd devrel-demos/ai-ml/gemini-chatbot-app/lesson03
```

**Setup**

Create a virtual environment to install dependencies.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you like to use UV, then

```
uv venv
uv add -r requirements.txt
```

**Mandatory steps to access Gemini Models from your Google Cloud Project.** I
have installed the Gcloud tool and used Application Default Credentials to get
the credentials.

If you want to run the code in Google Cloud project, then you need to update
respective service-account with the required permissions. For details, check
out this user-managed service account article.

**Run the code (locally in CLI)** Let’s run the code locally using the python
command. This allows you to have a quick chat with Gemini from CLI and also
allows you to do pre-check for the Streamlit Web application to authenticate
and get the response from the Gemini Model.

```
python llm.py
```

Samples Logs:

```
(venv) sampath:lesson03 sampathm$ python llm.py 
Chat session ID: 4563963584
Enter your question (or 'exit' to quit)
User: Hi there
Model: Hello! 👋 How can I help you today?
User: exit
Exiting the chat session. Goodbye!
(venv) sampath:lesson03 sampathm$
```

Run the Application (locally in Google Chrome)

```
streamlit run streamlit_app.py
```

Samples Logs:

```
(venv) sampath:lesson03 sampathm$ streamlit run streamlit_app.py
 You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.0.0.2:8501
  For better performance, install the Watchdog module:
  $ xcode-select --install
  $ pip install watchdog
            
Chat session ID: 4604152912
2025-07-07 18:54:50,592 - INFO - New chat session initialized.
```

**Deploy the app to Cloud RUN**

```
bash deploy.sh
```

Example Logs

```
(venv) sampath:lesson03 sampathm$ bash deploy.sh 
Building using Buildpacks and deploying container to Cloud Run service [simple-app] in project [...] region [europe-north1]
⠹ Building and deploying... Uploading sources.                                                      
  ⠹ Uploading sources...                                                                            
  . Building Container...                                                                           
✓ Building and deploying... Done.                                                                   
  ✓ Uploading sources...                                                                            
  ✓ Building Container... Logs are available at [https://console.cloud.google.com/cloud-build/builds
  ;region=europe-north1/XXXX-XXX-XXXX-XXXX-XXXX?project=0001110001110].                 
  ✓ Creating Revision...                                                                            .
  ✓ Routing traffic...                                                                              
  ✓ Setting IAM Policy...                                                                           
Done.                                                                                               
Service [simple-app] revision [simple-app-00004-hs7] has been deployed and is serving 100 percent of traffic.
Service URL: https://simple-app-0001110001110.europe-north1.run.app
(venv) sampath:lesson03 sampathm$
(venv) sampath:lesson03 sampathm$
```

Wether you deploy to Cloud Run or run locally, here is a preview of the
application.

**Chatbot Preview**

![Chatbot Preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i6f8uaaz120lcqqyt5gv.webp)

If you have reached this far, then I believe you have successfully deployed
your Chatbot web application on Google Cloud Platform.

Congratulations! 🎉👏🎊

**Conclusion**

In this lesson, we learned how to deploy a simple web application using Google
Cloud Run. We also learned about the different components of a container.

My Medium repost:
https://medium.com/google-cloud/how-to-build-deploy-a-simple-streamlit-chatbot-using-gemini-2-5-flash-lite-8398e4d29819
