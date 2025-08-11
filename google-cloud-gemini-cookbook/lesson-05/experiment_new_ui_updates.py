import streamlit as st
import time

# --- Page Configuration ---
# The `st.set_page_config` command is used to set the title, icon, and layout of the page.
# This should be the first Streamlit command in your script.
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


# --- Helper Functions ---
def add_new_session():
    """Adds a new chat session."""
    session_count = len(st.session_state.sessions) + 1
    new_session_name = f"Chat {session_count}"
    st.session_state.sessions[new_session_name] = []
    st.session_state.active_session = new_session_name
    # st.rerun()


def switch_session(session_name):
    """Switches the active chat session."""
    st.session_state.active_session = session_name
    # st.rerun()


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

# --- Main Area ---
# We split the main area into two columns for the chat and configuration.
# The ratio is set to 2:1, giving the chat area (66%) more space than the config area (33%).
chat_col, config_col = st.tabs(["Chat", "Config"])

# --- Table 1: Chat Configuration ---
with chat_col:
    cols = st.columns([12, 1, 1])
    with cols[0]:
        st.header(f"Active Session: {st.session_state.active_session}")
    with cols[-2]:
        if st.button(
            "🧽󠁝 Clear Chat",
            use_container_width=True,
            help="Clears all messages in the current session.",
        ):
            st.session_state.sessions[st.session_state.active_session] = []
            st.rerun()
    with cols[-1]:
        if st.button(
            "🗑 Delete Chat",
            use_container_width=True,
            help="Clears all messages in the current session.",
        ):
            st.session_state.sessions[st.session_state.active_session] = []
            st.rerun()

    # Display existing chat messages for the active session
    for message in st.session_state.sessions[st.session_state.active_session]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # The chat input widget is placed at the bottom.
    if prompt := st.chat_input("What is up?"):
        # Add user message to the active session's state and display it
        st.session_state.sessions[st.session_state.active_session].append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simulate and display a bot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate a streaming response for a better user experience
            assistant_response = f"Echo: {prompt}"
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # Add the bot's response to the session state
        st.session_state.sessions[st.session_state.active_session].append(
            {"role": "assistant", "content": full_response}
        )

# --- Tab 2: Configuration ---
with config_col:
    # We use an expander to make this section collapsible.
    with st.expander("⚙️ Configuration", expanded=True):
        st.write("Model Settings")
        st.selectbox(
            "Model",
            ["gpt-4", "gpt-3.5-turbo", "gemini-pro"],
            key="model",
            help="Select the AI model to use.",
        )
        st.slider(
            "Temperature",
            0.0,
            1.0,
            0.7,
            0.01,
            key="temperature",
            help="Controls randomness. Lower is more deterministic.",
        )
        st.checkbox(
            "Enable Streaming",
            value=True,
            key="streaming",
            help="Enable real-time response streaming.",
        )

        st.write("---")

        st.write("UI Settings")
        st.checkbox(
            "Show System Prompts",
            key="show_system_prompts",
            help="Display system-level prompts in the chat.",
        )
