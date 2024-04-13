import requests

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


