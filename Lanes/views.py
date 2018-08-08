# Functions to handle HTTP requests

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Lane
from .models import Task
from .forms import laneForm
from .forms import taskForm
import json
from solver.FirstFit import run


# Sends you to the home page
def index(request):
    return render(request, 'Lanes/index.html')


# Displays the Add Lane form
# sends form inputs to DB
def addLane(request):
    if request.method == 'POST':
        form = laneForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            cost = form.cleaned_data['cost']

            Lane.objects.create(
                name=name,
                description=description,
                cost=cost
            ).save()

            return HttpResponseRedirect('/')


    else:
        form = laneForm()

        return render(request, 'Lanes/addLane.html', {'laneForm': form})

# Displays the Add Task form
# sends form inputs to DB
def addTask(request):
    if request.method == 'POST':
        form = taskForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            start_date = form.cleaned_data['start_date']
            length = form.cleaned_data['length']
            lane = form.cleaned_data['lane']

            Task.objects.create(
                name=name,
                description=description,
                start_date=start_date,
                length=length,
                lane=lane
            ).save()

            return HttpResponseRedirect('/')

    else:
        form = taskForm()

        return render(request, 'Lanes/addTask.html', {'taskForm': form})

# new lane, the task ID and the new X-pos
# are sent with AJAX request at the end of the URL
# updates the record values in the DB for the specific task
def moveTask(request,lane,task,start,end):
    task_id = task
    task = Task.objects.get(pk=task_id)
    task.resources = lane
    task.start = start
    task.end = end
    task.save()

    return HttpResponseRedirect('/')

def addPosition(request, lane, task, start, end):
    task_id = task
    task = Task.objects.get(pk=task_id)
    task.resources = lane
    task.start = start
    task.end = end
    task.save()

    return HttpResponse(status=201)

# Defines the endpoint to access Lane Records as JSON
def lanesJSON(request):
    data = list(Lane.objects.values())
    return JsonResponse(data, safe=False)

# Defines the endpoint to access Task Records as JSON
def taskJSON(request):
    data = list(Task.objects.values())
    return JsonResponse(data, safe=False)


def uploadJSON(request):
    return render(request, 'Lanes/addTask.html')

def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        json_file = json.load(file)

        Task.objects.all().delete()

        for i in json_file:
            Task.objects.create(
                name=i['name'],
                family=i['family'],
                least_start=i['least_start'],
                max_end=i['max_end'],
                late_cost=i['late_cost'],
                length=i['length'],
                early_cost=i['early_cost'],
                fixed=i['fixed'],
                color=i['color']).save()

    return HttpResponseRedirect('/')

def firstFit(request):
    run()
    return HttpResponseRedirect('/')





