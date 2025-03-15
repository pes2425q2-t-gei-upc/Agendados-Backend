from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Town(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'region')


class Location(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.CharField(max_length=400, null=True)
    space = models.CharField(max_length=400, null=True)
