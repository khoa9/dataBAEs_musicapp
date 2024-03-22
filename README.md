# flask-movietweetings
Recommender platform for research


## Setup

#### Repository steps

1) Git Clone the master branch :  https://github.com/arctic-gsu/RSPM/tree/master
2) Create a new development branch from master 
3) Checkout the newly created branch . Make sure its in sync with the master.
4) Setup python environment (flask folder has needed libraries)

#### Sql

1) Create a Mysql Database on local
2) Use any client e.g. MySQLClient
3) Create an empty schema with default characterset as UTF-8


#### Changes in files (on your branch)
1) Config.py - Point the application to correct database (new schema created)
2) Model.py - In main()

            a. Uncomment create_tables() and run it. 
                - Check if the tables are created in the schema. 
                - Drop table userrating (This will get created during application run)
                - Disconnect rating table from foreign key constraints
            b. Comment create_tables and uncomment Movie data part to load movies - Run the model.py
            c. Comment Movie_data and uncomment  Ratings part - run model.py
            e. Comment Ratings part and uncomment items update - run model.py
            f. Comment items and uncomment current_algo . Run model.py

This should have our code and the tables ready. 