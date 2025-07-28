import pandas as pd
from ipywidgets import IntSlider, Button, VBox, Output
from IPython.display import display, HTML
import pandas as pd
from google.colab import files

def slider_filter(df, column):
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
            total_sum = current_filtered[column].sum()
            summary_html = f"""
                <h4>Summary</h4>
                <p><b>Rows:</b> {count}</p>
                <p><b>Sum of {column}:</b> {total_sum}</p>
                """
            display(HTML(summary_html))
            display(current_filtered)

    def export_csv(b):
        filename = "filtered_data.csv"
        current_filtered.to_csv(filename, index=False)
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
