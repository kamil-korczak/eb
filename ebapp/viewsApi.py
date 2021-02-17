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

from .serializer import AuctionsSelectedSerializer
from ebapp.classes.report import Report

# Create your views here.
# class AuctionsAPIViewSet(viewsets.ModelViewSet):
#     lookup_field = 'external_id'
#     queryset = Auctions.objects.all() # query na last
#     serializer_class = AuctionsSerializer
#     permissions_classes = [permissions.IsAuthenticated]


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

    def post(self, request, pk, format=None):
        auction = self.get_object(pk)

        serializer = AuctionsSelectedSerializer(auction, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
