import csv
import json
from pathlib import Path
from typing import Optional

import typer

from src.profiler import profile_csv
from src.render import generate_json_report, generate_markdown_report

app = typer.Typer(help="CSV Profiler - Analyze and profile CSV files")


@app.command()
def profile(
    csv_file: Path = typer.Argument(
        ...,
        help="Path to the CSV file to profile",
        exists=True,
        readable=True,
    ),
    out_dir: Optional[Path] = typer.Option(
        None,
        "--out-dir",
        "-o",
        help="Output directory for generated reports",
    ),
    format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json, markdown, or both",
    ),
) -> None:
    """
    Profile a CSV file and generate statistics.

    Analyzes the CSV file and outputs profiling information including
    column types, missing values, unique counts, and basic statistics.
    """
    # Read CSV file
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Generate profile
    result = profile_csv(rows)

    # Determine output directory
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    # Generate and output reports
    if format in ("json", "both"):
        json_report = generate_json_report(result)
        if out_dir:
            json_path = out_dir / f"{csv_file.stem}_profile.json"
            json_path.write_text(json_report, encoding="utf-8")
            typer.echo(f"JSON report saved to: {json_path}")
        else:
            typer.echo(json_report)

    if format in ("markdown", "md", "both"):
        md_report = generate_markdown_report(result)
        if out_dir:
            md_path = out_dir / f"{csv_file.stem}_profile.md"
            md_path.write_text(md_report, encoding="utf-8")
            typer.echo(f"Markdown report saved to: {md_path}")
        else:
            typer.echo(md_report)

    # Summary output
    if out_dir:
        typer.echo(f"\nProfiled {result['n_rows']} rows, {result['n_cols']} columns")


@app.command()
def info(
    csv_file: Path = typer.Argument(
        ...,
        help="Path to the CSV file",
        exists=True,
        readable=True,
    ),
) -> None:
    """
    Show basic info about a CSV file without full profiling.
    """
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if rows:
        columns = list(rows[0].keys())
        typer.echo(f"File: {csv_file}")
        typer.echo(f"Rows: {len(rows)}")
        typer.echo(f"Columns: {len(columns)}")
        typer.echo(f"Column names: {', '.join(columns)}")
    else:
        typer.echo("Empty CSV file")


if __name__ == "__main__":
    app()
