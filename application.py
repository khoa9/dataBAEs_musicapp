
# importing the model file and required packages for the platform. Primarily includes flask and sqlalchemy modules

from flask import Flask, render_template, redirect, request, flash, session, url_for

import model
import pandas as pd
#import vectorImpl
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
    model.add_pageview(item_id=None, page="login", activity_type="successful login",rating=None) #pageview
    return redirect(url_for('instructions_basic'))


'''@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        # Save the file to the application folder
        file.save('/data/input_song.mp3')
        # Here you can process the data or extract any information you need
        # For example, let's pass the filename to the next page
        filename = file.filename
        return redirect('/next?filename=' + filename)
    return 'No file uploaded.'

@app.route('/next')
def next():
    filename = request.args.get('filename')
    # Pass the filename to the template
    return render_template('next.html', filename=filename)'''


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

