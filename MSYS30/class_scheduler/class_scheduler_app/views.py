from django.shortcuts import render
from .models import *

# Create your views here.
def teachers(request): 
    teacher = Teacher.objects.all()
    return render (request, 'class_scheduler_app/teachers.html', {'teacher': teacher} )

def sections(request):
    section = Section.objects.all()
    return render (request, 'class_scheduler_app/sections.html', {'section': section} )