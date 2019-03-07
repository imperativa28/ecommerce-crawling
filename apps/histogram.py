import dash_core_components as dcc
import dash_html_components as html
import math
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
                    html.H3('Settings', className='card-title',
                            )
                ], className='card-header'),
                html.Div([
                    html.Div([
                        dcc.Markdown('**Column:**'),
                        dcc.Dropdown(
                            id='column_dropdown_histogram',
                            options=[{'label': value, 'value': key}
                                     for key, value in columns.items()],
                            value='active_product'
                        )
                    ], className='form-group'),
                    html.Div([
                        dcc.Markdown('**Outlier:**'),
                        dcc.RadioItems(
                            id='outlier_radio_histogram',
                            labelStyle={'margin-right': '0.5rem'},
                            options=[
                                {'label': 'Without Outlier', 'value': 0},
                                {'label': 'With Outlier', 'value': 1},
                            ],
                            value=0
                        )
                    ], className='form-group'),
                    html.Div([
                        dcc.Markdown('**Bins:**'),
                        dcc.Input(
                            id='bin_input_histogram',
                            placeholder='Bins',
                            type='number',
                            value='20',
                            min=1,
                            max=100,
                            step=1
                        )
                    ], className='form-group')
                ], className='card-body')
            ], className='card')
        ], className='col-lg-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Histogram', className='card-title')
                ], className='card-header'),
                html.Div([
                    dcc.Graph(id='graph_histogram'),
                    dcc.RangeSlider(
                        id='data_range_slider_histogram',
                        step=1,
                    )
                ], className='card-body', style={'padding-top': '0'}),
            ], className='card')
        ], className='col-lg-9'),
    ], className='row row-deck'),
], className='container')


@app.callback(
    Output('outlier_radio_histogram', 'value'),
    [Input('column_dropdown_histogram', 'value')]
)
def update_outlier_radio_histogram_value(column):
    return 0


@app.callback(
    Output('data_range_slider_histogram', 'min'),
    [
        Input('column_dropdown_histogram', 'value'),
        Input('outlier_radio_histogram', 'value')
    ]
)
def update_data_range_slider_histogram_min(column, with_outlier):
    return df[column].min() if with_outlier else remove_outlier(df, column).min()


@app.callback(
    Output('data_range_slider_histogram', 'max'),
    [
        Input('column_dropdown_histogram', 'value'),
        Input('outlier_radio_histogram', 'value')
    ]
)
def update_data_range_slider_histogram_max(column, with_outlier):
    return df[column].max() if with_outlier else remove_outlier(df, column).max()


@app.callback(
    Output('data_range_slider_histogram', 'value'),
    [
        Input('data_range_slider_histogram', 'min'),
        Input('data_range_slider_histogram', 'max')
    ]
)
def update_data_range_slider_histogram_value(min_value, max_value):
    return [min_value, max_value]


@app.callback(
    Output('data_range_slider_histogram', 'marks'),
    [
        Input('data_range_slider_histogram', 'min'),
        Input('data_range_slider_histogram', 'max')
    ]
)
def update_data_range_slider_histogram_marks(min_value, max_value):
    return {min_value: {'label': str(min_value)}, max_value: {'label': str(max_value)}}


@app.callback(
    Output('graph_histogram', 'figure'),
    [
        Input('column_dropdown_histogram', 'value'),
        Input('bin_input_histogram', 'value'),
        Input('data_range_slider_histogram', 'value')
    ]
)
def update_graph_histogram(column, bin, range_value):
    figure = {
        'data': [
            go.Histogram(
                x=df[column],
                xbins=dict(
                    start=range_value[0],
                    end=range_value[1],
                    size=math.ceil((range_value[1] - range_value[0])/int(bin))
                ),
            )
        ],
        'layout': {
            'title': 'Histogram of {}'.format(columns[column]),
            'xaxis': {
                'title': columns[column]
            },
            'yaxis': {
                'title': 'Shops'
            }
        }
    }
    return figure