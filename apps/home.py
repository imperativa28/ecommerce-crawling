import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

from dash.dependencies import Input, Output
from app import app

from src.data import df, area_summary, summary


col_names = ['Column', 'Non Null Data', 'Mean',
             'Std', 'Min', '25%', '50%', '75%', 'Max']
layout = html.Div([
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
                             {'name': 'Area', 'id': 'city'},
                             {'name': 'Active Products',
                              'id': 'active_product'},
                             {'name': 'Products Sold',
                              'id': 'product_sold'},
                             {'name': 'Number of Transactions',
                              'id': 'total_tx'},
                             {'name': 'Number of Physical Stores',
                              'id': 'num_store'}
                         ],
                         style_table={'overflowX': 'scroll'},
                         style_cell={'padding': '5px'},
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': 'city'},
                                 'textAlign': 'left',
                                 'fontWeight': 'bold',
                             }
                         ],
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
        ], className='col-12'),
        # end of area summary table and graph

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
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': 'index'},
                                 'textAlign': 'left',
                                 'fontWeight': 'bold',
                             }
                         ],
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
    ], className='row row-cards')
], className='container')


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
                            'x': dff['city'],
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
        ], className='col-lg-3 col-md-6 col-sm-12')
        for name, id in [('Active Products', 'active_product'), ('Products Sold', 'product_sold'), ('Number of Transactions', 'total_tx'), ('Number of Physical Stores', 'num_store')]], className='row')
