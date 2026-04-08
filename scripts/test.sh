#!/bin/bash

set -e
set -x

# Run pytest with coverage
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
