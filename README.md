# Cox's Bazar AI Itinerary MCP Server

A Model Context Protocol (MCP) server that provides travel planning tools and weather information for Cox's Bazar, Bangladesh.

<a href="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server/badge" alt="Cox's Bazar AI Itinerary Server MCP server" />
</a>

## Features

- **Weather Tools**: Get temperature forecasts and detailed weather information
- **Itinerary Tools**: Generate AI-powered travel itineraries
- **Travel Prompts**: Pre-configured prompts for travel planning

## Installation

```bash
uv sync
```

## Usage

### Run with MCP dev (development)
```bash
uv run mcp dev src/mcp_server/server.py
```

### Run as installed command
```bash
uv run simple-mcp-server
```

## Requirements

- Python 3.13+
- mcp[cli] >= 1.20.0
- python-dateutil >= 2.9.0
- requests >= 2.32.5

## Project Structure

```
src/
└── mcp_server/
    ├── server.py           # Main server entry point
    ├── tools/              # MCP tools
    │   ├── weather.py      # Weather-related tools
    │   └── itinerary.py    # Travel itinerary tools
    ├── resources/          # MCP resources
    │   └── weather.py      # Weather data resources
    ├── prompts/            # MCP prompts
    │   └── travel_prompts.py  # Travel planning prompts
    └── utils/              # Utilities
        └── helpers.py      # Helper functions
```

## connect to cluade desktop 

```json
{
  "mcpServers": {
    "coxs-bazar-itinerary": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/code4mk/Documents/GitHub/gumpper-group/mcp-explore/mcp-server-python-template",
        "run",
        "simple-mcp-server"
      ]
    }
  }
}
```

## License

MIT