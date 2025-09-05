from __future__ import annotations

import os
from typing import Literal, TypedDict

import requests
from dotenv import load_dotenv


class ChatMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


load_dotenv()

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-5")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
API_KEY = os.getenv("LLM_API_KEY") or os.getenv("GPT5_API_KEY") or ""


def chat(messages: list[ChatMessage], temperature: float | None = None) -> str:
    """Send a chat request to an OpenAI-compatible API and return text content.

    Environment variables:
    - LLM_MODEL (default: gpt-5)
    - LLM_BASE_URL (default: https://api.openai.com/v1)
    - LLM_API_KEY or GPT5_API_KEY
    """

    body: dict = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "stream": False,
    }
    if temperature is not None:
        body["temperature"] = temperature

    headers = {"content-type": "application/json"}
    if API_KEY:
        headers["authorization"] = f"Bearer {API_KEY}"

    url = f"{BASE_URL}/chat/completions"
    resp = requests.post(url, json=body, headers=headers, timeout=60)
    if not resp.ok:
        raise RuntimeError(
            f"LLM request failed: {resp.status_code} {resp.reason} - {resp.text[:400]}"
        )
    data = resp.json()
    content = (
        (data.get("choices") or [{}])[0]
        .get("message", {})
        .get("content")
    )
    if not content:
        raise RuntimeError("LLM returned empty response")
    return str(content)
