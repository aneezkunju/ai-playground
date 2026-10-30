# from mcp.server.fastmcp import FastMCP
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("hello-mcp")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b

@mcp.tool()
def modulus(a: float, b: float) -> float:
    """Return the remainder of a divided by b."""
    return a % b

@mcp.tool()
def subtract (a:float, b:float) -> float:
    '''
    returns subtractio of two numbers
    '''
    return a - b

@mcp.tool()
def square (a:float) -> float:
    '''
    returns sqyare of a number
    '''
    return a**2

@mcp.resource("resource://constants")
def constants() -> str:
    return "g = 9.8\ne = 1.2"

@mcp.resource("resource://multiplication-table/5")
def five_times_table() -> str:
    return "\n".join(f"5 x {i} = {5 * i}" for i in range(1, 11))

if __name__ == "__main__":
    mcp.run(transport="stdio")