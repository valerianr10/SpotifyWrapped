from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

def create_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope="user-top-read user-read-recently-played",
        show_dialog=True,
        cache_path=".cache"
    ))  


    token_info = auth_manager.get_access_token(as_dict=True)
    sp = spotipy.Spotify(auth=token_info["access_token"])
    return sp, token_info


def get_user_info(sp):
    """
    Mengambil informasi user Spotify:
    - user_id
    - display_name
    - email
    """
    user = sp.current_user()
    return {
        "id": user["id"],
        "display_name": user.get("display_name", ""),
        "email": user.get("email", "")
    }


def get_top_tracks(sp, time_range="long_term", limit=10):
    """
    Mengambil top tracks user berdasarkan time_range.
    """
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = []
    for item in results["items"]:
        track_info = {
            "track": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "popularity": item["popularity"]
        }
        tracks.append(track_info)
    return tracks


def get_recently_played(sp, limit=50):
    """
    Mengambil riwayat pemutaran terakhir user.
    """
    results = sp.current_user_recently_played(limit=limit)
    tracks = []
    for item in results["items"]:
        track = item["track"]
        track_info = {
            "track": track["name"],
            "artist": track["artists"][0]["name"],
            "played_at": item["played_at"]
        }
        tracks.append(track_info)
    return tracks
