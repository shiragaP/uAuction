__author__ = 'Shiraga-P'

import psycopg2

import DatabaseInfo


class User:
    def __init__(self, username):
        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        rows = cur.fetchall()

        for row in rows:
            if row[1] == username:
                self.id = row[0]
                self.username = row[1]
                self.firstname = row[3]
                self.lastname = row[4]
                self.address1 = row[5]
                self.address1 = row[6]
                self.province = row[7]
                self.country = row[8]
                self.zipcode = row[9]

    def print(self):
        print("ID:", self.id)
        print(self.firstname, self.lastname)
