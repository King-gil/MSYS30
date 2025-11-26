from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(scheduleentry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = ('section', 'subject', 'teacher', 'room', 'timeslot')
    list_filter = ('teacher', 'room', 'timeslot')

admin.site.register([section, student, teacher, room, subject, timeslot, teacheravailability])