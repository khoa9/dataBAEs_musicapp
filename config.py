## ALL THE CONFIGURATIONS GO HERE

import os
from sqlalchemy import *
from astrapy.db import AstraDB


#parameters for local database BOOK
db_username = 'root'
db_password = 'Admin123'
#db_host = 'recommendation-3.c8scn1wkslmg.us-east-2.rds.amazonaws.com'
db_host = 'localhost'
#db_host = 'arcresdb.rs.gsu.edu'
db_port = '3306'
#db_name = 'rspm'
#db_name = 'rspmdev'
db_name = 'rspm_book_prod_new'


# Create the database URL in the format required by SQLAlchemy
DB_URI = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

def connect_AstraDB():
    # Initialize the client
    db = AstraDB(
        token="AstraCS:cJRHkPPfbcQCaJFKxnFjJoUE:d0eb7d0643c1255dd583daac12a86710650813c6f97f407b42399746d77be7a4",
        api_endpoint="https://be61fb62-4f40-45db-8cd0-14c061a597ff-us-east-1.apps.astra.datastax.com")

    print("Connected to Astra DB")
    return db