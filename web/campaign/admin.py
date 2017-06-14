from django.contrib import admin
from campaign.models import *

# Register your models here.
admin.site.register(Campaign)
admin.site.register(StatusCampaign)
admin.site.register(Working)
admin.site.register(WaitingPay)
admin.site.register(Pay)
admin.site.register(End)


