__author__ = 'Shiraga-P'

import psycopg2
import DatabaseInfo

def main():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    cur = conn.cursor()
    cur.execute("SELECT * from users")
    rows = cur.fetchall()
    print('\nShow me the databases:\n')
    for row in rows:
        print('   ,', row)


def createDatabase():
    conn = psycopg2.connect("host='%s' user='%s' password='%s'" %
                           (DatabaseInfo.host, DatabaseInfo.user, DatabaseInfo.password))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE " + DatabaseInfo.dbname)
    cur.close()
    conn.close()


def deleteTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                           (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    cur = conn.cursor()
    cur.execute("DROP TABLE users CASCADE")
    conn.commit()
    cur.close()
    conn.close()


def createTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                           (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    statement = ""
    statement += """CREATE TABLE users(
                    id serial PRIMARY KEY,
                    username VARCHAR (15),
                    password VARCHAR (15),
                    email VARCHAR(63),
                    firstname VARCHAR (31),
                    lastname VARCHAR (31),
                    address1 VARCHAR (31),
                    address2 VARCHAR (31),
                    province VARCHAR (31),
                    country VARCHAR (31),
                    zipcode VARCHAR (15)
                    );
                    """
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()

def rebuildTable():
    deleteTable()
    createTable()

if __name__ == '__main__':
    rebuildTable()
