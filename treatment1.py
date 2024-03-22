# from __future__ import absolute_import, division, print_function, unicode_literals
import os
os.getcwd()
#import algorithms from surprise
import surprise
from surprise import Dataset
from surprise import Reader
from surprise import accuracy
# from surprise import evaluate
# from surprise import print_perf
import model
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
import copy

# from surprise import dump
# from model import add_pageview

# algorithm = SVD(biased=False,n_epochs=10,lr_all=0.005,reg_all=0.6)

def compute_recommendations_to_csv(user_id):

    algo = 'SVD'
    algorithm = SVD(n_factors=2, n_epochs=2)

    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Initialize Predictions - " + algo, rating=None) #pageview

    engine = create_engine(config.DB_URI, echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))


    model.delete_recommendations1(user_id)
    model.delete_transposed_prediction1(user_id)
    model.delete_numeric_predictions1(user_id)

    #reading in the database
    #user_id=1
    #df_ratings = pd.read_csv('data/user_selections.csv',low_memory=False, encoding='UTF-8')
    df_ratings = pd.read_sql(f'SELECT * FROM user_selections WHERE user_id={user_id};', con=engine)
    df_ratings.replace("null", pd.NA, inplace=True)
    df_ratings = df_ratings.dropna()
    #df_ratings = df_ratings.drop(['Unnamed: 0'], axis=1)
    df_ratings = df_ratings.drop(['title'], axis=1)

    df_ratings2 = pd.read_csv('data/ratings.csv', low_memory=False, encoding='UTF-8')
    df_ratings2 = df_ratings2.rename(columns = {'movie_id': 'item_id'})
    df_ratings2 = df_ratings2[['user_id','item_id','rating']]
    df_ratings2 = df_ratings2.dropna()
    df_ratings2 = df_ratings2.drop_duplicates()

    df_ratings = pd.concat([df_ratings, df_ratings2], axis=0).drop_duplicates() #.sample(n=100)
    # df_ratings.head()
    #df_ratings.to_csv('data/df_ratings.csv')

    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 10))
    data = Dataset.load_from_df(df_ratings, reader=reader)

    trainset = data.build_full_trainset()

#   algorithm = eval(algo + "()")# set the algorithm...............................................

    print('&'*1000, 'fitting the model')
    algorithm.fit(trainset)


    # items = pd.read_sql('SELECT distinct id FROM items;', con = engine)
    items_full = pd.read_csv('./data/items.csv', low_memory=False, encoding='UTF-8')
    items = items_full[['id']].drop_duplicates()
    total_items = items.id.unique()
    # items_full.rename(columns={'id':'item_id'}, inplace=True)

    # # user_id=51556
    df_user_items = df_ratings.loc[df_ratings['user_id'] == user_id]
    # df_user_items.head()
    user_items = df_user_items.item_id.unique()
    # user_id = str(user_id)


    prediction_items = [x for x in total_items if x not in user_items]

    predictions = pd.DataFrame(columns=['user_id', 'item_id', 'prediction'])

    predicted_ratings = []

    for i in prediction_items:
        a = user_id
        b = i
        est = algorithm.predict(a, b)
        predicted_ratings.append(est[3])

    predictions['item_id'] = prediction_items
    predictions['user_id'] = pd.Series([user_id for x in range(len(predictions.index))], index=predictions.index)
    predictions['prediction'] = predicted_ratings
    predictions = predictions.sort_values('prediction', ascending=False)

    #### Bring in the Genre Data
    ## Find genre information and merge
    #items_full = pd.read_sql('SELECT * FROM items;', con=engine)
    predictions_w_item_info = pd.merge(predictions, items_full, how='left', left_on='item_id', right_on='id')
    predictions_w_item_info['genre'] = predictions_w_item_info['genres']

    #pd.set_option('display.max_columns', 100);
    #rint("Prediction!!! " , predictions_w_item_info.head(10))

    ## Round & Normalize prediction values
    predictions_w_item_info['prediction'] = predictions_w_item_info['prediction']/predictions_w_item_info['prediction'].max()*10
    predictions_w_item_info['prediction'] = predictions_w_item_info['prediction'].round(2)

    '''output_path = './data/predictions/svd_predictions_w_item_info.csv'
    predictions_w_item_info.to_csv(output_path, index=False)
    print(f'prediction saved at {output_path}')'''

    ##################  Save SVD PREDICTIONS  ##################
    # Select 10 top items from different genres
    #added 1 in cumulative count as rank start with 0

    predictions_w_item_info['rank'] = predictions_w_item_info.groupby('genres')['prediction'].cumcount() + 1
    pd.set_option('display.max_columns', 100);
    print("Prediction!!! ", predictions_w_item_info.head(10))
    genreSelected = predictions_w_item_info.loc[predictions_w_item_info['rank'] == 10].head(1)['genre']
    genreSelectedNew = genreSelected.reset_index(drop=True)
    genreString = genreSelectedNew.iloc[0]
    print("genreSelected   " + genreSelectedNew.iloc[0])
    print("genreTYPE !!! ")
    print(type(genreSelected))

    index_of_2023 = predictions_w_item_info[predictions_w_item_info['year'] == 2017].index[0]
    print("Index of the first occurrence of the year 2023:", index_of_2023)

    i_list = []  # list of genres and indexes
    for i in predictions_w_item_info.index:
        g = predictions_w_item_info.loc[i, 'genre']
        i_list.append(i)
        print(f'index {i} selected')
        if len(i_list) == 10:
            break

    svd_predictions = predictions_w_item_info.loc[i_list]
    svd_predictions = svd_predictions.sample(frac=1)
    A =pd.DataFrame( svd_predictions[0:5].sort_values('prediction', ascending=False))
    B =pd.DataFrame( svd_predictions[5:10].sort_values('prediction', ascending=False))
    svd_predictions = A._append(B)
    svd_predictions['algo']='SVD'

    '''for i in range(len(svd_predictions)):
        if (svd_predictions.loc[i,'prediction']>7) & (svd_predictions.loc[i,'prediction'] <= 8):
            svd_predictions.loc[i, 'prediction'] = svd_predictions.loc[i,'prediction'] + 1
        elif (svd_predictions.loc[i,'prediction']> 6) & (svd_predictions.loc[i,'prediction'] <= 7):
            svd_predictions.loc[i, 'prediction'] = svd_predictions.loc[i,'prediction'] + 2
        elif (svd_predictions.loc[i, 'prediction'] > 5) & (svd_predictions.loc[i, 'prediction'] <= 6):
            svd_predictions.loc[i, 'prediction'] = svd_predictions.loc[i,'prediction'] + 3
        else:
            break'''

    '''output_path = './data/predictions/svd_predictions.csv'
    svd_predictions.to_csv(output_path, index=False)
    print(f'prediction saved at {output_path}')'''

    # Amruta changes

    #model.delete_svdpredictions(user_id)
    svd_prediction_original = copy.deepcopy(svd_predictions)
    svd_predictions.to_sql('svd_predictions', engine, if_exists='append', index=False)  # if_exists='append'


    #svd_predict = pd.read_csv('./data/predictions/svd_predictions.csv',low_memory=False, encoding='UTF-8')
    # svd_ad = pd.read_csv('./data/predictions/svd_ad_predictions.csv',low_memory=False)
    #svd_all = svd_prediction_original
    #result = svd_all
    result = svd_prediction_original
    result = result[['user_id', 'item_id', 'prediction','algo']]
    # result.to_csv('./data/predictions/result.csv')

    result.to_sql('prediction_personalized', engine, if_exists='append', index=False) #if_exists='append'
    session.commit()


def compute_recommendations(user_id, recommendations1, transposed_prediction1):
    algo = 'SVD'
    algorithm = SVD(n_factors=2, n_epochs=2)
    engine = create_engine(config.DB_URI, echo=True)
    session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))


    model.delete_recommendations1(user_id)
    model.delete_transposed_prediction1(user_id)
    model.delete_numeric_predictions1(user_id)

    while True:
        # Perform a query to check if the ID exists in the database
        result = pd.read_sql(f'SELECT user_id FROM svd_predictions WHERE user_id={user_id};', con=engine)
        # Check if the ID is found
        if not result.empty:
            print(f"ID {user_id} found in the database!")
            break
        time.sleep(1)  # Sleep for 1 second (adjust as needed)


    predictions = pd.read_sql(f'SELECT * FROM svd_predictions WHERE user_id={user_id};', con=engine)
    predictions = predictions.tail(10) if len(predictions) > 10 else predictions
    #predictions = pd.read_sql('SELECT * FROM svd_predictions;', con=engine)
    #predictions = pd.read_csv('./data/predictions/svd_predictions.csv',low_memory=False, encoding='UTF-8')

    print('*' * 100, '\n')
    # print("items_full:\n\n\n", items_full.head())
    # print("predictions (augmented) before adding inferior:\n\n\n", predictions.head())

    predictions = predictions[['user_id', 'item_id', 'prediction']].copy()
    # predictions.iloc[1] = predictions.loc[inferior_item_index].copy() ## Turn off swapping to exclude the decoy

    ## Print the result
    print("**** predictions with inferior item:\n\n\n", predictions)

################################  End  #################################

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

    df_pred.to_sql(recommendations1, engine, if_exists='append', index=False) #if_exists='append'
    session.commit()
    #df_pred.to_csv('./data/Predictions/temp/recommendations1.csv', index=False)


    predictions_top20 = test_prediction.head(n=20)

    predictions_top20['algorithm'] = algo
    predictions_top20.rename(columns={'prediction':'predicted_rating'}, inplace=True)

    predictions_top20.to_sql('numeric_predictions',engine,if_exists='append', index=False) #if_exists='append'
    session.commit()
    #predictions_top20.to_csv('./data/Predictions/temp/numeric_predictions.csv', index=False)


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




    df_num_ratings_transpose.to_sql(transposed_prediction1, engine, if_exists='append', index=False)#if_exists='append'
    session.commit()
    #df_num_ratings_transpose.to_csv('./data/Predictions/temp/transposed_prediction1.csv', index=False)
    # add_pageview(user_id=user_id, item_id=None, page="Model Predictions", activity_type="Finish Computing Predictions - " + algo, rating=None) #pageview


