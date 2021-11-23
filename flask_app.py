
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from db import get_db_conn


app=Flask(__name__, static_url_path='/static')
app.secret_key = 'Bruce Wayne is Spiderman'

conn = get_db_conn

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   pass

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   pass

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))





# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    app.run()

