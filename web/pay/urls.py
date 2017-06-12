from django.conf.urls import patterns, url
from pay.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^payment/$', login_required(buy_my_item),name='pay_payment'),
    url(r'^return/$', login_required(return_url_premium), name='pay_return_url_premium'),
    url(r'^cancel/$', login_required(cancel_return_premium), name='pay_cancel_return_premium'),
    url(r'^plans/$', login_required(HomePayView.as_view()), name='pay_plans'),

]

