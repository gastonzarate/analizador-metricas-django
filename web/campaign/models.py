
from django.db import models
from model_utils.managers import InheritanceManager
from accounts.models import MyUser


class StatusCampaign(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    objects = InheritanceManager()

    def __str__(self):
        return self.name

    def delete(self):
        return False

    def get_name(self):
        return self.name

    def is_working(self):
        return False

    def is_end(self):
        return False

    def is_delete(self):
        return False


class Working(StatusCampaign):
    def is_delete(self):
        return False

    def get_name(self):
        return self.name

    def is_end(self):
        return False

    def is_working(self):
        return True

    def delete(self, campaign):
        campaign.set_status(Delete.objects.all().first())
        campaign.save()
        return True


class End(StatusCampaign):
    def is_delete(self):
        return False

    def is_working(self):
        return False

    def is_end(self):
        return True

    def delete(self, campaign):
        campaign.set_status(Delete.objects.all().first())
        campaign.save()
        return True

    def active(self,campaign):
        if campaign.get_budget_spent()<campaign.get_budget():
            campaign.set_status(Working.objects.all().first())

class Delete(StatusCampaign):
    def is_end(self):
        return False

    def is_working(self):
        return False

    def is_delete(self):
        return True

    def delete(self, campaign):
        pass

    def active(self):
        pass

class Campaign(models.Model):
    user = models.ForeignKey(MyUser)
    name = models.CharField(max_length=256)
    budget = models.FloatField()
    budget_spent = models.FloatField(default=0)
    status = models.ForeignKey(StatusCampaign,default=1)

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

    def delete(self):
        return self.get_status().delete(self)

    def set_data(self,campaign):
        self.name= campaign.name
        self.budget=campaign.budget
        self.get_status().active(self)
        self.save()



class SocialNetwork(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Ads(models.Model):
    campaign = models.ForeignKey(Campaign)
    name = models.CharField(max_length=256)
    social_network = models.ForeignKey(SocialNetwork)

    def get_name(self):
        return self.name


class Register(models.Model):
    ads = models.ForeignKey(Ads)
    week_start = models.DateField()
    week_end= models.DateField()
    spend = models.FloatField()
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    sign_ups= models.IntegerField()
    conversion = models.IntegerField()
    revenues = models.FloatField()

