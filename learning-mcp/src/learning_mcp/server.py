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

if __name__ == "__main__":
    mcp.run()