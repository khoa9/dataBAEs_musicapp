import requests
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

#This script will look at all the track_id obtained in Step 2 and download it to subfolder of its genre. 

# Set the path to the CSV file containing the track details
csv_file_path = '/Users/bach/Documents/MP3-Project/ID-Scrap/Metadata/song_get_response_previews.csv'

# Set the base path for the folder where files will be saved
base_download_path = '/Users/bach/Documents/MP3-Project/ID-Scrap/mp3/'

# Function to download the preview and save it with the track ID as its name
def download_preview(preview_url, genre, track_id):
    # Create the directory for the genre if it doesn't already exist
    genre_path = os.path.join(base_download_path, genre)
    os.makedirs(genre_path, exist_ok=True)  # Use exist_ok=True to avoid FileExistsError

    # The path to save the file, named after the track ID
    file_path = os.path.join(genre_path, f"{track_id}.mp3")

    # Download the file
    response = requests.get(preview_url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return f"Downloaded track {track_id} to {file_path}"
    else:
        return f"Failed to download track {track_id}. Status code: {response.status_code}"

# Function to initiate download for a single row (track)
def download_track(row):
    if row['Preview URL'] and row['Preview URL'] != 'No preview available':
        return download_preview(row['Preview URL'], row['Genre'], row['Track ID'])

# Start timing
start_time = time.time()

# Use pandas to read the CSV file
df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

# Setup ThreadPoolExecutor to download in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit all tasks to the executor
    futures = [executor.submit(download_track, row) for index, row in df.iterrows()]

    # Wait for all futures to complete
    for future in as_completed(futures):
        print(future.result())

# End timing
end_time = time.time()

# Calculate and print the total time taken
total_time = end_time - start_time
print(f"Total time taken: {total_time:.2f} seconds")