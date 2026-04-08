# Linting & Formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) for both linting and code formatting, managed through [pre-commit](https://pre-commit.com/) hooks and CLI scripts.

## Tools

| Tool | Version | Purpose |
|------|---------|---------|
| Ruff | v0.15.9 | Linter + formatter (replaces flake8, isort, black) |
| pre-commit | ≥4.5.1 | Git hook runner |

## Quick Start

```bash
# One-time setup: install pre-commit git hooks
uv run pre-commit-install

# Run linting + formatting on all files (via pre-commit)
uv run lint

# Or run linting and formatting individually
./scripts/lint.sh      # ruff check . --fix
./scripts/format.sh    # ruff format .
```

## How It Works

### Pre-commit Hooks (`.pre-commit-config.yaml`)

Pre-commit runs automatically on every `git commit` against staged files. Two hooks are configured:

1. **ruff** — lints and auto-fixes violations (`--fix`)
2. **ruff-format** — formats code (quote style, indentation, line length)

### CLI Commands (`pyproject.toml` scripts)

| Command | What it runs |
|---------|-------------|
| `uv run lint` | `pre-commit run --all-files` (lint + format, all files) |
| `uv run pre-commit-install` | `pre-commit install` (set up git hooks) |

### Shell Scripts (`scripts/`)

| Script | Command | Use case |
|--------|---------|----------|
| `scripts/lint.sh` | `uv run ruff check . --fix` | Lint only, no formatting |
| `scripts/format.sh` | `uv run ruff format .` | Format only, no linting |

> **Note:** `uv run lint` runs both linting and formatting via pre-commit. The shell scripts run them independently.

## Ruff Configuration (`ruff.toml`)

### General

| Setting | Value |
|---------|-------|
| Line length | 100 |
| Indent width | 4 spaces |
| Target Python | 3.12+ |
| Quote style | Double (`"`) |
| Indent style | Spaces |

### Rule Selection

All rules are enabled (`select = ["ALL"]`) with specific exclusions:

| Rule | Description |
|------|-------------|
| D203 | Blank line before class docstring |
| D212 | Multi-line docstring first-line summary |
| D100 | Missing module docstring |
| PLR0913 | Too many function arguments |
| I001 | Unsorted imports |
| TC002 | Third-party import grouping |
| ARG001, ARG002 | Unused arguments |
| TD002, TD003 | TODO author/issue requirements |
| FIX002 | TODO resolution reminder |
| COM812 | Missing trailing comma |
| N805 | `self` first-argument naming |
| ERA001 | Commented-out code |
| FAST002 | FastAPI dependency annotation |
| B008 | Function call in argument defaults |
| RET504 | Unnecessary assignment before return |
| F841 | Unused variable |
| S603 | Subprocess call with non-literal input |

### Per-File Ignores

| Pattern | Ignored Rules | Reason |
|---------|--------------|--------|
| `__init__.py` | F401 | Re-exports are expected in init files |
| `tests/**/*.py` | S101, PLR2004 | `assert` and magic values are normal in tests |
| `src/mcp_server/lib/httpx_client.py` | ANN401 | `Any` types needed for pass-through wrapper |

### Excluded Paths

The following directories are excluded from linting entirely:

`.venv`, `venv`, `scripts`, `tests`, `alembic`, `build`, `dist`, `node_modules`, and common VCS/tool directories.

## Adding a `noqa` Comment

To suppress a specific rule on a single line, add `# noqa: <RULE>` to that line:

```python
print("debug")  # noqa: T201
```

> **Avoid using `# noqa: S603`** on individual lines — it conflicts with `--fix` (ruff removes the directive then re-flags the error). S603 is ignored globally in `ruff.toml` instead.
