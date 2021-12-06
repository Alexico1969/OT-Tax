import sqlite3, os
from flask import g
import psycopg2
from urllib import parse
from helper import get_hashed_password, check_password
from datetime import date
import sys

todays_date = date.today()

def get_db_conn():

    conn = sqlite3.connect('OT-tax.db', check_same_thread=False)
    print("opened database")
    return conn

def create_invitation_codes(conn):
  # Create invitation codes

    cur = conn.cursor()

    query = '''Select * from invitation_codes'''
    result = cur.execute(query)
    data = result.fetchall()

    if len(data) == 0:
        query = '''insert into invitation_codes (code, times_used, remarks) values 
            ('Jv90_o!lskKv', 0, 'For OT admins'),
            ('KjmK091!$9an', 0, 'For OT members'),
            ('8iajhnbaa231', 0, 'Spare_01'),
            ('I98cann1h212', 0, 'Spare_02'),
            ('a981sjlowj12', 0, 'Test-01')
              '''
        conn.execute(query)
        conn.commit()
        print("Invitation codes created")
    else:
        print(len(data), "invitation codes found")

    return

def username_in_use(conn, usr):
    cur = conn.cursor()
    query = '''Select * from users where username=?'''
    result = cur.execute(query,(usr,))
    data = result.fetchall()
    if len(data) > 0:
        return True
    else:
        return False

def check_inv_code(conn, input):
    cur = conn.cursor()
    query = '''Select * from invitation_codes where code=?'''
    result = cur.execute(query, (input,))
    data = result.fetchall()
    if len(data) > 0:
        return True
    else:
        return False

def add_user(conn, name, username, password, roles, inv_code):
    cur = conn.cursor()

    hash = get_hashed_password(password)
    
    query = '''insert into users (name, username, password, roles) values (?,?,?,?)'''
    result = cur.execute(query, ( name, username, hash, roles))
    conn.commit()

    query = '''select times_used from invitation_codes where code=?'''
    result = cur.execute(query, (inv_code,))
    data = result.fetchone()
    counter = data[0]
    counter += 1
    query = '''update invitation_codes set times_used=? where code=?'''
    cur.execute(query, (counter, inv_code))
    
    conn.commit()
    print("user added")
    return


def password_checks_out(conn, username, password):
    cur = conn.cursor()
    query = '''Select password from users where username=?'''
    result = cur.execute(query,(username,))
    data = result.fetchone()
    if data:
        stored_password = data[0]
        if check_password(password,stored_password):
            return True
    return False

def get_name(conn, username):
    cur = conn.cursor()
    query = '''Select name from users where username=?'''
    result = cur.execute(query,(username,))
    data = result.fetchone()
    if data:
        name = data[0]
    else:
        name = "Hacker"
    return name

def get_all_users(conn):
    cur = conn.cursor()
    query = '''Select * from users'''
    result = cur.execute(query)
    data = result.fetchall()
    return data

def get_all_mutations(conn):
    cur = conn.cursor()
    query = '''Select * from mutations ORDER BY mutation_id DESC'''
    result = cur.execute(query)
    data = result.fetchall()
    return data

def get_this_month_mutations(conn):
    cur = conn.cursor()

    todays_month = todays_date.month
    todays_year = todays_date.year

    month = str(todays_year) + "-" + str(todays_month)

    print("**** month : ", month)

    query = '''Select * from mutations ORDER BY mutation_id  DESC'''
    result = cur.execute(query)
    data = result.fetchall()

    output = []

    for row in data:
        date = row[2]
        print("*** date: ", date)
        if month in date:
            output.append(row)

    return output

def get_all_goals(conn):
    cur = conn.cursor()
    query = '''Select * from monthly_goals'''
    result = cur.execute(query)
    data = result.fetchall()
    return data

def add_entry_data(conn, amount, date, donor, logged_by, remarks):
    cur = conn.cursor()
    query = '''insert into mutations(amount, date, donor, logged_by, remarks) values (?,?,?,?,?)'''
    cur.execute(query, ( amount, date, donor, logged_by, remarks))
    conn.commit()
    print("entry added")
    return

def add_goal_data(conn, month, amount, remarks):
    cur = conn.cursor()

    query = '''Select * from monthly_goals where month=?'''
    result = cur.execute(query, (month,))
    data = result.fetchall()

    if len(data) > 0:
        query = '''update monthly_goals set goal=? where month=?'''
        cur.execute(query, ( amount, month))
        print("entry updated")
    else:
        query = '''insert into monthly_goals(month, goal, remarks) values (?,?,?) '''
        cur.execute(query, ( month, amount, remarks))
        print("entry added")
    conn.commit()

    return

def this_months_total(conn):

    todays_month = todays_date.month

    cur = conn.cursor()
    query = '''Select * from mutations'''
    result = cur.execute(query)
    data = result.fetchall()
    
    total = 0

    if data:
        for row in data:
            temp = row[2].split("-")
            m = temp[1]
            if int(m) == int(todays_month):
                total += row[1]

    return total


def this_months_goal(conn):

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    todays_month = months[todays_date.month-1]
    todays_year = str(todays_date.year)

    search_str = todays_year + "/" + todays_month

    cur = conn.cursor()
    query = '''Select goal from monthly_goals where month=?'''
    result = cur.execute(query, (search_str,))
    data = result.fetchall()
    if data:
        output = data[0][0]
    else:
        output = 0
    return output



def execute_query(conn, query):
    result = "-"
    cur = conn.cursor()
    query = query

    try:
        result = cur.execute(query)
        conn.commit()
    except:
        result = "Error"

    print("query executed: ",query)
    return result
    