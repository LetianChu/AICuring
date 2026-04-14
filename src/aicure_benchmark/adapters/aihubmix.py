import http.client
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from aicure_benchmark.adapters.base import AdapterResponse
from aicure_benchmark.models.common import SamplingProfile


AIHUBMIX_API_KEY_ENV = "AIHUBMIX_API_KEY"
AIHUBMIX_BASE_URL_ENV = "AIHUBMIX_BASE_URL"
DEFAULT_AIHUBMIX_API_URL = "https://aihubmix.com/v1/chat/completions"


def _load_env_value(
    env_name: str,
    *,
    dotenv_path: Path,
) -> Optional[str]:
    env_value = os.environ.get(env_name)
    if env_value:
        return env_value

    if not dotenv_path.exists():
        return None

    for line in dotenv_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() != env_name:
            continue
        cleaned = value.strip().strip('"').strip("'")
        if cleaned:
            return cleaned

    return None


def load_aihubmix_api_key(
    *,
    dotenv_path: Path = Path(".env"),
) -> Optional[str]:
    return _load_env_value(AIHUBMIX_API_KEY_ENV, dotenv_path=dotenv_path)


def load_aihubmix_api_url(
    *,
    dotenv_path: Path = Path(".env"),
) -> str:
    raw_base_url = _load_env_value(AIHUBMIX_BASE_URL_ENV, dotenv_path=dotenv_path)
    if not raw_base_url:
        return DEFAULT_AIHUBMIX_API_URL

    base_url = raw_base_url.rstrip("/")
    if base_url.endswith("/chat/completions"):
        return base_url
    return f"{base_url}/chat/completions"


def _extract_message_text(message: dict) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "text" and item.get("text"):
                text_parts.append(str(item["text"]))
        return "\n".join(text_parts)
    return ""


def _strip_think_blocks(text: str) -> str:
    cleaned = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL)
    return cleaned.strip()


def _uses_responses_api(model_name: str) -> bool:
    return model_name.startswith("gpt-5")


def _resolve_request_url(*, api_url: str, use_responses_api: bool) -> str:
    base_url = api_url.rstrip("/")
    if use_responses_api:
        if base_url.endswith("/chat/completions"):
            return f"{base_url[:-len('/chat/completions')]}/responses"
        if base_url.endswith("/responses"):
            return base_url
        return f"{base_url}/responses"

    return base_url


def _extract_responses_text(response_payload: dict) -> str:
    text_parts: list[str] = []
    for output_item in response_payload.get("output") or []:
        if not isinstance(output_item, dict):
            continue
        for content_item in output_item.get("content") or []:
            if not isinstance(content_item, dict):
                continue
            if content_item.get("type") == "output_text" and content_item.get("text"):
                text_parts.append(str(content_item["text"]))
    return "\n".join(text_parts)


class AIHubMixAdapter:
    adapter_name = "aihubmix"

    def __init__(
        self,
        *,
        model_name: str,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        request_timeout_s: int = 120,
        retry_delays_s: tuple[int, ...] = (0, 2, 5, 10, 20, 40, 60, 90),
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key or load_aihubmix_api_key()
        self.api_url = api_url or load_aihubmix_api_url()
        self.request_timeout_s = request_timeout_s
        self.retry_delays_s = retry_delays_s

        if not self.api_key:
            raise ValueError(f"{AIHUBMIX_API_KEY_ENV} is required for AIHubMix runs")

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

        use_responses_api = _uses_responses_api(self.model_name)
        request_url = _resolve_request_url(
            api_url=self.api_url,
            use_responses_api=use_responses_api,
        )

        payload_dict = {
            "model": self.model_name,
            "temperature": sampling_profile.temperature,
            "top_p": sampling_profile.top_p,
        }
        if use_responses_api:
            payload_dict.update(
                {
                    "input": request_messages,
                    "max_output_tokens": sampling_profile.max_tokens,
                }
            )
        else:
            payload_dict.update(
                {
                    "messages": request_messages,
                    "max_tokens": sampling_profile.max_tokens,
                }
            )

        payload = json.dumps(payload_dict).encode("utf-8")

        last_error = None
        for delay in self.retry_delays_s:
            if delay:
                time.sleep(delay)

            request = urllib.request.Request(
                request_url,
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
                    if use_responses_api:
                        content = _strip_think_blocks(
                            _extract_responses_text(response_payload)
                        )
                        finish_reason = response_payload.get("status") or "completed"
                        reasoning_len = 0
                    else:
                        choice = (response_payload.get("choices") or [{}])[0]
                        message = choice.get("message") or {}
                        content = _strip_think_blocks(_extract_message_text(message))
                        finish_reason = choice.get("finish_reason") or "stop"
                        reasoning_len = len(message.get("reasoning") or "")

                    event_tags = []
                    if not content.strip():
                        event_tags.append("empty_response")
                    return AdapterResponse(
                        text=content,
                        finish_reason=finish_reason,
                        event_tags=event_tags,
                        raw_payload={
                            "id": response_payload.get("id"),
                            "model": response_payload.get("model"),
                            "provider": response_payload.get("provider"),
                            "usage": response_payload.get("usage"),
                            "reasoning_len": reasoning_len,
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

        raise RuntimeError(last_error or "AIHubMix request failed")
