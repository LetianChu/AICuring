from typer.testing import CliRunner

from aicure_benchmark.cli import app


def test_cli_help_renders() -> None:
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "validate-assets" in result.stdout
