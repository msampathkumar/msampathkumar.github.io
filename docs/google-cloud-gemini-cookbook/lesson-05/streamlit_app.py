import streamlit as st
import logging
import settings
import llm
from cache import CacheManager
from rag import RagCorpusManager
import os
import sys
from chat_setting import ChatSettings

# Add local path to sys.path
local_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(local_path)

# --- Page Configuration ---
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

# --- Session State Initialization ---
if 'sessions' not in st.session_state:
    st.session_state.sessions = {
        "Chat 1": {
            "history": [],
            "chat_session": None,
            "chat_settings": ChatSettings(chat_session_name="Chat 1")
        }
    }
if 'active_session' not in st.session_state:
    st.session_state.active_session = "Chat 1"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Helper Functions ---
def get_active_session_state():
    return st.session_state.sessions[st.session_state.active_session]

def add_new_session():
    session_count = len(st.session_state.sessions) + 1
    new_session_name = f"Chat {session_count}"
    st.session_state.sessions[new_session_name] = {
        "history": [], 
        "chat_session": None,
        "chat_settings": ChatSettings(chat_session_name=new_session_name)
        }
    st.session_state.active_session = new_session_name

def switch_session(session_name):
    st.session_state.active_session = session_name

def clear_chat_session():
    st.session_state.sessions[st.session_state.active_session]["history"] = []
    st.session_state.sessions[st.session_state.active_session]["chat_session"] = None

def delete_session():
    session_to_delete = st.session_state.active_session
    session_keys = list(st.session_state.sessions.keys())
    current_index = session_keys.index(session_to_delete)
    del st.session_state.sessions[session_to_delete]
    if not st.session_state.sessions:
        add_new_session()
    else:
        new_index = current_index - 1 if current_index > 0 else 0
        st.session_state.active_session = session_keys[new_index]

def get_chat_session(session_state):
    return llm.get_chat_session(
        chat_settings=session_state["chat_settings"],
        cache_name=session_state.get("cache_name"),
        rag_corpus_name=session_state.get("rag_corpus_name"),
        use_context_cache=session_state.get("use_context_cache", False),
        use_rag_corpus=session_state.get("use_rag_corpus", False),
        use_google_search=session_state.get("use_google_search", False),
    )


# --- UI Rendering ---
with st.sidebar:
    st.title("Chat History")
    st.button("➕ New Chat", on_click=add_new_session, use_container_width=True)
    st.write("---")
    for session in st.session_state.sessions.keys():
        button_type = "primary" if session == st.session_state.active_session else "secondary"
        if st.button(session, key=f"session_btn_{session}", use_container_width=True, type=button_type):
            switch_session(session)

chat_col, config_col = st.tabs(["Chat", "Config"])

with chat_col:
    st.header(f"Active Session: {st.session_state.active_session}")
    if st.button("🧽 Clear Chat"):
        clear_chat_session()
    if st.button("🗑 Delete Chat"):
        delete_session()

    active_session_state = get_active_session_state()
    if active_session_state["chat_session"] is None:
        active_session_state["chat_session"] = get_chat_session(active_session_state)

    # Display chat messages from history
    for message in active_session_state["history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to history
        active_session_state["history"].append({"role": "user", "content": prompt})
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        if active_session_state["chat_session"]:
            with st.chat_message("assistant"):
                try:
                    with st.spinner("Assistant is thinking..."):
                        response = active_session_state["chat_session"].send_message(prompt)
                        st.markdown(response.text)
                    # Add assistant response to history
                    active_session_state["history"].append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

with config_col:
    with st.expander("⚙️ Configuration", expanded=True):
        active_session_state = get_active_session_state()

        option = st.radio("Choose an option:", 
                        ("Default", "Use Context Cache", "Use RAG as Tool", "Use Grounding"), 
                        horizontal=True, 
                        key=f"option_{st.session_state.active_session}")

        active_session_state["use_context_cache"] = option == "Use Context Cache"
        active_session_state["use_rag_corpus"] = option == "Use RAG as Tool"
        active_session_state["use_google_search"] = option == "Use Grounding"

        if active_session_state["use_context_cache"]:
            active_session_state["cache_name"] = CacheManager().main()
        if active_session_state["use_rag_corpus"]:
            active_session_state["rag_corpus_name"] = RagCorpusManager().main()

        # When config changes, re-initialize the chat session
        st.session_state.sessions[st.session_state.active_session]["chat_session"] = get_chat_session(active_session_state)
