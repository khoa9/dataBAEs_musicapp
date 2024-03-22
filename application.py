
# importing the model file and required packages for the platform. Primarily includes flask and sqlalchemy modules

from flask import Flask, render_template, redirect, request, flash, session, url_for

import model
import pandas as pd
import vectorImpl
pd.options.mode.chained_assignment = None
import logging



logging.basicConfig(filename='error.log',level=logging.DEBUG)


application = Flask(__name__)
app = application

#app.config['REDIS_URL'] = "redis://localhost:6379/0"
#redis_store = FlaskRedis(app)
#redis_conn = Redis.from_url(app.config['REDIS_URL'])
#queue = Queue(connection=redis_conn)


app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567'

@app.route("/")

def index():
    return render_template("index.html")

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


@app.route("/find_similarity")
def find_similarity(id, round=0):

    vectorImpl.similarity()






    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type= 'used recommender ' + str(algo1_id[0].algorithm)[13:].upper(), rating=None) #pageview

    model.add_pageview(user_id=session["user"], item_id=None, page="recommender_algorithm", activity_type="finish recommender computation", rating=None) #pageview
    # job = queue.enqueue(task_function, user_id, id,round)
    # job.delete()
    return redirect(url_for('view_recommendations', id=id,round=round))

# Showing recommendations. Top 10 are taken by prediction value.
@app.route("/view_recommendations/<int:id>/<int:round>")
def view_recommendations(id,round):


   # code to get the recommendations and display


    return render_template(f"show_similar_songs", id=id)


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

