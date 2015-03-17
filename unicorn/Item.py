__author__ = 'Shiraga-P'

import psycopg2

import DatabaseInfo


class Item():
    def __init__(self, item_id):
        self.item_id = item_id

        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
        cur = conn.cursor()

        print(self.item_id)
        cur.execute("SELECT * from items WHERE items.id=%s", (self.item_id,))
        row = cur.fetchall()[0]
        self.itemname = row[1]
        self.seller_id = row[2]
        self.buyoutavailable = row[3]
        self.buyoutprice = row[4]
        self.bidprice = row[5]
        self.bidnumber = row[6]
        self.description = row[7]
        self.thumbnail = row[8]
        conn.commit()

        #TODO: load all item's images
        self.images = list()

        cur.close()
        conn.close()