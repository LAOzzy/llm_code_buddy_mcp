# TODO

- [ ] Install Python dependencies and MCP SDK
  - Command: `pip install -r requirements.txt`
- [ ] Verify MCP imports and run server
  - Command: `make dev` (expects `mcp` package)
- [ ] Configure LLM backend
  - Set `LLM_MODEL=gpt-5`, `LLM_API_KEY` or `GPT5_API_KEY`, and optionally `LLM_BASE_URL`
- [ ] Connectivity check and smoke test
  - Command: `python -m src.cli freeform "Hello"`
- [ ] Add unit tests for `src/llm.py`
  - Mock HTTP and test error paths/timeouts
- [ ] Document cline.bot integration steps
  - How to register this MCP server and use tools
- [ ] Optional: CI workflow (lint + test)
  - GitHub Actions: run `make check`
- [ ] Optional tools: `summarize_logs`, `troubleshoot_error`, `gen_tests`
  - Tailored prompts for common agent needs
