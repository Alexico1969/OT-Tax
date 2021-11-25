from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from db import get_db_conn, create_invitation_codes, username_in_use, check_inv_code
from db import add_user, get_all_users, password_checks_out, get_name
from tables import create_tables

app=Flask(__name__, static_url_path='/static')
app.secret_key = 'Bruce Wayne is Spiderman'

conn = get_db_conn()
create_tables(conn)
create_invitation_codes(conn)

@app.route('/')
def home_page():
    name=""
    if 'username' in session:
      username = session['username']
      name = get_name(conn, username)
    return render_template('home.html', user=name)

@app.route('/login', methods=['GET', 'POST'])
def login():

    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pssw1")
        check1 = not(username_in_use(conn, username))
        check2 = not(password_checks_out(conn, username, password))
        if  check1:
            print("check1: ", check1)
            message="username or password unknown"
        elif check2:
            print("check2: ", check2)
            message="username or password unknown"
        else:
            name = get_name(conn, username)
            message="Welcome, " + name
            session['username'] = username
            message = "Welcome, "
            desto = "/"
            return render_template('message.html', msg=message, name=name, desto=desto)

        
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
            message="Registration complete, you can now log in."
            return redirect(url_for('login'))


    return render_template('signup.html', msg=message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home_page'))


@app.route('/dump')
def dump():
    if 'username' in session:
        username = session['username']
        user_list = get_all_users(conn)
        return render_template('dump.html', users=user_list, user=username)
    else:
        message = "403 - Admins only !"
        desto = "/"
        return render_template('message.html', msg=message, desto=desto)


# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    app.run()

