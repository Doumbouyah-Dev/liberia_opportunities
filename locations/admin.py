from django.contrib import admin
from .models import Country, Region, County, City

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    list_filter = ("region",)



@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "county")
    list_filter = ("county",)
