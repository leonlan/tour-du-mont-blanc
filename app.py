from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

today = datetime.today()

try:
    # Get the most recent hut availability data.
    df = pd.read_csv(
        f"https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/availability/daily/{today.date()}.csv",
        index_col=0,
    )
    text = f"Data fetched on {today.date()}"
except:
    # Fallback to yesterday's data if today's data is not available.
    yesterday = today - timedelta(days=1)
    df = pd.read_csv(
        f"https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/availability/daily/{yesterday.date()}.csv",
        index_col=0,
    )
    text = f"Data fetched on {yesterday.date()}"

# Title of the Streamlit app
st.title("TMB hut availability calendar")

st.markdown(text)

# Define the default start and end dates
start_date = today
end_date = datetime.strptime("2024-09-30", "%Y-%m-%d")

# Define the min and max date range
min_date = datetime.strptime("2024-06-01", "%Y-%m-%d")
max_date = end_date

# Date range selector with min and max date range
date_range = st.date_input(
    "Select a date range:",
    value=(start_date, end_date),
    min_value=min_date,
    max_value=max_date,
)

# Multiselect widget for name selection
hut_names = sorted(df.index.unique())
selected_names = st.multiselect(
    "Select names:",
    options=hut_names,
    default=hut_names,
)


def highlight_conditions(val):
    if val in [1, 2]:
        color = "#FFEB3B"  # yellow
    elif val >= 3:
        color = "#81C784"  # green
    else:
        color = ""
    return f"background-color: {color}"


if len(date_range) > 1:
    cols = []

    for col in df.columns:
        date = datetime.strptime(col, "%Y-%m-%d").date()

        if date_range[0] <= date <= date_range[1]:
            cols.append(col)

    filtered_df = df[cols]
    filtered_df = filtered_df.loc[selected_names]

    if not filtered_df.empty:
        styled_df = filtered_df.style.map(highlight_conditions)
        st.dataframe(styled_df)
