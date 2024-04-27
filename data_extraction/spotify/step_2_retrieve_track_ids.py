import csv
import requests
import pandas as pd
import base64
import concurrent.futures
import time 
import os


#Looking up all the AlbumID Scrapped from Step 1, and retrieve all track_ID from the album. Only retain track_ID that contains a Preview_URL.
# Main script setup
#csv_file_path will point to the csv obtained from Step 1
#output_csv_path will be the file used to download song from Step 3.

client_id = '#'
client_secret = '#'
csv_file_path = 'album_id_list.csv'
output_csv_path = 'track_id_list.csv'

def get_access_token(client_id, client_secret):
    print("Requesting access token...")
    token_url = 'https://accounts.spotify.com/api/token'
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode())
    headers = {
        'Authorization': f'Basic {encoded_credentials.decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'grant_type': 'client_credentials'}
    response = requests.post(token_url, headers=headers, data=payload)
    if response.status_code == 200:
        print("Access token successfully obtained.")
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to obtain access token. Status code: {response.status_code}, Response: {response.text}")

def read_album_ids_genres_and_characteristics(csv_file_path):
    print(f"Reading album IDs, genres, and characteristics from {csv_file_path}...")
    df = pd.read_csv(csv_file_path, header=0)
    album_info_dict = {row['Spotify ID']: {'Genre': row['Genre'], 'Characteristics': row.get('Characteristics', '')} for index, row in df.iterrows()}
    print(f"Found {len(album_info_dict)} album IDs with genres and characteristics.")
    return album_info_dict

def fetch_album_details(album_id, album_info, access_token, market=None, retries=3, backoff_factor=0.5):
    genre = album_info['Genre']
    characteristics = album_info['Characteristics']
    base_url = f'https://api.spotify.com/v1/albums/{album_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'market': market} if market else {}
    for attempt in range(retries):
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            album_data = response.json()
            release_date = album_data.get('release_date', '')
            release_year = release_date.split('-')[0] if release_date else 'Unknown'
            tracks = album_data['tracks']['items']
            album_details = []
            for track in tracks:
                preview_url = track.get('preview_url')
                if preview_url:
                    album_details.append({
                        'Album ID': album_id,
                        'Album Name': album_data['name'],
                        'Genre': genre,
                        'Characteristics': characteristics,
                        'Release Year': release_year,
                        'Track ID': track['id'],
                        'Track Name': track['name'],
                        'Artists': ', '.join([artist['name'] for artist in track['artists']]),
                        'Available Markets': ', '.join(track.get('available_markets', [])),
                        'Duration (ms)': track['duration_ms'],
                        'Explicit': track['explicit'],
                        'Preview URL': preview_url
                    })
            return album_details
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            sleep_time = int(retry_after) if retry_after else (2 ** attempt) * backoff_factor
            print(f"Rate limit exceeded, sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
        else:
            print(f"Failed to fetch details for album ID {album_id} with market {market}. Status code: {response.status_code}, Response: {response.text}")
            break
    return []

def fetch_albums_details_parallel(album_info_dict, access_token, market=None, save_threshold=1000):
    start_time = time.time()
    album_tracks_details = []
    processed_albums_count = 0  # Counter for processed albums

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(fetch_album_details, album_id, album_info, access_token, market): album_id
            for album_id, album_info in album_info_dict.items()
        }

        total_albums = len(futures)
        for future in concurrent.futures.as_completed(futures):
            details = future.result()
            album_tracks_details.extend(details)
            processed_albums_count += 1  # Increment the processed albums counter
            print(f"Processed album {processed_albums_count} of {total_albums} (ID: {futures[future]})")  # Log progress

    # Save any remaining songs after processing all albums
    if album_tracks_details:
        save_album_tracks_details_to_csv(album_tracks_details, output_csv_path, mode='a')
    
    # After processing all albums, save track previews
    save_track_previews_to_csv(album_tracks_details, output_csv_path)

    end_time = time.time()
    print(f"Finished processing {total_albums} albums in {end_time - start_time:.2f} seconds.")


def save_album_tracks_details_to_csv(album_tracks_details, output_csv_path, mode='w'):
    with open(output_csv_path, mode=mode, newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['Album ID', 'Album Name', 'Genre', 'Characteristics', 'Release Year', 'Track ID', 'Track Name', 'Artists', 'Available Markets', 'Duration (ms)', 'Explicit', 'Preview URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w' or csvfile.tell() == 0:  # Write headers only if file is empty or in write mode
            writer.writeheader()
        writer.writerows(album_tracks_details)

def save_track_previews_to_csv(album_tracks_details, output_csv_path):
    previews_csv_path = output_csv_path.replace('.csv', '_previews.csv')
    print(f"Saving track previews, genres, and characteristics to {previews_csv_path}...")

    # Check if the file already exists
    file_exists = os.path.exists(previews_csv_path)
    mode = 'a' if file_exists else 'w'  # Append if exists, otherwise write

    fieldnames = ['Track ID', 'Preview URL', 'Genre']
    with open(previews_csv_path, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:  # Write headers only if file does not exist
            writer.writeheader()
        for track_detail in album_tracks_details:
            if track_detail['Preview URL'] != 'No preview available':
                writer.writerow({
                    'Track ID': track_detail['Track ID'],
                    'Preview URL': track_detail['Preview URL'],
                    'Genre': track_detail['Genre']
                })
    print("Track previews saved successfully.")

# Execute the script
if __name__ == "__main__":
    access_token = get_access_token(client_id, client_secret)
    market = 'US'
    if access_token:
        album_info_dict = read_album_ids_genres_and_characteristics(csv_file_path)
        fetch_albums_details_parallel(album_info_dict, access_token, market)
        print("Data fetching and saving complete.")
    else:
        print("Could not obtain access token. Exiting script.")