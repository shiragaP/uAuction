#!/usr/bin/python

# Copyright Jon Berg , turtlemeat.com
# Modified by nikomu @ code.google.com     

import pickle
import cgi
import time
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
import os  # os. path

import psycopg2

import DatabaseInfo


CWD = os.path.abspath('.')
## print CWD

# PORT = 8080
UPLOAD_PAGE = 'upload.html'  # must contain a valid link with address and port of the servers
# -----------------------------------------------------------------------

class AuctionSite(BaseHTTPRequestHandler):
    def __init__(self):
        self.DEBUGMODE = False

    def make_index(self,relpath):
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
            print(self.path)
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
        # global rootnode ## something remained in the orig. code     
        try:
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            print(self.path)
            if ctype == 'multipart/form-data':
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
                    conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" % (
                    DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
                    cur = conn.cursor()
                    cur.execute(statement)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(pickle.dumps(cur.fetchall()))
                    conn.commit()
                    cur.close()
                    conn.close()

                elif self.path == '/insert_auction_images':
                    fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                    auction_id = fs['auction_id'].value
                    imagepaths = fs['imagepaths'].value

                    for image in range(imagepaths):
                        filename = os.path.split(image.name)[1]  # strip the path, if it presents
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
                                o.write(image.read())

                        conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" %
                                                (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
                        cur = conn.cursor()

                        statement = """INSERT INTO auction_images (directory, auctionid)
                                        VALUES (%s, %s);
                                        """

                        if (self.DEBUGMODE):
                            print("Sql Statement")
                            print(statement)

                        cur.execute(statement, (fullname, auction_id,))

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(pickle.dumps(cur.fetchall()))
                    conn.commit()
                    cur.close()
                    conn.close()


                # elif self.path == '/auction':
                # fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                #     auction_id = fs['auction_id'].value
                #     conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
                #     cur = conn.cursor()
                #     cur.execute("SELECT * from auctions WHERE auctions.id=%s", (auction_id,))
                #     self.send_response(200)
                #     self.end_headers()
                #     self.wfile.write(pickle.dumps(cur.fetchall()))
                #     conn.commit()
                #     cur.close()
                #     conn.close()
                # elif self.path == '/auction_images':
                #     fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                #     auction_id = fs['auction_id'].value
                #     conn = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'" % (DatabaseInfo.host, DatabaseInfo.dbname, DatabaseInfo.user, DatabaseInfo.password))
                #     cur = conn.cursor()
                #     cur.execute("SELECT * from auction_images WHERE auction_images.id=%s", (auction_id,))
                #     self.send_response(200)
                #     self.end_headers()
                #     self.wfile.write(pickle.dumps(cur.fetchall()))
                #     conn.commit()
                #     cur.close()
                #     conn.close()

                else:
                    raise Exception("Unexpected request path")
            else:
                raise Exception("Unexpected POST request")

        except Exception as e:
            print("Exception: ", e)
            self.send_error(404, 'POST to "%s" failed: %s' % (self.path, str(e)))


def main():
    try:
        import socket

        print(socket.gethostbyname(socket.gethostname()))
        # server = HTTPServer((socket.gethostbyname(socket.gethostname()), 8080), MyHandler)
        server = HTTPServer(('localhost', 8080), AuctionSite)
        print('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()


if __name__ == '__main__':
    main()

