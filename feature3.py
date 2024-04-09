from openai import OpenAI

import config


def get_fun_fact(Artist, Album, songname):

    apikey = config.getAPIkey()
    client = OpenAI(api_key=apikey)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"Can you tell me a fact for {Artist} song {songname} from the album {Album}?"}
        ]
    )
    fact= response.choices[0].message.content
    return fact