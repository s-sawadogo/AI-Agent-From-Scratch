# AI-Agent-From-Scratch

**Building AI Agent from scratch**

## Overview :

**Create an AI agent acting as a chatbot with the ability to use new tools**

## How to use this project :


**Install uv using pip**

```bash
pip install uv
```

**Starting uv environment with default files**

```bash
uv init . (initialising a uv project inside one directory)
```

**Installing necessary libraries with uv**

```bash
uv add langgraph langchain python-dotenv langchain-openai
```

**Create and put an OPENAI key in the .env file**

````
OPENAI_API_KEY=your_openai_api_key
````


**Running the main file**

```bash
uv run main.py
```

## Tools :

- **Langchain**
- **Langgraph**

**uv documentation :**

[https://docs.astral.sh/uv/getting-started/installation/#standalone-installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)