import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select

# Creamos un DICCIONARIO de datos con más registros
data = {
    'Fecha': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05',
              '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10'],
    'Ventas': [1000, 1500, 1200, 1800, 2000, 1900, 1600, 1700, 2200, 2100],
    'Ganancias': [400, 500, 450, 600, 700, 650, 550, 600, 750, 720]
}

# Convertimos a DataFrame usando el paquete PANDAS
df = pd.DataFrame(data)
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Creamos la fuente de datos que admite BOKEH, para esto se usó el paquete models y el método ColumnDataSource
source = ColumnDataSource(df)

# Crear gráfico de línea para ventas
ventas_plot = figure(title="Ventas Diarias", x_axis_label='Fecha', y_axis_label='Ventas',
                     x_axis_type='datetime', width=800, height=300)
ventas_plot.line(x='Fecha', y='Ventas', source=source, line_width=2)

# Crear gráfico de barras para ganancias
ganancias_plot = figure(title="Ganancias Diarias", x_axis_label='Fecha', y_axis_label='Ganancias',
                        x_axis_type='datetime', width=800, height=300)
ganancias_plot.vbar(x='Fecha', top='Ganancias', width=0.5, source=source)

# Crear gráfico de dispersión para ventas
scatter_plot = figure(title="Dispersión de Ventas", x_axis_label='Fecha', y_axis_label='Ventas',
                      x_axis_type='datetime', width=800, height=300)
scatter_plot.scatter(x='Fecha', y='Ventas', source=source, size=8, color="navy", alpha=0.5)

# Crear gráfico de área para ganancias
area_plot = figure(title="Área de Ganancias", x_axis_label='Fecha', y_axis_label='Ganancias',
                   x_axis_type='datetime', width=800, height=300)
area_plot.varea(x='Fecha', y1=0, y2='Ganancias', source=source, color="green", alpha=0.5)

# Agregar herramienta de información a los gráficos
hover = HoverTool()
hover.tooltips = [("Fecha", "@Fecha{%F}"), ("Valor", "$y")]
hover.formatters = {'@Fecha': 'datetime'}
ventas_plot.add_tools(hover)
ganancias_plot.add_tools(hover)
scatter_plot.add_tools(hover)
area_plot.add_tools(hover)

# Crear lista desplegable para seleccionar el gráfico
select = Select(title="Seleccionar Gráfico:", options=['Ventas Diarias', 'Ganancias Diarias',
                                                      'Dispersión de Ventas', 'Área de Ganancias'])

# Función para actualizar el gráfico seleccionado
def update_plot(attrname, old, new):
    if select.value == 'Ventas Diarias':
        layout.children[1] = ventas_plot
    elif select.value == 'Ganancias Diarias':
        layout.children[1] = ganancias_plot
    elif select.value == 'Dispersión de Ventas':
        layout.children[1] = scatter_plot
    else:
        layout.children[1] = area_plot

# Actualizar gráfico cuando se selecciona una opción
select.on_change('value', update_plot)

# Organizar elementos en el layout
layout = column(select, ventas_plot)

# Agregar layout al documento
curdoc().add_root(layout)
