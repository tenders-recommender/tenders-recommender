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
    complete_df = complete_df[complete_df['param_biased']]

    print(complete_df)

    # max_y = (complete_df['rmse']['mean'] + complete_df['rmse']['std']).max() * 1.1
    max_x = (complete_df['mean_time'] + complete_df['std_time']).max() * 1.1

    traces = []
    for index, value in enumerate(complete_df['param_init_mean'].unique()):
        value_df = complete_df[complete_df['param_init_mean'] == value]

        trace = go.Scatter(
            y=value_df['mean_test_rmse'],
            x=value_df['mean_time'],
            error_y={
                'array': value_df['std_test_rmse']
            },
            error_x={
                'array': value_df['std_time']
            },
            mode='markers',
            marker=go.scatter.Marker(
                size=5
            ),
            name=str(value)
        )

        traces.append(trace)

    layout = go.Layout(
        width=700,
        height=800,
        showlegend=True,
        margin=go.layout.Margin(
            t=10,
            b=40,
            l=80,
            r=40
        ),
        legend=go.layout.Legend(
            orientation='v'
        ),
        xaxis=go.layout.XAxis(
            title='Training time [s]',
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            range=[0, max_x],
            dtick=5,
        ),
        yaxis=go.layout.YAxis(
            title='RMSE',
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            dtick=0.01,
            tickangle=-30
        )
    )

    fig = go.Figure(data=traces, layout=layout)

    pio.write_image(fig, 'svd_init_mean_comparison.svg')


if __name__ == '__main__':
    make_plot()
