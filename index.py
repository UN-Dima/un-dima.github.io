#!brython

import os
from radiant.server import RadiantAPI, RadiantServer, pyscript
from browser import document, html


########################################################################
class BareMinimum(RadiantAPI):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

        document.select_one('body') <= html.DIV(id='mpl')
        self.plot()

    # ----------------------------------------------------------------------
    @pyscript(output=None)
    def plot(self):
        """"""
        # Import libraries
        import pandas as pd
        import js
        import json
        import plotly
        import plotly.express as px

        from js import document
        from pyodide import create_proxy
        from pyodide.http import open_url

        def plot(chart):
            #fig = px.line(df,
                          #x="Month", y=chart,
                          #width=800, height=400)
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            js.plot(graphJSON, "chart1")
            #js.Plotly.newPlot('chart1', graphJSON, {})

        #def selectChange(event):
            #choice = document.getElementById("select").value
            #plot(choice)

        #def setup():
            ## Create a JsProxy for the callback function
            #change_proxy = create_proxy(selectChange)

            #e = document.getElementById("select")
            #e.addEventListener("change", change_proxy)

        #setup()

        plot('Tmax')


if __name__ == '__main__':
    RadiantServer('BareMinimum',
                  template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  )
