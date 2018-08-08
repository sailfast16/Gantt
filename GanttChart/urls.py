from django.contrib import admin
from django.urls import path
from django.urls import include
from Lanes import views


urlpatterns = [
    # Admin Site
    path('admin/', admin.site.urls),

    # Home
    path('', views.index),

    # Add Lane Page/ Endpoint
    path('addLane/', views.addLane, name='addLane'),

    # Add Task Page/ Endpoint
    path('addTask/', views.uploadJSON, name='uploadJSON'),

    # Fetch Lane Data from DB
    path('lanesJSON/', views.lanesJSON, name='getLanes'),

    # Fetch Task Data from DB
    path('tasksJSON/', views.taskJSON, name='getTasks'),

    # Change Task data in DB (used by AJAX)
    path("moveTask/<lane>/<task>/<start>/<end>", views.moveTask, name='moveTask'),

    path("addPosition/<lane>/<task>/<start>/<end>", views.addPosition, name='addPosition'),

    path("upload", views.upload, name='uploadTask'),

    path("solve/", views.firstFit, name='firstFit')
]
