from .models import Auctions, AuctionsDetails
from rest_framework import serializers

class AuctionsSelectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auctions
        fields = [
            'selected',
        ]