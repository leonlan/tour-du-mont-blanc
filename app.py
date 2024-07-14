from datetime import datetime

import pandas as pd
import streamlit as st

df = pd.read_csv("20231212_availability.csv", index_col=0)

# Title of the Streamlit app
st.title("TMB hut availability calendar")

# Define the default start and end dates
start_date = datetime.strptime("2024-07-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-07-07", "%Y-%m-%d")

# Define the min and max date range
min_date = datetime.strptime("2024-06-01", "%Y-%m-%d")
max_date = datetime.strptime("2024-09-30", "%Y-%m-%d")

# Date range selector with min and max date range
date_range = st.date_input(
    "Select a date range:",
    value=(start_date, end_date),
    min_value=min_date,
    max_value=max_date,
)


# Multiselect widget for name selection
selected_names = st.multiselect("Select names:", options=sorted(df.index.unique()))


def highlight_conditions(val):
    if val in [1, 2]:
        color = "#FFEB3B"  # A nicer shade of yellow (hex color code)
    elif val >= 3:
        color = "#81C784"  # A nicer shade of green (hex color code)
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
        # Select and display specific columns
        styled_df = filtered_df.style.applymap(highlight_conditions)
        st.dataframe(styled_df)
