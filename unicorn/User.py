__author__ = 'Shiraga-P'

import psycopg2

import DatabaseInfo


class User():

    def __init__(self, user_id):
        self.user_id = user_id

        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        cur.execute("SELECT * from users WHERE users.id=%s", (self.user_id,))
        row = cur.fetchall()[0]
        self.username = row[1]
        self.password = row[2]
        self.email = row[3]
        self.firstname = row[4]
        self.lastname = row[5]
        self.address1 = row[6]
        self.address2 = row[7]
        self.province = row[8]
        self.country = row[9]
        self.zipcode = row[10]
        self.phone = row[11]
        conn.commit()

        cur.close()
        conn.close()