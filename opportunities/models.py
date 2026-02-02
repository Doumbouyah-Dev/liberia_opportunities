from django.db import models
from django.utils import timezone
from django.urls import reverse
from locations.models import Country, County, Region, City


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=150)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


class Opportunity(models.Model):

    OPPORTUNITY_TYPE_CHOICES = (
        ("paid", "Paid"),
        ("unpaid", "Unpaid"),
        ("funded", "Fully Funded"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="opportunities"
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        default=1  # Liberia
    )

    county = models.ForeignKey(
            County,
            on_delete=models.SET_NULL,
            null=True,
            default=1  # Liberia
        )

    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    remote = models.BooleanField(default=False)

    application_deadline = models.DateField()

    opportunity_type = models.CharField(
        max_length=20,
        choices=OPPORTUNITY_TYPE_CHOICES
    )

    description = models.TextField()
    eligibility = models.TextField()
    benefits = models.TextField(blank=True)

    application_link = models.URLField(blank=True)
    application_email = models.EmailField(blank=True)

    source = models.CharField(max_length=150)

    featured = models.BooleanField(default=False)

    posted_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-featured", "-posted_date"]

    def is_expired(self):
        return self.application_deadline < timezone.now().date()

    def get_absolute_url(self):
        return reverse("opportunity_detail", args=[self.slug])

    def __str__(self):
        return self.title
