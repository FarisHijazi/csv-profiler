"""I/O utilities for reading and parsing CSV files."""

from io import StringIO
from pathlib import Path
import csv


def parse_csv_string(csv_text: str) -> list[dict]:
    """
    Parse CSV text into a list of dictionaries.

    Args:
        csv_text: CSV content as string

    Returns:
        List of dicts (each dict is one row)
    """
    reader = csv.DictReader(StringIO(csv_text))
    return list(reader)


def read_csv_file(file_path: Path) -> list[dict]:
    """
    Read a CSV file and return rows as a list of dictionaries.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dicts (each dict is one row)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))
