from django.contrib import admin
from .models import BusinessAccount, BusinessLocations, BusinessCategory, BusinessRating


class BusinessAccountAdmin(admin.ModelAdmin):
    list_display = ["legalbusinessname", "active"]
    search_filter = ["legalbusinessname"]
    list_filter = ["legalbusinessname"]
    list_editable = ["active"]

    class Meta:
        model = BusinessAccount


class BusinessLocationsAdmin(admin.ModelAdmin):
    list_display = ["locationname", "address_line1", "address_line2", "city", "state", "zipcode"]
    search_filter = ["locationname", "city", "state", "zipcode"]
    list_filter = ["locationname", "city", "state", "zipcode"]

    class Meta:
        model = BusinessLocations


class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "description"]
    search_filter = ["description"]
    list_filter = ["description"]

    class Meta:
        model = BusinessCategory


class BusinessRatingAdmin(admin.ModelAdmin):
    list_display = ["businessId", "userId", "rating", "review"]
    search_filter = ["businessId"]
    list_filter = ["businessId"]

    class Meta:
        model = BusinessRating


admin.site.register(BusinessAccount, BusinessAccountAdmin)
admin.site.register(BusinessLocations, BusinessLocationsAdmin)
admin.site.register(BusinessCategory, BusinessCategoryAdmin)
admin.site.register(BusinessRating, BusinessRatingAdmin)

