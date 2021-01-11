#from django.shortcuts import render

from itertools import chain

from .models import Auctions, AuctionsDetails
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import renderers
from rest_framework.decorators import action, api_view
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status

from .serializer import (
    AuctionsSerializer, AuctionsDetailsSerializer, #, AuctionsWithDetailsSerializer
    AuctionsSelectedSerializer
    )
from ebapp.classes.report import Report

""" @dataclass
class Auction:
    id: str
    price: float

@dataclass
class AuctionDetails:
    id: str
    description: str """

# Create your views here.
class AuctionsAPIViewSet(viewsets.ModelViewSet):
    #plugin do podpowiadania poszukanie intelisense
    lookup_field = 'external_id'
    queryset = Auctions.objects.all() # query na last
    serializer_class = AuctionsSerializer
    permissions_classes = [permissions.IsAuthenticated]
    #auction = Auction('1', 23.3)
    #details = AuctionDetails('1', 'angeboten jumper jaja natulsish')
    #merged = (
    #    ('id', auction.id),
    #    ('price', auction.price),
    #    ('description', details.description)
    #)

    "SELECT * FROM auction LEFT JOIN details on  auction.id=detail.id ORDER BY DESC detail.date LIMIT 1"


""" class ReportsViewSet(APIView):
    queryset = Auctions.objects.all()
    serializer_class = AuctionsSerializer
    permissions_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def recent_reports(self, request):
        
        serializer_class = AuctionsSerializer
        permissions_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def generate_report(self,request): """

class AuctionsSelectedListAPIView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, format=None):
        auctions = Auctions.objects.all()

        auctions = [(auction.id, auction.external_id, auction.selected) for auction in auctions]

        return Response(auctions)

class AuctionsSelectedAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [renderers.JSONRenderer]

    def get_object(self, pk):
        try:
            return Auctions.objects.get(pk=pk)
        except Auctions.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):

    #     auction = self.get_object(pk)

    #     serializer = AuctionsSelectedSerializer(auction)

    #     return Response(serializer.data)

    def post(self, request, pk, format=None):
        auction = self.get_object(pk)

        serializer = AuctionsSelectedSerializer(auction, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuctionsPrivateIdAPIViewSet(generics.ListAPIView):
    #plugin do podpowiadania poszukanie intelisense
    lookup_field = 'private_id'
    queryset = Auctions.objects.all() # query na last
    serializer_class = AuctionsSerializer
    permissions_classes = [permissions.IsAuthenticated]


class ReportsAPIListView(APIView):

    def get(self, request):
        
        # auctions = Auctions.objects.all()
        auctions = Auctions.objects.all()
        auctionsDet = AuctionsDetails.objects.all()

        auctions = list(chain())

        result_list = auctions.union(auctions, auctionsDet)

        serializer = AuctionsWithDetailsSerializer(result_list, many=True)

        return Response({"auctions":serializer.data})

    def post(self,request):
        data = {}
        data['test'] = 'test'

        auctions = Auctions.objects.all()
        
        report = Report()

        report.generate(auctions)
        
        return Response(data)
