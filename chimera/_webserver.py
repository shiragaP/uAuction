#!/usr/bin/python

# Copyright Jon Berg , turtlemeat.com
# Modified by nikomu @ code.google.com     

import pickle
import json
import cgi
from threading import Timer
import time
from datetime import datetime
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
import os  # os. path
from urllib.parse import urlparse, parse_qs

import DBInfo
from chimera.EmailSender import sendEmail
from chimera.Users import Users
from chimera.Auctions import Auctions
from chimera._postgreSQLManager import DBManager

CWD = os.path.abspath('.')
UPLOAD_PAGE = 'upload.html'  # must contain a valid link with address and port of the servers
# -----------------------------------------------------------------------


class AuctionSite(BaseHTTPRequestHandler):
    def make_index(self, relpath):
        abspath = os.path.abspath(relpath)  # ; print abspath
        flist = os.listdir(abspath)  # ; print flist

        rellist = []
        for fname in flist:
            relname = os.path.join(relpath, fname)
            rellist.append(relname)

        # print rellist
        inslist = []
        for r in rellist:
            inslist.append('<a href="%s">%s</a><br>' % (r, r))

        # print inslist

        page_tpl = "<html><head></head><body>%s</body></html>"

        ret = page_tpl % ( '\n'.join(inslist), )

        return ret

    def do_GET(self):
        try:
            self.path = self.path.replace('%20', ' ')
            if self.path == '/':
                page = self.make_index('.')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(page.encode('ascii'))
                return

            elif self.path.endswith(".png") or self.path.endswith(".jpg"):
                f = open(self.path, "rb")
                print(f.name)
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            elif self.path.endswith(".html"):
                ## print curdir + sep + self.path
                f = open(curdir + sep + self.path)
                # note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read().encode('ascii'))
                f.close()
                return

            elif self.path.endswith(".esp"):  # our dynamic content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("hey, today is the" + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                return

            else:  # default: just send the file

                # filepath = self.path[1:]  # remove leading '/'
                f = open(self.path, 'rb')
                # f = open(os.path.join(CWD, filepath), 'rb')
                # note that this potentially makes every file on your computer readable by the internet

                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            return  # be sure not to fall into "except:" clause ?

        except IOError as e:
            print("IOError: ", e)
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        dbmanager = DBManager()
        # global rootnode ## something remained in the orig. code     
        try:
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/octet-stream':

                fs = cgi.FieldStorage(fp=self.rfile,
                                      headers=self.headers,
                                      environ={'REQUEST_METHOD': 'POST'}
                                      )

                fs_up = fs['upfile']
                # print(fs_up)
                filename = os.path.split(fs_up.filename)[1]
                fullname = os.path.join(CWD, filename)

                if os.path.exists(fullname):
                    fullname_test = fullname + '.copy'
                    i = 0
                    while os.path.exists(fullname_test):
                        fullname_test = "%s.copy(%d)" % (fullname, i)
                        i += 1
                    fullname = fullname_test

                if not os.path.exists(fullname):
                    with open(fullname, 'wb') as o:
                        # self.copyfile(fs['upfile'].file, o)
                        o.write(fs_up.file.read())

                self.send_response(200)
                self.end_headers()

                self.wfile.write("<HTML><HEAD></HEAD><BODY>POST OK.<BR><BR>".encode('ascii'))
                self.wfile.write(("File uploaded under name: " + os.path.split(fullname)[1]).encode('ascii'))
                self.wfile.write(('<BR><A HREF=%s>back</A>' % (UPLOAD_PAGE, )).encode('ascii'))
                self.wfile.write("</BODY></HTML>".encode('ascii'))

            elif ctype == 'multipart/form-data':
                # original version :
                '''
                query=cgi.parse_multipart(self.rfile, pdict)
                upfilecontent = query.get('upfile')
                print "filecontent", upfilecontent[0]
                '''

                fs = cgi.FieldStorage(fp=self.rfile,
                                      headers=self.headers,
                                      environ={'REQUEST_METHOD': 'POST'}
                                      # all the rest will come from the 'headers' object,
                                      # but as the FieldStorage object was designed for CGI, absense of 'POST' value in environ
                                      # will prevent the object from using the 'fp' argument !
                                      )
                # print 'have fs'

                fs_up = fs['upfile']
                # print(fs_up)
                filename = os.path.split(fs_up.filename)[1]  # strip the path, if it presents
                fullname = os.path.join(CWD, filename)

                # check for copies :
                if os.path.exists(fullname):
                    fullname_test = fullname + '.copy'
                    i = 0
                    while os.path.exists(fullname_test):
                        fullname_test = "%s.copy(%d)" % (fullname, i)
                        i += 1
                    fullname = fullname_test

                if not os.path.exists(fullname):
                    with open(fullname, 'wb') as o:
                        # self.copyfile(fs['upfile'].file, o)
                        o.write(fs_up.file.read())

                self.send_response(200)
                self.end_headers()

                self.wfile.write("<HTML><HEAD></HEAD><BODY>POST OK.<BR><BR>".encode('ascii'))
                self.wfile.write(("File uploaded under name: " + os.path.split(fullname)[1]).encode('ascii'))
                self.wfile.write(('<BR><A HREF=%s>back</A>' % (UPLOAD_PAGE, )).encode('ascii'))
                self.wfile.write("</BODY></HTML>".encode('ascii'))

            elif ctype == 'application/x-www-form-urlencoded':
                if self.path == '/query':
                    fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                    statement = fs['statement'].value
                    try:
                        arguments = fs['arguments'].value
                        arguments = json.loads(arguments)
                    except KeyError as e:
                        print("KeyError", e)
                        arguments = tuple()

                    self.send_response(200)
                    self.end_headers()
                    fetch = dbmanager.query(statement, arguments)
                    self.wfile.write(pickle.dumps(fetch))

                elif self.path == '/insert_category_tags':
                    fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                    auction_id = fs['auction_id'].value
                    categories = fs['categories'].value
                    categories = json.loads(categories)
                    for category in categories:
                        statement = """INSERT INTO category_tags (category, auctionid)
                                        VALUES (%s, %s);
                                        """

                        dbmanager.query(statement, (category, auction_id,))

                    self.send_response(200)
                    self.end_headers()

                elif self.path == '/send_auction_end_notification':
                    fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                    auctionid = fs['auctionid'].value

                    self.send_response(200)
                    self.end_headers()

                    Timer(0.1, lambda: AuctionSiteHelper().sendAuctionEndNotification(auctionid)).start()

                else:
                    raise Exception("Unexpected request path")
            else:
                raise Exception("Unexpected POST request")

        except Exception as e:
            print("Exception: ", e)
            self.send_error(404, 'POST to "%s" failed: %s' % (self.path, str(e)))

    def do_PUT(self):
        dbmanager = DBManager()
        try:
            length = int(self.headers['Content-Length'])
            # content = self.rfile.read(length)
            self.send_response(200)
            self.path = self.path.replace('%20', ' ')
            auction_id = int(parse_qs(urlparse(self.path).query)["auction_id"][0])
            fs_up = self.rfile
            filename = os.path.split(urlparse(self.path).path)[1]  # strip the path, if it presents
            fullname = os.path.join(CWD+'\\images', filename)

            if os.path.exists(fullname):
                fullname, fileExtension = os.path.splitext(fullname)
                fullname_test = fullname + '.copy' + fileExtension
                i = 0
                while os.path.exists(fullname_test):
                    fullname_test = "%s.copy(%d)%s" % (fullname, i, fileExtension)
                    i += 1
                fullname = fullname_test

            if not os.path.exists(fullname):
                with open(fullname, 'wb') as o:
                    o.write(fs_up.read(length))

            statement = """INSERT INTO auction_images (directory, auctionid)
                                VALUES (%s, %s);
                                """
            if fullname[1:].startswith(":\\"):
                fullname = fullname[3:].replace("\\", '/')
            dbmanager.query(statement, ("http://" + DBInfo.server + ":8080/" + fullname, auction_id,))

            self.send_response(200)
            self.end_headers()
        except Exception as e:
            print("Exception: ", e)
            self.send_error(404, 'PUT to "%s" failed: %s' % (self.path, str(e)))

class AuctionSiteHelper():
    def __init__(self):
        self.manager = DBManager()

    def run(self):
        statement = """SELECT * FROM auctions
                                WHERE expirytime=(SELECT min(expirytime) FROM auctions WHERE soldout=0 AND expirytime<%s)
        """
        arguments = (datetime.now(), )
        rows = self.manager.query(statement, arguments)
        for row in rows:
            print(row)
            statement = """UPDATE auctions
                                SET soldout=2
                                WHERE id=%s;
            """
            arguments = (row[0], )
            self.manager.query(statement, arguments)
            self.sendAuctionEndNotification(row[0])
        Timer(0.1, self.run).start()

    def sendAuctionEndNotification(self, auction_id):
        auction = Auctions().getAuction(auction_id)
        seller = Users().getUser(auction.seller_id)
        statement = """SELECT DISTINCT userid FROM bid_history
                                WHERE auctionid=%s
        """
        arguments = (auction_id, )
        rows = self.manager.query(statement, arguments)
        users = Users().getUsers(rows)
        userEmails = list()
        for user in users:
            userEmails.append(user.email)
        soldoutPrice = auction.bidprice
        if auction.buyer != 0:
            soldoutPrice = auction.buyoutprice
        text = \
"""Auction ID: %s

Sold out at %s Baht
""" % (auction.auction_id, soldoutPrice)
        if len(userEmails) > 0:
            sendEmail(userEmails, "Auction End Notification", text)

def main():
    try:
        # server = HTTPServer(('uauction.mooo.com', 8080), AuctionSite)

        import getpass
        if getpass.getuser() == 'Fujiwara':
            server = HTTPServer(('localhost', 8080), AuctionSite)

        Timer(0, AuctionSiteHelper().run).start()
        print('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


if __name__ == '__main__':
    main()

