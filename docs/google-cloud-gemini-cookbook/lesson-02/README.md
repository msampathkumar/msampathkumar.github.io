# Cookbook Lesson 02: Deploy Your AI Chatbot to Google Cloud Run: Go Live! ☁️

Welcome to the second lesson in our Gemini Cookbook series! This time, we're
diving into the exciting world of conversational AI. You'll learn to build a
smart, interactive chatbot using the power of Streamlit and Google's Gemini 2.5
Flash model. We'll be using the official Google Cloud Vertex AI SDK, which has
powerful features like chat sessions that give your bot a memory.

> This lesson is part of the
[Google Cloud - Gemini Cookbook (GitHub Link)](https://github.com/msampathkumar/msampathkumar.github.io/tree/master/docs/google-cloud-gemini-cookbook/).

## What You'll Create

Get ready to build a sleek, web-based chatbot. With Streamlit as our frontend,
your chatbot will connect to the mighty Gemini 1.5 Flash model, enabling you to
have dynamic and stateful conversations. It's like having your own personal AI
assistant!

![Your Streamlit Chatbot in Action](https://storage.googleapis.com/github-repo/img/lesson-02-streamlit-chatbot.png)

## What You'll Need

To get started, make sure you have the following essentials:

- A Google Cloud project with the Vertex AI API ready to go.
- Python 3.8 or a newer version.
- The `pip` package manager for installing our dependencies.

### Mandatory steps

This is a mandatory steps to access Gemini Models from your Google Cloud
Project.

I have installed the Gcloud tool and used
[Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)
to get the credentials. If you want to run the code in Google Cloud project,
then you need to update respective service-account with the required
permissions. For details, check out this
[user-managed service account](https://cloud.google.com/docs/authentication/set-up-adc-attached-service-account)
article.

## Let's Get Building!

1. **Get the Code:** First, clone the repository and hop into the right
   directory:

   ```bash
   git clone https://github.com/msampathkumar/msampathkumar.github.io.git
   cd msampathkumar.github.io/docs/google-cloud-gemini-cookbook/lesson-02
   ```

1. **Set Up Your Workspace:** Create a virtual environment to keep things tidy:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

1. **Install the Magic:** Time to install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

1. **Connect to Google Cloud:** Authenticate your local environment to use
   Google Cloud services:

```bash
gcloud auth application-default login
```

## A Look Under the Hood

Let's take a peek at the code that makes our chatbot tick.

### The Chatbot UI: `streamlit_app.py`

This file is the heart of our Streamlit app. It's responsible for:

- Providing a chat interface for user input.
- Displaying the response from the model.
- Maintaining the conversation history.

While you would typically use Streamlit's `session_state` to store the
conversation history manually, the Vertex AI SDK simplifies this. We'll use a
`ChatSession` object from the SDK, which automatically handles the history for
us. We just need to store this one object in `st.session_state` to make our
chat stateful.

You can see the core logic below:

```python
import streamlit as st
import llm

# Initialize chat session in Streamlit's session state.
# This will be run only once, on the first run of the session.
if "chat_session" not in st.session_state:
    st.session_state.chat_session = llm.start_chat()

# Display chat history from the session state
for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)
```

### The Brains of the Operation: `llm.py`

This file handles all the communication with the Gemini 2.5 Flash model. As we
are using GenAI SDK, we can use environment variables to set up the required
details for authentication. Also, GenAI SDK provides us with `Client` class
which we can use to create a chat session and send messages to the Gemini Model
and receive.

```python
from google import genai

# Using environment variables to pass essential parameters to the client.
client = genai.Client()

# Create chat session
chat_session = client.chats.create("gemini-2.0-flash-lite-001")
```

#### To run chatbot in CLI

```bash
python llm.py
```

#### To run streamlit chatbot

```bash
streamlit run streamlit_app.py
```

## Deploy the application

You can deploy your chatbot to Google Cloud Run and share it with the world.

Use the `deploy.sh` script to package your app into a Docker image and send it
to the Google Artifact Registry.

```bash
./deploy.sh
```

The script will then deploy your app to Cloud Run, making it live on the web.

## You Did It!

High five! You've built and deployed a fully functional chatbot with Streamlit
and Gemini Pro. You've seen how to use the new Generative AI SDK and its chat
features to create a more natural and engaging conversational experience. Now,
go ahead and have a chat with your new AI friend!
