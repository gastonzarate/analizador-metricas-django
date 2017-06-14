from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from campaign.forms import CampaignForm
from campaign.models import *

def CampaignAll(request):
    campaings = Campaign.objects.filter(user=request.user)
    return render(request,'campaign_all.html',{'campaings': campaings,'footer':(len(campaings)>5)})


def CampaignNew(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["budget"] >= 500:
                campaign = form.save(commit=False)
                campaign.set_user(request.user)
                campaign.save()
                return HttpResponseRedirect(reverse('pay_payment',kwargs={'campaign_id':campaign.id}))
            else:
                form.add_error("budget","Presupuesto Minimo $500")
    else:
        form = CampaignForm()
    return render(request,'campaign_new.html',{'form':form})


def CampaignMetrics(request,campaign_id):
    campaign = Campaign.objects.get(id=campaign_id,user=request.user)
    if campaign.get_status().is_waiting_pay():
        return HttpResponseRedirect(reverse('pay_payment',kwargs={'campaign_id':campaign.id}))

    return render(request,'campaign_metrics.html',{'campaign':campaign})


def CampaignMetricsAll(request):
    return render(request,'campaign_metrics_all.html')