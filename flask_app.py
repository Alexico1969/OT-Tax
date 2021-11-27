from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from db import get_db_conn, create_invitation_codes, username_in_use, check_inv_code
from db import add_user, get_all_users, password_checks_out, get_name, get_all_mutations, get_all_goals
from db import add_entry_data, add_goal_data, this_months_total, this_months_goal,execute_query
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
    else:
        name = ""
    mutations = get_all_mutations(conn)
    
    donated = this_months_total(conn)
    monthly_goal = this_months_goal(conn)
    remainder = monthly_goal - donated
    if remainder < 0:
        remainder = 0
    monthly_goal = "{:,}".format(monthly_goal)
    remainder = "{:,}".format(remainder)
    donated = "{:,}".format(donated)
    
    return render_template('home.html', user=name, mutations=mutations, monthly_goal=monthly_goal, donated=donated, remainder=remainder)

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
        mutations = get_all_mutations(conn)
        goals = get_all_goals(conn)
        return render_template('dump.html', users=user_list, user=username, mutations=mutations, goals=goals)
    else:
        message = "403 - Admins only !"
        desto = "/"
        return render_template('message.html', msg=message, desto=desto)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if 'username' in session:
        username = session['username']

        if request.method == "POST":
            result = ""
            query = request.form.get("query")
            result = execute_query(conn, query)
            data = result.fetchall()
            message = "Result : " + str(result) + " Data = " + str(data)
            desto = "/query"
            return render_template('message.html', msg=message, desto=desto)


        return render_template('query.html')
    else:
        message = "403 - Admins only !"
        desto = "/"
        return render_template('message.html', msg=message, desto=desto)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if 'username' in session:
        username = session['username']

        if request.method == "POST":
            amount = request.form.get("amount")
            date = request.form.get("date")
            donor = request.form.get("donor")
            logged_by = request.form.get("logged_by")
            remarks = request.form.get("remarks")

            add_entry_data(conn, amount, date, donor, logged_by, remarks)

            name = ""
            message = "Entry added"
            session['username'] = username
            desto = "/add_entry"

            return render_template('message.html', msg=message, name=name, desto=desto)



        return render_template('add_entry.html', user=username)

    else:
        message = "403 - Admins only !"
        desto = "/"
        return render_template('message.html', msg=message, desto=desto)

@app.route('/add_goal', methods=['GET', 'POST'])
def add_goal():
    if 'username' in session:
        username = session['username']

        if request.method == "POST":
            year = request.form.get("year")
            month_temp = request.form.get("month")
            month = year + "/" + month_temp
            amount = request.form.get("amount")
            remarks = request.form.get("remarks")

            add_goal_data(conn, month, amount, remarks)

            name = ""
            message="Entry added" + name
            session['username'] = username
            desto = "/add_goal"

            return render_template('message.html', msg=message, name=name, desto=desto)



        return render_template('add_goal.html', user=username)

    else:
        message = "403 - Admins only !"
        desto = "/"
        return render_template('message.html', msg=message, desto=desto)





# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    app.run()

