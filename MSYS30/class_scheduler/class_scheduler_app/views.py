from django.shortcuts import render, redirect
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

def add_teacher(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        subject_taught = request.POST.get('subject_taught')
        availability_choice = request.POST.get('availability_choice')
        if Teacher.objects.filter(name=name).exists():
            return redirect('teachers')
        Teacher.objects.create(name=name, subject_taught=subject_taught, availability_choice=availability_choice)
        return redirect('teachers')
    else:
        return render(request, 'class_scheduler_app/add_teacher.html', {"teacheravailability": Teacheravailability, "subjects_list": Subjectslist})


def add_section(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        grade_level = request.POST.get('grade_level')
        subjects_list = request.POST.getlist('subjects_list')
        room_type = request.POST.get('room_type')
        availability = list(range(1, 12))
        if Section.objects.filter(name=name).exists():
            return redirect('sections')
        new_section = Section.objects.create(name=name, grade_level=grade_level, room=room_type, availability=availability)
        if subjects_list:
            new_section.subjects.set(subjects_list)
        return redirect('sections')
    else:
        return render(request, 'class_scheduler_app/add_section.html', {"grade_level": Grade_level, "subjects_list": Subjectslist, "room_type": Roomtype})