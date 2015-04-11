__author__ = 'Shiraga-P'

from datetime import datetime

import psycopg2

import DatabaseInfo


class Auction():
    def __init__(self, auction_id):
        self.auction_id = auction_id

        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        cur.execute("SELECT * from auctions WHERE auctions.id=%s", (self.auction_id,))
        row = cur.fetchall()[0]
        self.name = row[1]
        self.seller_id = row[2]
        self.buyoutavailable = row[3]
        self.buyoutprice = row[4]
        self.bidprice = row[5]
        self.bidnumber = row[6]
        self.description = row[7]
        self.thumbnailpath = row[8]
        self.expirytime = row[9]
        self.soldout = row[10]
        self.imagepathes = list()

        cur.execute("SELECT * from auction_images WHERE auctionid=%s", (self.auction_id,))
        rows = cur.fetchall()
        for row in rows:
            self.imagepathes += (row[1],)

        conn.commit()
        cur.close()
        conn.close()

    def printInfo(self):
        print("Name: " + str(self.name))
        print("Seller ID: " + str(self.seller_id))
        print("Buyout Available: " + str(self.buyoutavailable))
        print("Buyout Price: " + str(self.buyoutprice))
        print("Bid Price: " + str(self.bidprice))
        print("Bid Number " + str(self.bidnumber))
        print("Description: " + str(self.description))
        print("Thumbnail Path: " + str(self.thumbnailpath))
        print("Expirytime: " + str(self.expirytime))

if __name__ == '__main__':
    auction = Auction(1)
    auction.printInfo()