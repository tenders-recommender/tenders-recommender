import json
from importlib.resources import open_binary

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio


def make_plot():
    data = json.load(open_binary('resources.plots', 'rmse_alg.json'))
    raw_df = pd.DataFrame(data)
    grouped_df = raw_df.groupby('algorithm')
    complete_df = grouped_df.agg({'rmse': ['mean', 'std'], 'time_elapsed': ['mean', 'std']})\
        .sort_values(by=('rmse', 'mean'), ascending=True)

    print(complete_df)

    max_x = (complete_df['rmse']['mean'] + complete_df['rmse']['std']).max() * 1.1
    max_y = (complete_df['time_elapsed']['mean'] + complete_df['time_elapsed']['std']).max() * 1.1

    traces = []
    for index, algorithm in enumerate(complete_df.index.values):
        trace = go.Scatter(
            y=[complete_df['rmse']['mean'][index]],
            x=[complete_df['time_elapsed']['mean'][index]],
            error_y={
                'value': complete_df['rmse']['std'][index],
                'type': 'constant'
            },
            error_x={
                'value': complete_df['time_elapsed']['std'][index],
                'type': 'constant'
            },
            mode='markers',
            name=algorithm
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
            orientation='h'
        ),
        xaxis=go.layout.XAxis(
            title='Training time [s]',
            autorange=False,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            range=[0, max_y],
            dtick=2,
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

    pio.write_image(fig, 'alg_comparison.svg')


if __name__ == '__main__':
    make_plot()
