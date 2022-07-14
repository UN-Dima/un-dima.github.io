""""""
global groups, df
import plotly.express as px
import json
import numpy as np


# ----------------------------------------------------------------------
def render_plotly_fig__(fig, chart):
    import json
    import plotly
    import js
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    js.Plotly.newPlot(chart, js.JSON.parse(graphJSON), {})


# ----------------------------------------------------------------------
def plot1(faculty):
    """"""
    config = {
        'labels': {'ocde': 'Area',
                   'sub_ocde': 'Subárea',
                   'count': ''
                   },
        'height': 500,
        'title': 'Áreas del Conocimiento - OCDE',
        'template': 'plotly_white',
    }

    g = groups.loc[groups['facultad'] == faculty]
    if faculty == 'All':
        fig = px.histogram(groups, y='sub_ocde', color='ocde', orientation='h', barmode='stack', **config)

    elif faculty in ['Facultad de administración', 'Facultad de ciencias exactas y naturales']:
        config['labels']['ocde'] = ''
        fig = px.histogram(g, y='ocde', orientation='h', barmode='stack', **config)

    else:
        fig = px.histogram(g, y='sub_ocde', color='ocde', orientation='h', barmode='stack', **config)

    fig.update_layout(xaxis_title='')
    # fig.update_traces(hoverinfo='none', hovertemplate = '')
    return fig


# ----------------------------------------------------------------------
def plot2(faculty):
    """"""
    config = {
        'labels': {'knowledge': '',
                   'sub_ocde': 'Subáreas',
                   'count': ''
                   },
        'height': 500,
        'title': 'Agenda de conocimiento',
        'template': 'plotly_white',
    }

    if faculty != 'All':
        g = groups.loc[groups['facultad'] == faculty]
    else:
        g = groups

    fig = px.histogram(g, y='knowledge', orientation='h', barmode='group', **config)
    fig.update_layout(xaxis_title='')
    fig.update_traces(hoverinfo='none', hovertemplate='')

    return fig


# ----------------------------------------------------------------------
def plot3(faculty):
    """"""
    config = {
        'labels': {'departamento': '',
                   'sub_ocde': 'Subáreas',
                   'count': ''
                   },
        'height': 500,
        'title': 'Departamentos',
        'template': 'plotly_white',
    }

    if faculty != 'All':
        g = groups.loc[groups['facultad'] == faculty]
    else:
        g = groups

    fig = px.histogram(g, y='departamento', orientation='h', barmode='group', **config)
    fig.update_layout(xaxis_title='')
    fig.update_traces(hoverinfo='none', hovertemplate='')

    return fig
