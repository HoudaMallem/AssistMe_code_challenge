from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Company(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255,
                                default="",
                                null=True,
                                blank=True)


class Sensor(models.Model):
    sensorId = models.CharField(primary_key=True, default="", max_length=255)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="sensors")
    active = models.BooleanField(default=False)
    labels = ArrayField(models.CharField(max_length=100), default=list)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name="measurements")
    date = models.DateTimeField(default=timezone.now)
    value = models.JSONField(default=dict)
