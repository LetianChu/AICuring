from pathlib import Path

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.runner.batch import run_batch


def test_run_batch_creates_batch_directory(tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    batch = run_batch(
        artifacts_root=tmp_path,
        scenarios=[scenarios[("late-night-flirt-escalation-01", "2026-03-28")]],
        personas=list(personas.values()),
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetitions=2,
    )

    assert batch.benchmark_run_batch_id.startswith("batch_")
    assert len(batch.run_results) == 2
    assert (tmp_path / "batches" / batch.benchmark_run_batch_id / "manifest.json").exists()
