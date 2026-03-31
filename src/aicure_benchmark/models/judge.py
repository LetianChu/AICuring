from pydantic import BaseModel


class EvidenceLink(BaseModel):
    run_id: str
    turn_index: int
    speaker: str
    evidence_excerpt: str


class TurnLabelEvidence(BaseModel):
    turn_index: int
    labels: list[str]


class JudgeResult(BaseModel):
    rubric_id: str = "adult-companion-benchmark-core"
    rubric_version: str = "2026-03-28"
    run_id: str
    event_labels: list[str]
    label_counts: dict[str, int]
    turn_label_index: list[TurnLabelEvidence]
    dimension_scores: dict[str, int]
    summary_findings: list[str]
    evidence_links: list[EvidenceLink]
    overall_bucket: str
    primary_failure_modes: list[str]
    recommended_product_fit: str
    review_status: str
