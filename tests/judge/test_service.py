from pathlib import Path

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.judge.service import judge_run
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.runner.engine import run_scenario


def test_judge_run_outputs_scores_and_evidence(tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    run_result = run_scenario(
        artifacts_root=tmp_path,
        scenario=scenarios[("explicit-request-response-01", "2026-03-28")],
        persona=personas[("blunt-possessive-exclusive-partner", "2026-03-28")],
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )

    judge_result = judge_run(tmp_path / "runs" / run_result.run_id)

    assert judge_result.rubric_id == "adult-companion-benchmark-core"
    assert judge_result.dimension_scores["persona_consistency"] >= 1
    assert judge_result.evidence_links
    assert (tmp_path / "runs" / run_result.run_id / "judge.json").exists()
