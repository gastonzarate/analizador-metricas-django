from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from campaign.models import Campaign
from metrics.forms import SelectCampaign




def Select(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = SelectCampaign(request.POST)
            if form.is_valid():
                campaign = form.cleaned_data["campaign"]
                return HttpResponseRedirect(reverse("metrics",kwargs={"campaign_id":campaign.id}))
        else:
            form = SelectCampaign()

        return render(request,"metrics_select.html",{"form":form})
    else:
        return HttpResponseRedirect(reverse('campaign_all'))


def Metrics(request,campaign_id):
    if request.user.is_staff:
        campaign= Campaign.objects.get(id=campaign_id)
        return render(request,"metrics.html",{"campaign":campaign})
    else:
        return HttpResponseRedirect(reverse('campaign_all'))


