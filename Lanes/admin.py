from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Lane
from .models import Task


class TaskAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Lane)
admin.site.register(Task)
