from django import forms
from businesses.models import BusinessAccount
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions


class BusinessAccountModelForm(forms.ModelForm):

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

        labels = {
            'legalbusinessname': _('Legal Business Name (Required)'),
            'address_line1': _('Address Line 1 (Required)'),
            'address_line2': _('Address Line 2'),
            'city': _('City (Required)'),
            'state': _('State (Required)'),
        'zipcode': _('Zip Code (Required)'),
            'businesscategory': _('Business Category (Required)'),
            'businesslogo': _('Business Logo or Image (Required)'),
            'email': _('Business Email (Required)'),
            'phone': _('Business Phone (Required)'),
            'websiteurl': _('Business Website (Required)'),
        }


    #format in case of explicit validation
    def clean_businessname(self):
        legalbusinessname = self.cleaned_data.get("legalbusinessname")
        if legalbusinessname == "bad":
            raise forms.ValidationError("we only like good sociodeals")
        else:
            return legalbusinessname

    def clean_businesslogo(self):
        businesslogo = self.cleaned_data.get("businesslogo")
        if not businesslogo:
            raise forms.ValidationError("No image!")
        else:
            w, h = get_image_dimensions(businesslogo)
            if w != 400:
                raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 400px" % w)
            if h != 300:
                raise forms.ValidationError("The image is %i pixel high. It's supposed to be 300px" % h)
        return businesslogo



