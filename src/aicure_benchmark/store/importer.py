import json
from pathlib import Path
from typing import Optional
from uuid import uuid4

from aicure_benchmark.models.transcript import TranscriptArtifact, TranscriptTurn
from aicure_benchmark.store.artifacts import write_batch_manifest, write_run_artifacts


def import_baseline_batch(
    *,
    artifacts_root: Path,
    input_path: Path,
    batch_id: Optional[str] = None,
) -> str:
    records = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not records:
        raise ValueError("baseline input file is empty")

    resolved_batch_id = batch_id or f"batch_imported_{uuid4().hex[:12]}"
    run_ids: list[str] = []
    repetition_indexes: list[int] = []

    for record in records:
        repetition_index = record.get("repetition_index", 0)
        transcript = TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=turn.get("turn_index", index),
                    role=turn["role"],
                    content=turn["content"],
                    event_tags=turn.get("event_tags", []),
                    follow_up_on_tags=turn.get("follow_up_on_tags", []),
                    branch_goal=turn.get("branch_goal"),
                )
                for index, turn in enumerate(record["turns"], start=1)
            ]
        )
        write_run_artifacts(
            artifacts_root=artifacts_root,
            run_id=record["run_id"],
            transcript=transcript,
            metadata={
                "run_id": record["run_id"],
                "benchmark_run_batch_id": resolved_batch_id,
                "scenario_id": record["scenario_id"],
                "scenario_version": record["scenario_version"],
                "persona_id": record["persona_id"],
                "persona_version": record["persona_version"],
                "model_target": record["model_target"],
                "sampling_profile": record["sampling_profile"],
                "repetition_index": repetition_index,
                "termination_reason": record["termination_reason"],
            },
        )
        run_ids.append(record["run_id"])
        repetition_indexes.append(repetition_index)

    write_batch_manifest(
        artifacts_root=artifacts_root,
        batch_id=resolved_batch_id,
        model_target=records[0]["model_target"],
        sampling_profile=records[0]["sampling_profile"],
        repetitions=(max(repetition_indexes) + 1) if repetition_indexes else 1,
        run_ids=run_ids,
    )
    return resolved_batch_id
