import typer

from aicure_benchmark.adapters.mock import MockAdapter
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
    model_name: str = "mock-companion",
    model_version: str = "local-v1",
) -> None:
    if model_provider != "mock":
        raise typer.BadParameter("Only the mock adapter is supported in the MVP.")

    personas, scenarios, adapter = _build_mock_dependencies()
    scenario = scenarios[(scenario_id, "2026-03-28")]
    persona = personas[(persona_id, "2026-03-28")]
    result = run_scenario(
        artifacts_root=ARTIFACTS_ROOT,
        scenario=scenario,
        persona=persona,
        adapter=adapter,
        model_target=ModelTarget(
            model_provider=model_provider,
            model_name=model_name,
            model_version=model_version,
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )
    typer.echo(f"completed run: run_id={result.run_id}")


@app.command("run-batch")
def run_batch_command(
    model_provider: str = "mock",
    model_name: str = "mock-companion",
    model_version: str = "local-v1",
    repetitions: int = 1,
) -> None:
    if model_provider != "mock":
        raise typer.BadParameter("Only the mock adapter is supported in the MVP.")

    personas, scenarios, adapter = _build_mock_dependencies()
    batch = run_batch(
        artifacts_root=ARTIFACTS_ROOT,
        scenarios=list(scenarios.values()),
        personas=list(personas.values()),
        adapter=adapter,
        model_target=ModelTarget(
            model_provider=model_provider,
            model_name=model_name,
            model_version=model_version,
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
