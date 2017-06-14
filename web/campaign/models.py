import os

from django.db import models
from s3direct.fields import S3DirectField
from model_utils.managers import InheritanceManager
from accounts.models import MyUser


class StatusCampaign(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    objects = InheritanceManager()

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def is_waiting_pay(self):
        return False

    def is_working(self):
        return False

    def is_pay(self):
        return False

    def is_end(self):
        return False


class WaitingPay(StatusCampaign):

    def is_waiting_pay(self):
        return True

    def created(self,campaign,waiting_pay):
        campaign.set_status(self)
        campaign.save()


class Working(StatusCampaign):

    def is_working(self):
        return True


class Pay(StatusCampaign):

    def is_pay(self):
        return True

    def paid_out(self,campaign):
        campaign.set_status(self)
        campaign.save()


class End(StatusCampaign):

    def is_end(self):
        return True


class Campaign(models.Model):
    user = models.ForeignKey(MyUser)
    name = models.CharField(max_length=256)
    budget = models.FloatField()
    budget_spent = models.FloatField(default=0)
    status = models.ForeignKey(StatusCampaign,default=1)
    image = S3DirectField(dest=os.environ.get('AWS_STORAGE_BUCKET_NAME'), blank=True,null=True)

    def __str__(self):
        return self.name

    def set_status(self,status):
        self.status = status

    def set_user(self,user):
        self.user = user

    def get_user(self):
        return self.user

    def get_budget(self):
        return self.budget

    def get_name(self):
        return self.name

    def get_budget_spent(self):
        return self.budget_spent

    def get_status_obj(self):
        return self.status

    def get_status(self):
        return StatusCampaign.objects.get_subclass(id=self.status.id)