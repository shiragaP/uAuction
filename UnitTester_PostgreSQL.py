__author__ = 'Shiraga-P'

import psycopg2

import DBInfo


def printUsers():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    cur = conn.cursor()
    cur.execute("SELECT * from users")
    rows = cur.fetchall()
    print('\nShow me the databases:\n')
    for row in rows:
        print(row)
    conn.commit()
    cur.close()
    conn.close()


def printAuctions():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    cur = conn.cursor()
    cur.execute("SELECT * from auctions")
    rows = cur.fetchall()
    print('\nShow me the databases:\n')
    for row in rows:
        print(row)
    conn.commit()
    cur.close()
    conn.close()


def printItemsImage():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    cur = conn.cursor()
    cur.execute("SELECT * from item_images")
    rows = cur.fetchall()
    print('\nShow me the databases:\n')
    for row in rows:
        print(row)
    conn.commit()
    cur.close()
    conn.close()


def createDatabase():
    conn = psycopg2.connect("host='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.user, DBInfo.password))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE " + DBInfo.dbname)
    conn.commit()
    cur.close()
    conn.close()


def deleteUsersTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    cur = conn.cursor()
    cur.execute("DROP TABLE users CASCADE")
    conn.commit()
    cur.close()
    conn.close()


def createUsersTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
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
                    zipcode VARCHAR (15),
                    phonenumber VARCHAR (15)
                    );
                    """
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()


def deleteItemsTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    cur = conn.cursor()
    cur.execute("DROP TABLE items CASCADE")
    conn.commit()
    cur.close()
    conn.close()


def createItemsTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    statement = ""
    statement += """CREATE TABLE items(
                    id serial PRIMARY KEY,
                    name VARCHAR (63),
                    seller serial,
                    buyoutavailable BOOLEAN,
                    buyoutprice INTEGER,
                    bidprice INTEGER,
                    bidnumber INTEGER,
                    description VARCHAR (8191),
                    thumbnail VARCHAR (127),
                    expirytime TIMESTAMP,
                    soldout BOOLEAN
                    );
                    """
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()


def deleteItemImagesTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    cur = conn.cursor()
    cur.execute("DROP TABLE item_images CASCADE")
    conn.commit()
    cur.close()
    conn.close()


def createItemImagesTable():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    statement = ""
    statement += """CREATE TABLE item_images(
                    id serial PRIMARY KEY,
                    directory VARCHAR (127),
                    itemid serial
                    );
                    """
    cur = conn.cursor()
    cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()


def rebuildUsersTable():
    try:
        deleteUsersTable()
    except:
        pass
    createUsersTable()


def rebuildItemsTable():
    try:
        deleteItemsTable()
    except:
        pass
    createItemsTable()


def rebuildItemImagesTable():
    try:
        deleteItemImagesTable()
    except:
        pass
    createItemImagesTable()


def rebuildAll():
    try:
        createDatabase()
    except:
        pass
    rebuildUsersTable()
    rebuildItemsTable()
    rebuildItemImagesTable()


def sqlExecute():
    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                            (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    statement = input()
    cur = conn.cursor()
    cur.execute(statement)
    rows = cur.fetchall()
    print('\nShow me the databases:\n')
    for row in rows:
        print(row)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    printAuctions()
