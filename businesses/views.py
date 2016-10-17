from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from dummy_app.mixins import MultiSlugMixin, LoginRequiredMixin, StaffRequiredMixin
from .forms import NewBusinessForm, ProfileModelForm, BusinessLocationsModelForm
from .models import BusinessAccount, BusinessLocations, BusinessRating
from dummy_app.forms import BusinessAccountModelForm


class BusinessAccountDashboard(LoginRequiredMixin, FormMixin, View):
    form_class = NewBusinessForm
    success_url = "businesses/dashboard.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form()
        account = BusinessAccount.objects.filter(business=self.request.user)
        exists = account.exists()
        active = None

        context = {}

        if exists:
            account = account.first()
            active = account.active

        if not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Business Dashboard"
        else:
            pass

        return render(request, "businesses/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(BusinessAccountDashboard, self).form_valid(form)
        obj = BusinessAccount.objects.create(business=self.request.user)
        return valid_data


class BusinessProfileCreateView(LoginRequiredMixin, MultiSlugMixin, CreateView):
    template_name = "businesses/create_profile.html"
    form_class = ProfileModelForm
    success_url = "/businesses/profile"

    def form_valid(self, form):
        form.instance.accountuser = self.request.user
        return super(BusinessProfileCreateView, self).form_valid(form)


class BusinessProfileUpdateView(StaffRequiredMixin, MultiSlugMixin, UpdateView):
    model = BusinessAccount
    template_name = "businesses/edit_profile.html"
    form_class = BusinessAccountModelForm
    success_url = "/businesses/profile"

    def form_valid(self, form):
        form.instance.accountuser = self.request.user
        return super(BusinessProfileUpdateView, self).form_valid(form)


def BusinessProfileDetailView(request):
    account = BusinessAccount.objects.filter(accountuser=request.user)
    locations = BusinessLocations.objects.filter(business=account)
    ratings = BusinessRating.objects.filter(businessId=locations)

    context = {
        "account": account,
        "ratings": ratings
    }

    return render(request, "businesses/profile.html", context)


def Support(request):
    return render(request, 'businesses/support.html')


def Billing(request):
    return render(request, 'businesses/billing.html')


def Appoval(request):
    return render(request, 'businesses/Approval.html')


def CreditCard(request):
    return render(request, 'businesses/add_creditcard.html')


def CreditCardInfoCreateView(request):

    return render(request, 'businesses/add_creditcard.html')


def CreditCardInfoUpdateView(request):

    return render(request, 'businesses/edit_creditcard.html')


def Faq(request):
    return render(request, 'businesses/faq.html')


def Settings(request):
    return render(request, 'businesses/settings.html')


def Locations(request):
    account = BusinessAccount.objects.filter(accountuser=request.user)
    locations = BusinessLocations.objects.filter(business=account)

    context = {
        'locations': locations,
    }
    return render(request, 'businesses/locations.html', context)


class LocationCreateView(LoginRequiredMixin, MultiSlugMixin, CreateView):
    template_name = "businesses/create_location.html"
    form_class = BusinessLocationsModelForm
    success_url = "/businesses/approval"

    def form_valid(self, form):
        form.instance.business = BusinessAccount.objects.get(accountuser=self.request.user)
        return super(LocationCreateView, self).form_valid(form)


class LocationUpdateView(StaffRequiredMixin, MultiSlugMixin, UpdateView):
    model = BusinessLocations
    template_name = "businesses/edit_location.html"
    form_class = BusinessLocationsModelForm
    success_url = "/businesses/locations"

    def form_valid(self, form):
        form.instance.business = BusinessAccount.objects.get(accountuser=self.request.user)
        return super(LocationUpdateView, self).form_valid(form)


class LocationDeleteView(StaffRequiredMixin, MultiSlugMixin, DeleteView):
    model = BusinessLocations
    template_name = "businesses/confirm_delete_location.html"
    form_class = BusinessLocationsModelForm
    success_url = "/businesses/locations"


