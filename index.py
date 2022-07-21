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
        self.add_css_file('root/styles.css')
        self.add_css_file('/root/styles.css')
        # self.on_load(self.ready, 'DOMContentLoaded')
        self.load_database()

        # for btn in document.select('.btn-check'):
            # btn.addEventListener('click', self.fn)

    # # ----------------------------------------------------------------------
    # def fn(self, evt):
        # """"""
        # self.render_plots(evt.target.attrs['dima-facultad'])

    # ----------------------------------------------------------------------
    def render_plots(self, event=None):
        """"""
        if event is None:
            faculty = 'All'
        else:
            faculty = event.target.value

        self.plot1(faculty)
        self.plot2(faculty)
        self.plot3(faculty)
        self.plot4(faculty)
        self.plot_catego(faculty)

    # ----------------------------------------------------------------------
    def show_group_info(self, data):
        """"""
        print('#' * 70)
        print(data)
        style_cat = {
            'float': 'right',
            'color': '#636efa',
        }
        document.select_one('.dima-group').clear()
        document.select_one('.dima-group') <= html.H1(data['categoria'], Class='display-1', style=style_cat)
        document.select_one('.dima-group') <= html.H1(data['name'], Class='display-4')
        document.select_one('.dima-group') <= html.H1(f'{data["departamento"]}', Class='h3')
        document.select_one('.dima-group') <= html.H1(f'Director: {data["lider"]}', Class='h5', style={'margin-bottom': '500px', })
        # document.select_one('.dima-group') <= html.H1(f'ODCE: {data["ocde"]},  {data["sub_ocde"]}', Class='h3')


if __name__ == '__main__':
    RadiantServer('BareMinimum',
                  template=os.path.join('templates', 'layout.html'),
                  static_app=True,
                  templates_path='templates',
                  )
