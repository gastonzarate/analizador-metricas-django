import datetime

from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from campaign.forms import CampaignForm, CsvFile
from campaign.models import *
import csv
from io import TextIOWrapper
import re


def CampaignAll(request):
    campaings = Campaign.objects.filter(user=request.user)
    return render(request,'campaign_all.html',{'campaings': campaings,'footer':(len(campaings)>5)})

def CampaignEdit(request):
    id = request.GET.get('camp_id','')
    campaign = Campaign.objects.get(id=id)
    if campaign.get_user() == request.user:
        if request.method == 'POST':
            form = CampaignForm(request.POST)
            if form.is_valid():
                campaign.set_data(form.save(commit=False))
                return HttpResponseRedirect(reverse('campaign_csv',kwargs={'campaign_id':campaign.id}))
        else:
            form = CampaignForm(initial=campaign)
        return render(request,'campaign_new.html',{'form':form})
    else:
        raise Http404

def CampaignNew(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
                campaign = form.save(commit=False)
                campaign.set_user(request.user)
                campaign.save()
                return HttpResponseRedirect(reverse('campaign_csv'))
    else:
        form = CampaignForm()
    return render(request,'campaign_new.html',{'form':form})


def CampaignMetrics(request):
    id = request.GET.get('camp_id', '')
    campaign = Campaign.objects.get(id=id)
    if campaign.get_user()==request.user or request.user.is_staff:
        return render(request,'campaign_metrics.html',{'campaign':campaign})
    else:
        raise Http404


def Csv(request):
    user = request.user
    if user.is_staff:
        if request.method=='POST':
            form = CsvFile(request.POST,request.FILES)
            if form.is_valid():
                campaign = form.cleaned_data["campaign"]
                social_network = form.cleaned_data["social_network"]
                #Creo una diccionario con los auncios
                ads_all = Ads.objects.filter(campaign=campaign)
                ads_dict = {}
                for ads in ads_all:
                    ads_dict[ads.get_name()] = ads

                registers=[]

                file = request.FILES['csv']
                text = TextIOWrapper(file.file, encoding='utf-8 ', errors='replace')
                data = csv.reader(text, delimiter=",")
                cont=0
                patron = re.compile(r'\d+.*,*\d*')
                patron_int = re.compile(r'\d+')
                for row in data:
                    if cont!=0:
                        week = row[0]
                        week_start = datetime.datetime.strptime(week.split("-")[0].strip(), '%Y/%m/%d').date()
                        week_end = datetime.datetime.strptime(week.split("-")[1].strip(), '%Y/%m/%d').date()
                        ads = row[1]
                        spend = float(patron.search(row[2]).group().replace(',','.'))
                        impressions = int(patron_int.search(row[3]).group())
                        clicks = int(patron_int.search(row[4]).group())
                        sign_ups = int(patron_int.search(row[5]).group())
                        conversions = int(patron_int.search(row[6]).group())
                        revenues = float(patron.search(row[7]).group().replace(',','.'))

                        if not ads in ads_dict:
                            ads_new = Ads(campaign=campaign,social_network=social_network,name=ads)
                            ads_new.save()
                            ads_dict[ads_new.get_name()]= ads_new

                        registers.append(Register(ads=ads_dict[ads], spend=spend, impressions=impressions,
                                               clicks=clicks, sign_ups=sign_ups, conversion=conversions,
                                               revenues=revenues, week_start=week_start, week_end=week_end))

                    cont+=1

                Register.objects.bulk_create(registers)

                return HttpResponseRedirect(reverse("campaign_metrics",kwargs={"campaign_id":campaign.id}))
        else:
            campaigns = Campaign.objects.filter(user=user)
            form = CsvFile(initial={'campaign':campaigns})
        return render(request,'campaign_csv.html',{'form':form})
    else:
        return HttpResponseRedirect(reverse('campaign_all'))


def CampaignMetricsAll(request):
    return render(request,'campaign_metrics_all.html')