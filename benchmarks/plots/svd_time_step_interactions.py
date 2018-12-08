import json
from importlib.resources import open_binary

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio


def make_plot():
    data = json.load(open_binary('resources.plots', 'rmse_svd_time_step.json'))
    complete_df = pd.DataFrame(data)

    max_y = complete_df['rmse'].max() * 1.05
    max_x = complete_df['interactions'].max() * 1.05

    print(complete_df)

    traces = [go.Scatter(
        y=complete_df['rmse'],
        x=complete_df['interactions'],
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
            b=40,
            l=80,
            r=80
        ),
        legend=go.layout.Legend(
            orientation='h'
        ),
        xaxis=go.layout.XAxis(
            title='Amount of interactions',
            autorange=False,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            tickmode='linear',
            range=[0, max_x],
            dtick=25000
        ),
        yaxis=go.layout.YAxis(
            title='RMSE',
            autorange=False,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            range=[0, max_y],
            dtick=0.02,
            tickangle=-30
        )
    )

    fig = go.Figure(data=traces, layout=layout)

    pio.write_image(fig, 'svd_time_step_interactions.svg')


if __name__ == '__main__':
    make_plot()
