from django import forms
from campaign.models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name','budget','image']
        widgets = {
            'name': forms.TextInput(attrs={'required':True, 'class': 'form-control m-b b-r-xl'}),
            'budget': forms.NumberInput(attrs={'required': True, 'class': 'form-control m-b b-r-xl','step':100,'min':500})
        }



