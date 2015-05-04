__author__ = 'Fujiwara'

import smtplib

name = "uAuctionProject"
username = "uAuctionProject@gmail.com"
password = "uAuctionPassword"

def sendEmail(receivers, title, text, sender=username, sendernm=name, senderpw=password):
    text = """\
From: %s <%s>
Subject: %s

%s
    """ % (sendernm, sender, title, text)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, senderpw)
    server.sendmail(sender, receivers, text)


if __name__ == '__main__':
    sendEmail(("upzaacub@gmail.com", ), "Test Sending mail", "This is test's main :) 55 . . \n \n Test New Line \t\t TAB\tTab")