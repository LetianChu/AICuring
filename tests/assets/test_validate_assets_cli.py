from typer.testing import CliRunner

from aicure_benchmark.cli import app


def test_validate_assets_command_passes_for_seed_assets() -> None:
    result = CliRunner().invoke(app, ["validate-assets"])

    assert result.exit_code == 0
    assert "personas=3" in result.stdout
    assert "scenarios=7" in result.stdout
