from astrapy.db import AstraDB
import numpy as np
import pandas as pd
from mp3_to_vector_transformation import create_pipeline, embed_song
from feature1 import search_similar
import gradio as gr
from gradio import themes
from feature3 import get_fun_fact, get_mood_fact
from feature2 import characteristic_predict
import tensorflow as tf
from spotify_get_url import get_spotify_preview_url
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import json

model_path = '/Users/bach/Documents/MP3-Project/MP3_Project_Git/dataBAEs_musicapp/my_model_weighted.h5'


logging.basicConfig(filename='/data/gradio.log', level=logging.INFO)
js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

def process_song(uploaded_file_path):
    filename = os.path.splitext(os.path.basename(uploaded_file_path))[0]
    audio = MP3(uploaded_file_path, ID3=EasyID3)
    # Fetching artist, album, and title information
    artist = audio.get('artist', ['Unknown Artist'])[0]
    album = audio.get('album', ['Unknown Album'])[0]
    title = audio.get('title', ['Unknown Title'])[0]

    mp3 = embed_song(uploaded_file_path)
    result = search_similar(mp3)

    print(result)
    
    result = result.drop_duplicates(subset=['track_id'])
    result = result.iloc[:5]
    result['preview_url'] = result['track_id'].apply(get_spotify_preview_url)

    # Generate the HTML for the audio players
    def audio_player_html(row):
        if pd.notna(row['preview_url']):
            return f"<audio controls src='{row['preview_url']}'></audio>"
        return "No preview available"
    
    result['audio_player'] = result.apply(audio_player_html, axis=1)
    result = result.drop(columns=['_id','track_id','$similarity','preview_url'])

    mood_prediction = characteristic_predict(mp3, model_path)
    styled_mood_predictions = ['<b style="color: #c305ed;">' + mood + '</b>' for mood in mood_prediction]
    mood_string = '<span style="color: black;">This song gives </span>' + '<span style="color: black;">, </span>'.join(styled_mood_predictions) + '<span style="color: black;"> mood. </span>'
    
    try:
        fun_fact_data = get_fun_fact(artist,album,filename)
        fun_fact_dict = json.loads(fun_fact_data)
        if 'fun_fact' in fun_fact_dict:
            fun_fact = fun_fact_dict['fun_fact']
        else:
            fun_fact = "No fun fact available for this song."
    except json.JSONDecodeError:
        fun_fact = "Error in decoding fun fact data."
    except Exception as e:
        print("Error fetching fun fact:", str(e))
        fun_fact = "Put more money in! You probably don't have the API key. Error"

    try:
        mood_fact_data = get_mood_fact(mood_prediction)
        mood_fact_dict = json.loads(mood_fact_data)
        if 'mood_fact' in mood_fact_dict:
            mood_fact = mood_fact_dict['mood_fact']
        else:
            mood_fact = "No mood fact available for this mood."
    except json.JSONDecodeError:
        mood_fact = "Error in decoding mood fact data."
    except Exception as e:
        print("Error fetching mood fact:", str(e))
        mood_fact = "I'm not in the mood to give you a mood fact. You haven't put the OPEN API KEy. Error!"

    html_result = result.to_html(escape=False, classes="data", index=False)
    styled_html_result = f"""
    <style>
        .data {{
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }}
        .data th {{
            background-color: #e4a6ed; /* Dark background for the header */
            color: #080206; /* White text for visibility */
            padding: 8px;
            text-align: left;
        }}
    </style>
    {html_result}
    """
    html_fun_fact = f"""
    <div style='margin-top: 20px; padding: 15px; background-color: #7ef7bb; border-left: 5px solid #2a9d8f; font-family: Arial, sans-serif; font-size: 16px; color: #333; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);'>
        <strong style='color: #333;'>Mood Analysis:</strong> <span>{mood_string}</span>{mood_fact}<br>
    </div>
    <div style='margin-top: 20px; padding: 15px; background-color: #7ef7bb; border-left: 5px solid #e76f51; font-family: Arial, sans-serif; font-size: 16px; color: #333; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);'>
        <strong style='color: #333;'>Fun Fact:</strong> {fun_fact}
    </div>
    """

    return styled_html_result + html_fun_fact


with gr.Blocks(js=js_func) as demo:
    gr.Markdown("# Welcome to Databae's Audio Platform.")
    gr.Markdown("Upload an MP3 file to find similar songs. Discover fun facts and mood prediction of your tracks!!")
    
    with gr.Row():
        file_input = gr.File(label="Upload MP3 File", type="filepath")
        submit_button = gr.Button("Submit")
    
    output = gr.HTML()
    
    submit_button.click(process_song, inputs=file_input, outputs=output)

# Apply queue settings to manage load effectively
demo.queue(default_concurrency_limit=4)  # Adjust based on your needs and resources

# Launch the application with a specific number of workers
demo.launch(share=True)