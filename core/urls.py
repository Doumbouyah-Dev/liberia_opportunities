
from django.urls import path
from . import views


urlpatterns = [
path("opportunities/", views.opportunities, name="opportunity_list"),
path("contact/", views.contact, name="contact"),
path("about/", views.about, name="about"),
]