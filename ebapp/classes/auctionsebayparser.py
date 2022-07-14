from django.contrib import messages

from bs4 import BeautifulSoup
from ebapp.models import Auctions, AuctionsDetails

import requests

class AuctionsEbayParser:
    
    def setDataFromEbayAuction(self, request, external_id):
        self.auction_data = self.__getDataFromEbayAuction(request, external_id)
        self.external_id = external_id
        
        if self.auction_data is not False:
            self.setSoup(self.auction_data)

    def getDataAuctionRaw(self):
        return self.auction_data

    def __getDataFromEbayAuction(self, request, external_id):
        try:
            return requests.get(f'https://www.ebay.de/itm/{external_id}').content
        except ConnectionError as e:
            messages.error(request, 'Failed to establish a new connection.')
            return False

    def setSoup(self, ebay_data):
        self.soup = BeautifulSoup(ebay_data, 'html.parser')
    
    def getSoup(self):
        return self.soup

    def parseDataFromEbayAuction(self, ebay_data):
        if ebay_data is not False:

            soup = self.getSoup()

            auction_data = {}

            """ external_id """
            auction_data['external_id'] = self.parseExternalId(soup)

            """ title_auction """
            auction_data['title_auction'] = self.parseTitleAuction(soup)

            """ price normal """
            auction_data['price_normal'] = self.parsePriceNormal(soup)

            """ price_uvp """
            auction_data['price_uvp'] = self.parsePriceUvp(soup)
            
            """ auction_account """
            auction_data['auction_account'] = self.parseAuctionAccount(soup)
            
            """ img_auction """
            auction_data['img_auction'] = self.parseImgAuction(soup)

            return auction_data

    def parseExternalId(self, soup):
        return soup.select_one('#descItemNumber').text

    def __getExternalId(self):
        return self.external_id

    def parseTitleAuction(self, soup):
        return soup.select_one('#itemTitle').text.replace('Details zu  ', '').strip()

    def parsePriceNormal(self, soup):
        return soup.select_one('#prcIsum').text.replace('EUR ', '')

    def parsePriceUvp(self, soup):
        try:
            price_uvp = soup.select_one('#orgPrc').text.replace('EUR ', '').strip()
        except AttributeError as e:
            price_uvp = None
            pass

        return price_uvp

    def parseAuctionAccount(self, soup):
        return soup.select_one('.mbg-nw').text

    def parseImgAuction(self, soup):
        return soup.select_one('#icImg')['src']

    def saveAuctionData(self, request, auction_data):

        external_id = auction_data['external_id']

        data = {
            'external_id': auction_data['external_id'],
            'title_auction': auction_data['title_auction'],
            'auction_account': auction_data['auction_account'],
            'img_auction': auction_data['img_auction'],
            'status': 0,
        }

        obj_auction, created = Auctions.objects.update_or_create(
            external_id=external_id,
            defaults=data
        )

        data_details = {
            'auction_id': obj_auction.id,
            'price_normal': auction_data['price_normal'].replace(",", "."),
            'price_uvp': auction_data['price_uvp'].replace(",", "."),
        }

        details = AuctionsDetails.objects.create(**data_details)
    
    def saveMultipleAuctionsData(self, request, auctions_list_data):
        for auction_data in auctions_list_data:
            self.saveAuctionData(request, auction_data=auctions_list_data[auction_data])
   

    def getDataFromMultipleAuctions(self, request, auctions_list):

        parsed_data = {}

        for auction in auctions_list:

            auctionsebayparser = AuctionsEbayParser()

            auctionsebayparser.setDataFromEbayAuction(request, external_id=auction)

            ebay_data = auctionsebayparser.getDataAuctionRaw()

            parsed_data[auction] = auctionsebayparser.parseDataFromEbayAuction(ebay_data=ebay_data)

        return parsed_data

    def getDataAndSaveMultiple(self, request, auctions_list):

        auctions_list_data = self.getDataFromMultipleAuctions(request, auctions_list)

        self.saveMultipleAuctionsData(request, auctions_list_data)

        messages.success(request, f'Added/updated {len(auctions_list)} auctions.')

        