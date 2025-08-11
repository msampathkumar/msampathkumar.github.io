## Welcome to Cookbook series Lesson 05.

From Lesson 01 to Lesson 04, we have covered several key items from how to build a hello world to how to build really cool context aware smart chatbots. In this lesson 05, we are going to do a quick recap of lesson 01 to 04 and of course finally we will go over some important tips to make really good features of Gemini that are applicable for most people.


### Takeaway 01: Multi Layered Application

Let me quote from a Google Developer Advocate.

“To effectively monitor your agent, it’s best to adopt a practical, layered approach. Here’s a guide to setting up observability at every stage of the development lifecycle.” — Alvin Prayuda Juniarta Dwiyantoro

https://medium.com/google-cloud/prepping-your-agent-for-production-observability-for-agent-development-kit-adk-a6d74c744ef2 

Building an application and features can become a cascading challenge when you want to build an app that can be used, maintained, updated and deployed to production environments.  As mentioned in the above quote, building applications in a layered approach can help you to minimize the overall flow. The application we have built have a similar approach.


#### Flow chart



*   LLM.py - LLM Interface
    *   Create and provides a Chat Session with Gemini Models
        *   Uses rag.py and cache.py as user instructions
    *   (optional) Can run in CLI with a simple Chat Session
*   Streamlit_app.py - User Interface
    *   UI for User Chat session
    *   UI for User controls (to select RAG, Context Cache, Google Search)
*   (Optional - User Plugin) Cache.py  - Context Cache Manager
    *   Use .cache file to record detailed cache created. 
    *   Uses config.py to identify required files  that need to be cached
    *   Automatically cache management of Cache.
        *   Default cache time is set to 60 mins. After 60 mins, cache is deleted.
*   (Optional - User Plugin)  RAG.py - RAG Engine
    *   Uses `.rag` file to record detailed of created cache
    *   Uses `rag_dataset` folder RAG content
    *   Automatic RAG management
        *   As per changes to the rag_dataset folder, RAG content is updated.
*   cleanup.py - CleanUP
    *   To cleanup any RAG related content
    *   To (forcefully) any Cache content before its expiry time.
    *   To clean local files (.rag and .cache) \


Building the app in layers helped me to build and scale the app, while ensuring that over-debugging requirements to a minimum.


### Takeaway 02: Improve your speed

LLMs are huge software apps that consume up a lot of CPU, memory, and network resources. For example, `gemma3:27b` alone needed over 15 GB of disk space! Just like services such as BigQuery or Cloud SQL, these models are hosted globally, serving folks all over the world.


#### Global Endpoints:

This section has some speculations & experiments on my part.

It's pretty common to think that using the closest LLM location is the best bet. While being nearby helps with network speed, that's not the whole story. LLMs are shared services, meaning they naturally have a queue (first-in, first-out). So, the best way to pick a location boils down to the "min_response(Nearby locations + shorter queue)" equation. Throw in extra factors like time and potential datacenter hiccups (think maintenance, power outages, or even underwater cable issues), and the ideal solution becomes "min_response(Nearby _available_ locations + shorter queue)." 

But here's the catch: predicting all these conditions is tough. Constantly pinging every Gemini model globally to check response times could actually slow things down more than it helps. That's where Global Endpoints really shine! They automatically figure out which LLM model will give you the fastest response, speeding up your interactions.

Just a couple of things to keep in mind when using Gemini Endpoints:



1. **Data Localization:** If your app needs to keep data in a specific place (like for GDPR), Global Endpoints might not be the right choice.
2. **Feature Limitation:** For systems like RAG (Vector Search) built in certain regions (say, Europe or US-Central), you might be stuck using Gemini models only available in those spots.

Back in March 2024, I whipped up a demo app that hit a global endpoint instead of a specific regional one, like `us-central1` or `europe-central2`. Since I was working from my place in Warsaw, Poland, with an old router, I figured there might be some lag. But honestly, the huge performance difference between the global endpoint and my go-to `europe-west1` was pretty wild – in a good way!


![alt_text](images/image1.png "image_tooltip")



#### Using Gemini-Lite Models

When Gemini Live API was announced for the first time, I was pretty excited. In my case, one exciting part was sockets. (I think WebSockets are just too amazing when you compare them with standard HTTPS requests. They are just fast.). After the announcement and exploring a couple of times, I found that my best choice of option was a simple text based chat, compared to audio conversation or video conferencing with Gemini.

While the Live Api provide a nice transcribe options (`https://cloud.google.com/vertex-ai/generative-ai/docs/live-api#transcribe_audio`

) for both input and output, I felt it was effective to text cases chat as it allows me to review what my query is before sending it to Gemini.

Given the above 2 reasons, I started switching to the gemini-flash-lite model whenever I needed a very simple chatbot.


### Takeaway 03: Cost Saving


#### Use Context Caching

If you are using Gemini and observability to track your token usage then you may have a good surprise waiting for you. It is Gemini’s Implicit Context Caching (ICC) and Explicit Context Caching (ECC) features. By default Implicit Context Caching feature is enabled for you but you can disable it if needed.

If you know about caching, you may already know that it is always about cache-hit vs cache-miss ratio that determines the best cache. In ICC, it is not guaranteed that you will save money. Imagine this. For instance, if I were to answer 100-200 questions and all of them are completely different from each other and in different languages, then it is not possible to save a common token as token cache. In such cases, Gemini can’t save money for you.

Unlike ICC, ECC has a cost saving guarantee. Personally I found that ECC is amazing but it is a design choice. https://ai.google.dev/gemini-api/docs/caching?lang=python#explicit-caching Like escape velocity, you need to hit a certain threshold that is cost-effective. It's purely mathematical. No magic!


#### Provision Throughput (PT)

This is Vertex AI only feature.

Provisioned Throughput is a fixed-cost, fixed-term subscription available in several term-lengths that reserves throughput for supported generative AI models on Vertex AI. To reserve your throughput, you must specify the model and available locations in which the model runs.

A big note here is that, if you go over your PT limit then your requests won’t stop. This is big win if you dont enjoy error but on the downside, you can’t limit your Gemini Costs if you have budget limits.


### Takeaway 04: Context Awareness

Whether it's Gemini or some other LLMs, it's always the same rule. People are calling  `context is the king` but when I was learning data science, I heard a similar quote about `Data / Information`.

Let me take a personal example here. Back in 2015, my colleagues had a simple classification challenge but the difficult part was the data distributions.  Client has provided 1 TB of data positive data and 10 MB of negative data. (1,000,000 MB of positive data set and 10 MB is -tive dataset). 

When I say context, it is the data relevancy. If your queries are not relevant to the context or theme you have set for the model, then you may be doing some fundamentally wrong. Imagine studying poetry to improve painting.

So to keep your model responses relative to what users need, with gemini I have tested the following approaches



1. Use System Instructions: Define all the critical details that your model needs to remember. For example, “You are Bill Nye, the science guy. You are an American science communicator, television presenter, and former mechanical engineer. You are  best known as the host of the science education television show Bill Nye the Science Guy and as a science educator in pop culture.” (Copied from wikipedia) \

2. Use Grounding with Google Search: To the scope limited, many times LLM models are not connected to search engines like Google (or DuckDuckGo or Yahoo). By enabling this, you can allow Gemini Model to browse the internet and get the latest information like date, climate and so. \

3. Use RAG: Similar to Grounding with Google Search, you may find your in a case where you want the model to automatically learn information about a certain project or certain dataset that is private to you or your team or organization. In such cases, using RAG has turned out to be an amazing investment. \
 \
Using Vertex AI’s RAG feature, all the provided data is converted into vectors and stored in a Vector database. When user queries, relevant data is identified from this Vecotor database and included as part of the overall context for the Model. As you may expect now this allows the model to get relevant answers.


### Takeaway 05:  Simplicity

Actually this is not a take away. It's the reality check or a reminder if you already know.

Keep it simple!

At the end of the day, it is always about simplicity. 

For example: If you have 1 bug in 10 lines of code, then your probability of randomly finding it on first attachment if 10% but if your code has 500 lines then it 0.2%

Simple designs are easier to understand, build, iterate and to maintain. As mentioned above in Takesaway 01, if possible try a layer approach but keep in mind to have simplicity in mind. 
