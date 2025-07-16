from db.dbconf import get_connection

def insert_top_tracks(tracks, time_range, user_id):
    conn = get_connection()
    cur = conn.cursor()
    for _, track in tracks.iterrows():
        cur.execute("""
            INSERT INTO top_tracks (track, artist, album, popularity, time_range, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            track["track"],
            track["artist"],
            track["album"],
            track["popularity"],
            time_range,
            user_id
        ))
    conn.commit()
    cur.close()
    conn.close()

def insert_recently_played(tracks, user_id):
    conn = get_connection()
    cur = conn.cursor()
    for _, track in tracks.iterrows():
        cur.execute("""
            INSERT INTO recently_played (track, artist, played_at, user_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            track["track"],
            track["artist"],
            track["played_at"],
            user_id
        ))
    conn.commit()
    cur.close()
    conn.close()
