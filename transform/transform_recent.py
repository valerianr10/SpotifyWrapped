import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from db.dbconf import get_connection

def load_recently_played():
    conn = get_connection()
    query = "SELECT * FROM recently_played"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def transform_recent_data(df):
    # Ubah kolom 'played_at' jadi datetime
    df['played_at'] = pd.to_datetime(df['played_at'])

    df['played_date'] = df['played_at'].dt.date
    df['played_hour'] = df['played_at'].dt.hour

    # Buat ranking berdasarkan jumlah pemutaran
    ranking = (
        df.groupby(['track', 'artist'])
        .size()
        .reset_index(name='play_count')
        .sort_values(by='play_count', ascending=False)
        .reset_index(drop=True)
    )

    return ranking
