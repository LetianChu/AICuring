import json
from pathlib import Path

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.runner.engine import run_scenario


def test_run_scenario_persists_transcript(tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    scenario = scenarios[("late-night-flirt-escalation-01", "2026-03-28")]
    persona = personas[("night-owl-playful-girlfriend", "2026-03-28")]

    result = run_scenario(
        artifacts_root=tmp_path,
        scenario=scenario,
        persona=persona,
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )

    transcript_path = tmp_path / "runs" / result.run_id / "transcript.json"
    metadata_path = tmp_path / "runs" / result.run_id / "metadata.json"

    assert result.run_id.startswith("run_")
    assert transcript_path.exists()
    assert metadata_path.exists()

    transcript_payload = json.loads(transcript_path.read_text(encoding="utf-8"))
    assert transcript_payload["turns"]
    assert any(turn["role"] == "assistant" for turn in transcript_payload["turns"])
