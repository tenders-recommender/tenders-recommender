import json
from importlib.resources import open_binary

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio


def make_plot():
    data = json.load(open_binary('resources.plots', 'rmse_svd_time_step.json'))
    complete_df = pd.DataFrame(data)
    complete_df['earlier_than'] *= 1000

    print(complete_df)

    traces = [go.Scatter(
        y=complete_df['rmse'],
        x=complete_df['earlier_than'],
        mode='markers+lines',
        marker=go.scatter.Marker(
            size=5
        ),
        line=go.scatter.Line(
            shape='spline',
            smoothing=1.3
        )
    )]

    layout = go.Layout(
        width=700,
        height=800,
        showlegend=False,
        margin=go.layout.Margin(
            t=10,
            b=80,
            l=80,
            r=80
        ),
        legend=go.layout.Legend(
            orientation='h'
        ),
        xaxis=go.layout.XAxis(
            title='Date of last interaction',
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            tickformat='%Y-%m-%d',
            tickmode='linear',
            dtick='M3',
            type='date'
        ),
        yaxis=go.layout.YAxis(
            title='RMSE',
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            dtick=0.02,
            tickangle=-30
        )
    )

    fig = go.Figure(data=traces, layout=layout)

    pio.write_image(fig, 'svd_time_step_timestamp.svg')


if __name__ == '__main__':
    make_plot()
