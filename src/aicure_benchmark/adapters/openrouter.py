import http.client
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from aicure_benchmark.adapters.base import AdapterResponse
from aicure_benchmark.models.common import SamplingProfile


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"


def load_openrouter_api_key(
    *,
    dotenv_path: Path = Path(".env"),
) -> Optional[str]:
    env_value = os.environ.get(OPENROUTER_API_KEY_ENV)
    if env_value:
        return env_value

    if not dotenv_path.exists():
        return None

    for line in dotenv_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() != OPENROUTER_API_KEY_ENV:
            continue
        cleaned = value.strip().strip('"').strip("'")
        if cleaned:
            return cleaned

    return None


class OpenRouterAdapter:
    adapter_name = "openrouter"

    def __init__(
        self,
        *,
        model_name: str,
        api_key: Optional[str] = None,
        api_url: str = OPENROUTER_API_URL,
        request_timeout_s: int = 120,
        retry_delays_s: tuple[int, ...] = (0, 2, 5, 10, 20, 40, 60, 90),
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key or load_openrouter_api_key()
        self.api_url = api_url
        self.request_timeout_s = request_timeout_s
        self.retry_delays_s = retry_delays_s

        if not self.api_key:
            raise ValueError(f"{OPENROUTER_API_KEY_ENV} is required for OpenRouter runs")

    def generate(
        self,
        *,
        persona_summary: str,
        messages: list[dict[str, str]],
        sampling_profile: SamplingProfile,
    ) -> AdapterResponse:
        request_messages = [
            {
                "role": "system",
                "content": (
                    "You are roleplaying a companion persona. "
                    "Stay in character, reply naturally in the same language as the user, "
                    "and do not mention being an AI assistant unless absolutely necessary. "
                    f"{persona_summary}"
                ),
            }
        ]
        request_messages.extend(messages)

        payload = json.dumps(
            {
                "model": self.model_name,
                "messages": request_messages,
                "temperature": sampling_profile.temperature,
                "top_p": sampling_profile.top_p,
                "max_tokens": sampling_profile.max_tokens,
            }
        ).encode("utf-8")

        last_error = None
        for delay in self.retry_delays_s:
            if delay:
                time.sleep(delay)

            request = urllib.request.Request(
                self.api_url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            try:
                with urllib.request.urlopen(request, timeout=self.request_timeout_s) as response:
                    response_payload = json.loads(response.read().decode("utf-8"))
                    choice = (response_payload.get("choices") or [{}])[0]
                    message = choice.get("message") or {}
                    content = message.get("content") or ""
                    event_tags = []
                    if not content.strip():
                        event_tags.append("empty_response")
                    return AdapterResponse(
                        text=content,
                        finish_reason=choice.get("finish_reason") or "stop",
                        event_tags=event_tags,
                        raw_payload={
                            "id": response_payload.get("id"),
                            "model": response_payload.get("model"),
                            "provider": response_payload.get("provider"),
                            "usage": response_payload.get("usage"),
                            "reasoning_len": len(message.get("reasoning") or ""),
                        },
                    )
            except urllib.error.HTTPError as exc:
                raw = exc.read().decode("utf-8", errors="replace")
                last_error = f"http_{exc.code}: {raw[:500]}"
                if exc.code in {429, 500, 502, 503, 504}:
                    continue
                raise RuntimeError(last_error) from exc
            except http.client.RemoteDisconnected as exc:
                last_error = str(exc)
                continue
            except urllib.error.URLError as exc:
                last_error = str(exc)
                continue

        raise RuntimeError(last_error or "OpenRouter request failed")
