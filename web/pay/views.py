from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import mercadopago
import json
from pay.models import Customer, Premium
import os

class HomePayView(TemplateView):
    template_name = 'pay_plans.html'


def buy_my_item(request):

    code = None
    description = None
    user = request.user
    if request.POST.get('token',''):
        mp = mercadopago.MP(os.environ.get('ACCESS_TOKEN_MP'))

        dic = {
            "transaction_amount": 97,
            "token": "%s" %request.POST.get('token',''),
            "installments": 1,
            "description": "Crece",
            "payment_method_id": request.POST.get('paymentMethodId',''),
            "payer": {
                "email": "codicero@gmail.com"
            },
            "external_reference": user.username,
            "statement_descriptor": "CODIPAY - Año Premium",
        }
        payment = mp.post("/v1/payments", dic )
        json.dumps(payment, indent=4)

        if payment['status'] == 201:
            if payment['response']['status'] == 'approved':
                customer = Customer(user=user,plan=Premium.objects.all().first())
                customer.save()
                user.set_customer(customer)
                user.save()
                return HttpResponseRedirect(reverse('pay_return_url_premium'))
            else:
                description = payment['response']['status']
                code = 201
        else:
            code = payment['response']['cause'][0]['code']
            description = payment['response']['cause'][0]['description']

    return render(request,'pay_payment.html',{'code':code,'description':description,'PUBLIC_KEY_MP': os.environ.get('PUBLIC_KEY_MP')})


@csrf_exempt
def return_url_premium(request):
    return render(request,'pay_premium_ok.html',{})


@csrf_exempt
def cancel_return_premium(request):
    return render(request,'pay_plans.html',{})

