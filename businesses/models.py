from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify


class BusinessCategory(models.Model):
    description = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.description


class BusinessAccount(models.Model):

    class Meta:
        unique_together = ("accountuser", "legalbusinessname")

    accountuser = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    legalbusinessname = models.CharField(max_length=200, unique=True)
    businesslogo = models.ImageField(blank=False, null=False)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    businesscategory = models.ForeignKey(BusinessCategory)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100)
    websiteurl = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.legalbusinessname


def create_account_slug(instance, new_slug=None):
    slug = slugify(instance.legalbusinessname)

    if new_slug is not None:
        slug = new_slug

    qs = BusinessAccount.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_account_slug(instance, new_slug=new_slug)
    return slug


def businessaccount_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_account_slug(instance)

pre_save.connect(businessaccount_pre_save_receiver, sender=BusinessAccount)


class BusinessLocations(models.Model):
    business = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    locationname = models.CharField(max_length=100, unique=True)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    gps = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    websiteurl = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.locationname


def create_slug(instance, new_slug=None):
    slug = slugify(instance.locationname)

    if new_slug is not None:
        slug = new_slug

    qs = BusinessLocations.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def businesslocation_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(businesslocation_pre_save_receiver, sender=BusinessLocations)


class BusinessRating(models.Model):
    businessId = models.ForeignKey(BusinessLocations, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)













