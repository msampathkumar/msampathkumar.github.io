import streamlit as st

import logging

import settings
import llm

from cache import CacheManager
from rag import RagCorpusManager

import os.path
import sys

# add local path to sys.path
local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(local_path)

# --- Page Configuration ---
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

# --- Session State Initialization ---
# We use session_state to store data that persists across user interactions (reruns).
# Here, we initialize a dictionary for chat sessions and set the default active session.
if "sessions" not in st.session_state:
    # Start with a default session
    st.session_state.sessions = {"Chat 1": []}

if "active_session" not in st.session_state:
    # Set the first session as active by default
    st.session_state.active_session = "Chat 1"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- Helper Functions ---
def add_new_session():
    """Adds a new chat session."""
    # TODO: Implement the logic for adding a new session
    session_count = len(st.session_state.sessions) + 1
    new_session_name = f"Chat {session_count}"
    st.session_state.sessions[new_session_name] = []
    st.session_state.active_session = new_session_name


def switch_session(session_name):
    """Switches the active chat session."""
    # TODO: Implement the logic for switching a session
    st.session_state.active_session = session_name


# --- UI Rendering ---

# --- Column 1: Session List (Collapsible Sidebar) ---
# The sidebar is a natural fit for a collapsible list of chat sessions.
with st.sidebar:
    st.title("Chat History")
    st.button("➕ New Chat", on_click=add_new_session, use_container_width=True)

    st.write("---")

    # Display a button for each session. The active session is highlighted.
    for session in st.session_state.sessions.keys():
        button_type = (
            "primary" if session == st.session_state.active_session else "secondary"
        )
        if st.button(
            session,
            key=f"session_btn_{session}",
            use_container_width=True,
            type=button_type,
        ):
            switch_session(session)


st.title(settings.HEADER)
st.markdown(settings.DESCRIPTION)

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
