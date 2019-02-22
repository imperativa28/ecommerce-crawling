import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
import math

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
                             dcc.Tab(label='Maps', value='tab_maps',
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
        col_names = ['Column', 'Count', 'Mean',
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
                                    id='column_dropdown',
                                    options=[{'label': value, 'value': key}
                                             for key, value in columns.items()],
                                    value='active_product'
                                )
                            ], className='form-group'),
                            html.Div([
                                dcc.Markdown('**Bins:**'),
                                dcc.Input(
                                    id='bin_input',
                                    placeholder='Bins',
                                    type='number',
                                    value='20',
                                    min=1,
                                    max=100,
                                    step=1
                                )
                            ], className='form-group'),
                            html.Div([
                                dcc.Markdown('**Data Range:**'),
                                dcc.RangeSlider(
                                    id='data_range_slider',
                                    step=1,
                                )
                            ], className='form-group')
                        ], className='card-body')
                    ], className='card')
                ], className='col-lg-3'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Histogram', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            dcc.Graph(id='histogram')
                        ], className='card-body'),
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
                            html.H3('Settings', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            html.Div([
                                dcc.Markdown('**X Axis:**'),
                                dcc.Dropdown(
                                    id='x_axis_dropdown',
                                    options=[{'label': value, 'value': key}
                                             for key, value in columns.items()],
                                    value='active_product'
                                )
                            ], className='form-group'),
                            html.Div([
                                dcc.Markdown('**Y Axis:**'),
                                dcc.Dropdown(
                                    id='y_axis_dropdown',
                                    options=[{'label': value, 'value': key}
                                             for key, value in columns.items()],
                                    value='product_sold'
                                )
                            ], className='form-group')
                        ], className='card-body')
                    ], className='card')
                ], className='col-lg-3'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Scatter Plot', className='card-title',
                                    )
                        ], className='card-header'),
                        html.Div([
                            dcc.Graph(id='scatterplot')
                        ], className='card-body'),
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

                            ], id='word_counts_graph'),
                            dash_table.DataTable(
                                id='word_counts_table',
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


@app.callback(
    Output('data_range_slider', 'min'),
    [Input('column_dropdown', 'value')]
)
def update_data_range_slider_min(value):
    return df[value].min()


@app.callback(
    Output('data_range_slider', 'max'),
    [Input('column_dropdown', 'value')]
)
def update_data_range_slider_max(value):
    return df[value].max()


@app.callback(
    Output('data_range_slider', 'value'),
    [Input('data_range_slider', 'min'), Input('data_range_slider', 'max')]
)
def update_data_range_slider_value(min_value, max_value):
    return [min_value, max_value]


@app.callback(
    Output('data_range_slider', 'marks'),
    [Input('data_range_slider', 'min'), Input('data_range_slider', 'max')]
)
def update_data_range_slider_marks(min_value, max_value):
    return {min_value: {'label': str(min_value)}, max_value: {'label': str(max_value)}}


@app.callback(
    Output('histogram', 'figure'),
    [
        Input('column_dropdown', 'value'),
        Input('bin_input', 'value'),
        Input('data_range_slider', 'value')
    ]
)
def update_histogram(column, bin, range_value):
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


@app.callback(
    Output('scatterplot', 'figure'),
    [
        Input('x_axis_dropdown', 'value'),
        Input('y_axis_dropdown', 'value'),
    ]
)
def update_scatterplot(x_axis, y_axis):
    figure = {
        'data': [
            go.Scattergl(
                x=df[x_axis],
                y=df[y_axis],
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


@app.callback(
    Output('word_counts_table', 'data'),
    [
        Input('word_counts_table', 'pagination_settings'),
        Input('word_counts_table', 'sorting_settings'),
        Input('word_counts_table', 'filtering_settings'),
    ]
)
def update_word_counts_table(pagination_settings, sorting_settings, filtering_settings):
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
    Output('word_counts_graph', 'children'),
    [Input('word_counts_table', 'data')])
def update_word_counts_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div([
        html.Div([
            dcc.Graph(
                id='word_counts',
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


if __name__ == '__main__':
    app.run_server(debug=True)
