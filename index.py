#!brython

import os
from radiant.server import RadiantAPI, RadiantServer, pyscript
from browser import document, html
from visualizations import Group
from bootstrap.btn import Button
import logging


########################################################################
class BareMinimum(RadiantAPI, Group):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.add_css_file('/root/styles.css')
        # self.on_load(self.ready, 'DOMContentLoaded')
        self.load_database()

        for btn in document.select('.btn-check'):
            btn.addEventListener('click', self.fn)

    # ----------------------------------------------------------------------
    def fn(self, evt):
        """"""
        self.render_plots(evt.target.attrs['dima-facultad'])

    # ----------------------------------------------------------------------
    def render_plots(self, faculty='All'):
        """"""
        self.plot1(faculty)
        self.plot2(faculty)
        self.plot3(faculty)


if __name__ == '__main__':
    RadiantServer('BareMinimum',
                  template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  )
