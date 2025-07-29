import streamlit as st
import os
import llm  # Our custom LLM interaction module

st.set_page_config(layout="wide")
st.title("Unlock Enterprise AI: Grounding Gemini with RAG and Google Cloud Search 🚀")
st.markdown(
    "Ask questions about our mock internal documents, and Gemini will provide grounded answers. 🎯"
)

# --- Simulated Knowledge Base (In-Memory Documents) ---
# In a real RAG system, this would be a vast, external knowledge base
# indexed by Google Cloud Search or a vector database.
MOCK_INTERNAL_DOCS = [
    {
        "title": "Project Phoenix Q1 2025 Report 📈",
        "content": """
        **Project Phoenix - Q1 2025 Performance Summary**
        The 'Project Phoenix' initiative demonstrated strong performance in Q1 2025.
        **Revenue:** EMEA region generated $10.5 million (up 15% YoY), driven by 5 new client wins in Germany and France. 💰
        North America achieved $8.2 million (up 10% YoY), fueled by existing client expansion. 🇺🇸🇨🇦
        **Key Milestones:**
        - Beta launch completed for Phase 2 in early February. ✅
        - Integration with existing CRM systems reached 80% completion by end of March. 🔗
        - Onboarding 3 new sales reps in EMEA. 👥
        **Challenges:** Supply chain disruptions impacted hardware delivery by 5%. 📉
        """,
    },
    {
        "title": "IT Policy: New Hardware Requests 💻",
        "content": """
        **IT Policy: Hardware Procurement and New Laptop Requests**
        Employees requiring new laptops or hardware must submit a request via the IT Service Portal. 🛠️
        **Process:**
        1. Fill out the 'New Hardware Request' form on the IT Service Portal. ✍️
        2. Obtain manager approval within the portal. ✅
        3. IT procurement will review the request (allow 3-5 business days). 🗓️
        4. Device ordered and configured (delivery typically 2-4 weeks). 🚚
        **Approval Criteria:** Requests are evaluated based on job role requirements and existing equipment age (typically 3+ years). 📏
        """,
    },
    {
        "title": "HR Handbook: Vacation Policy 🏖️",
        "content": """
        **HR Handbook: Vacation and Leave Policy**
        All full-time employees accrue 20 days of paid vacation leave annually. ☀️
        Vacation requests must be submitted at least 4 weeks in advance via the HR Portal. 📅
        Managers must approve requests within 5 business days. ✅
        Unused vacation days can be carried over for up to 5 days to the next calendar year. Any days above this limit are forfeited. ⏳
        Maximum carry-over is 5 days.
        """,
    },
]

# --- Streamlit UI ---
st.header("Simulated RAG Chatbot 💬")
st.write(
    "This chatbot uses a *simulated* internal knowledge base to provide grounded answers. Imagine this data is indexed by Google Cloud Search! 🔍"
)

if "messages_rag" not in st.session_state:
    st.session_state.messages_rag = []

for message in st.session_state.messages_rag:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about our internal documents... 🤔"):
    st.session_state.messages_rag.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Searching internal knowledge base and generating response... ⏳"):
        # 1. Simulate Retrieval using our llm.py helper
        retrieved_docs = llm.retrieve_relevant_docs_simulated(
            prompt, MOCK_INTERNAL_DOCS
        )

        # 2. Augment and Generate using our llm.py helper
        gemini_response = llm.get_grounded_response_from_gemini(prompt, retrieved_docs)

    st.session_state.messages_rag.append(
        {"role": "assistant", "content": gemini_response}
    )
    with st.chat_message("assistant"):
        st.markdown(gemini_response)
