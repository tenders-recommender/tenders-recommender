import json
from importlib.resources import open_binary

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio


def make_plot():
    data = json.load(open_binary('resources.plots', 'rmse_svd_params.json'))
    complete_df = pd.DataFrame(data)
    complete_df['mean_time'] = complete_df['mean_fit_time'] + complete_df['mean_test_time']
    complete_df['std_time'] = complete_df['std_fit_time'] + complete_df['std_test_time']

    chosen_df = complete_df
    chosen_df = chosen_df[chosen_df['param_biased']]
    chosen_df = chosen_df[chosen_df['param_init_mean'] == 0]
    chosen_df = chosen_df[chosen_df['param_n_epochs'] == 50]
    chosen_df = chosen_df[chosen_df['param_init_std_dev'] == 0.0]
    chosen_df = chosen_df[chosen_df['param_lr_all'] == 0.01]
    chosen_df = chosen_df[chosen_df['param_n_factors'] == 50]
    chosen_df = chosen_df[chosen_df['param_reg_all'] == 0.01]

    print(complete_df)
    print(chosen_df)

    max_y = (complete_df['mean_test_rmse'] + complete_df['std_test_rmse']).max() * 1.05
    max_x = (complete_df['mean_time'] + complete_df['std_time']).max() * 1.05

    traces = [
        go.Scatter(
            y=complete_df['mean_test_rmse'],
            x=complete_df['mean_time'],
            error_y={
                'array': complete_df['std_test_rmse']
            },
            error_x={
                'array': complete_df['std_time']
            },
            opacity=0.25,
            mode='markers',
            marker=go.scatter.Marker(
                size=1
            )
        ),
        go.Scatter(
            y=chosen_df['mean_test_rmse'],
            x=chosen_df['mean_time'],
            error_y={
                'array': chosen_df['std_test_rmse'],
                'color': 'red'
            },
            error_x={
                'array': chosen_df['std_time'],
                'color': 'red'
            },
            opacity=1,
            mode='markers',
            marker=go.scatter.Marker(
                size=5,
                color='red'
            )
        )
    ]

    layout = go.Layout(
        width=700,
        height=800,
        showlegend=False,
        margin=go.layout.Margin(
            t=10,
            b=40,
            l=80,
            r=40
        ),
        legend=go.layout.Legend(
            orientation='h'
        ),
        xaxis=go.layout.XAxis(
            title='Training time [s]',
            autorange=False,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            range=[0, max_x],
            dtick=5,
        ),
        yaxis=go.layout.YAxis(
            title='RMSE',
            autorange=False,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            range=[0, max_y],
            dtick=0.1,
            tickangle=-30
        ),
        annotations=[
            go.layout.Annotation(
                y=chosen_df['mean_test_rmse'].values[0] * 0.9,
                x=chosen_df['mean_time'].values[0] * 1.03,
                text='Chosen combination of parameters',
                showarrow=True,
                ax=40,
                ay=40
            )
        ]
    )

    fig = go.Figure(data=traces, layout=layout)

    pio.write_image(fig, 'svd_chosen_params_comparison.svg')


if __name__ == '__main__':
    make_plot()
