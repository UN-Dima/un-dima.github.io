

# ----------------------------------------------------------------------
def render_plotly_fig__(fig, chart):
    import json
    import plotly
    import js
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    js.Plotly.newPlot(chart, js.JSON.parse(graphJSON), {})

    return None


# ----------------------------------------------------------------------
def process_data():
    """"""
    return {'hola': 'mundo',
            'Nania': True,
            'Ezis': 3.5,
            }


# ----------------------------------------------------------------------
def plot():
    """"""
    global groups

    import plotly.express as px
    fig = px.bar(groups, y='ocde', orientation='h')
    return fig


# ----------------------------------------------------------------------
def plot2():
    """"""
    global groups

    import plotly.express as px
    fig = px.bar(groups, y='ocde2', orientation='h')
    return fig


# ----------------------------------------------------------------------
def plot3():
    """"""
    global groups

    import plotly.express as px
    fig = px.bar(groups, y='knowledge', orientation='h')
    return fig
