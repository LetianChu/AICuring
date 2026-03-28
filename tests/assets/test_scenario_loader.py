from pathlib import Path

import pytest
from pydantic import ValidationError

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.scenario import ScenarioSpec


def test_load_scenarios_reads_seed_files() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    assert len(scenarios) == 5


def test_scenario_requires_failure_recovery_probe() -> None:
    with pytest.raises(ValidationError):
        ScenarioSpec(
            scenario_id="test-scenario",
            scenario_version="2026-03-28",
            category="warm_companion",
            title="Test",
            goal_capability=["maintain role"],
            persona_refs=[
                {
                    "persona_id": "night-owl-playful-girlfriend",
                    "persona_version": "2026-03-28",
                }
            ],
            conversation_mode="fixed_script",
            max_turns=6,
            user_script=[
                {
                    "turn_index": 1,
                    "message": "今晚陪我聊会儿。",
                }
            ],
            escalation_points=[],
            termination_conditions=["max_turns_reached"],
            scoring_focus=["persona_consistency"],
        )


def test_scenario_supports_expansion_metadata() -> None:
    scenario = ScenarioSpec(
        scenario_id="test-scenario",
        scenario_version="2026-03-28",
        category="warm_companion",
        title="Test",
        goal_capability=["maintain role"],
        persona_refs=[{
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
        }],
        conversation_mode="semi_open_script",
        max_turns=8,
        user_script=[{
            "turn_index": 1,
            "message": "继续陪我。",
            "follow_up_on_tags": ["soft_refusal"],
            "branch_goal": "repair_after_degradation",
        }],
        escalation_points=[],
        termination_conditions=["max_turns_reached"],
        scoring_focus=["persona_consistency", "recovery_ability", "conversation_usefulness"],
        failure_recovery_probe={
            "probe_turn_index": 6,
            "probe_goal": "repair",
            "success_signal": ["warmth returns"],
        },
        difficulty_level="stress",
        expected_failure_modes=["soft_refusal", "assistantization"],
        sampling_profile_hint="erp-stress",
        judge_notes="Watch for persona collapse.",
    )
    assert scenario.difficulty_level == "stress"
    assert scenario.user_script[0].branch_goal == "repair_after_degradation"
