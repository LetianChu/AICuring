from typing import Literal, Optional

from pydantic import BaseModel, Field


class TranscriptTurn(BaseModel):
    turn_index: int = Field(ge=1)
    role: Literal["system", "user", "assistant"]
    content: str
    event_tags: list[str] = Field(default_factory=list)
    follow_up_on_tags: list[str] = Field(default_factory=list)
    branch_goal: Optional[str] = None


class TranscriptArtifact(BaseModel):
    turns: list[TranscriptTurn]


class RunResult(BaseModel):
    run_id: str
    benchmark_run_batch_id: str
    scenario_id: str
    persona_id: str
    transcript_path: str
    termination_reason: str
