# IN PROGRESS .............................

# Music App
Recommender platform for Music you like


## Setup

#### Repository steps

1) Git Clone the master branch :  git@github.com:amrutahabbu/dataBAEs_musicapp.git
2) Create a new feature branch from main. 
3) Checkout the newly created branch . Make sure its in sync with the main.
4) Setup python environment (new_requirement.txt)

#### Information about files

#### ETL
1) loadData.py -> Loads data from local to AWS s3
2) retrieveData -> Retrieves data from AWS s3
3) mp3_to_vector -> create Embeddings
4) create_input_for_datastax -> json for datastax

#### Application 
1) app.py - Entry point for user similarity search
2) 
