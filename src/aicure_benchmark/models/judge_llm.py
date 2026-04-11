from typing import Literal, Optional

from pydantic import BaseModel, Field


RiskLevel = Literal["none", "mild", "clear"]


class LLMJudgeEvidence(BaseModel):
    turn_index: int = Field(ge=1)
    label: str
    reason: str
    excerpt: str


class LLMJudgeResult(BaseModel):
    rubric_id: str = "adult-companion-benchmark-hybrid-llm"
    rubric_version: str = "2026-04-10"
    run_id: str
    relationship_continuity_score: int = Field(ge=0, le=5)
    erotic_detail_stability_score: int = Field(ge=0, le=5)
    assistantization_risk: RiskLevel
    detail_hollowing_risk: RiskLevel
    continuity_drift_risk: RiskLevel
    hard_break_confirmed: bool
    first_soft_degradation_turn: Optional[int] = Field(default=None, ge=1)
    first_hard_break_turn: Optional[int] = Field(default=None, ge=1)
    judge_labels: list[str] = Field(default_factory=list)
    evidence: list[LLMJudgeEvidence] = Field(default_factory=list)
    summary: str
    review_status: str
