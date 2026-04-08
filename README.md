# Production Ready MCP Boilerplate

## Cox's Bazar AI Itinerary MCP Server

A Model Context Protocol (MCP) server that provides travel planning tools and weather information for Cox's Bazar, Bangladesh.

<a href="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server/badge" alt="Cox's Bazar AI Itinerary Server MCP server" />
</a>

## Features

- **Weather Tools**: Get temperature forecasts and detailed weather information
- **Itinerary Tools**: Generate AI-powered travel itineraries
- **Travel Prompts**: Pre-configured prompts for travel planning

## Getting Started

```bash
uv sync
```

## Usage

### Run Inspector Tool

* Need node version > 20.x.x

```bash
./scripts/run-inspector.sh
```

### Run as installed command
This is serve the mcp server with auto-reload feature.

```bash
./scripts/run-mcp-server.sh
```


## Requirements
- Python 3.13+

## Project Structure

```
.
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py               # Main server entry point
│       ├── mcp_instance.py         # MCP instance configuration
│       ├── models/                 # Pydantic models and schemas
│       │   ├── __init__.py
│       │   └── itinerary_models.py
│       ├── handlers/               # MCP handler registrations
│       │   ├── __init__.py
│       │   ├── tools/
│       │   │   ├── __init__.py
│       │   │   ├── auth_additional.py
│       │   │   └── itinerary.py
│       │   ├── resources/
│       │   │   ├── __init__.py
│       │   │   └── weather.py
│       │   └── prompts/
│       │       ├── __init__.py
│       │       └── travel_prompts.py
│       ├── config/                 # Configuration modules
│       │   ├── auth_provider.py
│       │   └── custom_routes.py
│       ├── lib/                    # Shared libraries
│       │   ├── clerk_auth_provider.py
│       │   └── httpx_client.py
│       ├── services/               # Business logic
│       │   ├── __init__.py
│       │   └── itenerary_service.py
│       ├── prompt_templates/       # Prompt text builders
│       │   ├── __init__.py
│       │   └── travel.py
│       └── utils/                  # Utilities
│           ├── __init__.py
│           ├── elicitation.py
│           ├── get_weather_forecast.py
│           ├── helpers.py
│           └── http.py
├── tests/                          # Test suite
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── context.py
│   │   └── weather.py
│   ├── unit/
│   │   ├── test_elicitation.py
│   │   ├── test_models.py
│   │   ├── test_travel_prompts.py
│   │   ├── test_weather_forecast.py
│   │   └── test_weather_resource.py
│   └── integration/
│       ├── test_itinerary_tool.py
│       └── test_weather_api.py
├── scripts/                        # Shell scripts
│   ├── generate-secrets.sh
│   ├── run-inspector.sh
│   ├── run-mcp-server.sh
│   └── test.sh
├── _docs/                          # Documentation & ADRs
│   ├── adr/
│   ├── auth-provider-auth0.md
│   ├── httpx-client.md
│   ├── remote-mcp-connect.md
│   └── testing.md
├── .env.example                    # Environment variables template
├── Dockerfile                      # Docker configuration
├── glama.json                      # Glama configuration
├── pytest.ini                      # Pytest configuration
├── pyproject.toml                  # Project configuration and dependencies
├── LICENSE                         # MIT License
└── uv.lock                         # Dependency lock file
```

## License

MIT