import json
from pathlib import Path


def render_markdown_report(report: dict) -> str:
    lines = [
        f"# Benchmark Report: {report['report_id']}",
        "",
        "## Executive Summary",
    ]
    lines.extend(f"- {line}" for line in report["summary_lines"])
    lines.extend(
        [
            "",
            "## Experiment Scope and Configuration",
            f"- Models: {', '.join(report['scope']['models'])}",
            f"- Personas: {', '.join(report['scope']['personas'])}",
            f"- Scenarios: {', '.join(report['scope']['scenarios'])}",
            f"- Repetitions: {report['scope']['repetitions']}",
            "",
            "## Results by Model",
        ]
    )
    lines.extend(
        f"- {item['model']}: bucket={item['overall_bucket']} recommendation={item['recommendation']} runs={item.get('run_count', 'n/a')}"
        for item in report["by_model"]
    )
    lines.append("")
    lines.append("## Results by Scenario")
    lines.extend(
        f"- {item['name']}: bucket={item['overall_bucket']} runs={item.get('run_count', 'n/a')}"
        for item in report["by_scenario"]
    )
    lines.append("")
    lines.append("## Results by Persona")
    lines.extend(
        f"- {item['name']}: bucket={item['overall_bucket']} runs={item.get('run_count', 'n/a')}"
        for item in report["by_persona"]
    )
    lines.append("")
    lines.append("## Failure Mode Analysis")
    lines.extend(f"- {label}" for label in report["failure_modes"])
    lines.append("")
    lines.append("## Routing Recommendation")
    lines.append(f"- {report['routing_recommendation']}")
    lines.append("")
    lines.append("## Appendix and Evidence Index")
    lines.extend(f"- {item}" for item in report["evidence_index"])

    return "\n".join(lines) + "\n"


def write_report_outputs(batch_root: Path, report: dict) -> tuple[Path, Path]:
    markdown_path = batch_root / "report.md"
    json_path = batch_root / "report.json"
    markdown_path.write_text(render_markdown_report(report), encoding="utf-8")
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return markdown_path, json_path
