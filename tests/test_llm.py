import importlib
import sys
from types import SimpleNamespace
from typing import Any


def import_llm_with(fake_requests: Any, fake_dotenv: Any):
    # Inject fakes before importing the module under test
    sys.modules['requests'] = fake_requests
    sys.modules['dotenv'] = fake_dotenv
    # Remove cached module if previously imported
    sys.modules.pop('src.llm', None)
    mod = importlib.import_module('src.llm')
    return mod


class FakeResponse:
    def __init__(
        self,
        ok: bool = True,
        data: dict | None = None,
        status_code: int = 200,
        reason: str = 'OK',
        text: str = '',
    ) -> None:
        self.ok = ok
        self._data = data or {}
        self.status_code = status_code
        self.reason = reason
        self.text = text

    def json(self):
        return self._data


def test_chat_success_returns_content():
    def post(url, json=None, headers=None, timeout=None):  # noqa: A002 - shadowing json param ok here
        assert url.endswith('/chat/completions')
        # Validate minimal payload
        assert isinstance(json, dict)
        assert 'model' in json and 'messages' in json
        data = {
            'choices': [
                {'message': {'content': 'Hello from fake model'}}
            ]
        }
        return FakeResponse(ok=True, data=data)

    FakeRequests = SimpleNamespace(post=post)
    FakeDotenv = SimpleNamespace(load_dotenv=lambda: None)

    llm = import_llm_with(FakeRequests, FakeDotenv)
    out = llm.chat([{"role": "user", "content": "hi"}])
    assert isinstance(out, str)
    assert 'Hello from fake model' in out


def test_chat_raises_on_http_error():
    def post(url, json=None, headers=None, timeout=None):
        return FakeResponse(
            ok=False,
            data={'error': 'bad'},
            status_code=500,
            reason='Server Error',
            text='oops',
        )

    FakeRequests = SimpleNamespace(post=post)
    FakeDotenv = SimpleNamespace(load_dotenv=lambda: None)

    llm = import_llm_with(FakeRequests, FakeDotenv)
    try:
        llm.chat([{"role": "user", "content": "hi"}])
        raise AssertionError('Expected RuntimeError')
    except RuntimeError as e:
        assert 'LLM request failed' in str(e)


def test_chat_raises_on_empty_content():
    def post(url, json=None, headers=None, timeout=None):
        return FakeResponse(ok=True, data={'choices': [{'message': {}}]})

    FakeRequests = SimpleNamespace(post=post)
    FakeDotenv = SimpleNamespace(load_dotenv=lambda: None)

    llm = import_llm_with(FakeRequests, FakeDotenv)
    try:
        llm.chat([{"role": "user", "content": "hi"}])
        raise AssertionError('Expected RuntimeError')
    except RuntimeError as e:
        assert 'empty' in str(e).lower()


def test_chat_propagates_timeout_exception():
    class Timeout(Exception):
        pass

    def post(url, json=None, headers=None, timeout=None):
        raise Timeout('request timed out')

    FakeRequests = SimpleNamespace(post=post, exceptions=SimpleNamespace(Timeout=Timeout))
    FakeDotenv = SimpleNamespace(load_dotenv=lambda: None)

    llm = import_llm_with(FakeRequests, FakeDotenv)
    try:
        llm.chat([{"role": "user", "content": "hi"}], temperature=0.1)
        raise AssertionError('Expected Timeout')
    except Timeout:
        pass
