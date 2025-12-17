"""Command-line interface for CSV Profiler."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from .io import read_csv_file
from .profiler import profile_csv
from .render import generate_json_report, generate_markdown_report

# Create the CLI app
app = typer.Typer(help="CSV Profiler - Analyze and profile CSV files")


@app.command()
def profile(
    csv_file: Path = typer.Argument(..., help="Path to the CSV file to profile", exists=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o", help="Output directory for reports"),
    format: str = typer.Option("json", "--format", "-f", help="Output format: json, markdown, or both"),
) -> None:
    """Profile a CSV file and generate statistics."""
    # Read and profile the CSV
    rows = read_csv_file(csv_file)
    result = profile_csv(rows)

    # Create output directory if specified
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    # Output JSON report
    if format in ("json", "both"):
        json_report = generate_json_report(result)
        if out_dir:
            path = out_dir / f"{csv_file.stem}_profile.json"
            path.write_text(json_report, encoding="utf-8")
            typer.echo(f"JSON report saved to: {path}")
        else:
            typer.echo(json_report)

    # Output Markdown report
    if format in ("markdown", "md", "both"):
        md_report = generate_markdown_report(result)
        if out_dir:
            path = out_dir / f"{csv_file.stem}_profile.md"
            path.write_text(md_report, encoding="utf-8")
            typer.echo(f"Markdown report saved to: {path}")
        else:
            typer.echo(md_report)

    # Print summary when saving to files
    if out_dir:
        typer.echo(f"\nProfiled {result['n_rows']} rows, {result['n_cols']} columns")


@app.command()
def info(
    csv_file: Path = typer.Argument(..., help="Path to the CSV file", exists=True),
) -> None:
    """Show basic info about a CSV file without full profiling."""
    rows = read_csv_file(csv_file)

    if rows:
        columns = list(rows[0].keys())
        typer.echo(f"File: {csv_file}")
        typer.echo(f"Rows: {len(rows)}")
        typer.echo(f"Columns: {len(columns)}")
        typer.echo(f"Column names: {', '.join(columns)}")
    else:
        typer.echo("Empty CSV file")


@app.command()
def web() -> None:
    """Launch the Streamlit web interface."""
    # Get path to app.py relative to this module
    app_path = Path(__file__).parent / "app.py"
    typer.echo(f"Starting Streamlit app...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])


if __name__ == "__main__":
    app()
