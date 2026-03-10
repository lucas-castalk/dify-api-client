# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync --extra dev

# Run all tests
uv run pytest -v

# Run a single test file
uv run pytest dify_client/tests/test_clientx.py -v

# Lint
ruff check .

# Format check
ruff format --check .

# Lint/format fix
ruff check --fix . && ruff format .

# Build distribution
hatch build
```

## Architecture

This is a Python SDK for the Dify Service API. The core is two parallel client classes in `dify_client/_clientx.py`:

- **`DifyClient`** — synchronous, uses `httpx.Client`
- **`AsyncDifyClient`** — asynchronous, uses `httpx.AsyncClient`; async methods are prefixed with `a` (e.g., `achat_messages`)

Both clients inherit from Pydantic `BaseModel` and share the same API surface covering: chat, completion, workflows, file uploads, conversations, feedback, and dataset/knowledge-base management.

### Key internals

- `request()` / `arequest()` — standard HTTP calls
- `request_stream()` / `arequest_stream()` — SSE streaming via `httpx-sse`
- `_prepare_url()` — constructs API URLs with template variable substitution and version-path detection
- `raise_for_status()` in `errors.py` — validates both HTTP responses and SSE error events, mapping Dify error codes to typed exceptions (all inherit from `DifyAPIError`)

### Models (`dify_client/models/`)

All request/response shapes are Pydantic models. Key base types live in `base.py` (`FileType`, `ResponseMode`, `Usage`). Stream event types are in `stream.py` (`StreamEvent` enum). Models use `exclude_none=True` when serializing for API requests.

### Adding a new endpoint

1. Add request/response models in the appropriate `models/` file (or a new one).
2. Add the method to both `DifyClient` and `AsyncDifyClient` in `_clientx.py`, following the existing pattern (blocking vs. streaming via `ResponseMode`).
3. Export new models from `dify_client/models/__init__.py` and `dify_client/__init__.py` if they are part of the public API.

## Configuration

- **Ruff** line length: 79, Google docstring convention, double quotes.
- **pytest** config in `pyproject.toml`; test paths: `dify_client/tests/`.
- Version is read dynamically from `dify_client/__init__.py`; bump it there before tagging a release.
- Publishing to PyPI is triggered automatically on GitHub release creation.
