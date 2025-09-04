# Repository Guidelines

## Project Structure & Module Organization
- Keep code in `src/` and tests in `tests/`. Scripts and local tooling belong in `scripts/`. Docs can go in `docs/`.
- Mirror module paths between `src/` and `tests/` (e.g., `src/foo/bar.py` → `tests/foo/test_bar.py`).
- Assets, fixtures, and sample data live under `assets/` or `tests/fixtures/` as appropriate.

Example layout:
```
/ src/            # implementation
/ tests/          # unit/integration tests
/ scripts/        # dev/build/test wrappers
/ docs/           # architecture and notes
```

## Build, Test, and Development Commands
- Prefer Make targets or script wrappers when available:
  - `make dev` – start a local dev workflow.
  - `make test` – run the full test suite.
  - `make fmt` / `make lint` – format and lint.
- If no Makefile exists, use scripts instead:
  - `./scripts/dev`, `./scripts/test`, `./scripts/fmt`, `./scripts/lint`.

## Coding Style & Naming Conventions
- Indentation: 4 spaces for Python; 2 spaces for JS/TS.
- Names: `snake_case` for files and functions (Python), `camelCase` for variables/functions and `PascalCase` for classes.
- Line length target: 100 chars.
- Formatting/Linting (use if present): Python → Black + Ruff; JS/TS → Prettier + ESLint.
- Keep modules small and focused; avoid circular imports.

## Testing Guidelines
- Frameworks: prefer `pytest` (Python) or `jest/vitest` (JS/TS), depending on stack.
- Name tests clearly: `tests/foo/test_bar.py` or `foo/bar.spec.ts`.
- Aim for meaningful coverage of public interfaces and edge cases. Run locally with `make test` or `./scripts/test`.

## Commit & Pull Request Guidelines
- Use Conventional Commits where possible (e.g., `feat: add agent registry`).
- Commit messages: imperative mood, concise summary, optional body with rationale.
- PRs should include: clear description, linked issues, before/after notes, and tests for new behavior.
- Keep diffs focused; separate refactors from features/bugfixes.

## Security & Configuration Tips
- Never commit secrets; use `.env` with a checked-in `.env.example`.
- Document required environment variables in `docs/config.md`.
- Prefer least-privilege tokens and rotate credentials.

## Agent-Specific Instructions (Codex CLI)
- Keep patches minimal and targeted; use `apply_patch` and avoid unrelated changes.
- Add a brief preamble before running commands; use `update_plan` for multi-step work.
- Respect sandboxing; avoid network access unless explicitly approved.
