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

huts_df = pd.read_csv(
    "https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/main/data/huts.csv",
)


st.title("TMB hut availability calendar")


date_range = st.date_input(
    "Select a date range:",
    value=(today, END_DATE),
    min_value=START_DATE,
    max_value=END_DATE,
    key="date_range",
)

hut_names = sorted(df.index.unique())
selected_huts = st.multiselect(
    "Select huts:",
    options=hut_names,
    default=hut_names,
    key="selected_huts",
)


def highlight_conditions(val):
    if not isinstance(val, int):
        return
    if val >= 4:
        color = "#81C784"  # green
    elif 0 < val:
        color = "#FFEB3B"  # yellow
    else:
        color = ""
    return f"background-color: {color}"


name2url = huts_df[["mon_name", "mon_url"]].set_index("mon_name")["mon_url"].to_dict()
url2name = {v: k for k, v in name2url.items()}

if len(date_range) == 2:  # both dates must be selected
    cols = [
        col
        for col in df.columns
        if date_range[0] <= datetime.strptime(col, "%Y-%m-%d").date() <= date_range[1]
    ]
    filtered_df = df.loc[selected_huts, cols]

    if not filtered_df.empty:
        display_df = filtered_df.copy()

        # Turn hut name index into column and replace it with the URLs. Then
        # style the column to display the hut names again, while making them clickable.
        # Bit of a workaround but thats what they say in the docs: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.linkcolumn
        display_df = display_df.reset_index().rename(columns={"index": "Hut"})
        display_df["Hut"] = display_df["Hut"].map(name2url)

        styled_df = display_df.style.format(
            {"Hut": lambda url: url2name[url]},
            escape="html",
        )
        styled_df = styled_df.map(highlight_conditions)

        st.dataframe(
            styled_df,
            column_config={
                "Hut": st.column_config.LinkColumn("Hut"),
            },
            hide_index=True,
        )


st.markdown(text)
st.markdown("Green: 4 or more beds available; Yellow: 1-3 beds available.")
