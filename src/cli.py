from __future__ import annotations

import argparse
import sys

from .llm import chat


def cmd_ask_expert(args: argparse.Namespace) -> int:
    system = (
        "You are an expert developer assisting another agent. Provide concise, actionable guidance."
    )
    user = args.question + (f"\n\nContext:\n{args.context}" if args.context else "")
    content = chat([
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])
    print(content)
    return 0


def cmd_generate_docs(args: argparse.Namespace) -> int:
    system = "You create clear, concise development docs with actionable steps and examples."
    prompt = (
        f"Topic: {args.topic}\nGoals: {args.goals or '-'}\nNotes: {args.notes or '-'}\n\nWrite a focused document (<=400 words)."
    )
    content = chat([
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ])
    print(content)
    return 0


def cmd_freeform(args: argparse.Namespace) -> int:
    content = chat([{"role": "user", "content": args.prompt}], temperature=args.temperature)
    print(content)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="llm-buddy", description="LLM helper CLI")
    sub = p.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("ask-expert", help="Ask a larger LLM for help")
    p1.add_argument("question", help="Precise question to ask")
    p1.add_argument("--context", help="Optional context", default="")
    p1.set_defaults(func=cmd_ask_expert)

    p2 = sub.add_parser("generate-docs", help="Generate development docs")
    p2.add_argument("topic", help="Topic for the document")
    p2.add_argument("--goals", help="Goals", default="")
    p2.add_argument("--notes", help="Notes", default="")
    p2.set_defaults(func=cmd_generate_docs)

    p3 = sub.add_parser("freeform", help="Freeform prompt")
    p3.add_argument("prompt", help="Prompt text")
    p3.add_argument("--temperature", type=float, default=0.3)
    p3.set_defaults(func=cmd_freeform)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

