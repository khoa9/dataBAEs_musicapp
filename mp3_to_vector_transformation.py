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
    with concurrent.futures.ThreadPoolExecutor() as executor:
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
def get_metadata_df(json_path):
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
    
    return metadata_df


# Create function to get completed df with vector and meta data
def get_completed_df(json_path, song_path):
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
    
    # Create metadata_df and join with vector_idf for a completed df
    metadata_df = get_metadata_df(json_path)
    completed_df = pd.merge(metadata_df, vector_df, on="track_id", how='inner')

    return completed_df

#End this with dataframe

