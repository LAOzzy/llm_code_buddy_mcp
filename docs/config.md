# Configuration

Set environment variables (or a `.env` loaded by your runner) to configure the LLM backend and MCP server.

Required
- `LLM_API_KEY` or `GPT5_API_KEY`: API key for the chosen provider.

Optional
- `LLM_MODEL`: Model name. Default: `gpt-5`.
- `LLM_BASE_URL`: OpenAI-compatible API base URL. Default: `https://api.openai.com/v1`.

Examples
- OpenAI-compatible (default):
  - `LLM_MODEL=gpt-5`
  - `LLM_BASE_URL=https://api.openai.com/v1`
  - `LLM_API_KEY=sk-...`
- Local OpenAI-compatible gateway (e.g., LM Studio, vLLM):
  - `LLM_MODEL=your-local-model`
  - `LLM_BASE_URL=http://localhost:8000/v1`
  - `LLM_API_KEY=local-dev-key`

Tips
- Rotate keys regularly and never commit real keys. Use `.env.example` as a template.
- Use `make dev` to run the MCP server if the MCP SDK is installed; otherwise, use `python -m src.cli` commands.
