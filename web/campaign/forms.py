from django import forms

from accounts.models import MyUser
from campaign.models import Campaign, SocialNetwork


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name','budget']
        widgets = {
            'name': forms.TextInput(attrs={'required':True, 'class': 'form-control m-b b-r-xl'}),
            'budget': forms.NumberInput(attrs={'required': True, 'class': 'form-control m-b b-r-xl','step':100,'min':500})
        }


class CsvFile(forms.Form):
    campaign = forms.ModelChoiceField(queryset=Campaign.objects.all(),widget=forms.Select(attrs={'class':'form-control m-b b-r-xl'}))
    csv = forms.FileField()
    social_network = forms.ModelChoiceField(queryset=SocialNetwork.objects.all(),widget=forms.Select(attrs={'class':'form-control m-b b-r-xl'}))
