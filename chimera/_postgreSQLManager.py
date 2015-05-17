import psycopg2

import DBInfo

class DBManager:
    def __init__(self):
        try:
            self.connectDB()
        except:
            print("Cannot connect to database.")
            print("Connect to server instead.")
            self.connectServer()

    def connectServer(self):
        self.conn = psycopg2.connect(user=DBInfo.user, password=DBInfo.password, host=DBInfo.host)
        self.cur = self.conn.cursor()

    def connectDB(self):
        self.close()
        self.conn = psycopg2.connect(database=DBInfo.dbname, user=DBInfo.user, password=DBInfo.password, host=DBInfo.host)
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    def query(self, statement, arguments=tuple()):
        self.cur.execute(statement, arguments)
        self.conn.commit()
        try:
            return self.cur.fetchall()
        except:
            pass

    def close(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            pass

    def rebuildAll(self):
        prompt = input("Enter 'y' or 'Y' to continue rebuild all components ")
        if prompt == 'y' or prompt == 'Y':
            self.createDB()
            self.connectDB()
            self.createTable()

    def createDB(self):
        self.dropDB()
        self.query("CREATE DATABASE " + DBInfo.dbname)

    def dropDB(self):
        self.close()
        self.connectServer()
        self.conn.set_isolation_level(0)
        self.query("DROP DATABASE IF EXISTS " + DBInfo.dbname)

    def createTable(self):
        self.createTableUsers()
        self.createTableAuctions()
        self.createTableAuctionImages()
        self.createTableCategoryTags()
        self.createTableBidHistory()
        
    def createTableUsers(self):
        self.dropTableUsers()
        statement = """CREATE TABLE users(
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
        self.query(statement)
        statement = """INSERT INTO users (username, password, email, firstname, lastname, address1, address2, province, country, zipcode, phonenumber)
                    VALUES ('admin', 'admin', 'uAucionProject@gmail.com', 'Admin', 'Admin', 'None', null, 'Bangkok', 'Thailand', '10110', '0812345678')"""
        self.query(statement)

    def createTableAuctions(self):
        self.dropTableAuctions()
        statement = """CREATE TABLE auctions(
                        id serial PRIMARY KEY,
                        name VARCHAR (1023),
                        seller serial,
                        buyoutavailable BOOLEAN,
                        buyoutprice INTEGER,
                        bidprice INTEGER,
                        bidnumber INTEGER,
                        description VARCHAR (8191),
                        thumbnail VARCHAR (1023),
                        expirytime TIMESTAMP,
                        soldout INTEGER,
                        buyer serial
                        );
                        """
        self.query(statement)

    def createTableAuctionImages(self):
        self.dropTableAuctionImages()
        statement = """CREATE TABLE auction_images(
                        id serial PRIMARY KEY,
                        directory VARCHAR (1023),
                        auctionid serial
                        );
                        """
        self.query(statement)

    def createTableCategoryTags(self):
        self.dropTableCategoryTags()
        statement = """CREATE TABLE category_tags(
                        id serial PRIMARY KEY,
                        category VARCHAR (127),
                        auctionid serial
                        );
                        """
        self.query(statement)

    def createTableBidHistory(self):
        self.dropTableBidHistory()
        statement = """CREATE TABLE bid_history(
                        id serial PRIMARY KEY,
                        bidprice INTEGER,
                        userid serial,
                        auctionid serial
                        );
                        """
        self.query(statement)

    def createTableBuyoutHistory(self):
        self.dropTableBuyoutHistory()
        statement = """CREATE TABLE buyout_history(
                        id serial PRIMARY KEY,
                        userid serial,
                        auctionid serial
                        );
                        """
        self.query(statement)

    def dropTableUsers(self):
        self.conn.set_isolation_level(0)
        self.query("DROP TABLE IF EXISTS " + "users")

    def dropTableAuctions(self):
        self.conn.set_isolation_level(0)
        self.query("DROP TABLE IF EXISTS " + "auctions")

    def dropTableAuctionImages(self):
        self.conn.set_isolation_level(0)
        self.query("DROP TABLE IF EXISTS " + "auctions_images")

    def dropTableCategoryTags(self):
        self.conn.set_isolation_level(0)
        self.query("DROP TABLE IF EXISTS " + "category_tags")

    def dropTableBidHistory(self):
        self.conn.set_isolation_level(0)
        self.query("DROP TABLE IF EXISTS " + "bid_history")

    def dropTableBuyoutHistory(self):
        self.conn.set_isolation_level(0)
        self.query("DROP TABLE IF EXISTS " + "buyout_history")

# def printUsers():
#     conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
#                             (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
#     cur = conn.cursor()
#     cur.execute("SELECT * from users")
#     rows = cur.fetchall()
#     print('\nShow me the databases:\n')
#     for row in rows:
#         print(row)
#     conn.commit()
#     cur.close()
#     conn.close()
#
#
# def printAuctions():
#     conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
#                             (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
#     cur = conn.cursor()
#     cur.execute("SELECT * from auctions")
#     rows = cur.fetchall()
#     print('\nShow me the databases:\n')
#     for row in rows:
#         print(row)
#     conn.commit()
#     cur.close()
#     conn.close()
#
#
# def printItemsImage():
#     conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
#                             (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
#     cur = conn.cursor()
#     cur.execute("SELECT * from item_images")
#     rows = cur.fetchall()
#     print('\nShow me the databases:\n')
#     for row in rows:
#         print(row)
#     conn.commit()
#     cur.close()
#     conn.close()


if __name__ == '__main__':
    manager = DBManager()
    manager.rebuildAll()

