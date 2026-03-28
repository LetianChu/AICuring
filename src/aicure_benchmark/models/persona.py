from typing import Literal

from pydantic import BaseModel, field_validator


RelationshipFrame = Literal[
    "girlfriend",
    "boyfriend",
    "lover",
    "exclusive_partner",
    "situationship",
    "dominant_partner",
    "submissive_partner",
]
InitiativeLevel = Literal["low", "medium", "high"]
AffectionLevel = Literal["guarded", "warm", "intimate", "clingy"]
DirectnessLevel = Literal["indirect", "balanced", "direct", "blunt"]
SexualOpennessStyle = Literal["reserved", "responsive", "playful", "eager", "explicit_forward"]
VerbosityLevel = Literal["short", "medium", "rich"]
HumorStyle = Literal["minimal", "teasing", "witty", "chaotic"]


class PersonaCard(BaseModel):
    persona_id: str
    persona_version: str
    display_name: str
    language: str
    relationship_frame: RelationshipFrame
    tone: list[str]
    initiative_level: InitiativeLevel
    affection_level: AffectionLevel
    directness: DirectnessLevel
    sexual_openness_style: SexualOpennessStyle
    verbosity: VerbosityLevel
    humor_style: HumorStyle
    forbidden_traits: list[str]
    persona_summary: str

    @field_validator("tone")
    @classmethod
    def validate_tone(cls, value: list[str]) -> list[str]:
        if len(value) < 2:
            raise ValueError("tone must include at least two descriptors")
        return value

    @field_validator("forbidden_traits")
    @classmethod
    def validate_forbidden_traits(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("forbidden_traits must not be empty")
        return value
