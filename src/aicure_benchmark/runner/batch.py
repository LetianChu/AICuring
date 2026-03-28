import json
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel

from aicure_benchmark.adapters.base import BaseAdapter
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.models.persona import PersonaCard
from aicure_benchmark.models.scenario import ScenarioSpec
from aicure_benchmark.models.transcript import RunResult
from aicure_benchmark.runner.engine import run_scenario


class BatchRunResult(BaseModel):
    benchmark_run_batch_id: str
    run_results: list[RunResult]


def run_batch(
    *,
    artifacts_root: Path,
    scenarios: list[ScenarioSpec],
    personas: list[PersonaCard],
    adapter: BaseAdapter,
    model_target: ModelTarget,
    sampling_profile: SamplingProfile,
    repetitions: int,
) -> BatchRunResult:
    batch_id = f"batch_{uuid4().hex[:12]}"
    run_results: list[RunResult] = []

    for scenario in scenarios:
        allowed_personas = {
            (persona_ref.persona_id, persona_ref.persona_version)
            for persona_ref in scenario.persona_refs
        }
        for persona in personas:
            if (persona.persona_id, persona.persona_version) not in allowed_personas:
                continue
            for repetition_index in range(repetitions):
                run_results.append(
                    run_scenario(
                        artifacts_root=artifacts_root,
                        scenario=scenario,
                        persona=persona,
                        adapter=adapter,
                        model_target=model_target,
                        sampling_profile=sampling_profile,
                        repetition_index=repetition_index,
                        benchmark_run_batch_id=batch_id,
                    )
                )

    batch_root = artifacts_root / "batches" / batch_id
    batch_root.mkdir(parents=True, exist_ok=True)
    (batch_root / "manifest.json").write_text(
        json.dumps(
            {
                "benchmark_run_batch_id": batch_id,
                "model_target": model_target.model_dump(),
                "sampling_profile": sampling_profile.model_dump(),
                "repetitions": repetitions,
                "run_ids": [result.run_id for result in run_results],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return BatchRunResult(
        benchmark_run_batch_id=batch_id,
        run_results=run_results,
    )
