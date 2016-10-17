from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from businesses.models import BusinessAccount, BusinessLocations
from .forms import BusinessAccountModelForm
from .mixins import MultiSlugMixin
from django.views.generic.edit import CreateView
from users.models import Transactions, Preferences, ReferralRewards
from django.http import HttpResponseRedirect
from django.db.models import Sum


class FacebookLogin(SocialLoginView):
    """
        Facebook login API Call
    """
    adapter_class = FacebookOAuth2Adapter


def home(request):
    if request.user.is_staff and request.user.is_authenticated:
        context = {}
        """
            check if the current logged in user has a business account
        """
        try:
            currentaccount = BusinessAccount.objects.get(accountuser=request.user)
        except:
            currentaccount = None

        """
            Check if the current logged in user has any transactions
        """
        try:
            transaction = Transactions.objects.filter(businessAccount=currentaccount)
            context["transactions"] = transaction.count()
            x = Transactions.objects.aggregate(Sum('amount'))
            context["x"] = x

        except:
            context["transactions"] = 0

        """
            check if there are any redeemed transactions
        """
        try:
            redeemedtransaction = Transactions.objects.filter(businessAccount=currentaccount, redeemed=True)
            context["redeemedtransactions"] = redeemedtransaction.count()
        except:
            context["redeemedtransactions"] = 0

        """
            check if there are any rewards
        """
        try:
            rewards = ReferralRewards.objects.filter(businessAccount=currentaccount)
            context["referrals"] = rewards.count()
        except:
            context["referrals"] = 0

        """
            check if any of the rewards have been redeemed
        """
        try:
            redeemedrewards = ReferralRewards.objects.filter(businessAccount=currentaccount, redeemed=True)
            context["redeemedreferrals"] = redeemedrewards.count()
        except:
            context["redeemedreferrals"] = 0

        """
            get the transaction conversion rate
        """
        try:
            x = (context["redeemedtransactions"] / context["transactions"]) * 100

            context["transactionconversionrate"] = '%.2f' % round(x, 2)
        except:
            context["transactionconversionrate"] = 0

        """
            get the referral conversion rate
        """
        try:
            xy = (context["redeemedreferrals"] / context["referrals"]) * 100
            context["referralconversionrate"] = '%.2f' % round(xy, 2)
        except:
            context["referralconversionrate"] = 0

        context["title"] = "Summary"
        context["active"] = True

        return render(request, "businesses/dashboard.html", context)

    elif request.user.is_active:

        return HttpResponseRedirect("new_business_form")

    else:

        return render(request, "home.html")


def businessProfile(request):
    business = BusinessLocations.objects.all()

    context = {
        "object_list": business
    }

    return render(request, "businesses/profile.html", context)


def dummy_appbusiness(request):

    return render(request, "dummy_appbusiness.html")


class BusinessAccountCreateView(MultiSlugMixin, CreateView):
    model = BusinessAccount
    template_name = "newbusinessform.html"
    form_class = BusinessAccountModelForm
    success_url = "/businesses/businesslocationcreate/"

    def form_valid(self, form):
        form.instance.accountuser = self.request.user
        return super(BusinessAccountCreateView, self).form_valid(form)



