import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import home, map, histogram, scatterplot, text_analysis
from dash.dependencies import Input, Output

tabs = ['home', 'map', 'histogram', 'scatterplot', 'text_analysis']

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Div([
                dcc.Link([
                    html.I(className='fab fa-flipboard',
                           style={'margin-right': '10px'}),
                    'Dashboard Crawler ECommerce'
                ], className='header-brand', href='/'),
                html.A([
                    html.Span(className='header-toggler-icon')
                ], className='header-toggler d-lg-none ml-3 ml-lg-0', href='#', **{'data-toggle': 'collapse', 'data-target': 'header_menu_collapse'})
            ], className='d-flex')
        ], className='container')
    ], className='header py-4'),
    html.Div([
        html.Div([
            html.Div([
                html.Div(id='tab_content', className='col-lg order-lg-first')
            ], className='row align-item-center')
        ], className='container')
    ], className='header collapse d-lg-flex p-0'),
    html.Div(className='my-3 my-md-5'),
    html.Div(id='page_content')
])


@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home' or pathname == '/':
        return home.layout
    elif pathname == '/apps/map':
        return map.layout
    elif pathname == '/apps/histogram':
        return histogram.layout
    elif pathname == '/apps/scatterplot':
        return scatterplot.layout
    elif pathname == '/apps/text_analysis':
        return text_analysis.layout
    else:
        # TODO: Create 404 page
        return '404'

@app.callback(Output('tab_content', 'children'),
              [Input('url', 'pathname')])
def display_tab(pathname):
    tab = html.Ul([
        html.Li([
            dcc.Link([
                html.I([
                ], className='fe fe-home'),
                'Home'
            ], className='nav-link active' if pathname == '/apps/home' or pathname == '/' else 'nav-link', href='/apps/home', id='tab_home')
        ], className='nav-item'),
        html.Li([
            dcc.Link([
                html.I([
                ], className='fe fe-map'),
                'Map'
            ], className='nav-link active' if pathname == '/apps/map' else 'nav-link', href='/apps/map', id='tab_map')
        ], className='nav-item'),
        html.Li([
            dcc.Link([
                html.I([
                ], className='fe fe-bar-chart-2'),
                'Histogram'
            ], className='nav-link active' if pathname == '/apps/histogram' else 'nav-link', href='/apps/histogram', id='tab_histogram')
        ], className='nav-item'),
        html.Li([
            dcc.Link([
                html.I([
                ], className='fe fe-more-vertical'),
                'Scatter Plot'
            ], className='nav-link active' if pathname == '/apps/scatterplot' else 'nav-link', href='/apps/scatterplot', id='tab_scatterplot')
        ], className='nav-item'),
        html.Li([
            dcc.Link([
                html.I([
                ], className='fe fe-clipboard'),
                'Text Analysis'
            ], className='nav-link active' if pathname == '/apps/text_analysis' else 'nav-link', href='/apps/text_analysis', id='tab_text_analysis')
        ], className='nav-item')
    ], className='nav nav-tabs border-0 flex-column flex-lg-row')
    return tab


if __name__ == '__main__':
    app.run_server(debug=True)
