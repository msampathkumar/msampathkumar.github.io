from google import genai
from google.genai.types import (
    HttpOptions,
    GenerateContentConfig,
    Retrieval,
    Tool,
    VertexRagStore,
)
import logging


# Gemini AI model name
MODEL_NAME = "gemini-2.5-flash"

# Gemini AI client
#  - Using environment variables to pass essential parameters to the client.
#  - Read more at https://github.com/googleapis/python-genai/tree/main?tab=readme-ov-file#create-a-client
client = genai.Client(
    http_options=HttpOptions(api_version="v1"),
    location='us-location1'
)


system_instruction = [
    "You're a helpful Gemini AI Chatbot.",
    "Answer user's questions and use simple and clear language."
    "When possible, reply to user's question with a single sentence or a few sentences.",
    "Free to use emojis."
    "Be open and friendly. Don't be afraid to ask questions or clarify things.",
]


# Create chat session
def get_chat_session(
    cache_name=None, rag_corpus_name=None, use_context_cache=False, use_rag_corpus=False
):
    # RAG Corpus
    if use_rag_corpus and rag_corpus_name:
        rag_retrieval_tool = Tool(
            retrieval=Retrieval(
                vertex_rag_store=VertexRagStore(
                    rag_corpora=[rag_corpus_name],
                    # similarity_top_k=10,
                    # vector_distance_threshold=0.5,
                )
            )
        )
        tools = [rag_retrieval_tool]
        logging.info(f"Using rag corpus name: {rag_corpus_name}")
    else:
        tools = None
    # Context Cache
    if use_context_cache:
        config = GenerateContentConfig(
            cached_content=cache_name if use_context_cache else None,
            system_instruction=None if use_context_cache else system_instruction,
            tools=tools,
        )
    else:
        config = GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
        )
    print("---" * 15)
    print(f"use_context_cache: {use_context_cache} \nuse_rag_corpus: {use_rag_corpus}")
    print("---" * 15)
    new_chat_session = client.chats.create(model=MODEL_NAME, config=config)
    # Print chat session ID
    print(f"Chat session ID: {new_chat_session}")
    return new_chat_session


if __name__ == "__main__":
    # Initialize chat session
    chat_session = get_chat_session()

    # CLI - Chat Session
    print("Enter your question (or 'exit' to quit)")
    while user_input := input("\nUser: "):
        if user_input.lower() == "exit":
            print("Exiting the chat session. Goodbye!")
            break
        # Send a message to LLM
        response = chat_session.send_message(user_input)
        print(f"Model: {response.text}")
