import typer

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.config import ASSETS_ROOT


app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """CLI entrypoint for benchmark workflows."""


@app.command("validate-assets")
def validate_assets() -> None:
    """Validate persona and scenario assets."""
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)
    typer.echo(f"validated assets: personas={len(personas)} scenarios={len(scenarios)}")


if __name__ == "__main__":
    app()
