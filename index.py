#!brython

import os
from radiant.server import RadiantAPI, RadiantServer
from browser import document, html
from visualizations import Group


########################################################################
class BareMinimum(RadiantAPI, Group):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.plot()


if __name__ == '__main__':
    RadiantServer('BareMinimum',
                  template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  )
