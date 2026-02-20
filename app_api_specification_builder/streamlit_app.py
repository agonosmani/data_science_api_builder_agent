# streamlit_app.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from api_agent import app
from question_generator import generate_user_requests
import json
from api_spec_python_tool_generator import generate_python_tool_latest


st.set_page_config(page_title="API Spec Builder", page_icon="⚡")

# ---------------- Session State ----------------
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


# ---------------- UI ----------------
st.title("API Specification Builder")

initial_message = """
To build the API specification, I'll need the following information from you:

1. **API Name**: What is the name of the API?
2. **Description**: A brief description of what the API does.
3. **Base URL**: The base URL where the API can be accessed.
4. **Endpoints**: Details about each endpoint, including:
- **Endpoint Name**: The name of the endpoint.
- **Description**: A brief description of what the endpoint does.
- **HTTP Method**: The HTTP method used (GET, POST, PUT, DELETE, etc.).
- **URI**: The URI path for the endpoint.
- **Parameters**: A list of parameters (if any) required for the endpoint, including:
    - Name
    - Description
    - Type (e.g., string, integer)
    - Required (true/false)

Feel free to provide this information piece by piece, and I'll help you create the specification!
"""
    

if not st.session_state.chat_open:
    
    if st.button("➕ Add specification"):
        st.session_state.chat_open = True
        st.rerun()
        
else:
    st.chat_message("assistant").write(f"🤖 {initial_message}")

    # # ---- Chat history ----
    # Render new messages
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage) and msg.content:
            st.chat_message("user").write(msg.content)
        if isinstance(msg, AIMessage) and msg.content.strip():
            st.chat_message("assistant").write(f"🤖 {msg.content}")


     # ---- User input ----
    if prompt := st.chat_input("Describe your API spec..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.chat_message("user").write(prompt)

        # Run graph until terminal
        state = {
            "messages": st.session_state.messages,
            "document_content": st.session_state.document_content,
        }

        result = app.invoke(state)

        # Update state
        st.session_state.messages = result.get("messages", [])
        st.session_state.document_content = result.get(
            "document_content", {}
        )

        latest_ai_message = next(
            (msg for msg in reversed(st.session_state.messages) 
             if isinstance(msg, AIMessage) and msg.content), 
            None
        )

        if latest_ai_message:
            st.chat_message("assistant").write(f"🤖 {latest_ai_message.content}")
            
        # ---- Terminal detection ----
        if any(
            isinstance(m, ToolMessage)
            and m.name == "save"
            and m.status != "error"
            for m in st.session_state.messages
        ):
            st.success("Specification completed.")
            st.json(st.session_state.document_content)

            # Convert to JSON string
            json_str = json.dumps(
                st.session_state.document_content,
                indent=2
            )
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"{st.session_state.document_content['name'].replace(' ', '_').lower()}_document.json",
                mime="application/json",
            )   

            generate_python_tool_latest()

            st.chat_message("assistant").write("🤖 Hold on a moment while I generate 10 example questions for you...")


            generated_questions = generate_user_requests(st.session_state.document_content)
            questions_message = "Here are 10 questions that real users might ask about the API:\n" + "\n".join(generated_questions)
            st.session_state.messages.append(AIMessage(content=questions_message))

            print(questions_message)
            
            st.chat_message("assistant").write(f"🤖 {questions_message}")


            reset_chat()

        else:
            # st.info("Specification updated. Let me know if there's feedback or if you want to save.")
            st.info("Specification updated.")
            st.json(st.session_state.document_content)
