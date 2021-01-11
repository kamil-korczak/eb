import pytest
from ebapp.tests.helper.auction_helper import AuctionTestFile
from ebapp.tests.helper.auction_helper import AuctionExpected
from ebapp.classes.auctionsebayparser import AuctionsEbayParser


test_data = [
        (AuctionTestFile(external_id=164169141533), AuctionExpected(external_id=164169141533, title_auction='Herren Jogginghose Sporthose Männer Trainingshose Sweatpants 601', price_normal='12,90', price_uvp='29,90', auction_account='redox-fashion', img_auction='https://i.ebayimg.com/images/g/mk8AAOSwEVhftU~1/s-l500.jpg'), ),
        (AuctionTestFile(external_id=164090262546), AuctionExpected(external_id=164090262546,title_auction='A. Salvarini Designer Herren Jeans Hose Basic Jeanshose Comfort Fit gerades Bein', price_normal='29,90', price_uvp='79,90', auction_account='golden-brands', img_auction='https://i.ebayimg.com/images/g/bm8AAOSwzFFe4J-C/s-l500.jpg'), ),
        (AuctionTestFile(external_id=152953724302), AuctionExpected(external_id=152953724302,title_auction='A. Salvarini Herren Sweatjacke Kapuzenpullover Jacke Kapuze Hoodie Sweater AS072', price_normal='24,90', price_uvp='49,90', auction_account='golden-brands', img_auction='https://i.ebayimg.com/images/g/tPAAAOSwO-Jf4FGI/s-l500.jpg'), ),
    ]

@pytest.mark.parametrize("test, expected", test_data)    
class TestAuctionParser:
    
    def processAuctionData(self, test):
        auctionsebayparser = AuctionsEbayParser()
        auctionsebayparser.setSoup(test.getAuctionTestData())
        soup = auctionsebayparser.getSoup()
        result = (auctionsebayparser, soup) # result = test, expected
        
        return result

    def test_parser_if_enough_elements(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert len(test.parseDataFromEbayAuction(soup)) == 6

    def test_parser_if_dict(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert type(test.parseDataFromEbayAuction(soup)) == dict

    # test invidual elements    
    def test_external_id(self, test, expected):
        test, soup = self.processAuctionData(test)
        test_external_id = test.parseExternalId(soup)
        print(test_external_id) 
        assert test_external_id == expected.get_external_id()

    def test_title_auction(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert test.parseTitleAuction(soup) == expected.get_title_auction()

    def test_price_normal(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert test.parsePriceNormal(soup) == expected.get_price_normal()

    def test_price_uvp(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert test.parsePriceUvp(soup) == expected.get_price_uvp()

    def test_auction_account(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert test.parseAuctionAccount(soup) == expected.get_auction_account()

    def test_img_auction(self, test, expected):
        test, soup = self.processAuctionData(test)
        assert test.parseImgAuction(soup) == expected.get_img_auction()

