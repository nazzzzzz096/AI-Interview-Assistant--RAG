"""
Streamlit Frontend for AI Interview Assistant

This app connects to the FastAPI RAG backend
and allows users to ask interview-related questions.
"""

import streamlit as st
import requests

# Replace with your deployed backend URL
API_URL = "https://ai-interview-assistant-rag.onrender.com/chat"

st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Interview Assistant")
st.markdown("Ask questions about Python, ML, Data Science, DSA, SQL, etc.")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
question = st.chat_input("Ask your question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("Thinking..."):

        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()

                answer = data.get("answer", "No answer")
                sources = data.get("sources", [])

                bot_response = answer

                if sources:
                    bot_response += "\n\n📄 **Sources:**\n"
                    for src in sources:
                        bot_response += f"- {src}\n"

            else:
                bot_response = f"Error: {response.text}"

        except Exception as e:
            bot_response = f"Error connecting to backend: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
