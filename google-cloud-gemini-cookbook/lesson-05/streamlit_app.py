import streamlit as st

import logging

import config
import llm

from cache import CacheManager
from rag import RagCorpusManager

import os.path
import sys
from PIL import Image

# add local path to sys.path
local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(local_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set page configuration
# https://fonts.google.com/icons?selected=Material+Symbols+Outlined:editor_choice:FILL@0;wght@400;GRAD@0;opsz@24&icon.size=24&icon.color=%231f1f1f&icon.query=winner
st.set_page_config(
    layout="wide",
    page_icon="""<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#1f1f1f"><path d="M240-40v-329L110-580l185-300h370l185 300-130 211v329l-240-80-240 80Zm80-111 160-53 160 53v-129H320v129Zm20-649L204-580l136 220h280l136-220-136-220H340Zm98 383L296-558l57-57 85 85 169-170 57 56-226 227ZM320-280h320-320Z"/></svg>""",
    page_title="Gemini Chatbot",
    initial_sidebar_state="collapsed",
)
# Hide deploy options
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(config.HEADER)
st.markdown(config.DESCRIPTION)

# Let the user choose between Context Cache and RAG
option = st.radio(
    "Choose an option:",
    ("Default", "Use Context Cache", "Use RAG as Tool", "Use Grounding"),
    horizontal=True,
)

# Logic to handle the chosen option
use_context_cache = option == "Use Context Cache"
use_rag_corpus = option == "Use RAG as Tool"
use_google_search = option == "Use Grounding"

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
    logging.info(f"cache_name={cache_name}")

rag_corpus_name = None
if use_rag_corpus:
    logging.info(f"use_rag_corpus={use_rag_corpus}")
    rag_corpus_name = RagCorpusManager().main()
    logging.info(f"rag_corpus_name={rag_corpus_name}")


# Initialize chat session in Streamlit's session state.
# This will be run only once, on the first run of the session.
if "chat_session" not in st.session_state:
    logging.info("New chat session initialized.")
    st.session_state.chat_session = llm.get_chat_session(
        cache_name=cache_name,
        rag_corpus_name=rag_corpus_name,
        use_context_cache=use_context_cache,
        use_rag_corpus=use_rag_corpus,
        use_google_search=use_google_search,
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
