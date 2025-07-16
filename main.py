from dotenv import load_dotenv
import os
import pandas as pd
from spotify_auth import create_spotify_client, get_user_info
from etl.extract import extract_data
from etl.load import insert_top_tracks, insert_recently_played
from csvfile.savedt import save_tracks_to_csv

load_dotenv()

def clear_spotify_cache():
    try:
        os.remove(".cache")
        print("🧹 Token cache dihapus!")
    except FileNotFoundError:
        print("ℹ️ Tidak ada cache untuk dihapus.")

if __name__ == "__main__":
    # 1. Auth Spotify
    sp, _ = create_spotify_client()

    # 2. Get user info
    user_info = get_user_info(sp)
    user_id = user_info["id"]

    print(f"✅ Logged in as: {user_info['display_name']} (user_id={user_id})")

    # 3. Extract data
    top_tracks_raw, recent_tracks_raw, _ = extract_data()
    top_tracks_df = pd.DataFrame(top_tracks_raw)
    recent_tracks_df = pd.DataFrame(recent_tracks_raw)

    # 4. Load ke DB
    insert_top_tracks(top_tracks_df, "long_term", user_id)
    insert_recently_played(recent_tracks_df, user_id)

    # 5. Simpan ke CSV
    save_tracks_to_csv(top_tracks_df, recent_tracks_df)

    print("✅ Semua data berhasil diproses.")
