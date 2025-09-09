from dash import html, dcc, callback, Output, Input, register_page
import pandas as pd
import plotly.express as px
from pathlib import Path
import pycountry

# Register this tab
register_page(__name__, path="/page2", name="Spotify Map")

# Load and clean data
DataPath = Path(__file__).resolve().parent.parent / "data" / "top_songs_by_country.csv"
df = pd.read_csv(DataPath)

# Rename columns
df = df.rename(columns={
    "country": "country_name",
    "name": "top_song",
    "artists": "artist",
    "popularity": "popularity_score"
})

# Clean strings
df["country_name"] = df["country_name"].astype(str).str.strip()
df["top_song"] = df["top_song"].astype(str).str.strip()
df["artist"] = df["artist"].astype(str).str.strip()

# Ensure popularity_score is numeric
df["popularity_score"] = pd.to_numeric(df["popularity_score"], errors="coerce")
df = df.dropna(subset=["popularity_score"])

# Select top song per country using idxmax
df = df.loc[df.groupby("country_name")["popularity_score"].idxmax()].reset_index(drop=True)

# Add ISO-3 country codes using fuzzy matching
def get_iso3(name):
    try:
        match = pycountry.countries.search_fuzzy(name)
        return match[0].alpha_3
    except LookupError:
        return None

df["country_code"] = df["country_name"].apply(get_iso3)
df = df.dropna(subset=["country_code"])

# Assign uniform color
df["uniform_color"] = "Spotify Green"

# Layout
layout = html.Div(
    style={"backgroundColor": "#FDF9F9", "padding": "20px"},
    children=[
        html.H1("Top Spotify Songs Around the World", style={"color": "#000000", "textAlign": "center"}),
        html.Div(
            dcc.Graph(id="spotify-map"),
            style={"textAlign": "center", "marginBottom": "40px"}
        ),
        html.H2("Top Songs by Country", style={"color": "#000000", "textAlign": "center"}),
        html.Div(
            id="song-list",
            style={
                "maxHeight": "500px",
                "overflowY": "scroll",
                "padding": "10px",
                "backgroundColor": "#ffffff",
                "border": "1px solid #ccc",
                "borderRadius": "5px",
                "width": "80%",
                "margin": "0 auto",
                "color": "#000000"
            }
        )
    ]
)

# Callback
@callback(
    Output("spotify-map", "figure"),
    Output("song-list", "children"),
    Input("spotify-map", "id")
)
def update_map(_):
    # Map figure
    fig = px.choropleth(
        df,
        locations="country_code",
        locationmode="ISO-3",
        color="uniform_color",
        hover_name="country_name",
        hover_data={
            "top_song": True,
            "artist": True,
            "popularity_score": True,
            "country_code": False
        },
        color_discrete_map={"Spotify Green": "#1DB954"},
        title="Spotify Coverage Map"
    )

    fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br>" +
        "🎵 <b>Song:</b> %{customdata[0]}<br>" +
        "🎤 <b>Artist:</b> %{customdata[1]}<br>" +
        "🔥 <b>Popularity Score:</b> %{customdata[2]:,.0f}<extra></extra>",
        customdata=df[["top_song", "artist", "popularity_score"]]
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False, projection_type="equirectangular"),
        paper_bgcolor="#1e1e1e",
        font_color="white",
        margin=dict(l=10, r=10, t=50, b=10),
        legend_title_text="",
        showlegend=False
    )

    # Song list
    song_items = [
        html.Div([
            html.Strong(f"{row['country_name']}: "),
            f"{row['top_song']} — {row['artist']} (Score: {int(row['popularity_score'])})"
        ], style={"marginBottom": "8px"})
        for _, row in df.iterrows()
    ]

    return fig, song_items