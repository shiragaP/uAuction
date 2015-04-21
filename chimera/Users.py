__author__ = 'Waterstrider'

import pickle
import http.client
import urllib.parse

from chimera.User import User
import DatabaseInfo


class Users:
    def addUser(username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                phonenumber):
        conn = http.client.HTTPConnection(DatabaseInfo.host, 8080)
        params = urllib.parse.urlencode({'statement': """INSERT INTO users (username, password, email, firstname, lastname, address1, address2, province, country, zipcode, phonenumber)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""" % (
            username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
            phonenumber)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)

        conn.close()

    def getUser(user_id):
        conn = http.client.HTTPConnection(DatabaseInfo.host, 8080)
        params = urllib.parse.urlencode({'statement': "SELECT * from users WHERE users.id=%s" % (user_id,)})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn.request("POST", "/query", params, headers)
        response = conn.getresponse()
        data = response.read()

        row = pickle.loads(data)[0]
        username = row[1]
        password = row[2]
        email = row[3]
        firstname = row[4]
        lastname = row[5]
        address1 = row[6]
        address2 = row[7]
        province = row[8]
        country = row[9]
        zipcode = row[10]
        phonenumber = row[11]

        conn.close()

        return User(username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                    phonenumber, user_id)


if __name__ == '__main__':
    user = Users.getUser(1)
    print("username", user.username)
    print("password", user.password)
    print("firstname", user.firstname)
    print("lastname", user.lastname)
    print("address1", user.address1)
    print("address2", user.address2)
    print("province", user.province)
    print("country", user.country)
    print("zipcode", user.zipcode)
    print("phonenumber", user.phonenumber)