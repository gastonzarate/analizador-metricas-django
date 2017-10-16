from django import forms
from accounts.models import MyUser
from campaign.models import Campaign



class SelectCampaign(forms.Form):
    user = forms.ModelChoiceField(queryset=MyUser.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control m-b b-r-xl'}))
    campaign = forms.ModelChoiceField(queryset=Campaign.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control m-b b-r-xl'}))

    def __init__(self,*args,**kwargs):
        super(SelectCampaign, self).__init__(*args,**kwargs)
        self.fields['campaign'].choices = Campaign.objects.none()
