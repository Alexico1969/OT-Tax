import sqlite3, os
from flask import g
import psycopg2
from urllib import parse

def get_db_conn():

    conn = sqlite3.connect('OT-tax.db')
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
            ('I98cann1h212', 0, 'Spare_02')
              '''
        conn.execute(query)
        conn.commit()
        print("Invitation codes created")
    else:
        print(len(data), "invitation codes found")
    return