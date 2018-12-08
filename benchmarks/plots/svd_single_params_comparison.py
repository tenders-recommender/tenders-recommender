import json
from importlib.resources import open_binary

import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio


def create_default_df():
    data = json.load(open_binary('resources.plots', 'rmse_svd_params.json'))
    complete_df = pd.DataFrame(data)
    complete_df['mean_time'] = complete_df['mean_fit_time'] + complete_df['mean_test_time']
    complete_df['std_time'] = complete_df['std_fit_time'] + complete_df['std_test_time']

    return complete_df


def make_plot(complete_df: pd.DataFrame, param_name: str, x_dtick: float, y_dtick: float):
    print(complete_df)

    max_x = (complete_df['mean_time'] + complete_df['std_time']).max() * 1.1

    traces = []
    for index, value in enumerate(complete_df['param_' + param_name].unique()):
        value_df = complete_df[complete_df['param_' + param_name] == value]

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
            dtick=x_dtick,
        ),
        yaxis=go.layout.YAxis(
            title='RMSE',
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            showticklabels=True,
            dtick=y_dtick,
            tickangle=-30
        )
    )

    fig = go.Figure(data=traces, layout=layout)

    pio.write_image(fig, 'svd_' + param_name + '_comparison.svg')


def make_param_biased_plot():
    df = create_default_df()
    make_plot(df, 'biased', 5, 0.1)


def make_param_init_mean_plot():
    df = create_default_df()
    df = df[df['param_biased']]
    make_plot(df, 'init_mean', 5, 0.01)


def make_param_n_epochs_plot():
    df = create_default_df()
    df = df[df['param_biased']]
    df = df[df['param_init_mean'] == 0]
    make_plot(df, 'n_epochs', 5, 0.01)


def make_param_init_std_dev_plot():
    df = create_default_df()
    df = df[df['param_biased']]
    df = df[df['param_init_mean'] == 0]
    df = df[df['param_n_epochs'] == 50]
    make_plot(df, 'init_std_dev', 5, 0.01)


def make_param_lr_all_plot():
    df = create_default_df()
    df = df[df['param_biased']]
    df = df[df['param_init_mean'] == 0]
    df = df[df['param_n_epochs'] == 50]
    df = df[df['param_init_std_dev'] == 0.0]
    make_plot(df, 'lr_all', 5, 0.002)


def make_param_n_factors_plot():
    df = create_default_df()
    df = df[df['param_biased']]
    df = df[df['param_init_mean'] == 0]
    df = df[df['param_n_epochs'] == 50]
    df = df[df['param_init_std_dev'] == 0.0]
    df = df[df['param_lr_all'] == 0.01]
    make_plot(df, 'n_factors', 5, 0.001)


def make_param_reg_all_plot():
    df = create_default_df()
    df = df[df['param_biased']]
    df = df[df['param_init_mean'] == 0]
    df = df[df['param_n_epochs'] == 50]
    df = df[df['param_init_std_dev'] == 0.0]
    df = df[df['param_lr_all'] == 0.01]
    df = df[df['param_n_factors'] == 50]
    make_plot(df, 'reg_all', 0.05, 0.001)


if __name__ == '__main__':
    make_plot()
