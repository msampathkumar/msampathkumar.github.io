import logging
import streamlit as st

st.set_page_config(
    page_title="Gemini AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """
    The main function of the Streamlit application.
    """
    st.title("Gemini AI ✨")

    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        st.info(
            "This is a demo of a Streamlit app that uses the Gemini AI API to generate text."
        )

        # Model selection
        model_name = st.selectbox(
            "Select a model:",
            ("gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"),
            index=0,
        )

        # Temperature and token limit
        temperature = st.slider(
            "Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1
        )
        token_limit = st.slider(
            "Token Limit:", min_value=1, max_value=2048, value=1024, step=1
        )

        # Grounding options
        st.subheader("Grounding Options")
        use_rag = st.checkbox("Use RAG")
        use_google_search = st.checkbox("Use Google Search")

        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.messages = []

    # Main chat interface
    st.header("Chat with Gemini")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
                    f"An error occurred while sending message to LLM: {e}",
                    exc_info=True,
                )
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
