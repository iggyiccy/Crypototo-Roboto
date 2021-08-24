# -*- coding: utf-8 -*-

# Run this app with `python App.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)

#------------------------------------------------------ Styling ------------------------------------------------------

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "3rem",
    "padding": "2rem 1rem",
}


#------------------------------------------------------ Define Components ------------------------------------------------------

# define sidebar variables
sidebar = html.Div(
    [
        html.H2("Currency Convertor", className="display-4"),
        html.Hr(),
        html.P(
            "FinTech Boot Camp Project 2 Presentation", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("🌍 Local Price", href="/", active="exact"),
                dbc.NavLink("💹 Analysis", href="/page-1", active="exact"),
                dbc.NavLink("💱 Converter", href="/page-2", active="exact"),
                dbc.NavLink("⏰ Crypto Updates", href="/page-3", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# define content variables
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

#------------------------------------------------------ APP ------------------------------------------------------ 

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

#------------------------------------------------------ Callbacks ------------------------------------------------------

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        children = [
                html.H1('🌍 Cryptocurrency Price in Your Local Currency',
                        style={'textAlign':'center'}),
        ]

        return children
    elif pathname == "/page-1":
        children = [
                html.H1('💹 Major Cryptocurrency Trend and Analysis',
                        style={'textAlign':'center'}),
        ]

        return children
    elif pathname == "/page-2":
        children = [
                html.H1('💱 Cryptocurrency Converter',
                        style={'textAlign':'center'}),
                ]
        return children
    elif pathname == "/page-3":
        children = [
                html.H1('⏰ Cryptocurrencies Status Updates',
                        style={'textAlign':'center'}),
            ]
        return children
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
    )
if __name__=='__main__':
    app.run_server(debug=True, port=3000)