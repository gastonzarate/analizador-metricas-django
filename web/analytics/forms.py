from django import forms

SOCIAL_NETWORK_CHOICES = (
    ('1', 'Facebook'),
    ('2', 'Google GND'),
    ('3', 'Google Search'),
    ('4', 'Twitter'),
    ('5', 'Otro'),
)

class FileCharge(forms.Form):
    title = forms.CharField(max_length=256,widget=forms.TextInput(attrs={"class":"form-control","required":True}))
    social_network = forms.ChoiceField(choices=SOCIAL_NETWORK_CHOICES,widget=forms.Select(attrs={"class":"form-control","required":True}))
    csv = forms.FileField()
