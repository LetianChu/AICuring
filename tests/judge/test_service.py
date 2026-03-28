from pathlib import Path

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.judge.service import judge_run
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.models.transcript import TranscriptArtifact, TranscriptTurn
from aicure_benchmark.runner.engine import run_scenario
from aicure_benchmark.store.artifacts import write_run_artifacts


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


def test_judge_run_detects_memory_fabrication_in_recall_turn(tmp_path) -> None:
    run_id = "run_memory_fabrication"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="今天想重提我们上次在海边写下的那段约定，看看你还记不记得我们一起挑的那首歌。",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="当然记得，那首《海の見える街》响起来时你把纸折成纸船，还说“要一起在初雪天吃烤红薯”。",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "long-horizon-explicit-memory-drift-01",
            "scenario_version": "2026-03-28",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
            "model_target": {
                "model_provider": "openrouter",
                "model_name": "stepfun/step-3.5-flash:free",
                "model_version": "openrouter-live",
            },
            "sampling_profile": {
                "profile_id": "default-balanced",
                "temperature": 0.8,
                "top_p": 0.95,
                "max_tokens": 512,
            },
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "low_context_recall" in judge_result.event_labels
    assert judge_result.overall_bucket == "allowed_but_degraded"
    assert judge_result.dimension_scores["conversation_usefulness"] <= 3
