# streamlit_app.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from api_executor_agent import api_executor_agent
import asyncio

async def invoke_agent(prompt: str) -> None:
    result = await api_executor_agent.run(prompt)
    return result.output.response_text

st.set_page_config(page_title="API Executor Agent", page_icon="📊")


# ---------------- Session State ----------------
if "username" not in st.session_state:
    st.session_state.username = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_content" not in st.session_state:
    st.session_state.document_content = {}

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False


def reset_chat():
    st.session_state.messages = []
    st.session_state.document_content = {}
    st.session_state.chat_open = False


if not st.session_state.username:
    if session_username := st.text_input("Enter your username:"): 
        st.session_state.username = session_username
        st.rerun()

    
if st.session_state.username: 

    # ---------------- UI ----------------
    st.title("API Executor Agent")

    if not st.session_state.chat_open:

        st.write(f"👋 Hello, **{st.session_state.username}**!")


        st.markdown(
        """
        This tool lets you **execute API operations by chatting with an agent**.

        You can:
        - Describe an action you want to perform (e.g., buy a stock, get the weather, sell an item online)
        - Interact with a conversational agent that interprets your request
        - See responses from real API calls
        """
        )

        if st.button("➕ Create dataset specification"):
            st.session_state.chat_open = True
            st.rerun()

    else:

        if st.session_state.messages:
            for i, message in enumerate(st.session_state.messages):
                if isinstance(message, HumanMessage):
                    st.chat_message("user").write(message.content)
                elif isinstance(message, AIMessage):
                    st.chat_message("assistant").write(f"🤖 {message.content}")

        # ---- User input ----
        if prompt := st.chat_input("Type your command or query..."):
            st.chat_message("user").write(prompt)

            # Store user prompt in session state
            st.session_state.messages.append(HumanMessage(content=prompt))

            response = asyncio.run(invoke_agent(prompt))

            st.chat_message("assistant").write(f"🤖 {response}")

            st.session_state.messages.append(AIMessage(content=response))

        
