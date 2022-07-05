from radiant.server import PyScriptAPI, pyscript
from browser import document, html
import json


########################################################################
class Group(PyScriptAPI):
    """"""

    # ----------------------------------------------------------------------
    def callback_fn(self, data):
        """"""
        data = json.loads(data)
        document.select_one('#dima-counters-facultades').html = f'{len(data["facultades"])}'
        document.select_one('#dima-counters-grupos').html = f'{len(data["grupos"])}'
        document.select_one('#dima-counters-departamentos').html = f'{len(data["departamentos"])}'
        document.select_one('#dima-counters').style = {'display': 'flex', }

    # ----------------------------------------------------------------------
    @pyscript(output='RAW', callback='callback_fn')
    def process_data(self):
        """"""
        global groups, df

        import json
        import numpy as np

        return json.dumps({
            'grupos': np.unique(df['Nombre del grupo'].tolist()),
            'facultades': np.unique(groups['facultad'].tolist()),
            'departamentos': np.unique(groups['departamento'].tolist()),

        })

    # ----------------------------------------------------------------------
    @pyscript(inline=True)
    def load_database(self):
        """"""
        global groups, df
        import json

        from pyodide.http import open_url
        import pandas as pd
        import numpy as np

        filenames = ['/root/databases/FIA.csv', '/root/databases/FA.csv', '/root/databases/FCEN.csv']
        df = pd.concat([pd.read_csv(open_url(f)) for f in filenames])
        for col in df.columns:
            df[col] = df[col].fillna(method='ffill')

        ids = np.unique(df['Nombre del grupo'].tolist())

        def get_name(df, g): return df[df['Nombre del grupo'] == g]['Nombre del grupo'].tolist()[0]
        def get_members(df, g): return df[df['Nombre del grupo'] == g]
        # get_line = lambda df,g:df[df['Nombre del grupo'] == g]['Lineas de Investigación'].tolist()[0]
        def get_sub_OCDE(df, g): return df[df['Nombre del grupo'] == g]['Area_Conocimiento_OCDE'].tolist()[0]
        def get_OCDE(df, g): return df[df['Nombre del grupo'] == g]['Area_OCDE'].tolist()[0]
        def get_know(df, g): return df[df['Nombre del grupo'] == g]['Agenda del Conocimiento'].tolist()[0]
        def get_facultad(df, g): return df[df['Nombre del grupo'] == g]['Facultad'].tolist()[0]
        def get_departamento(df, g): return df[df['Nombre del grupo'] == g]['Departamento'].tolist()[0]

        groups = {}
        for group in ids:
            groups.setdefault('members', []).append(len(get_members(df, group)))
            groups.setdefault('name', []).append(get_name(df, group).capitalize())
            # groups.setdefault('line', []).append(get_line(df, group).capitalize())
            groups.setdefault('sub_ocde', []).append(get_sub_OCDE(df, group).capitalize())
            groups.setdefault('ocde', []).append(get_OCDE(df, group).capitalize())
            groups.setdefault('knowledge', []).append(get_know(df, group).capitalize())
            groups.setdefault('facultad', []).append(get_facultad(df, group).replace('4- ', '').capitalize())
            groups.setdefault('departamento', []).append(get_departamento(df, group).replace('4- ', '').capitalize())

        groups = pd.DataFrame.from_dict(groups)
        groups['knowledge'].replace('Cyt de minerales y materiales', 'Ciencia y tecnología de minerales y materiales', inplace=True)

    # ----------------------------------------------------------------------

    @pyscript(inline=True, plotly_out='chart1')
    def plot1(self, faculty):
        """"""
        global groups

        import plotly.express as px
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
    @pyscript(inline=True, plotly_out='chart2')
    def plot2(self, faculty):
        """"""
        global groups

        import plotly.express as px

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
    @pyscript(inline=True, plotly_out='chart3')
    def plot3(self, faculty):
        """"""
        global groups

        import plotly.express as px

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

    # # ----------------------------------------------------------------------
    # @pyscript(plotly_out='chart4')
    # def plot4(self):
        # """"""
        # global groups

        # import plotly.express as px
        # import numpy as np

        # config = {
            # 'labels': {'facultad': '',
                       # 'sub_ocde': 'Subáreas',
                       # 'count': ''
                       # },
            # 'height': 400,
            # 'title': 'Facultad',
            # 'template': 'plotly_white',
        # }

        # fig = px.histogram(groups, y='facultad', orientation='h', barmode='group', **config)
        # fig.update_layout(xaxis_title='')
        # fig.update_traces(hoverinfo='none', hovertemplate='')

        # return fig

