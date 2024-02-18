from shiny import render
from shiny.express import input, ui

ui.input_slider("n", "N", min=1, max=50, value=30)


@render.code
def txt():
    return f"Hello! n*2 is {input.n() * 2}."
