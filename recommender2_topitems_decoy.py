

from __future__ import (absolute_import, division, print_function, unicode_literals)

#import algorithms from surprise


import numpy as np
import pandas as pd
from sqlalchemy import create_engine
np.random.seed(101)
from collections import defaultdict
import os, io, sys
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import config
# from model import add_pageview
import model
import time

# disable print


def compute_recommendations(user_id, recommendations1, transposed_prediction1):

    # numeric_prediction_table=0
    #connecting to the database
    # engine = create_engine("mysql://root:sesame@localhost/ratingsx?charset=utf8", echo=True)
    engine = create_engine(config.DB_URI, echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

    algo = 'top items'

    model.delete_transposed_prediction1(user_id)
    model.delete_numeric_predictions1(user_id)

    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Initialize Predictions - " + algo, rating=None) #pageview


    #reading in the database


    top_decoy = pd.read_csv('./data/predictions/top_decoy.csv',low_memory=False)
    predictions = top_decoy[['user_id', 'item_id', 'prediction']].copy()

    test_prediction = predictions

    cols = ['pred_1', 'pred_2', 'pred_3', 'pred_4',
            'pred_5', 'pred_6', 'pred_7', 'pred_8',
            'pred_9', 'pred_10']

    df_pred = predictions[['item_id']].T

    df_pred.columns = cols

    df_pred['id'] = user_id

    df_pred = df_pred[['id', 'pred_1', 'pred_2', 'pred_3', 'pred_4',
                       'pred_5', 'pred_6', 'pred_7', 'pred_8',
                       'pred_9', 'pred_10']]

    df_pred['id'] = df_pred['id'].astype(int)

    print('#' * 1000, 'writing to recommendations1 Table\n')

    df_pred.to_sql(recommendations1, engine, if_exists='append', index=False)
    session.commit()

    predictions_top20 = test_prediction.head(n=20)
    predictions_top20['algorithm'] = algo

    predictions_top20.rename(columns={'prediction':'predicted_rating'}, inplace=True)

    predictions_top20.to_sql('numeric_predictions', engine, if_exists='append', index=False)
    session.commit()



    predcols = ['num_1', 'num_2', 'num_3', 'num_4',
                'num_5', 'num_6', 'num_7', 'num_8',
                'num_9', 'num_10']

    df_num_ratings_transpose = predictions[['prediction']].T
    df_num_ratings_transpose.columns = predcols

    df_num_ratings_transpose['id'] = user_id

    df_num_ratings_transpose = df_num_ratings_transpose[['id', 'num_1', 'num_2', 'num_3', 'num_4',
                                                         'num_5', 'num_6', 'num_7', 'num_8',
                                                         'num_9', 'num_10']]

    df_num_ratings_transpose['id'] = df_num_ratings_transpose['id'].astype(int)

    df_num_ratings_transpose.to_sql(transposed_prediction1, engine, if_exists='append',index=False)
    session.commit()

