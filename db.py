import sqlite3, os
from flask import g
import psycopg2
from urllib import parse

def get_db_conn():

    conn = sqlite3.connect('OT-tax.db')
    print("opened database")
    return conn