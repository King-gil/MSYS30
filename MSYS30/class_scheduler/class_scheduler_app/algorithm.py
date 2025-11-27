from .models import Teacher, Section, Subject, Assignment

# DEFINING THE BREAKS
RECESS_PERIOD = 4
LUNCH_PERIOD = 7
FORBIDDEN_SLOTS = {RECESS_PERIOD, LUNCH_PERIOD}

def quicksort_teachers(teachers):
    if len(teachers) <= 1:
        return teachers
    
    pivot = teachers[len(teachers) // 2]
    # Calculate availability excluding breaks
    pivot_len = len(set(pivot.availability) - FORBIDDEN_SLOTS)

    left = [t for t in teachers if len(set(t.availability) - FORBIDDEN_SLOTS) < pivot_len]
    middle = [t for t in teachers if len(set(t.availability) - FORBIDDEN_SLOTS) == pivot_len]
    right = [t for t in teachers if len(set(t.availability) - FORBIDDEN_SLOTS) > pivot_len]

    return quicksort_teachers(left) + middle + quicksort_teachers(right)

def assign_teachers_to_sections(sections, teachers):
    sorted_teachers = quicksort_teachers(list(teachers))
    assignments = {}
    
    # 1. Initialize Pools (Remove breaks immediately)
    teacher_pool = {t.id: set(t.availability) - FORBIDDEN_SLOTS for t in teachers}
    section_pool = {s.id: set(s.availability) - FORBIDDEN_SLOTS for s in sections}
    
    teacher_loads = {t.id: 0 for t in teachers}

    for section in sections:
        assigned_subjects = {}

        # 2. Loop through subjects
        for subject in section.subjects.all():
            assigned_data = None
            target_subject_id = subject.subject_title

            for teacher in sorted_teachers:
                # A. Match Subject
                if teacher.subject_taught != target_subject_id:
                    continue

                # B. Check Max Load
                if teacher_loads[teacher.id] >= teacher.max_weekly_loads:
                    continue

                # C. Find Common Slots
                current_teacher_slots = teacher_pool[teacher.id]
                current_section_slots = section_pool[section.id]
                common_slots = current_teacher_slots.intersection(current_section_slots)
                
                if common_slots:
                    # --- THE FIX IS HERE ---
                    # We SORT the common slots and pick the FIRST one.
                    # This forces the class into the earliest possible period (e.g., Period 6 before Period 11)
                    chosen_slot = sorted(list(common_slots))[0]
                    
                    # Update Pools & Load
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

        # 3. Inject Breaks for Display
        assigned_subjects["RECESS"] = {'teacher': None, 'slot': RECESS_PERIOD, 'type': 'break'}
        assigned_subjects["LUNCH"] = {'teacher': None, 'slot': LUNCH_PERIOD, 'type': 'break'}

        assignments[section.name] = assigned_subjects

    print_debug_schedule(assignments)
    return assignments

def print_debug_schedule(assignments):
    print("\n" + "="*50)
    print(" GENERATED SCHEDULE (Optimized)")
    print("="*50)
    
    for section_name, subjects in assignments.items():
        print(f"SECTION: {section_name}")
        
        # Sort output by Period so it looks like a real timeline
        def get_slot_key(item):
            key, val = item
            if val == "UNASSIGNED": return 999
            return val['slot']

        sorted_subs = sorted(subjects.items(), key=get_slot_key)

        for subj_code, data in sorted_subs:
            if data == "UNASSIGNED":
                 print(f"  - {str(subj_code):<15}: [!] NO TEACHER FOUND (Max Load Reached?)")
            elif data['type'] == 'break':
                 print(f"  - {'*** ' + str(subj_code) + ' ***':<15}: ---------------- Period {data['slot']}")
            else:
                 t_name = data['teacher'].name
                 slot = data['slot']
                 print(f"  - {str(subj_code):<15}: {t_name:<20} | Period {slot}")
        print("-" * 50)