## ALL THE CONFIGURATIONS GO HERE

from astrapy.db import AstraDB

def connect_AstraDB():
    # Initialize the client
    db = AstraDB(
        token="##",
        api_endpoint="##")

    print("Connected to Astra DB")
    return db

def getOpenAIKey():

    api_key = "##"
    return api_key

def getSpotifyToken():
    
    user_token = "##"
    return user_token
