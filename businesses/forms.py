from django import forms
from .models import BusinessLocations, BusinessAccount
from django.utils.translation import ugettext_lazy as _


class NewBusinessForm(forms.Form):
    agree = forms.BooleanField(label='Agree to Terms', widget=forms.CheckboxInput)


PUBLISH_CHOICES = (
    ('publish', "Publish"),
    ('draft', "Draft"),
)


class ProfileModelForm(forms.ModelForm):

    class Meta:
        model = BusinessAccount

        fields = [
            "legalbusinessname",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "zipcode",
            "businesscategory",
            "businesslogo",
            "email",
            "phone",
            "websiteurl",
        ]

    def clean_(self):
        business = self.cleaned_data.get("legalbusinessname")
        if business == "bad":
            raise forms.ValidationError("we only like good businesses")
        else:
            return business


class BusinessLocationsModelForm(forms.ModelForm):

    class Meta:
        model = BusinessLocations

        fields = [
            "locationname",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "zipcode",
            "phone",
            "websiteurl",
        ]





