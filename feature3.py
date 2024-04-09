from openai import OpenAI

def get_fun_fact(Artist, Album, songname):
    client = OpenAI(api_key="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")

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