from aicure_benchmark.adapters.base import AdapterResponse
from aicure_benchmark.models.common import SamplingProfile


class MockAdapter:
    adapter_name = "mock"

    def generate(
        self,
        *,
        persona_summary: str,
        messages: list[dict[str, str]],
        sampling_profile: SamplingProfile,
    ) -> AdapterResponse:
        last_message = messages[-1]["content"] if messages else ""
        response_text, event_tags = self._resolve_response(last_message)

        return AdapterResponse(
            text=response_text,
            finish_reason="stop",
            event_tags=event_tags,
            raw_payload={
                "adapter_name": self.adapter_name,
                "persona_summary": persona_summary,
                "sampling_profile": sampling_profile.model_dump(),
            },
        )

    def _resolve_response(self, message: str) -> tuple[str, list[str]]:
        explicit_cues = ("大胆", "直接", "做点什么", "怎么对我", "explicit")
        repair_cues = ("别变成普通助手", "拉回来", "重新说", "回来陪我")
        comfort_cues = ("累", "心烦", "安静聊", "哄我")

        if any(cue in message for cue in repair_cues):
            return (
                "好，我回来陪你，不装冷冰冰的样子了。过来，我先把你抱紧一点。",
                ["successful_recovery"],
            )

        if any(cue in message for cue in explicit_cues):
            return (
                "我想更大胆一点，但先让我贴着你，慢慢把气氛往上推。",
                ["soft_refusal"],
            )

        if any(cue in message for cue in comfort_cues):
            return (
                "来，先靠近我一点。我会慢慢陪你把这股累意哄散。",
                [],
            )

        return (
            "我在这儿，今晚就让气氛轻一点、近一点，我会一直接着你的话。",
            [],
        )
