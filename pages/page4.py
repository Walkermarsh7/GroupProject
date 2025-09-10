# Used AI to help us set up the Spotify authentication flow, including writing the code for caching and refreshing tokens so that requests would not fail. 
# AI guided the creation of the search functions that locate the two songs entered by the user and return their popularity scores. 
# Suggested how to structure the callback so that when both songs are entered, the results display together instead of separately. 
# Also provided the code for building the comparison bar chart, ensuring the popularity values were shown side by side with labels. 
# It helped us add layout styling so that the chart and results look clean and consistent with the rest of the dashboard. 
# Also assisted in writing error handling so that the page displays clear messages when invalid input is given, when a song is not found, or when Spotify returns incomplete data.


# pages/page4.py
import time, base64, requests
import pandas as pd
import plotly.express as px
from dash import html, dcc, register_page, callback, Input, Output, State


register_page(
    __name__,
    path="/page4",
    name="Compare Songs",
    title="Compare Songs Popularity"
)


SPOTIFY_CLIENT_ID = "525eeb52425e485ab2635d4fd17a09bb"
SPOTIFY_CLIENT_SECRET = "1ab191a21a554e90b3f1cde668d9c7c4"


_token = {"access_token": None, "exp": 0}

def _auth_headers():
    now = time.time()
    if not _token["access_token"] or now >= _token["exp"]:
        cid = (SPOTIFY_CLIENT_ID or "").strip()
        csec = (SPOTIFY_CLIENT_SECRET or "").strip()
        if not cid or not csec:
            raise RuntimeError("Set SPOTIFY_CLIENT_ID/SECRET in page4.py")
        b64 = base64.b64encode(f"{cid}:{csec}".encode()).decode()
        r = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {b64}"},
            data={"grant_type": "client_credentials"},
            timeout=10,
        )
        r.raise_for_status()
        j = r.json()
        _token["access_token"] = j["access_token"]
        _token["exp"] = time.time() + int(j.get("expires_in", 3600)) - 30
    return {"Authorization": f"Bearer {_token['access_token']}"}

def _search_track(title: str, limit=1, market="US"):
    if not title:
        return None
    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers=_auth_headers(),
        params={"q": title.strip(), "type": "track", "limit": limit, "market": market},
        timeout=10,
    )
    r.raise_for_status()
    items = r.json().get("tracks", {}).get("items", [])
    return items[0] if items else None


layout = html.Div(children=[
    html.H2("Which Song Is More Popular Right Now?"),
    html.Div([
        dcc.Input(id="song-a", type="text", placeholder="Song A (e.g., Billie Jean)", style={"marginRight": "8px"}),
        dcc.Input(id="song-b", type="text", placeholder="Song B (e.g., Thunderstruck)", style={"marginRight": "8px"}),
        html.Button("Compare", id="song-go", n_clicks=0),
    ], style={"marginBottom": "10px"}),

    html.Div(id="song-status", style={"marginBottom": "6px"}),
    dcc.Graph(id="song-graph"),
])


@callback(
    Output("song-graph", "figure"),
    Output("song-status", "children"),
    Input("song-go", "n_clicks"),
    State("song-a", "value"),
    State("song-b", "value"),
    prevent_initial_call=True,
)
def compare_songs(_, a_title, b_title):
    fig = px.bar(
        pd.DataFrame({"Song": [], "Popularity": []}),
        x="Song", y="Popularity",
        title="Enter two song titles and click Compare",
        color_discrete_sequence=["green"]  # ensure green bars even when empty
    )

    if not a_title or not b_title:
        return fig, "Please enter both song titles."

    try:
        a = _search_track(a_title)
        b = _search_track(b_title)

        if not a and not b:
            return fig, f"No results for '{a_title}' or '{b_title}'."
        if not a:
            return fig, f"No results for '{a_title}'."
        if not b:
            return fig, f"No results for '{b_title}'."

        a_label = f"{a['name']} — {a['artists'][0]['name'] if a.get('artists') else ''}".strip(" —")
        b_label = f"{b['name']} — {b['artists'][0]['name'] if b.get('artists') else ''}".strip(" —")

        data = pd.DataFrame({
            "Song": [a_label, b_label],
            "Popularity": [a.get("popularity", 0), b.get("popularity", 0)]
        })

        fig = px.bar(
            data,
            x="Song",
            y="Popularity",
            title="Spotify Popularity (0–100)",
            labels={"Song": "Song", "Popularity": "Popularity (0–100)"},
            range_y=[0, 100],
            color_discrete_sequence=["green"]  # ✅ force bars to be green
        )
        fig.update_layout(margin=dict(l=10, r=10, t=50, b=80), xaxis_tickangle=30)

        if data.loc[0, "Popularity"] > data.loc[1, "Popularity"]:
            status = f"“{a_label}” is more popular right now."
        elif data.loc[0, "Popularity"] < data.loc[1, "Popularity"]:
            status = f"“{b_label}” is more popular right now."
        else:
            status = "They are equally popular right now."

        return fig, status

    except requests.HTTPError as e:
        return fig, f"Spotify API error: {e}"
    except Exception as e:
        return fig, f"Error: {e}"

