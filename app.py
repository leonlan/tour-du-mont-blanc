from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

START_DATE = datetime.strptime("2025-06-02", "%Y-%m-%d")
END_DATE = datetime.strptime("2025-09-28", "%Y-%m-%d")

AVAILABILITY_URL = "https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/refs/heads/main/data/2025/{datetime:%Y-%m-%d-%H}.csv"
HUTS_URL = "https://raw.githubusercontent.com/leonlan/tour-du-mont-blanc/main/data/huts.csv"


now = datetime.now()
now -= timedelta(hours=2)  # UTC+2

try:
    url = AVAILABILITY_URL.format(datetime=now)
    print(url)
    df = pd.read_csv(url, index_col=0)
except:
    url = AVAILABILITY_URL.format(datetime=datetime.now() - timedelta(hours=1))
    df = pd.read_csv(url, index_col=0)

last_updated_at = f"Data last updated on: {now.date()}."

huts_df = pd.read_csv(HUTS_URL)


st.title("TMB hut availability calendar")

text = "Check out our website at [TMB Planner](https://tmbplanner.com/) for planning tools for your Tour du Mont Blanc hike."
st.markdown(text)


@st.dialog("Check out our new website!", width="small")
def popup():
    st.write(text)


popup()


date_range = st.date_input(
    "Select a date range:",
    value=(max(START_DATE, datetime.today()), END_DATE),
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
        style = "background-color: #81C784; color: black"  # green
    elif 0 < val:
        style = "background-color: #FFF176; color: black"  # yellow
    else:
        style = ""
    return style


# Add the URL for each hut.
cols = ["mon_name", "mon_url"]
name2url = huts_df[cols].set_index("mon_name")["mon_url"].to_dict()
url2name = {v: k for k, v in name2url.items()}
df.insert(0, "URL", df.index.map(name2url))

# Reorder on counter-clockwise order of huts.
cc_ordering = huts_df["mon_name"].tolist()
cc_ordering = {name: i for i, name in enumerate(cc_ordering, 1)}
df.insert(1, "TMB order", df.index.map(cc_ordering))

if len(date_range) == 2:  # both dates must be selected
    cols = ["URL", "TMB order"]
    dates = [
        col
        for col in df.columns
        if col not in cols
        and date_range[0]
        <= datetime.strptime(col, "%Y-%m-%d").date()
        <= date_range[1]
    ]
    filtered = df.loc[selected_huts, cols + dates]

    if not filtered.empty:
        display = filtered.copy()
        styled = display.style
        styled = styled.format(
            {"URL": lambda _: "Link"},
            escape="html",
        )
        styled = styled.map(highlight_conditions, subset=dates)

        st.dataframe(
            styled,
            column_config={
                "URL": st.column_config.LinkColumn("Website"),
            },
        )


st.markdown(
    "Sorting by TMB order will arrange the huts in counter-clockwise (ascending) or clockwise (descending) order around the TMB trek."
)
st.markdown("Green: 4 or more beds available; Yellow: 1-3 beds available.")
st.markdown(
    "Click [here](https://umap.openstreetmap.fr/fr/map/tour-du-mont-blanc-ccpmb_206457#11/45.9051/6.9293) for a map of the TMB huts."
)
st.markdown(last_updated_at)
