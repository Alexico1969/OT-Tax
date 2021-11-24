
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from db import get_db_conn, create_invitation_codes, username_in_use, check_inv_code
from db import add_user, get_all_users
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

    message = ""

    if request.method == "POST":
       print("todo")
        


    return render_template('login.html', msg=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    message = ""

    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("pssw1")
        pconfirm = request.form.get("pssw2")
        inv_code = request.form.get("inv_code")

        if username_in_use(conn, username):
            message = "This username is already used"
        elif password != pconfirm:
            message = "Passwords don't match"
        elif not(check_inv_code(conn, inv_code)):
            message = "Unknown invitation code"
        else:
            roles="add_entry"
            add_user(conn, name, username, password, roles, inv_code)


    return render_template('signup.html', msg=message)

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))


@app.route('/dump')
def dump():
    user_list = get_all_users(conn)
    print("user_list", user_list)
    return render_template('dump.html', users=user_list)


# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    app.run()

