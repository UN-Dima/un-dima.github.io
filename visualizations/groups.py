from radiant.server import PyScriptAPI, pyscript


########################################################################
class Group(PyScriptAPI):
    """"""

    # ----------------------------------------------------------------------
    @pyscript(output='RAW', callback='callback_fn')
    def process_data(self):
        """"""
        return {'hola': 'mundo',
                'Nania': True,
                'Ezis': 3.5,
                }

    # ----------------------------------------------------------------------
    def callback_fn(self, data):
        """"""
        self.data = data
        print(f'CALLBACK: {self.data}')

    # ----------------------------------------------------------------------
    @pyscript(inline=True)
    def load_database(self):
        """"""
        global groups

        from pyodide.http import open_url
        import pandas as pd
        import numpy as np

        df = pd.read_csv(open_url("/root/databases/RGI.csv"))

        for col in df.columns:
            df[col] = df[col].fillna(method='ffill')

        ids = np.unique(df['Nombre del grupo'].tolist())

        def get_name(df, g): return df[df['Nombre del grupo'] == g]['Nombre del grupo'].tolist()[0]
        def get_members(df, g): return df[df['Nombre del grupo'] == g]
        def get_line(df, g): return df[df['Nombre del grupo'] == g]['Lineas de Investigación'].tolist()[0]
        def get_OCDE(df, g): return df[df['Nombre del grupo'] == g]['Area_Conocimiento_OCDE'].tolist()[0]
        def get_OCDE2(df, g): return df[df['Nombre del grupo'] == g]['Area_OCDE'].tolist()[0]
        def get_know(df, g): return df[df['Nombre del grupo'] == g]['Agenda del Conocimiento'].tolist()[0]

        groups = {}
        for group in ids:
            groups.setdefault('members', []).append(len(get_members(df, group)))
            groups.setdefault('name', []).append(get_name(df, group).capitalize())
            groups.setdefault('line', []).append(get_line(df, group).capitalize())
            groups.setdefault('ocde', []).append(get_OCDE(df, group).capitalize())
            groups.setdefault('ocde2', []).append(get_OCDE2(df, group).capitalize())
            groups.setdefault('knowledge', []).append(get_know(df, group).capitalize())

        groups = pd.DataFrame.from_dict(groups)
        # groups.head()

    # ----------------------------------------------------------------------
    @pyscript(plotly_out='chart1')
    def plot(self):
        """"""
        global groups

        import plotly.express as px
        fig = px.bar(groups, y='ocde', orientation='h')
        return fig

    # ----------------------------------------------------------------------

    @pyscript(plotly_out='chart2')
    def plot2(self):
        """"""
        global groups

        import plotly.express as px
        fig = px.bar(groups, y='ocde2', orientation='h')
        return fig

    # ----------------------------------------------------------------------
    @pyscript(plotly_out='chart3')
    def plot3(self):
        """"""
        global groups

        import plotly.express as px
        fig = px.bar(groups, y='knowledge', orientation='h')
        return fig

