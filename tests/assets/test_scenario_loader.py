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
