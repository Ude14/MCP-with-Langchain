# MCP with LangChain

This repository contains everything you need to run:

- An **MCP Server**
- An **Ollama LLM Server**
- A **LangChain agent** that connects to the MCP server and allows you to interact with it.

---

# 1. Running the Ollama Server

First, install **Ollama** from the official website:

https://ollama.com/download/windows

## Configure Ollama

Before installing or running any model, configure Ollama to listen on all network interfaces. This is required if external applications need to connect to it.

```bash
set OLLAMA_HOST=0.0.0.0:11434
```

## Start the Ollama server

```bash
ollama serve
```

## Download a model

Open a new terminal and choose a model from:

https://ollama.com/search

Then download it with:

```bash
ollama pull <model>
```

For example:

```bash
ollama pull llama3.2:1b
```

## Test the model

Run the downloaded model:

```bash
ollama run llama3.2:1b
```

You can ask the model any question to verify that everything works correctly. Exit the interactive session with:

```text
/bye
```

If the model cannot be found, verify that it was installed successfully:

```bash
ollama list
```

The command should display the installed models along with their sizes and other information.

Finally, make sure the Ollama server is running before using the rest of the project:

```bash
ollama serve
```

---

# 2. Running the MCP Server

## Install FastMCP

```bash
pip install fastmcp
```

## Run the server

You can start the MCP server using FastMCP:

```bash
fastmcp run server_mcp_lang.py:mcp --port 9001 --transport streamable-http
```

Alternatively, you can run it directly with Python:

```bash
python server_mcp.py
```

---

# 3. Running the LangChain Client

To test the MCP server using the provided LangChain client, simply run:

```bash
python clientLangChain.py
```

---

# 4. Running the Agent as an API Server

If you want to expose the LangChain agent through a REST API, make sure the following services are already running:

1. Ollama Server
2. MCP Server

Then start the API server:

```bash
uvicorn main_server:app --reload
```

Once the server is running, you can send requests using `curl`:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d "{\"user_prompt\":\"Give me the author of the book The Lord of the Rings\"}" \
  http://127.0.0.1:8000/answerer/
```

---

# Project Workflow

The complete execution flow is:

```text
User
   │
   ▼
LangChain Agent
   │
   ▼
MCP Server
   │
   ▼
Ollama LLM
```

The LangChain agent receives the user's request, communicates with the MCP server whenever tools are required, and the MCP server uses the Ollama LLM to generate the final response.
