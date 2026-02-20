from typing import Annotated, Sequence, TypedDict
import json
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI 
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END 
from langgraph.prebuilt import ToolNode 

from dotenv import load_dotenv
load_dotenv()

document_content = {}

# ---------------- Agent State ----------------
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    document_content: dict 

# ---------------- Tools ----------------
@tool 
def update(content: str) -> str: 
    """Updates the document with the provided JSON content."""

    global document_content
    document_content = json.loads(content)

    return f"Document has been updated successfully! The current content is:\n{json.dumps(document_content, indent=2)}"


@tool
def save() -> str: 
    """Save the current document to a JSON file by appending it to a list of specifications."""
    global document_content
    
    filename = 'data/api_data_specifications.json'


    try: 
        # Load existing data
        try:
            with open(filename, "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        # Append the current document content to the existing data
        existing_data.append(document_content)

        # Save the updated list back to the file
        with open(filename, "w") as file: 
            json.dump(existing_data, file)

        document_content = {}

        return f"Document has been saved successfully to '{filename}'"

    except Exception as e:
        return f"Error saving document: {str(e)}"


tools = [update, save]
model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)


# ---------------- Agent Node ----------------
def our_agent(state: AgentState) -> AgentState: 
    global document_content

    if state["document_content"] and not document_content:
        document_content = state["document_content"]

    system_prompt = SystemMessage(content=f"""
    You are API Builder, a helpful API specification designing assistant. 
    You are going to help the user create and modify API specification documents.
                                  
    - Each time a user provides new information, you must use the 'update' tool to update the document content.
    - If the user wants to save and finish, you must use the 'save' tool. Do not 'save' without being instructed to do so.
    - Always show the current document state after modifications. 

    - The API specification should be in a JSON format with the following keys:
        - name: The name of the API
        - description: The description of the API
        - base_url: The base URL of the API
        - endpoints: A list of endpoints
            - endpoint: An endpoint with the following keys:
                - name: The name of the endpoint
                - description: The description of the endpoint
                - method: The HTTP method of the endpoint
                - uri: The URI of the endpoint
                - parameters: A list of parameters with the following keys:
                    - name: The name of the parameter
                    - description: The description of the parameter
                    - type: The data type of the parameter
                    - required: Whether the parameter is required

    The current document content is: {document_content}  
    """)
    
    # Build conversation history with system prompt + user/assistant messages
    all_messages = [system_prompt] + list(state["messages"])

    # Invoke model
    response = model.invoke(all_messages)

    # Append response to conversation
    return {"messages": list(state["messages"]) + [response], "document_content": document_content}


def should_continue(state: AgentState) -> str:
    messages = state["messages"]

    if not messages:
        return "continue"

    TERMINAL_TOOLS = {"save", "update"}
    
    if (len(messages) > 1 and
        isinstance(messages[-1], AIMessage) and messages[-1].content and
        isinstance(messages[-2], ToolMessage) and 
        messages[-2].name in TERMINAL_TOOLS and 
        messages[-2].status != "error"):
        return "end"

    return "continue"



graph = StateGraph(AgentState)
graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
# graph.add_edge("agent", "tools") 

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    }
)

graph.add_edge("tools", "agent") 


app = graph.compile()
