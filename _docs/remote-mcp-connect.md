# cox-mcp-server connect remote mcp server

## Cursor, Kiro and http type supported mcp clients

```json
{
	"mcpServers": {
		"cox-mcp-server": {
			"type": "http",
			"url": "https://coxs-bazar-itinerary-mcp-server.onrender.com/mcp"
		}
	}
}
```

## claude desktop 

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

## vscode

```json
{
  "servers": {
    "cox-mcp-server": {
      "type": "http",
      "url": "https://coxs-bazar-itinerary-mcp-server.onrender.com/mcp"
    }
  }
}
```


