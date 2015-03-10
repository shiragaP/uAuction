__author__ = 'Fujiwara'

import sys
import psycopg2

def main():
    try:
        conn = psycopg2.connect("dbname='database SE Y2' user='postgres' host='localhost' password='admin' port='5432'")
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
    con = psycopg2.connect("host='localhost' user='postgres' password='admin'")
    dbname = 'sep_project_database'
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute("CREATE DATABASE " + dbname)
    cur.close()
    con.close()


def deleteTable():
    con = psycopg2.connect("host='localhost' dbname='sep_project_database' user='postgres' host='localhost' password='admin'")
    cur = con.cursor()
    cur.execute("DROP TABLE users CASCADE;")
    cur.close()
    con.close()


def createTable():
    con = psycopg2.connect("host='localhost' dbname='sep_project_database' user='postgres' host='localhost' password='admin'")
    dbname = 'sep_project_database'
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
                    postNumber VARCHAR (15),
                    PRIMARY KEY (id)
                    );""")
    cur.close()
    con.close()


if __name__ == '__main__':
    createTable()