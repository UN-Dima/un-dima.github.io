from radiant.server import pyscript


########################################################################
class CustomPlots:
    """"""
    # ----------------------------------------------------------------------
    @pyscript()
    def plot_categories(self, categories, height=500, width=1000):
        """"""
        subplots = make_subplots(
            rows=len(categories),
            cols=1,
            subplot_titles=[x["name"] for x in categories],
            shared_xaxes=True,
            print_grid=False,
            vertical_spacing=(0.45 / len(categories)),
        )
        subplots['layout'].update(
            width=550,
            plot_bgcolor='#fff',
        )

        for k, x in enumerate(categories):
            subplots.add_trace(dict(
                type='bar',
                orientation='h',
                y=[x["name"]],
                x=[x["value"]],
                text=["{:,.0f}".format(x["value"])],
                hoverinfo='text',
                textposition='auto',
                marker=dict(
                    color="#636efa",
                ),
            ), k + 1, 1)

        subplots['layout'].update(
            showlegend=False,
        )

        for x in subplots["layout"]['annotations']:
            x['x'] = 0
            x['xanchor'] = 'left'
            x['align'] = 'left'
            x['font'] = dict(
                size=12,
            )

        for axis in subplots['layout']:
            if axis.startswith('yaxis') or axis.startswith('xaxis'):
                subplots['layout'][axis]['visible'] = False

        subplots['layout']['margin'] = {
            'l': 0,
            'r': 0,
            't': 20,
            'b': 1,
        }
        # height_calc = 50 * len(categories)
        # height_calc = max([height_calc, 350])
        subplots['layout']['height'] = height
        subplots['layout']['width'] = width

        return subplots
