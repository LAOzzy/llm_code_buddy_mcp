from __future__ import annotations

import asyncio

from .llm import chat


def _server_instructions() -> str:
    return (
        "MCP server exposing tools for expert guidance and docs generation."
    )


def build_server():
    from mcp.server import FastMCP

    mcp = FastMCP(name="llm-code-buddy-mcp", instructions=_server_instructions())

    @mcp.tool(
        name="ask_expert",
        description=(
            "Ask a larger LLM for guidance on a specific issue. "
            "Provide a precise question and optional context."
        ),
    )
    async def ask_expert(question: str, context: str | None = None) -> str:
        system = (
            "You are an expert developer assisting another agent. "
            "Provide concise, actionable guidance."
        )
        user = question + (f"\n\nContext:\n{context}" if context else "")
        # Run sync HTTP call off the event loop
        return await asyncio.to_thread(
            chat,
            [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )

    @mcp.tool(
        name="generate_docs",
        description=(
            "Generate development documentation (setup, architecture, troubleshooting). "
            "Provide topic and optional goals."
        ),
    )
    async def generate_docs(topic: str, goals: str | None = None, notes: str | None = None) -> str:
        system = "You create clear, concise development docs with actionable steps and examples."
        prompt = (
            f"Topic: {topic}\n"
            f"Goals: {goals or '-'}\n"
            f"Notes: {notes or '-'}\n\n"
            "Write a focused document (<=400 words)."
        )
        return await asyncio.to_thread(
            chat,
            [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )

    @mcp.tool(
        name="freeform_chat",
        description=(
            "Send an arbitrary prompt to the configured LLM. Use when no other tool fits."
        ),
    )
    async def freeform_chat(prompt: str, temperature: float | None = None) -> str:
        return await asyncio.to_thread(
            chat, [{"role": "user", "content": prompt}], temperature=temperature
        )

    return mcp


def run_stdio_server() -> None:
    """Start an MCP stdio server using the modern `mcp` SDK (FastMCP)."""

    try:
        mcp = build_server()
        asyncio.run(mcp.run_stdio_async())
    except Exception as exc:  # pragma: no cover
        # Fallback help if imports or runtime fail
        import sys

        print(
            "Failed to start MCP server. Ensure 'mcp' package is installed (pip install mcp).\n"
            f"Error: {exc}",
            file=sys.stderr,
        )
        raise


if __name__ == "__main__":
    run_stdio_server()
