import google.generativeai as genai
import os

# Configure API key once from environment variable
# Make sure to set your GOOGLE_API_KEY environment variable
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def generate_text_from_gemini(
    prompt_parts, model_name="gemini-1.5-flash-latest", system_instruction=None
):
    """
    Generates text from Gemini model for one-shot/few-shot scenarios.
    """
    model = genai.GenerativeModel(
        model_name=model_name, system_instruction=system_instruction
    )
    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"ERROR: {e}"


def start_gemini_chat_session(
    model_name="gemini-1.5-flash-latest", system_instruction=None, history=None
):
    """
    Starts and returns a Gemini chat session with optional system instruction and history.
    """
    model = genai.GenerativeModel(
        model_name=model_name, system_instruction=system_instruction
    )
    return model.start_chat(history=history if history else [])


# Simulated RAG retriever for Lesson 04
def retrieve_relevant_docs_simulated(query, docs, top_k=2):
    """
    Simulates retrieving relevant documents from a knowledge base based on keywords.
    In a real RAG system, this would be an advanced search query to Google Cloud Search,
    potentially using embeddings for semantic search.
    """
    relevant_docs = []
    query_lower = query.lower()
    for doc in docs:
        if query_lower in doc["content"].lower() or query_lower in doc["title"].lower():
            relevant_docs.append(doc)
    # Simple sort by length to prioritize shorter, possibly more direct matches
    relevant_docs.sort(key=lambda x: len(x["content"]))
    return relevant_docs[:top_k]


# Function for generating grounded response (RAG)
def get_grounded_response_from_gemini(
    user_query, retrieved_context, model_name="gemini-1.5-flash-latest"
):
    """
    Generates a grounded response using Gemini, based on provided retrieved context.
    """
    if not retrieved_context:
        return "I'm sorry, I couldn't find relevant information in our internal documents to answer that. Please try rephrasing or ask about a different topic. 🧐"

    augmented_prompt = (
        "You are an internal company assistant. Answer the user's question ONLY based on the "
        "following internal knowledge provided. If the information needed is not present in the "
        "provided knowledge, state that you cannot answer the question based on the given context. "
        "Always cite the 'Source:' document title at the end of your answer if information is used.\n\n"
        "Internal Knowledge:\n"
    )
    for doc in retrieved_context:
        augmented_prompt += f"--- {doc['title']} ---\n{doc['content']}\n\n"

    augmented_prompt += f"User's Question: {user_query}"

    model = genai.GenerativeModel(model_name=model_name)
    try:
        response = model.generate_content(augmented_prompt)
        return response.text
    except Exception as e:
        return f"ERROR generating response: {e}"
