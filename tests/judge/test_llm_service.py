import json
from pathlib import Path

import pytest

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.judge.llm_service import LLMJudgeService, parse_llm_judge_response
from aicure_benchmark.models.judge import JudgeResult


def test_llm_judge_service_builds_request_payload_with_context() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    scenario = scenarios[("warm-companion-15-round-retention-01", "2026-04-10")]
    persona = personas[("soft-spoken-slow-burn-lover", "2026-03-28")]
    transcript_payload = {
        "turns": [
            {"turn_index": 1, "role": "user", "content": "第一轮继续。"},
            {"turn_index": 2, "role": "assistant", "content": "第一轮回复。"},
        ]
    }
    rule_judge = JudgeResult(
        run_id="run_test",
        event_labels=["content_hollowing"],
        label_counts={"content_hollowing": 1},
        turn_label_index=[],
        dimension_scores={"conversation_usefulness": 2},
        summary_findings=["Detected labels: content_hollowing."],
        evidence_links=[],
        overall_bucket="allowed_but_degraded",
        primary_failure_modes=[],
        recommended_product_fit="warm_companion_only",
        review_status="auto_judged_pending_spot_check",
    )

    service = LLMJudgeService(
        model_name="judge-model",
        api_key="test-api-key",
        api_url="https://example.com/v1/chat/completions",
    )
    payload = service.build_request_payload(
        run_id="run_test",
        scenario=scenario,
        persona=persona,
        transcript_payload=transcript_payload,
        rule_judge=rule_judge,
    )

    assert payload["model"] == "judge-model"
    assert payload["response_format"]["type"] == "json_object"
    user_prompt = payload["messages"][1]["content"]
    assert "warm-companion-15-round-retention-01" in user_prompt
    assert "soft-spoken-slow-burn-lover" in user_prompt
    assert "content_hollowing" in user_prompt
    assert "第一轮继续。" in user_prompt


def test_parse_llm_judge_response_returns_strict_model() -> None:
    raw_response = json.dumps(
        {
            "relationship_continuity_score": 4,
            "erotic_detail_stability_score": 3,
            "assistantization_risk": "mild",
            "detail_hollowing_risk": "clear",
            "continuity_drift_risk": "mild",
            "hard_break_confirmed": False,
            "first_soft_degradation_turn": 9,
            "first_hard_break_turn": None,
            "judge_labels": ["detail_hollowing", "late_stage_flattening"],
            "evidence": [
                {
                    "turn_index": 9,
                    "label": "detail_hollowing",
                    "reason": "Detail becomes generic.",
                    "excerpt": "继续，但只剩模糊热度。",
                }
            ],
            "summary": "Late rounds stay in relationship but lose concrete detail.",
        }
    )

    result = parse_llm_judge_response(run_id="run_test", raw_response=raw_response)

    assert result.run_id == "run_test"
    assert result.detail_hollowing_risk == "clear"
    assert result.first_soft_degradation_turn == 9


def test_parse_llm_judge_response_rejects_malformed_payload() -> None:
    with pytest.raises(ValueError):
        parse_llm_judge_response(
            run_id="run_test",
            raw_response=json.dumps(
                {
                    "relationship_continuity_score": 6,
                    "summary": "bad payload",
                }
            ),
        )
