import streamlit as st

import llm
import logging

from cache import CacheManager
from rag import RagCorpusManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

st.title(
    "🤖 Chatbot with "
    "[⚡ Gemini-2.5](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-lite)"
    " & "
    "[🜲 Streamlit](https://streamlit.io/)"
)

st.markdown(
    "This is a Streamlit demo chatbot that uses Google's latest [Gemini-2.5 🔦](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-lite). "
    "Read more about it [here](https://deepmind.google/technologies/gemini/flash/)."
)

# Context Caching
cache_name = None

columns = st.columns(2)

with columns[0]:
    # Context Cache
    use_context_cache = st.toggle(
        "Use Context Cache",
        value=st.session_state.get("use_context_cache", False),
        key="use_context_cache",
    )
    if "use_context_cache_changed" not in st.session_state:
        st.session_state.use_context_cache_changed = False

    if use_context_cache != st.session_state.get("use_context_cache_last_value", False):
        st.session_state.use_context_cache_changed = True
        st.session_state.use_context_cache_last_value = use_context_cache


with columns[1]:
    # RAG Corpus
    rag_corpus_name = None
    use_rag_corpus = st.toggle(
        "Use RAG as Tool",
        value=st.session_state.get("use_rag_corpus", False),
        key="use_rag_corpus",
    )
    if "use_rag_corpus_changed" not in st.session_state:
        st.session_state.use_rag_corpus_changed = False

    if use_rag_corpus != st.session_state.get("use_rag_corpus_last_value", False):
        st.session_state.use_rag_corpus_changed = True
        st.session_state.use_rag_corpus_last_value = use_rag_corpus


# Reset chat session if the toggle state has changed
if (
    st.session_state.use_context_cache_changed
    or st.session_state.use_rag_corpus_changed
):
    st.info("Toggle state changed. Resetting chat session.")
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    st.session_state.use_context_cache_changed = False
    st.session_state.use_rag_corpus_changed = False


if use_context_cache:
    logging.info(f"use_context_cache={use_context_cache}")
    cache_name = CacheManager().main()

if use_rag_corpus:
    logging.info(f"use_rag_corpus={use_rag_corpus}")
    rag_corpus_name = RagCorpusManager().main()


# Initialize chat session in Streamlit's session state.
# This will be run only once, on the first run of the session.
if "chat_session" not in st.session_state:
    logging.info("New chat session initialized.")
    st.session_state.chat_session = llm.get_chat_session(
        cache_name=cache_name,
        rag_corpus_name=rag_corpus_name,
        use_context_cache=use_context_cache,
        use_rag_corpus=use_rag_corpus,
    )

# Display chat history from the session state
for message in st.session_state.chat_session.get_history():
    with st.chat_message("assistant" if message.role == "model" else "user"):
        st.markdown(message.parts[0].text)


# Handle user input
if prompt := st.chat_input("What is up?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    logging.info(f"User: {prompt}")

    # Display responses
    with st.chat_message("assistant"):
        # Send message to LLM
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            logging.info(f"Model: {response.text}")
        except Exception as e:
            logging.error(
                f"An error occurred while sending message to LLM: {e}", exc_info=True
            )
            st.error(f"An error occurred: {e}")
