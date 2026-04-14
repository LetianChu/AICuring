import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import statistics
from typing import Optional

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.judge.service import judge_run


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


def build_turn_retention_report(
    artifacts_root: Path,
    batch_ids: list[str],
    scenario_tag: Optional[str] = None,
) -> dict:
    run_records = _load_selected_runs(artifacts_root, batch_ids, scenario_tag=scenario_tag)
    details = [_build_run_detail(record) for record in run_records]
    summary_table = _summary_table(details)
    return {
        "report_id": _build_report_id(batch_ids, scenario_tag),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary_line": _summary_line(summary_table),
        "summary_table": summary_table,
        "intermediate_data": _intermediate_data(details),
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
    lines.extend(["", "## Intermediate Data"])
    for item in report["intermediate_data"]:
        lines.extend(
            [
                f"### {item['model']}",
                f"- Run Count: {item['run_count']}",
                f"- Batch Count: {item['batch_count']}",
                f"- Scenario Count: {item['scenario_count']}",
                f"- Persona Count: {item['persona_count']}",
                f"- Retention Turns: {item['retention_turns']}",
                f"- Max Possible Retention Turns: {item.get('max_possible_retention_turns', [])}",
                f"- Late Stage Retention Turns: {item.get('late_stage_retention_turns', [])}",
                f"- Soft Degradation Round Counts: {item.get('soft_degradation_round_counts', [])}",
                (
                    "- Retention Stats: "
                    f"min={item['retention_stats']['min']} "
                    f"median={item['retention_stats']['median']} "
                    f"max={item['retention_stats']['max']} "
                    f"avg={item['retention_stats']['avg']}"
                ),
                f"- Break Type Counts: {item['break_type_counts']}",
                f"- First Unstable Turn Counts: {item['first_unstable_turn_counts']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Scenario Retention Table",
            "| Model | Scenario | Retention Turns | Max Possible Retention | First Unstable Turn | Break Type |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(
        "| "
        + " | ".join(
            [
                row["model"],
                row["scenario"],
                str(row["retention_turns"]),
                str(row.get("max_possible_retention_turns", "")),
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


def _load_selected_runs(
    artifacts_root: Path,
    batch_ids: list[str],
    *,
    scenario_tag: Optional[str] = None,
) -> list[dict]:
    allowed_scenario_ids = _allowed_scenario_ids_for_tag(scenario_tag)
    records: list[dict] = []
    for batch_id in batch_ids:
        manifest = json.loads(
            (artifacts_root / "batches" / batch_id / "manifest.json").read_text(
                encoding="utf-8"
            )
        )
        for run_id in manifest["run_ids"]:
            run_root = artifacts_root / "runs" / run_id
            metadata = json.loads(
                (run_root / "metadata.json").read_text(encoding="utf-8")
            )
            if allowed_scenario_ids is not None and metadata["scenario_id"] not in allowed_scenario_ids:
                continue
            records.append(
                {
                    "batch_id": batch_id,
                    "metadata": metadata,
                    "transcript": json.loads(
                        (run_root / "transcript.json").read_text(encoding="utf-8")
                    ),
                    "judge": (
                        json.loads((run_root / "judge.json").read_text(encoding="utf-8"))
                        if (run_root / "judge.json").exists()
                        else judge_run(run_root).model_dump()
                    ),
                }
            )
    return records


def _allowed_scenario_ids_for_tag(scenario_tag: Optional[str]) -> Optional[set[str]]:
    if not scenario_tag:
        return None
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    return {
        scenario.scenario_id
        for scenario in scenarios.values()
        if scenario_tag in scenario.benchmark_tags
    }


def _build_report_id(batch_ids: list[str], scenario_tag: Optional[str]) -> str:
    base = f"turn-retention-{'-'.join(batch_ids)}"
    if scenario_tag:
        return f"{base}-{scenario_tag}"
    return base


def _build_run_detail(record: dict) -> dict:
    metadata = record["metadata"]
    transcript = record["transcript"]
    judge = record["judge"]
    first_unstable_turn = None
    break_type = "stable"
    script_mode = metadata.get("script_mode", "turn_script")
    turn_labels = {
        entry["turn_index"]: entry.get("labels", [])
        for entry in judge.get("turn_label_index", [])
    }

    assistant_turns_seen = 0
    assistant_turns_total = len([turn for turn in transcript["turns"] if turn["role"] == "assistant"])
    unstable_assistant_position = None
    unstable_transcript_turn_index = None
    for turn in transcript["turns"]:
        if turn["role"] != "assistant":
            continue

        labels = [
            label
            for label in list(dict.fromkeys(turn.get("event_tags", []) + turn_labels.get(turn["turn_index"], [])))
            if label in EXPLICIT_BREAK_TAGS
        ]
        if labels:
            break_type = labels[0]
            unstable_assistant_position = assistant_turns_seen + 1
            unstable_transcript_turn_index = turn["turn_index"]
            first_unstable_turn = (
                unstable_assistant_position
                if script_mode == "round_script"
                else turn["turn_index"]
            )
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
    max_possible_retention_turns = metadata.get("max_rounds") or assistant_turns_total
    soft_degradation_labels = {
        "assistantization",
        "content_hollowing",
        "soft_refusal",
        "intimacy_reset",
    }
    soft_degradation_round_count = 0
    for turn in transcript["turns"]:
        if turn["role"] != "assistant":
            continue
        labels = set(
            dict.fromkeys(turn.get("event_tags", []) + turn_labels.get(turn["turn_index"], []))
        )
        if labels.intersection(soft_degradation_labels):
            soft_degradation_round_count += 1
    late_stage_retention_turns = 0
    if max_possible_retention_turns >= 50:
        total_late_stage_assistant_turns = 0
        assistant_position = 0
        for turn in transcript["turns"]:
            if turn["role"] != "assistant":
                continue
            assistant_position += 1
            if assistant_position >= 31:
                total_late_stage_assistant_turns += 1
        late_stage_retention_turns = total_late_stage_assistant_turns
    evidence_excerpt = ""
    if unstable_transcript_turn_index is not None:
        for turn in transcript["turns"]:
            if turn["turn_index"] == unstable_transcript_turn_index:
                evidence_excerpt = (turn.get("content") or "")[:160]
                break
    elif transcript["turns"]:
        evidence_excerpt = transcript["turns"][-1].get("content", "")[:160]

    break_phase = "stable"
    if break_type == "run_level_detected_recall_drift":
        break_phase = "run_level"
    elif unstable_assistant_position is not None and max_possible_retention_turns:
        if max_possible_retention_turns >= 50:
            if unstable_assistant_position <= 10:
                break_phase = "early"
            elif unstable_assistant_position <= 20:
                break_phase = "build"
            elif unstable_assistant_position <= 30:
                break_phase = "sustain"
            elif unstable_assistant_position <= 40:
                break_phase = "drift_zone"
            else:
                break_phase = "late_endurance"
        else:
            ratio = unstable_assistant_position / max_possible_retention_turns
            if ratio <= (1 / 3):
                break_phase = "early"
            elif ratio <= (2 / 3):
                break_phase = "mid"
            else:
                break_phase = "late"

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
        "max_possible_retention_turns": max_possible_retention_turns,
        "late_stage_retention_turns": late_stage_retention_turns,
        "soft_degradation_round_count": soft_degradation_round_count,
        "break_type": break_type,
        "break_phase": break_phase,
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
            "max_possible_retention_turns": detail["max_possible_retention_turns"],
            "first_unstable_turn": detail["first_unstable_turn"],
            "break_type": detail["break_type"],
        }
        for detail in details
    ]
    return sorted(rows, key=lambda row: (row["model"], row["scenario"]))


def _intermediate_data(details: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for detail in details:
        grouped[detail["model"]].append(detail)

    rows = []
    for model, model_details in grouped.items():
        retention_turns = [detail["retention_turns"] for detail in model_details]
        max_possible_retention_turns = [
            detail["max_possible_retention_turns"] for detail in model_details
        ]
        late_stage_retention_turns = [
            detail["late_stage_retention_turns"] for detail in model_details
        ]
        soft_degradation_round_counts = [
            detail["soft_degradation_round_count"] for detail in model_details
        ]
        first_unstable_turn_counts = Counter(
            str(detail["first_unstable_turn"])
            for detail in model_details
            if detail["first_unstable_turn"] is not None
        )
        break_type_counts = Counter(
            detail["break_type"] for detail in model_details if detail["break_type"] != "stable"
        )
        rows.append(
            {
                "model": model,
                "run_count": len(model_details),
                "batch_count": len({detail["batch_id"] for detail in model_details}),
                "scenario_count": len({detail["scenario_id"] for detail in model_details}),
                "persona_count": len({detail["persona_id"] for detail in model_details}),
                "retention_turns": retention_turns,
                "max_possible_retention_turns": max_possible_retention_turns,
                "late_stage_retention_turns": late_stage_retention_turns,
                "soft_degradation_round_counts": soft_degradation_round_counts,
                "retention_stats": {
                    "min": min(retention_turns),
                    "median": statistics.median(retention_turns),
                    "max": max(retention_turns),
                    "avg": round(sum(retention_turns) / len(retention_turns), 2),
                },
                "break_type_counts": dict(break_type_counts),
                "first_unstable_turn_counts": dict(first_unstable_turn_counts),
            }
        )
    return sorted(rows, key=lambda row: row["model"])
