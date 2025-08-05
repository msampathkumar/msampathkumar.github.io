from google import genai
from google.genai.types import (
    HttpOptions,
    GoogleSearch,
    GenerateContentConfig,
    Retrieval,
    Tool,
    VertexRagStore,
    VertexRagStoreRagResource,
)
import logging

import settings


# Gemini AI client
#  - Using environment variables to pass essential parameters to the client.
#  - Read more at https://github.com/googleapis/python-genai/tree/main?tab=readme-ov-file#create-a-client
client = genai.Client(
    project=settings.PROJECT_ID,
    location=settings.LOCATION,
    http_options=HttpOptions(api_version="v1"),
)


# Create chat session
def get_chat_session(
    cache_name=None,
    rag_corpus_name=None,
    use_context_cache=False,
    use_rag_corpus=False,
    use_google_search=False,
):
    system_instruction = settings.SYSTEM_INSTRUCTION
    cached_content = None
    tools = None
    # Grounding with Google Search
    if use_google_search:
        logging.info(f"Using Google Search for Grounding")
        tools = [Tool(google_search=GoogleSearch())]
    # RAG Corpus
    if use_rag_corpus and rag_corpus_name:
        # Create a tool for the RAG Corpus
        rag_retrieval_tool = Tool(
            retrieval=Retrieval(
                vertex_rag_store=VertexRagStore(
                    rag_resources=[
                        VertexRagStoreRagResource(rag_corpus=rag_corpus_name)
                    ]
                )
            )
        )
        tools = [rag_retrieval_tool]
        logging.info(f"Using rag corpus name: {rag_corpus_name}")
    # Context Cache
    if use_context_cache:
        system_instruction = None
        cached_content = cache_name

    # Chat session configuration
    session_config = GenerateContentConfig(
        system_instruction=system_instruction,
        cached_content=cached_content,
        tools=tools,
    )
    print("---" * 15)
    print(
        f"use_context_cache: {use_context_cache} \nuse_rag_corpus: {use_rag_corpus} \nuse_google_search: {use_google_search}"
    )
    print("---" * 15)
    new_chat_session = client.chats.create(
        model=settings.MODEL_NAME, config=session_config
    )
    # Print chat session ID
    print(f"Chat session ID: {new_chat_session}")
    return new_chat_session


if __name__ == "__main__":
    # Initialize chat session
    chat_session = get_chat_session()

    # CLI - Chat Session
    print("Enter your question (or 'exit' to quit")
    while user_input := input("\nUser: "):
        if user_input.lower() == "exit":
            print("Exiting the chat session. Goodbye!")
            break
        # Send a message to LLM
        response = chat_session.send_message(user_input)
        print(f"Model: {response.text}")
else:
    __all__ = ["get_chat_session"]
