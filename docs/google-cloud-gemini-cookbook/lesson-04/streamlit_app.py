import streamlit as st

import logging

import config
import llm

from cache import CacheManager
from rag import RagCorpusManager

import os.path
import sys

# add local path to sys.path
local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(local_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

st.title(config.HEADER)
st.markdown(config.DESCRIPTION)

# Let the user choose between Context Cache and RAG
option = st.radio(
    "Choose an option:",
    ("Use System Instructions only", "Use Context Cache", "Use RAG as Tool"),
    horizontal=True,
)

# Logic to handle the chosen option
use_context_cache = option == "Use Context Cache"
use_rag_corpus = option == "Use RAG as Tool"

# Reset chat session if the option has changed
if "last_option" not in st.session_state:
    st.session_state.last_option = option

if st.session_state.last_option != option:
    st.info("Option changed. Resetting chat session.")
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
    st.session_state.last_option = option

cache_name = None
if use_context_cache:
    logging.info(f"use_context_cache={use_context_cache}")
    cache_name = CacheManager().main()

rag_corpus_name = None
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
