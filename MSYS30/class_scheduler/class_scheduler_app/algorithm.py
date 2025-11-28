import bisect
from .models import Teacher, Section, Subject, Assignment

RECESS_PERIOD = 4
LUNCH_PERIOD = 7
FORBIDDEN_SLOTS = {RECESS_PERIOD, LUNCH_PERIOD}

def quicksort_teachers(teachers):
    if len(teachers) <= 1:
        return teachers
    
    pivot = teachers[len(teachers) // 2]
    pivot_len = len(set(pivot.availability) - FORBIDDEN_SLOTS)

    left = [t for t in teachers if len(set(t.availability) - FORBIDDEN_SLOTS) < pivot_len]
    middle = [t for t in teachers if len(set(t.availability) - FORBIDDEN_SLOTS) == pivot_len]
    right = [t for t in teachers if len(set(t.availability) - FORBIDDEN_SLOTS) > pivot_len]

    return quicksort_teachers(left) + middle + quicksort_teachers(right)

def find_common_slot_binary(section_slots, teacher_slots):
    """
    BINARY SEARCH HELPER:
    Iterates through sorted Sections and binary searches for them in the Teachers. Returns the first match.
    """

    for slot in section_slots:
        idx = bisect.bisect_left(teacher_slots, slot)
        if idx < len(teacher_slots) and teacher_slots[idx] == slot:
            return slot
    return None

def assign_teachers_to_sections(sections, teachers):
    sorted_teachers = quicksort_teachers(list(teachers))
    assignments = {}
# initialization
    teacher_pool = {}
    for t in teachers:
        # convert set to sorted list
        valid_slots = sorted(list(set(t.availability) - FORBIDDEN_SLOTS))
        teacher_pool[t.id] = valid_slots

    section_pool = {}
    for s in sections:
        valid_slots = sorted(list(set(s.availability) - FORBIDDEN_SLOTS))
        section_pool[s.id] = valid_slots
    
    teacher_loads = {t.id: 0 for t in teachers}

    for section in sections:
        assigned_subjects = {}

        for subject in section.subjects.all():
            assigned_data = None
            target_subject_id = subject.subject_title

            for teacher in sorted_teachers:
                # mathing subjects
                if teacher.subject_taught != target_subject_id:
                    continue

                # checking teacher max loads
                if teacher_loads[teacher.id] >= teacher.max_weekly_loads:
                    continue

                # Binary Search for Slots
                current_teacher_slots = teacher_pool[teacher.id]
                current_section_slots = section_pool[section.id]
                chosen_slot = find_common_slot_binary(current_section_slots, current_teacher_slots)
                
                if chosen_slot is not None:
                    # update the teacher, section pools and add teacher load (since there is a chosen slot)
                    teacher_pool[teacher.id].remove(chosen_slot)
                    section_pool[section.id].remove(chosen_slot)
                    teacher_loads[teacher.id] += 1
                    
                    assigned_data = {
                        'teacher': teacher,
                        'slot': chosen_slot,
                        'type': 'academic'
                    }
                    break

            if assigned_data:
                assigned_subjects[subject.subject_title] = assigned_data
            else:
                assigned_subjects[subject.subject_title] = "UNASSIGNED"

        # breaks (Recess, Lunch)
        assigned_subjects["RECESS"] = {'teacher': None, 'slot': RECESS_PERIOD, 'type': 'break'}
        assigned_subjects["LUNCH"] = {'teacher': None, 'slot': LUNCH_PERIOD, 'type': 'break'}

        assignments[section.name] = assigned_subjects

    # print_debug_schedule(assignments)
    return assignments

''' def print_debug_schedule(assignments):
    print("\n" + "="*60)
    print(" GENERATED SCHEDULE (Binary Search)")
    print("="*60)
    
    for section_name, subjects in assignments.items():
        print(f"SECTION: {section_name}")
        
        def get_slot_key(item):
            key, val = item
            if val == "UNASSIGNED": return 999
            return val['slot']

        sorted_subs = sorted(subjects.items(), key=get_slot_key)

        for subj_code, data in sorted_subs:
            if data == "UNASSIGNED":
                 print(f"  - {str(subj_code):<20}: [!] NO TEACHER FOUND")
            elif data['type'] == 'break':
                 print(f"  - {'*** ' + str(subj_code) + ' ***':<20}: ---------------- Period {data['slot']}")
            else:
                 t_name = data['teacher'].name
                 slot = data['slot']
                 print(f"  - {str(subj_code):<20}: {t_name:<20} | Period {slot}")
        print("-" * 60) '''