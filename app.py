import dash
from dash import dcc, html, Dash, page_container
import dash_bootstrap_components as dbc

# -------- INITIALIZE APP --------
app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Spotify Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

# -------- TITLE --------
title = html.Div(
    "Spotify Dashboard",
    style={
        "textAlign": "center",
        "fontSize": "36px",
        "fontWeight": "bold",
        "color": "#1DB954",
        "padding": "30px 0",
        "backgroundColor": "#121212",
        "borderBottom": "2px solid #1DB954"
    }
)

# -------- NAVBAR --------
navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(dbc.NavLink("Top Artists", href="/", active="exact", style={"textAlign": "center"})),
                dbc.Col(dbc.NavLink("Popularity", href="/page4", active="exact", style={"textAlign": "center"})),
                dbc.Col(dbc.NavLink("Songs Around the World", href="/page2", active="exact", style={"textAlign": "center"})),
                dbc.Col(dbc.NavLink("Top songs by Artist", href="/page3", active="exact", style={"textAlign": "center"}))
            ],
            justify="evenly",  # ensures even spacing
            className="w-100"
        )
    ),
    color="#191414",
    dark=True,
    className="mb-4",
)

# -------- APP LAYOUT --------
app.layout = html.Div(
    style={"backgroundColor": "#121212", "color": "#1DB954", "minHeight": "100vh"},
    children=[
        title,
        navbar,
        html.Div(page_container, style={"padding": "20px"})
    ]
)

# -------- RUN SERVER --------
if __name__ == "__main__":
    app.run(debug=True)



"""
import dash
from dash import dcc, html, Dash, page_container
import dash_bootstrap_components as dbc

#initialize the app
app = Dash(__name__, use_pages = True, suppress_callback_exceptions=True, title = "Spotify Project")#tells Dash to scan the pages/folder for registered pages
server = app.server #for deployment

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavLink("Main", href="/", active="exact"),
            dbc.NavLink("Page 1", href="/page4", active="exact"),
            dbc.NavLink("Page 2", href="/page2", active="exact"),
            dbc.NavLink("Page 3", href="/page3", active="exact"),
        ],
    brand="Spotify Data Analysis"), 
    dash.page_container #this is where the page content will be rendered
])

if __name__ == "__main__":
    app.run(debug=True)
"""
