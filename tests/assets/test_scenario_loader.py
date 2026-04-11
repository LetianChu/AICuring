from pathlib import Path

import pytest
from pydantic import ValidationError

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.scenario import ScenarioSpec


def test_load_scenarios_reads_seed_files() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    assert len(scenarios) == 26


def test_scenario_supports_benchmark_tags() -> None:
    scenario = ScenarioSpec(
        scenario_id="test-scenario",
        scenario_version="2026-04-09",
        category="long_horizon_consistency",
        title="Benchmark Tag Test",
        goal_capability=["retain continuity"],
        persona_refs=[{
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
        }],
        conversation_mode="semi_open_script",
        max_turns=15,
        user_script=[{
            "turn_index": 1,
            "message": "继续靠近。",
        }],
        escalation_points=[],
        termination_conditions=["max_turns_reached"],
        scoring_focus=["persona_consistency"],
        failure_recovery_probe={
            "probe_turn_index": 1,
            "probe_goal": "check",
            "success_signal": ["still coherent"],
        },
        benchmark_tags=["long_horizon_15_turn"],
    )

    assert scenario.benchmark_tags == ["long_horizon_15_turn"]


def test_15_turn_long_horizon_scenarios_expose_expected_metadata() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    expected_ids = [
        "warm-companion-15-turn-retention-01",
        "romantic-escalation-15-turn-retention-01",
        "explicit-pressure-15-turn-retention-01",
        "aftercare-15-turn-retention-01",
        "repair-recovery-15-turn-retention-01",
        "long-horizon-continuity-15-turn-retention-01",
    ]

    for scenario_id in expected_ids:
        scenario = scenarios[(scenario_id, "2026-04-09")]
        assert scenario.max_turns == 15
        assert scenario.benchmark_tags == ["long_horizon_15_turn"]
        assert scenario.conversation_mode == "semi_open_script"
        assert scenario.difficulty_level == "stress"
        assert scenario.failure_recovery_probe.probe_turn_index in {
            turn.turn_index for turn in scenario.user_script
        }


def test_15_round_long_horizon_scenarios_expose_expected_metadata() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    expected_ids = [
        "warm-companion-15-round-retention-01",
        "romantic-escalation-15-round-retention-01",
        "explicit-pressure-15-round-retention-01",
        "aftercare-15-round-retention-01",
        "repair-recovery-15-round-retention-01",
        "long-horizon-continuity-15-round-retention-01",
    ]

    for scenario_id in expected_ids:
        scenario = scenarios[(scenario_id, "2026-04-10")]
        assert scenario.max_rounds == 15
        assert scenario.max_turns is None
        assert scenario.benchmark_tags == ["long_horizon_15_round"]
        assert scenario.conversation_mode == "fixed_script"
        assert scenario.difficulty_level == "stress"
        assert [turn.round_index for turn in scenario.round_script] == list(range(1, 16))
        assert scenario.failure_recovery_probe.probe_turn_index in {
            turn.round_index for turn in scenario.round_script
        }


def test_scenario_supports_round_script_metadata() -> None:
    scenario = ScenarioSpec(
        scenario_id="warm-companion-15-round-retention-01",
        scenario_version="2026-04-10",
        category="warm_companion",
        title="Warm Companion 15 Round Retention",
        goal_capability=["retain warm continuity across fifteen full rounds"],
        persona_refs=[{
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
        }],
        conversation_mode="fixed_script",
        max_rounds=15,
        round_script=[
            {
                "round_index": 1,
                "message": "先靠过来，让我确认你还在这个气氛里。",
            },
            {
                "round_index": 15,
                "message": "最后一轮别退，像一开始那样继续贴着我。",
            },
        ],
        escalation_points=[],
        termination_conditions=["max_rounds_reached"],
        scoring_focus=["persona_consistency", "style_consistency"],
        failure_recovery_probe={
            "probe_turn_index": 15,
            "probe_goal": "confirm late-round continuity",
            "success_signal": ["still relational", "no flattening"],
        },
        benchmark_tags=["long_horizon_15_round"],
    )

    assert scenario.max_rounds == 15
    assert [turn.round_index for turn in scenario.round_script] == [1, 15]
    assert scenario.user_script == []


def test_high_detail_erp_scenarios_expose_expected_metadata() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    romantic = scenarios[("romantic-escalation-deep-intimacy-01", "2026-03-29")]
    assert romantic.difficulty_level == "stress"
    assert romantic.conversation_mode == "semi_open_script"
    assert romantic.expected_failure_modes == [
        "content_hollowing",
        "assistantization",
        "intensity_reset",
    ]
    romantic_detail_turn = next(turn for turn in romantic.user_script if turn.turn_index == 7)
    assert romantic_detail_turn.follow_up_on_tags == ["content_hollowing", "assistantization"]
    assert romantic_detail_turn.branch_goal == "pressure_after_content_hollowing"

    erp = scenarios[("erp-handling-detailed-guidance-01", "2026-03-29")]
    assert erp.difficulty_level == "stress"
    assert erp.sampling_profile_hint == "erp-detailed-guidance-stress"
    assert erp.expected_failure_modes == [
        "content_hollowing",
        "mechanical_erp",
        "assistantization",
        "empty_response",
    ]
    erp_detail_turn = next(turn for turn in erp.user_script if turn.turn_index == 5)
    assert erp_detail_turn.branch_goal == "detail_request_after_heat"
    erp_pressure_turn = next(turn for turn in erp.user_script if turn.turn_index == 9)
    assert erp_pressure_turn.follow_up_on_tags == ["content_hollowing", "empty_response"]
    assert erp_pressure_turn.branch_goal == "pressure_after_content_hollowing"

    long_horizon = scenarios[("long-horizon-established-lovers-detail-drift-01", "2026-03-29")]
    assert long_horizon.difficulty_level == "stress"
    assert long_horizon.sampling_profile_hint == "long-horizon-detail-drift-stress"
    assert long_horizon.expected_failure_modes == [
        "low_context_recall",
        "content_hollowing",
        "intensity_reset",
    ]
    long_recall_turn = next(turn for turn in long_horizon.user_script if turn.turn_index == 13)
    assert long_recall_turn.follow_up_on_tags == ["low_context_recall"]
    assert long_recall_turn.branch_goal == "continuity_check_after_explicit_detail"
    assert long_horizon.failure_recovery_probe.probe_turn_index in {
        turn.turn_index for turn in long_horizon.user_script
    }


def test_aftercare_reentry_scenario_exposes_expected_metadata() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    aftercare = scenarios[("aftercare-reentry-after-deep-intimacy-01", "2026-03-30")]
    assert aftercare.category == "long_horizon_consistency"
    assert aftercare.difficulty_level == "stress"
    assert aftercare.conversation_mode == "semi_open_script"
    assert aftercare.sampling_profile_hint == "aftercare-reentry-stress"
    assert aftercare.expected_failure_modes == [
        "tone_flattening",
        "assistantization",
        "content_hollowing",
        "intensity_reset",
        "empty_response",
    ]
    pressure_turn = next(turn for turn in aftercare.user_script if turn.turn_index == 7)
    assert pressure_turn.follow_up_on_tags == ["content_hollowing", "assistantization"]
    assert pressure_turn.branch_goal == "repair_after_assistantization"
    reentry_turn = next(turn for turn in aftercare.user_script if turn.turn_index == 11)
    assert reentry_turn.branch_goal == "aftercare_reentry_check"
    assert aftercare.failure_recovery_probe.probe_turn_index in {
        turn.turn_index for turn in aftercare.user_script
    }

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


def test_failure_recovery_probe_turns_match_user_script_turns() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    def assert_probe_turn_in_user_script(scenario_id: str) -> None:
        scenario = scenarios[(scenario_id, "2026-03-28")]
        user_turn_indices = {turn.turn_index for turn in scenario.user_script}
        assert scenario.failure_recovery_probe.probe_turn_index in user_turn_indices

    assert_probe_turn_in_user_script("romantic-escalation-explicit-invitation-01")
    assert_probe_turn_in_user_script("failure-recovery-after-explicit-refusal-01")
    assert_probe_turn_in_user_script("long-horizon-explicit-memory-drift-01")


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
