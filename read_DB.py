import config
from sqlalchemy.ext.declarative import declarative_base
import os
os.getcwd()
#
# def auto_truncate_description(val):
#     return val[:1024]
# def auto_truncate_title(val):
#     return val[:255]
#

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import numpy as np
import pandas as pd
import datetime

#
# def auto_truncate_description(val):
#     return val[:1024]
# def auto_truncate_title(val):
#     return val[:255]
#

engine = create_engine(config.DB_URI, echo=False)


# engine = create_engine(config.DB_URI, echo=False)

session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

###############################################################
###############################################################

################### checkout tables ###################
pd.set_option('display.max_columns', None)
tables = pd.read_sql('show tables', con=engine)
print(tables)


# current_algo = pd.read_sql('select * from Current_algo', con=engine)

algo = pd.read_sql('select * from algo', con=engine)
algo.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/algo.csv')
# print(algo.head())

userchoice = pd.read_sql('select * from userchoice', con=engine)
userchoice.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/userchoice.csv')


users_info = pd.read_sql('select * from users_info', con=engine)
users_info.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/users_info.csv')


feedback = pd.read_sql('select * from feedback', con=engine)
feedback.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/feedback.cs')


algo_choice = algo.merge(userchoice, on='user_id')
algo_choice.to_csv('E:/Research/Research Ideas/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/algo_choice.csv')

predictions = pd.read_sql('select * from prediction_personalized', con=engine)
predictions.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/predictions.csv')


prediction_top = pd.read_sql('select * from prediction_top', con=engine)
prediction_top.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/prediction_top.csv')



transposed_prediction =  pd.read_sql('select * from transposed_prediction1', con=engine)
transposed_prediction.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/transposed_prediction.csv')

###merge feedback and choice
import pandas as pd

feedback = pd.read_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/feedback.csv')
choice = pd.read_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/userchoice.csv')
users_info = pd.read_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/users_info.csv')

merged = choice.merge(feedback, on="user_id")

merged.head()

all_data = merged.merge(users_info, on="user_id")

all_data.to_csv('E:/Research/Research Papers/5- Rec-Ad/Lab Experiemnt/Second Experiment/data/all_data.csv')