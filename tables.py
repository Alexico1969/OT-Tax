import sqlite3, os
from flask import g
import psycopg2
from urllib import parse

def create_tables(conn):

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
            remarks TEXT
            )    '''
    conn.execute(query)

    #create table monthly_data
    query = '''create table if not exists monthly_data (
                md_id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            goal INTEGER,
            remarks TEXT
            )    '''
    conn.execute(query)
            
            
    print("tables created where needed")