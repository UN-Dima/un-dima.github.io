""""""
global groups, df
import plotly.express as px
import json
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from json import dumps as brython_serializer


# ----------------------------------------------------------------------
def render_plotly_fig__(fig, chart):
    import json
    import plotly
    import js
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    js.Plotly.newPlot(chart, js.JSON.parse(graphJSON), {})

# # ----------------------------------------------------------------------
# @pyscript()
# def brython_serializer(data):
    # """"""
    # return json.dumps(data)


# ----------------------------------------------------------------------
def plot_categories(categories, height=500, width=1000):
    """"""
    subplots = make_subplots(
        rows=len(categories),
        cols=1,
        subplot_titles=[x["name"] for x in categories],
        shared_xaxes=True,
        print_grid=False,
        vertical_spacing=(0.45 / len(categories)),
    )
    subplots['layout'].update(
        width=550,
        plot_bgcolor='#fff',
    )

    for k, x in enumerate(categories):
        subplots.add_trace(dict(
            type='bar',
            orientation='h',
            y=[x["name"]],
            x=[x["value"]],
            text=["{:,.0f}".format(x["value"])],
            hoverinfo='text',
            textposition='auto',
            marker=dict(
                color="#636efa",
            ),
        ), k + 1, 1)

    subplots['layout'].update(
        showlegend=False,
    )

    for x in subplots["layout"]['annotations']:
        x['x'] = 0
        x['xanchor'] = 'left'
        x['align'] = 'left'
        x['font'] = dict(
            size=12,
        )

    for axis in subplots['layout']:
        if axis.startswith('yaxis') or axis.startswith('xaxis'):
            subplots['layout'][axis]['visible'] = False

    subplots['layout']['margin'] = {
        'l': 0,
        'r': 0,
        't': 20,
        'b': 1,
    }
    # height_calc = 50 * len(categories)
    # height_calc = max([height_calc, 350])
    subplots['layout']['height'] = height
    subplots['layout']['width'] = width

    return subplots


# ----------------------------------------------------------------------
def plot1(faculty):
    """"""
    config = {
        'labels': {'ocde': 'Area',
                   'sub_ocde': 'Subárea',
                   'count': ''
                   },
        'height': 500,
        # 'title': 'Áreas del Conocimiento - OCDE',
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

    fig.update_layout(xaxis_title='Grupos de investigación')
    # fig.update_traces(hoverinfo='none', hovertemplate = '')
    return fig

# # ----------------------------------------------------------------------
# @pyscript(plotly_out='dima-agendas')
# def plot2(faculty):
    # """"""
    # config = {
        # 'labels': {'knowledge': '',
                   # 'sub_ocde': 'Subáreas',
                   # 'count': 'Grupos de investigación',
                   # },
        # 'height': 500,
        # 'title': '',
        # 'template': 'plotly_white',

    # }

    # if faculty != 'All':
        # g = groups.loc[groups['facultad'] == faculty]
    # else:
        # g = groups

    # fig = px.histogram(g, y='knowledge', orientation='h', barmode='group', **config)
    # fig.update_layout(xaxis_title='Grupos de investigación')
    # fig.update_traces(hoverinfo='none', hovertemplate='')

    # return fig


# ----------------------------------------------------------------------
def plot2(faculty):
    """"""
    names = groups['knowledge'].value_counts(dropna=False).keys().tolist()
    counts = groups['knowledge'].value_counts(dropna=False).tolist()
    categories = [{'name': name, 'value': count} for name, count in zip(names, counts)]

    fig = plot_categories(categories, height=750, width=700)
    return fig


# ----------------------------------------------------------------------
def plot3(faculty):
    """"""
    names = groups['facultad'].value_counts(dropna=False).keys().tolist()
    counts = groups['facultad'].value_counts(dropna=False).tolist()
    categories = [{'name': name, 'value': count} for name, count in zip(names, counts)]

    fig = plot_categories(categories, height=200, width=500)
    return fig

# # ----------------------------------------------------------------------
# @pyscript(plotly_out='chart3')
# def plot3(faculty):
    # """"""
    # config = {
        # 'labels': {'departamento': '',
                   # 'sub_ocde': 'Subáreas',
                   # 'count': ''
                   # },
        # 'height': 500,
        # 'title': 'Departamentos',
        # 'template': 'plotly_white',
    # }

    # if faculty != 'All':
        # g = groups.loc[groups['facultad'] == faculty]
    # else:
        # g = groups

    # fig = px.histogram(g, y='departamento', orientation='h', barmode='group', **config)
    # fig.update_layout(xaxis_title='')
    # fig.update_traces(hoverinfo='none', hovertemplate='')

    # return fig


# ----------------------------------------------------------------------
def plot4(faculty):
    """"""
    if faculty != 'All':
        g = groups.loc[groups['facultad'] == faculty]['name'].tolist()
    else:
        g = groups['name'].tolist()

    return json.dumps({
        'groups': g
    })


# ----------------------------------------------------------------------
def plot_catego(faculty):
    """"""

    if faculty != 'All':
        g = groups.loc[groups['facultad'] == faculty]
    else:
        g = groups

    labels = g['categoria'].value_counts().keys()
    values = g['categoria'].value_counts().to_list()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+value', hole=.3)])
    fig.update_traces(hoverinfo='none', hovertemplate='')
    fig.update(layout_showlegend=False)

    return fig


# ----------------------------------------------------------------------
def load_group(name):
    """"""
    g = groups.loc[groups['name'] == name]
    grupo = g.to_dict('records')[0]

    return json.dumps(grupo)
