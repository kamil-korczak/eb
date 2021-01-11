# ebapp/urls.py
from django.views.generic.base import RedirectView

from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views, viewsApi

from django.conf.urls import handler404


# router.register(r'reports', views.ReportsViewSet) #views.ReportsViewSet


router = routers.DefaultRouter()
router.register(r'api/auctions', viewsApi.AuctionsAPIViewSet)


urlpatterns = [
    # * normal urls
    path('', views.AuctionsView.as_view(), name='home-notlogged'),
    
    path('auctions/', views.AuctionsView.as_view(), name='home'),
    path('auctions/', views.AuctionsView.as_view(), name='auctions'),

    re_path(r'^auctions/page-(?P<page>\d+)/$', views.AuctionsView.as_view(), name='home'),


    re_path(r'^auctions/(?P<external_id>[0-9]{12})/add', views.AuctionsAddPageView.as_view()),
    
    re_path(r'^auctions/(?P<external_id>[0-9]{12})/', views.AuctionsPageView.as_view(), name='auction'),
    
    re_path(r'^auctions/(?P<some_number>\d+)', views.error_404_view),

    path('auctions/add/', views.AuctionsAddSinglePageView.as_view(), name='auctions-add-single'),
    re_path(r'^auctions/add/(?P<add_type>(single|multiple))/', views.AuctionsAddPageView.as_view(), name='auctions-add'),
    
    

    path('accounts/', include('django.contrib.auth.urls')), # includes login
    
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    path('settings/', views.SettingsView.as_view(), name='settings'),
    
    # * API urls
    re_path(r'api/auctions/(?P<pk>\d+)', viewsApi.AuctionsSelectedAPIView.as_view()),

    # path('api/auctions/selected/', viewsApi.AuctionsSelectedListAPIView.as_view()),

    #path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    #path('api/', include(router.urls)),
    #re_path(r'api/auctions/id/(?P<private_id>\d+)', viewsApi.AuctionsPrivateIdAPIViewSet.as_view()),
    #path('api/reports/', viewsApi.ReportsAPIListView.as_view()),
        
    # path('', RedirectView.as_view(url='/'), name='go-home'),
    # path('', RedirectView.as_view(url='/auctions/'), name='go-home', kwargs={'redirect_authenticated_user': False}),
    # path('auctions/add/', views.AuctionsAddPageView.as_view(), name='auctions-add'),
    # re_path('auctions/add/', views.AuctionsAddSinglePageView.as_view(), name='auctions-add-single'),
    # re_path(r'^auctions/add/(?P<external_id>[0-9]{12})/', views.AuctionsAddSinglePageView.as_view(), name='auctions-add-single'),
    # path('auctions/add/', views.AuctionsAddSinglePageView.as_view(), name='auctions-add'),
]


#TODO_LATER
#handler404 = 'ebapp.views.error_404_view'