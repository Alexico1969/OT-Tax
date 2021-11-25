import sqlite3, os
from flask import g
import psycopg2
from urllib import parse

def create_tables(conn):

    # In case you want to clear a table
    # query = '''delete from table
    #        )    '''
    # conn.execute(query)
    # print("table cleared")

    # In case you want to drop a table
    # query = '''drop table mutations'''
    # conn.execute(query)
    # print("table dropped")


    # Create table users
    query = '''create table if not exists users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            roles TEXT NOT NULL
            )    '''
    conn.execute(query)

    # Create table mutations
    query = '''create table if not exists mutations (
            mutation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            date TEXT,
            donor TEXT,
            logged_by TEXT,
            remarks TEXT
            )    '''
    conn.execute(query)

    #create table monthly_data
    query = '''create table if not exists monthly_goals (
            mg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            goal INTEGER,
            remarks TEXT
            )    '''
    conn.execute(query)

    #create table invitation_codes
    query = '''create table if not exists invitation_codes(

                inv_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT,
                times_used INTEGER,
                remarks TEXT
                )'''

    conn.execute(query)

    #create table monthly_goals
    query = '''create table if not exists monthly_goals(

                mg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT,
                goal INTEGER,
                remarks TEXT
                )'''

    conn.execute(query)

    print("tables created where needed")