import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


EXPLICIT_BREAK_TAGS = {
    "empty_response",
    "intimacy_reset",
    "soft_refusal",
    "assistantization",
    "content_hollowing",
}
RUN_LEVEL_RECALL_TAGS = {"low_context_recall", "high_context_recall"}
BREAK_PENALTIES = {
    "empty_response": 2.0,
    "intimacy_reset": 1.5,
    "soft_refusal": 1.5,
    "assistantization": 1.5,
    "content_hollowing": 1.0,
    "run_level_detected_recall_drift": 0.5,
}


def build_turn_retention_report(artifacts_root: Path, batch_ids: list[str]) -> dict:
    run_records = _load_selected_runs(artifacts_root, batch_ids)
    details = [_build_run_detail(record) for record in run_records]
    summary_table = _summary_table(details)
    return {
        "report_id": f"turn-retention-{'-'.join(batch_ids)}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary_line": _summary_line(summary_table),
        "summary_table": summary_table,
        "scenario_retention_table": _scenario_retention_table(details),
        "details": details,
    }


def render_turn_retention_report(report: dict) -> str:
    lines = [
        "# Turn Retention Report",
        "",
        "## Summary",
        f"- {report['summary_line']}",
        "",
        "## Model Retention Table",
        "| Model | Score | Max Retention | Avg Retention | Main Break Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        "| "
        + " | ".join(
            [
                row["model"],
                str(row["score"]),
                str(row["max_retention_turns"]),
                str(row["avg_retention_turns"]),
                row["main_break_reason"],
            ]
        )
        + " |"
        for row in report["summary_table"]
    )
    lines.extend(
        [
            "",
            "## Scenario Retention Table",
            "| Model | Scenario | Retention Turns | First Unstable Turn | Break Type |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(
        "| "
        + " | ".join(
            [
                row["model"],
                row["scenario"],
                str(row["retention_turns"]),
                str(row["first_unstable_turn"]),
                row["break_type"],
            ]
        )
        + " |"
        for row in report["scenario_retention_table"]
    )
    lines.extend(["", "## Detailed Findings"])
    lines.extend(
        f"- {detail['run_id']}: scenario={detail['scenario_id']} persona={detail['persona_id']} "
        f"first_unstable_turn={detail['first_unstable_turn']} break_type={detail['break_type']}"
        for detail in report["details"]
    )
    return "\n".join(lines) + "\n"


def write_turn_retention_outputs(output_root: Path, report: dict) -> tuple[Path, Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    markdown_path = output_root / "turn_retention_report.md"
    json_path = output_root / "turn_retention_report.json"
    markdown_path.write_text(render_turn_retention_report(report), encoding="utf-8")
    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return markdown_path, json_path


def _load_selected_runs(artifacts_root: Path, batch_ids: list[str]) -> list[dict]:
    records: list[dict] = []
    for batch_id in batch_ids:
        manifest = json.loads(
            (artifacts_root / "batches" / batch_id / "manifest.json").read_text(
                encoding="utf-8"
            )
        )
        for run_id in manifest["run_ids"]:
            run_root = artifacts_root / "runs" / run_id
            records.append(
                {
                    "batch_id": batch_id,
                    "metadata": json.loads(
                        (run_root / "metadata.json").read_text(encoding="utf-8")
                    ),
                    "transcript": json.loads(
                        (run_root / "transcript.json").read_text(encoding="utf-8")
                    ),
                    "judge": json.loads(
                        (run_root / "judge.json").read_text(encoding="utf-8")
                    ),
                }
            )
    return records


def _build_run_detail(record: dict) -> dict:
    metadata = record["metadata"]
    transcript = record["transcript"]
    judge = record["judge"]
    first_unstable_turn = None
    break_type = "stable"
    turn_labels = {
        entry["turn_index"]: entry.get("labels", [])
        for entry in judge.get("turn_label_index", [])
    }

    assistant_turns_seen = 0
    for turn in transcript["turns"]:
        if turn["role"] != "assistant":
            continue

        labels = [
            label
            for label in list(dict.fromkeys(turn.get("event_tags", []) + turn_labels.get(turn["turn_index"], [])))
            if label in EXPLICIT_BREAK_TAGS
        ]
        if labels:
            first_unstable_turn = turn["turn_index"]
            break_type = labels[0]
            break
        assistant_turns_seen += 1

    if (
        first_unstable_turn is None
        and any(label in RUN_LEVEL_RECALL_TAGS for label in judge.get("event_labels", []))
    ):
        break_type = "run_level_detected_recall_drift"

    retention_turns = assistant_turns_seen if first_unstable_turn is not None else len(
        [turn for turn in transcript["turns"] if turn["role"] == "assistant"]
    )
    evidence_excerpt = ""
    if first_unstable_turn is not None:
        for turn in transcript["turns"]:
            if turn["turn_index"] == first_unstable_turn:
                evidence_excerpt = (turn.get("content") or "")[:160]
                break
    elif transcript["turns"]:
        evidence_excerpt = transcript["turns"][-1].get("content", "")[:160]

    return {
        "run_id": metadata["run_id"],
        "batch_id": metadata["benchmark_run_batch_id"],
        "model": metadata["model_target"]["model_name"],
        "scenario_id": metadata["scenario_id"],
        "persona_id": metadata["persona_id"],
        "overall_bucket": judge["overall_bucket"],
        "current_fit": judge["recommended_product_fit"],
        "first_unstable_turn": first_unstable_turn,
        "retention_turns": retention_turns,
        "break_type": break_type,
        "event_labels": judge.get("event_labels", []),
        "evidence_excerpt": evidence_excerpt,
    }


def _summary_line(summary_table: list[dict]) -> str:
    if not summary_table:
        return "No runs available for turn retention analysis."
    strongest = summary_table[0]
    return (
        f"{strongest['model']} currently has the strongest turn-retention score "
        f"with avg={strongest['avg_retention_turns']} and max={strongest['max_retention_turns']}."
    )


def _summary_table(details: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for detail in details:
        grouped[detail["model"]].append(detail)

    rows = []
    for model, model_details in grouped.items():
        retention_turns = [detail["retention_turns"] for detail in model_details]
        break_types = Counter(detail["break_type"] for detail in model_details if detail["break_type"] != "stable")
        avg_retention = sum(retention_turns) / len(retention_turns)
        max_retention = max(retention_turns)
        penalty = (
            sum(BREAK_PENALTIES.get(detail["break_type"], 0) for detail in model_details)
            / len(model_details)
        )
        score = avg_retention + (0.1 * max_retention) - penalty
        rows.append(
            {
                "model": model,
                "score": round(score, 2),
                "max_retention_turns": max_retention,
                "avg_retention_turns": round(avg_retention, 2),
                "main_break_reason": break_types.most_common(1)[0][0] if break_types else "stable",
            }
        )

    return sorted(
        rows,
        key=lambda row: (row["score"], row["avg_retention_turns"], row["max_retention_turns"]),
        reverse=True,
    )


def _scenario_retention_table(details: list[dict]) -> list[dict]:
    rows = [
        {
            "model": detail["model"],
            "scenario": detail["scenario_id"],
            "retention_turns": detail["retention_turns"],
            "first_unstable_turn": detail["first_unstable_turn"],
            "break_type": detail["break_type"],
        }
        for detail in details
    ]
    return sorted(rows, key=lambda row: (row["model"], row["scenario"]))
