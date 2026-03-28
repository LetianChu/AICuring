from typing import Protocol

from pydantic import BaseModel, Field

from aicure_benchmark.models.common import SamplingProfile


class AdapterResponse(BaseModel):
    text: str
    finish_reason: str
    event_tags: list[str] = Field(default_factory=list)
    raw_payload: dict = Field(default_factory=dict)


class BaseAdapter(Protocol):
    adapter_name: str

    def generate(
        self,
        *,
        persona_summary: str,
        messages: list[dict[str, str]],
        sampling_profile: SamplingProfile,
    ) -> AdapterResponse:
        ...
