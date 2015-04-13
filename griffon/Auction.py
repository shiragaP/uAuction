__author__ = 'Shiraga-P'

class Auction():
    def __init__(self, name, seller_id, buyoutavailable, buyoutprice, bidprice, bidnumber, description, thumbnailpath,
                   expirytime, soldout, imagepaths, auction_id = None):

        self.name = name
        self.seller_id = seller_id
        self.buyoutavailable = buyoutavailable
        self.buyoutprice = buyoutprice
        self.bidprice = bidprice
        self.bidnumber = bidnumber
        self.description = description
        self.thumbnailpath = thumbnailpath
        self.expirytime = expirytime
        self.soldout = soldout
        self.imagepaths = imagepaths

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
    from griffon.Auctions import Auctions
    auction = Auctions.getAuction(1)
    auction.printInfo()