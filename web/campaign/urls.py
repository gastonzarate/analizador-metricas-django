from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from campaign.ajax import delete_campaign
from campaign.views import *

urlpatterns = [
    url(r'all/$',login_required(CampaignAll),name='campaign_all'),
    url(r'new/$', login_required(CampaignNew),name='campaign_new'),
    url(r'edit/$', login_required(CampaignEdit),name='campaign_edit'),
    url(r'csv/$',login_required(Csv),name='campaign_csv'),
    url(r'metrics/one/$', login_required(CampaignMetrics),name='campaign_metrics'),
    url(r'metrics/$', login_required(CampaignMetricsAll),name='campaign_metrics_all'),
    url(r'campaign/$',login_required(delete_campaign),name='delete_campaign')
]