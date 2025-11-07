# Renote MCP server connect with Client

## remote server connect vscode

```json
{
	"servers": {
		"cox-mcp-server": {
			"url": "https://coxs-bazar-itinerary-mcp-server.onrender.com/mcp",
			"type": "http"
		}
	}
}
```

## remove server connect claude code (desktop app)

```bash
nvm use --lts
open -a Claude.app

```

```json
{
  "mcpServers": {
    "cox-mcp-server": {
      "command": "npx", 
      "args": ["-y", "mcp-remote", "https://coxs-bazar-itinerary-mcp-server.onrender.com/mcp"]
    }
  }
}
```

## remotte server connect kiro

```json 
{
  "mcpServers": {
    "cox-mcp-server": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```
