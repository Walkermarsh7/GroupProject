# Group7Dash

## Project Overview  
The inspiration for our project came from our orientation scavenger hunt, where we kept debating which artists were more popular and which songs “won” in different contexts. We wanted a way to actually test those debates with data, which led to the idea of a Spotify dashboard.  

The app has four pages, each highlighting a different angle: top artists by genre, a direct comparison of two songs, a global map of songs by country, and artist-level top tracks. The intended audience includes casual Spotify users such as our classmates, and anyone interested in exploring music trends visually such as aspiring musicians, music analysts, and content creators. The value of the project is that it makes Spotify’s raw data interactive and engaging, so people can explore music popularity instead of arguing about it without evidence.  

## How to Run Locally and Make Live  
To run the app on your computer, clone the repository and set up a Python environment. Install the requirements from `requirements.txt`, then start the server with:

The dashboard will open in a browser at [http://127.0.0.1:8050](http://127.0.0.1:8050).

Because the app uses Spotify’s API, you’ll need to register for a free developer account with Spotify and create an app to get a `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`. These should be stored as environment variables so the app can authenticate properly.

Once the app is running locally, the next step is to make it live by deploying to the web. We are using Render for deployment. The process involves connecting our GitHub repository to Render, adding the Spotify credentials as environment variables in the Render dashboard, and specifying commands to install dependencies and start the server. Render will then build and then host the app, making it available to anyone through a public URL.

## Data Sources and Data Dictionary

Our project combines both live and static data. The Spotify Web API provides artist details, song metadata, popularity scores, and images, which power most of the interactive features. We also used a prepared dataset, `top_songs_by_country.csv`, to create a global map of top songs. This dataset contains countries, the most popular song in each, the performing artist, and a popularity score. We cleaned the file, standardized field names, and added ISO-3 country codes to support mapping.

The main fields we used include:
- `country`: the name of the country  
- `name`: the top track in that country  
- `artists`: the artist(s) of that track  
- `popularity`: Spotify’s popularity score (0–100)  
- `country_code`: ISO-3 code derived from the country name  

From the Spotify API we also used:
- `name`: artist or track name  
- `popularity`: Spotify popularity score  
- `genres`: list of genres associated with an artist  
- `images`: URLs to artist or album images  

Together these sources let us use the dashboard to answer questions like “Who are the biggest artists in each genre?”, “What songs dominate around the world?”, and “Which of two tracks is more popular right now?”

## AI Appendix

For our project, we combined our own work based on class exercises with AI assistance for new features. The multipage app structure (`app.py` scaffold with `Dash(use_pages=True)` and simple page registration) and general callback patterns are drawn directly from class and written by us. These form the backbone of our app.

We relied on AI assistance for all sections to help us go beyond the class demos. The AI tools that we used to help were ChatGPT and GitHub co-pilot. For Page 1 (Top Artists by Genre), AI generated the Spotify API integration using Spotipy, the dictionary of top artists per genre, and the logic to fetch images and popularity scores. We verified the queries and adjusted the styling of the artist cards. On Page 2 (Spotify Map), AI helped clean the CSV, implement fuzzy ISO code matching with `pycountry`, and build a choropleth with hover templates and a scrollable song list. We validated the data cleaning steps and tested map behavior across multiple countries.

For Page 3 (Songs by Artist), AI assisted with implementing Spotify’s client credentials flow, searching for an artist, fetching their top tracks, and returning both a bar chart of popularity scores and clickable links. We reviewed the API endpoints, confirmed proper token refresh, and validated callback outputs. On Page 4 (Compare Songs), AI wrote the helper functions to cache tokens, search for tracks, and compare popularity, as well as the callback that displays results in a bar chart. We tested error cases (invalid input, no results, API errors) and adjusted messages for clarity.

In `app.py`, while the multipage setup is class-based, we used AI to help us refine our code for our theme. We adopted the even spacing, dark background, and green accents, which improved aesthetics.

We also used AI to help us format this `README.md`. When previewing the document, we noticed that the formatting looked off. We uploaded it into ChatGPT and asked for help making it easier to read in GitHub. In doing this, AI suggested adding backticks around commands and structuring the file with proper headers. These adjustments improved the overall readability and visual appeal of our project documentation.

It’s worth noting that AI did not always get things right. In particular, it occasionally mishandled Spotify credentials: sometimes putting keys directly into code, sometimes mixing up Spotipy with raw requests, and other times omitting the token refresh logic. We caught these issues during testing, fixed them by following Spotify’s documentation, and moved secrets to the correct places. This process made us more careful about security and helped us understand how the API flow actually works.

We manually validated all AI-generated code, tested it for correctness, fixed mistakes (especially with credentials), edited variable names and messages for clarity, and ensured the project remained consistent with class-taught structures.
