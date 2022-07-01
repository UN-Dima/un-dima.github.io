from radiant.server import pyscript


########################################################################
class Group:
    """"""

    # ----------------------------------------------------------------------
    @pyscript(output=None)
    def plot(self):
        """"""
        def show(fig, chart):
            import json
            import plotly
            import js
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            js.Plotly.newPlot(chart, js.JSON.parse(graphJSON), {})

        import plotly.express as px

        fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
        show(fig, 'chart1')

