import pandas as pd
from ipywidgets import interact, IntSlider
from IPython.display import display

def slider_filter(df, column):
    """
    Creates interactive sliders to filter the dataframe based on the column.
    """
    min_val = int(df[column].min())
    max_val = int(df[column].max())

    def filter_data(min_value, max_value):
        filtered = df[(df[column] >= min_value) & (df[column] <= max_value)]
        display(filtered)

    interact(
        filter_data,
        min_value=IntSlider(value=min_val, min=min_val, max=max_val, step=1, description='Min'),
        max_value=IntSlider(value=max_val, min=min_val, max=max_val, step=1, description='Max')
    )
