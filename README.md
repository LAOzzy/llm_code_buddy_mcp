# LLM Code Buddy MCP

An MCP stdio server that lets agents/tools consult a larger LLM for expert guidance and generate concise development docs. Includes a small CLI for quick local checks.

## Overview
- Tools exposed over MCP:
  - ask_expert: Ask for targeted guidance with optional context.
  - generate_docs: Produce focused development docs (setup, architecture, troubleshooting).
  - freeform_chat: Send arbitrary prompts to the configured LLM.
- Stack: Python 3.10+, `requests`, `python-dotenv`, `mcp`.

## Repository Layout
- `src/`: Implementation (`llm.py`, `mcp_server.py`, `cli.py`)
- `tests/`: Unit tests (pytest-compatible)
- `scripts/`: Dev helpers for lint/format/test/dev
- `docs/`: Additional docs (`config.md`, `cline_bot_integration.md`)

## Requirements
- Python 3.10+
- Pip packages from `requirements.txt`
- An OpenAI-compatible HTTP endpoint and API key (or local gateway). See `docs/config.md`.

## Quick Start
1) Install dependencies
- `pip install -r requirements.txt`

2) Configure environment
- Copy `.env.example` to `.env` and set values:
  - `LLM_API_KEY` or `GPT5_API_KEY`
  - `LLM_MODEL` (default: `gpt-5`)
  - `LLM_BASE_URL` (default: `https://api.openai.com/v1`)

3) Smoke test the CLI
- `python -m src.cli freeform "Hello"`
  - Optionally pass `--temperature` if your provider requires a specific default.

4) Run the MCP stdio server
- `make dev` (auto-starts if `mcp` is installed)
- Or directly: `python -m src.mcp_server`

## Using with MCP Clients
Point your client at a stdio command. Example configuration (YAML/JSON-equivalent):

command: ["python", "-m", "src.mcp_server"]
env:
  LLM_MODEL: "gpt-5"
  LLM_BASE_URL: "https://api.openai.com/v1"
  LLM_API_KEY: "${YOUR_API_KEY}"
cwd: "${PROJECT_ROOT}"

- Tools available:
  - ask_expert: `{ question: string, context?: string }`
  - generate_docs: `{ topic: string, goals?: string, notes?: string }`
  - freeform_chat: `{ prompt: string, temperature?: number }`
- See `docs/cline_bot_integration.md` for more details and tips.

## Development
- Run tests: `make test`
- Lint: `make lint`
- Format: `make fmt`
- All checks: `make check`

## Deployment Options
- Client-managed (recommended): Most MCP clients launch this server directly via the command shown above—no separate deployment required.
- Systemd service (example):

[Unit]
Description=LLM Code Buddy MCP
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/llm-code-buddy-mcp
Environment=LLM_MODEL=gpt-5
Environment=LLM_BASE_URL=https://api.openai.com/v1
Environment=LLM_API_KEY=YOUR_KEY
ExecStart=/usr/bin/python -m src.mcp_server
Restart=on-failure

[Install]
WantedBy=multi-user.target

- Docker (included):
  - Build: `docker build -t llm-code-buddy-mcp .`
  - Run (stdio MCP):
    - `docker run --rm -i \`
      `-e LLM_MODEL=gpt-5 \`
      `-e LLM_BASE_URL=https://api.openai.com/v1 \`
      `-e LLM_API_KEY=YOUR_KEY \`
      `llm-code-buddy-mcp`
    - Note the `-i` flag keeps STDIN open for MCP stdio.
  - Use with clients: Configure a command that launches Docker with `-i` or run the container as a long‑lived service and connect via your client’s process runner tools.

Note: Adjust Python version, paths, and env handling for your environment.

### Docker Helpers
- `scripts/docker-run`: Runs the MCP stdio server in Docker, using `.env` automatically if present.
  - Build + run: `scripts/docker-run --build`
  - Custom image name: `scripts/docker-run --image my-mcp`
- `scripts/docker-smoke`: Executes a CLI smoke test in Docker.
  - Example: `scripts/docker-smoke --build "Hello from Docker"`
  - Temperature (if required by provider): `scripts/docker-smoke --temperature 1.0 "Hello"`
- `scripts/docker-run-detached`: Starts the MCP server in detached mode and follows logs.
  - Build + start: `scripts/docker-run-detached --build`
  - Custom image/name: `scripts/docker-run-detached --image my-mcp --name mcp-demo`
  - Stop: Ctrl+C (auto-removes) or `docker rm -f mcp-demo`
- Compose: `docker-compose.yml` provided for convenience.
  - Build and run interactively: `docker compose run --rm --service-ports mcp`
  - Note: Keep STDIN open when your client launches the service (compose sets `stdin_open: true`).

## Configuration
- Required: `LLM_API_KEY` or `GPT5_API_KEY`
- Optional: `LLM_MODEL` (default `gpt-5`), `LLM_BASE_URL` (default `https://api.openai.com/v1`)
- The CLI and server load `.env` via `python-dotenv` if present.
- Temperature is omitted by default; pass it explicitly if the provider requires it.

## Troubleshooting
- 400 invalid_request_error on temperature: Some models only accept the default value; pass `--temperature 1.0` or omit it.
- Connectivity errors: Check `LLM_BASE_URL`, network, and key validity.
- Import issues in tests: Ensure `make test` is used (adds project root to `PYTHONPATH`).
