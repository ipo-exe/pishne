import datetime, shutil
import pandas as pd
from ipywidgets import IntSlider, Dropdown, Button, VBox, Output, Text, Layout, FloatText
from IPython.display import display, HTML, clear_output
import pandas as pd
from google.colab import files


def get_timestamp(mode="record"):
    """Return a string timestamp

    :return: full timestamp text %Y-%m-%d %H:%M:%S
    :rtype: str
    """
    # compute timestamp
    _now = datetime.datetime.now()
    if mode == "record":
        return str(_now.strftime("%Y-%m-%d %H:%M:%S"))
    elif mode == "file":
        return str(_now.strftime("%Y-%m-%d-T%Hh%Mm%Ss"))


def slider_filter(df, column, label1="Filtrados", label2="Total"):
    """
    Creates interactive sliders to filter the dataframe based on the column.
    """
    min_val = int(df[column].min())
    max_val = int(df[column].max())

    # Widgets
    min_slider = IntSlider(value=min_val, min=min_val, max=max_val, step=1, description='Min')
    max_slider = IntSlider(value=max_val, min=min_val, max=max_val, step=1, description='Max')
    export_button = Button(description="Download Excel", button_style='success')
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
            summary_html = f"""
                <h4>Resumo</h4>
                <p><b>{label1}:</b> {count}</p>
                """
            display(HTML(summary_html))
            display(current_filtered)

    def export_excel(b):
        filename = "filtered_data_{}.xlsx".format(get_timestamp(mode="file"))
        current_filtered.to_excel(filename, index=False, engine="openpyxl")
        files.download(filename)

    # Link events
    min_slider.observe(update_display, 'value')
    max_slider.observe(update_display, 'value')
    export_button.on_click(export_excel)

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
        options = sorted(df[column].dropna().unique())

    # Widgets
    dropdown = Dropdown(options=['All'] + options, description=column)
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
                summary_html = f"""
                <h4>Resumo</h4>
                <p><b>{label1}:</b> {count}</p>
                """

            display(HTML(summary_html))
            display(current_filtered)

    def export_csv(b):
        filename = "filtered_data.csv"
        current_filtered.to_csv(filename, index=False, sep=";", encoding="utf-8")
        files.download(filename)

    def export_excel(b):
        filename = "filtered_data_{}.xlsx".format(get_timestamp(mode="file"))
        current_filtered.to_excel(filename, index=False, engine="openpyxl")
        files.download(filename)

    # Link events
    dropdown.observe(update_display, 'value')
    export_button.on_click(export_excel)

    # Initial display
    update_display()

    # Layout
    ui = VBox([dropdown, export_button, output])
    display(ui)


def create_dynamic_form(df, text_fields=None, dropdown_fields=None, on_submit_callback=None):
    """
    Creates a dynamic form where:
    - text_fields: list of column names for text inputs
    - dropdown_fields: list of column names for dropdowns (auto-populated with unique values)
    - on_submit_callback: function that receives a dict with form data
    """

    # Create widgets dynamically
    widgets_dict = {}

    # Text inputs
    if text_fields:
        for field in text_fields:
            widgets_dict[field] = Text(description=f'{field}:')

    # Dropdowns populated from DataFrame
    if dropdown_fields:
        for field in dropdown_fields:
            options = sorted(df[field].dropna().unique().tolist())
            widgets_dict[field] = Dropdown(options=options, description=f'{field}:')

    # Submit button and output
    submit_button = Button(description='Submit', button_style='success')
    output = Output()

    # On click
    def on_submit(b):
        with output:
            clear_output()
            form_data = {key: widget.value for key, widget in widgets_dict.items()}
            if on_submit_callback:
                on_submit_callback(form_data)
            else:
                print("Form data:", form_data)

    submit_button.on_click(on_submit)

    # Layout
    form_items = list(widgets_dict.values()) + [submit_button, output]
    form_box = VBox(form_items)
    display(form_box)


def download(df, filename="data.csv", filter=False):
    """
    Creates a simple button to download the entire DataFrame as CSV.
    """
    s_extension = filename.split(".")[-1]
    if s_extension == "csv":
        s_aux = "CSV"
    elif s_extension == "xlsx":
        s_aux = "Excel"
    elif s_extension == "gpkg":
        s_aux = "GPKG"

    export_button = Button(description=f"Download {s_aux}", button_style='success')

    def export_csv(b):
        filename = "pishne_data_" + get_timestamp(mode="file") + ".csv"
        if filter:
            filename = "resumo_" + filename
        print(filename)
        df.to_csv(filename, index=False, sep=";", encoding="utf-8")
        files.download(filename)

    def export_xlsx(b):
        filename = "pishne_data_" + get_timestamp(mode="file") + ".xlsx"
        if filter:
            filename = "resumo_" + filename
        print(filename)
        df.to_excel(filename, index=False, engine="openpyxl")
        files.download(filename)

    def export_geo(b):
        filename2 = filename.replace("_db_0", "_db_{}".format(get_timestamp(mode="file")))
        shutil.copy(
            src=filename,
            dst=filename2,
        )
        files.download(filename2)

    if s_extension == "csv":
        export_button.on_click(export_csv)
    elif s_extension == "xlsx":
        export_button.on_click(export_xlsx)
    elif s_extension == "gpkg":
        export_button.on_click(export_geo)
    display(export_button)


def selector(db, sub="origem"):
    origem_investimento = widgets.Dropdown(
        options=db["origem"].data["origem_investimento"].unique(),
        value='Estados',
        description='Origem:'
    )
    # Display the form
    form_items = widgets.VBox([
        origem_investimento,
    ])

    display(form_items)


# Callback function
def handle_selection(data):
    return data


def action_form(db, df):

    df["cde_componente"] = df['cod_componente'] + ' -- ' + df['desc_componente']
    df["cde_subcomponente"] = df['cod_subcomponente'] + ' -- ' + df['desc_subcomponente']

    hierarchy = ['cde_componente', 'cde_subcomponente', 'nm_tematica']
    hierarchy_labels = {
        'cde_componente': "Componente",
        'cde_subcomponente': "Sub-componente",
        'nm_tematica': "Temática"
    }
    widgets_dict = {}
    for col in hierarchy:
        widgets_dict[col] = Dropdown(
            description="{}:".format(hierarchy_labels[col]),
            options=['Selecionar'],
            layout=Layout(width='800px'),
            style={'description_width': '200px'}
        )

    # Update function for cascading effect
    def update_options(change, current_col):
        current_idx = hierarchy.index(current_col)
        if current_idx + 1 < len(hierarchy):
            next_col = hierarchy[current_idx + 1]
            # Filter df based on previous selections
            filtered_df = df.copy()
            for col in hierarchy[:current_idx + 1]:
                if widgets_dict[col].value != 'Selecionar':
                    filtered_df = filtered_df[filtered_df[col] == widgets_dict[col].value]
            next_options = sorted(filtered_df[next_col].dropna().unique().tolist())
            widgets_dict[next_col].options = ['Selecionar'] + next_options

            # Reset deeper dropdowns
            for deeper_col in hierarchy[current_idx + 2:]:
                widgets_dict[deeper_col].options = ['Selecionar']

    # Attach observers
    for col in hierarchy[:-1]:
        widgets_dict[col].observe(lambda change, c=col: update_options(change, c), 'value')

    all_cols = hierarchy.copy()
    # descrição
    desc_acao = Text(
        description='Descrição:',
        layout=Layout(width='800px'),
        style={'description_width': '200px'},
    )
    widgets_dict["desc_acao"] = desc_acao
    all_cols = all_cols + ["desc_acao"]

    # valor investimento
    valor_investimento = FloatText(
        description='Investimento (Mi R$):',
        layout=Layout(width='800px'),
        style={'description_width': '200px'},
    )
    widgets_dict['valor_investimento'] = valor_investimento
    all_cols = all_cols + ['valor_investimento']

    # origem
    options_origem = sorted(db["origem"].data["origem_investimento"].unique())
    origem_investimento = Dropdown(
        options=options_origem,
        value=options_origem[0],
        description='Origem:',
        layout=Layout(width='800px'),
        style={'description_width': '200px'}
    )
    widgets_dict['origem_investimento'] = origem_investimento
    all_cols = all_cols + ['origem_investimento']

    # escala
    options_escala = sorted(db["escala"].data["escala_acao"].unique()) + ["Mix de Estados (preencher abaixo)"]
    escala_acao = Dropdown(
        options=options_escala,
        value="Mix de Estados (preencher abaixo)",
        description='Escala:',
        layout=Layout(width='800px'),
        style={'description_width': '200px'}
    )
    widgets_dict['escala_acao'] = escala_acao
    all_cols = all_cols + ['escala_acao']

    # mix
    mix_estados = Text(
        description="Mix de Estados (ex: 'SE & PE'):",
        value="SE & PE",
        layout=Layout(width='800px'),
        style={'description_width': '200px'},
    )
    widgets_dict["mix"] = mix_estados
    all_cols = all_cols + ["mix"]

    # Initial options for the first dropdown
    first_col = hierarchy[0]
    widgets_dict[first_col].options = ['Selecionar'] + sorted(df[first_col].dropna().unique().tolist())

    # Submit and capture values
    output = Output()
    submit_button = Button(description="Submeter Ação", button_style="success")
    form_data = {}

    def on_submit(b):
        with output:
            clear_output()
            for key, w in widgets_dict.items():
                v = w.value
                if "cde_" in key:
                    v = v.split(" -- ")[0]
                    key = key.replace("cde_", "cod_")
                if v == 'Selecionar':
                    v = None
                form_data[key] = v
            # handle mix
            if form_data["escala_acao"] == "Mix de Estados (preencher abaixo)":
                form_data["escala_acao"] = form_data["mix"][:]
                del form_data["mix"]

            print(" >>> Formulário submetido.")
            print(" >>> ATENÇÃO: consolidar inserção abaixo.")

    submit_button.on_click(on_submit)

    # Layout
    form_items = [widgets_dict[col] for col in all_cols] + [submit_button, output]
    display(VBox(form_items))

    return form_data