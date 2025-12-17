import streamlit as st
import csv
from io import StringIO
from profiler import profile_csv

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

# Upload
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    # Parse
    text = uploaded.getvalue().decode("utf-8")
    rows = list(csv.DictReader(StringIO(text)))

    # Profile on button click
    if st.button("Generate Profile"):
        profile = profile_csv(rows)
        st.session_state["profile"] = profile
        print(profile)

    # Display if available
    if "profile" in st.session_state:
        profile = st.session_state["profile"]
        # Show metrics, tables, download buttons...
