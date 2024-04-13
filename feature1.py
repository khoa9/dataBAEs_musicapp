#Feature1 is the similarity search
# Added for testing
import json
from astrapy.db import AstraDB

import config
import pandas as pd


def search_similar(input_song_vector):
 # Initialize the client
  db = config.connect_AstraDB()



  #get_collections gives a dictionary of collection names
  collections = db.get_collections()
  collection_name = collections['status']['collections'][0]    #using 0 as we will have only 1 collection as of now.


  #Extracting from AstraDB - the collection object
  music_collection_object = db.collection(collection_name)
  similar_songs = music_collection_object.vector_find(input_song_vector, limit=5,fields={"track_id","name","album","artist", "genre" })
  similar_songs_df = pd.DataFrame(similar_songs)
  return similar_songs_df
