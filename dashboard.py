import streamlit as st
import pandas as pd
import psycopg2
from store_user import run_sync
from main import clear_spotify_cache
import os

st.set_page_config(page_title="🎧 Spotify Wrapped Dashboard", layout="wide")

def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"]
    )

@st.cache_data
def load_user_ids():
    conn = get_connection()
    df = pd.read_sql_query("SELECT DISTINCT user_id FROM top_tracks", conn)
    conn.close()
    return df["user_id"].tolist()

@st.cache_data
def load_top_tracks(user_id):
    conn = get_connection()
    query = "SELECT * FROM top_tracks WHERE user_id = %s"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    df = df.drop_duplicates(subset="track")
    df["Rank"] = range(1, len(df) + 1)
    return df

@st.cache_data
def load_recently_played(user_id):
    conn = get_connection()
    query = "SELECT * FROM recently_played WHERE user_id = %s"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    df["played_at"] = pd.to_datetime(df["played_at"])
    df["played_date"] = df["played_at"].dt.date
    df["played_hour"] = df["played_at"].dt.hour
    df["day_name"] = df["played_at"].dt.day_name()
    return df

st.title("🎵 My Spotify Wrapped - Personal Edition")

st.subheader("🔄 Sinkronisasi Data Spotify")
if st.button("Klik untuk Sync Data dari Spotify"):
    try:
        run_sync()
        st.cache_data.clear()
        st.success("✅ Data berhasil disinkronkan dari Spotify!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Gagal sync data: {e}")

st.subheader("🔁 Ganti Akun Spotify")
if st.button("Logout / Ganti Akun"):
    clear_spotify_cache()
    st.success("🧹 Logout berhasil. Silakan klik Sync untuk login ulang dengan akun berbeda.")

st.subheader("👤 Pilih User")
user_ids = load_user_ids()
if not user_ids:
    st.warning("Belum ada user yang disimpan.")
    st.stop()

selected_user = st.selectbox("Pilih User", user_ids)

df_top = load_top_tracks(selected_user)
df_recent = load_recently_played(selected_user)

st.subheader("🎶 Top 10 Lagu (Long Term - Ranked)")
top_10_tracks = df_top[["Rank", "track", "artist"]].head(10)
top_10_tracks = top_10_tracks.rename(columns={"track": "Track", "artist": "Artist"})
st.table(top_10_tracks.set_index("Rank"))

st.subheader("🧑‍🎤 Top 10 Artis (Long Term - Ranked)")
top_10_artists = df_top["artist"].value_counts().reset_index().head(10)
top_10_artists.columns = ["Artist", "Jumlah Lagu Masuk Top"]
top_10_artists["Rank"] = range(1, len(top_10_artists) + 1)
st.table(top_10_artists.set_index("Rank"))

st.subheader("📻 Lagu yang Sering Diputar (Recently Played)")
top_recent_tracks = (
    df_recent.groupby(["track", "artist"])
    .size()
    .reset_index(name="Jumlah Diputar")
    .sort_values(by="Jumlah Diputar", ascending=False)
    .head(10)
)
top_recent_tracks["Rank"] = range(1, len(top_recent_tracks) + 1)
top_recent_tracks = top_recent_tracks.rename(columns={
    "track": "Track",
    "artist": "Artist"
})
st.table(top_recent_tracks[["Rank", "Track", "Artist", "Jumlah Diputar"]].set_index("Rank"))
