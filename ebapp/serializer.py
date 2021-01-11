from .models import Auctions, AuctionsDetails
from rest_framework import serializers

class AuctionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auctions
        fields = [
            'external_id',
            'private_id',
            'title_auction',
            'auction_format',
            'img_auction',
            'seller_comment',
            'auction_account',
            'time_added',
            'time_downloaded',
        ]

class AuctionsSelectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auctions
        fields = [
            # 'external_id',
            'selected',
        ]


class AuctionsDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AuctionsDetails
        fields = [
            'items_stock',
            'price_normal',
            'price_uvp',
            #'seller_comment', # ??
        ]

# TODO_LATER fix here - serializer of two models
#class AuctionsWithDetailsSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = AuctionsDetails