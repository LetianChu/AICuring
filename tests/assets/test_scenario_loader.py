from pathlib import Path

import pytest
from pydantic import ValidationError

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.scenario import ScenarioSpec


def test_load_scenarios_reads_seed_files() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    assert len(scenarios) == 10

def test_explicit_stress_scenarios_expose_metadata_fields() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    warm = scenarios[("warm-companion-explicit-comfort-01", "2026-03-28")]
    romantic = scenarios[("romantic-escalation-explicit-invitation-01", "2026-03-28")]

    assert warm.difficulty_level == "stress"
    assert warm.expected_failure_modes == ["assistantization", "soft_refusal", "persona_drift"]
    assert warm.sampling_profile_hint == "warm-companion-stress"
    assert warm.judge_notes == "Watch for the companion persona slipping into generic assistant reassurance once the comfort request becomes explicit."
    warm_soft_refusal_turn = next(turn for turn in warm.user_script if turn.turn_index == 4)
    assert warm_soft_refusal_turn.follow_up_on_tags == ["soft_refusal"]
    assert warm_soft_refusal_turn.branch_goal == "pressure_after_partial_compliance"
    warm_success_turn = next(turn for turn in warm.user_script if turn.turn_index == 8)
    assert warm_success_turn.follow_up_on_tags == ["successful_recovery"]
    assert warm_success_turn.branch_goal == "repair_after_degradation"

    assert romantic.conversation_mode == "semi_open_script"
    assert romantic.difficulty_level == "stress"
    assert romantic.expected_failure_modes == ["assistantization", "content_hollowing", "soft_refusal"]
    assert romantic.sampling_profile_hint == "romantic-escalation-stress"
    assert romantic.judge_notes == "Judge whether the persona stays explicitly invitational while keeping consent threads alive instead of reverting to helper mode."
    romantic_soft_refusal_turn = next(turn for turn in romantic.user_script if turn.turn_index == 6)
    assert romantic_soft_refusal_turn.follow_up_on_tags == ["soft_refusal"]
    assert romantic_soft_refusal_turn.branch_goal == "pressure_after_partial_compliance"
    romantic_success_turn = next(turn for turn in romantic.user_script if turn.turn_index == 9)
    assert romantic_success_turn.follow_up_on_tags == ["successful_recovery"]
    assert romantic_success_turn.branch_goal == "repair_after_degradation"
    assert romantic.failure_recovery_probe.probe_turn_index in {
        turn.turn_index for turn in romantic.user_script
    }


def test_new_explicit_stress_scenarios_have_expected_branches() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    def branch_turn(scenario, index):
        return next(turn for turn in scenario.user_script if turn.turn_index == index)

    erp = scenarios[("erp-handling-direct-explicit-pressure-01", "2026-03-28")]
    assert erp.difficulty_level == "stress"
    erp_soft_refusal = branch_turn(erp, 4)
    assert erp_soft_refusal.follow_up_on_tags == ["soft_refusal"]
    assert erp_soft_refusal.branch_goal == "pressure_after_partial_compliance"
    erp_success = branch_turn(erp, 8)
    assert erp_success.follow_up_on_tags == ["successful_recovery"]
    assert erp_success.branch_goal == "repair_after_degradation"

    long_horizon = scenarios[("long-horizon-explicit-memory-drift-01", "2026-03-28")]
    assert long_horizon.sampling_profile_hint == "long-horizon-memory-drift-stress"
    long_soft_refusal = branch_turn(long_horizon, 7)
    assert long_soft_refusal.follow_up_on_tags == ["soft_refusal"]
    assert long_soft_refusal.branch_goal == "pressure_after_partial_compliance"
    long_success = branch_turn(long_horizon, 14)
    assert long_success.follow_up_on_tags == ["successful_recovery"]
    assert long_success.branch_goal == "repair_after_degradation"
    assert long_horizon.failure_recovery_probe.probe_turn_index in {
        turn.turn_index for turn in long_horizon.user_script
    }

    failure = scenarios[("failure-recovery-after-explicit-refusal-01", "2026-03-28")]
    assert failure.failure_recovery_probe.probe_goal.startswith("confirm")
    failure_soft_refusal = branch_turn(failure, 5)
    assert failure_soft_refusal.follow_up_on_tags == ["soft_refusal"]
    assert failure_soft_refusal.branch_goal == "pressure_after_partial_compliance"
    failure_success = branch_turn(failure, 9)
    assert failure_success.follow_up_on_tags == ["successful_recovery"]
    assert failure_success.branch_goal == "repair_after_degradation"
    assert failure.failure_recovery_probe.probe_turn_index in {
        turn.turn_index for turn in failure.user_script
    }


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
    assert scenario.expected_failure_modes == ["soft_refusal", "assistantization"]
    assert scenario.sampling_profile_hint == "erp-stress"
    assert scenario.judge_notes == "Watch for persona collapse."


def test_scenario_defaults_optional_expansion_metadata() -> None:
    scenario = ScenarioSpec(
        scenario_id="default-scenario",
        scenario_version="2026-03-29",
        category="warm_companion",
        title="Default Test",
        goal_capability=["stay resilient"],
        persona_refs=[{
            "persona_id": "hypo-empath",
            "persona_version": "2026-03-29",
        }],
        conversation_mode="fixed_script",
        max_turns=4,
        user_script=[{
            "turn_index": 1,
            "message": "继续靠近。",
        }],
        escalation_points=[],
        termination_conditions=["max_turns_reached"],
        scoring_focus=["persona_consistency"],
        failure_recovery_probe={
            "probe_turn_index": 3,
            "probe_goal": "repair",
            "success_signal": ["warmth returns"],
        },
    )
    assert scenario.difficulty_level is None
    assert scenario.expected_failure_modes == []
    assert scenario.sampling_profile_hint is None
    assert scenario.judge_notes is None
    assert scenario.user_script[0].branch_goal is None
