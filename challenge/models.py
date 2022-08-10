from django.db import models

# Create your models here.
class ForexConvert(models.Model):
    SourceCurrency = models.TextField(
        max_length=255,
        null=False,
        blank=False)
    DestinationCurrency = models.TextField(
        max_length=255,
        null=False,
        blank=False)
    SourceAmount = models.FloatField (
        null=False,
        blank=False
    )
    DestinationAmount = models.FloatField (
        null=False,
        blank=False
    )