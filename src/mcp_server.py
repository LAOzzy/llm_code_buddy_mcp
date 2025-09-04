from __future__ import annotations

import sys
from typing import Any, Dict

from .llm import chat


def _missing_mcp_server() -> None:
    print(
        "MCP server not available: Python MCP SDK not installed.\n"
        "Install the SDK:\n"
        "  pip install mcp\n",
        file=sys.stderr,
    )


def run_stdio_server() -> None:
    """Start an MCP stdio server exposing tools for expert help and docs.

    Uses the 'mcp' Python package. Ensure it's installed (pip install mcp).
    """

    try:
        from mcp.server import Server  # type: ignore
        from mcp.transport.stdio import StdioServerTransport  # type: ignore
    except Exception:  # pragma: no cover
        _missing_mcp_server()
        sys.exit(2)

    server = Server({"name": "llm-code-buddy-mcp", "version": "0.1.0"}, {})

    @server.tool(
        "ask_expert",
        description=(
            "Ask a larger LLM for guidance on a specific issue."
            " Provide a precise question and optional context."
        ),
        input_schema={
            "type": "object",
            "properties": {"question": {"type": "string"}, "context": {"type": "string"}},
            "required": ["question"],
            "additionalProperties": False,
        },
    )
    def ask_expert(input: Dict[str, Any]) -> Dict[str, Any]:
        question = input.get("question", "").strip()
        context = input.get("context", "").strip()
        system = (
            "You are an expert developer assisting another agent. Provide concise, actionable guidance."
        )
        user = question + (f"\n\nContext:\n{context}" if context else "")
        content = chat([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
        return {"content": [{"type": "text", "text": content}]}

    @server.tool(
        "generate_docs",
        description=(
            "Generate development documentation (setup, architecture, troubleshooting)."
            " Provide topic and optional goals."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "goals": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["topic"],
            "additionalProperties": False,
        },
    )
    def generate_docs(input: Dict[str, Any]) -> Dict[str, Any]:
        topic = input.get("topic", "")
        goals = input.get("goals", "-")
        notes = input.get("notes", "-")
        system = "You create clear, concise development docs with actionable steps and examples."
        prompt = (
            f"Topic: {topic}\nGoals: {goals}\nNotes: {notes}\n\nWrite a focused document (<=400 words)."
        )
        content = chat([
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ])
        return {"content": [{"type": "text", "text": content}]}

    @server.tool(
        "freeform_chat",
        description=("Send an arbitrary prompt to the configured LLM. Use when no other tool fits."),
        input_schema={
            "type": "object",
            "properties": {"prompt": {"type": "string"}, "temperature": {"type": "number"}},
            "required": ["prompt"],
            "additionalProperties": False,
        },
    )
    def freeform_chat(input: Dict[str, Any]) -> Dict[str, Any]:
        prompt = input.get("prompt", "")
        temperature = input.get("temperature")
        content = chat([{"role": "user", "content": prompt}], temperature=temperature)
        return {"content": [{"type": "text", "text": content}]}

    transport = StdioServerTransport()
    server.connect(transport)


if __name__ == "__main__":
    run_stdio_server()
