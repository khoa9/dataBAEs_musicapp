##THIS FILE IS FOR THE ENTIRE FLOW FROM USER END
## AT THE END THIS WILL BE INTEGRATED WITH UI

import feature1
import pandas as pd



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
