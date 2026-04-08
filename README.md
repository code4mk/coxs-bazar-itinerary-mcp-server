# Production Ready MCP Boilerplate

## Cox's Bazar AI Itinerary MCP Server

A Model Context Protocol (MCP) server that provides travel planning tools and weather information for Cox's Bazar, Bangladesh. Built with [FastMCP](https://github.com/jlowin/fastmcp) and managed by [uv](https://docs.astral.sh/uv/).

<a href="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@code4mk/coxs-bazar-itinerary-mcp-server/badge" alt="Cox's Bazar AI Itinerary Server MCP server" />
</a>

## Features

- **Weather Resources**: Temperature forecasts and detailed weather information
- **Itinerary Tools**: AI-powered travel itinerary generation
- **Travel Prompts**: Pre-configured prompts for travel planning
- **Auth Support**: Optional authentication via Clerk (configurable via env)
- **Rate Limiting**: Built-in rate limiting middleware
- **Docker Ready**: Production Dockerfile included
- **Linting & Formatting**: Ruff + pre-commit hooks (see [`_docs/lint-formatting.md`](_docs/lint-formatting.md))

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Node.js 20+ (only for MCP Inspector)

## Getting Started

```bash
# Install dependencies
uv sync

# Copy environment variables and configure
cp .env.example .env

# (Optional) Install pre-commit git hooks
uv run pre-commit-install
```

## CLI Commands

All commands are registered in `pyproject.toml` and available via `uv run`:

| Command | Description |
|---------|-------------|
| `uv run mcp-server` | Start the MCP server |
| `uv run mcp-server-dev` | Start the MCP server in dev mode (auto-reload) |
| `uv run mcp-inspector` | Launch the MCP Inspector UI (requires Node.js 20+) |
| `uv run lint` | Run pre-commit hooks (lint + format) on all files |
| `uv run pre-commit-install` | Install pre-commit hooks into the git repo |

### Dev Server

Start the MCP server with auto-reload via [watchdog](https://pypi.org/project/watchdog/):

```bash
uv run mcp-server-dev
# or
./scripts/run-mcp-server.sh
```

### MCP Inspector

Launch the interactive MCP Inspector UI to test tools, resources, and prompts:

```bash
uv run mcp-inspector
# or
./scripts/run-inspector.sh
```

### Linting & Formatting

```bash
# Run lint + format via pre-commit
uv run lint

# Or run individually
./scripts/lint.sh       # ruff check . --fix
./scripts/format.sh     # ruff format .
```

See [`_docs/lint-formatting.md`](_docs/lint-formatting.md) for full configuration details.

### Testing

```bash
./scripts/test.sh
```

See [`_docs/testing.md`](_docs/testing.md) for test conventions and fixtures.

## Docker

```bash
docker build -t mcp-server .
docker run mcp-server
```

The server runs via `uv run mcp-server` inside the container. Transport and port are configurable through environment variables (`TRANSPORT_NAME`, `SERVER_PORT`, `SERVER_HOST`).

## Project Structure

```
.
├── src/mcp_server/
│   ├── server.py                  # Main server entry point
│   ├── mcp_instance.py            # FastMCP instance & auth config
│   ├── cli.py                     # CLI command definitions
│   ├── config/
│   │   ├── auth_provider.py       # Auth provider factory
│   │   └── custom_routes.py       # Custom HTTP routes
│   ├── handlers/                  # MCP handler registrations (auto-discovered)
│   │   ├── tools/
│   │   │   ├── auth_additional.py
│   │   │   └── itinerary.py
│   │   ├── resources/
│   │   │   └── weather.py
│   │   └── prompts/
│   │       └── travel_prompts.py
│   ├── models/
│   │   └── itinerary_models.py    # Pydantic models & schemas
│   ├── services/
│   │   └── itenerary_service.py   # Business logic
│   ├── lib/
│   │   ├── clerk_auth_provider.py # Clerk OAuth provider
│   │   └── httpx_client.py        # Async HTTP client wrapper
│   ├── prompt_templates/
│   │   └── travel.py              # Prompt text builders
│   └── utils/
│       ├── elicitation.py
│       ├── get_weather_forecast.py
│       ├── helpers.py
│       └── http.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── context.py
│   │   └── weather.py
│   ├── unit/
│   │   ├── test_auth_additional_tools.py
│   │   ├── test_auth_provider.py
│   │   ├── test_elicitation.py
│   │   ├── test_helpers.py
│   │   ├── test_itinerary_service_extra.py
│   │   ├── test_itinerary_tool_handler.py
│   │   ├── test_models.py
│   │   ├── test_server.py
│   │   ├── test_travel_prompts.py
│   │   ├── test_travel_prompts_handler.py
│   │   ├── test_weather_forecast.py
│   │   └── test_weather_resource.py
│   └── integration/
│       ├── test_itinerary_tool.py
│       └── test_weather_api.py
├── scripts/
│   ├── run-mcp-server.sh          # Dev server with auto-reload
│   ├── run-inspector.sh           # MCP Inspector launcher
│   ├── test.sh                    # Test runner
│   ├── lint.sh                    # Ruff lint --fix
│   ├── format.sh                  # Ruff format
│   └── generate-secrets.sh        # Secret key generator
├── _docs/                         # Documentation & ADRs
│   ├── adr/
│   │   ├── 001-choose-fastmcp.md
│   │   ├── 002-choose-httpx.md
│   │   └── ADR-template.md
│   ├── auth-provider-auth0.md
│   ├── httpx-client.md
│   ├── lint-formatting.md
│   ├── remote-mcp-connect.md
│   └── testing.md
├── .env.example                   # Environment variables template
├── .pre-commit-config.yaml        # Pre-commit hook config
├── Dockerfile                     # Production Docker image
├── pyproject.toml                 # Project config & dependencies
├── ruff.toml                      # Ruff linter/formatter config
├── pytest.ini                     # Pytest configuration
├── glama.json                     # Glama registry config
└── LICENSE                        # MIT License
```

## Documentation

| Document | Description |
|----------|-------------|
| [`_docs/lint-formatting.md`](_docs/lint-formatting.md) | Ruff & pre-commit configuration |
| [`_docs/testing.md`](_docs/testing.md) | Test setup, fixtures, and conventions |
| [`_docs/httpx-client.md`](_docs/httpx-client.md) | Async HTTP client usage |
| [`_docs/auth-provider-auth0.md`](_docs/auth-provider-auth0.md) | Auth provider integration |
| [`_docs/remote-mcp-connect.md`](_docs/remote-mcp-connect.md) | Remote MCP connection guide |
| [`_docs/adr/`](_docs/adr/) | Architecture Decision Records |

## License

MIT
