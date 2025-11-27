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
    # Step 1: Sort teachers (Least available first is usually better constraint logic)
    sorted_teachers = quicksort_teachers(teachers)

    assignments = {}
    
    # NEW: Track how many classes each teacher currently has
    # Format: { TeacherID: Current_Load_Count }
    teacher_loads = {t.id: 0 for t in teachers}

    # NEW: Track occupied slots to prevent double booking
    # Format: { TeacherID: Set(occupied_blocks) }
    teacher_busy_slots = {t.id: set() for t in teachers}

    for section in sections:
        assigned_subjects = {}

        for subject in section.subjects.all():
            assigned_teacher = None

            for teacher in sorted_teachers:
                # 1. Match Subject
                if teacher.subject_taught != subject.subject_title:
                    continue
                
                # 2. Check Max Load (Don't use teacher if they are full)
                if teacher_loads[teacher.id] >= teacher.max_weekly_loads:
                    continue

                # 3. Check Availability Intersection
                # We need to ensure the teacher is free at the specific time the SECTION needs
                # (Assuming section.availability is the list of blocks the section needs filled)
                
                # Calculate what blocks are actually viable
                # (Section needs) INTERSECT (Teacher is Free) MINUS (Teacher is already busy)
                
                section_needs = set(section.availability) # e.g. {1, 2, 3...}
                teacher_free = set(teacher.availability)
                teacher_busy = teacher_busy_slots[teacher.id]
                
                # Find a valid slot that matches
                viable_slots = (section_needs & teacher_free) - teacher_busy

                if viable_slots:
                    # Assign the teacher
                    assigned_teacher = teacher
                    
                    # Update trackers
                    teacher_loads[teacher.id] += 1
                    
                    # Important: We need to know WHICH slot was chosen.
                    # For this simple logic, let's assume we pick the first viable slot
                    chosen_slot = list(viable_slots)[0] 
                    teacher_busy_slots[teacher.id].add(chosen_slot)
                    
                    # DO NOT REMOVE THE TEACHER FROM THE LIST
                    break

            assigned_subjects[subject.subject_title] = assigned_teacher

        assignments[section.name] = assigned_subjects
    print(assignments)
    return assignments
