# from __future__ import absolute_import, division, print_function, unicode_literals
import os
import model
os.getcwd()
# from surprise import evaluate, print_perf, dump, Reader, Dataset
#import algorithms from surprise
from surprise import Dataset
from surprise import Reader
from surprise import accuracy
# from surprise import evaluate
# from surprise import print_perf

#from surprise import Reader, Dataset, accuracy, evaluate, print_perf

# from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, AlgoBase, SlopeOne, CoClustering, NormalPredictor,NMF, SVD, BaselineOnly

import time
start_time = time.time()

from surprise import SVD
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
# from surprise import dump
# from model import add_pageview

# algorithm = SVD(biased=False,n_epochs=10,lr_all=0.005,reg_all=0.6)
# def compute_recommendations_to_csv(user_id):
#
#     ################################### Resume & Add Inferior #########################################
#     predictions_w_item_info = pd.read_csv('./data/predictions/svd_predictions_w_item_info.csv')
#
#
#     print('*' * 100, '\n')
#     # print("items_full:\n\n\n", items_full.head())
#     print("predictions (augmented) before adding inferior:\n\n\n", predictions_w_item_info.head())
#
#     ## Find the top item
#     top_item = predictions_w_item_info.loc[0, 'item_id']
#     top_item_genres = predictions_w_item_info.loc[0, 'genres']
#     #top_item_main_genre = top_item_genres.split(",")[0]
#
#     ## Find the inferior item
#     inferior_item_index = None
#     genres = None
#     #main_genre = None
#     for i in reversed(predictions_w_item_info.index):
#         genres = predictions_w_item_info.loc[i, "genres"]
#         #main_genre = genres.split(",")[0]
#         if genres == top_item_genres:
#             inferior_item_index = i
#             # print("inferior_item_genres:", genres)
#             # print("inferior_item_main_genre:", main_genre)
#             # print("inferior_item_index:", inferior_item_index)
#             # print("inferior_item_title:", predictions_w_item_info.loc[i, "title"])
#             break
#
#         ## Swap the inferior item with the second item
#         # print("predictions.loc[1] =",predictions.loc[1])
#     print("Inferior item added: ", predictions_w_item_info.loc[inferior_item_index])
#     print("Min Prediction Score: ", min(predictions_w_item_info['prediction']))
#
#     predictions_w_item_info.iloc[1] = predictions_w_item_info.loc[inferior_item_index]
#     print("**** 1- predictions with inferior item:\n\n\n", predictions_w_item_info)
#
#     # No other item allowed in the same genre as the top item or decoy
#     top_two = predictions_w_item_info.iloc[0:2, :].copy()
#     print("**** top two:\n\n\n", top_two)
#
#     all_else_clean = predictions_w_item_info[predictions_w_item_info['genres'] != top_item_genres]
#     print("**** all_else_clean:\n\n\n", all_else_clean)
#
#     predictions = top_two.append(all_else_clean)
#
#     predictions = predictions[['user_id', 'item_id', 'prediction']]
#
#
#     ## Print the result
#     print("**** predictions with inferior item:\n\n\n", predictions)
#     ################################  End  #################################
#
#
#     ## Round & Normalize prediction values
#     predictions['prediction'] = predictions['prediction']/predictions['prediction'].max()*10
#     predictions['prediction'] = predictions['prediction'].round(1)
#     predictions = predictions.head(n=10)
#
#
#     output_path = './data/predictions/svd_decoy_predictions.csv'
#     predictions.to_csv(output_path, index=0)
#     print(f'prediction saved at {output_path}')
#


def compute_recommendations(user_id, recommendations1, transposed_prediction1):

    algo = 'SVD'

    algorithm = SVD()

    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Initialize Predictions - " + algo, rating=None) #pageview

    engine = create_engine(config.DB_URI, echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))


    model.delete_recommendations1(user_id)
    model.delete_transposed_prediction1(user_id)
    model.delete_numeric_predictions1(user_id)


    #reading in the database


    svd_decoy_predictions = pd.read_csv('./data/predictions/svd_ad_predictions.csv',low_memory=False)
    predictions = svd_decoy_predictions[['user_id', 'item_id', 'prediction']].copy()



    test_prediction = predictions


    cols =['pred_1', 'pred_2','pred_3','pred_4',
                                   'pred_5','pred_6','pred_7','pred_8',
                                  'pred_9','pred_10']


    df_pred = predictions[['item_id']].T

    df_pred.columns = cols

    df_pred['id'] = user_id


    df_pred = df_pred[['id','pred_1', 'pred_2','pred_3','pred_4',
                                       'pred_5','pred_6','pred_7','pred_8',
                                      'pred_9','pred_10']]

    df_pred['id'] = df_pred['id'].astype(int)


    print('#'*1000, 'writing to recommendations1 Table\n')

    #model.update_table(df=df_pred, table=recommendations1, engine=engine)

    df_pred.to_sql(recommendations1, engine, if_exists='append', index=False) #if_exists='append'
    session.commit()


    predictions_top20 = test_prediction.head(n=20)

    predictions_top20['algorithm'] = algo
    predictions_top20.rename(columns={'prediction':'predicted_rating'}, inplace=True)


    predictions_top20.to_sql('numeric_predictions',engine,if_exists='append', index=False) #if_exists='append'
    session.commit()


    predcols =['num_1', 'num_2','num_3','num_4',
                                       'num_5','num_6','num_7','num_8',
                                      'num_9','num_10']

    df_num_ratings_transpose = predictions[['prediction']].T
    df_num_ratings_transpose.columns = predcols

    df_num_ratings_transpose['id'] = user_id

    df_num_ratings_transpose = df_num_ratings_transpose[['id','num_1', 'num_2','num_3','num_4',
                                       'num_5','num_6','num_7','num_8',
                                      'num_9','num_10']]

    df_num_ratings_transpose['id'] = df_num_ratings_transpose['id'].astype(int)


    #model.update_table(df=df_num_ratings_transpose, table=transposed_prediction1, engine=engine)
    df_num_ratings_transpose.to_sql(transposed_prediction1, engine, if_exists='append', index=False) #if_exists='append'
    session.commit()



    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Finish Computing Predictions - " + algo, rating=None) #pageview
