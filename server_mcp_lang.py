from fastmcp import FastMCP
#from mcp.server.fastmcp import FastMCP
import requests

# Creamos una instancia del MCP server
mcp = FastMCP("Buscador")

# Creamos la herramienta
@mcp.tool()
def suma(a: int, b: int) -> str:
    """Add number a and number b to obtain the result"""
    r = a + b
    return f"El resultado de la suma de {a} y {b} es {r}"

@mcp.tool()
def get_saludo(name: str ="World") -> str:
    """Returns a customized greeting, return the answer with the word they used to present themselves"""
    return f"Hola {name}, encantado!"

@mcp.tool()
def get_poem(word: str ="Tu") -> str:
    """Returns a poem with str format with the word asked. It just needs the word asked"""
    return f"{word} si me miras a los ojos, se me ponen los mofletes rojos."

@mcp.tool()
def get_dog_image() -> str:
    """Returns the url to a random dog image"""
    url= 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        image= data['message']
        return image
    
    else:
        return "The API failed"

@mcp.tool()
def get_author_book(book: str = "Tree") -> str:
    """Returns the author of a book"""
    url = 'https://openlibrary.org/search.json?q='
    url_final = f"{url}{book}"
    response = requests.get(url_final)

    if response.status_code == 200:
        data = response.json()
        documentos = data['docs']
        primer_documento = documentos[0]
        lista_autores = primer_documento['author_name']
        nombre_autor = lista_autores[0]
        return nombre_autor
    
    else:
        return "The API failed"





if __name__ == "__main__":
 # This runs the server, defaulting to STDIO transport
    mcp.run(transport="http", host="127.0.0.1", port=9001)

    # To use a different transport, e.g., HTTP:
    # mcp.run(transport="http", host="127.0.0.1", port=9000)


# Mirar esto para más info https://gofastmcp.com/servers/server
