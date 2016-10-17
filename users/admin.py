from django.contrib import admin
from .models import Transactions, Preferences, ReferralRewards


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_filter = []
    list_filter = []

    class Meta:
        model = Transactions


admin.site.register(Transactions, TransactionsAdmin)


class ReferralRewardAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_filter = []
    list_filter = []

    class Meta:
        model = ReferralRewards


admin.site.register(ReferralRewards, ReferralRewardAdmin)


class PreferencesAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_filter = ["user"]
    list_filter = ["user"]

    class Meta:
        model = Preferences


admin.site.register(Preferences, PreferencesAdmin)

