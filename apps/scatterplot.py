import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output
from app import app

from src.data import columns, df
from src.helper import remove_outlier

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Settings', className='card-title')
                ], className='card-header'),
                html.Div([
                    html.Div([
                        dcc.Markdown('**X Axis:**'),
                        dcc.Dropdown(
                            id='x_axis_dropdown_scatterplot',
                            options=[{'label': value, 'value': key}
                                     for key, value in columns.items()],
                            value='active_product'
                        )
                    ], className='form-group'),
                    html.Div([
                        dcc.Markdown('**Y Axis:**'),
                        dcc.Dropdown(
                            id='y_axis_dropdown_scatterplot',
                            options=[{'label': value, 'value': key}
                                     for key, value in columns.items()],
                            value='product_sold'
                        )
                    ], className='form-group'),
                    html.Div([
                        dcc.Markdown('**Outlier:**'),
                        dcc.RadioItems(
                            id='outlier_radio_scatterplot',
                            labelStyle={'margin-right': '0.5rem'},
                            options=[
                                {'label': 'Without Outlier', 'value': 0},
                                {'label': 'With Outlier', 'value': 1},
                            ],
                            value=0
                        )
                    ], className='form-group')
                ], className='card-body')
            ], className='card')
        ], className='col-lg-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Scatter Plot', className='card-title')
                ], className='card-header'),
                html.Div([
                    dcc.Graph(id='graph_scatterplot')
                ], className='card-body', style={'padding-top': '0'}),
            ], className='card')
        ], className='col-lg-9')
    ], className='row row-deck')
], className='container')


@app.callback(
    Output('graph_scatterplot', 'figure'),
    [
        Input('x_axis_dropdown_scatterplot', 'value'),
        Input('y_axis_dropdown_scatterplot', 'value'),
        Input('outlier_radio_scatterplot', 'value'),
    ]
)
def update_graph_scatterplot(x_axis, y_axis, with_outlier):
    if not with_outlier:
        if x_axis != y_axis:
            dff_x = pd.DataFrame(remove_outlier(df, x_axis))
            dff_y = pd.DataFrame(remove_outlier(df, y_axis))
            dff = dff_x.join(dff_y, how='inner')
        else:
            dff = pd.DataFrame(remove_outlier(df, x_axis))
    else:
        dff = df
    figure = {
        'data': [
            go.Scattergl(
                x=dff[x_axis],
                y=dff[y_axis],
                mode='markers'
            )
        ],
        'layout': {
            'title': 'Scatter Plot of {} and {}'.format(columns[x_axis], columns[y_axis]),
            'xaxis': {
                'title': columns[x_axis]
            },
            'yaxis': {
                'title': columns[y_axis]
            }
        }
    }
    return figure