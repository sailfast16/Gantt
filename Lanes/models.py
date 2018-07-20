# Defines Lane/Task record fields for DB
# -----------------------------------------------------------------------------------------
# DB automatically assigns PK to an always increasing value
# JS file uses the Lane ID to determine Y-pos so PK needs to always be the lowest available value

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multipleselectionfield import MultipleSelectionField

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
    lane = models.IntegerField(default=0)


color_choices = ((1,'Red'),(2,'Green'),(3,'Blue'))
resource_list = ((1,'Resource 1'),(2,'Resource 2'), (3, 'Resource 3'))


class Task1(models.Model):
    family = models.IntegerField(default=0)
    resources = MultipleSelectionField(choices=resource_list)
    least_start = models.IntegerField(default=0)
    max_end = models.IntegerField(default=0)
    start = models.IntegerField(MinValueValidator(least_start))
    end = models.IntegerField(MaxValueValidator(max_end))
    late_cost = models.IntegerField(default=100)
    early_cost = models.IntegerField(default=0)
    fixed = models.BooleanField()
    color = models.IntegerField(choices=color_choices, default=1)

