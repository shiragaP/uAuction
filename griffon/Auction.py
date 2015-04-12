__author__ = 'Shiraga-P'

import pickle
import http.client
import urllib.parse
import tempfile


class Auction():
    def __init__(self, auction_id):
        self.auction_id = auction_id

        # TODO: make connection not localhost
        conn = http.client.HTTPConnection("localhost", 8080)

        # params = urllib.parse.urlencode({'auction_id':auction_id})
        # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        # conn.request("POST", "/auction", params, headers)
        params = urllib.parse.urlencode({'statement': "SELECT * from auctions WHERE auctions.id=%s" % (auction_id,)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        row = pickle.loads(data)[0]
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

        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
        data = response.read()

        #TODO: change imagelist to imagepaths
        imageurls = pickle.loads(data)
        self.imagepaths = list()
        for imageurl in imageurls:
            conn.request("GET", imageurl[1])
            response = conn.getresponse()
            temp = tempfile.TemporaryFile()
            temp.write(response.read())
            self.imagepaths.append(temp)
            print(tempfile.gettempdir(), temp.name)

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
        print("Soldout: " + str(self.soldout))
        print("imagepaths: " + str(self.imagepaths))


if __name__ == '__main__':
    auction = Auction(1)
    auction.printInfo()