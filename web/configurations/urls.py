"""landingpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView

from django.views.static import serve

from analytics.views import Csv

handler404 = 'home.views.handler404'

urlpatterns = [
    url(r'^.well-known/acme-challenge/apleiLjuTLpQoQDhrIjpvsI0vwD1AvYXWQWiJyQt15Q/$', TemplateView.as_view(template_name='home_ssl.html')),
    #Admin
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT,'show_indexes':settings.DEBUG}),
    url(r'^admin/', admin.site.urls),
    #Auth Email
    url(r'^accounts/', include('accounts.urls')),
    #My Apps
    # url(r'^pay/',include('pay.urls')),
    # url(r'campaign/',include('campaign.urls')),
    # url(r'metrics/',include('metrics.urls')),
    # Aws
    url(r'^s3direct/', include('s3direct.urls')),
    # App Home
    url(r'^$', Csv, name='index'),
    # url(r'^',  include('home.urls')),
            ]
