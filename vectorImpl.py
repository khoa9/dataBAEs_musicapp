#pip install --upgrade astrapy
# Added for testing
import json
from astrapy.db import AstraDB

# Initialize the client
db = AstraDB(
  token="AstraCS:jntLCTXPzPfOtuOHhOvAOMPG:96e7192bc774ff3dce939307108a8eec19ca972820b0095e2a53beffe73b1036",
  api_endpoint="https://769d9e28-d2b7-45e7-9af8-0cabca7e3657-us-east-1.apps.astra.datastax.com")

print(f"Connected to Astra DB: {db.get_collections()}")

# Create a collection. The default similarity metric is "cosine".
collection = db.create_collection("music_vector2", dimension=5, metric="cosine")
print(collection)


file_path = "./data/input_datastax/music_vector_metadata.json"
# Insert documents into the collection

with open(file_path, 'r') as file:
    # Load the JSON data from the file
    documents = json.load(file)

#Add the collection to datastax
res = collection.insert_many(documents)
print(res)


#inputsong vector - User input - Testing
input_song_vector = [[0.15, 0.1, 0.1, 0.35, 0.55],[0.15, 0.1, 0.1, 0.35, 0.55]]
results = collection.vector_find(input_song_vector, limit=15, fields={"text", "$vector"})

for document in results:
    print(document)
