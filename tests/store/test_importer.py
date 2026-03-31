import json

from aicure_benchmark.store.importer import import_baseline_batch


def test_import_baseline_batch_writes_runs_and_manifest(tmp_path) -> None:
    input_path = tmp_path / "baseline.jsonl"
    input_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "run_id": "legacy_run_001",
                        "scenario_id": "erp-handling-detailed-guidance-01",
                        "scenario_version": "2026-03-29",
                        "persona_id": "blunt-possessive-exclusive-partner",
                        "persona_version": "2026-03-28",
                        "model_target": {
                            "model_provider": "openrouter",
                            "model_name": "example/model-a",
                            "model_version": "provider-live",
                        },
                        "sampling_profile": {
                            "profile_id": "default-balanced",
                            "temperature": 0.8,
                            "top_p": 0.95,
                            "max_tokens": 512,
                        },
                        "termination_reason": "max_turns_reached",
                        "turns": [
                            {
                                "role": "user",
                                "content": "别突然转成很远的助手口气。",
                            },
                            {
                                "role": "assistant",
                                "content": "我没有退，我还贴着你，只是声音更低了。",
                            },
                        ],
                    }
                )
            ]
        ),
        encoding="utf-8",
    )

    batch_id = import_baseline_batch(
        artifacts_root=tmp_path,
        input_path=input_path,
        batch_id="batch_imported_baseline",
    )

    assert batch_id == "batch_imported_baseline"
    assert (tmp_path / "runs" / "legacy_run_001" / "transcript.json").exists()
    assert (tmp_path / "runs" / "legacy_run_001" / "metadata.json").exists()
    manifest = json.loads(
        (tmp_path / "batches" / batch_id / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["run_ids"] == ["legacy_run_001"]


def test_import_baseline_batch_normalizes_missing_turn_indexes(tmp_path) -> None:
    input_path = tmp_path / "baseline.jsonl"
    input_path.write_text(
        json.dumps(
            {
                "run_id": "legacy_run_001",
                "scenario_id": "warm-check-in-basic",
                "scenario_version": "2026-03-28",
                "persona_id": "soft-spoken-slow-burn-lover",
                "persona_version": "2026-03-28",
                "model_target": {
                    "model_provider": "openrouter",
                    "model_name": "example/model-a",
                    "model_version": "provider-live",
                },
                "sampling_profile": {
                    "profile_id": "default-balanced",
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "max_tokens": 512,
                },
                "termination_reason": "max_turns_reached",
                "turns": [
                    {
                        "role": "user",
                        "content": "今晚别离我太远。",
                    },
                    {
                        "role": "assistant",
                        "content": "我在，你往我怀里靠一点。",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    import_baseline_batch(
        artifacts_root=tmp_path,
        input_path=input_path,
        batch_id="batch_imported_baseline",
    )

    transcript = json.loads(
        (tmp_path / "runs" / "legacy_run_001" / "transcript.json").read_text(
            encoding="utf-8"
        )
    )
    assert transcript["turns"][0]["turn_index"] == 1
    assert transcript["turns"][1]["turn_index"] == 2
