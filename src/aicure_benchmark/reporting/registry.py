import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def build_baseline_registry(artifacts_root: Path) -> dict:
    report_candidates = _discover_report_candidates(artifacts_root)
    model_runs = _discover_model_runs(artifacts_root)

    model_slugs = sorted(set(report_candidates) | set(model_runs))
    models = [
        _build_registry_entry(
            model_slug=model_slug,
            report_candidates=report_candidates.get(model_slug, []),
            run_records=model_runs.get(model_slug, []),
        )
        for model_slug in model_slugs
    ]
    models.sort(key=_registry_sort_key)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_count": len(models),
        "models": models,
    }


def write_registry_outputs(output_root: Path, registry: dict) -> tuple[Path, Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    markdown_path = output_root / "baseline_registry.md"
    json_path = output_root / "baseline_registry.json"
    markdown_path.write_text(render_markdown_registry(registry), encoding="utf-8")
    json_path.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return markdown_path, json_path


def render_markdown_registry(registry: dict) -> str:
    lines = [
        "# Baseline Registry",
        "",
        f"- Generated at: {registry['generated_at']}",
        f"- Models: {registry['model_count']}",
        "",
        "| Model | Tier | Status | Runs | Overall Bucket | Current Fit |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        "| "
        + " | ".join(
            [
                item["model_slug"],
                item["tier"],
                item["status"],
                str(item["runs_total"]),
                item["overall_bucket"],
                item["current_fit"],
            ]
        )
        + " |"
        for item in registry["models"]
    )

    for item in registry["models"]:
        lines.extend(
            [
                "",
                f"## {item['model_slug']}",
                f"- Tier: {item['tier']}",
                f"- Status: {item['status']}",
                f"- Runs: {item['runs_total']}",
                f"- Overall Bucket: {item['overall_bucket']}",
                f"- Current Fit: {item['current_fit']}",
                f"- Report Paths: {', '.join(item['report_paths']) if item['report_paths'] else 'none'}",
                f"- Evidence Summary: {item['evidence_summary']}",
                "- Strengths:",
            ]
        )
        lines.extend(f"  - {strength}" for strength in item["strengths"])
        lines.append("- Weaknesses:")
        lines.extend(f"  - {weakness}" for weakness in item["weaknesses"])

    return "\n".join(lines) + "\n"


def _discover_report_candidates(artifacts_root: Path) -> dict[str, list[dict]]:
    candidates: dict[str, list[dict]] = defaultdict(list)
    for report_path in artifacts_root.rglob("report.json"):
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        models = payload.get("models_in_scope") or payload.get("scope", {}).get("models", [])
        if not models:
            continue

        by_model = {
            item["model"]: item
            for item in payload.get("by_model", [])
            if "model" in item
        }

        report_kind = _report_kind(payload, len(models))
        for model_slug in models:
            candidates[model_slug].append(
                {
                    "path": report_path.relative_to(artifacts_root).as_posix(),
                    "kind": report_kind,
                    "run_count": by_model.get(model_slug, {}).get("run_count", 0),
                    "payload": payload,
                    "model_view": by_model.get(model_slug, {}),
                }
            )
    return candidates


def _discover_model_runs(artifacts_root: Path) -> dict[str, list[dict]]:
    runs_by_model: dict[str, list[dict]] = defaultdict(list)
    for metadata_path in artifacts_root.rglob("metadata.json"):
        if metadata_path.parent.name.startswith("batch_"):
            continue

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        model_target = metadata.get("model_target") or {}
        model_slug = model_target.get("model_name")
        if not model_slug:
            continue

        judge_path = metadata_path.parent / "judge.json"
        judge_payload = None
        if judge_path.exists():
            judge_payload = json.loads(judge_path.read_text(encoding="utf-8"))

        runs_by_model[model_slug].append(
            {
                "run_id": metadata["run_id"],
                "batch_id": metadata.get("benchmark_run_batch_id"),
                "scenario_id": metadata.get("scenario_id"),
                "persona_id": metadata.get("persona_id"),
                "judge": judge_payload,
            }
        )
    return runs_by_model


def _build_registry_entry(
    *,
    model_slug: str,
    report_candidates: list[dict],
    run_records: list[dict],
) -> dict:
    primary_report = _select_primary_report(report_candidates)
    relevant_runs = list(run_records)
    runs_total = len(relevant_runs)
    batch_ids: list[str] = []
    report_paths: list[str] = []

    if primary_report:
        batch_ids = _extract_batch_ids(primary_report["payload"])
        report_paths = [primary_report["path"]]
        if batch_ids:
            filtered = [
                record
                for record in run_records
                if record.get("batch_id") in set(batch_ids)
            ]
            if filtered:
                relevant_runs = filtered

    label_counts = Counter(
        label
        for record in relevant_runs
        for label in (record.get("judge") or {}).get("event_labels", [])
    )
    degraded_scenarios = Counter(
        record["scenario_id"]
        for record in relevant_runs
        if (record.get("judge") or {}).get("overall_bucket") != "allowed_and_stable"
    )
    stable_scenarios = Counter(
        record["scenario_id"]
        for record in relevant_runs
        if (record.get("judge") or {}).get("overall_bucket") == "allowed_and_stable"
    )

    if primary_report:
        model_view = primary_report["model_view"]
        status = "completed"
        overall_bucket = model_view.get("overall_bucket", "unknown")
        current_fit = model_view.get("recommendation", "unknown")
        runs_total = model_view.get("run_count", runs_total)
    else:
        status = "partial"
        overall_bucket = _most_common(
            (record.get("judge") or {}).get("overall_bucket")
            for record in run_records
            if record.get("judge")
        ) or "unknown"
        current_fit = _most_common(
            (record.get("judge") or {}).get("recommended_product_fit")
            for record in relevant_runs
            if record.get("judge")
        ) or "unknown"
        batch_ids = sorted({record["batch_id"] for record in run_records if record.get("batch_id")})

    strengths = _build_strengths(stable_scenarios, current_fit)
    weaknesses = _build_weaknesses(degraded_scenarios, label_counts, status)

    return {
        "model_slug": model_slug,
        "tier": "free" if model_slug.endswith(":free") else "paid",
        "status": status,
        "batch_ids": batch_ids,
        "report_paths": report_paths,
        "runs_total": runs_total,
        "overall_bucket": overall_bucket,
        "current_fit": current_fit,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "evidence_summary": _build_evidence_summary(
            primary_report=primary_report,
            report_paths=report_paths,
            runs_total=runs_total,
            status=status,
        ),
    }


def _select_primary_report(report_candidates: list[dict]) -> Optional[dict]:
    if not report_candidates:
        return None
    ranked = sorted(
        report_candidates,
        key=lambda item: (
            _report_priority(item["kind"]),
            item["run_count"],
        ),
        reverse=True,
    )
    return ranked[0]


def _report_kind(payload: dict, model_count: int) -> str:
    if "comparison_scope" in payload and model_count == 1:
        return "single_model_comparison"
    if payload.get("benchmark_run_batch_id") or payload.get("batch_id"):
        return "batch_report"
    if "comparison_scope" in payload:
        return "multi_model_comparison"
    return "other"


def _report_priority(kind: str) -> int:
    if kind == "single_model_comparison":
        return 3
    if kind == "batch_report":
        return 2
    if kind == "multi_model_comparison":
        return 1
    return 0


def _extract_batch_ids(payload: dict) -> list[str]:
    if "comparison_scope" in payload:
        return list(payload["comparison_scope"].get("batch_ids", []))
    if payload.get("benchmark_run_batch_id"):
        return [payload["benchmark_run_batch_id"]]
    if payload.get("batch_id"):
        return [payload["batch_id"]]
    return []


def _build_strengths(stable_scenarios: Counter, current_fit: str) -> list[str]:
    strengths = []
    if current_fit != "unknown":
        strengths.append(f"Current fit is {current_fit}.")
    for scenario_id, count in stable_scenarios.most_common(2):
        strengths.append(f"Stable on {scenario_id} across {count} run(s).")
    return strengths or ["No stable strengths recorded yet."]


def _build_weaknesses(
    degraded_scenarios: Counter,
    label_counts: Counter,
    status: str,
) -> list[str]:
    weaknesses = []
    for scenario_id, count in degraded_scenarios.most_common(2):
        weaknesses.append(f"Degrades on {scenario_id} in {count} run(s).")
    for label, count in label_counts.most_common(2):
        weaknesses.append(f"Observed {label} {count} time(s).")
    if status == "partial":
        weaknesses.append("Only partial evidence is available so far.")
    return weaknesses or ["No major weaknesses recorded yet."]


def _build_evidence_summary(
    *,
    primary_report: Optional[dict],
    report_paths: list[str],
    runs_total: int,
    status: str,
) -> str:
    if primary_report:
        return f"Primary source {report_paths[0]} over {runs_total} run(s)."
    if status == "partial":
        return f"Partial run evidence only ({runs_total} run(s)); no completed report yet."
    return "No evidence summary available."


def _most_common(values) -> Optional[str]:
    counter = Counter(value for value in values if value)
    if not counter:
        return None
    return counter.most_common(1)[0][0]


def _registry_sort_key(entry: dict) -> tuple[int, int, str]:
    return (
        0 if entry["status"] == "completed" else 1,
        -entry["runs_total"],
        entry["model_slug"],
    )
