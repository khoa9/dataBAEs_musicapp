import requests

import config

'''
client_id = '##'  # Exposed credentials (please reset these in your Spotify Developer Dashboard)
client_secret = '##'
'''

client_id,client_secret = config.getSpotifyClientCredentials()

def get_spotify_preview_url(track_id,market='US'):
    # Replace 'your_client_id' and 'your_client_secret' with your Spotify API credentials
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        {
            'grant_type': 'client_credentials',
            'client_id': client_id,  # Exposed credentials (please reset these in your Spotify Developer Dashboard)
            'client_secret': client_secret,  # Exposed credentials (please reset these in your Spotify Developer Dashboard)
        },
    )
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    # Use the access token to access the Spotify Web API; Spotify returns the access token in a JSON payload
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Include the market parameter in the request
    track_response = requests.get(
        f'https://api.spotify.com/v1/tracks/{track_id}',
        headers=headers,
        params={'market': market}
    )
    track_data = track_response.json()
    return track_data.get('preview_url')

def search_spotify_song(song_name, artist_name, market='US'):

    # Authenticate and retrieve access token
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
    )

    # Check authentication success
    if auth_response.status_code != 200:
        return None, None  # Authentication failed

    auth_response_data = auth_response.json()
    access_token = auth_response_data.get('access_token')
    if not access_token:
        return None, None  # No access token received

    # Use the access token to search for the song
    headers = {'Authorization': f'Bearer {access_token}'}
    search_params = {
        'q': f'track:{song_name} artist:{artist_name}',
        'type': 'track',
        'market': market,
        'limit': 1  # Limit the search to the top result
    }

    search_response = requests.get(
        'https://api.spotify.com/v1/search',
        headers=headers,
        params=search_params
    )

    # Check search success
    if search_response.status_code != 200:
        return None, None  # Search request failed

    search_data = search_response.json()
    items = search_data.get('tracks', {}).get('items', [])

    if items:
        track_id = items[0].get('id')
        preview_url = items[0].get('preview_url')
        track_name = items[0].get('name')
        artist_names = ', '.join([artist['name'] for artist in items[0]['artists']])
        album_name = items[0]['album']['name']
        return track_id, preview_url, track_name, artist_names, album_name
    
    return None, None, None, None, None  # No tracks found


def create_spotify_playlist(user_token, song_name, artist_name):
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