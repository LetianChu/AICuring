import typer


app = typer.Typer(no_args_is_help=True)


@app.command("validate-assets")
def validate_assets() -> None:
    """Placeholder command until asset loaders are implemented."""
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
