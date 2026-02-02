from django.urls import path
from . import views

urlpatterns = [
    path("", views.opportunity_list, name="opportunity_list"),
    path("category/<slug:category_slug>/", views.opportunity_list, name="category_filter"),
    path("<slug:slug>/", views.opportunity_detail, name="opportunity_detail"),
]
