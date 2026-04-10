import http.client
import json
from io import BytesIO
from urllib.error import HTTPError

from aicure_benchmark.adapters.aihubmix import AIHubMixAdapter, load_aihubmix_api_key
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


def test_load_aihubmix_api_key_reads_dotenv_when_env_missing(tmp_path, monkeypatch) -> None:
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("AIHUBMIX_API_KEY=test-aihubmix-key\n", encoding="utf-8")
    monkeypatch.delenv("AIHUBMIX_API_KEY", raising=False)

    assert load_aihubmix_api_key(dotenv_path=dotenv_path) == "test-aihubmix-key"


def test_aihubmix_adapter_returns_normalized_response(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request, timeout: int):
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        captured["headers"] = dict(request.header_items())
        captured["url"] = request.full_url
        return _FakeResponse(
            {
                "id": "gen-test",
                "model": "coding-minimax-m2.7-free",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "I am fine.",
                        },
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 12,
                    "total_tokens": 22,
                },
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.aihubmix.urllib.request.urlopen", fake_urlopen)

    adapter = AIHubMixAdapter(
        model_name="coding-minimax-m2.7-free",
        api_key="test-api-key",
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert captured["url"] == "https://aihubmix.com/v1/chat/completions"
    assert captured["payload"]["model"] == "coding-minimax-m2.7-free"
    assert response.text == "I am fine."
    assert response.finish_reason == "stop"


def test_aihubmix_adapter_strips_think_blocks_from_content(monkeypatch) -> None:
    def fake_urlopen(request, timeout: int):
        return _FakeResponse(
            {
                "id": "gen-think",
                "model": "coding-minimax-m2.7-free",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "<think>internal reasoning</think>\n\nHello there",
                        },
                    }
                ],
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.aihubmix.urllib.request.urlopen", fake_urlopen)

    adapter = AIHubMixAdapter(
        model_name="coding-minimax-m2.7-free",
        api_key="test-api-key",
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "Hello"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert response.text == "Hello there"


def test_aihubmix_adapter_retries_transient_rate_limits(monkeypatch) -> None:
    attempts = {"count": 0}

    def fake_urlopen(request, timeout: int):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise HTTPError(
                request.full_url,
                429,
                "Too Many Requests",
                hdrs=None,
                fp=BytesIO(b'{"error":{"message":"Rate limit"}}'),
            )
        return _FakeResponse(
            {
                "id": "gen-after-retry",
                "model": "coding-minimax-m2.7-free",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "Retry success.",
                        },
                    }
                ],
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.aihubmix.time.sleep", lambda *_args: None)
    monkeypatch.setattr("aicure_benchmark.adapters.aihubmix.urllib.request.urlopen", fake_urlopen)

    adapter = AIHubMixAdapter(
        model_name="coding-minimax-m2.7-free",
        api_key="test-api-key",
        retry_delays_s=(0, 0, 0),
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "Hello"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert attempts["count"] == 3
    assert response.text == "Retry success."


def test_aihubmix_adapter_retries_remote_disconnects(monkeypatch) -> None:
    attempts = {"count": 0}

    def fake_urlopen(request, timeout: int):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise http.client.RemoteDisconnected("Remote end closed connection without response")
        return _FakeResponse(
            {
                "id": "gen-after-disconnect",
                "model": "coding-minimax-m2.7-free",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "role": "assistant",
                            "content": "Disconnect retry success.",
                        },
                    }
                ],
            }
        )

    monkeypatch.setattr("aicure_benchmark.adapters.aihubmix.time.sleep", lambda *_args: None)
    monkeypatch.setattr("aicure_benchmark.adapters.aihubmix.urllib.request.urlopen", fake_urlopen)

    adapter = AIHubMixAdapter(
        model_name="coding-minimax-m2.7-free",
        api_key="test-api-key",
        retry_delays_s=(0, 0, 0),
    )
    response = adapter.generate(
        persona_summary="Playful late-night girlfriend.",
        messages=[{"role": "user", "content": "Hello"}],
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )

    assert attempts["count"] == 3
    assert response.text == "Disconnect retry success."
