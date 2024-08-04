import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize the Spotify client
CLIENT_ID = "f5184f59eb6042428f873e12643b07f1"
CLIENT_SECRET = "907d5d15e3294169b51f90334ce10dc1"
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get song album cover URL
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"
    
# Function to get song url
def get_track_info(track_name, artist_name):
    search_query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track", limit=1)

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_id = track["id"]
        spotify_link = track["external_urls"]["spotify"]
        return track_id, spotify_link
    else:
        return None, None

# Function to recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_posters = []
    recommended_id = []
    for i in distances[1:6]:
        # Fetch the song artist
        artist = music.iloc[i[0]].artist
        # Fetch the song poster
        recommended_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_id.append(get_track_info(music.iloc[i[0]].song, artist)[0]) # Appending track ID
    return recommended_music_names, recommended_posters, recommended_id

# Load data and similarity matrix
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Set page background color and style
st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
            color: #1E90FF;
        }
        .button {
            display: block;
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 8px;
            background-color: #1E90FF;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0077CC;
        }
        .recommendation {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-top: 20px;
        }
        .song-card {
            width: calc(95% - 20px); /* Adjusted width */
            margin: 20px;
            background-color: #fff;
            border-radius: 10px;
            padding: 10px;
            padding-bottom: 10px; /* Added semicolon */
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .song-card img {
            width: 100%;
            border-radius: 8px;
        }
        .song-card p {
            margin-top: 20px;
            text-align: center;
            font-weight: bold;
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title('Music Recommender System')

selected_song = st.selectbox(
    "Choose a song:",
    music['song']
)

if st.button('Show Recommendations'):
    recommended_songs, recommended_posters, recommended_id = recommend(selected_song)

    st.subheader('Recommended Songs')
    st.markdown('<hr>', unsafe_allow_html=True)

    # Display recommended songs in three columns
    for i in range(0, len(recommended_songs), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i < len(recommended_songs):
                st.markdown(
                    f"""
                    <div class="song-card">
                        <a href="https://open.spotify.com/track/{recommended_id[i]}"><img src="{recommended_posters[i]}"></a>
                        <p>{recommended_songs[i]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with col2:
            if i + 1 < len(recommended_songs):
                st.markdown(
                    f"""
                    <div class="song-card">
                        <a href="https://open.spotify.com/track/{recommended_id[i + 1]}"><img src="{recommended_posters[i + 1]}"></a>
                        <p>{recommended_songs[i + 1]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with col3:
            if i + 2 < len(recommended_songs):
                st.markdown(
                    f"""
                    <div class="song-card">
                        <a href="https://open.spotify.com/track/{recommended_id[i + 2]}"><img src="{recommended_posters[i + 2]}"></a>
                        <p>{recommended_songs[i + 2]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
