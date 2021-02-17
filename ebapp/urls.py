# ebapp/urls.py
from django.views.generic.base import RedirectView

from django.urls import path, re_path, include
from rest_framework import routers
from . import views, viewsApi


urlpatterns = [
    # * normal urls
    path('', views.AuctionsView.as_view(), name='home-notlogged'),
    
    path('auctions/', views.AuctionsView.as_view(), name='home'),
    path('auctions/', views.AuctionsView.as_view(), name='auctions'),

    re_path(r'^auctions/page-(?P<page>\d+)/$', views.AuctionsView.as_view(), name='home'),
    
    re_path(r'^auctions/(?P<external_id>[0-9]{12})/', views.AuctionsPageView.as_view(), name='auction'),
    
    re_path(r'^auctions/(?P<some_number>\d+)', views.error_404_view),

    path('auctions/add/', views.AuctionsAddSinglePageView.as_view(), name='auctions-add-single'),
    re_path(r'^auctions/add/(?P<add_type>(single|multiple))/', views.AuctionsAddPageView.as_view(), name='auctions-add'),

    path('accounts/', include('django.contrib.auth.urls')), # includes login
    
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    path('settings/', views.SettingsView.as_view(), name='settings'),
    
    # * API urls
    re_path(r'api/auctions/(?P<pk>\d+)', viewsApi.AuctionsSelectedAPIView.as_view()),
]