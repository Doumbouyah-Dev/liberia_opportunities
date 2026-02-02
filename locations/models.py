from django.db import models

# Country Model
class Country(models.Model):
    name = models.CharField(max_length=100, default="Liberia")
    code = models.CharField(max_length=3, default="LBR")

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

# Region Model
class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="regions"
    )

    def __str__(self):
        return f"{self.name} ({self.country.name})"

# County Model
class County(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="counties"
    )

    def __str__(self):
        return f"{self.name} ({self.region.name})"

# City Model
class City(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name="cities"
    )

    def __str__(self):
        return f"{self.name} ({self.county.name})"


