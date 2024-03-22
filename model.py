from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, Text, MetaData, Table
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine, text , delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func
# import recommender1
# import recommender2
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

import config

engine = create_engine(config.DB_URI, echo=False ,pool_pre_ping=True)
#create_engine("mysql://scott:tiger@localhost/test", pool_recycle=3600)
try:
    connection = engine.connect()
    print("Connected successfully!")
    connection.close()
except Exception as e:
    print("Connection error:", e)
if not database_exists(engine.url):
    create_database(engine.url)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit=False,
                                      autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    old_user_id = Column(String(64), nullable = True)
    user_add_time = Column(DateTime, server_default=func.now())

class User_Info(Base):
    __tablename__ = "users_info"

    info_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    age = Column(String(64), nullable=True)
    gender = Column(String(64), nullable=True)
    native = Column(String(64), nullable=True)
    famil = Column(String(64), nullable=True)
    experience = Column(String(64), nullable=True)
    movie_count = Column(String(64), nullable=True)
    favorite_genre = Column(String(64), nullable=True)
    old_user = Column(String(64), nullable=True)
    user_info_add_time = Column(DateTime, server_default=func.now())
    expec = Column (String(64), nullable = True)
    trustlos = Column(String(64), nullable=True)
    manipmech1 = Column(String(64), nullable=True)
    manipmech2 = Column(String(64), nullable=True)
    reactance = Column(String(64), nullable=True)



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    tmdb_id = Column(String(128), nullable=True)
    youtubeId = Column(Text, nullable=True)
    imdb_id = Column(String(64), nullable=True)
    original_language = Column(String(64), nullable=True)
    overview = Column(Text, nullable=True)
    popularity = Column(String(64), nullable=True)
    poster_path = Column(Text, nullable=True)
    runtime = Column(String(64), nullable=True)
    tagline = Column(String(512), nullable=True)
    vote_average = Column(String(64), nullable=True)
    vote_count = Column(Text, nullable=True)
    genres = Column(String(256), nullable=True)
    year = Column(Integer, nullable=True)
    title = Column(String(1280), nullable=True)
    item_time = Column(DateTime, server_default=func.now())


class Rating(Base):
    ### Association object
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    rating = Column(Integer, nullable=True)
    # rating = Column(Float,nullable=True)
    text_rating = Column(String(256), nullable=True)

    rating_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("ratings", order_by=id))
    item = relationship("Item", backref=backref("ratings", order_by=id))


# class Recommendations(Base):
# ### Association object
#     __tablename__= "recommendations"
#
#     id = Column(Integer, ForeignKey('users.id'),primary_key = True)
#     pred_1 = Column(String(128), nullable=True)
#     pred_2 = Column(String(128), nullable=True)
#     pred_3 = Column(String(128), nullable=True)
#     pred_4 = Column(String(128), nullable=True)
#     pred_5 = Column(String(128), nullable=True)
#     pred_6 = Column(String(128), nullable=True)
#     pred_7 = Column(String(128), nullable=True)
#     pred_8 = Column(String(128), nullable=True)
#     pred_9 = Column(String(128), nullable=True)
#     pred_10 = Column(String(128), nullable=True)
#
#     user = relationship("User", backref=backref("recommendations", order_by=id))
#

class Recommendations1(Base):
### Association object
    __tablename__= "recommendations1"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    pred_1 = Column(Integer, nullable=True)
    pred_2 = Column(Integer, nullable=True)
    pred_3 = Column(Integer, nullable=True)
    pred_4 = Column(Integer, nullable=True)
    pred_5 = Column(Integer, nullable=True)
    pred_6 = Column(Integer, nullable=True)
    pred_7 = Column(Integer, nullable=True)
    pred_8 = Column(Integer, nullable=True)
    pred_9 = Column(Integer, nullable=True)
    pred_10= Column(Integer, nullable=True)

    user = relationship("User", backref=backref("recommendations1", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))

#
# class Recommendations2(Base):
# ### Association object
#     __tablename__= "recommendations2"
#
#     id = Column(Integer, ForeignKey('users.id'),primary_key = True)
#     pred_1 = Column(Integer, nullable=True)
#     pred_2 = Column(Integer, nullable=True)
#     pred_3 = Column(Integer, nullable=True)
#     pred_4 = Column(Integer, nullable=True)
#     pred_5 = Column(Integer, nullable=True)
#     pred_6 = Column(Integer, nullable=True)
#     pred_7 = Column(Integer, nullable=True)
#     pred_8 = Column(Integer, nullable=True)
#     pred_9 = Column(Integer, nullable=True)
#     pred_10= Column(Integer, nullable=True)
#
#     user = relationship("User", backref=backref("recommendations2", order_by=id))
#     # item = relationship("Item", backref=backref("recommendations", order_by=id))
#
# class Recommendations3(Base):
# ### Association object
#     __tablename__= "recommendations3"
#
#     id = Column(Integer, ForeignKey('users.id'),primary_key = True)
#     pred_1 = Column(Integer, nullable=True)
#     pred_2 = Column(Integer, nullable=True)
#     pred_3 = Column(Integer, nullable=True)
#     pred_4 = Column(Integer, nullable=True)
#     pred_5 = Column(Integer, nullable=True)
#     pred_6 = Column(Integer, nullable=True)
#     pred_7 = Column(Integer, nullable=True)
#     pred_8 = Column(Integer, nullable=True)
#     pred_9 = Column(Integer, nullable=True)
#     pred_10= Column(Integer, nullable=True)
#
#     user = relationship("User", backref=backref("recommendations3", order_by=id))
#     # item = relationship("Item", backref=backref("recommendations", order_by=id))
#
#
# class Recommendations4(Base):
# ### Association object
#     __tablename__= "recommendations4"
#
#     id = Column(Integer, ForeignKey('users.id'),primary_key = True)
#     pred_1 = Column(Integer, nullable=True)
#     pred_2 = Column(Integer, nullable=True)
#     pred_3 = Column(Integer, nullable=True)
#     pred_4 = Column(Integer, nullable=True)
#     pred_5 = Column(Integer, nullable=True)
#     pred_6 = Column(Integer, nullable=True)
#     pred_7 = Column(Integer, nullable=True)
#     pred_8 = Column(Integer, nullable=True)
#     pred_9 = Column(Integer, nullable=True)
#     pred_10= Column(Integer, nullable=True)
#
#     user = relationship("User", backref=backref("recommendations4", order_by=id))
#     # item = relationship("Item", backref=backref("recommendations", order_by=id))

class Transposed_prediction1(Base):
### Association object
    __tablename__= "transposed_prediction1"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    num_1 = Column(Float, nullable=True)
    num_2 = Column(Float, nullable=True)
    num_3 = Column(Float, nullable=True)
    num_4 = Column(Float, nullable=True)
    num_5 = Column(Float, nullable=True)
    num_6 = Column(Float, nullable=True)
    num_7 = Column(Float, nullable=True)
    num_8 = Column(Float, nullable=True)
    num_9 = Column(Float, nullable=True)
    num_10= Column(Float, nullable=True)

    user = relationship("User", backref=backref("transposed_prediction1", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))

class Transposed_prediction2(Base):
### Association object
    __tablename__= "transposed_prediction2"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    num_1 = Column(Float, nullable=True)
    num_2 = Column(Float, nullable=True)
    num_3 = Column(Float, nullable=True)
    num_4 = Column(Float, nullable=True)
    num_5 = Column(Float, nullable=True)
    num_6 = Column(Float, nullable=True)
    num_7 = Column(Float, nullable=True)
    num_8 = Column(Float, nullable=True)
    num_9 = Column(Float, nullable=True)
    num_10= Column(Float, nullable=True)

    user = relationship("User", backref=backref("transposed_prediction2", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))

class Transposed_prediction3(Base):
### Association object
    __tablename__= "transposed_prediction3"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    num_1 = Column(Float, nullable=True)
    num_2 = Column(Float, nullable=True)
    num_3 = Column(Float, nullable=True)
    num_4 = Column(Float, nullable=True)
    num_5 = Column(Float, nullable=True)
    num_6 = Column(Float, nullable=True)
    num_7 = Column(Float, nullable=True)
    num_8 = Column(Float, nullable=True)
    num_9 = Column(Float, nullable=True)
    num_10= Column(Float, nullable=True)

    user = relationship("User", backref=backref("transposed_prediction3", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))

class Transposed_prediction4(Base):
### Association object
    __tablename__= "transposed_prediction4"

    id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    num_1 = Column(Float, nullable=True)
    num_2 = Column(Float, nullable=True)
    num_3 = Column(Float, nullable=True)
    num_4 = Column(Float, nullable=True)
    num_5 = Column(Float, nullable=True)
    num_6 = Column(Float, nullable=True)
    num_7 = Column(Float, nullable=True)
    num_8 = Column(Float, nullable=True)
    num_9 = Column(Float, nullable=True)
    num_10= Column(Float, nullable=True)

    user = relationship("User", backref=backref("transposed_prediction4", order_by=id))
    # item = relationship("Item", backref=backref("recommendations", order_by=id))

class Recrating(Base):
### Association object
    __tablename__= "recrating"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_rating_1 = Column(Integer, nullable = True)
    user_rating_2 = Column(Integer, nullable = True)
    user_rating_3 = Column(Integer, nullable = True)
    user_rating_4 = Column(Integer, nullable = True)
    user_rating_5 = Column(Integer, nullable = True)
    user_rating_6 = Column(Integer, nullable = True)
    user_rating_7 = Column(Integer, nullable = True)
    user_rating_8 = Column(Integer, nullable = True)
    user_rating_9 = Column(Integer, nullable = True)
    user_rating_10 = Column(Integer, nullable = True)
    rec_rating_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("recrating", order_by=id))

class Userrating(Base):
### Association object
    __tablename__= "userrating"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    novel_rating_1 = Column(Integer, nullable = True)
    novel_rating_2 = Column(Integer, nullable = True)
    novel_rating_3 = Column(Integer, nullable = True)
    novel_rating_4 = Column(Integer, nullable = True)
    novel_rating_5 = Column(Integer, nullable = True)
    novel_rating_6 = Column(Integer, nullable = True)
    novel_rating_7 = Column(Integer, nullable = True)
    novel_rating_8 = Column(Integer, nullable = True)
    novel_rating_9 = Column(Integer, nullable = True)
    novel_rating_10 = Column(Integer, nullable = True)
    unexp_find_rating_1 = Column(Integer, nullable = True)
    unexp_find_rating_2 = Column(Integer, nullable = True)
    unexp_find_rating_3 = Column(Integer, nullable = True)
    unexp_find_rating_4 = Column(Integer, nullable = True)
    unexp_find_rating_5 = Column(Integer, nullable = True)
    unexp_find_rating_6 = Column(Integer, nullable = True)
    unexp_find_rating_7 = Column(Integer, nullable = True)
    unexp_find_rating_8 = Column(Integer, nullable = True)
    unexp_find_rating_9 = Column(Integer, nullable = True)
    unexp_find_rating_10 = Column(Integer, nullable = True)
    unexp_recom_rating_1 = Column(Integer, nullable = True)
    unexp_recom_rating_2 = Column(Integer, nullable = True)
    unexp_recom_rating_3 = Column(Integer, nullable = True)
    unexp_recom_rating_4 = Column(Integer, nullable = True)
    unexp_recom_rating_5 = Column(Integer, nullable = True)
    unexp_recom_rating_6 = Column(Integer, nullable = True)
    unexp_recom_rating_7 = Column(Integer, nullable = True)
    unexp_recom_rating_8 = Column(Integer, nullable = True)
    unexp_recom_rating_9 = Column(Integer, nullable = True)
    unexp_recom_rating_10 = Column(Integer, nullable = True)
    diversity_rating_1 = Column(Integer, nullable = True)
    diversity_rating_2 = Column(Integer, nullable = True)
    diversity_rating_3 = Column(Integer, nullable = True)
    diversity_rating_4 = Column(Integer, nullable = True)
    diversity_rating_5 = Column(Integer, nullable = True)
    diversity_rating_6 = Column(Integer, nullable = True)
    diversity_rating_7 = Column(Integer, nullable = True)
    diversity_rating_8 = Column(Integer, nullable = True)
    diversity_rating_9 = Column(Integer, nullable = True)
    diversity_rating_10 = Column(Integer, nullable = True)
    unexp_implic_1 = Column(Integer, nullable = True)
    unexp_implic_2 = Column(Integer, nullable = True)
    unexp_implic_3 = Column(Integer, nullable = True)
    unexp_implic_4 = Column(Integer, nullable = True)
    unexp_implic_5 = Column(Integer, nullable = True)
    unexp_implic_6 = Column(Integer, nullable = True)
    unexp_implic_7 = Column(Integer, nullable = True)
    unexp_implic_8 = Column(Integer, nullable = True)
    unexp_implic_9 = Column(Integer, nullable = True)
    unexp_implic_10 = Column(Integer, nullable = True)
    rating_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("userrating", order_by=id))


class User_Choice(Base):
### Association object
    __tablename__= "userchoice"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))

    round = Column(Integer, nullable = True)
    user_choice = Column(Integer, nullable = True)
    choice_time = Column(DateTime, server_default=func.now())
    rec = Column(String(512))

    user = relationship("User", backref=backref("userchoice", order_by=id))


class Feedback(Base):
### Association object
    __tablename__= "feedback"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    Manip1 = Column(Integer, nullable=True)
    Manip2 = Column(Integer, nullable=True)
    Manip3 = Column(Integer, nullable=True)
    Mech11 = Column(Integer, nullable=True)
    Mech12 = Column(Integer, nullable=True)
    Mech21 = Column(Integer, nullable=True)
    Mech22 = Column(Integer, nullable=True)
    Control1 = Column(Integer, nullable=True)
    Control2 = Column(Integer, nullable=True)
    Control3 = Column(Integer, nullable=True)
    Control4 = Column(Integer, nullable=True)
    Control5 = Column(Integer, nullable=True)
    feedback_time = Column(DateTime, server_default=func.now())
    round = Column(Integer, nullable = True)
    algo_name = Column(String(256))

    user = relationship("User", backref=backref("feedback", order_by=id))



class Within_feedback(Base):
### Association object
    __tablename__= "within_feedback"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    within_unexp_find = Column(Integer, nullable = True)
    within_unexp_implicit = Column(Integer, nullable = True)
    within_novel = Column(Integer, nullable = True)
    within_diversity = Column(Integer, nullable = True)
    within_satisfaction = Column(Integer, nullable = True)
    any_feedback = Column(String(512), nullable = True)
    feedback_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("within_feedback", order_by=id))



# class Algo(Base):
#     __tablename__ = "algo"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     algorithm = Column(String(128))
#     train_mae = Column(Float, nullable=True)
#     test_mae = Column(Float, nullable=True)
#     train_rmse = Column(Float, nullable=True)
#     test_rmse = Column(Float, nullable=True)
#     algo_time = Column(DateTime, server_default=func.now())
#
#     user = relationship("User", backref=backref("algo", order_by=id))



class Algo(Base):
    __tablename__ = "algo"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    algorithm = Column(String(128))
    algo_time = Column(DateTime, server_default=func.now())
    round = Column(Integer)

    user = relationship("User", backref=backref("algo", order_by=id))


class Current_algo(Base):
### Association object
    __tablename__= "current_algo"

    id = Column(Integer, primary_key = True)
    algorithm = Column(String(256), nullable = False)
    update_time = Column(DateTime, server_default=func.now())


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey('users.id'))
    algorithm = Column(String(128))
    train_mae = Column(Float, nullable=True)
    test_mae = Column(Float, nullable=True)
    train_rmse = Column(Float, nullable=True)
    test_rmse = Column(Float, nullable=True)
    algo_train_time = Column(DateTime, server_default=func.now())
    # user = relationship("User", backref=backref("algo", order_by=id))


class Numeric_predictions(Base):
### Association object
    __tablename__= "numeric_predictions"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    predicted_rating = Column(Float,nullable=True)
    algorithm = Column(String(128))
    prediction_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("numeric_predictions", order_by=id))
    item = relationship("Item", backref=backref("numeric_predictions", order_by=id))


class PredictionLog(Base):
### Association object
    __tablename__= "predictionlogs"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pred_1 = Column(String(128), nullable=True)
    pred_2 = Column(String(128), nullable=True)
    pred_3 = Column(String(128), nullable=True)
    pred_4 = Column(String(128), nullable=True)
    pred_5 = Column(String(128), nullable=True)
    pred_6 = Column(String(128), nullable=True)
    pred_7 = Column(String(128), nullable=True)
    pred_8 = Column(String(128), nullable=True)
    pred_9 = Column(String(128), nullable=True)
    pred_10 = Column(String(128), nullable=True)
    algorithm = Column(String(128), nullable=True)
    pred_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("predictionlogs", order_by=id))


class ShoppingCart(Base):
### Association object
    __tablename__= "shoppingcart"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    cart_time = Column(DateTime, server_default=func.now())

    user = relationship("User", backref=backref("shoppingcart", order_by=id))
    item = relationship("Item", backref=backref("shoppingcart", order_by=id))


class PageviewLog(Base):
    __tablename__ = "pageview"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable = True)
    item_id = Column(Integer, nullable = True)
    page = Column(String(128), nullable=True)
    activity_type = Column(String(128), nullable=True)
    rating = Column(Integer, nullable=True)

    activity_time = Column(DateTime, server_default=func.now())


class SvdPredictions(Base):
    __tablename__ = 'svd_predictions'

    svd_id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(BigInteger, nullable = True)
    item_id = Column(BigInteger, nullable = True)
    prediction = Column(Float, nullable = True)
    id = Column(BigInteger, nullable = True)
    imdb_id = Column(String(128), nullable = True)
    tmdb_id = Column(Float, nullable = True)
    original_language = Column(Float, nullable = True)
    overview = Column(Text, nullable = True)
    popularity = Column(Float, nullable = True)
    runtime = Column(Float, nullable = True)
    tagline = Column(String(128), nullable = True)
    title = Column(String(1280), nullable = True)
    vote_average = Column(Float, nullable = True)
    vote_count = Column(Text, nullable = True)
    year = Column(BigInteger, nullable = True)
    genres = Column(String(128), nullable = True)
    poster_path = Column(Text, nullable = True)
    youtubeId = Column(Text, nullable = True)
    genre = Column(String(128), nullable = True)
    rank = Column(BigInteger, nullable = True)
    algo = Column(String(128), nullable = True)
    svd_entry_time = Column(DateTime, server_default=func.now())

### End class declarations
# start function declarations

'''def delete_svdpredictions2(user_id):
    #old_svd_predictions = SvdPredictions.query.filter_by(user_id=user_id).all()
    delete_query = delete(SvdPredictions).where(SvdPredictions.user_id == user_id)
    session.execute(delete_query)
    session.commit()
'''
def delete_svdpredictions(user_id):
    # Reflect the table structure
    metadata = MetaData(bind=engine)
    svd_predictions_table = Table('svd_predictions', metadata, autoload=True)
    delete_query = delete(svd_predictions_table).where(svd_predictions_table.c.user_id == user_id)
    session.execute(delete_query)
    session.commit()

def add_pageview(user_id, item_id, page, activity_type,rating):
    page_activity = PageviewLog(user_id=user_id,item_id=item_id, page=page, activity_type=activity_type,rating=rating)
    session.add(page_activity)
    session.commit()

#
# def add_algo(user_id, algorithm, train_mae, test_mae, train_rmse, test_rmse):
#     new_algo_usage = Algo(user_id=user_id, algorithm=algorithm, train_mae=train_mae,test_mae=test_mae, train_rmse=train_rmse,  test_rmse=test_rmse)
#     session.add(new_algo_usage)
#     session.commit()


def add_algo(user_id, algorithm, round):
    new_algo_usage = Algo(user_id=user_id, algorithm=algorithm, round=round)
    session.add(new_algo_usage)
    session.commit()


def add_training(algorithm, train_mae, test_mae, train_rmse, test_rmse):
    new_algo_train = Training(algorithm=algorithm, train_mae=train_mae,test_mae=test_mae, train_rmse=train_rmse,  test_rmse=test_rmse)
    session.add(new_algo_train)
    session.commit()


def get_user_from_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def get_user_from_id(id):
    user = User.query.filter_by(id=id).first()
    return user

# def get_sequence_from_id(id):
#     seq = Sequence.query.filter_by(id=id).first()
#     return seq

def get_item_from_id(id):
    item = Item.query.filter_by(id=id).first()
    return item

def create_user(email):

    user = User(
        email=email)  # , age=age, gender=gender, familiar=familiar, native=native, movie_count=movie_count, used=used, genre=genre)
    session.add(user)
    session.commit()
    added_user = User.query.filter_by(
        email=email).first()  # , age=age, gender=gender, familiar=familiar, native=native, movie_count=movie_count, used=used, genre=genre
    new_user_id = added_user.id
    # query = text("INSERT INTO ratings SELECT null as id,u.id as user_id, i.id as item_id, null as rating, null as text_rating, NOW() as user_add_time FROM items as i CROSS JOIN users as u WHERE u.id = :param")
    # session.execute(query.format(user = new_user_id), {'param': user})
    session.execute(text(
        "INSERT INTO ratings SELECT null as id,u.id as user_id, i.id as item_id, null as rating, null as text_rating, NOW() as user_add_time FROM items as i CROSS JOIN users as u WHERE u.id = {user}".format(
            user=new_user_id)))
    session.commit()


def add_user_info(user_id, old_user_id, age, gender, familiar, native, movie_count, used, genre,expec,trustlos,manipmech1,manipmech2,reactance):
    new_user_info = User_Info(user_id=user_id, old_user=old_user_id, age=age, gender=gender, famil=familiar, native=native, movie_count=movie_count, experience=used, favorite_genre=genre,expec = expec ,trustlos = trustlos , manipmech1=manipmech1,manipmech2=manipmech2 , reactance = reactance)
    session.add(new_user_info)
    session.commit()

def show_item_details(id):
    item = Rating.query.filter_by(item_id=id).all()
    return item

def add_rating(item_id, user_id, rating,text_rating):
    rating = Rating(item_id=item_id, user_id=user_id, rating=rating,text_rating=text_rating)
    session.add(rating)
    session.commit()

def is_rating(user_id, item_id):
    rating = Rating.query.filter_by(user_id=user_id, item_id=item_id).first()
    return rating

def update_rating(user_id, item_id, new_rating,new_text_rating):
    old_rating = Rating.query.filter_by(user_id=user_id, item_id=item_id).first()
    old_rating.rating = new_rating
    old_rating.text_rating=new_text_rating
    session.commit()


def show_current_algo(id):
    algo = Current_algo.query.filter_by(id=id).all()
    return algo


def update_current_algo(id, algorithm):
    old_algo = Current_algo.query.filter_by(id=id).first()
    old_algo.id = id
    old_algo.algorithm=algorithm
    session.commit()
    # return old_algo


def update_table(df, table, engine):
    temp_table = table+'_temp'
    df.to_sql(temp_table, engine, if_exists='replace', index=False)
    engine.execute(f"INSERT IGNORE INTO {table} SELECT * FROM {temp_table}")
    engine.execute(f'DROP TABLE {temp_table}')
    session.commit()



def add_new_item(user_id, item_id, rating,text_rating):
    new_rating = Rating(user_id=user_id, item_id=item_id, rating=rating,text_rating=text_rating)
    session.add(new_rating)
    session.commit()


def delete_recommendations1(id):
    session.execute(text("DELETE FROM recommendations1 WHERE id={id}".format(id = id)))
    #print("#" * 100, f"DELETE FROM recommendations1 WHERE id={id}")
    session.commit()

def delete_transposed_prediction1(id):
    session.execute(text("DELETE FROM transposed_prediction1 WHERE id={id}".format(id = id)))
    #print("#"*100, f"DELETE FROM transposed_prediction1 WHERE id={id}")
    session.commit()
#

def delete_numeric_predictions1(id):
    session.execute(text("DELETE FROM numeric_predictions WHERE user_id={id}".format(id = id)))
    session.commit()
#
# def delete_numeric_predictions2():
#     session.execute("DELETE FROM transposed_prediction2")
#     session.commit()
#
# def delete_numeric_predictions3():
#     session.execute("DELETE FROM transposed_prediction3")
#     session.commit()
#
# def delete_numeric_predictions4():
#     session.execute("DELETE FROM transposed_prediction4")
#     session.commit()

# def calculate_recommendations_rec_1():
    # compute_recommendations1()
    # session.commit()

# def calculate_recommendations_rec_2():
    # compute_recommendations2()
    # session.commit()

def show_recommendations1(id):
    rec = Recommendations1.query.filter_by(id=id).first()
    pred_1=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_1).first()
    pred_2=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_2).first()
    pred_3=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_3).first()
    pred_4=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_4).first()
    pred_5=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_5).first()
    pred_6=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_6).first()
    pred_7=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_7).first()
    pred_8=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_8).first()
    pred_9=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_9).first()
    pred_10=Item.query.filter_by(id=Recommendations1.query.filter_by(id=id).first().pred_10).first()
    return rec, pred_1, pred_2, pred_3, pred_4, pred_5, pred_6,pred_7, pred_8, pred_9,pred_10


def show_transposed_prediction1(id):
    tp_1 = Transposed_prediction1.query.filter_by(id=id).first()
    return tp_1

def show_transposed_prediction2(id):
    tp_2 = Transposed_prediction2.query.filter_by(id=id).first()
    return tp_2

def show_transposed_prediction3(id):
    tp_3 = Transposed_prediction3.query.filter_by(id=id).first()
    return tp_3

def show_transposed_prediction4(id):
    tp_4 = Transposed_prediction4.query.filter_by(id=id).first()
    return tp_4




def add_rec_rating(user_id,user_rating_1,user_rating_2,user_rating_3,user_rating_4,user_rating_5,user_rating_6,user_rating_7,user_rating_8,user_rating_9,user_rating_10):
    rec_rating = Recrating(user_id=user_id,user_rating_1=user_rating_1,user_rating_2=user_rating_2,user_rating_3=user_rating_3,user_rating_4=user_rating_4,user_rating_5=user_rating_5,user_rating_6=user_rating_6,user_rating_7=user_rating_7,user_rating_8=user_rating_8,user_rating_9=user_rating_9,user_rating_10=user_rating_10)
    session.add(rec_rating)
    session.commit()




def add_user_rating(user_id,novel_rating_1,novel_rating_2,novel_rating_3,novel_rating_4,novel_rating_5,novel_rating_6,novel_rating_7,novel_rating_8,novel_rating_9,novel_rating_10,
    unexp_find_rating_1,unexp_find_rating_2,unexp_find_rating_3,unexp_find_rating_4,unexp_find_rating_5,unexp_find_rating_6,unexp_find_rating_7,unexp_find_rating_8,unexp_find_rating_9,unexp_find_rating_10,
    unexp_recom_rating_1,unexp_recom_rating_2,unexp_recom_rating_3,unexp_recom_rating_4,unexp_recom_rating_5,unexp_recom_rating_6,unexp_recom_rating_7,unexp_recom_rating_8,unexp_recom_rating_9,unexp_recom_rating_10,
    diversity_rating_1,diversity_rating_2,diversity_rating_3,diversity_rating_4,diversity_rating_5,diversity_rating_6,diversity_rating_7,diversity_rating_8,diversity_rating_9,diversity_rating_10,
    unexp_implic_1,unexp_implic_2,unexp_implic_3,unexp_implic_4,unexp_implic_5,unexp_implic_6,unexp_implic_7,unexp_implic_8,unexp_implic_9,unexp_implic_10):
    user_rating = Userrating(user_id=user_id,novel_rating_1=novel_rating_1,novel_rating_2=novel_rating_2,novel_rating_3=novel_rating_3,novel_rating_4=novel_rating_4,novel_rating_5=novel_rating_5,novel_rating_6=novel_rating_6,novel_rating_7=novel_rating_7,novel_rating_8=novel_rating_8,novel_rating_9=novel_rating_9,novel_rating_10=novel_rating_10,
    unexp_find_rating_1=unexp_find_rating_1,unexp_find_rating_2=unexp_find_rating_2,unexp_find_rating_3=unexp_find_rating_3,unexp_find_rating_4=unexp_find_rating_4,unexp_find_rating_5=unexp_find_rating_5,unexp_find_rating_6=unexp_find_rating_6,unexp_find_rating_7=unexp_find_rating_7,unexp_find_rating_8=unexp_find_rating_9,unexp_find_rating_9=unexp_find_rating_9,unexp_find_rating_10=unexp_find_rating_10,
    unexp_recom_rating_1=unexp_recom_rating_1,unexp_recom_rating_2=unexp_recom_rating_2,unexp_recom_rating_3=unexp_recom_rating_3,unexp_recom_rating_4=unexp_recom_rating_4,unexp_recom_rating_5=unexp_recom_rating_5,unexp_recom_rating_6=unexp_recom_rating_6,unexp_recom_rating_7=unexp_recom_rating_7,unexp_recom_rating_8=unexp_recom_rating_8,unexp_recom_rating_9=unexp_recom_rating_9,unexp_recom_rating_10=unexp_recom_rating_10,
    diversity_rating_1=diversity_rating_1,diversity_rating_2=diversity_rating_2,diversity_rating_3=diversity_rating_3,diversity_rating_4=diversity_rating_4,diversity_rating_5=diversity_rating_5,diversity_rating_6=diversity_rating_6,diversity_rating_7=diversity_rating_7,diversity_rating_8=diversity_rating_8,diversity_rating_9=diversity_rating_9,diversity_rating_10=diversity_rating_10,
    unexp_implic_1=unexp_implic_1, unexp_implic_2=unexp_implic_2,unexp_implic_3=unexp_implic_3,unexp_implic_4=unexp_implic_4,unexp_implic_5=unexp_implic_5,unexp_implic_6=unexp_implic_6,unexp_implic_7=unexp_implic_7,unexp_implic_8=unexp_implic_8,unexp_implic_9=unexp_implic_9,unexp_implic_10=unexp_implic_10)
    session.add(user_rating)
    session.commit()


def add_user_choice(user_id, user_choice, round, rec):
    new_choice = User_Choice(user_id=user_id,user_choice=user_choice, round=round, rec=rec)
    session.add(new_choice)
    session.commit()

def add_feedback(user_id,round,algo_name,Manip1,Manip2,Manip3,Mech11,Mech12,Mech21, Mech22, Control1,Control2,Control3,Control4,Control5):
    new_feedback = Feedback(user_id=user_id,round=round,algo_name=algo_name,Manip1=Manip1, Manip2=Manip2, Manip3=Manip3, Mech11=Mech11, Mech12=Mech12, Mech21=Mech21, Mech22=Mech22, Control1 = Control1,Control2 = Control2,Control3 = Control3,Control4 = Control4,Control5 = Control5)
    session.add(new_feedback)
    session.commit()
def add_within_feedback(user_id,within_unexp_find, within_unexp_implicit, within_novel, within_diversity, within_satisfaction, any_feedback):
    new_within_feedback = Within_feedback(user_id=user_id,within_unexp_find=within_unexp_find, within_unexp_implicit=within_unexp_implicit, within_novel=within_novel,
    within_diversity=within_diversity, within_satisfaction=within_satisfaction,any_feedback=any_feedback)
    session.add(new_within_feedback)
    session.commit()



def add_cart(user_id, item_id):
    cart = ShoppingCart(user_id=user_id, item_id=item_id)
    session.add(cart)
    session.add(cart)
    session.commit()


def delete_cart(user_id, item_id):
    del_cart = ShoppingCart(user_id=user_id, item_id=item_id)
    session.expunge(del_cart)
    session.commit()


# def view_cart(user_id, item_id):
#     viewer = ShoppingCart.query.filter_by(user_id=user_id, item_id=item_id).first()
#     return viewer

def view_shoppingcart(id):
    cart = ShoppingCart.query.filter_by(id=id).first()
    # cart = ShoppingCart.query.filter_by(id=id).first()
    return cart

def delete_initial_ratings(id):
    session.execute(text("DELETE FROM ratings WHERE user_id={id}".format(id = id)))
    #print("#" * 100, f"DELETE FROM recommendations1 WHERE id={id}")
    session.commit()


# only to create Database
def create_tables():
    Base.metadata.create_all(engine)


def main():

    #Uncomment while creating tables
    #create_tables()

    #Uncomment to load data
    '''
    df_ratings = pd.read_csv("./data/ratings.csv", low_memory=False, encoding='UTF-8')
    df_ratings = df_ratings.rename(columns={'movie_id': 'item_id'})
    df_ratings = df_ratings.rename(columns={'timestamp':'text_rating'})
    table_name = "ratings"
    # Use the 'if_exists' parameter to specify what to do if the table already exists ('replace', 'append', or 'fail')
    df_ratings.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    df_ratings_data = pd.read_sql('SELECT * FROM ratings;', con=engine)
    print(df_ratings_data.columns)

    print(df_ratings_data.head(10))

    df_items = pd.read_csv("./data/items.csv", low_memory=False, encoding='UTF-8')
    table_name = "items"

    # Use the 'if_exists' parameter to specify what to do if the table already exists ('replace', 'append', or 'fail')
    df_items.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    df_items_data = pd.read_sql('SELECT * FROM items;', con=engine)
    print(df_items_data.columns)
    print(df_items_data.head(10))

    df_current_algo = pd.read_csv("./data/current_algo.csv", low_memory=False, encoding='UTF-8')
    table_name = "current_algo"
    # Use the 'if_exists' parameter to specify what to do if the table already exists ('replace', 'append', or 'fail')
    df_current_algo.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    df_current_algo_data = pd.read_sql('SELECT * FROM current_algo;', con=engine)
    print(df_current_algo_data.columns)

    print(df_current_algo_data.head(4))
    '''


#if the name of the algos change then make changes in current_algo table as well.
print("Done")


if __name__ == "__main__":
    main()
