from spotify_auth import create_spotify_client

def extract_data(time_range="long_term", limit=50):
    sp = create_spotify_client()
    user_info = sp.current_user()
    user_id = user_info["id"]

    top_tracks = get_top_tracks(sp, user_id, time_range, limit)
    recent_tracks = get_recently_played(sp, user_id, limit)
    return top_tracks, recent_tracks, user_id

def get_top_tracks(sp, user_id, time_range="long_term", limit=50):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [
        {
            "track": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "popularity": item["popularity"],
            "user_id": user_id  
        }
        for item in results["items"]
    ]

def get_recently_played(sp, user_id, limit=50):
    results = sp.current_user_recently_played(limit=limit)
    return [
        {
            "track": item["track"]["name"],
            "artist": item["track"]["artists"][0]["name"],
            "played_at": item["played_at"],
            "user_id": user_id 
        }
        for item in results["items"]
    ]

