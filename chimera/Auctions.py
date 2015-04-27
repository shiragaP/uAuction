__author__ = 'Waterstrider'

import pickle
import http.client
import urllib.parse
import tempfile
import mimetypes

from chimera.Auction import Auction
from DBInfo import server


class Auctions:
    def __init__(self):
        self.connection = http.client.HTTPConnection(server, 8080)

    def post_multipart(self, selector, fields, files):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        content_type, body = self.encode_multipart_formdata(fields, files)
        headers = {
            'Content-Type': content_type
        }
        self.connection.request('POST', selector, body, headers)
        res = self.connection.getresponse()
        return res.read()

    def encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def addAuction(self, auction):
        import json
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

        # params = urllib.parse.urlencode({'auction_id': auction_id, "imagepaths": json.dumps(auction.imagepaths)})
        # self.connection.request("POST", "/insert_auction_images", params, headers)
        # response = self.connection.getresponse()
        # print(response.status, response.reason)

        params = urllib.parse.urlencode({'auction_id': auction_id, "categories": json.dumps(auction.categories)})
        self.connection.request("POST", "/insert_category_tags", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def getAuction(self, auction_id):
        params = urllib.parse.urlencode({'statement': "SELECT * from auctions WHERE auctions.id=%s" % (auction_id,)})
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
            {'statement': "SELECT * from auction_images WHERE auction_images.auctionid=%s" % (auction_id,)})
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()
        imageurls = pickle.loads(data)
        imagepaths = list()

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