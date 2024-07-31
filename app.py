from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

START_DATE = datetime.strptime("2024-06-01", "%Y-%m-%d")
END_DATE = datetime.strptime("2024-09-29", "%Y-%m-%d")

today = datetime.today()

try:
    # Get the most recent hut availability data.
    df = pd.read_csv(
        f"https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/availability/daily/{today.date()}.csv",
        index_col=0,
    )
    text = f"Data last updated on: {today.date()}."
except:
    # Fallback to yesterday's data if today's data is not available.
    yesterday = today - timedelta(days=1)
    df = pd.read_csv(
        f"https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/availability/daily/{yesterday.date()}.csv",
        index_col=0,
    )
    text = f"Data last updated on: {yesterday.date()}"

hut_names = sorted(df.index.unique())

st.title("TMB hut availability calendar")


date_range = st.date_input(
    "Select a date range:",
    value=(today, END_DATE),
    min_value=START_DATE,
    max_value=END_DATE,
    key="date_range",
)

selected_huts = st.multiselect(
    "Select huts:",
    options=hut_names,
    default=hut_names,
    key="selected_huts",
)


def highlight_conditions(val):
    if val >= 4:
        color = "#81C784"  # green
    elif 0 < val:
        color = "#FFEB3B"  # yellow
    else:
        color = ""
    return f"background-color: {color}"


if len(date_range) > 0:
    cols = [
        col
        for col in df.columns
        if date_range[0] <= datetime.strptime(col, "%Y-%m-%d").date() <= date_range[1]
    ]
    filtered_df = df.loc[selected_huts, cols]

    if not filtered_df.empty:
        styled_df = filtered_df.style.map(highlight_conditions)
        st.dataframe(styled_df)


st.markdown(text)
st.markdown("Green: 4 or more beds available; Yellow: 1-3 beds available.")
