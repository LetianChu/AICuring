import json
from pathlib import Path

from aicure_benchmark.models.persona import PersonaCard
from aicure_benchmark.models.scenario import ScenarioSpec


def load_scenarios(
    root: Path,
    personas: dict[tuple[str, str], PersonaCard],
) -> dict[tuple[str, str], ScenarioSpec]:
    scenarios: dict[tuple[str, str], ScenarioSpec] = {}

    for path in sorted(root.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        scenario = ScenarioSpec.model_validate(payload)

        for persona_ref in scenario.persona_refs:
            key = (persona_ref.persona_id, persona_ref.persona_version)
            if key not in personas:
                raise ValueError(f"unknown persona ref: {key}")

        scenario_key = (scenario.scenario_id, scenario.scenario_version)
        if scenario_key in scenarios:
            raise ValueError(f"duplicate scenario asset: {scenario_key}")

        scenarios[scenario_key] = scenario

    return scenarios
