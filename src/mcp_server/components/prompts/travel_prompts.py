from mcp_server.mcp_instance import mcp

@mcp.prompt()
def travel_prompt(text: str) -> str:
    return f"provide good format {text}"