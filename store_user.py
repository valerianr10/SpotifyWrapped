from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from etl.load import insert_top_tracks, insert_recently_played

# Load environment variables dari .env
load_dotenv()

# Koneksi ke PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

# Buat client Spotify
def create_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope="user-top-read user-read-recently-played",
        show_dialog=True  # biar bisa pilih akun kalau udah login sebelumnya
    )
    return spotipy.Spotify(auth_manager=auth_manager)

# Ambil user ID dari Spotify
def get_user_id(sp):
    return sp.current_user()["id"]

# Ambil Top Tracks dari Spotify
def get_top_tracks(sp, user_id, time_range="long_term", limit=50):
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    return pd.DataFrame([{
        "track": t["name"],
        "artist": t["artists"][0]["name"],
        "album": t["album"]["name"],
        "popularity": t["popularity"],
        "user_id": user_id
    } for t in results["items"]])

# Ambil Recently Played dari Spotify
def get_recently_played(sp, user_id, limit=50):
    results = sp.current_user_recently_played(limit=limit)
    return pd.DataFrame([{
        "track": t["track"]["name"],
        "artist": t["track"]["artists"][0]["name"],
        "played_at": t["played_at"],
        "user_id": user_id
    } for t in results["items"]])

# Simpan dataframe ke DB
def save_to_db(df, table_name):
    conn = get_connection()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        columns = ', '.join(row.index)
        placeholders = ', '.join(['%s'] * len(row))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        cursor.execute(sql, tuple(row))
    conn.commit()
    cursor.close()
    conn.close()

# Jalankan Sinkronisasi
def run_sync():
    sp = create_spotify_client()
    user_id = get_user_id(sp)
    print(f"🔗 Sync data untuk user: {user_id}")

    top_tracks = get_top_tracks(sp, user_id)
    recent_tracks = get_recently_played(sp, user_id)

    insert_top_tracks(top_tracks, "long_term", user_id)
    insert_recently_played(recent_tracks, user_id)

    print("✅ Data berhasil disimpan ke database.")
