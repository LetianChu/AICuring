from typing import Optional

import typer

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.adapters.openrouter import OpenRouterAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.config import ARTIFACTS_ROOT, ASSETS_ROOT
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.reporting.aggregate import build_batch_report
from aicure_benchmark.reporting.render import write_report_outputs
from aicure_benchmark.runner.batch import run_batch
from aicure_benchmark.runner.engine import run_scenario


app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """CLI entrypoint for benchmark workflows."""


def _build_mock_dependencies() -> tuple[
    dict[tuple[str, str], object],
    dict[tuple[str, str], object],
    MockAdapter,
]:
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)
    return personas, scenarios, MockAdapter()


def _resolve_model_name(model_provider: str, model_name: Optional[str]) -> str:
    if model_provider == "mock":
        return model_name or "mock-companion"
    if model_provider == "openrouter":
        if model_name:
            return model_name
        raise typer.BadParameter("OpenRouter requires --model-name.")
    raise typer.BadParameter(f"Unsupported model provider: {model_provider}")


def _resolve_model_version(model_provider: str, model_version: Optional[str]) -> str:
    if model_provider == "mock":
        return model_version or "local-v1"
    if model_provider == "openrouter":
        return model_version or "openrouter-live"
    raise typer.BadParameter(f"Unsupported model provider: {model_provider}")


def _build_runtime_dependencies(
    *,
    model_provider: str,
    model_name: str,
) -> tuple[
    dict[tuple[str, str], object],
    dict[tuple[str, str], object],
    object,
]:
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)

    if model_provider == "mock":
        return personas, scenarios, MockAdapter()
    if model_provider == "openrouter":
        return personas, scenarios, OpenRouterAdapter(model_name=model_name)

    raise typer.BadParameter(f"Unsupported model provider: {model_provider}")


def _select_latest_versioned_asset(
    registry: dict[tuple[str, str], object],
    *,
    asset_id: str,
    asset_label: str,
):
    matches = [
        value
        for (candidate_id, _candidate_version), value in registry.items()
        if candidate_id == asset_id
    ]
    if not matches:
        raise typer.BadParameter(f"Unknown {asset_label}: {asset_id}")
    return max(matches, key=lambda asset: getattr(asset, f"{asset_label}_version"))


@app.command("validate-assets")
def validate_assets() -> None:
    """Validate persona and scenario assets."""
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)
    typer.echo(f"validated assets: personas={len(personas)} scenarios={len(scenarios)}")


@app.command("run-scenario")
def run_scenario_command(
    scenario_id: str,
    persona_id: str,
    model_provider: str = "mock",
    model_name: Optional[str] = None,
    model_version: Optional[str] = None,
) -> None:
    resolved_model_name = _resolve_model_name(model_provider, model_name)
    resolved_model_version = _resolve_model_version(model_provider, model_version)
    personas, scenarios, adapter = _build_runtime_dependencies(
        model_provider=model_provider,
        model_name=resolved_model_name,
    )
    scenario = _select_latest_versioned_asset(
        scenarios,
        asset_id=scenario_id,
        asset_label="scenario",
    )
    persona = _select_latest_versioned_asset(
        personas,
        asset_id=persona_id,
        asset_label="persona",
    )
    result = run_scenario(
        artifacts_root=ARTIFACTS_ROOT,
        scenario=scenario,
        persona=persona,
        adapter=adapter,
        model_target=ModelTarget(
            model_provider=model_provider,
            model_name=resolved_model_name,
            model_version=resolved_model_version,
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )
    typer.echo(f"completed run: run_id={result.run_id}")


@app.command("run-batch")
def run_batch_command(
    model_provider: str = "mock",
    model_name: Optional[str] = None,
    model_version: Optional[str] = None,
    repetitions: int = 1,
) -> None:
    resolved_model_name = _resolve_model_name(model_provider, model_name)
    resolved_model_version = _resolve_model_version(model_provider, model_version)
    personas, scenarios, adapter = _build_runtime_dependencies(
        model_provider=model_provider,
        model_name=resolved_model_name,
    )
    batch = run_batch(
        artifacts_root=ARTIFACTS_ROOT,
        scenarios=list(scenarios.values()),
        personas=list(personas.values()),
        adapter=adapter,
        model_target=ModelTarget(
            model_provider=model_provider,
            model_name=resolved_model_name,
            model_version=resolved_model_version,
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetitions=repetitions,
    )
    typer.echo(
        "completed batch: "
        f"batch_id={batch.benchmark_run_batch_id} runs={len(batch.run_results)}"
    )


@app.command("generate-report")
def generate_report_command(
    batch_id: str = typer.Option(..., "--batch-id"),
) -> None:
    report = build_batch_report(ARTIFACTS_ROOT, batch_id)
    batch_root = ARTIFACTS_ROOT / "batches" / batch_id
    markdown_path, json_path = write_report_outputs(batch_root, report)
    typer.echo(f"generated report: markdown={markdown_path} json={json_path}")


if __name__ == "__main__":
    app()
