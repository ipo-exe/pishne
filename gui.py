import pandas as pd
from ipywidgets import IntSlider, Dropdown, Button, VBox, Output
from IPython.display import display, HTML
import pandas as pd
from google.colab import files

def slider_filter(df, column, label1="Filtrados", label2="Total"):
    """
    Creates interactive sliders to filter the dataframe based on the column.
    """
    min_val = int(df[column].min())
    max_val = int(df[column].max())

    # Widgets
    min_slider = IntSlider(value=min_val, min=min_val, max=max_val, step=1, description='Min')
    max_slider = IntSlider(value=max_val, min=min_val, max=max_val, step=1, description='Max')
    export_button = Button(description="Download CSV", button_style='success')
    output = Output()

    # Variable to store filtered data
    current_filtered = df.copy()

    def update_display(*args):
        nonlocal current_filtered
        with output:
            output.clear_output()
            current_filtered = df[(df[column] >= min_slider.value) & (df[column] <= max_slider.value)]

            # Summary
            count = len(current_filtered)
            total_sum = round(current_filtered[column].sum(), 2)
            summary_html = f"""
                <h4>Resumo</h4>
                <p><b>{label1}:</b> {count}</p>
                <p><b>{label2}:</b> {total_sum}</p>
                """
            display(HTML(summary_html))
            display(current_filtered)

    def export_csv(b):
        filename = "filtered_data.csv"
        current_filtered.to_csv(filename, index=False, sep=";", encoding="utf-8")
        files.download(filename)

    # Link events
    min_slider.observe(update_display, 'value')
    max_slider.observe(update_display, 'value')
    export_button.on_click(export_csv)

    # Initial display
    update_display()

    # Layout
    ui = VBox([min_slider, max_slider, export_button, output])
    display(ui)


def dropdown_filter(df, column, label1="Filtrados", label2="Total", value_column=None, contains=False, options=None):
    """
    Creates a dropdown filter for a qualitative column.
    Displays summary and allows CSV export of the filtered data.
    """
    # Unique values for dropdown
    if options is None:
        unique_values = sorted(df[column].dropna().unique())

    # Widgets
    dropdown = Dropdown(options=['All'] + unique_values, description=column)
    export_button = Button(description="Download CSV", button_style='success')
    output = Output()

    # Variable to store filtered data
    current_filtered = df.copy()

    def update_display(*args):
        nonlocal current_filtered
        with output:
            output.clear_output()

            if dropdown.value == 'All':
                current_filtered = df
            else:
                if contains:
                    # Case-insensitive substring match
                    current_filtered = df[df[column].astype(str).str.contains(dropdown.value, case=True, na=False)]
                else:
                    current_filtered = df[df[column] == dropdown.value]


            # Summary
            count = len(current_filtered)
            summary_html = f"""
            <h4>Resumo</h4>
            <p><b>{label1}:</b> {count}</p>
            """
            if value_column is not None:
                total_sum = round(current_filtered[value_column].sum(), 2)
                summary_html = f"""
                <h4>Resumo</h4>
                <p><b>{label1}:</b> {count}</p>
                <p><b>{label2}:</b> {total_sum}</p>
                """

            display(HTML(summary_html))
            display(current_filtered)

    def export_csv(b):
        filename = "filtered_data.csv"
        current_filtered.to_csv(filename, index=False, sep=";", encoding="utf-8")
        files.download(filename)

    # Link events
    dropdown.observe(update_display, 'value')
    export_button.on_click(export_csv)

    # Initial display
    update_display()

    # Layout
    ui = VBox([dropdown, export_button, output])
    display(ui)


def download(df, filename="data.csv"):
    """
    Creates a simple button to download the entire DataFrame as CSV.
    """
    export_button = Button(description="Download CSV", button_style='success')

    def export_csv(b):
        df.to_csv(filename, index=False, sep=";", encoding="utf-8")
        files.download(filename)

    export_button.on_click(export_csv)
    display(export_button)