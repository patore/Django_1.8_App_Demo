from django.db import models
from django.contrib.auth.models import User
from businesses.models import BusinessAccount, BusinessCategory, BusinessLocations


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    businessLocation = models.ForeignKey(BusinessLocations, on_delete=models.CASCADE)
    redeemed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


class ReferralRewards(models.Model):
    class Meta:
        unique_together = ('user', 'businessLocation', 'referredto')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    businessLocation = models.ForeignKey(BusinessLocations, on_delete=models.CASCADE)
    redeemed = models.BooleanField(default=False)
    referredto = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referredto')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


class Points(models.Model):
    class Meta:
        unique_together = ('user', 'businessLocation')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    businessLocation = models.ForeignKey(BusinessLocations, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)


class Preferences(models.Model):
    class Meta:
        unique_together = ('user', 'businesslocationid')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    businesslocationid = models.ForeignKey(BusinessLocations, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
