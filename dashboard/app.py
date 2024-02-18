import numpy as np
import pandas as pd

from ipyleaflet import Map, Marker, AwesomeIcon
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget


df = pd.read_csv("20231212_availability.csv", index_col=0)
huts = list(df.index)
dates: np.ndarray = df.columns  # type: ignore


ui.page_opts(
    title="Tour du Mont Blanc planner",
    window_title="TMB planner",
)


with ui.sidebar(width="20%"):
    ui.input_date_range("daterange", "Date range", start=dates.min(), end=dates.max())

    ui.input_checkbox_group(
        "select",
        "Select huts",
        {val: val for val in df.index},
        selected=huts,
    )


@reactive.Calc
def filter_df() -> pd.DataFrame:
    selected_huts = list(input.select())
    filt_df = df.loc[selected_huts]

    # Filter by date range; converting to datetime makes this easier to
    # filter. But we need to convert back to string for display.
    filt_df.columns = pd.to_datetime(filt_df.columns)
    start_date, end_date = input.daterange()
    filt_df = filt_df.loc[:, start_date:end_date]
    filt_df.columns = filt_df.columns.strftime("%Y-%m-%d")

    return filt_df


with ui.card(height="1000px"):
    ui.card_header("Hut availability")

    @render.data_frame
    def summary_statistics():
        display_df = filter_df()
        display_df = display_df.reset_index().rename(columns={"index": "Hut"})

        return render.DataGrid(
            display_df,
            summary=False,
            row_selection_mode="multiple",
            height="100%",
        )

    @render.download(filename="tmb_hut_availability.csv", label="Download as CSV")
    def download():
        # TODO I'm not sure what the first return value is for, but without the
        # download raises an error about the CSV output not being a valid file name.
        return "", filter_df().to_csv(index=False)


hut_data = pd.read_csv("data/huts.csv")
coord_data = [
    ((str(item.mon_name), (item.lt, item.lg))) for item in hut_data.itertuples()
]

with ui.card(height="1000px"):
    ui.card_header("TMB map")

    @render_widget
    def map():
        icon = AwesomeIcon(name="bed")
        map = Map(center=(45.900577, 6.7994213), zoom=10)

        for name, coords in coord_data:
            point = Marker(location=coords, icon=icon, draggable=False, title=name)
            map.add_layer(point)

        return map
