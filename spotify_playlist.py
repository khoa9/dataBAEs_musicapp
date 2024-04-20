import requests

def create_spotify_playlist(user_token,song_name,artist_name):
    endpoint_url = "https://api.spotify.com/v1/users/bachkhoa144/playlists"
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }
    
    full_playlist_name = f"Song Similar to {song_name} from {artist_name} by Databae"  # Dynamic playlist name

    payload = {
        "name": full_playlist_name,
        "description": "New playlist created through Databae's Audio Platform",
        "public": False  # Set to True if you want the playlist to be public
    }
    
    print(f"Creating playlist with name: {full_playlist_name}")
    response = requests.post(endpoint_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        print("Playlist created successfully.")
        return response.json()
    else:
        print(f"Failed to create playlist: {response.status_code} - {response.text}")
        return response.json()

def add_tracks_to_playlist(user_token, playlist_id, track_ids):
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "uris": [f"spotify:track:{track_id}" for track_id in track_ids]
    }
    
    print(f"Adding tracks to playlist ID {playlist_id}. Track IDs: {track_ids}")
    response = requests.post(endpoint_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        print(f"Tracks added successfully to playlist {playlist_id}.")
        return response.json()
    else:
        print(f"Failed to add tracks to playlist: {response.status_code} - {response.text}")
        return response.json()