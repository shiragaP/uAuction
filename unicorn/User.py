__author__ = 'Shiraga-P'

import psycopg2

class User:

    def __init__(self, id, username, password):
        try:
            conn = psycopg2.connect("dbname='database SE Y2' user='postgres' host='localhost' password='admin' port='5432'")
        except:
            print('I am unable to connect to the database')
            return

        self.id = id
        self.username = username
        self.password = password
