__author__ = 'Shiraga-P'

import psycopg2
import DatabaseInfo

def main():
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='localhost' password='admin' port='5432'" % ('database SE Y2', 'postgres'))
    except:
        print('I am unable to connect to the database')
        return
    cur = conn.cursor()
    cur.execute("SELECT pres_name from president")
    rows = cur.fetchall()
    print('\nShow me the databases:\n')
    for row in rows:
        print('   ', row[0])


def createDatabase():
    con = psycopg2.connect("host='%s' user='%s' password='%s'" %
                           (DatabaseInfo.host, DatabaseInfo.user, DatabaseInfo.password))
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute("CREATE DATABASE " + DatabaseInfo.dbname)
    cur.close()
    con.close()


def deleteTable():
    con = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                           (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    cur = con.cursor()
    cur.execute("DROP TABLE users CASCADE")
    cur.close()
    con.close()


def createTable():
    con = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                           (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute("""CREATE TABLE users(
                    id INT,
                    username VARCHAR (15),
                    password VARCHAR (15),
                    firstName VARCHAR (31),
                    lastNmae VARCHAR (31),
                    address1 VARCHAR (31),
                    address2 VARCHAR (31),
                    province VARCHAR (31),
                    country VARCHAR (31),
                    zipcode VARCHAR (15),
                    PRIMARY KEY (id)
                    );""")
    cur.close()
    con.close()


if __name__ == '__main__':
    createTable()