from django.contrib import admin
from django.utils.text import slugify
from .models import Category, Organization, Opportunity

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("name",)}

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "social_links")

    def social_links(self, obj):
        return obj.website

    social_links.short_description = "Social Media"


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "country",
        "county",
        "remote",
        "featured",
        "application_deadline",
        "is_active",
    )

    list_filter = (
        "category",
        "country",
        "county",
        "remote",
        "featured",
        "is_active",
    )

    search_fields = (
        "title",
        "organization__name",
        "source",
    )

    list_editable = (
        "featured",
        "is_active",
    )

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = "application_deadline"

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "category", "organization")
        }),
        ("Location", {
            "fields": ("country", "region",  "county", "city", "remote")
        }),
        ("Opportunity Details", {
            "fields": (
                "opportunity_type",
                "application_deadline",
                "description",
                "eligibility",
                "benefits",
            )
        }),
        ("Application", {
            "fields": ("application_link", "application_email", "source")
        }),
        ("Publishing Options", {
            "fields": ("featured", "is_active")
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)
