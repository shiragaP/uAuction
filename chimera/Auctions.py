__author__ = 'Waterstrider'

import pickle
import http.client
import urllib.parse
import tempfile
import json

from chimera.Auction import Auction
from DBInfo import server


class Auctions:
    def __init__(self):
        self.connection = http.client.HTTPConnection(server, 8080)

    def addAuction(self, auction):
        print("Sent...")
        params = urllib.parse.urlencode({'statement': """INSERT INTO auctions (name, seller, buyoutavailable,
            buyoutprice, bidprice, bidnumber, description, thumbnail, expirytime, soldout)VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", 'arguments': json.dumps([auction.name,
                                                                                   auction.seller_id,
                                                                                   auction.buyoutavailable,
                                                                                   auction.buyoutprice,
                                                                                   auction.bidprice,
                                                                                   auction.bidnumber,
                                                                                   auction.description,
                                                                                   auction.thumbnailpath,
                                                                                   auction.expirytime,
                                                                                   auction.soldout, ])})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

        params = urllib.parse.urlencode({'statement': "SELECT max(id) from auctions"})
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()
        auction_id = pickle.loads(data)[0][0]
        print(auction.imagepaths)

        for image in auction.imagepaths:
            self.connection.request("PUT", image.name + "?auction_id=" + str(auction_id), image)
            response = self.connection.getresponse()
            print(response.status, response.reason)

        params = urllib.parse.urlencode({'auction_id': auction_id, "categories": json.dumps(auction.categories)})
        self.connection.request("POST", "/insert_category_tags", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def getAuction(self, auction_id):
        params = urllib.parse.urlencode(
            {'statement': "SELECT * from auctions WHERE auctions.id=%s", 'arguments': json.dumps((auction_id,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()

        row = pickle.loads(data)[0]
        name = row[1]
        seller_id = row[2]
        buyoutavailable = row[3]
        buyoutprice = row[4]
        bidprice = row[5]
        bidnumber = row[6]
        description = row[7]
        thumbnailpath = row[8]
        expirytime = row[9]
        soldout = row[10]

        params = urllib.parse.urlencode(
            {'statement': "SELECT * from auction_images WHERE auction_images.auctionid=%s",
             'arguments': json.dumps((auction_id,))})
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()
        imageurls = pickle.loads(data)
        imagepaths = list()
        print(imageurls)

        for imageurl in imageurls:
            self.connection.request("GET", imageurl[1])
            response = self.connection.getresponse()
            temp = tempfile.TemporaryFile()
            temp.write(response.read())
            imagepaths.append(temp)

        return Auction(name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnailpath,
                       expirytime, soldout, imagepaths, auction_id)

    def updateBidPrice(self, auction_id, newBidPrice):
        params = urllib.parse.urlencode(
            {'statement': "UPDATE items SET bidprice=%s WHERE id=%s" % (newBidPrice, auction_id,)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def delete(self):
        pass

    def insert(self):
        pass

    def select(self):
        pass

    def update(self):
        pass


if __name__ == '__main__':
    auction = Auctions().getAuction(1)
    print("name", auction.name)