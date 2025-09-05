# Cline.bot / MCP Client Integration

This project exposes an MCP stdio server with three tools:
- ask_expert: Ask a larger LLM for targeted guidance.
- generate_docs: Produce concise development docs on a topic.
- freeform_chat: Send a freeform prompt to the configured LLM.

## Prerequisites
- Python 3.10+
- Dependencies installed: `pip install -r requirements.txt`
- MCP SDK: `pip install mcp`
- Environment variables set (see `docs/config.md`) or a local `.env`.

## Run the MCP server
- Easiest: `make dev` (auto-runs stdio server if `mcp` is available)
- Direct: `python -m src.mcp_server`

The server communicates over stdio; MCP-aware clients can launch it as a process.

## Configure in Cline (or similar MCP client)
Use a stdio “command” transport entry. Example (YAML/JSON-equivalent):

command: ["python", "-m", "src.mcp_server"]
env:
  LLM_MODEL: "gpt-5"
  LLM_BASE_URL: "https://api.openai.com/v1"
  LLM_API_KEY: "${YOUR_API_KEY}"
cwd: "${PROJECT_ROOT}"

Once registered, the following tools are available:
- ask_expert: input { question: string, context?: string }
- generate_docs: input { topic: string, goals?: string, notes?: string }
- freeform_chat: input { prompt: string, temperature?: number }

## Tips
- Run `make check` locally to lint and test before use.
- For local models/gateways, set `LLM_BASE_URL` (e.g., `http://localhost:8000/v1`) and a dummy key.
- If your client supports `.env`, place keys there and never commit real secrets.

