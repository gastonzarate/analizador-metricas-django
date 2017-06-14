from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from campaign.views import *

urlpatterns = [
    url(r'all/$',login_required(CampaignAll),name='campaign_all'),
    url(r'new/$', login_required(CampaignNew),name='campaign_new'),
    url(r'metrics/(?P<campaign_id>\d{1,1000000})/$', login_required(CampaignMetrics),name='campaign_metrics'),
    url(r'metrics/$', login_required(CampaignMetricsAll),name='campaign_metrics_all')
]