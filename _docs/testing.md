# Testing Documentation

## Overview

This MCP server project includes a comprehensive test suite with unit tests and integration tests. The test suite uses pytest as the testing framework and includes coverage reporting, fixtures, and custom markers for organizing tests.

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                          # Shared pytest configuration (imports fixtures)
├── fixtures/                            # Test fixtures and mocks
│   ├── __init__.py
│   ├── context.py                       # Mock MCP Context fixture
│   └── weather.py                       # Weather sample data fixtures
├── unit/                                # Unit tests (90 tests)
│   ├── __init__.py
│   ├── test_auth_additional_tools.py    # Auth-related MCP tool handlers
│   ├── test_auth_provider.py            # Auth provider selection logic
│   ├── test_elicitation.py              # Trip extension elicitation flows
│   ├── test_helpers.py                  # Shared helper utilities
│   ├── test_itinerary_service_extra.py  # Itinerary service activity suggestions
│   ├── test_itinerary_tool_handler.py   # Itinerary tool handler delegation
│   ├── test_models.py                   # Data model validation
│   ├── test_server.py                   # Server main() wiring and transports
│   ├── test_travel_prompts.py           # Travel prompt template generation
│   ├── test_travel_prompts_handler.py   # Prompt handler delegation
│   ├── test_weather_forecast.py         # Weather forecast utilities
│   └── test_weather_resource.py         # Weather MCP resource handler
└── integration/                         # Integration tests (13 tests)
    ├── __init__.py
    ├── test_itinerary_tool.py           # End-to-end itinerary generation
    └── test_weather_api.py              # Open-Meteo weather API client
```

**Total Tests**: 103 tests
- **Unit Tests**: 90 tests across 12 files (fast, isolated component testing)
- **Integration Tests**: 13 tests across 2 files (component interaction testing)

## Quick Start

### Installation

Ensure you have the dev dependencies installed:

```bash
# Using uv (recommended)
uv sync --dev
```

### Run All Tests

```bash
# Using the test script (recommended)
./scripts/test.sh

# Or directly with uv
uv run pytest

# Or with verbose output
uv run pytest tests/ -v
```

### Test Script (`scripts/test.sh`)

The project includes a ready-to-use test script that runs the full suite with coverage:

```bash
#!/bin/bash
set -e
set -x

uv run pytest \
    --cov=src/mcp_server \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    --cov-fail-under=80 \
    --cov-config=.coveragerc \
    -v \
    tests/ \
    "${@}"
```

This script:
- Runs all tests with verbose output
- Generates coverage reports (terminal with missing lines, HTML, and XML)
- Enforces a minimum 80% coverage threshold
- Uses `.coveragerc` for coverage configuration
- Passes any extra arguments through (e.g., `./scripts/test.sh -k "weather"`)

## Test Organization

### Test Markers

Tests are organized using pytest markers defined in `pytest.ini`:

- `@pytest.mark.unit` - Unit tests for isolated component testing
- `@pytest.mark.integration` - Integration tests for component interactions
- `@pytest.mark.slow` - Tests that take longer to execute
- `@pytest.mark.skip_ci` - Tests to skip in CI environments

### Test Files

#### Unit Tests (12 files, 90 tests)

| File | Tests | Description |
|------|------:|-------------|
| `test_helpers.py` | 27 | Shared helpers: date formatting, day validation, temperature labels, auth permission/premium checks, request/context accessors, Auth0 userinfo HTTP client |
| `test_weather_forecast.py` | 12 | Weather description from codes, time-of-day activity suggestions, fallback forecast structure |
| `test_elicitation.py` | 9 | Trip-extension elicitation paths: accept, reject, cancel, unsupported, errors, ValueError propagation |
| `test_travel_prompts.py` | 8 | Itinerary and weather-based activity prompt templates: structure, content, edge cases |
| `test_server.py` | 7 | Server `main()` wiring: transports (stdio, HTTP, streamable HTTP, SSE, default), provider registration, rate limiting |
| `test_models.py` | 6 | `ItineraryPreferences` model validation, defaults, day bounds, dict round-trip |
| `test_auth_additional_tools.py` | 5 | Auth-related MCP tools: GitHub/Auth0 user info, custom auth message, request/session info |
| `test_auth_provider.py` | 5 | `get_auth_provider` behavior: GitHub, Auth0, Clerk, case-insensitivity, unsupported provider errors |
| `test_itinerary_service_extra.py` | 4 | Itinerary service activity suggestions by time of day and defaults |
| `test_weather_resource.py` | 3 | Weather MCP resource handler: success, "today" shorthand, varying day counts |
| `test_itinerary_tool_handler.py` | 2 | Itinerary tool handlers call service and return expected output shapes |
| `test_travel_prompts_handler.py` | 2 | Prompt handler delegates to prompt template with correct parameters |

#### Integration Tests (2 files, 13 tests)

| File | Tests | Description |
|------|------:|-------------|
| `test_itinerary_tool.py` | 7 | End-to-end itinerary generation with elicitation, invalid dates, weather formatting, and activity suggestions |
| `test_weather_api.py` | 6 | Open-Meteo weather client with mocked HTTP: success, errors, date parsing, range validation |

## Running Tests

### Basic Commands

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with extra verbose output
uv run pytest -vv

# Run quietly (minimal output)
uv run pytest -q
```

### Run Tests by Type

```bash
# Unit tests only (fast, isolated)
uv run pytest tests/unit/ -v
uv run pytest -m unit

# Integration tests only (component interactions)
uv run pytest tests/integration/ -v
uv run pytest -m integration

# Exclude slow tests
uv run pytest -m "not slow"
```

### Run Specific Tests

```bash
# Single test file
uv run pytest tests/unit/test_models.py -v

# Multiple test files
uv run pytest tests/unit/test_models.py tests/unit/test_helpers.py -v

# Specific test class
uv run pytest tests/unit/test_models.py::TestItineraryPreferences -v

# Specific test method
uv run pytest tests/unit/test_helpers.py::TestFormatDate::test_format_date_standard -v

# Pattern matching by keyword
uv run pytest -k "elicitation" -v
uv run pytest -k "weather and not api" -v
uv run pytest -k "auth" -v
```

### Run Tests by Path Pattern

```bash
uv run pytest tests/unit/test_*.py
uv run pytest tests/**/test_weather*.py
```

## Coverage

### Coverage Configuration

The project uses a `.coveragerc` file to configure coverage collection:

```ini
[run]
omit =
    */tests/*
    */__init__.py
    */lib/*
    */prompt_templates/*
```

### Using the Test Script

The simplest way to run tests with coverage is via the test script:

```bash
# Full suite with coverage (enforces 80% minimum)
./scripts/test.sh

# Pass extra args to pytest
./scripts/test.sh -k "weather"
./scripts/test.sh tests/unit/ --maxfail=1
```

### Manual Coverage Commands

```bash
# Run tests with coverage
uv run pytest --cov=src/mcp_server

# With terminal report showing missing lines
uv run pytest --cov=src/mcp_server --cov-report=term-missing

# With HTML report (opens in browser)
uv run pytest --cov=src/mcp_server --cov-report=html
open htmlcov/index.html

# Enforce minimum coverage threshold
uv run pytest --cov=src/mcp_server --cov-fail-under=80
```

### Detailed Coverage

```bash
# Coverage for specific module
uv run pytest --cov=src/mcp_server.utils tests/unit/test_weather_forecast.py

# Generate multiple report formats
uv run pytest --cov=src/mcp_server --cov-report=html --cov-report=xml --cov-report=term-missing

# Unit tests only with coverage
uv run pytest tests/unit/ --cov=src/mcp_server --cov-report=term-missing -v
```

## Output Control

### Verbose and Debug Output

```bash
# Show test names
uv run pytest -v

# Show more details
uv run pytest -vv

# Show print statements from tests
uv run pytest -s

# Show local variables on failure
uv run pytest -l

# Show captured log messages
uv run pytest --log-cli-level=INFO
```

### Custom Log Configuration

The project's `pytest.ini` configures logging:
- Log level: INFO
- Format: `%(asctime)s [%(levelname)8s] %(message)s`
- Date format: `%Y-%m-%d %H:%M:%S`

## Debugging

### Stop on Failures

```bash
# Stop on first failure
uv run pytest -x
uv run pytest --maxfail=1

# Stop after N failures
uv run pytest --maxfail=3
```

### Rerun Failed Tests

```bash
# Run only last failed tests
uv run pytest --lf
uv run pytest --last-failed

# Run failed tests first, then continue with others
uv run pytest --ff
uv run pytest --failed-first
```

### PDB Debugging

```bash
# Drop into debugger on failure
uv run pytest --pdb

# Drop into debugger at start of each test
uv run pytest --trace

# Debug specific test with all output
uv run pytest tests/unit/test_helpers.py::TestFormatDate::test_format_date_standard -vv -s --pdb
```

## Performance

### Parallel Execution

```bash
# Auto-detect CPU count (requires pytest-xdist)
uv run pytest -n auto

# Specific number of workers
uv run pytest -n 4

# Parallel execution with coverage
uv run pytest -n auto --cov=src/mcp_server --cov-report=html
```

### Duration Reports

```bash
# Show slowest 10 tests
uv run pytest --durations=10

# Show all test durations
uv run pytest --durations=0
```

## Reporting

### Generate Reports for CI/CD

```bash
# JUnit XML report (for CI systems)
uv run pytest --junitxml=report.xml

# JSON report (requires pytest-json-report)
uv run pytest --json-report --json-report-file=report.json

# Multiple report formats
uv run pytest \
  --cov=src/mcp_server \
  --cov-report=xml \
  --cov-report=term \
  --junitxml=test-results.xml \
  -v
```

### List All Markers

```bash
# List all available markers
uv run pytest --markers

# Run with strict marker checking (enabled by default in pytest.ini)
uv run pytest --strict-markers
```

## Common Workflows

### Development Workflow

```bash
# Quick feedback: run related unit tests
uv run pytest tests/unit/test_helpers.py -v

# Debug with print statements
uv run pytest tests/unit/test_models.py -v -s

# Debug failing test with pdb
uv run pytest tests/unit/test_elicitation.py::TestElicitTripExtension::test_accept -x --pdb
```

### Pre-Commit Check

```bash
# Run all tests with coverage, fail-fast, and minimum threshold
./scripts/test.sh --maxfail=5
```

### Quick Sanity Check

```bash
# Fast unit tests only, fail fast
uv run pytest tests/unit/ -v --maxfail=1
```

### Full Quality Check

```bash
# Comprehensive test run with coverage and strict checks
uv run pytest \
  --cov=src/mcp_server \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=80 \
  --strict-markers \
  --maxfail=1 \
  -vv
```

### CI Pipeline

```bash
# Full test suite optimized for CI
uv run pytest \
  --cov=src/mcp_server \
  --cov-report=xml \
  --cov-report=term \
  --cov-fail-under=80 \
  --junitxml=test-results.xml \
  --maxfail=1 \
  -v
```

## Watch Mode

For continuous testing during development:

```bash
# Install pytest-watch
uv pip install pytest-watch

# Run in watch mode
ptw

# Watch mode with options
ptw -- -v --maxfail=1
```

## Configuration

### Pytest Configuration (pytest.ini)

The project includes a comprehensive `pytest.ini` configuration:

- **Test Discovery**: Automatically finds `test_*.py` files in `Test*` classes with `test_*` functions
- **Markers**: Custom markers for organizing tests (`unit`, `integration`, `slow`, `skip_ci`)
- **Strict Markers**: Enabled by default — unknown markers cause failures
- **Asyncio**: Auto mode for async test support
- **Warnings**: Error on warnings (except deprecated and pending deprecated)
- **Minimum Python**: 3.10
- **Default Options**: `--strict-markers --verbose --tb=short --maxfail=10 -ra`
- **Console Output**: Progress style

### Coverage Configuration (.coveragerc)

Coverage collection is configured to omit:
- Test files (`*/tests/*`)
- Init files (`*/__init__.py`)
- Library files (`*/lib/*`)
- Prompt templates (`*/prompt_templates/*`)

### Environment Variables

```bash
# Use different config file
uv run pytest -c custom_pytest.ini

# Override config options
uv run pytest -o markers="custom: custom marker description"

# Ensure module is importable
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
uv run pytest
```

## Writing Tests

### Test Structure

Tests follow the AAA pattern:
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the results

### Using Fixtures

Shared fixtures are available in:
- `tests/conftest.py` - Imports and re-exports all project fixtures
- `tests/fixtures/context.py` - Mock MCP `Context` fixture
- `tests/fixtures/weather.py` - Weather sample data and Open-Meteo-style response fixtures

### Example Test

```python
import pytest
from mcp_server.models import ItineraryPreferences

@pytest.mark.unit
class TestItineraryPreferences:
    def test_valid_preferences(self):
        """Test creating valid itinerary preferences."""
        prefs = ItineraryPreferences(
            destination="Paris",
            start_date="2024-06-01",
            end_date="2024-06-07"
        )
        assert prefs.destination == "Paris"
        assert prefs.days == 7
```

### Example Async Test

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.unit
class TestWeatherResource:
    @pytest.mark.asyncio
    async def test_get_weather_success(self, mock_context):
        """Test weather resource returns forecast data."""
        result = await get_weather(uri="weather://London/3", ctx=mock_context)
        assert "London" in result
```

## Best Practices

### Test Organization

1. **Unit Tests**: Test individual components in isolation
   - Mock external dependencies
   - Fast execution
   - High coverage of edge cases

2. **Integration Tests**: Test component interactions
   - Use real dependencies when possible
   - Test realistic scenarios
   - Verify end-to-end workflows

### Tips for Effective Testing

1. **Fast Feedback**: Start with `uv run pytest tests/unit/ -x` for quick failures
2. **Debugging**: Use `uv run pytest --pdb -x` to debug first failure immediately
3. **Coverage**: Use `./scripts/test.sh` for full coverage with 80% enforcement
4. **CI**: Use `uv run pytest --maxfail=1 -v` to fail fast in continuous integration
5. **Development**: Use `ptw` (pytest-watch) for continuous testing during coding
6. **Isolation**: Keep unit tests isolated and fast
7. **Realistic**: Make integration tests reflect real-world usage
8. **Fixtures**: Reuse test fixtures to reduce duplication
9. **Markers**: Use markers to organize and filter tests effectively
10. **Documentation**: Add docstrings to explain what each test validates

## Useful Command Combinations

```bash
# Fast unit tests with coverage
uv run pytest tests/unit/ --cov=src/mcp_server --cov-report=term-missing -v

# Integration tests with detailed output
uv run pytest tests/integration/ -vv -s

# All tests, stop on first failure, show coverage
uv run pytest --cov=src/mcp_server -x -v

# Parallel execution with coverage (faster)
uv run pytest -n auto --cov=src/mcp_server --cov-report=html

# Debug specific test with full context
uv run pytest tests/unit/test_helpers.py::TestFormatDate -vv -s --pdb

# Pre-commit: full suite with coverage threshold
./scripts/test.sh --maxfail=5

# CI-ready: comprehensive test with reports
uv run pytest --cov=src/mcp_server --cov-report=xml --junitxml=results.xml --cov-fail-under=80 -v --maxfail=1
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure src is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
uv run pytest
```

**Async Tests Not Running**
- Ensure `pytest-asyncio` is installed
- Check `asyncio_mode = auto` in `pytest.ini`

**Coverage Not Working**
- Install `pytest-cov`: `uv pip install pytest-cov`
- Verify source path: `--cov=src/mcp_server`
- Check `.coveragerc` omit patterns aren't excluding your code

**Coverage Below 80%**
- The test script enforces `--cov-fail-under=80`
- Run `./scripts/test.sh` to see which lines are missing coverage
- Check the HTML report: `open htmlcov/index.html`

**Tests Running Slowly**
- Run unit tests only: `uv run pytest tests/unit/`
- Use parallel execution: `uv run pytest -n auto`
- Profile slow tests: `uv run pytest --durations=10`

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)

## Test Statistics

Current test suite statistics:
- **Total Tests**: 103
- **Unit Tests**: 90 (12 test files)
- **Integration Tests**: 13 (2 test files)
- **Fixture Modules**: 2 modules (`context.py`, `weather.py`)
- **Test Markers**: 4 custom markers (`unit`, `integration`, `slow`, `skip_ci`)
- **Coverage Threshold**: 80% minimum

## Continuous Integration

For CI/CD pipelines, use the test script or configure directly:

```yaml
# Example GitHub Actions configuration
- name: Run Tests
  run: |
    ./scripts/test.sh
```

Or with explicit options:

```yaml
- name: Run Tests
  run: |
    uv run pytest \
      --cov=src/mcp_server \
      --cov-report=xml \
      --cov-report=term \
      --cov-fail-under=80 \
      --cov-config=.coveragerc \
      --junitxml=test-results.xml \
      --maxfail=1 \
      -v
```

This will:
- Run all 103 tests with verbose output
- Generate coverage reports (XML for CI integration, terminal for logs)
- Enforce 80% minimum coverage threshold
- Use `.coveragerc` to omit non-source files from coverage
- Create JUnit XML for test result reporting
- Fail fast on first error
