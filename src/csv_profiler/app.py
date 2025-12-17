"""Streamlit web interface for CSV Profiler."""

import sys
from pathlib import Path
import importlib.util

import streamlit as st

# Handle imports for both direct execution and package import
try:
    from .io import parse_csv_string
    from .profiler import profile_csv
    from .render import generate_json_report, generate_markdown_report
except ImportError:
    # When run directly by streamlit, load modules from local directory
    _pkg_dir = Path(__file__).parent

    # Load local io.py (can't use 'import io' as it shadows stdlib)
    _spec = importlib.util.spec_from_file_location("csv_io", _pkg_dir / "io.py")
    _csv_io = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_csv_io)
    parse_csv_string = _csv_io.parse_csv_string

    # Load other modules normally
    sys.path.insert(0, str(_pkg_dir))
    from profiler import profile_csv
    from render import generate_json_report, generate_markdown_report

# Page configuration
st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.markdown("Upload a CSV file to analyze its structure and statistics.")

# File upload widget
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    # Parse the uploaded CSV file
    text = uploaded.getvalue().decode("utf-8")
    rows = parse_csv_string(text)

    # Show basic file info
    st.info(f"Loaded **{len(rows)}** rows from `{uploaded.name}`")

    # Profile button
    if st.button("Generate Profile", type="primary"):
        # Run profiling and store in session state
        profile = profile_csv(rows)
        st.session_state["profile"] = profile

    # Display results if profile exists
    if "profile" in st.session_state:
        profile = st.session_state["profile"]

        # Summary metrics at the top
        st.subheader("Summary")
        col1, col2 = st.columns(2)
        col1.metric("Rows", f"{profile['n_rows']:,}")
        col2.metric("Columns", profile['n_cols'])

        # Tabs for different output formats
        tab_table, tab_markdown, tab_json = st.tabs(["Table View", "Markdown", "JSON"])

        # Tab 1: Interactive table view
        with tab_table:
            st.subheader("Column Details")
            # Build a simple table from column profiles
            table_data = []
            for col in profile['columns']:
                n_rows = profile['n_rows']
                missing_pct = (col['missing'] / n_rows * 100) if n_rows else 0
                row = {
                    "Column": col['name'],
                    "Type": col['type'],
                    "Missing": f"{col['missing']} ({missing_pct:.1f}%)",
                    "Unique": col['unique'],
                }
                # Add stats based on type
                if col['type'] == 'number':
                    row["Min"] = col.get('min', '-')
                    row["Max"] = col.get('max', '-')
                    row["Mean"] = f"{col.get('mean', 0):.2f}" if col.get('mean') else '-'
                else:
                    # Show top values for text columns
                    top = col.get('top', [])
                    top_str = ", ".join([f"{t['value']} ({t['count']})" for t in top[:3]])
                    row["Top Values"] = top_str if top_str else '-'
                table_data.append(row)

            st.table(table_data)

        # Tab 2: Markdown report
        with tab_markdown:
            md_report = generate_markdown_report(profile)
            st.markdown(md_report)
            # Download button for markdown
            st.download_button(
                label="Download Markdown",
                data=md_report,
                file_name=f"{uploaded.name.replace('.csv', '')}_profile.md",
                mime="text/markdown",
            )

        # Tab 3: JSON report
        with tab_json:
            json_report = generate_json_report(profile)
            st.code(json_report, language="json")
            # Download button for JSON
            st.download_button(
                label="Download JSON",
                data=json_report,
                file_name=f"{uploaded.name.replace('.csv', '')}_profile.json",
                mime="application/json",
            )

else:
    # Show placeholder when no file is uploaded
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. Click **Browse files** above to upload a CSV file
    2. Click **Generate Profile** to analyze the data
    3. View results in Table, Markdown, or JSON format
    4. Download reports using the download buttons
    """)
