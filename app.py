import pandas as pd
from data_extraction.audio_embedding import embed_song
from user_features.similarity_search import search_similar
import gradio as gr
from user_features.song_summarization import get_fun_fact, get_mood_fact
from user_features.mood_classification import characteristic_predict
from user_features.spotify_service import get_spotify_preview_url , search_spotify_song
import json
from config import getSpotifyToken
from user_features.spotify_service import create_spotify_playlist, add_tracks_to_playlist

model_path = 'data/NN_mood_prediction_feature.h5'


js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

global_track_ids = []
global_song_name = []
global_artist_name =[]

def process_song_spotify(song_name, artist_name):
    global global_track_ids, global_song_name,global_artist_name

    track_id, preview_url, track_name, artist_names, album_name = search_spotify_song(song_name, artist_name)
    global_song_name, global_artist_name = track_name,artist_name

    if not track_id:
        return "Song not found on Spotify"
    
    mp3 = embed_song(preview_url)
    if not mp3:
        return "Failed to embed song."
    
    result = search_similar(mp3)
    if result.empty:
        return "No similar songs found."
    
    result = result.drop_duplicates(subset=['track_id'])
    global_track_ids = result['track_id'].tolist()
    
    result = result.iloc[1:6]
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
        fun_fact_data = get_fun_fact(artist_names,album_name,track_name)
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
        <strong style='color: #333;'>Song Fact:</strong> {fun_fact}
    </div>
    """
    # Generate the HTML for the audio player along with the song details

    audio_player_html = f"""
    <style>
        .now-playing-table {{
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }}
        .now-playing-table th {{
            background-color: #e4a6ed;
            color: #fff;
            padding: 10px 8px;
            text-align: left;
        }}
        .now-playing-table td {{
            padding: 10px 8px;
            text-align: left;
            vertical-align: middle;
            border-bottom: 1px solid #ddd;
        }}
        .now-playing-table td:nth-child(2) {{
            width: 250px; /* Adjust the width as necessary */
        }}
        .now-playing-table audio {{
            width: 100%;
            max-width: 400px; /* Adjust the max-width to match your player's size */
        }}
    </style>

    <table class='now-playing-table'>
        <tr>
            <th>Now Playing</th>
            <th>Audio Player</th>
        </tr>
        <tr>
            <td>{track_name} by {artist_names}</td>
            <td><audio controls src='{preview_url}'></audio></td>
        </tr>
    </table>
    """

    return audio_player_html + styled_html_result + html_fun_fact

def create_playlist():
    global global_track_ids,global_song_name,global_artist_name

    if not global_track_ids:
        return "No tracks available to add to a playlist."

    user_token = getSpotifyToken()
    print(user_token)
    playlist_response = create_spotify_playlist(user_token,global_song_name,global_artist_name)

    playlist_id = playlist_response.get("id")

    if playlist_id:
        add_tracks_response = add_tracks_to_playlist(user_token, playlist_id, global_track_ids)
        global_track_ids = []
        return f"Playlist created successfully! ID: {playlist_id}"
    else:
        return "Could not create playlist."


def process_song(uploaded_file_path):

    mp3 = embed_song(uploaded_file_path)
    result = search_similar(mp3)

    print(result)
    
    result = result.drop_duplicates(subset=['track_id'])
    result = result.iloc[1:6]
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
    

    fun_fact = "Sorry, this function only works with Spotify Search!"

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
    <h2 style="text-align: center; color: #080206; margin-top: 20px;">Our Songs Recommendation</h2>
    {html_result}
    """
    html_fun_fact = f"""
    <div style='margin-top: 20px; padding: 15px; background-color: #7ef7bb; border-left: 5px solid #2a9d8f; font-family: Arial, sans-serif; font-size: 16px; color: #333; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);'>
        <strong style='color: #333;'>Mood Analysis:</strong> <span>{mood_string}</span>{mood_fact}<br>
    </div>
    <div style='margin-top: 20px; padding: 15px; background-color: #7ef7bb; border-left: 5px solid #e76f51; font-family: Arial, sans-serif; font-size: 16px; color: #333; border-radius: 8px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);'>
        <strong style='color: #333;'>Song Fact:</strong> {fun_fact}
    </div>
    """
    return styled_html_result + html_fun_fact


with gr.Blocks(js=js_func) as demo:
    gr.Markdown("# Welcome to Databae's Audio Platform.")
    gr.Markdown("Use a song you like to find similar songs based on its Characteristics. Discover Song Fact and Mood Prediction of your tracks!!")
    
    with gr.Row():
        file_input = gr.File(label="Upload MP3 File", type="filepath",scale=2)
        song_input = gr.Textbox(label="Song Name")
        artist_input = gr.Textbox(label="Artist Name")
    with gr.Row():
        mp3_submit_button = gr.Button("Submit MP3",scale=2)
        spotify_submit_button = gr.Button("Search on Spotify",scale=2)

    output = gr.HTML()

    mp3_submit_button.click(process_song, inputs=file_input, outputs=output)
    
    #output_spotify = gr.HTML()
    spotify_submit_button.click(process_song_spotify, inputs=[song_input, artist_input], outputs=output)
    
    with gr.Row():
        create_playlist_button = gr.Button("Create Spotify Playlist")
        playlist_output = gr.HTML()

    create_playlist_button.click(
        create_playlist,
        inputs=[],
        outputs=playlist_output)
    
# Apply queue settings to manage load effectively
demo.queue(default_concurrency_limit=5)  # Adjust based on your needs and resources

# Launch the application with a specific number of workers
demo.launch(share=True)