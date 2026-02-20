
# Intuitive AI-Driven API Interaction Platform

Providing a simple, intuitive frontend for backend services is often harder than it should be. Many solutions still require users to understand technical details or navigate complex interfaces. Now imagine letting users interact with your backend simply by chatting with an AI that understands your business logic, knows your API endpoints, and can perform CRUD operations through natural language commands. That is exactly the experience this platform delivers.

Our solution is a lightweight multi-agent system designed to make your APIs accessible through natural conversation. 


> **No-Code, Natural Language Approach:**  
> Everything in this platform is built for no-code users. You configure your agent with natural language, and use it with natural language. No programming required.

## How It Works

Before you begin, it's recommended to use a virtual environment to manage dependencies. From your project root, run:

```
python -m venv venv
```

Then activate the virtual environment:

- On **Windows**:
  ```
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```
  source venv/bin/activate
  ```

Next, install the required packages:

```
pip install -r requirements.txt
```


### 1. API Specification Builder Agent

First, we help the agents understand your backend. You describe your endpoints to our system. Either by dropping in documentation, pasting your OpenAPI/Swagger specs, or even typing plain text descriptions. The Spec Builder Agent parses and ingests this info so the ecosystem knows which APIs are available, what each endpoint does, and which parameters are required for every use case.

**To start the API Specification Builder, run:**

```
python3 -m streamlit run app_api_specification_builder/streamlit_app.py
```

Follow the prompts to upload or describe your API.

### 2. Executor Agent

Once your specification is saved, the Executor Agent is ready to go. This AI can now understand your backend and execute API calls in response to plain language requests. No coding required.

**To launch the Executor Agent, run:**

```
python3 -m streamlit run agent_api_executor/executor_streamlit_app.py
```

You can now interact with your agent, perform business logic, and trigger backend operations just by chatting using natural language.



