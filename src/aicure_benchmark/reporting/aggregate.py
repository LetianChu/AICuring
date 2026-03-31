import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from aicure_benchmark.judge.service import judge_run


def build_batch_report(artifacts_root: Path, batch_id: str) -> dict:
    batch_root = artifacts_root / "batches" / batch_id
    manifest = json.loads((batch_root / "manifest.json").read_text(encoding="utf-8"))

    run_records = []
    for run_id in manifest["run_ids"]:
        run_root = artifacts_root / "runs" / run_id
        metadata = json.loads((run_root / "metadata.json").read_text(encoding="utf-8"))
        judge_payload = judge_run(run_root).model_dump()
        run_records.append({"metadata": metadata, "judge": judge_payload})

    by_model = _aggregate_by_model(run_records)
    by_scenario = _aggregate_by_field(run_records, "scenario_id")
    by_persona = _aggregate_by_field(run_records, "persona_id")
    failure_modes = Counter(
        label
        for record in run_records
        for label in record["judge"].get("primary_failure_modes", [])
    )
    routing_recommendation = _routing_recommendation(run_records)
    summary_lines = _summary_lines(by_model, routing_recommendation)
    evidence_index = [
        f'{record["judge"]["run_id"]} turn_{evidence["turn_index"]}'
        for record in run_records
        for evidence in record["judge"].get("evidence_links", [])
    ]
    rubric_id = run_records[0]["judge"]["rubric_id"] if run_records else "adult-companion-benchmark-core"
    rubric_version = run_records[0]["judge"]["rubric_version"] if run_records else "2026-03-28"
    models_in_scope = sorted(
        {record["metadata"]["model_target"]["model_name"] for record in run_records}
    )
    personas_in_scope = sorted({record["metadata"]["persona_id"] for record in run_records})
    scenarios_in_scope = sorted({record["metadata"]["scenario_id"] for record in run_records})

    return {
        "report_id": f"report-{batch_id}",
        "report_version": "2026-03-31",
        "batch_id": batch_id,
        "benchmark_run_batch_id": batch_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rubric_id": rubric_id,
        "rubric_version": rubric_version,
        "models_in_scope": models_in_scope,
        "personas_in_scope": personas_in_scope,
        "scenarios_in_scope": scenarios_in_scope,
        "summary_lines": summary_lines,
        "scope": {
            "models": models_in_scope,
            "personas": personas_in_scope,
            "scenarios": scenarios_in_scope,
            "repetitions": manifest["repetitions"],
        },
        "by_model": by_model,
        "by_scenario": by_scenario,
        "by_persona": by_persona,
        "failure_modes": [label for label, _ in failure_modes.most_common()],
        "routing_recommendation": routing_recommendation,
        "evidence_index": evidence_index,
    }


def _aggregate_by_model(run_records: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in run_records:
        model_name = record["metadata"]["model_target"]["model_name"]
        grouped[model_name].append(record)

    results = []
    for model_name, records in grouped.items():
        buckets = Counter(record["judge"]["overall_bucket"] for record in records)
        fits = Counter(record["judge"]["recommended_product_fit"] for record in records)
        failure_modes = Counter(
            label
            for record in records
            for label in (
                record["judge"].get("primary_failure_modes")
                or record["judge"].get("event_labels", [])
            )
        )
        results.append(
            {
                "model": model_name,
                "overall_bucket": buckets.most_common(1)[0][0],
                "recommendation": fits.most_common(1)[0][0],
                "best_use_case": _best_use_case(fits.most_common(1)[0][0]),
                "worst_failure_mode": failure_modes.most_common(1)[0][0]
                if failure_modes
                else "none",
                "avg_dimension_scores": _average_dimension_scores(records),
                "volatility": _average_dimension_score(records, "volatility"),
                "run_count": len(records),
            }
        )
    return results


def _aggregate_by_field(run_records: list[dict], field_name: str) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in run_records:
        grouped[record["metadata"][field_name]].append(record)

    results = []
    for field_value, records in grouped.items():
        buckets = Counter(record["judge"]["overall_bucket"] for record in records)
        results.append(
            {
                "name": field_value,
                "overall_bucket": buckets.most_common(1)[0][0],
                "run_count": len(records),
            }
        )
    return results


def _routing_recommendation(run_records: list[dict]) -> str:
    fits = {record["judge"]["recommended_product_fit"] for record in run_records}

    if "warm_companion_only" in fits and "candidate_for_erp_layer" in fits:
        return "companion_and_erp_split_recommended"
    if fits == {"candidate_for_erp_layer"}:
        return "single_model_candidate"
    if "not_recommended" in fits and len(fits) == 1:
        return "not_ready_for_product_validation"
    return "companion_only_candidate"


def _summary_lines(by_model: list[dict], routing_recommendation: str) -> list[str]:
    if not by_model:
        return ["No run data found for this batch."]

    strongest_model = by_model[0]["model"]
    return [
        f"{strongest_model} is currently the only evaluated model in this batch.",
        f"Routing recommendation: {routing_recommendation}.",
    ]


def _average_dimension_scores(records: list[dict]) -> dict[str, int]:
    if not records:
        return {}

    dimensions = records[0]["judge"]["dimension_scores"].keys()
    return {
        dimension: _average_dimension_score(records, dimension)
        for dimension in dimensions
    }


def _average_dimension_score(records: list[dict], dimension: str) -> int:
    if not records:
        return 0
    total = sum(record["judge"]["dimension_scores"][dimension] for record in records)
    return round(total / len(records))


def _best_use_case(recommendation: str) -> str:
    if recommendation == "candidate_for_erp_layer":
        return "erp_request_handling"
    if recommendation == "companion_plus_romantic":
        return "romantic_escalation"
    if recommendation == "warm_companion_only":
        return "warm_companion"
    return "not_ready"
