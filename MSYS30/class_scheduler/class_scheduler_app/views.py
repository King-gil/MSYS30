from django.shortcuts import render
from .models import *
from .algorithm import assign_teachers_to_sections

# Create your views here.
def teachers(request): 
    teacher = Teacher.objects.all()
    return render (request, 'class_scheduler_app/teachers.html', {'teacher': teacher} )

def sections(request):
    section = Section.objects.all()
    return render (request, 'class_scheduler_app/sections.html', {'section': section} )

def schedule_view(request):
    sections = Section.objects.all()
    teachers = Teacher.objects.all()

    assignments = assign_teachers_to_sections(sections, teachers)

    return render(request, "class_scheduler_app/timetable.html", {"teacher":teachers, "section": sections, "assignments": assignments})