
# importing the model file and required packages for the platform. Primarily includes flask and sqlalchemy modules

from flask import Flask, render_template, redirect, request, flash, session, url_for
#from flask_session import Session
#from flask_redis import FlaskRedis
#from redis import Redis
#from rq import Queue
import model
from sqlalchemy.orm import joinedload
from threading import Thread
import time
import pandas as pd
pd.options.mode.chained_assignment = None
import csv
from sqlalchemy import text
from random import randint, choice
import random
import treatment1
import treatment2
import treatment3
import treatment1_decoy
import control
#import pyautogui
import time
import logging
from surprise import SVD
from sqlalchemy import create_engine
import config


logging.basicConfig(filename='error.log',level=logging.DEBUG)


application = Flask(__name__)
app = application

#app.config['REDIS_URL'] = "redis://localhost:6379/0"
#redis_store = FlaskRedis(app)
#redis_conn = Redis.from_url(app.config['REDIS_URL'])
#queue = Queue(connection=redis_conn)


app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567'
algos = ['control', 'treatment1', 'treatment2' ,'treatment3'] #pre-defined algo order

#seqs = {0: [2, 0, 1], 1: [0, 2, 1], 2: [1, 2, 0], 3: [0, 1, 2],
#4: [1, 0, 2], 5: [2, 0, 1]} #pre-defined user sequences

#seqs = {0: [0,1 ], 1: [1,0]} #pre-defined user sequences

seqs = {0:[0,1,2, 3 ], 1:[1,0,3,2],2:[2,1,3,0],3:[3,0,1,2]} #pre-defined user sequences

# seqs = {0: [0, 1, 2], 1: [0, 2, 1], 2: [1, 2, 0], 3: [0, 1, 2],
# 4: [1, 0, 2], 5: [2, 0, 1]} ## Correct one should be like this

html_number = {0:0, 1:1, 2:2, 3:3} #pre-defined user sequences

# Global Variable Indicating Computations are Complete
Computed = 0

def run_computations(user_id):
    global Computed
    print('Inside Run computations...')
    #print(f"Thread Status: {threading.current_thread().name}")
    #process = psutil.Process()
    #print(f"Memory Usage: {process.memory_info().rss / (1024 ** 2):.2f} MB")
    #time.sleep(5)
    #control.compute_recommendations_to_csv(user_id=user_id)
    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]
    algo_name = seq_names[0]
    #algo_name="control"
    Computed = 1
    if(algo_name.__eq__("control")):
         Computed = 1
         control.compute_recommendations_to_csv(user_id=user_id)
         Computed = 2
    elif(algo_name.__eq__("treatment1")):
        Computed = 1
        treatment1.compute_recommendations_to_csv(user_id=user_id)
        Computed = 2
    elif (algo_name.__eq__("treatment2")):
        Computed = 1
        treatment2.compute_recommendations_to_csv(user_id=user_id)
        Computed = 2
    elif (algo_name.__eq__("treatment3")):
        Computed = 1
        treatment3.compute_recommendations_to_csv(user_id=user_id)
        Computed = 2

    print('Computing Finished.')
    return None

@app.route("/")

def index():
    return render_template("index.html")

# Decorator for the login, signup and instructions pages. Each decorator may point to either an update action (e.g filling in signup/login forms) or an
# HTML page found in the templates folder.

@app.route("/install")
def install_surprise():
    import install_surprise
    return render_template("surprise_install.html")


@app.route("/login")
def show_login():
    model.add_pageview(user_id=None, item_id=None, page="login", activity_type="enter login page",rating=None) #pageview
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    user = model.get_user_from_email(email)

    if user == None:
        flash ("This user is not registered yet. You can sign up below.")
        model.add_pageview(user_id=None, item_id=None, page="login", activity_type="non-registered id / incorrect details",rating=None) #pageview
        return redirect('login')
    else:
        session['user'] = user.id
        model.add_pageview(user_id=user.id, item_id=None, page="login", activity_type="successful login",rating=None) #pageview
        return redirect(url_for('instructions_basic', id=user.id, round=0))


@app.route("/instructions_basic/<int:id>/<int:round>")
def instructions_basic(id=None,round=None):
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="start viewing instructions_basic", rating=None) #pageview

    user_id = session['user']
    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]
    algo_num = user_sequence[round] # number of the current algorithm
    return render_template("instructions_basic.html", id=id, round=round)

@app.route("/instructions/<int:id>/<int:round>", methods=["POST", "GET"])
def instructions(id=None,round=None):
    engine = create_engine(config.DB_URI, echo=True)
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="start viewing instructions", rating=None) #pageview
    user_id = session['user']
    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]
    algo_num = user_sequence[round] # number of the current algorithm

    if round == 0:
        item_ids = request.form.getlist('item_id')
        user_ratings = request.form.getlist('user_rating')
        titles = request.form.getlist('titles')
        user = [user_id]*100
        combined_df = pd.DataFrame(list(zip(user, titles,item_ids,user_ratings)), columns=['user_id','title', 'item_id', 'rating'])
        #combined_df.to_csv('./data/user_selections.csv')
        combined_df.to_sql('user_selections', engine, if_exists='append', index=False)  # if_exists='append'
        model.delete_initial_ratings(user_id)
        for index, row in combined_df.iterrows():
            user_rating = row['rating']  # Extract the value of the "rating" column
            item_id = row['item_id']
            if user_rating != "null":  # Check if the "rating" column value is between 0 and 10
                model.add_rating(item_id,user_id,user_rating,"")


        thr = Thread(target=run_computations, args=[user_id])
        thr.start()
        #run_computations(user_id)


    # do not proceed until computation is done.
    if Computed <= 1: #computed = {0:not started, 1:started, 2:finished}
        flash('')
        return render_template("instructions_personalized.html", id=id, round=round)

    if algo_num in (0,2):
         return render_template("instructions_nonPersonalized.html", id=id, round=round)
    else:
         return render_template("instructions_personalized.html", id=id, round=round)


@app.route("/signup")
def show_signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def make_new_account():
    email = request.form.get("email2")
    user = model.get_user_from_email(email)

    if user == None:
        model.create_user(email)
        model.add_pageview(user_id=None, item_id=None, page="login", activity_type="already_registered id / instructed to sign in",rating=None) #pageview
    else:
        flash("This user was already registered. You are now signed in.")


    user = model.get_user_from_email(email)
    session['user'] = user.id
    model.add_pageview(user_id=None, item_id=None, page="signup", activity_type="successful signup",rating=None) #pageview
    return redirect(url_for('instructions_basic', id=user.id, round=0))

@app.route("/user_list/", defaults={"page":1})
@app.route("/user_list/<int:page>")
def user_list(page):
    perpage = 50
    pages = (model.session.query(model.User).count()) / perpage
    back_one = page - 1
    forward_one = page + 1
    user_list = model.session.query(model.User).limit(perpage).offset((page*perpage) -perpage).all()
    return render_template("user_list.html", users=user_list, pages=pages, back=back_one, forward=forward_one)

# Decorator for the user-items pages. Various attributes are queried for each item and show on the respective pages.
# view_item shows a more detailed item view

@app.route("/view_user/<int:id>/<int:round>")
def show_user_details(id,round):
    user_id = session["user"]
    model.add_pageview(user_id=user_id, item_id=None, page="Movie List", activity_type="enter Movie List",rating=None) #pageview


    #user = model.session.query(model.User).filter_by(id=id).join(model.Rating).join(model.Item).first()

    # for the second round for the same user, we will be able to select only those items which were selected by the user in round 1.

    ratings = model.session.query(model.Rating).options(joinedload(model.Rating.item)).filter_by(user_id=id).all()
    ratings = [r for r in ratings if r != None] # remove None
    ratings = [r for r in ratings if r.item != None] # remove None
    ratings = [r for r in ratings if int(r.item.year) >= 2005] # remove old
    ratings = sorted(ratings, key=lambda x: float(x.item.vote_count), reverse=True)[0:100]
    return render_template("view_user.html", user=user_id, ratings=ratings, round=round)


#votecount and voteaverage - this is popularity
#Ratings is the voteaverage not ratings


@app.route("/algo")
def view_algo():
    algo1_id = model.show_current_algo(1)
    model.add_pageview(user_id=None, item_id=None, page="current_recommender", activity_type= 'current recommender 1 is ' + str(algo1_id[0].algorithm)[13:].upper(), rating=None) #pageview
    algo2_id = model.show_current_algo(2)
    model.add_pageview(user_id=None, item_id=None, page="current_recommender", activity_type= 'current recommender 2 is ' + str(algo2_id[0].algorithm)[13:].upper(), rating=None) #pageview
    algo3_id = model.show_current_algo(3)
    model.add_pageview(user_id=None, item_id=None, page="current_recommender", activity_type= 'current recommender 3 is ' + str(algo3_id[0].algorithm)[13:].upper(), rating=None) #pageview
    algo4_id = model.show_current_algo(4)
    model.add_pageview(user_id=None, item_id=None, page="current_recommender", activity_type= 'current recommender 4 is ' + str(algo4_id[0].algorithm)[13:].upper(), rating=None) #pageview
    return render_template("algo.html", algo1_id=algo1_id, algo2_id=algo2_id) #prediction_items=prediction_items,

@app.route("/update_algo", methods=["POST"])
def update_algo():
    algorithm_1 = request.form.get("algorithm_1")
    algorithm_2 = request.form.get("algorithm_2")

    model.update_current_algo(id=1, algorithm=algorithm_1)
    model.update_current_algo(id=2, algorithm=algorithm_2)

    algorithm_3 = request.form.get("algorithm_3")
    algorithm_4 = request.form.get("algorithm_4")

    model.update_current_algo(id=1, algorithm=algorithm_3)
    model.update_current_algo(id=2, algorithm=algorithm_4)
    model.add_pageview(user_id=None, item_id=None, page="update_recommender", activity_type= 'updated recommenders', rating=None) #pageview
    return redirect(url_for('view_algo'))

@app.route("/view_item/<int:id>/<int:round>")
def view_item_details(id,round):
    item_ratings = model.show_item_details(id)
    item = item_ratings[0].item
    model.add_pageview(user_id=session["user"], item_id=item.id, page="item", activity_type="start item view",rating=None) #pageview
    return render_template("view_item.html", item=item, round=round) #prediction_items=prediction_items,

# Update_rating updates the rating for each item
@app.route("/update_rating/<int:round>", methods=["POST"])
def update_rating(round):
    new_rating = request.form.get("rating")
    item_id = request.form.get("item")
    new_text_rating = request.form.get("text_rating")
    user_id = session['user']
    model.update_rating(user_id, item_id, new_rating, new_text_rating)
    model.add_pageview(user_id=session["user"], item_id=item_id, page="item", activity_type="rate item",rating=new_rating) #pageview
    model.add_pageview(user_id=session["user"], item_id=item_id, page="item", activity_type="end item view",rating=None) #pageview
    return redirect(url_for('show_user_details', id=user_id, round=round))

# This decorator is used to run the recommenders when the user clicks on the calculate and show recommmendations button
# It starts by capturing the click itself, and then deletes previous recommendations corresponding to that user (they are stil stored in the ....... tablee)

@app.route("/recommend_compute/<int:id>/<int:round>")
def recsys_compute(id, round=0):
    global Computed
    print("Inside recommend compute")
    user_id = session['user']
    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="initialize recommender", rating=None) #pageview
    model.delete_recommendations1(id)
    model.delete_numeric_predictions1(id)
    #user_sequence = seqs[user_id % 6]
    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]

    if round == 0:
        while Computed == 1:
            time.sleep(5)
            #treatment1.compute_recommendations_to_csv(user_id=user_id)
            #control.compute_recommendations_to_csv(user_id=user_id)

    algo1_id = model.show_current_algo(user_sequence[round]+1)
    recommender1 = __import__(algo1_id[0].algorithm)

    model.add_algo(user_id=user_id, algorithm=str(algo1_id[0].algorithm)[13:].upper(), round=round)
    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type= 'used recommender ' + str(algo1_id[0].algorithm)[13:].upper(), rating=None) #pageview

    recommender1.compute_recommendations(user_id=user_id, recommendations1='recommendations1', transposed_prediction1='transposed_prediction1')
    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="finish recommender computation", rating=None) #pageview
    # job = queue.enqueue(task_function, user_id, id,round)
    # job.delete()
    return redirect(url_for('view_recommendations', id=id,round=round))


# Showing recommendations. Top 10 are taken by prediction value.
@app.route("/view_recommendations/<int:id>/<int:round>")
def view_recommendations(id,round):
    #user_id = id
    user_id = session['user']
    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]
    html_num = html_number[user_id % 4]
    algo_num = user_sequence[round]  # number of the current algorithm
    # personalized = algo_num in (1, 3)

    rec,pred_1, pred_2, pred_3, pred_4, pred_5, pred_6,pred_7, pred_8, pred_9,pred_10 = model.show_recommendations1(id)
    tp_1 = model.show_transposed_prediction1(id)
    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="start viewing recommendations", rating=None) #pageview

    return render_template(f"recommendations_personalized{html_num}.html", id=id, rec=rec, pred_1=pred_1, pred_2=pred_2,
                           pred_3=pred_3, pred_4=pred_4, pred_5=pred_5, pred_6=pred_6, pred_7=pred_7,
                           pred_8=pred_8, pred_9=pred_9, pred_10=pred_10, tp_1 = tp_1,
                           round=round)


@app.route("/choice/<int:id>/<int:round>", methods=["POST"])
def choice(id, round):
    user_id = session['user']
    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]
    algo_num = user_sequence[round] # number of the current algorithm
    time.sleep(5)
    user_choice = request.form.get("user_choice")
    __,pred_1, pred_2, pred_3, pred_4, pred_5, __,__, __, __,__  = model.show_recommendations1(user_id)
    rec = str((pred_1.title, pred_2.title, pred_3.title, pred_4.title, pred_5.title))
    model.add_user_choice(user_id, user_choice, round, rec)

    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations",
                       activity_type="submit choice", rating=None)  # pageview
    return redirect(url_for('to_overall_feedback', id=user_id, round=round))


@app.route("/view_recommended_item/<int:id>/<int:round>")
def view_recommended_item_details(id,round):
    item_ratings = model.show_item_details(id)
    item = item_ratings[0].item
    model.add_pageview(user_id=session["user"], item_id=item.id, page="item", activity_type="recommended item view",rating=None) #pageview
    return render_template("view_recommended_item.html", item=item, round=round) #prediction_items=prediction_items,

# Decorators for user feedback for recommendations. Include per-recommendation, overall and per-algorithm feedback
@app.route("/rate_recommendations", methods=["POST"])
def add_rec_rating():
    user_id = session['user']
    user_rating_1 = request.form.get("user_rating_1")
    user_rating_2 = request.form.get("user_rating_2")
    user_rating_3 = request.form.get("user_rating_3")
    user_rating_4 = request.form.get("user_rating_4")
    user_rating_5 = request.form.get("user_rating_5")
    user_rating_6 = request.form.get("user_rating_6")
    user_rating_7 = request.form.get("user_rating_7")
    user_rating_8 = request.form.get("user_rating_8")
    user_rating_9 = request.form.get("user_rating_9")
    user_rating_10 = request.form.get("user_rating_10")
    model.add_rec_rating(user_id,user_rating_1,user_rating_2,user_rating_3,user_rating_4,user_rating_5,user_rating_6,user_rating_7,user_rating_8,user_rating_9,user_rating_10)
    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="rate recommendations and finish view", rating=None) #pageview
    return redirect(url_for('to_overall_feedback', id=user_id))


# Overall feedback page
@app.route("/overall_feedback/<int:id>/<int:round>")
def to_overall_feedback(id,round):
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="start viewing overall feedback", rating=None) #pageview
    return render_template("feedback.html", id=id, round=round)


@app.route("/overall_feedback/<int:id>/<int:round>", methods=["POST"])
def overall_feedback(id,round):
    user_id = session['user']
    Manip1 = request.form.get("Manip1")
    Manip2 = request.form.get("Manip2")
    Manip3 = request.form.get("Manip3")
    Mech11 = request.form.get("Mech11 ")
    Mech12 = request.form.get("Mech12")
    Mech21 = request.form.get("Mech21")
    Mech22 = request.form.get("Mech22")
    Control1 = request.form.get("Control1")
    Control2 = request.form.get("Control2")
    Control3 = request.form.get("Control3")
    Control4 = request.form.get("Control4")
    Control5 = request.form.get("Control5")

    user_sequence = seqs[user_id % 4]
    seq_names = [algos[i] for i in user_sequence]

    algo_name = seq_names[round]
    model.add_feedback(user_id, round, algo_name, Manip1, Manip2, Manip3, Mech11, Mech12, Mech21, Mech22,
                       Control1, Control2, Control3, Control4, Control5)
    model.add_pageview(user_id=session["user"], item_id=None, page="feedback", activity_type="finish viewing and giving overall feedback", rating=None) #pageview
    return redirect(url_for('show_user_info', id=user_id, round=round))

    # if round in range(0,3):   # at round 1/2 show the instructions
    #     return redirect(url_for('instructions', id=user_id, round=round+1))
    # if round == 3:   # end. Move to the user info survey
    #     return redirect(url_for('show_user_info', id=user_id, round=round))
    # else:  # at round 2, just recompute
    #     return redirect(url_for('recsys_compute', id=user_id, round=round+1))


@app.route("/user_info/<int:id>/<int:round>")
def show_user_info(id, round):
    return render_template("user_info.html", id=id, round=round)

@app.route("/user_info/<int:id>/<int:round>", methods=["POST"])
def get_user_info(id, round):
    user_id = session["user"]
    old_user_id = request.form.get("old_user")
    age = request.form.get("age")
    gender = request.form.get("gender")
    familiar = request.form.get("famil")
    native = request.form.get("native")
    movie_count = request.form.get("movie_count")
    used = request.form.get("experience")
    genre = request.form.get("favorite_genre")
    expec = request.form.get("expec")

    trustlos = request.form.get("trustlos")
    manipmech1 = request.form.get("manipmech1")
    manipmech2 = request.form.get("manipmech2")
    reactance = request.form.get("reactance")
    model.add_user_info(user_id, old_user_id, age, gender, familiar, native, movie_count, used, genre,expec, trustlos,
                        manipmech1, manipmech2, reactance)
    model.add_pageview(user_id=user_id, item_id=None, page="user_info", activity_type="submitted user info survey", rating=None)  # pageview
    return redirect(url_for('thank_you', id=user_id, round=round))

    model.add_user_info(user_id, age, gender, familiar, native, movie_count, used, genre)
    model.add_pageview(user_id=user_id, item_id=None, page="user_info", activity_type="submitted user info survey",rating=None) #pageview
    return redirect(url_for('thank_you', id=user_id, round=round))


@app.route("/thank_you/<int:id>/<int:round>")
def thank_you(id,round):
    model.add_pageview(user_id=session["user"], item_id=None, page="thankyou", activity_type="viewed thank you page", rating=None) #pageview
    return render_template("thank_you.html", id=id, round=round)

# Page for comparison of algorithm 1 vs algorithm 2
@app.route("/view_combined_recommendations/<int:id>/<int:round>")
def view_combined_recommendations(id,round):
    rec,pred_1, pred_2, pred_3, pred_4, pred_5, pred_6,pred_7, pred_8, pred_9,pred_10 = model.show_recommendations1(id)
    rec2,pred_11, pred_12, pred_13, pred_14, pred_15, pred_16,pred_17, pred_18, pred_19,pred_20 = model.show_recommendations2(id)
    model.add_pageview(user_id=session["user"], item_id=None, page="recommendations", activity_type="start viewing combined recommendations", rating=None) #pageview
    return render_template("combined_recommendations.html", id=id, rec=rec, pred_1=pred_1, pred_2=pred_2,pred_3=pred_3, pred_4=pred_4,pred_5=pred_5, pred_6=pred_6, pred_7=pred_7, pred_8=pred_8, pred_9=pred_9, pred_10=pred_10,
    rec2=rec2,pred_11=pred_11, pred_12=pred_12, pred_13=pred_13, pred_14=pred_14, pred_15=pred_15, pred_16=pred_16,pred_17=pred_17, pred_18=pred_18, pred_19=pred_19,pred_20=pred_20, round=round)

# page for logout

@app.route("/logout")
def process_logout():
    model.add_pageview(user_id=session["user"], item_id=None, page="logout", activity_type="user logout", rating=None) #pageview
    session.clear()
    return redirect("/")

#apply_profiler(app)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #total_memory_usage = get_total_memory_usage()
    #print(f"Total memory usage of the application: {total_memory_usage:.2f} MiB")

