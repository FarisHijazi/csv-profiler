from io import StringIO
import csv

def parse_csv_string(csv_text):
    """
    Parse CSV text into a list of dictionaries.

    Args:
        csv_text: CSV content as string

    Returns:
        List of dicts (each dict is one row)
    """
    reader = csv.DictReader(StringIO(csv_text))
    return list(reader)
