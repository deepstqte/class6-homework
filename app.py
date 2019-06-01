# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from itertools import combinations

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.config['suppress_callback_exceptions']=True

SCALE = 25
SCALE_LIST = ["{0}".format(i+1) for i in range(0, SCALE)]

features = {
        "CRIM": "CRIM - per capita crime rate by town",
        "ZN": "ZN - proportion of residential land zoned for lots over 25,000 sq.ft.",
        "INDUS": "INDUS - proportion of non-retail business acres per town",
        "CHAS": "CHAS - If tract bounds Charles River or not",
        "NOX": "NOX - nitric oxides concentration (parts per 10 million)",
        "RM": "RM - average number of rooms per dwelling",
        "AGE": "AGE - proportion of owner-occupied units built prior to 1940",
        "DIS": "DIS - weighted distances to five Boston employment centres",
        "RAD": "RAD - index of accessibility to radial highways",
        "TAX": "TAX - full-value property-tax rate per $10,000",
        "PTRATIO": "PRRATIO - pupil-teacher ratio by town",
        "B": "B - 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town",
        "LSTAT": "LSTAT - % lower status of the population",
        "MEDV": "MEDV - Median value of owner-occupied homes in $1000's",
}

housing_df = pd.read_csv("housing.data", names=features.keys(), delim_whitespace=True)

feature_couples = list(combinations(features.keys(), 2))

children = [
    html.Div(
        children=[
            html.P(
                children='X Axis:'
            ),
            dcc.Dropdown(
                id='xaxis',
                options=[{'label': j, 'value': i} for (i, j) in features.items()],
                value='DIS'
            )
        ]
    ),
    html.Div(
        children=[
            html.P(
                children='Y Axis:'
            ),
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': j, 'value': i} for (i, j) in features.items()],
                value='LSTAT'
            )
        ]
    ),
    html.Div(
        children=[
            html.P(
                children='Graph Type:'
            ),
            dcc.Dropdown(
                id='plot_type',
                options=[{'label': i, 'value': j} for (i, j) in [
                    ("Heatmap", "heatmap"),
                    ("Scatter", "scatter")
                ]],
                value='heatmap'
            )
        ]
    )
]

app.layout = html.Div(children=[
        html.Div(children=children),
        html.Div(id="graphs")
    ])

@app.callback(
    Output('graphs', 'children'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value'),
     Input('plot_type', 'value')])
def update_graphs(x, y, plot_type):
    i = 0
    graphs = []
    row_children = []
    for dim3 in features.keys():
        if dim3 not in (x, y):
            grouped_housing_df = housing_df
            grouped_housing_df[f'{x}_GROUP'] = pd.cut(housing_df[f'{x}'], SCALE, labels=SCALE_LIST)
            grouped_housing_df[f'{y}_GROUP'] = pd.cut(housing_df[f'{y}'], SCALE, labels=SCALE_LIST)
            matrix = pd.pivot_table(grouped_housing_df, values=dim3, index=f'{x}_GROUP', columns=f'{y}_GROUP', aggfunc='mean')
            if (plot_type == 'heatmap'):
                graph = dcc.Graph(
                            id=f'heatmap-{x}-{y}-{dim3}',
                            figure={
                                'data': [
                                    go.Heatmap(
                                        x=list(range(1, matrix.shape[0]+1)),
                                        y=list(range(1, matrix.shape[1]+1)),
                                        z=matrix.values.tolist(),
                                        colorscale='Viridis',
                                    )
                                ],
                                'layout': go.Layout(title=f"{features[dim3]}", xaxis={"title": features[x]}, yaxis={"title": features[y]})
                            },
                        )
            elif (plot_type == 'scatter'):
                graph = dcc.Graph(
                            id=f'scatter-{x}-{y}-{dim3}',
                            figure={
                                'data': [
                                    go.Scatter(
                                        x=housing_df[f'{x}'],
                                        y=housing_df[f'{y}'],
                                        mode='markers',
                                        marker={
                                            'size': housing_df[f'{dim3}']
                                        }
                                    )
                                ],
                                'layout': go.Layout(title=f"{features[dim3]}", xaxis={"title": features[x]}, yaxis={"title": features[y]})
                            },
                        )
            graphs.append(html.Div(children=graph, className='five columns'))
            i = i+1
    return(graphs)

if __name__ == '__main__':
    app.run_server(debug=True)
