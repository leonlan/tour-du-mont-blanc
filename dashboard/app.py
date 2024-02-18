import numpy as np
import pandas as pd

from shiny import reactive
from shiny.express import input, render, ui

df = pd.read_csv("20231212_availability.csv", index_col=0)
huts = list(df.index)
dates: np.ndarray = df.columns  # type: ignore

ui.page_opts(
    title="Tour du Mont Blanc planner",
    window_title="TMB planner",
    fillable=True,
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


with ui.layout_columns():
    with ui.card():
        ui.card_header("Hut availability")

        @render.data_frame
        def summary_statistics():
            display_df = filter_df()
            display_df = display_df.reset_index().rename(columns={"index": "Hut"})

            return render.DataGrid(
                display_df,
                height="100%",
                summary=False,
                row_selection_mode="multiple",
            )
