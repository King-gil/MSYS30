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

def prepare_schedule_for_template(assignments):
    view_data = []

    for section_name, subjects_data in assignments.items():
        def get_slot_key(item):
            key, val = item
            if val == "UNASSIGNED": return 999
            return val['slot']

        sorted_subs = sorted(subjects_data.items(), key=get_slot_key)
        
        section_schedule = []
        
        for subj_code, data in sorted_subs:
            row = {
                'subject': str(subj_code),
                'is_break': False,
                'is_unassigned': False,
                'teacher': '',
                'slot': '',
                'css_class': ''
            }

            if data == "UNASSIGNED":
                row['is_unassigned'] = True
                row['css_class'] = 'table-danger'
                row['slot'] = "N/A"

                if isinstance(subj_code, int):
                    row['subject'] = Subjectslist(subj_code).label
            
            elif data['type'] == 'break':
                row['is_break'] = True
                row['css_class'] = 'table-warning'
                row['slot'] = data['slot']
                row['subject'] = f"*** {subj_code} ***"
            
            else:
                row['teacher'] = data['teacher'].name
                row['slot'] = data['slot']
                
                if isinstance(subj_code, int):
                    row['subject'] = Subjectslist(subj_code).label

            section_schedule.append(row)

        view_data.append({
            'section_name': section_name,
            'schedule': section_schedule
        })
    
    return view_data

def schedule_view_generated(request):
    sections = list(Section.objects.prefetch_related('subjects').all())
    teachers = list(Teacher.objects.all())
    
    raw_assignments = assign_teachers_to_sections(sections, teachers)
    formatted_data = prepare_schedule_for_template(raw_assignments)

    context = {
        'schedule_data': formatted_data
    }
    return render(request, 'class_scheduler_app/timetables.html', context)