from django.conf.urls import url
from pay.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^payment/(?P<campaign_id>\d{1,1000000})/$', login_required(buy_my_item),name='pay_payment'),
    url(r'^return/$', login_required(return_url_premium), name='pay_return_url_premium'),
    url(r'^cancel/$', login_required(cancel_return_premium), name='pay_cancel_return_premium'),

]

