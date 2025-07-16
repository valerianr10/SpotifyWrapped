import sys
import os
import pandas as pd

# Biar bisa import dari folder lain
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spotify_auth import create_spotify_client, get_user_info, get_top_tracks, get_recently_played
from etl.load import insert_top_tracks, insert_recently_played
from csvfile.savedt import save_tracks_to_csv

# 1. Autentikasi Spotify
sp = create_spotify_client()

# 2. Ambil info user
user_info = get_user_info(sp)
user_id = user_info["id"]
print(f"✅ Logged in as: {user_info['display_name']} (user_id={user_id})")

# 3. Extract data dari Spotify
top_tracks_raw = get_top_tracks(sp, time_range="long_term", limit=50)
recent_tracks_raw = get_recently_played(sp, limit=50)

# 4. Tambahkan user_id ke setiap item
for track in top_tracks_raw:
    track["user_id"] = user_id
for track in recent_tracks_raw:
    track["user_id"] = user_id

# 5. Ubah ke DataFrame biar aman buat insert
top_tracks_df = pd.DataFrame(top_tracks_raw)
recent_tracks_df = pd.DataFrame(recent_tracks_raw)

# 6. Load ke Database
insert_top_tracks(top_tracks_df, "long_term", user_id)
insert_recently_played(recent_tracks_df, user_id)

# 7. Simpan ke CSV (opsional)
save_tracks_to_csv(top_tracks_df, recent_tracks_df)
def clear_spotify_cache():
    try:
        os.remove(".cache")
        print("🧹 Token cache dihapus!")
    except FileNotFoundError:
        print("ℹ️ Tidak ada cache untuk dihapus.")

print("✅ Data berhasil dimasukkan ke database & CSV.")
