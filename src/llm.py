from __future__ import annotations

import os
import time
import uuid
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

# Retry/timeout configuration
DEFAULT_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "60"))
RETRY_TOTAL = int(os.getenv("LLM_RETRY_TOTAL", "3"))
RETRY_BACKOFF = float(os.getenv("LLM_RETRY_BACKOFF", "0.5"))
_retry_status = os.getenv("LLM_RETRY_STATUS", "429,500,502,503,504")
RETRY_STATUS = {int(s.strip()) for s in _retry_status.split(",") if s.strip().isdigit()}


def _post_with_retry(url: str, body: dict, headers: dict) -> requests.Response:
    backoff = max(RETRY_BACKOFF, 0.0)
    max_attempts = max(RETRY_TOTAL, 1)

    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.post(url, json=body, headers=headers, timeout=DEFAULT_TIMEOUT)
        except Exception as exc:
            timeout_type = getattr(getattr(requests, "exceptions", object()), "Timeout", ())
            if timeout_type and isinstance(exc, timeout_type) and attempt < max_attempts:
                if backoff > 0:
                    time.sleep(backoff)
                    backoff *= 2
                continue
            raise

        if not resp.ok:
            status = getattr(resp, "status_code", None)
            if status in RETRY_STATUS and attempt < max_attempts:
                retry_after = resp.headers.get("Retry-After") if hasattr(resp, "headers") else None
                try:
                    retry_after_s = float(retry_after) if retry_after is not None else 0.0
                except Exception:
                    retry_after_s = 0.0
                sleep_s = max(retry_after_s, backoff)
                if sleep_s > 0:
                    time.sleep(sleep_s)
                backoff = max(backoff * 2 if backoff > 0 else RETRY_BACKOFF * 2, 0.0)
                continue
        return resp

    # Should not reach: last attempt returns or raised
    return resp  # type: ignore[name-defined]


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
    headers.setdefault("Idempotency-Key", str(uuid.uuid4()))

    url = f"{BASE_URL}/chat/completions"
    resp = _post_with_retry(url, body, headers)
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
