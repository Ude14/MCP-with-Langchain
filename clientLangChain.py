from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
import asyncio
import os
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

os.environ["LANGCHAIN_DEBUG"] = "true"

#Ajustar parámetros según se quiera

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.2,            # Más determinista y rápido
    num_ctx=4096,               # Más contexto
    max_tokens=512,              # Respuestas más rápidas
    base_url="http://localhost:11434"
)




client = MultiServerMCPClient(
    {
        "buscador": {
            "transport": "stdio",
            "command": "python",
             "args": ["/Users/udeHP/TFG/server_mcp_lang.py"]
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
    """Crea y devuelve un agente listo para usar."""
    tools = await client.get_tools()
    print("\nConnected to server with tools:", [tool.name for tool in tools])


    #Con este prompt, la pregunta 1 funciona bien pero la 2 ya no tanto
    system_prompt1 = "You are a helpful assistant that uses the tools given to give answers, if they have arguments search the prompt to find it"

    system_prompt2 ="Don't answer the cuestion given, just evaluate if any tools given can be used to respond"
    system_prompt3 = ("You are a helpful assistant. Always use the available tools to answer questions. "
    "If you recibe a tool with parameters call the tool"
    "When calling a tool, ensure all required parameters are provided with the exact values extracted from the user's message.")
#Hay un argumento que lo que hace es decir al LLM el formato de respuesta

    
    agent = create_agent(
        llm,
        tools,
        system_prompt= system_prompt3,
        middleware = [handle_tool_errors]
    )
    return agent

"""
Estoy probando diferentes formas de preguntar y enseñar el resultado
async def ask(agent, message: str):
    ""Envía una instrucción y devuelve la respuesta final limpia.""
    try:
        response = await agent.ainvoke({"messages": [
            {"role": "user", "content": message}
        ]})

        for msg in response["messages"]:
            if msg.type == "tool":
                return msg.content

        final_msg = response["messages"][-1].content
        return final_msg

    except Exception as e:
        return f"❌ Error en el agente: {e}"

"""
# Antigravity
async def ask(agent, message: str):
    result = await agent.ainvoke({"messages": [
        {"role": "user", "content": message}
    ]})
    for message in result["messages"]:
        message.pretty_print()


async def main():
    print("prueba de la conexión con el llm sin neceisdad de crear agente")
    try:
        # Esto usa SÓLO el LLM, sin agente ni herramientas
        respuesta = llm.invoke("Cúal es la capital de España")
        print(f"Respuesta del LLM: {respuesta.content}")
    except Exception as e:
        print(f"FALLO: Error al invocar al LLM. ¡OLLAMA NO ESTÁ CONECTADO!: {e}")


    print("🚀 Construyendo agente optimizado...")
    agent = await build_agent()

    # Pregunta 1
    await ask(agent, "Dame un saludo personalizado, me llamo Edu")
    await ask(agent, "How much is 2 + 2?")
    await ask(agent, "Return a poem with the word María")


"""
    print("\n👉 Pregunta 1")
    print(await ask(agent, "Dame un saludo personalizado, me llamo Edu"))
    print("-" * 40)

    # Pregunta 2
    print("👉 Pregunta 2")
    print(await ask(agent, "How much is 2 + 2?"))
    print("-" * 40)

    # Pregunta 3
    print("👉 Pregunta 3 (Poema)")
    print(await ask(agent, "Give me a poem with the word Rose"))
    print("-" * 40)

    # Pregunta 4
    saludo = await ask(agent, "Dame un saludo personalizado, me llamo Edu")
    print(await ask(agent, saludo))

"""



if __name__ == "__main__":
    asyncio.run(main())