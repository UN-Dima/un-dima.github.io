

# ----------------------------------------------------------------------
def render_plotly_fig__(fig, chart):
    import json
    import plotly
    import js
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    js.Plotly.newPlot(chart, js.JSON.parse(graphJSON), {})


# ----------------------------------------------------------------------
def process_data():
    """"""
    global groups, df

    import json
    import numpy as np

    return json.dumps({
        'grupos': np.unique(df['Nombre del grupo'].tolist()),
        'facultades': np.unique(groups['facultad'].tolist()),
        'departamentos': np.unique(groups['departamento'].tolist()),

    })
