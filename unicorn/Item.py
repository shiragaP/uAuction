__author__ = 'Shiraga-P'

import psycopg2

import DBInfo


class Item():
    def __init__(self, item_id):
        self.item_id = item_id

        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DBInfo.host, DBInfo.dbname, DBInfo.user, DBInfo.password))
        cur = conn.cursor()

        cur.execute("SELECT * from auctions WHERE auctions.id=%s", (self.item_id,))
        row = cur.fetchall()[0]
        self.itemname = row[1]
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

        cur.execute("SELECT * from auction_images WHERE id=%s", (self.item_id,))
        rows = cur.fetchall()
        for row in rows:
            self.imagepathes += (row[1],)

        conn.commit()
        cur.close()
        conn.close()

    def printInfo(self):
        print(self.itemname)
        print(self.seller_id)
        print(self.buyoutavailable)
        print(self.buyoutprice)
        print(self.bidprice)
        print(self.bidnumber)
        print(self.description)
        print(self.thumbnail)
        print(self.expirytime)


if __name__ == '__main__':
    item = Item(1)