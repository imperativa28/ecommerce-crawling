import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
import math
import numpy as np

from dash.dependencies import Input, Output

# Prepare data
columns = {
    'active_product': 'Active Products',
    'product_sold': 'Products Sold',
    'num_store': 'Number of Physical Stores'
}
df = pd.read_csv('tokopedia.csv', header=0, sep=';', index_col=0)
summary = df[list(columns.keys())].describe().transpose().reset_index(level=0)
summary['index'] = [columns[key] for key in summary['index']]

area_summary = df.groupby('area')[['active_product', 'product_sold']].sum()
area_summary['count'] = list(df.groupby('area')['num_store'].count())
area_summary.reset_index(level='area', inplace=True)

word_counts = pd.read_csv('word_counts.csv', index_col=0)

# Prepare data instagram
mapblox_token = 'pk.eyJ1IjoiaW1wZXJhdGl2YTI4IiwiYSI6ImNqc2ZvcDJzaDFqZTg0Nm9heWFtMXd2NW0ifQ.4z5BuZSALFx7vM8alGvXzw'
columns_ig = {
    'post_number': 'Number of Posts',
    'media_count': 'Media Count',
    'follower_count': 'Follower Count',
    'following_count': 'Following Count'
}
df_ig = pd.read_csv('instagram.csv', header=0, sep=';')

# testing
# df_ig = pd.read_csv('instagram_all.csv', header=0, sep=';')
# df_ig['taken_at_timestamp'] = pd.to_datetime(df_ig['taken_at_timestamp'], utc=True, unit='s')
# df_ig['year'] = pd.DatetimeIndex(df_ig['taken_at_timestamp']).year
# df_ig['month'] = pd.DatetimeIndex(df_ig['taken_at_timestamp']).month
# df_ig['day'] = pd.DatetimeIndex(df_ig['taken_at_timestamp']).day
# df_ig['hour'] = pd.DatetimeIndex(df_ig['taken_at_timestamp']).hour
# df.groupby(['lng', 'lat', 'username'])['location_id'].count()
# df_ig['taken_at_timestamp'].max().strftime('%Y-%m-%d')

# Prepare app
external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True
app.title = 'ECommerce'


app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.A([
                    html.I(className='fab fa-flipboard ',
                           style={'margin-right': '10px'}),
                    'Dashboard Crawler ECommerce'
                ], className='header-brand')
            ], className='d-flex')
        ], className='container')
    ], className='header py-4'),
    html.Div([
        html.Div([
            html.Div([
                dcc.Tabs(id='tabs', value='tab_home', parent_className='col-lg order-lg-first', className='nav nav-tabs border-0 flex-column flex-lg-row',
                         children=[
                             dcc.Tab(label='Home', value='tab_home',
                                     className='tab_class', selected_className='tab_selected_class'),
                             dcc.Tab(label='Histogram', value='tab_histogram',
                                     className='tab_class', selected_className='tab_selected_class'),
                             dcc.Tab(label='Scatter Plot', value='tab_scatterplot',
                                     className='tab_class', selected_className='tab_selected_class'),
                             dcc.Tab(label='Text Analysis', value='tab_text_analysis',
                                     className='tab_class', selected_className='tab_selected_class'),
                             dcc.Tab(label='Map', value='tab_map',
                                     className='tab_class', selected_className='tab_selected_class'),
                         ])
            ], className='row align-item-center')
        ], className='container')
    ], className='header d-lg-flex p-0'),
    html.Div(className='my-3 my-md-5'),
    html.Div(id='tabs_content')
])


@app.callback(Output('tabs_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab_home':
        col_names = ['Column', 'Non Null Data', 'Mean',
                     'Std', 'Min', '25%', '50%', '75%', 'Max']
        tab_home_content = html.Div([
            html.Div([
                # info cards
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span([
                                html.I(className='fa fa-shopping-bag')
                            ], className='stamp stamp-md bg-azure mr-3'),
                            html.Div([
                                html.H4([
                                    len(df)
                                ], className='m-0'),
                                html.Small('Online Shops Crawled',
                                           className='text-muted')
                            ]),
                        ], className='d-flex align-item-center')
                    ], className='card p-3')
                ], className='col-lg-3 col-md-6 col-sm-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span([
                                html.I(className='fa fa-shopping-cart')
                            ], className='stamp stamp-md bg-teal mr-3'),
                            html.Div([
                                html.H4([
                                    df['active_product'].sum(),
                                ], className='m-0'),
                                html.Small('Active Products',
                                           className='text-muted')
                            ]),
                        ], className='d-flex align-item-center')
                    ], className='card p-3')
                ], className='col-lg-3 col-md-6 col-sm-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span([
                                html.I(className='fa fa-cart-plus')
                            ], className='stamp stamp-md bg-cyan mr-3'),
                            html.Div([
                                html.H4([
                                    df['product_sold'].sum(),
                                ], className='m-0'),
                                html.Small('Products Sold',
                                           className='text-muted')
                            ]),
                        ], className='d-flex align-item-center')
                    ], className='card p-3')
                ], className='col-lg-3 col-md-6 col-sm-12'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Span([
                                html.I(className='fa fa-globe-asia')
                            ], className='stamp stamp-md bg-indigo mr-3'),
                            html.Div([
                                html.H4([
                                    len(area_summary),
                                ], className='m-0'),
                                html.Small('Areas Covered',
                                           className='text-muted')
                            ]),
                        ], className='d-flex align-item-center')
                    ], className='card p-3')
                ], className='col-lg-3 col-md-6 col-sm-12'),
                # end of info cards

                # summary table
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Overall Data Description', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            dash_table.DataTable(
                                id='summary_table',
                                columns=[{'name': name, 'id': id}
                                         for name, id in list(zip(col_names, summary.columns))],
                                data=summary.to_dict('rows'),
                                style_table={'overflowX': 'scroll'},
                                style_cell={'padding': '5px'},
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold',
                                    'textAlign': 'center'
                                },
                                sorting=True,
                            )
                        ], className='card-body')
                    ], className='card')
                ], className='col-12'),
                # end of summary table

                # area summary table and graph
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Per Area Data Description', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            html.Div([

                            ], id='area_summary_graph'),
                            dash_table.DataTable(
                                id='area_summary_table',
                                columns=[
                                    {'name': 'Area', 'id': 'area'},
                                    {'name': 'Active Products',
                                        'id': 'active_product'},
                                    {'name': 'Products Sold',
                                        'id': 'product_sold'},
                                    {'name': 'Count',
                                        'id': 'count'},
                                ],
                                style_table={'overflowX': 'scroll'},
                                style_cell={'padding': '5px'},
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold',
                                    'textAlign': 'center'
                                },
                                pagination_mode='be',
                                pagination_settings={
                                    'current_page': 0,
                                    'page_size': 10
                                },
                                sorting='be',
                                sorting_type='single',
                                sorting_settings=[],
                                filtering='be',
                                filtering_settings=''
                            ),
                            html.Hr(),
                            dcc.Markdown(
                                '''
A quick note on filtering. **Dash** have defined their own syntax for performing filtering operations. Here are some examples for this particular dataset:
* Enter `eq Jakarta` in `Area` column (**with spaces**)
* Enter `> 1000` in `Active Products` column (**with spaces**)
* Enter `< 10000` in `Product Solds` column (**with spaces**)
                                '''
                            )
                        ], className='card-body')
                    ], className='card')
                ], className='col-12')
                # end of area summary table and graph
            ], className='row row-cards')
        ], className='container')
        return tab_home_content

    elif tab == 'tab_histogram':
        tab_histogram_content = html.Div([
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
                                    id='outlier_histogram',
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
        return tab_histogram_content

    elif tab == 'tab_scatterplot':
        tab_scatterplot_content = html.Div([
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
                                    id='outlier_scatterplot',
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
        return tab_scatterplot_content

    elif tab == 'tab_text_analysis':
        tab_text_analysis_content = html.Div([
            html.Div([
                # word cloud
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Word Cloud', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            html.A([
                                html.Img(src='assets/image/wordcloudclean.png',
                                         height='350px', width='350px', className='mx-auto d-block')
                            ], className='mb-3')
                        ], className='card-body')
                    ], className='card')
                ], className='col-lg-4'),

                # word counts
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Word Frequencies', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            html.Div([

                            ], id='graph_word_counts'),
                            dash_table.DataTable(
                                id='table_word_counts',
                                columns=[
                                    {'name': 'Word', 'id': 'word'},
                                    {'name': 'Frequencies', 'id': 'frequencies'},
                                ],
                                style_table={'overflowX': 'scroll'},
                                style_cell={'padding': '5px'},
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold',
                                    'textAlign': 'center'
                                },
                                pagination_mode='be',
                                pagination_settings={
                                    'current_page': 0,
                                    'page_size': 20
                                },
                                sorting='be',
                                sorting_type='single',
                                sorting_settings=[],
                                filtering='be',
                                filtering_settings='',
                            ),
                            html.Hr(),
                            dcc.Markdown(
                                '''
A quick note on filtering. **Dash** have defined their own syntax for performing filtering operations. Here are some examples for this particular dataset:
* Enter `eq shop` in `Word` column (**with spaces**)
* Enter `> 1000` in `Frequencies` column (**with spaces**)
                                '''
                            )
                        ], className='card-body')
                    ], className='card')
                ], className='col-lg-8')
            ], className='row row-cards')
        ], className='container')
        return tab_text_analysis_content

    elif tab == 'tab_map':
        tab_map_content = html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Settings', className='card-title')
                        ], className='card-header'),
                        html.Div([
                            html.Div([
                                dcc.Markdown('**Color by:**'),
                                dcc.Dropdown(
                                    id='column_dropdown_map',
                                    options=[{'label': value, 'value': key}
                                             for key, value in columns_ig.items()],
                                    value='post_number'
                                )
                            ], className='form-group'),
                            html.Div([
                                dcc.Markdown('**Outlier:**'),
                                dcc.RadioItems(
                                    id='outlier_map',
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
                            html.Div([
                                dcc.DatePickerSingle(
                                    id='date_picker_map',
                                    min_date_allowed='2018-12-21',
                                    max_date_allowed='2019-02-02',
                                    date='2019-01-03'
                                )
                            ], className='card-options')
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
        return tab_map_content


# helper function
def remove_outlier(df, column):
    return df[((df[column] - df[column].mean()) / df[column].std()).abs() < 3][column]


# tab_histogram callback
@app.callback(
    Output('outlier_histogram', 'value'),
    [Input('column_dropdown_histogram', 'value')]
)
def update_outlier_histogram_value(column):
    return 0


@app.callback(
    Output('data_range_slider_histogram', 'min'),
    [
        Input('column_dropdown_histogram', 'value'),
        Input('outlier_histogram', 'value')
    ]
)
def update_data_range_slider_histogram_min(column, with_outlier):
    return df[column].min() if with_outlier else remove_outlier(df, column).min()


@app.callback(
    Output('data_range_slider_histogram', 'max'),
    [
        Input('column_dropdown_histogram', 'value'),
        Input('outlier_histogram', 'value')
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


# tab_scatterplot callback
@app.callback(
    Output('graph_scatterplot', 'figure'),
    [
        Input('x_axis_dropdown_scatterplot', 'value'),
        Input('y_axis_dropdown_scatterplot', 'value'),
        Input('outlier_scatterplot', 'value'),
    ]
)
def update_graph_scatterplot(x_axis, y_axis, with_outlier):
    figure = {
        'data': [
            go.Scattergl(
                x=df[x_axis] if with_outlier else remove_outlier(df, x_axis),
                y=df[y_axis] if with_outlier else remove_outlier(df, y_axis),
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


# tab_home callback
@app.callback(
    Output('area_summary_table', 'data'),
    [
        Input('area_summary_table', 'pagination_settings'),
        Input('area_summary_table', 'sorting_settings'),
        Input('area_summary_table', 'filtering_settings'),
    ]
)
def update_area_summary_table(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = area_summary
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0].replace('"', '')
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0].replace('"', '')
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0].replace('"', '')
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    if len(sorting_settings):
        dff.sort_values(
            sorting_settings[0]['column_id'],
            ascending=sorting_settings[0]['direction'] == 'asc',
            inplace=True
        )

    return dff.iloc[
        pagination_settings['current_page'] * pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1) *
        pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(
    Output('area_summary_graph', 'children'),
    [Input('area_summary_table', 'data')])
def update_area_summary_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div([
        html.Div([
            dcc.Graph(
                id='area_summary_graph_{}'.format(name),
                figure={
                    'data': [
                        {
                            'x': dff['area'],
                            'y': dff[id] if id in dff else [],
                            'type': 'bar',
                        }
                    ],
                    'layout': {
                        'title': 'Bar Plot of {}'.format(name),
                        'xaxis': {
                            'title': 'Area',
                            'automargin': True
                        },
                        'yaxis': {
                            'title': name,
                            'automargin': True
                        },
                        'height': 300,
                        'margin': {'t': 30, 'l': 15, 'r': 15, 'b': 30},
                    },
                },
            )
        ], className='col-lg-4 col-sm-12')
        for name, id in [('Active Products', 'active_product'), ('Products Sold', 'product_sold'), ('Count', 'count')]], className='row')


# tab_text_analysis callback
@app.callback(
    Output('table_word_counts', 'data'),
    [
        Input('table_word_counts', 'pagination_settings'),
        Input('table_word_counts', 'sorting_settings'),
        Input('table_word_counts', 'filtering_settings'),
    ]
)
def update_table_word_counts(pagination_settings, sorting_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = word_counts
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0].replace('"', '')
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0].replace('"', '')
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0].replace('"', '')
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    if len(sorting_settings):
        dff.sort_values(
            sorting_settings[0]['column_id'],
            ascending=sorting_settings[0]['direction'] == 'asc',
            inplace=True
        )

    return dff.iloc[
        pagination_settings['current_page'] * pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1) *
        pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(
    Output('graph_word_counts', 'children'),
    [Input('table_word_counts', 'data')])
def update_graph_word_counts(rows):
    dff = pd.DataFrame(rows)
    return html.Div([
        html.Div([
            dcc.Graph(
                figure={
                    'data': [
                        {
                            'x': dff['word'],
                            'y': dff['frequencies'],
                            'type': 'bar',
                        }
                    ],
                    'layout': {
                        'title': 'Bar Plot of Word Frequencies',
                        'xaxis': {
                            'title': 'Word',
                            'automargin': True
                        },
                        'yaxis': {
                            'title': 'Frequencies',
                            'automargin': True
                        },
                        'height': 300,
                        'margin': {'t': 30, 'l': 15, 'r': 15, 'b': 30},
                    },
                },
            )
        ])
    ], className='row')


# tab_map callback
@app.callback(
    Output('outlier_map', 'value'),
    [Input('column_dropdown_map', 'value')]
)
def update_outlier_map_value(column):
    return 0


@app.callback(
    Output('data_range_slider_map', 'min'),
    [
        Input('column_dropdown_map', 'value'),
        Input('outlier_map', 'value')
    ]
)
def update_data_range_slider_map_min(column, with_outlier):
    return df_ig[column].min() if with_outlier else remove_outlier(df_ig, column).min()


@app.callback(
    Output('data_range_slider_map', 'max'),
    [
        Input('column_dropdown_map', 'value'),
        Input('outlier_map', 'value')
    ]
)
def update_data_range_slider_map_max(column, with_outlier):
    return df_ig[column].max() if with_outlier else remove_outlier(df_ig, column).max()


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
        Input('column_dropdown_map', 'value'),
        Input('opacity_slider_map', 'value'),
        Input('data_range_slider_map', 'value')
    ]
)
def update_graph_map(column, opacity, range_value):
    dff_ig = df_ig[(df_ig[column] >= range_value[0]) &
                    (df_ig[column] <= range_value[1])]
    figure = {
        'data': [
            go.Scattermapbox(
                lat=list(dff_ig['lat']),
                lon=list(dff_ig['lng']),
                mode='markers',
                marker=dict(
                    # size=dff_ig['following_count'],
                    # sizemode='area',
                    # sizeref = 2. * max(dff_ig['following_count']) / (30. ** 2),
                    # sizemin=5,
                    size=5,
                    opacity=opacity,
                    color=dff_ig[column],
                    colorscale='RdBu',
                    showscale=True,
                ),
                text=dff_ig['name'],
            )
        ],
        'layout': {
            'title': 'Map of Instagram #olshop Posts by {}'.format(columns_ig[column]),
            'width': 800,
            'height': 550,
            'hovermode': 'closest',
            'mapbox': {
                'accesstoken': mapblox_token,
                'bearing': 0,
                'center': {
                    'lat': -2.600029,
                    'lon': 118.015776,
                },
                'pitch': 0,
                'zoom': 3
            }
        }
    }
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
