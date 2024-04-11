# This is test for Dang's branch
###THIS FILE IS FOR THE ENTIRE FLOW FROM USER END
## AT THE END THIS WILL BE INTEGRATED WITH UI
import json

import feature1
import pandas as pd

from feature3 import get_fun_fact

#from mp3_to_vector_transformation import embed_song, create_pipeline


'''def convert_input_to_vector():
    #Change this and test with an mp3 - Amruta
    p = create_pipeline()
    embed_song(p,)

with open('data/input_song_file', 'r') as file:
    # Read the contents of the file
    input_song_vector = file.read()
#before feature 1
# have an input song from user in mp3 format, stored in application
# convert this song into a vector. To do this:
# call a pipeline creation, reaturn p  (create_pipeline)
# call embedded fucntion, pass the p (check this)


#print(input_song_vector)
similar_songs = feature1.search_similar(input_song_vector)
pd.set_option('display.max_columns', None)
print(similar_songs.head(15))
'''


response_from_openai = get_fun_fact("Shahrukh Khan","Dil Se","Chaiyyan Chaiyyan")
response_to_json = json.loads(response_from_openai)
fact = response_to_json['fact']
print(fact)