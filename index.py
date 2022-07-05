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
        self.add_css_file('templates/styles.css')

        self.load_database()

        # container = html.DIV(Class='container')

        for btn in document.select('.btn-check'):
            btn.addEventListener('click', self.fn)

        # b = Button('All')
        # container <= b
        # b.bind('click', lambda evt: self.render_plots('All'))

        # b2 = Button('FIA')
        # container <= b2
        # b2.bind('click', lambda evt: self.render_plots('Facultad de ingeniería y arquitectura'))

        # document.select_one('#dima-toolbar') <= container

    # ----------------------------------------------------------------------
    def fn(self, evt):
        """"""
        self.render_plots(evt.target.attrs['dima-facultad'])

    # ----------------------------------------------------------------------
    def render_plots(self, faculty='All'):
        """"""
        self.process_data()
        self.plot1(faculty)
        self.plot2(faculty)
        self.plot3(faculty)


if __name__ == '__main__':
    RadiantServer('BareMinimum',
                  template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  )
