
__author__ = 'Waterstrider'

import os
import pickle
import http.client
import urllib.parse
import json

from chimera.Auction import Auction
from DBInfo import server

CWD = os.path.abspath('.')

class Auctions:
    def __init__(self):
        self.connection = http.client.HTTPConnection(server, 8080)

    def addAuction(self, auction):
        print("Sent...")
        params = urllib.parse.urlencode({'statement': """INSERT INTO auctions (name, seller, buyoutavailable,
            buyoutprice, bidprice, bidnumber, description, thumbnail, expirytime, soldout, buyer)VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", 'arguments': json.dumps([auction.name,
                                                                                   auction.seller_id,
                                                                                   auction.buyoutavailable,
                                                                                   auction.buyoutprice,
                                                                                   auction.bidprice,
                                                                                   auction.bidnumber,
                                                                                   auction.description,
                                                                                   auction.thumbnailpath,
                                                                                   auction.expirytime,
                                                                                   auction.soldout,
                                                                                   auction.buyer, ])})
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
            self.connection.request("PUT", image.name.replace(" ", "%20") + "?auction_id=" + str(auction_id), image)
            response = self.connection.getresponse()
            print(response.status, response.reason)

        params = urllib.parse.urlencode({'auction_id': auction_id, "categories": json.dumps(auction.categories)})
        self.connection.request("POST", "/insert_category_tags", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

        self.updateAuctionThumbnailPath(auction_id)

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
        buyer = row[11]

        params = urllib.parse.urlencode(
            {'statement': "SELECT * from auction_images WHERE auction_images.auctionid=%s",
             'arguments': json.dumps((auction_id,))})
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()
        imageurls = pickle.loads(data)
        imagepaths = list()
        for imageurl in imageurls:
            imagepaths.append(imageurl[1])

        return Auction(name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnailpath,
                       expirytime, soldout, imagepaths, buyer=buyer, auction_id=auction_id)

    def updateAuctionThumbnailPath(self, auctionid):
        params = urllib.parse.urlencode(
            {'statement': "SELECT directory from auction_images WHERE auctionid=%s ORDER BY id ASC", 'arguments': json.dumps((auctionid,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()

        rows = pickle.loads(data)

        if len(rows) > 0:
            path = rows[0][0]
        else:
            path = "http://" + server + ":8080/" + CWD[3:].replace("\\", '/') + "/images/noimage.png"
        params = urllib.parse.urlencode(
            {'statement': "UPDATE auctions SET thumbnail=%s WHERE id=%s", "arguments": json.dumps((path, auctionid,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def updateBidPrice(self, auction_id, userid, newBidPrice, bidNumber):
        params = urllib.parse.urlencode(
            {'statement': "UPDATE auctions SET bidprice=%s , bidnumber=%s , buyer=%s WHERE id=%s", "arguments": json.dumps((newBidPrice, bidNumber, userid, auction_id))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

        params = urllib.parse.urlencode(
            {'statement': """INSERT INTO bid_history (bidprice, userid, auctionid)
                                        VALUES (%s, %s, %s);""", "arguments": json.dumps((newBidPrice, userid, auction_id,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def updateBuyout(self, auction_id, userid, buyout):
        params = urllib.parse.urlencode(
            {'statement': "UPDATE auctions SET soldout=%s , buyer=%s WHERE id=%s", "arguments": json.dumps((buyout, userid, auction_id,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

        params = urllib.parse.urlencode(
            {'statement': """INSERT INTO buyout_history (userid, auctionid)
                                        VALUES (%s, %s);""", "arguments": json.dumps((userid, auction_id,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

        params = urllib.parse.urlencode(
            {'auctionid': auction_id})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/send_auction_end_notification", params, headers)
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

    def getActiveAuctionIDs(self):
        params = urllib.parse.urlencode(
            {'statement': "SELECT id from auctions WHERE soldout=0 ORDER BY id DESC"})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()

        rows = pickle.loads(data)

        return rows

    def getPopularCategories(self):
        params = urllib.parse.urlencode(
            {'statement': "SELECT category from category_tags GROUP BY category ORDER BY COUNT(category) DESC LIMIT 10"})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()

        rows = pickle.loads(data)

        return rows

    def searchAuctionIDs(self, keywords):
        if len(keywords) < 1:
            return list()
        statement = """SELECT id FROM auctions
                        WHERE id in(SELECT id FROM auctions
                            WHERE LOWER(name) LIKE LOWER(%s)"""
        arguments = ('%'+keywords[0]+'%',)
        for i in range(1, len(keywords)):
            statement += "OR LOWER(name) LIKE LOWER(%s)"
            arguments += ('%'+keywords[i]+'%',)
        statement += ")"

        params = urllib.parse.urlencode(
            {'statement': statement, 'arguments': json.dumps(arguments)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()

        rows = pickle.loads(data)

        return rows

    def getBidHistory(self, userid):
        statement = """SELECT DISTINCT auctionid FROM bid_history
                        WHERE userid=%s"""
        arguments = (userid,)

        params = urllib.parse.urlencode(
            {'statement': statement, 'arguments': json.dumps(arguments)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()

        rows = pickle.loads(data)

        return rows

def testData():
    from datetime import datetime, timedelta
    import glob
    import re

    rootpath = '..\\uAuction Test Data'
    auctionTestDataPaths = glob.glob(rootpath + "\\*.txt")
    auctions = Auctions()

    for auctionPath in auctionTestDataPaths:
        file = open(auctionPath, encoding='utf8')
        name = file.readline().replace("\n", "")
        buyoutprice = eval(file.readline())
        buyoutavailable = True if buyoutprice > 0 else False
        bidprice = eval(file.readline())
        categories = list(filter(''.__ne__, re.split(" |,|#|\n", file.readline())))
        description = ""
        imagepaths = list()

        rest = file.readlines()
        while len(rest) > 0 and rest[0][:3] == "[I]":
            imagepaths.append(rest[0][3:].replace("\n", ""))
            rest.remove(rest[0])
        while len(rest) > 0:
            description += rest[0]
            rest.remove(rest[0])

        thumbnailpath = imagepaths[0] if len(imagepaths) > 0 else "..\\resources\\img\\noimage.png"
        expirytime = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now() + timedelta(days=3))
        soldout = 0
        imagepaths = [open(rootpath + "\\" + imagepaths[i], 'rb') for i in
                      range(len(imagepaths))]

        Auctions().addAuction(
            Auction(name, 1, buyoutavailable, buyoutprice, bidprice, 0, description, thumbnailpath,
                    expirytime, soldout, imagepaths, categories))

if __name__ == '__main__':
    testData()