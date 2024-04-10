#Dang ML

# Install these packages in the terminal to run this code
# %pip install -q towhee towhee.models gradio ipython

import os
import pandas as pd
import numpy as np
import concurrent.futures
import json
from pathlib import Path

from towhee import pipe, ops

output_json_path = '/data'

# Functions for JSON metadata extraction
def get_metadata(x):
    # Define desired columns for metadata extraction
    cols = ['artist', 'genre', 'name', 'album']
    list_of_cols = []
    for col in cols:
        try:
            # Attempt to retrieve the first value for each metadata column
            mdata = list(x[col].values())[0]
        except:
            # If any metadata is missing, default to 'Unknown'
            mdata = "Unknown"
        list_of_cols.append(mdata)
    # Return a Series with the retrieved metadata
    return pd.Series(list_of_cols, index=cols)


# Create function to get metadata from json file as the dataframe 
def get_json_metadata_df(json_path):
    # Read JSON file into a DataFrame
    metadata = pd.read_json(json_path)
    # Apply metadata extraction function across the 'tracks' column
    metadata_df = metadata['tracks'].apply(get_metadata).reset_index()
    # Rename the 'index' column to 'track_id' for identification
    metadata_df = metadata_df.rename(columns={"index":"track_id"})
    # Initialize 'characteristic' column with NaN values to be filled later
    metadata_df['characteristic'] = np.nan
    return metadata_df

# Functions for CSV metadata cleaning and extraction
def clean_characteristics(characteristic, words_to_remove):
    # If value is NaN, return an empty string
    if pd.isna(characteristic):
        return ""
    # Split the characteristic string and remove unwanted words
    words = [word.strip() for word in characteristic.split(',')]
    cleaned_words = [word for word in words if word not in words_to_remove]
    # Rejoin the cleaned words into a single string
    return ', '.join(cleaned_words)

# Functions for CSV metadata cleaning and extraction
def clean_characteristics(characteristic, words_to_remove):
    # If value is NaN, return an empty string
    if pd.isna(characteristic):
        return ""
    # Split the characteristic string and remove unwanted words
    words = [word.strip() for word in characteristic.split(',')]
    cleaned_words = [word for word in words if word not in words_to_remove]
    # Rejoin the cleaned words into a single string
    return ', '.join(cleaned_words)

# Define words to remove from the 'characteristic' column
words_to_remove = {"melodic","avant-garde","rhythmic", "atmospheric", "instrumental", "sampling", "ballad",
                   "concept album", "progressive", "acoustic", "lo-fi", "LGBT", "technical",
                   "improvisation", "drug", "political", "uncommon time signatures", "minimalistic",
                   "philosophical", "vulgar", "crime", "violence", "autumn", "deadpan", "tropical",
                   "alienation", "winter", "Christian", "space", "science fiction", "alcohol",
                   "folklore", "self-hatred", "religious", "chamber music", "protest", "apocalyptic",
                   "satirical", "forest", "serious", "rain", "suicide", "misanthropic", "apathetic",
                   "disturbing", "tribal", "polyphonic", "ritualistic", "vocal group", "nihilistic",
                   "mythology", "war", "history", "choral", "medieval", "pagan", "hateful", "occult",
                   "infernal", "natural", "suite", "microtonal", "desert", "seasonal",
                   "a cappella", "Islamic", "novelty", "anarchism", "martial", "parody", "sports",
                   "Christmas", "Wall of Sound", "paranormal", "funereal", "patriotic", "concerto",
                   "oratorio", "generative music", "lobit", "anti-religious", "atonal", "waltz",
                   "rock opera", "madrigal", "nationalism", "string quartet", "sonata", "Halloween",
                   "fairy tale", "skit", "mood", "poem", "medley", "mashup", "interlude", "satanic",
                   "aleatory", "theme", "jingle", "symphony", "tone poem", "hymn", "movement",
                   "holiday", "opera", "ensemble", "monologue","urban","repetitive","drug","complex"}   

def get_csv_metadata(csv_path, words_to_remove):
    # Define columns to read from the CSV file
    columns_to_read = ['Track ID', 'Album Name', 'Genre', 'Track Name', 'Artists', 'Characteristics']
    # Map CSV column names to standardized DataFrame column names
    column_rename_map = {
        'Track ID': 'track_id',
        'Album Name': 'album',
        'Genre': 'genre',
        'Track Name': 'name',
        'Artists': 'artist',
        'Characteristics': 'characteristic'
    }
    # Read CSV, applying the column renaming map
    df = pd.read_csv(csv_path, usecols=columns_to_read, encoding='utf-8-sig')
    df.rename(columns=column_rename_map, inplace=True)
    # Apply characteristic cleaning function to the 'characteristic' column
    df['characteristic'] = df['characteristic'].apply(lambda x: clean_characteristics(x, words_to_remove))
    return df

# Define towhee pipeline for audio embedding with VGGish
def create_pipeline():
    return (
      pipe.input('path')
          .map('path', 'frame', ops.audio_decode.ffmpeg())
          .map('frame', 'vecs', ops.audio_embedding.vggish())
          .output('vecs')
    )

def embed_song(song_path):
    # Embed the song and return the vector
    p = create_pipeline()
    song_vector = p(song_path).get()[0]
    flat_song_vector = np.mean(song_vector, axis=0).tolist()  # Convert to list for JSON serialization
    return flat_song_vector

def process_subgenre_folder(folder_path, metadata_df):
    
    print(f"Processing folder: {folder_path.name}")
    song_vectors = []
    songs = [song for song in os.listdir(folder_path) if song.endswith('.mp3')]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(embed_song, os.path.join(folder_path, song)): song[:-4] for song in songs}
        for future in concurrent.futures.as_completed(futures):
            song_id = futures[future]
            vector = future.result()
            song_vectors.append({'track_id': song_id, 'vector': vector})

    # Convert song_vectors to a DataFrame
    vector_df = pd.DataFrame(song_vectors)
    
    # Merge vectors with metadata
    merged_df = pd.merge(metadata_df, vector_df, on='track_id', how='inner')
    
    # Append to JSON
    append_to_json(merged_df.to_dict(orient='records'), output_json_path)

def append_to_json(new_data, file_path):
    # Check if the file exists first
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and initialize with an empty list
        with open(file_path, 'w') as file:
            json.dump([], file)
    
    # Now, try to read the existing data
    try:
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                # If the file is empty or contains invalid JSON, start with an empty list
                existing_data = []
    except FileNotFoundError:
        # This block is technically redundant due to the initial check but added for clarity
        existing_data = []
    
    # Combine the existing data with the new data
    updated_data = existing_data + new_data
    
    # Write the combined data back to the file
    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=4)


# Create function to get completed df with vector and meta data and turn it into a json file.
def get_completed_df(json_path,csv_path, song_path):

    json_metadata_df = get_json_metadata_df(json_path)
    csv_metadata_df = get_csv_metadata(csv_path,words_to_remove)
    complete_metadata_df = pd.concat([json_metadata_df, csv_metadata_df], ignore_index=True)

    base_path = Path(song_path)
    subgenre_folders = [x for x in base_path.iterdir() if x.is_dir()]

    for folder in subgenre_folders:
        process_subgenre_folder(folder, complete_metadata_df.copy())

#if you want to run get_completed_df, put this before calling the function:
#if __name__ == '__main__':
    #get_completed_df(json_path,csv_path, song_path)
