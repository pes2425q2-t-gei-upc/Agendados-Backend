from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)

class Town(models.Model):
    name = models.CharField(max_length=200, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

class Location(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=200)
    space = models.CharField(max_length=200)