from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from django.db import models
from model_utils.managers import InheritanceManager


class Plan(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=254)

    objects = InheritanceManager()

    def __str__(self):
        return self.name

    def is_free(self):
        return False

    def is_premium(self):
        return False

    def get_name(self):
        return self.name


class Free(Plan):
    def is_free(self):
        return True

    def is_premium(self):
        return False


class Premium(Plan):
    def is_premium(self):
        return True


class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="user_customer", blank=True,null=True)
    subscr_date = models.DateField(auto_now_add=True)
    days = models.IntegerField(default=365)
    plan = models.ForeignKey(Plan,blank=True,null=True)

    def get_plan(self):
        return Plan.objects.get_subclass(id=self.plan.id)

    def is_finish(self):
        days_now = (now().date() - self.subscr_date).days
        return (days_now>self.days)

    def remaining_days(self):
        return (self.subscr_date - now().date()).days + self.days

    def date_finish(self):
        return (now().date()+timedelta(days=self.remaining_days()))

    def __str__(self):
        return self.user.username if self.user!=None else 'Sin Usuario Asignado'

    def get_user(self):
        return self.user

    def get_subscr_date(self):
        return self.subscr_date

    def get_days(self):
        return self.days

