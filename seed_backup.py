import config
from sqlalchemy.ext.declarative import declarative_base
import os
os.getcwd()

def auto_truncate_description(val):
    return val[:1024]
def auto_truncate_title(val):
    return val[:255]

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import numpy as np
import pandas as pd
import datetime


def auto_truncate_description(val):
    return val[:1024]
def auto_truncate_title(val):
    return val[:255]


df_ratings = pd.read_csv("./data/ratings.csv", low_memory=False)

# subsetting dataframe
df_ratings = df_ratings[["user_id", "movie_id", "rating", "timestamp"]]
df_ratings.timestamp = pd.to_datetime(df_ratings["timestamp"],unit = 's')

#changing column names
df_ratings = df_ratings.rename(columns={'movie_id': 'item_id'})

#extracting top rated items from the ratings dataframe

item_filter = pd.DataFrame(df_ratings['item_id'])
item_filter = item_filter.groupby('item_id').size()
item_filter = item_filter.to_frame().reset_index()

item_filter.columns.values[1] = 'count'
item_filter = item_filter.sort_values('count', ascending=False)

# item_filter = item_filter.head(n=8000)
item_filter = item_filter.sample(frac=1)


item_filter = item_filter[['item_id']]

df_ratings = pd.merge(left=df_ratings,right=item_filter, left_on='item_id', right_on='item_id')

# creating keys
df_ratings = df_ratings.sort_values("user_id")

df_ratings.user_id = df_ratings.user_id.astype("category")

df_ratings["userid_key"] = df_ratings["user_id"].cat.codes
df_ratings["userid_key"] = df_ratings["userid_key"] + 1

df_ratings = df_ratings.rename(columns={'user_id': 'old_user_id'})

df_ratings = df_ratings.rename(columns={'userid_key': 'user_id'})

# reading in items
# df_items = pd.read_csv("data/meta.csv", low_memory= False, converters={'description': auto_truncate_description,'title': auto_truncate_title})
df_items = pd.read_csv("./data/movie_data.csv", low_memory=False)
# extracting specific columns

# df_items = df_items[["movieId", "title", "genres"]]

df_items = df_items.rename(columns={'movieId': 'id'})

df_items = pd.merge(left=df_items,right=item_filter, left_on='id', right_on='item_id')

# df_items = df_items[["id", "title", "genres"]]
df_items.drop(['item_id'], axis=1, inplace=True)

df_users = pd.DataFrame()

df_users["id"] = df_ratings.user_id.unique()
df_users = pd.merge(df_users,df_ratings , left_on="id", right_on= "user_id")

df_users = df_users[['id', 'old_user_id']]
df_users = df_users.drop_duplicates()

df_ratings = df_ratings[['user_id', 'item_id', 'rating']]



for i in df_items.columns:
    print(i, df_items[i].head())
    df_items[i] = df_items[i].astype('str')
    # df_items[i] = df_items[i].apply(lambda x: x.\
    #                                       encode('ascii', 'ignore').\
    #                                       strip()) #.decode('unicode_escape').\


df_items['id'] = df_items['id'].astype(int)
# df_items['year'] = df_items['year'].astype(int)

# df_items['id'] = df_items['id'].astype(int)

df_current_algo = pd.DataFrame(columns = ['id', 'algorithm'])

df_current_algo.loc[1] = [1, 'recommender1_random']
df_current_algo.loc[2] = [2, 'control']

# DB_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://nabeeltariq2:nabeeltariq2@nabeeltariq2.cpliemudyxqt.us-east-1.rds.amazonaws.com/nabeeltariq6?charset=utf8')
# engine = create_engine(DB_URI, echo=False)


engine = create_engine(config.DB_URI, echo=False)


# engine = create_engine(config.DB_URI, echo=False)

session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

###############################################################
###############################################################
###############################################################

# Append users
df_users.to_sql('users', engine, if_exists='append', index=False) #if_exists='append'
session.commit()

#Append items
# df_items['id'] = df_items['id'].astype(str)
# df_items.head()
df_items.to_sql('items',engine,if_exists='append', index=False) #if_exists='append'
session.commit()

x = pd.read_sql('SELECT * FROM items;', con = engine)
x.head()

x.columns
x[['imdb_id', 'title', 'poster_path']]
x.loc[x['title']=='Inception', 'poster_path']


df_current_algo.to_sql('Current_algo',engine,if_exists='append', index=False) #if_exists='append'
session.commit()

pd.read_sql('SET FOREIGN_KEY_CHECKS=0;', con=engine)
# # Append ratings
df_ratings[1:10].to_sql('ratings',engine,if_exists='append', index=False) #if_exists='append'
session.commit()
pd.read_sql('select * from ratings;', con=engine)



# Change the current algorithms table
pd.read_sql('SELECT * FROM Current_algo;', con = engine)

row1 = Current_algo.query.filter_by(id=1).first()
row1.algorithm = "control"
session.commit()

row2 = Current_algo.query.filter_by(id=2).first()
row2.algorithm = "treatment1"
session.commit()
pd.read_sql('SELECT * FROM Current_algo;', con = engine)

row3 = Current_algo.query.filter_by(id=3).first()
row3.algorithm = "control_decoy"
session.commit()
pd.read_sql('SELECT * FROM Current_algo;', con = engine)

row4 = Current_algo.query.filter_by(id=4).first()
row4.algorithm = "treatment1_decoy"
session.commit()
pd.read_sql('SELECT * FROM Current_algo;', con = engine)

## ADD the round columns to the algo table
# pd.read_sql('SELECT * FROM algo;', con = engine)
# q = "ALTER TABLE algo ADD round Integer DEFAULT 0"
# pd.read_sql(q, con=engine)


## ADD the rec columns to the userchoice table
# pd.read_sql('SELECT * FROM userchoice;', con = engine)
# q2 = "ALTER TABLE userchoice ADD rec VARCHAR(128) DEFAULT ''"
# pd.read_sql(q2, con=engine)

## Read User Choices
x = pd.read_sql('SELECT * FROM userchoice;', con = engine)
print(x.iloc[:,0:5])
print(x['rec'])
pd.read_sql('SELECT * FROM algo;', con = engine)


pd.read_sql('SELECT * FROM Current_algo;', con = engine)
#
# a = [0,2]
# b = [1,3]
# c = [a,b]
# y = {}
# for i in range(8):
#     new = random.sample([random.sample(a,2),random.sample(b,2)], 2)
#     new = [x for sublist in new for x in sublist]
#     y[i] = new
# print(y)
# algos = ['control','treatment1','control_decoy','treatment1_decoy']
# seqs = {0: [2, 0, 3, 1], 1: [0, 2, 3, 1], 2: [3, 1, 2, 0], 3: [1, 3, 2, 0],
#         4: [2, 0, 1, 3], 5: [0, 2, 1, 3], 6: [3, 1, 0, 2], 7: [1, 3, 0, 2]}
# user_id = 53421
#
# seq = seqs[user_id%8]
# seq_names = [algos[i] for i in seq]


#
# # ADD the round and algo_name columns to the feedback table
# pd.read_sql('SELECT * FROM feedback;', con = engine)
# q = "ALTER TABLE feedback ADD round Integer DEFAULT 0"
# pd.read_sql(q, con=engine)
# q = "ALTER TABLE feedback ADD algo_name VARCHAR(128) DEFAULT ''"
# pd.read_sql(q, con=engine)

pd.set_option('display.max_columns', None)
x = pd.read_sql('SELECT * FROM feedback;', con = engine)
x[-10:]

pd.set_option('display.max_columns', None)
x = pd.read_sql('SELECT * FROM users;', con = engine)
print(x[-10:])
q = "ALTER TABLE users ADD familiar VARCHAR(128) DEFAULT ''"
pd.read_sql(q, con=engine)

q = "ALTER TABLE users ADD used VARCHAR(128) DEFAULT ''"
pd.read_sql(q, con=engine)

q = "ALTER TABLE users ADD native VARCHAR(128) DEFAULT ''"
pd.read_sql(q, con=engine)

q = "ALTER TABLE users ADD movie_count VARCHAR(128) DEFAULT ''"
pd.read_sql(q, con=engine)

q = "ALTER TABLE users ADD genre VARCHAR(128) DEFAULT ''"
pd.read_sql(q, con=engine)

q = "ALTER TABLE users_info ADD sponsored_content TEXT DEFAULT ''"
pd.read_sql(q, con=engine)


q = "ALTER TABLE items ADD item_time VARCHAR(128) DEFAULT ''"
pd.read_sql(q, con=engine)


# q = "drop table users_info"
# pd.read_sql(q, con=engine)

q = '''CREATE TABLE users_info (
info_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
user_id INT(15) UNSIGNED NOT NULL,
age VARCHAR(10),
gender VARCHAR(10) ,
native VARCHAR(10) ,
familiar VARCHAR(10) ,
used VARCHAR(10) ,
movie_count VARCHAR(10) ,
genre VARCHAR(10) ,
old_user_id VARCHAR(10) ,
user_info_add_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);'''   #--
pd.read_sql(q, con=engine)

# q = "ALTER TABLE users_info CHANGE old_user_id old_user"
# pd.read_sql(q, con=engine)

pd.set_option('display.max_columns', None)
x = pd.read_sql('SELECT * FROM users_info;', con = engine)
print(x[-10:])


# modify feedback table
q = "DELETE FROM items"
pd.read_sql(q, con=engine)
q = "DELETE FROM ratings"
pd.read_sql(q, con=engine)
pd.read_sql( "Select * FROM ratings", con=engine)
q = "DELETE FROM numeric_predictions"
pd.read_sql(q, con=engine)
q = "DELETE FROM shoppingcart"
pd.read_sql(q, con=engine)

q = "ALTER TABLE feedback ADD sponsored_manip Integer DEFAULT 0"
pd.read_sql(q, con=engine)

q = "drop table feedback"
pd.read_sql(q, con=engine)

pd.read_sql("Select * FROM feeback", con=engine)

q = '''CREATE TABLE feedback (
id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
user_id INT(15) UNSIGNED NOT NULL,
sat1 VARCHAR(10),
sat2 VARCHAR(10) ,
trust1 VARCHAR(10) ,
trust2 VARCHAR(10) ,
decoy_manip VARCHAR(10) ,
pers_manip VARCHAR(10) ,
sponsored_manip1 VARCHAR(10) ,
sponsored_manip2 VARCHAR(10) ,
round VARCHAR(10) ,
algo_name VARCHAR(10) ,
`user` varchar(10) DEFAULT NULL,
feedback_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);'''   #--
pd.read_sql(q, con=engine)

q = '''ALTER TABLE feedback 
modify column algo_name VARCHAR(30);'''
pd.read_sql(q, con=engine)

pd.set_option('display.max_columns', None)
x = pd.read_sql('SELECT * FROM feedback;', con = engine)
print(x[-10:])


q='''
ALTER TABLE ratings
DROP FOREIGN KEY `ratings_ibfk_2` ;
'''
pd.read_sql(q, con=engine)

pd.read_sql('FOREIGN_KEY_CHECKS=0', con=engine)

q='''
ALTER TABLE numeric_predictions
DROP FOREIGN KEY `numeric_predictions_ibfk_2`   ;
'''
pd.read_sql(q, con=engine)
q='''
ALTER TABLE shoppingcart
DROP FOREIGN KEY `shoppingcart_ibfk_2`  ;
'''
pd.read_sql(q, con=engine)

q='''SHOW CREATE TABLE ratings'''
x = pd.read_sql(q, con=engine)
print(x['Create Table'][0])

q='''SHOW CREATE TABLE items'''
x = pd.read_sql(q, con=engine)
print(x['Create Table'][0])

q='''SHOW CREATE TABLE shoppingcart'''
x = pd.read_sql(q, con=engine)
print(x['Create Table'][0])


q='''SHOW CREATE TABLE ratings'''
x = pd.read_sql(q, con=engine)
print(x['Create Table'][0])

q='''
ALTER TABLE numeric_predictions
	DROP FOREIGN KEY item_id; '''
pd.read_sql(q, con=engine)


q='''
Alter TABLE ratings
Add FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
'''
pd.read_sql(q, con=engine)


print(pd.read_sql('show CREATe table numeric_predictions', con=engine)['Create Table'][0])
q='''
Alter TABLE numeric_predictions
Add FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
'''
pd.read_sql(q, con=engine)

q='''
Alter TABLE shoppingcart
Add FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
'''
pd.read_sql(q, con=engine)


engine.execute("DELETE FROM ratings")
engine.execute("drop table items")
x = pd.read_sql("Select * FROM ratings", con=engine)
x.columns
x.head()

######################################################################

pd.read_sql('SET FOREIGN_KEY_CHECKS=0;', con=engine)
pd.read_sql('drop table items', con=engine)
q = '''CREATE TABLE `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `imdb_id` text DEFAULT NULL,
  `tmdb_id` text DEFAULT NULL,
  `original_language` text DEFAULT NULL,
  `overview` text DEFAULT NULL,
  `popularity` text DEFAULT NULL,
  `poster_path` text DEFAULT NULL,
  `runtime` text DEFAULT NULL,
  `tagline` text DEFAULT NULL,
  `title` text DEFAULT NULL,
  `vote_average` text DEFAULT NULL,
  `vote_count` text DEFAULT NULL,
  `year` int(5) DEFAULT NULL,
  `youtubeId` text DEFAULT NULL,
  `genres` text DEFAULT NULL,
  `item_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 '''
pd.read_sql(q, con=engine)
pd.read_sql('show CREATe table items', con=engine)['Create Table'][0]



engine.execute('drop table numeric_predictions')
q = '''CREATE TABLE `numeric_predictions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `predicted_rating` float DEFAULT NULL,
  `algorithm` varchar(128) DEFAULT NULL,
  `prediction_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `numeric_predictions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `numeric_predictions_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5994411 DEFAULT CHARSET=utf8'''
engine.execute(q)
print(pd.read_sql('show CREATe table numeric_predictions', con=engine)['Create Table'][0])
x = pd.read_sql('select * from numeric_predictions', con=engine)
x.columns
x.head()
x.iloc[1:2,0:4]


engine.execute('drop table shoppingcart')
q = '''
CREATE TABLE `shoppingcart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `cart_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `shoppingcart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `shoppingcart_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
engine.execute(q)
print(pd.read_sql('show CREATe table shoppingcart', con=engine)['Create Table'][0])
pd.read_sql('select * from shoppingcart', con=engine)


engine.execute('drop table ratings')
q = '''
CREATE TABLE `ratings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `text_rating` varchar(256) DEFAULT NULL,
  `rating_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1420116 DEFAULT CHARSET=utf8
'''
engine.execute(q)
print(pd.read_sql('show CREATe table ratings', con=engine)['Create Table'][0])
pd.read_sql('select * from ratings', con=engine)

################### checkout tables ###################
pd.set_option('display.max_columns', None)

x = pd.read_sql('select * from recommendations1', con=engine)
print(x.head())

x = pd.read_sql('select * from numeric_predictions', con=engine)
print(x.head())

x = pd.read_sql('select * from transposed_prediction1', con=engine)
print(x.head())


x = pd.read_sql('select * from transposed_prediction1', con=engine)
print(x.head())


## Read User Choices
x = pd.read_sql('SELECT * FROM userchoice  WHERE user_id=51550;', con = engine)
print(x.iloc[:,0:5])
print(x)
pd.read_sql('SELECT * FROM algo  WHERE user_id=51331;', con = engine)
x = pd.read_sql('SELECT * FROM pageview WHERE user_id=51331;', con = engine)
x[-100:]

pd.set_option('display.max_columns', None)
x = pd.read_sql('SELECT * FROM feedback;', con = engine)
x[-10:]


x = pd.read_sql('select * from items order by vote_average Desc LIMIT 100;', con=engine)
x.head()
x[x['vote_average']]


q = '''
CREATE TABLE `recommendations1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pred_1` int(11) DEFAULT NULL,
  `pred_2` int(11) DEFAULT NULL,
  `pred_3` int(11) DEFAULT NULL,
  `pred_4` int(11) DEFAULT NULL,
  `pred_5` int(11) DEFAULT NULL,
  `pred_6` int(11) DEFAULT NULL,
  `pred_7` int(11) DEFAULT NULL,
  `pred_8` int(11) DEFAULT NULL,
  `pred_9` int(11) DEFAULT NULL,
  `pred_10` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=1420116 DEFAULT CHARSET=utf8
'''
engine.execute(q)
print(pd.read_sql('show CREATe table ratings', con=engine)['Create Table'][0])
pd.read_sql('select * from ratings', con=engine)


engine.execute("drop table transposed_prediction1")

q = '''
CREATE TABLE `transposed_prediction1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_1` int(11) DEFAULT NULL,
  `num_2` int(11) DEFAULT NULL,
  `num_3` int(11) DEFAULT NULL,
  `num_4` int(11) DEFAULT NULL,
  `num_5` int(11) DEFAULT NULL,
  `num_6` int(11) DEFAULT NULL,
  `num_7` int(11) DEFAULT NULL,
  `num_8` int(11) DEFAULT NULL,
  `num_9` int(11) DEFAULT NULL,
  `num_10` int(11) DEFAULT NULL,
    PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=1420116 DEFAULT CHARSET=utf8
'''
engine.execute(q)
print(pd.read_sql('show CREATE table transposed_prediction1', con=engine)['Create Table'][0])
pd.read_sql('select * from transposed_prediction1', con=engine)


df_items.to_sql('items',engine,if_exists='append', index=False) #if_exists='append'

df_items.columns
i=0
for i in df_items.index:
    print(i)
    query = f"""INSERT INTO items (imdb_id, poster_path) VALUES('{df_items.imdb_id[i]}', '{df_items.poster_path[i]}')
    ON DUPLICATE KEY UPDATE items.poster_path= ' {str(df_items.poster_path[i])} ' """
    engine.execute(query)

df_items.poster_path.str.replace('b','')
df_items.poster_path = df_items.poster_path.str.decode('utf8')
df_items.imdb_id = df_items.imdb_id.str.decode('utf8')


x = pd.read_sql('select * from items', con=engine)
x.columns
x[x['title']=='Inception']
x[x['title']=='Inception']['poster_path']


i = 953
query = f"""INSERT INTO items (imdb_id, poster_path) VALUES('{df_items.imdb_id[i]}', '{df_items.poster_path[i]}')
ON DUPLICATE KEY UPDATE items.poster_path= '{str(df_items.poster_path[i])}' """
engine.execute(query)


df_items.loc[i,['poster_path', 'title']]
df_items[df_items['title']=='Inception']['poster_path']


####Nasim aded result of personalized items for each user from csv

q = '''
CREATE TABLE `prediction_personalized` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `user_id` INT(15) DEFAULT NULL,
    `item_id` INT(15) DEFAULT NULL,
    `prediction` VARCHAR(10) DEFAULT NULL,
    `algo` VARCHAR(10) DEFAULT NULL,
        PRIMARY KEY (`id`)
        
) ENGINE=InnoDB AUTO_INCREMENT=1420116 DEFAULT CHARSET=utf8
'''
engine.execute(q)
print(pd.read_sql('show CREATE table prediction_personalized', con=engine)['Create Table'][0])
pd.read_sql('select * from prediction_personalized', con=engine)


####Nasim aded result of popular items for each user from csv

q = '''
CREATE TABLE `prediction_top` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `user_id` INT(15) DEFAULT NULL,
    `item_id` INT(15) DEFAULT NULL,
    `prediction` VARCHAR(10) DEFAULT NULL,
    `algo` VARCHAR(10) DEFAULT NULL,
        PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=1420116 DEFAULT CHARSET=utf8
'''
engine.execute(q)
print(pd.read_sql('show CREATE table prediction_top', con=engine)['Create Table'][0])
pd.read_sql('select * from prediction_top', con=engine)




###test
pd.read_sql('show tables', con=engine)

x = pd.read_sql('select * from users_info', con=engine)
x.columns
x[-1:]