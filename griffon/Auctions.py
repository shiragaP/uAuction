__author__ = 'Waterstrider'

import pickle
import http.client
import urllib.parse
import tempfile

from griffon.Auction import Auction


class Auctions:
    def addAuction(auction):
        try:
            # TODO: make connection not localhost
            conn = http.client.HTTPConnection("localhost", 8080)
            params = urllib.parse.urlencode({'statement': """INSERT INTO auctions (name, seller, buyoutavailable,
                buyoutprice, bidprice, bidnumber, description, thumbnail, expirytime, soldout)VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""" % (Auction.name,
                                                                Auction.seller_id,
                                                                Auction.buyoutavailable,
                                                                Auction.buyoutprice,
                                                                Auction.bidprice,
                                                                Auction.bidnumber,
                                                                Auction.description,
                                                                Auction.thumbnailpath,
                                                                Auction.expirytime,
                                                                Auction.soldout,)})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            conn.request("POST", "/query", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)

            params = urllib.parse.urlencode({'statement': "SELECT max(id) from auctions"})
            conn.request("POST", "/query", params, headers)
            response = conn.getresponse()
            data = response.read()
            auction_id = pickle.loads(data)[0][0]

            params = urllib.parse.urlencode({'auction_id': auction_id, "imagepaths": auction.imagepaths})
            conn.request("POST", "/insert_auction_images", params, headers)
            response = conn.getresponse()
            print(response.status, response.reason)

            conn.close()
        except Exception as e:
            print(e)

    def getAuction(auction_id):
        # try:
        # TODO: make connection not localhost
        conn = http.client.HTTPConnection("localhost", 8080)
        params = urllib.parse.urlencode({'statement': "SELECT * from auctions WHERE auctions.id=%s" % (auction_id,)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
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
            {'statement': "SELECT * from auction_images WHERE auction_images.auctionid=%s" % (auction_id,)})
        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
        data = response.read()
        imageurls = pickle.loads(data)
        imagepaths = list()

        for imageurl in imageurls:
            conn.request("GET", imageurl[1])
            response = conn.getresponse()
            temp = tempfile.TemporaryFile(suffix=".jpg")
            temp.write(response.read())
            imagepaths.append(temp)

        conn.close()

        return Auction(name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnailpath,
                       expirytime, soldout, imagepaths)
        # except Exception as e:
        # print(e)

    def delete(self):
        pass

    def insert(self):
        pass

    def select(self):
        pass

    def update(self):
        pass