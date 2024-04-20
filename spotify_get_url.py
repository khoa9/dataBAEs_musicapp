import requests

client_id = 'fb04886b751a409e81639f7bc1891989'  # Exposed credentials (please reset these in your Spotify Developer Dashboard)
client_secret = '49afad6a5e2843d8807a0c7e8338600f'


def get_spotify_preview_url(track_id,market='US'):
    # Replace 'your_client_id' and 'your_client_secret' with your Spotify API credentials
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        {
            'grant_type': 'client_credentials',
            'client_id': 'fb04886b751a409e81639f7bc1891989',  # Exposed credentials (please reset these in your Spotify Developer Dashboard)
            'client_secret': '49afad6a5e2843d8807a0c7e8338600f',  # Exposed credentials (please reset these in your Spotify Developer Dashboard)
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
            'client_id': 'fb04886b751a409e81639f7bc1891989',
            'client_secret': '49afad6a5e2843d8807a0c7e8338600f',
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


