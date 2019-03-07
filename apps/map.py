import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output
from app import app

from src.data import columns, df, mapblox_token
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
                        dcc.Markdown('**Map type:**'),
                        dcc.Dropdown(
                            id='type_dropdown_map',
                            options=[{'label': 'Distributed', 'value': 'distributed'}, {
                                'label': 'Grouped', 'value': 'grouped'}],
                            value='distributed'
                        )
                    ], className='form-group'),
                    html.Hr(),
                    html.Div([
                        html.Div([
                            dcc.Markdown('**Color by:**'),
                            dcc.Dropdown(
                                id='color_dropdown_map',
                                options=[{'label': value, 'value': key}
                                         for key, value in columns.items()],
                                value='active_product'
                            )
                        ], className='form-group'),
                    ], id='type_distributed_option'),
                    html.Div([
                        html.Div([
                            dcc.Markdown('**Group By:**'),
                            dcc.Dropdown(
                                id='group_dropdown_map',
                                options=[
                                    {'label': 'City', 'value': 'City'}],
                                value='City'
                            )
                        ], className='form-group'),
                        html.Div([
                            dcc.Markdown('**Size by:**'),
                            dcc.Dropdown(
                                id='size_dropdown_map',
                                options=[{'label': 'Total ' + value, 'value': key}
                                         for key, value in columns.items()],
                                value='active_product'
                            )
                        ], className='form-group'),
                    ], id='type_grouped_option'),
                    html.Div([
                        dcc.Markdown('**Outlier:**'),
                        dcc.RadioItems(
                            id='outlier_radio_map',
                            labelStyle={'margin-right': '0.5rem'},
                            options=[
                                {'label': 'Without Outlier', 'value': 0},
                                {'label': 'With Outlier', 'value': 1},
                            ],
                            value=0
                        )
                    ], className='form-group'),
                    html.Div([
                        dcc.Markdown('**Opacity:**'),
                        dcc.Slider(
                            id='opacity_slider_map',
                            min=0,
                            max=1,
                            value=0.4,
                            marks={0: '0', 1: '1'},
                            step=0.1
                        )
                    ], className='form-group')
                ], className='card-body')
            ], className='card')
        ], className='col-lg-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Maps', className='card-title'),
                    # TODO: buat interactive map per date
                    # html.Div([
                    #     dcc.DatePickerSingle(
                    #         id='date_picker_map',
                    #         min_date_allowed='2018-12-21',
                    #         max_date_allowed='2019-02-02',
                    #         date='2019-01-03'
                    #     )
                    # ], className='card-options')
                ], className='card-header'),
                html.Div([
                    dcc.Graph(id='graph_map'),
                    dcc.RangeSlider(
                        id='data_range_slider_map',
                        step=1,
                    )
                ], className='card-body', style={'padding-top': '0'})
            ], className='card')
        ], className='col-lg-9'),
    ], className='row row-deck')
], className='container')


@app.callback(
    Output('type_distributed_option', 'style'),
    [Input('type_dropdown_map', 'value')]
)
def update_type_distributed_option_style(type):
    if type == 'distributed':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('type_grouped_option', 'style'),
    [Input('type_dropdown_map', 'value')]
)
def update_type_grouped_option_style(type):
    if type == 'grouped':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('outlier_radio_map', 'value'),
    [
        Input('type_dropdown_map', 'value'),
        Input('color_dropdown_map', 'value'),
        Input('size_dropdown_map', 'value'),
    ]
)
def update_outlier_radio_map_value(type, color, size):
    return 0


@app.callback(
    Output('data_range_slider_map', 'min'),
    [
        Input('type_dropdown_map', 'value'),
        Input('color_dropdown_map', 'value'),
        Input('size_dropdown_map', 'value'),
        Input('outlier_radio_map', 'value')
    ]
)
def update_data_range_slider_map_min(type, color, size, with_outlier):
    if type == 'distributed':
        return df[color].min() if with_outlier else remove_outlier(df, color).min()
    else:
        return df[size].min() if with_outlier else remove_outlier(df, size).min()


@app.callback(
    Output('data_range_slider_map', 'max'),
    [
        Input('type_dropdown_map', 'value'),
        Input('color_dropdown_map', 'value'),
        Input('size_dropdown_map', 'value'),
        Input('outlier_radio_map', 'value')
    ]
)
def update_data_range_slider_map_max(type, color, size, with_outlier):
    if type == 'distributed':
        return df[color].max() if with_outlier else remove_outlier(df, color).max()
    else:
        return df[size].max() if with_outlier else remove_outlier(df, size).max()


@app.callback(
    Output('data_range_slider_map', 'value'),
    [
        Input('data_range_slider_map', 'min'),
        Input('data_range_slider_map', 'max')
    ]
)
def update_data_range_slider_map_value(min_value, max_value):
    return [min_value, max_value]


@app.callback(
    Output('data_range_slider_map', 'marks'),
    [
        Input('data_range_slider_map', 'min'),
        Input('data_range_slider_map', 'max')
    ]
)
def update_data_range_slider_map_marks(min_value, max_value):
    return {min_value: {'label': str(min_value)}, max_value: {'label': str(max_value)}}


@app.callback(
    Output('graph_map', 'figure'),
    [
        Input('type_dropdown_map', 'value'),
        Input('group_dropdown_map', 'value'),
        Input('color_dropdown_map', 'value'),
        Input('size_dropdown_map', 'value'),
        Input('opacity_slider_map', 'value'),
        Input('data_range_slider_map', 'value')
    ]
)
def update_graph_map(type, group, color, size, opacity, range_value):
    if type == 'distributed':
        dff = df[(df[color] >= range_value[0]) & (df[color] <= range_value[1])]
        title = 'ECommerce Distribution in Indonesia by {}'.format(
            columns[color])
        data = [
            go.Scattermapbox(
                lat=list(dff['address_lat']),
                lon=list(dff['address_lng']),
                mode='markers',
                marker=dict(
                    size=5,
                    opacity=opacity,
                    color=dff[color],
                    colorscale='RdBu',
                    showscale=True,
                ),
                text=dff[color].apply(
                    lambda x: '{}: {}'.format(columns[color], x)),
            )
        ]
    else:
        # TODO: fix second {} value for all available group
        # use pd.DataFrame() because one column treated as Series
        dff = pd.DataFrame(df.groupby(
            ['city', 'city_lat', 'city_lng'])[size].sum())
        dff.reset_index(level=['city', 'city_lat', 'city_lng'], inplace=True)
        dff = dff[(dff[size] >= range_value[0]) & (dff[size] <= range_value[1])]
        title = 'Total {} Grouped by {}'.format(columns[size], 'City')
        data = [
            go.Scattermapbox(
                lat=list(dff['city_lat']),
                lon=list(dff['city_lng']),
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=dff[size],
                    sizemode='area',
                    sizeref=3. * max(dff[size]) / (20. ** 2),
                    sizemin=2,
                    opacity=opacity,
                ),
                text=dff[['city', size]].apply(
                    lambda x: '{}: {}'.format(x[0], x[1]), axis=1),
            )
        ]

    figure = {
        'data': data,
        'layout': {
            'title': title,
            'width': 800,
            'height': 550,
            'hovermode': 'closest',
            # 'mapbox': {
            #     'accesstoken': mapblox_token,
            #     'bearing': 0,
            #     'center': {
            #         'lat': -2.600029,
            #         'lon': 118.015776,
            #     },
            #     'pitch': 0,
            #     'zoom': 3
            # }
            'mapbox': go.layout.Mapbox(
                accesstoken=mapblox_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=-2.600029,
                    lon=118.015776,
                ),
                pitch=0,
                zoom=3
            )
        }
    }
    return figure
