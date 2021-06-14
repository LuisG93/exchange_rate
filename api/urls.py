from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExchangeListView

exchange_patterns = ([
    #Views for blog
    path('', ExchangeListView.as_view(), name='exchange'),
], 'exchange')
