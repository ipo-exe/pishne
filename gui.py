import pandas as pd
from ipywidgets import interact, IntSlider
from IPython.display import display, HTML

def slider_filter(df, column):
    """
    Creates interactive sliders to filter the dataframe based on the column.
    """
    min_val = int(df[column].min())
    max_val = int(df[column].max())

    export_button = Button(description="Download CSV", button_style='success')

    # Variable to store the current filtered dataframe
    current_filtered = df.copy()

    def filter_data(min_value, max_value):
        nonlocal current_filtered
        # Filter
        current_filtered = df[(df[column] >= min_value) & (df[column] <= max_value)]

        # Summary
        count = len(current_filtered)
        total_sum = round(filtered[column].sum(), 2)
        # Display summary
        summary_html = f"""
                    <h4>Resumo</h4>
                    <p><b>Ações filtradas:</b> {count}</p>
                    <p><b>Total filtrado: R$ (Mi) </b> {total_sum}</p>
                    """
        display(HTML(summary_html))

        # Show filtered data
        display(current_filtered)

    def export_csv(b):
        # Save filtered DataFrame to a CSV file
        filename = "dados_filtrados.csv"
        current_filtered.to_csv(filename, index=False)
        from google.colab import files
        files.download(filename)

    # Attach button event
    export_button.on_click(export_csv)

    # Create the UI
    ui = VBox([
        interact(
            filter_data,
            min_value=IntSlider(value=min_val, min=min_val, max=max_val, step=1, description='Min'),
            max_value=IntSlider(value=max_val, min=min_val, max=max_val, step=1, description='Max')
        ),
        export_button
    ])

    display(ui)
