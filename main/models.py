from django.db import models

# Create your models here.

class Person(models.Model):
    CardNumber = models.BigIntegerField(primary_key=True)
    PIN = models.PositiveSmallIntegerField()
    CVV = models.PositiveSmallIntegerField()
    Balance = models.PositiveIntegerField()
    sessionid = models.CharField(max_length=6, blank=True, unique=True)


