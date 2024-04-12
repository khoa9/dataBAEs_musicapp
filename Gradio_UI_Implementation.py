from astrapy.db import AstraDB
import numpy as np
import pandas as pd
from mp3_to_vector_transformation import create_pipeline, embed_song
from feature1 import search_similar
import gradio as gr
from feature3 import get_fun_fact, get_mood_fact
from feature2 import characteristic_predict
import tensorflow as tf
import pickle


model_path = '/Users/bach/Documents/MP3-Project/MP3_Project_Git/dataBAEs_musicapp/my_model_weighted.h5'


"""song_path = "/Users/bach/Documents/MP3-Project/MP3_Project_Git/test_data/04. Get Into It (Yuh).mp3"

mp3 = embed_song(song_path)
result = search_similar(mp3)
result = result.drop(columns=['_id','track_id'])
#artist,album,name = result[0],result[1],result[2]
artist = result['artist'].loc[result.index[0]]
album = result['album'].loc[result.index[0]]
name = result['name'].loc[result.index[0]]

print(result)

model_path = '/Users/bach/Documents/MP3-Project/MP3_Project_Git/dataBAEs_musicapp/my_model_weighted.h5'
print(characteristic_predict(mp3, model_path))"""



'''
from pydub import AudioSegment
from astrapy.db import AstraDB
import numpy as np
import config
import pandas as pd
from mp3_to_vector_transformation import create_pipeline, embed_song
from feature1 import search_similar
import gradio as gr

# Function to trim the song
def trim_song(song_path, start_min, start_sec, end_min, end_sec):
    # Load the song
    song = AudioSegment.from_mp3(song_path)

    # Calculate start and end times in milliseconds
    start_time = (start_min * 60 + start_sec) * 1000
    end_time = (end_min * 60 + end_sec) * 1000

    # Trim the song to the desired snippet
    snippet = song[start_time:end_time]

    # Return the audio segment
    return snippet

# Path to your original song
song_path = "/Users/bach/Downloads/DEAN - Howlin' 404 [L2SHARE]/01. Howlin' 404.mp3"
# Trim the song to a 30-second snippet from 1 minute to 1:30
snippet = trim_song(song_path, 1, 0, 1, 30)

# Save the snippet temporarily (assuming you're doing this for processing)
snippet_path = "/tmp/snippetk_pop.mp3"  # Using a temporary file
snippet.export(snippet_path, format="mp3")

# Now, use the snippet for the rest of your process
mp3 = embed_song(snippet_path)
result = search_similar(mp3)
result = result.drop(columns=['_id', 'album', 'genre'])

print(result)'''

import gradio as gr
import json  # Import the json module


def process_song(uploaded_file_path):
    mp3 = embed_song(uploaded_file_path)
    result = search_similar(mp3)
    result = result.drop(columns=['_id','$similarity'])
    artist = result['artist'].iloc[0]
    album = result['album'].iloc[0]
    name = result['name'].iloc[0]
    mood_prediction = characteristic_predict(mp3, model_path)
    mood_string = "This song gives a " + ", ".join(mood_prediction) + " mood."

    try:
        # Fetch the fun fact
        fun_fact_data = get_fun_fact(artist, album, name)
        # Convert JSON string to dictionary
        fun_fact_dict = json.loads(fun_fact_data)  # This will convert the JSON string to a Python dictionary

        # Check if 'fun_fact' key exists in the dictionary
        if 'fun_fact' in fun_fact_dict:
            fun_fact = fun_fact_dict['fun_fact']
        else:
            fun_fact = "No fun fact available for this song."
    except json.JSONDecodeError:
        fun_fact = "Error in decoding fun fact data."
    except Exception as e:
        print("Error fetching fun fact:", str(e))
        fun_fact = "Could not retrieve fun fact due to an error."

    try:
        # Fetch the fun fact
        mood_fact_data = get_mood_fact(mood_prediction)
        # Convert JSON string to dictionary
        mood_fact_dict = json.loads(mood_fact_data)  # This will convert the JSON string to a Python dictionary

        # Check if 'fun_fact' key exists in the dictionary
        if 'mood_fact' in mood_fact_dict:
            mood_fact = mood_fact_dict['mood_fact']
        else:
            fun_fact = "No mood fact available for this song."
    except json.JSONDecodeError:
        fun_fact = "Error in decoding fun fact data."
    except Exception as e:
        print("Error fetching mood fact:", str(e))
        fun_fact = "Could not retrieve mood fact due to an error."

    # Prepare HTML output with both song details and fun fact
    html_result = result.to_html(escape=False)
    html_fun_fact = f"""
    <div style='
        margin-top: 20px; 
        padding: 15px;
        background-color: #f4f4f9; 
        border-left: 5px solid #2a9d8f;
        font-family: Arial, sans-serif; 
        font-size: 16px;
        color: #333; /* This is the text color */
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    '>
        <strong style='color: #333;'>Mood:</strong> {mood_string}.{mood_fact}<br>
        <strong style='color: #333;'>Fun Fact:</strong> {fun_fact}
    </div>
    """
    
    return html_result + html_fun_fact

# Define your Gradio interface
iface = gr.Interface(
    fn=process_song,
    inputs=gr.File(label="Upload MP3 File", type="filepath"),
    outputs="html",
    title="Find Similar Songs",
    description="Upload an MP3 file to find similar songs. Discover fun facts about similar tracks!",
    thumbnail="https://cdn-icons-png.flaticon.com/512/9850/9850812.png"  # Add your logo URL here

)

# Run the Gradio app
iface.launch()

