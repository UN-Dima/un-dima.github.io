from radiant.server import PyScriptAPI, pyscript, pyscript_globals
from browser import document, html
import json
import bootstrap as bs
from .custom_plots import CustomPlots
# from json import dumps as brython_serializer


########################################################################
class Group(PyScriptAPI, CustomPlots):
    """"""

    # ----------------------------------------------------------------------
    @pyscript_globals
    def _(self):
        """"""
        global groups, df
        import plotly.express as px
        import json
        import numpy as np
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        # from json import dumps as brython_serializer

    # ----------------------------------------------------------------------

    def make_card(self, value, label):
        """"""
        card = html.DIV(f"""
              <div class="card-body">
                <h1 class="card-title">{value}</h1>
                <p class="card-text">{label}</p>
              </div>
          """, Class='card', style={'width': '10rem', })
        document.select_one('#dima-counters') <= card

    # ----------------------------------------------------------------------
    def update_cards(self, data):
        """"""
        for k in data:
            if k == 'Investigadores':
                self.make_card(sum(data[k]), k)
            elif k == 'Facultades':
                pass
            elif isinstance(data[k], list):
                self.make_card(len(data[k]), k)
            else:
                self.make_card(data[k], k)
        document.select_one('#dima-counters').style = {'display': 'flex', }
        # document.select_one('#faculty') <= html.DIV('Facultades', Class='display-5')

        options = [{'text': g, 'value': g} for g in data['Facultades']]
        options = [{'text': 'Todas las facultades', 'value': 'All'}] + options
        document.select_one('#faculty') <= bs.form.Select('Hola', options,
                                                          on_change=self.render_plots)

    # ----------------------------------------------------------------------
    def update_groups(self, data):
        """"""
        document.select_one('#groups').clear()
        # document.select_one('#groups') <= html.DIV('Grupos de investigación', Class='display-5')
        options = [{'text': g, 'value': g} for g in data['groups']]
        document.select_one('#groups') <= bs.form.Select('Grupo de investigación', options,
                                                         on_change=self.lg)

    # ----------------------------------------------------------------------
    def loaded(self, data):
        """"""
        self.update_cards(data)
        self.render_plots()

    # ----------------------------------------------------------------------
    @pyscript(inline=True, callback='loaded:1000000')
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
        def get_categoria(df, g): return df[df['Nombre del grupo'] == g]['Categoría (Conv 781 de Colciencias 2017)'].tolist()[0]
        def get_lider(df, g): return df[df['Nombre del grupo'] == g]['Lider colciencias'].tolist()[0]

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
            groups.setdefault('categoria', []).append(get_categoria(df, group).capitalize())
            groups.setdefault('lider', []).append(get_lider(df, group).title())

        groups = pd.DataFrame.from_dict(groups)
        groups['knowledge'].replace('Cyt de minerales y materiales', 'Ciencia y tecnología de minerales y materiales', inplace=True)

        return json.dumps({
            'Grupos de investigación': np.unique(groups['name'].tolist()).tolist(),
            'Facultades': np.unique(groups['facultad'].tolist()).tolist(),
            'Departamentos': np.unique(groups['departamento'].tolist()).tolist(),
            'sedes_int?': list(set([sede.strip() for sede in ','.join(np.unique(df['Sedes_Int']).tolist()).split(',')])),
            'Investigadores': groups['members'].to_list(),
        })

    # ----------------------------------------------------------------------
    @pyscript(plotly_out='chart1')
    def plot1(self, faculty):
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
    # def plot2(self, faculty):
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
    @pyscript(plotly_out='dima-agendas')
    def plot2(self, faculty):
        """"""
        names = groups['knowledge'].value_counts(dropna=False).keys().tolist()
        counts = groups['knowledge'].value_counts(dropna=False).tolist()
        categories = [{'name': name, 'value': count} for name, count in zip(names, counts)]

        fig = self.plot_categories(categories, height=750, width=700)
        return fig

    # ----------------------------------------------------------------------
    @pyscript(plotly_out='dima-facultades')
    def plot3(self, faculty):
        """"""
        names = groups['facultad'].value_counts(dropna=False).keys().tolist()
        counts = groups['facultad'].value_counts(dropna=False).tolist()
        categories = [{'name': name, 'value': count} for name, count in zip(names, counts)]

        fig = self.plot_categories(categories, height=200, width=500)
        return fig

    # # ----------------------------------------------------------------------
    # @pyscript(plotly_out='chart3')
    # def plot3(self, faculty):
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
    @pyscript(callback='update_groups:10000')
    def plot4(self, faculty):
        """"""
        if faculty != 'All':
            g = groups.loc[groups['facultad'] == faculty]['name'].tolist()
        else:
            g = groups['name'].tolist()

        return json.dumps({
            'groups': g
        })

    # ----------------------------------------------------------------------
    @pyscript(plotly_out='dima-categoria')
    def plot_catego(self, faculty):
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
    def lg(self, event):
        """"""
        name = event.target.value
        self.load_group(name)

    # ----------------------------------------------------------------------
    @pyscript(callback='show_group_info:10000')
    def load_group(self, name):
        """"""
        g = groups.loc[groups['name'] == name]
        grupo = g.to_dict('records')[0]

        return json.dumps(grupo)
