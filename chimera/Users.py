__author__ = 'Waterstrider'

import pickle
import json
import http.client
import urllib.parse

from chimera.User import User
from DBInfo import server


class Users:
    def __init__(self):
        self.connection = http.client.HTTPConnection(server, 8080)

    def addUser(self, username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                phonenumber):
        params = urllib.parse.urlencode({'statement': """INSERT INTO users (username, password, email, firstname, lastname, address1, address2, province, country, zipcode, phonenumber)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", 'arguments': json.dumps((
            username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
            phonenumber))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def getUser(self, user_id):
        params = urllib.parse.urlencode({'statement': "SELECT * from users WHERE users.id=%s", 'arguments': json.dumps((user_id,))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
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

        return User(username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                    phonenumber, user_id)

    def getUsers(self, user_id_list):
        user_list = list()

        for i in user_id_list:
            params = urllib.parse.urlencode({'statement': "SELECT * from users WHERE users.id=%s", 'arguments': json.dumps((i[0],))})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            self.connection.request("POST", "/query", params, headers)
            response = self.connection.getresponse()
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

            user = User(username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                    phonenumber, i[0])
            user_list.append(user)

        return user_list

    def updateUser(self, username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                phonenumber):
        statement = """UPDATE users
                        SET password=%s, email=%s, firstname=%s, lastname=%s, address1=%s, address2=%s, province=%s, country=%s, zipcode=%s, phonenumber=%s
                        WHERE username=%s;
        """
        params = urllib.parse.urlencode({'statement': statement, 'arguments': json.dumps((
            password, email, firstname, lastname, address1, address2, province, country, zipcode,
            phonenumber, username))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        print(response.status, response.reason)

    def validUser(self, username, password):
        params = urllib.parse.urlencode({'statement': "SELECT * from users WHERE users.username=%s", 'arguments': json.dumps((username, ))})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        self.connection.request("POST", "/query", params, headers)
        response = self.connection.getresponse()
        data = response.read()
        rows = pickle.loads(data)
        if len(rows) < 1:
            return -1
        elif password == rows[0][2]:
            return rows[0][0]
        return 0






if __name__ == '__main__':
    user = Users().getUser(1)
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