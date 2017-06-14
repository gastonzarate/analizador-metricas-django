from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from metrics.ajax import get_campaign
from metrics.views import *

urlpatterns = [
    url(r'csv/$',login_required(Csv),name='metrics_csv'),
    url(r'select/$',login_required(Select),name='metrics_select'),
    url(r'campaign/(?P<campaign_id>\d{1,1000000})$',login_required(Metrics),name='metrics'),
    url(r'get_campaign/$',login_required(get_campaign),name='get_campaign')
]