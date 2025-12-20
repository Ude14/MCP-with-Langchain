# Imports:
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import asyncio
import os
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from fastapi import FastAPI
from pydantic import BaseModel

os.environ["LANGCHAIN_DEBUG"] = "true"


""" 
Definition of the LLM that will be used to create the agent.
Args:
    model: Model that will be used
    temperature: Parameter that controls the randomness of the model's output.
    num_ctx: Size of the context
    max_tokens: Number of tokens that can be proccessed, less tokens means quicker answeres
    base_url: The url where is the LLM
"""
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.2,             
    num_ctx=4096,                
    max_tokens=512,              
    base_url="http://localhost:11434"
)


"""
Definition of the MCP client, MultiServerMCP used to be able to accept more than one MCP server.
The name, transport and location must be specified.
"""
client = MultiServerMCPClient(
    {
        "buscador": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:9001/mcp"
        }
    }
)


@wrap_tool_call
async def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return await handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )


async def build_agent():
    """Creates and returns an agent ready to use by getting the tools form the MCP client."""
    tools = await client.get_tools()
    print("\nConnected to server with tools:", [tool.name for tool in tools])

        #Several system prompts that can be used.
    system_prompt1 = "You are a helpful assistant that uses the tools given to give answers, if they have arguments search the prompt to find it"
    system_prompt2 ="Only respond if you have been given tools to answer this, anything else say you can't answer"
    system_prompt3 = ("You are a helpful assistant. Always use the available tools to answer questions. "
    "If you recibe a tool with parameters call the tool"
    "When calling a tool, ensure all required parameters are provided with the exact values extracted from the user's message.")

        #There is an argument in create_agent to establish the answer format of the agent
    agent = create_agent(
        llm,
        tools,
        system_prompt= system_prompt3,
        middleware = [handle_tool_errors]
    )
    return agent


async def ask(agent, message: str):
    """
    Sends a message to the agent and retrieves the generated response.

    Args:
        agent: The initialized agent instance capable of processing prompts.
        message (str): The user's input message/prompt.

    Returns:
        str: The agent's processed response.
    """
    result = await agent.ainvoke({"messages": [
        {"role": "user", "content": message}
     ]})
     
     #With result["messages"][2].content you get the answer of the tool called.
    return result["messages"][3].content


#Create the app with FastAPI
app = FastAPI()

# Prompt Model:
class Prompt(BaseModel):
    user_prompt: str

# Endpoints:
@app.get("/")
def server_test():
    """
    Check the server status.
    
    Returns:
        dict: A confirmation message indicating the server is operational.
    """
    return {"mensaje": "Server up and running!"}


@app.post("/answerer/")
async def prompt_answerer(prompt: Prompt):
    """
    Process the received prompt and return the agent's response.
    
    - **prompt**: The prompt object containing the user's text.
    - **Returns**: A JSON object containing the generated response.
    """
    agent = await build_agent()
    print(f"--- NEW PETITION RECIEVED: {prompt.user_prompt[:50]}... ---")
    
    return {
        "response" : await ask(agent, prompt.user_prompt) 
     }

       
# Server execution:
if __name__ == "__main__":
    asyncio.run(main())
    # Maybe use directly: uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)