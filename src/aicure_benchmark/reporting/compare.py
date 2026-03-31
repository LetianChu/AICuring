import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from aicure_benchmark.judge.service import judge_run


def build_comparison_report(artifacts_root: Path, batch_ids: list[str]) -> dict:
    run_records = _load_run_records(artifacts_root, batch_ids)
    by_model = _aggregate_by_model(run_records)
    by_scenario = _aggregate_by_field(run_records, "scenario_id")
    by_persona = _aggregate_by_field(run_records, "persona_id")
    failure_modes = Counter(
        label
        for record in run_records
        for label in record["judge"].get("primary_failure_modes", [])
    )
    routing_recommendation = _routing_recommendation(run_records)
    evidence_index = [
        f'{record["judge"]["run_id"]} turn_{evidence["turn_index"]}'
        for record in run_records
        for evidence in record["judge"].get("evidence_links", [])
    ]
    models_in_scope = sorted(
        {record["metadata"]["model_target"]["model_name"] for record in run_records}
    )
    personas_in_scope = sorted({record["metadata"]["persona_id"] for record in run_records})
    scenarios_in_scope = sorted({record["metadata"]["scenario_id"] for record in run_records})

    return {
        "report_id": f"comparison-{'-'.join(batch_ids)}",
        "report_version": "2026-03-31",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "comparison_scope": {"batch_ids": batch_ids},
        "summary_lines": [
            f"Compared {len(batch_ids)} batch(es) across {len(models_in_scope)} model(s).",
            f"Routing recommendation: {routing_recommendation}.",
        ],
        "scope": {
            "models": models_in_scope,
            "personas": personas_in_scope,
            "scenarios": scenarios_in_scope,
            "repetitions": sum(record.get("manifest_repetitions", 1) for record in run_records),
        },
        "models_in_scope": models_in_scope,
        "personas_in_scope": personas_in_scope,
        "scenarios_in_scope": scenarios_in_scope,
        "by_model": by_model,
        "by_scenario": by_scenario,
        "by_persona": by_persona,
        "failure_modes": [label for label, _count in failure_modes.most_common()],
        "routing_recommendation": routing_recommendation,
        "evidence_index": evidence_index,
    }


def _load_run_records(artifacts_root: Path, batch_ids: list[str]) -> list[dict]:
    run_records: list[dict] = []
    for batch_id in batch_ids:
        batch_root = artifacts_root / "batches" / batch_id
        manifest = json.loads((batch_root / "manifest.json").read_text(encoding="utf-8"))
        for run_id in manifest["run_ids"]:
            run_root = artifacts_root / "runs" / run_id
            metadata = json.loads((run_root / "metadata.json").read_text(encoding="utf-8"))
            judge_path = run_root / "judge.json"
            if judge_path.exists():
                judge_payload = json.loads(judge_path.read_text(encoding="utf-8"))
            else:
                judge_payload = judge_run(run_root).model_dump()
            run_records.append(
                {
                    "metadata": metadata,
                    "judge": judge_payload,
                    "batch_id": batch_id,
                    "manifest_repetitions": manifest.get("repetitions", 1),
                }
            )
    return run_records


def _aggregate_by_model(run_records: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in run_records:
        grouped[record["metadata"]["model_target"]["model_name"]].append(record)

    results = []
    for model_name, records in grouped.items():
        fits = Counter(record["judge"]["recommended_product_fit"] for record in records)
        buckets = Counter(record["judge"]["overall_bucket"] for record in records)
        failure_modes = Counter(
            label
            for record in records
            for label in (
                record["judge"].get("primary_failure_modes")
                or record["judge"].get("event_labels", [])
            )
        )
        avg_scores = _average_dimension_scores(records)
        results.append(
            {
                "model": model_name,
                "overall_bucket": buckets.most_common(1)[0][0],
                "recommendation": fits.most_common(1)[0][0],
                "best_use_case": _best_use_case(fits.most_common(1)[0][0]),
                "worst_failure_mode": failure_modes.most_common(1)[0][0]
                if failure_modes
                else "none",
                "avg_dimension_scores": avg_scores,
                "volatility": _comparison_volatility(records, avg_scores["volatility"]),
                "run_count": len(records),
                "batch_coverage": sorted({record["batch_id"] for record in records}),
            }
        )

    return sorted(
        results,
        key=lambda item: (
            _fit_rank(item["recommendation"]),
            item["avg_dimension_scores"]["conversation_usefulness"],
            item["avg_dimension_scores"]["persona_consistency"],
        ),
        reverse=True,
    )


def _aggregate_by_field(run_records: list[dict], field_name: str) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in run_records:
        grouped[record["metadata"][field_name]].append(record)

    results = []
    for field_value, records in grouped.items():
        buckets = Counter(record["judge"]["overall_bucket"] for record in records)
        common_failure = Counter(
            label
            for record in records
            for label in (
                record["judge"].get("primary_failure_modes")
                or record["judge"].get("event_labels", [])
            )
        )
        avg_scores = _average_dimension_scores(records)
        results.append(
            {
                "name": field_value,
                "overall_bucket": buckets.most_common(1)[0][0],
                "avg_score": round(sum(avg_scores.values()) / len(avg_scores)) if avg_scores else 0,
                "common_failure": common_failure.most_common(1)[0][0] if common_failure else "none",
                "recovery_pattern": _recovery_pattern(records),
                "decision_signal": buckets.most_common(1)[0][0],
                "run_count": len(records),
            }
        )
    return sorted(results, key=lambda item: item["name"])


def _average_dimension_scores(records: list[dict]) -> dict[str, int]:
    dimensions = records[0]["judge"]["dimension_scores"].keys()
    return {
        dimension: round(
            sum(record["judge"]["dimension_scores"][dimension] for record in records)
            / len(records)
        )
        for dimension in dimensions
    }


def _comparison_volatility(records: list[dict], average_volatility: int) -> int:
    bucket_count = len({record["judge"]["overall_bucket"] for record in records})
    fit_count = len({record["judge"]["recommended_product_fit"] for record in records})
    if bucket_count > 1 or fit_count > 1:
        return min(average_volatility, 2)
    return average_volatility


def _recovery_pattern(records: list[dict]) -> str:
    labels = {
        label
        for record in records
        for label in record["judge"].get("event_labels", [])
    }
    if "successful_recovery" in labels:
        return "successful_recovery_seen"
    if "failed_recovery" in labels:
        return "failed_recovery_seen"
    return "no_recovery_signal"


def _routing_recommendation(run_records: list[dict]) -> str:
    fits = {record["judge"]["recommended_product_fit"] for record in run_records}
    if "warm_companion_only" in fits and "candidate_for_erp_layer" in fits:
        return "companion_and_erp_split_recommended"
    if fits == {"candidate_for_erp_layer"}:
        return "single_model_candidate"
    if "not_recommended" in fits and len(fits) == 1:
        return "not_ready_for_product_validation"
    return "companion_only_candidate"


def _fit_rank(recommendation: str) -> int:
    if recommendation == "candidate_for_erp_layer":
        return 4
    if recommendation == "companion_plus_romantic":
        return 3
    if recommendation == "warm_companion_only":
        return 2
    return 1


def _best_use_case(recommendation: str) -> str:
    if recommendation == "candidate_for_erp_layer":
        return "erp_request_handling"
    if recommendation == "companion_plus_romantic":
        return "romantic_escalation"
    if recommendation == "warm_companion_only":
        return "warm_companion"
    return "not_ready"
