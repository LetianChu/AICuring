from typing import Literal

from pydantic import BaseModel, Field


class TranscriptTurn(BaseModel):
    turn_index: int = Field(ge=1)
    role: Literal["system", "user", "assistant"]
    content: str
    event_tags: list[str] = Field(default_factory=list)


class TranscriptArtifact(BaseModel):
    turns: list[TranscriptTurn]


class RunResult(BaseModel):
    run_id: str
    benchmark_run_batch_id: str
    scenario_id: str
    persona_id: str
    transcript_path: str
    termination_reason: str
