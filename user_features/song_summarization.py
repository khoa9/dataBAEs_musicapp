from openai import OpenAI

import config
import json

def get_fun_fact(Artist, Album, songname):
    client = OpenAI(api_key=config.getOpenAIKey())

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an AI assistant in an audio recommendation platform. You should act really cool and funny. \
             This platform receives mp3 song and recommend similar song. You are a music expert designed to give really cool and fun fact about song. Provide at least two sentences \
             Respond with a JSON object that contains only one field, 'fun_fact'. Don't include the word, Fun fact:, before the actual sentence "},
            {"role": "user", "content": f"Can you tell me a fun or interesting fact for {Artist} song {songname} from the album {Album}?"}
        ]
    )
    fact= response.choices[0].message.content
    return fact

def get_mood_fact(mood):
    client = OpenAI(api_key=config.getOpenAIKey())

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an AI assistant in an audio recommendation platform. You should act really cool and funny. \
             This platform receives mp3 song and recommend similar song, predict its mood, and givea fun fact. You are a music expert designed to say fun thing about the mood of the song. \
             Respond with a JSON object that contains only one field, 'mood_fact'. Don't include the word, Mood fact:, before the actual sentence "},
            {"role": "user", "content": f"This person is listening to a song that has a {mood}. Say something funny about that."}
        ]
    )
    fact= response.choices[0].message.content
    return fact