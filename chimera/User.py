__author__ = 'Fujiwara'


class User():
    def __init__(self, username, password, email, firstname, lastname, address1, address2, province, country, zipcode,
                 phonenumber, user_id=None):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address1 = address1
        self.address2 = address2
        self.province = province
        self.country = country
        self.zipcode = zipcode
        self.phonenumber = phonenumber
        self.user_id = user_id