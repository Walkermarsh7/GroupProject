
# Packages
import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import requests, base64, time

dash.register_page(__name__, path="/page3", name="Songs by Artist")

# Spotify Setup
client_id = "525eeb52425e485ab2635d4fd17a09bb"
client_secret = "1ab191a21a554e90b3f1cde668d9c7c4"

token_data = {"access_token": None, "expiration": 0}

def get_auth_headers():
    now = time.time()
    if not token_data["access_token"] or now >= token_data["expiration"]:
        auth_str = f"{client_id}:{client_secret}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        resp = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {b64_auth}"},
            data={"grant_type": "client_credentials"},
        )
        data = resp.json()
        token_data["access_token"] = data["access_token"]
        token_data["expiration"] = now + data["expires_in"] - 30
    return {"Authorization": f"Bearer {token_data['access_token']}"}

def find_artist(name):
    resp = requests.get(
        "https://api.spotify.com/v1/search",
        headers=get_auth_headers(),
        params={"q": name, "type": "artist", "limit": 1},
    )
    items = resp.json().get("artists", {}).get("items", [])
    return items[0] if items else None

def artist_top_tracks(artist_id, market="US"):
    resp = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        headers=get_auth_headers(),
        params={"market": market},
    )
    return resp.json().get("tracks", [])[:10]

layout = html.Div([
    html.H2("Songs by Artist"),
    dcc.Input(id="artist", type="text", placeholder="Enter an artist"),
    html.Button("Search", id="go", n_clicks=0),
    html.Div(id="status"),
    dcc.Graph(id="chart"),
    html.Div(id="list"),
])

# Layout 

@dash.callback(
    Output("chart", "figure"),
    Output("list", "children"),
    Output("status", "children"),
    Input("go", "n_clicks"),
    State("artist", "value"),
    prevent_initial_call=True,
)
def show_top_tracks(_, artist_name):
    if not artist_name:
        return go.Figure(), "", "Please enter an artist name."
    artist = find_artist(artist_name)
    if not artist:
        return go.Figure(), "", "Artist not found."

    tracks = artist_top_tracks(artist["id"])
    if not tracks:
        return go.Figure(), "", "No top tracks found."

    names = [t["name"] for t in tracks]
    pops  = [t["popularity"] for t in tracks]

    fig = go.Figure(go.Bar(x=names, y=pops))
    fig.update_layout(title=f"Top Tracks — {artist['name']}")

    links = [html.Li(html.A(t["name"], href=t["external_urls"]["spotify"], target="_blank")) for t in tracks]
    return fig, html.Ul(links), f"Showing {artist['name']}'s top tracks."


