from .models import * 

def quicksort_teachers(teachers):
    if len(teachers) <= 1:
        return teachers

    pivot = teachers[len(teachers) // 2]
    pivot_len = len(pivot.availability)

    left = [t for t in teachers if len(t.availability) < pivot_len]
    middle = [t for t in teachers if len(t.availability) == pivot_len]
    right = [t for t in teachers if len(t.availability) > pivot_len]

    return quicksort_teachers(left) + middle + quicksort_teachers(right)

def assign_teachers_to_sections(sections, teachers):
    # Step 1: sort teachers by availability using quicksort
    sorted_teachers = quicksort_teachers(teachers)

    assignments = {}

    for section in sections:
        assigned_subjects = {}

        for subject in section.subjects.all():
            assigned_teacher = None

            for teacher in sorted_teachers:
                # must match subject
                if teacher.subject_taught != subject.subject_title:
                    continue

                # check availability intersection
                # sections and teachers both store simple block lists
                common = set(section.availability).intersection(set(teacher.availability))

                if common:
                    assigned_teacher = teacher
                    sorted_teachers.remove(teacher)
                    break

            assigned_subjects[subject.subject_title] = assigned_teacher

        assignments[section.name] = assigned_subjects

    return assignments
