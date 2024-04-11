from openai import OpenAI

import config
import json

def get_fun_fact(Artist, Album, songname):

    apikey = config.getOpenAIKey()
    client = OpenAI(api_key=apikey)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an AI assistant in an audio recommendation platform. You should act really cool and funny. \
             This platform receives mp3 song and recommend similar song. You are a music expert designed to give really cool and fun fact about song. \
             Respond with a JSON object that contains only one field, 'fun_fact'. "},
            {"role": "user", "content": f"Can you tell me a fun or interesting fact for {Artist} song {songname} from the album {Album}?"}
        ]
    )
    fact= response.choices[0].message.content
    return fact