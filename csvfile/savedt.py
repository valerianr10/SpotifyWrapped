import pandas as pd

def save_tracks_to_csv(top_tracks, recent_tracks, top_path="CSV2/top_tracks.csv", recent_path="CSV2/recently_played.csv"):
    df_top = pd.DataFrame(top_tracks)
    df_recent = pd.DataFrame(recent_tracks)
    df_top.to_csv(top_path, index=False)
    df_recent.to_csv(recent_path, index=False)
