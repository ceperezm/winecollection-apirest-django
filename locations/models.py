from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=60)
    country_id = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta:
        ordering = ['country_id__name', 'name']

    def __str__(self):
        return f"{self.name}, {self.country_id.name}"