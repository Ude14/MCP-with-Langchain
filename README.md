# MCP-with-Langchain

This repository contains the necessary code to run an **MCP server**, an **Ollama LLM server**, and to execute petitions to the **LangChain agent** that connects them.

---

## 1. Running the Ollama Server

This section details how to set up and run the necessary Large Language Model (LLM) using Ollama.

1. Install **Ollama** from the official download page:

   
   [https://ollama.com/download/windows](https://ollama.com/download/windows)
2. **Before installing the LLM**, configure the host to listen on all interfaces. This is crucial for external connections:


   Bash

   
   set OLLAMA_HOST=0.0.0.0:11434
   
4. **Once we have done that** we can do:

   
   Bash

   
   ollama serve
   
   Opening a new terminal we are going to install the model, first choose from https://ollama.com/search a model that suits you best, then:

   
   Bash

   
   ollama pull <model>
   
   For example: ollama pull llama3.2:1b, once installed we just run it:

   
   Bash

   
   ollama run llama3.2:1b
   
   If you are having trouble with the run you can see if the model was installed with "ollama list" where you should see the name of the model, the size...
   When we do ollama run llama3.2:1b we can ask the LLM whatever we want to see if it works, then exit with /bye.
   Finally, to run it so we can use it in our system just do:

   
   Bash

   
   ollama serve

## 2. Running the MCP Server
   1. **First**, install FastMCP:


   Bash

   
   pip install fastmcp

   2. **Now**, it is ready to use once we write the code. Then you can see if it works with:
   -This one runs the server in the port especified


  Bash

  
   fastmcp run server_mcp_lang.py:mcp --port 9001 --transport streamable-http

   -Another possibility is to run directly:

   
   Bash

   
   python server_mcp.py

## 3. Trying out
   To try the code from clientLangChain.py just execute:


   Bash

   python clientLangChain.py


   # If what you want is to have your agent as a server to recibe questions:
   We need to have running beforehand the ollama server, the MCP server and then:



   Bash
   
   uvicorn main_server:app --reload

   With our server running we can to petitions with:

   curl -X POST -H "Content-Type: application/json" -d "{\"user_prompt\": \"Give me the author of the book The Lord of the Rings\"}" http://127.0.0.1:8000/answerer/

   

