
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from db import get_db_conn, create_invitation_codes
from helper import extract_username, extract_password
from tables import create_tables


app=Flask(__name__, static_url_path='/static')
app.secret_key = 'Bruce Wayne is Spiderman'

conn = get_db_conn()
create_tables(conn)
create_invitation_codes(conn)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        data = request.get_data("username")
        print("data:", data)
        converted = data.decode('UTF-8')
        print("converted:", converted)
        username = extract_username(converted)
        print("username:", username)
        password = extract_password(converted)
        print("password:", password)
        


    return render_template('login.html')

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

