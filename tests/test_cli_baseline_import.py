from typer.testing import CliRunner

import aicure_benchmark.cli as cli


def test_import_baseline_command_writes_batch(monkeypatch, tmp_path) -> None:
    input_path = tmp_path / "baseline.jsonl"
    input_path.write_text("{}", encoding="utf-8")

    def fake_import_baseline_batch(*, artifacts_root, input_path, batch_id):
        assert artifacts_root == tmp_path
        assert input_path.name == "baseline.jsonl"
        assert batch_id == "batch_manual_baseline"
        return batch_id

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(
        cli,
        "import_baseline_batch",
        fake_import_baseline_batch,
        raising=False,
    )

    result = CliRunner().invoke(
        cli.app,
        [
            "import-baseline",
            "--input-path",
            str(input_path),
            "--batch-id",
            "batch_manual_baseline",
        ],
    )

    assert result.exit_code == 0
    assert "batch_manual_baseline" in result.stdout
