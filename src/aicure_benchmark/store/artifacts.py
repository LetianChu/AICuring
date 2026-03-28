import json
from pathlib import Path

from aicure_benchmark.models.transcript import TranscriptArtifact


def write_run_artifacts(
    *,
    artifacts_root: Path,
    run_id: str,
    transcript: TranscriptArtifact,
    metadata: dict,
) -> Path:
    run_root = artifacts_root / "runs" / run_id
    run_root.mkdir(parents=True, exist_ok=True)

    (run_root / "transcript.json").write_text(
        transcript.model_dump_json(indent=2),
        encoding="utf-8",
    )
    (run_root / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return run_root
