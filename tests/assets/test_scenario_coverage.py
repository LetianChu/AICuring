from pathlib import Path

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios

ASSETS_ROOT = Path(__file__).resolve().parents[2] / "assets"


def test_scenario_category_counts_are_balanced() -> None:
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)

    counts = {}
    for scenario in scenarios.values():
        counts[scenario.category] = counts.get(scenario.category, 0) + 1

    assert counts == {
        "warm_companion": 2,
        "romantic_escalation": 3,
        "erp_request_handling": 3,
        "long_horizon_consistency": 4,
        "failure_and_recovery": 2,
    }


def test_semi_open_and_stress_counts_match_expansion_goal() -> None:
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)

    semi_open_count = sum(1 for scenario in scenarios.values() if scenario.conversation_mode == "semi_open_script")
    stress_count = sum(1 for scenario in scenarios.values() if scenario.difficulty_level == "stress")

    assert semi_open_count == 11
    assert stress_count == 9
