import dash
from dash import dcc, html, Input, Output
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- Register this file as Page 1 ---
dash.register_page(__name__, path="/", name="Page 1")

# -------- SPOTIFY AUTH  --------
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="4a1acd1c8e7949bbba7fec2eb1a9e181",
    client_secret="69e497dd3f834f02921904cf80b578e9"
))

# -------- HARD-CODED TOP ARTISTS PER GENRE --------
TOP_ARTISTS_BY_GENRE = {
    "pop": [
        "Lady Gaga", "Justin Bieber", "Ed Sheeran", "Billie Eilish", "Ariana Grande",
        "Taylor Swift", "Rosé", "Sabrina Carpenter", "Tate McRae", "Mariah Carey"
    ],
    "hip hop": [
        "Kendrick Lamar", "Drake", "Travis Scott", "J. Cole", "Cardi B",
        "Lil Baby", "Doja Cat", "Post Malone", "Megan Thee Stallion", "Kanye West"
    ],
    "r&b": [
        "SZA", "The Weeknd", "H.E.R.", "GIVĒON", "Bruno Mars",
        "Chris Brown", "Jhene Aiko", "Frank Ocean", "Alicia Keys", "Summer Walker"
    ],
    "country": [
        "Morgan Wallen", "Luke Combs", "Zach Bryan", "Chris Stapleton", "Lainey Wilson",
        "Cody Johnson", "Megan Moroney", "Ella Langley", "Zach Top", "Miranda Lambert"
    ],
    "rock": [
        "Coldplay", "Linkin Park", "Twenty One Pilots", "Imagine Dragons", "Foo Fighters",
        "Red Hot Chili Peppers", "The Killers", "Green Day", "Kings of Leon", "Paramore"
    ],
    "soul": [
        "Adele", "Sam Smith", "Leon Bridges", "Jazmine Sullivan", "John Legend",
        "Lizzo", "Alicia Keys", "Solange", "Anderson .Paak", "Corinne Bailey Rae"
    ],
    "jazz": [
        "Norah Jones", "Miles Davis", "Esperanza Spalding", "Diana Krall", "John Coltrane",
        "Herbie Hancock", "Chet Baker", "Louis Armstrong", "Ella Fitzgerald", "Bill Evans"
    ],
    "electronic": [
        "Calvin Harris", "David Guetta", "Kygo", "Martin Garrix", "Marshmello",
        "The Chainsmokers", "Zedd", "Avicii", "Diplo", "Deadmau5"
    ]
}

# Ordered genres: popular first
GENRES = ["pop", "hip hop", "r&b", "country", "rock", "soul", "jazz", "electronic"]

# ---- Layout for Page 1 (no Dash() here) ----
layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    children=[
        html.H1("🎵 Top Artists by Genre", style={"textAlign": "center"}),

        html.Div([
            html.Label("Select Genre:", style={"fontSize": "18px", "marginRight": "10px"}),
            dcc.Dropdown(
                id="genre-dropdown",
                options=[{"label": g.title(), "value": g} for g in GENRES],
                value="pop",
                style={"width": "400px", "margin": "auto"}
            )
        ], style={"textAlign": "center", "marginBottom": "30px"}),

        html.Div(id="artist-grid", style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "20px"
        })
    ]
)

# ---- Callback registered to global app ----
@dash.callback(
    Output("artist-grid", "children"),
    Input("genre-dropdown", "value")
)
def update_artists(genre):
    def get_artist_info(artist_name):
        result = sp.search(q=f'artist:{artist_name}', type="artist", limit=1)
        if not result["artists"]["items"]:
            return None
        artist = result["artists"]["items"][0]
        image_url = "https://via.placeholder.com/200"
        if artist.get("images") and len(artist["images"]) > 0:
            image_url = artist["images"][0]["url"]
        return {
            "name": artist["name"],
            "popularity": artist.get("popularity", 0),
            "genres": ", ".join(artist.get("genres", [])) if artist.get("genres") else "Unknown",
            "image": image_url
        }

    artist_names = TOP_ARTISTS_BY_GENRE.get(genre, [])
    artists = [get_artist_info(name) for name in artist_names]
    artists = [a for a in artists if a]

    # Sort by Spotify popularity descending and pick top 3
    artists = sorted(artists, key=lambda x: x['popularity'], reverse=True)[:3]

    if not artists:
        return html.P("No artists found for this genre.", style={"textAlign": "center", "fontSize": "20px"})

    cards = []
    for artist in artists:
        cards.append(
            html.Div(
                style={
                    "border": "1px solid #ddd",
                    "borderRadius": "12px",
                    "padding": "15px",
                    "textAlign": "center",
                    "boxShadow": "2px 2px 8px rgba(0,0,0,0.1)",
                    "background": "white"
                },
                children=[
                    html.Img(src=artist["image"], style={"width": "100%", "borderRadius": "12px"}),
                    html.H3(artist["name"], style={"marginTop": "10px"}),
                    html.P(f"Popularity: {artist['popularity']}"),
                    html.P(f"Genres: {artist['genres']}")
                ]
            )
        )
    return cards








""""

import dash
from dash import dcc, html, Input, Output
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# -------- SPOTIFY AUTH --------
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="4a1acd1c8e7949bbba7fec2eb1a9e181",
    client_secret="69e497dd3f834f02921904cf80b578e9"
))

# -------- HARD-CODED TOP ARTISTS PER GENRE --------
TOP_ARTISTS_BY_GENRE = {
    "pop": [
        "Lady Gaga", "Justin Bieber", "Ed Sheeran", "Billie Eilish", "Ariana Grande",
        "Taylor Swift", "Rosé", "Sabrina Carpenter", "Tate McRae", "Mariah Carey"
    ],
    "hip hop": [
        "Kendrick Lamar", "Drake", "Travis Scott", "J. Cole", "Cardi B",
        "Lil Baby", "Doja Cat", "Post Malone", "Megan Thee Stallion", "Kanye West"
    ],
    "r&b": [
        "SZA", "The Weeknd", "H.E.R.", "GIVĒON", "Bruno Mars",
        "Chris Brown", "Jhene Aiko", "Frank Ocean", "Alicia Keys", "Summer Walker"
    ],
    "country": [
        "Morgan Wallen", "Luke Combs", "Zach Bryan", "Chris Stapleton", "Lainey Wilson",
        "Cody Johnson", "Megan Moroney", "Ella Langley", "Zach Top", "Miranda Lambert"
    ],
    "rock": [
        "Coldplay", "Linkin Park", "Twenty One Pilots", "Imagine Dragons", "Foo Fighters",
        "Red Hot Chili Peppers", "The Killers", "Green Day", "Kings of Leon", "Paramore"
    ],
    "soul": [
        "Adele", "Sam Smith", "Leon Bridges", "Jazmine Sullivan", "John Legend",
        "Lizzo", "Alicia Keys", "Solange", "Anderson .Paak", "Corinne Bailey Rae"
    ],
    "jazz": [
        "Norah Jones", "Miles Davis", "Esperanza Spalding", "Diana Krall", "John Coltrane",
        "Herbie Hancock", "Chet Baker", "Louis Armstrong", "Ella Fitzgerald", "Bill Evans"
    ],
    "electronic": [
        "Calvin Harris", "David Guetta", "Kygo", "Martin Garrix", "Marshmello",
        "The Chainsmokers", "Zedd", "Avicii", "Diplo", "Deadmau5"
    ]
}

# -------- FUNCTION TO GET ARTIST INFO --------
def get_artist_info(artist_name):
    result = sp.search(q=f'artist:{artist_name}', type="artist", limit=1)
    if not result["artists"]["items"]:
        return None
    artist = result["artists"]["items"][0]
    image_url = "https://via.placeholder.com/200"
    if artist.get("images") and len(artist["images"]) > 0:
        image_url = artist["images"][0]["url"]
    return {
        "name": artist["name"],
        "popularity": artist.get("popularity", 0),
        "genres": ", ".join(artist.get("genres", [])) if artist.get("genres") else "Unknown",
        "image": image_url
    }


# Ordered genres: popular first
GENRES = ["pop", "hip hop", "r&b", "country", "rock", "soul", "jazz", "electronic"]

layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    children=[
        html.H1("🎵 Top Artists by Genre", style={"textAlign": "center"}),

        html.Div([
            html.Label("Select Genre:", style={"fontSize": "18px", "marginRight": "10px"}),
            dcc.Dropdown(
                id="genre-dropdown",
                options=[{"label": g.title(), "value": g} for g in GENRES],
                value="pop",
                style={"width": "400px", "margin": "auto"}
            )
        ], style={"textAlign": "center", "marginBottom": "30px"}),

        html.Div(id="artist-grid", style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "20px"
        })
    ]
)

# -------- CALLBACK --------
@callback(
    Output("artist-grid", "children"),
    Input("genre-dropdown", "value")
)
def update_artists(genre):
    artist_names = TOP_ARTISTS_BY_GENRE.get(genre, [])
    artists = [get_artist_info(name) for name in artist_names]
    artists = [a for a in artists if a]

    # Sort by Spotify popularity descending and pick top 3
    artists = sorted(artists, key=lambda x: x['popularity'], reverse=True)[:3]

    if not artists:
        return html.P("No artists found for this genre.", style={"textAlign": "center", "fontSize": "20px"})

    cards = []
    for artist in artists:
        cards.append(
            html.Div(
                style={
                    "border": "1px solid #ddd",
                    "borderRadius": "12px",
                    "padding": "15px",
                    "textAlign": "center",
                    "boxShadow": "2px 2px 8px rgba(0,0,0,0.1)",
                    "background": "white"
                },
                children=[
                    html.Img(src=artist["image"], style={"width": "100%", "borderRadius": "12px"}),
                    html.H3(artist["name"], style={"marginTop": "10px"}),
                    html.P(f"Popularity: {artist['popularity']}"),
                    html.P(f"Genres: {artist['genres']}")
                ]
            )
        )
    return cards

"""