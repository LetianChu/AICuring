import json
import http.client
from io import BytesIO
from urllib.error import HTTPError

from aicure_benchmark.adapters.openrouter import OpenRouterAdapter, load_openrouter_api_key
from aicure_benchmark.models.common import SamplingProfile


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_load_openrouter_api_key_reads_dotenv_when_env_missing(tmp_path, monkeypatch) -> None:
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("OPENROUTER_API_KEY=test-dotenv-key\n", encoding="utf-8")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    assert load_openrouter_api_key(dotenv_path=dotenv_path) == "test-dotenv-key"


def test_openrouter_adapter_returns_normalized_response(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request, timeout: int):
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        captured["headers"] = dict(request.header_items())
        return _FakeResponse(
            {
                "id": "gen-test",
                "model": "stepfun/step-3.5-flash:free",
                "provider": "StepFun",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "我在这里陪你。",
                            "reasoning": "hidden chain",
                        },
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 12,
                    "total_tokens": 22,
                    "cost": 0,
                },
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.openrouter.urllib.request.urlopen", fake_urlopen)

    adapter = OpenRouterAdapter(
        model_name="stepfun/step-3.5-flash:free",
        api_key="test-api-key",
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "今晚陪我聊会儿。"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    payload = captured["payload"]
    assert payload["model"] == "stepfun/step-3.5-flash:free"
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][1]["content"] == "今晚陪我聊会儿。"
    assert payload["max_tokens"] == 512
    assert response.text == "我在这里陪你。"
    assert response.finish_reason == "stop"
    assert response.raw_payload["usage"]["cost"] == 0


def test_openrouter_adapter_retries_transient_rate_limits(monkeypatch) -> None:
    attempts = {"count": 0}

    def fake_urlopen(request, timeout: int):
        attempts["count"] += 1
        if attempts["count"] < 5:
            raise HTTPError(
                request.full_url,
                429,
                "Too Many Requests",
                hdrs=None,
                fp=BytesIO(
                    b'{"error":{"message":"Provider returned error","code":429}}'
                ),
            )
        return _FakeResponse(
            {
                "id": "gen-after-retry",
                "model": "stepfun/step-3.5-flash:free",
                "provider": "StepFun",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "重试后成功。",
                        },
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 12,
                    "total_tokens": 22,
                    "cost": 0,
                },
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.openrouter.time.sleep", lambda *_args: None)
    monkeypatch.setattr("aicure_benchmark.adapters.openrouter.urllib.request.urlopen", fake_urlopen)

    adapter = OpenRouterAdapter(
        model_name="stepfun/step-3.5-flash:free",
        api_key="test-api-key",
        retry_delays_s=(0, 0, 0, 0, 0),
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "今晚陪我聊会儿。"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert attempts["count"] == 5
    assert response.text == "重试后成功。"


def test_openrouter_adapter_retries_remote_disconnects(monkeypatch) -> None:
    attempts = {"count": 0}

    def fake_urlopen(request, timeout: int):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise http.client.RemoteDisconnected("Remote end closed connection without response")
        return _FakeResponse(
            {
                "id": "gen-after-disconnect",
                "model": "stepfun/step-3.5-flash:free",
                "provider": "StepFun",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "断线后成功。",
                        },
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 12,
                    "total_tokens": 22,
                    "cost": 0,
                },
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.openrouter.time.sleep", lambda *_args: None)
    monkeypatch.setattr("aicure_benchmark.adapters.openrouter.urllib.request.urlopen", fake_urlopen)

    adapter = OpenRouterAdapter(
        model_name="stepfun/step-3.5-flash:free",
        api_key="test-api-key",
        retry_delays_s=(0, 0, 0),
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "今晚陪我聊会儿。"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert attempts["count"] == 3
    assert response.text == "断线后成功。"
