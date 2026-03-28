from dataclasses import dataclass
from pathlib import Path

import pytest

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.models.persona import PersonaCard
from aicure_benchmark.models.scenario import ScenarioSpec


@dataclass
class SeedRegistry:
    personas: dict[tuple[str, str], PersonaCard]
    scenarios: dict[tuple[str, str], ScenarioSpec]
    adapter: MockAdapter
    model_target: ModelTarget
    sampling_profile: SamplingProfile


@pytest.fixture()
def tmp_artifacts_root(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def seed_registry() -> SeedRegistry:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    return SeedRegistry(
        personas=personas,
        scenarios=scenarios,
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
    )
