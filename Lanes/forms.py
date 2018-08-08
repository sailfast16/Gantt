from django import forms
from .models import Lane
from .models import Task


class laneForm(forms.Form):
    name = forms.CharField(max_length=10)
    description = forms.CharField(max_length=50, widget=forms.Textarea)
    cost = forms.DecimalField(max_digits=6, decimal_places=2)


class taskForm(forms.Form):
    name = forms.CharField(max_length=20)
    description = forms.CharField(max_length=50)
    length = forms.IntegerField()
    start_date = forms.IntegerField()

    # this isn't working properly
    # tries to update the lane with the task parameters and throws an error
    lane = forms.ModelChoiceField(queryset=Lane.objects.all())

