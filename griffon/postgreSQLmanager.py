__author__ = 'Waterstrider'

import psycopg2

import DatabaseInfo


class DBmanager:
    def __init__(self):
        self.conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" % (
                    DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        self.cur = self.conn.cursor()

    def query(self, statement):
        self.cur.execute(statement)
        self.conn.commit()
        return self.cur.fetchall()