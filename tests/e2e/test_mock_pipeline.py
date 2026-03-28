from aicure_benchmark.reporting.aggregate import build_batch_report
from aicure_benchmark.reporting.render import write_report_outputs
from aicure_benchmark.runner.batch import run_batch


def test_mock_pipeline_generates_report(tmp_artifacts_root, seed_registry) -> None:
    batch = run_batch(
        artifacts_root=tmp_artifacts_root,
        scenarios=list(seed_registry.scenarios.values()),
        personas=list(seed_registry.personas.values()),
        adapter=seed_registry.adapter,
        model_target=seed_registry.model_target,
        sampling_profile=seed_registry.sampling_profile,
        repetitions=1,
    )

    expected_scenario_ids = {scenario.scenario_id for scenario in seed_registry.scenarios.values()}
    assert len(batch.run_results) == len(expected_scenario_ids)
    observed_scenario_ids = {result.scenario_id for result in batch.run_results}
    assert observed_scenario_ids == expected_scenario_ids

    report = build_batch_report(tmp_artifacts_root, batch.benchmark_run_batch_id)
    batch_root = tmp_artifacts_root / "batches" / batch.benchmark_run_batch_id
    report_path, _ = write_report_outputs(batch_root, report)

    assert report_path.exists()
    assert "Routing Recommendation" in report_path.read_text(encoding="utf-8")
