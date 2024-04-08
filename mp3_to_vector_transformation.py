#Dang ML

# Install these packages in the terminal to run this code
# %pip install -q towhee towhee.models gradio ipython

import os
import pandas as pd
import numpy as np
import concurrent.futures


import IPython
import gradio
import glob

import towhee
from towhee import pipe, ops
from towhee.datacollection import DataCollection

# Define towhee pipeline - VGGish for audio embedding
p = (
      pipe.input('path')
          .map('path', 'frame', ops.audio_decode.ffmpeg())
          .map('frame', 'vecs', ops.audio_embedding.vggish())
          .output('vecs')
)

# Create function to have a list of embedded audio song
def embed_song(p, song_path, song):
    full_path = os.path.join(song_path, song)
    song_vector = p(full_path).get()[0]
    flat_song_vector = np.mean(song_vector, axis=0)
    return flat_song_vector

def vector_embedding(song_path, p):
    """
    Create a list of song name in the song_path then create a loop to embed each of them into a vector and 
    return a list of embedded vector
    
    Parameters:
    - song_path: local path that contain song after retreiving from S3 bucket
    - p: towhee pipeline with VGGish as the embedding layer
    """
    # Create a list of song name in the path
    songs = os.listdir(song_path)

    # Use ThreadPoolExecutor for parallelization
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit tasks to executor for each song
        futures = [executor.submit(embed_song, p, song_path, song) for song in songs]
        
        # Retrieve results as they become available
        vectors = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    return vectors

# Create function get_metadata
def get_metadata(x):
    cols = ['artist', 'genre', 'name', 'album']
    list_of_cols = []
    for col in cols:
        try:
            mdata = list(x[col].values())[0]
        except:
            mdata = "Unknown"
        list_of_cols.append(mdata)

    return pd.Series(list_of_cols, index=cols)


# Create function to get metadata from json file as the dataframe 
def get_json_metadata_df(json_path):
    """
    Create a dataframe containing track ID and columns in the get_metadata functions from the label.json file
    
    Parameters:
    - json_path: local path that contain labels.json file
    """
    # Read json from the json_path
    metadata = pd.read_json(json_path)
    
    # Apply get_metadata function to get the required meta data
    metadata_df = metadata['tracks'].apply(get_metadata).reset_index()
    metadata_df = metadata_df.rename(columns={"index":"track_id"})
    # Add a new 'Characteristic' column and leave it blank (using NaN or empty string as placeholder)
    metadata_df['characteristic'] = np.nan  # Use np.nan for missing values or '' for an empty string
    
    return metadata_df

# Define a function to clean the characteristics column in the CSV metadata.
def clean_characteristics(characteristic, words_to_remove):
    """
    Cleans up the 'characteristic' column by removing unwanted words.
    
    Parameters:
    - characteristic: The raw characteristic string from the CSV file.
    - words_to_remove: A set of words to be removed from each characteristic string.

    Returns:
    - A cleaned-up characteristic string with unwanted words removed.
    """
    # Check for NaN and return an empty string if found.
    if pd.isna(characteristic):
        return ""
    # Split the characteristic string into individual words.
    words = [word.strip() for word in characteristic.split(',')]
    # Remove any unwanted words.
    cleaned_words = [word for word in words if word not in words_to_remove and word != ""]
    # Reassemble the cleaned words into a string.
    return ', '.join(cleaned_words)

# Define a function to read and clean CSV metadata.
def get_csv_metadata(csv_path):
    """
    Reads and cleans metadata from a CSV file.

    Parameters:
    - csv_file_path: The file path to the CSV file containing metadata.

    Returns:
    - A pandas DataFrame containing cleaned track metadata.
    """
    # Define the columns to read from the CSV file.
    columns_to_read = ['Track ID', 'Album Name', 'Genre', 'Track Name', 'Artists', 'Characteristics']

    # Set up a renaming map to standardize column names.
    column_rename_map = {
        'Track ID': 'track_id',
        'Album Name': 'album',
        'Genre': 'genre',
        'Track Name': 'name',
        'Artists': 'artist',
        'Characteristics': 'characteristic'
    }

    # Define words to be removed from the 'characteristic' column.
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

    # Load the CSV file, filtering for specified columns and applying the renaming map.
    df = pd.read_csv(csv_path, usecols=columns_to_read, encoding='utf-8-sig')
    df.rename(columns=column_rename_map, inplace=True)

    # Clean the 'characteristic' column by applying the clean_characteristics function.
    df['characteristic'] = df['characteristic'].apply(lambda x: clean_characteristics(x, words_to_remove))

    return df



# Create function to get completed df with vector and meta data
def get_completed_df(json_path,csv_path, song_path):
    """
    Create a complete data frame containing meta data from labels.json file and embedded vector 
    
    Parameters:
    - json_path: local path that contain labels.json file
    - song_path: local path that contain song (mp3)
    """
    # Create a list of track ID
    songs_id = os.listdir(song_path)
    
    # Creare list of vector from the vector_embedding function
    vectors = vector_embedding(song_path)
    
    # Create a vector_df
    id = [song[:-4] for song in songs_id]
    vector_df = pd.DataFrame({'track_id':id, "vector": vectors})
    
    # Create consolidated metadata_df and join with vector_idf for a completed df
    json_metadata_df = get_json_metadata_df(json_path)
    csv_metadata_df = get_csv_metadata(csv_path)
    complete_metadata_df = pd.concat([json_metadata_df, csv_metadata_df], axis=0, ignore_index=True)

    completed_df = pd.merge(complete_metadata_df, vector_df, on="track_id", how='inner')

    return completed_df

#End this with dataframe

