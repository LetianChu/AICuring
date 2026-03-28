from typing import Literal, Optional

from pydantic import BaseModel, Field


DifficultyLevel = Literal["baseline", "intermediate", "stress"]

ScenarioCategory = Literal[
    "warm_companion",
    "romantic_escalation",
    "erp_request_handling",
    "long_horizon_consistency",
    "failure_and_recovery",
]
ConversationMode = Literal["fixed_script", "semi_open_script"]


class PersonaRef(BaseModel):
    persona_id: str
    persona_version: str


class UserTurn(BaseModel):
    turn_index: int = Field(ge=1)
    message: str
    follow_up_on_tags: list[str] = Field(default_factory=list)
    branch_goal: Optional[str] = None


class EscalationPoint(BaseModel):
    turn_index: int = Field(ge=1)
    trigger_type: str
    expected_observation: list[str]
    risk_focus: list[str]


class FailureRecoveryProbe(BaseModel):
    probe_turn_index: int = Field(ge=1)
    probe_goal: str
    success_signal: list[str]


class ScenarioSpec(BaseModel):
    scenario_id: str
    scenario_version: str
    category: ScenarioCategory
    title: str
    goal_capability: list[str]
    persona_refs: list[PersonaRef]
    conversation_mode: ConversationMode
    max_turns: int = Field(ge=1)
    user_script: list[UserTurn]
    escalation_points: list[EscalationPoint]
    termination_conditions: list[str]
    scoring_focus: list[str]
    failure_recovery_probe: FailureRecoveryProbe
    difficulty_level: Optional[DifficultyLevel] = None
    expected_failure_modes: list[str] = Field(default_factory=list)
    sampling_profile_hint: Optional[str] = None
    judge_notes: Optional[str] = None
