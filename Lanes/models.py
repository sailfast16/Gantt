# Defines Lane/Task record fields for DB
# -----------------------------------------------------------------------------------------
# DB automatically assigns PK to an always increasing value
# JS file uses the Lane ID to determine Y-pos so PK needs to always be the lowest available value

from django.db import models


class Lane(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=6, decimal_places=2)


class Task(models.Model):
    # STATUS_CHOICES = ['Not Started', 'Finished', 'In Progress']
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    start_date = models.IntegerField(default=0)
    length = models.IntegerField(default=1)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)

