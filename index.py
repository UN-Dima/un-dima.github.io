#!brython

import os
from radiant.server import RadiantAPI, RadiantServer, pyscript
from browser import document, html
from visualizations import Group
from bootstrap.btn import Button

########################################################################


class BareMinimum(RadiantAPI, Group):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.load_database()

        container = html.DIV(Class='container')

        # b = Button('Load database')
        # container <= b
        # b.bind('click', lambda evt: self.load_database())

        b2 = Button('Plot')
        container <= b2
        b2.bind('click', lambda evt: self.render_plots())

        document.select_one('body') <= container

    # ----------------------------------------------------------------------
    def render_plots(self):
        self.plot()
        self.plot2()
        self.plot3()


if __name__ == '__main__':
    RadiantServer('BareMinimum',
                  template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  )
