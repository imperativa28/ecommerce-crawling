import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

from dash.dependencies import Input, Output
from app import app

from src.data import word_counts

layout = html.Div([
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
                        html.Img(src=app.get_asset_url('images/wordcloudclean.png'),
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