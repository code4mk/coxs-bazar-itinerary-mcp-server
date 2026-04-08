"""CLI commands for the MCP server project."""

import subprocess
import sys
from pathlib import Path


def dev() -> None:
    """Run the MCP server in development mode with auto-reload."""
    project_root = Path(__file__).parent.parent.parent
    script = project_root / "scripts" / "run-mcp-server.sh"

    print("Starting MCP server in dev mode (with auto-reload)...")  # noqa: T201
    try:
        subprocess.run(
            ["bash", str(script)],  # noqa: S607
            cwd=project_root,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        print(  # noqa: T201
            "ERROR: 'bash' or script not found. Ensure scripts/run-mcp-server.sh exists.",
            file=sys.stderr,
        )
        sys.exit(1)


def lint() -> None:
    """Run pre-commit hooks on all files."""
    project_root = Path(__file__).parent.parent.parent

    print("Running pre-commit on all files...")  # noqa: T201
    try:
        subprocess.run(
            ["uv", "run", "pre-commit", "run", "--all-files"],  # noqa: S607
            cwd=project_root,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        print(  # noqa: T201
            "ERROR: 'uv' command not found. Please ensure uv is installed.",
            file=sys.stderr,
        )
        sys.exit(1)


def pre_commit_install() -> None:
    """Install pre-commit hooks into the git repository."""
    project_root = Path(__file__).parent.parent.parent

    print("Installing pre-commit hooks...")  # noqa: T201
    try:
        subprocess.run(
            ["uv", "run", "pre-commit", "install"],  # noqa: S607
            cwd=project_root,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        sys.exit(1)
    except FileNotFoundError:
        print(  # noqa: T201
            "ERROR: 'uv' command not found. Please ensure uv is installed.",
            file=sys.stderr,
        )
        sys.exit(1)
