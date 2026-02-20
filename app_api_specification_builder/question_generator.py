import json
from typing import List
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# Initialize your LLM
question_model = ChatOpenAI(model="gpt-5-nano")

def generate_user_requests(api_spec: dict) -> List[str]:
    """
    Given an API specification JSON, generate 10 natural-language requests
    that a real user might make to an LLM capable of calling this API.

    Args:
        api_spec (dict): The API specification.

    Returns:
        List[str]: A list of 10 user-style requests in natural language.
    """
    prompt = SystemMessage(content=f"""
You are a helpful assistant that imagines **real users interacting with an LLM
that can call this API**. 

Given the following API specification (JSON), generate 10 natural-language
requests that a user might make to the LLM to interact with this API. 

Guidelines:
- Use **conversational language**, like a user asking a virtual assistant
- Include examples like: "Can you show me all tasks due today?" or 
  "Please delete the task with ID 123."
- Do NOT write in technical or documentation style
- Focus on real usage scenarios
- Return the output as a numbered list

API Specification:
{json.dumps(api_spec, indent=2)}
""")

    response = question_model.invoke([prompt])

    # Split into lines and clean
    requests = [
        line.strip()
        for line in response.content.split("\n")
        if line.strip() and (line[0].isdigit() or line[0] != "")
    ]

    # Only keep the first 10 requests
    return requests[:10]

# Example usage
if __name__ == "__main__":
    sample_api_spec = {
        "name": "Todo API",
        "description": "Manage your tasks",
        "base_url": "https://api.example.com",
        "endpoints": [
            {
                "name": "Get Todos",
                "description": "Retrieve all tasks",
                "method": "GET",
                "uri": "/todos",
                "parameters": []
            },
            {
                "name": "Add Todo",
                "description": "Add a new task",
                "method": "POST",
                "uri": "/todos",
                "parameters": [
                    {"name": "title", "description": "Task title", "type": "string", "required": True},
                    {"name": "due_date", "description": "Optional due date", "type": "string", "required": False}
                ]
            }
        ]
    }

    user_requests = generate_user_requests(sample_api_spec)
    print("\n".join(user_requests))
