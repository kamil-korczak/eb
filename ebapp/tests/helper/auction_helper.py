from ebapp.classes.auctionsebayparser import AuctionsEbayParser

AUCTION_TEST_DIR_LOCATION = '/home/kamil/Documents/apps/eb-project/eb/ebapp/tests/test_files/auctions/'
AUCTION_TEST_FILE_PREFIX = 'auction_data_'

class AuctionTestFile:
    
    def __init__(self, external_id):
        self.filename_auction_data_raw = f'{AUCTION_TEST_DIR_LOCATION}{AUCTION_TEST_FILE_PREFIX}{external_id}' 
        self.auction_test_data = self.setAuctionTestData(filename=self.filename_auction_data_raw)

    def getAuctionTestData(self):
        return self.auction_test_data

    def setAuctionTestData(self, filename):
        auctionsebayparser = AuctionsEbayParser()

        with open(filename, 'r') as reader:
            auction_test_data = reader.read()

            return auction_test_data

class AuctionExpected:

    def __init__(self, external_id, title_auction, price_normal, price_uvp, auction_account, img_auction):
        self.external_id = external_id
        self.title_auction = title_auction
        self.price_normal = price_normal
        self.price_uvp = price_uvp
        self.auction_account = auction_account
        self.img_auction = img_auction

    def getFileNameAuctionDataRaw(self):
        return self.filename_auction_data_raw
    
    def get_external_id(self):
        return str(self.external_id)

    def get_title_auction(self):
        return self.title_auction

    def get_price_normal(self):
        return self.price_normal

    def get_price_uvp(self):
        return self.price_uvp

    def get_auction_account(self):
        return self.auction_account

    def get_img_auction(self):
        return self.img_auction