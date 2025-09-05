from django.contrib import admin
from mytaskhubs.models import Task
from mytaskhubs.models import Entry
from mytaskhubs.models import Project
from mytaskhubs.models import Goal

admin.site.register(Task)
admin.site.register(Entry)
admin.site.register(Project)
admin.site.register(Goal)