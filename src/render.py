def generate_json_report(profile):
    """Generate JSON report string."""
    import json
    return json.dumps(profile, indent=2, ensure_ascii=False)

def generate_markdown_report(profile):
    """Generate Markdown report string."""
    lines = []
    lines.append("# CSV Profiling Report")
    lines.append("")
    lines.append(f"- **Rows:** {profile['n_rows']:,}")
    lines.append(f"- **Columns:** {profile['n_cols']}")
    lines.append("")
    lines.append("## Column Summary")
    lines.append("")
    lines.append("| Column | Type | Missing | Unique |")
    lines.append("|--------|------|--------:|-------:|")

    for col in profile['columns']:
        n_rows = profile['n_rows']
        missing_pct = (col['missing'] / n_rows * 100) if n_rows else 0
        lines.append(f"| {col['name']} | {col['type']} | {col['missing']} ({missing_pct:.1f}%) | {col['unique']} |")

    return "\n".join(lines)

def display_profile_summary(profile):
    """Display a summary of the profile."""
    print("=" * 50)
    print("PROFILE SUMMARY")
    print("=" * 50)
    print(f"Rows: {profile['n_rows']:,}")
    print(f"Columns: {profile['n_cols']}")
    print()

def display_column_table(profile):
    """Display column info as a table."""
    print("COLUMN DETAILS")
    print("-" * 60)
    print(f"{'Column':<15} {'Type':<10} {'Missing':<10} {'Unique':<10}")
    print("-" * 60)

    for col in profile['columns']:
        n_rows = profile['n_rows']
        missing_pct = (col['missing'] / n_rows * 100) if n_rows else 0
        print(f"{col['name']:<15} {col['type']:<10} {col['missing']} ({missing_pct:.1f}%)    {col['unique']}")
