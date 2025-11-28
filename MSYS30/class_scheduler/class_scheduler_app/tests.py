from django.test import TestCase
from .models import Section, Teacher, Subject, Subjectslist, Teacheravailability, Grade_level, Roomtype
from .algorithm import assign_teachers_to_sections

class TeacherModelTests(TestCase):
    def test_availability_auto_populate_morning(self):
        teacher = Teacher.objects.create(
            name="Morning Teacher",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.morning
        )
        expected_availability = [1, 2, 3, 4, 5, 6]
        self.assertEqual(teacher.availability, expected_availability)

    def test_availability_auto_populate_unavailable(self):
        teacher = Teacher.objects.create(
            name="Busy Teacher",
            subject_taught=Subjectslist.science,
            availability_choice=Teacheravailability.unavailable
        )
        self.assertEqual(teacher.availability, [])

    def test_availability_auto_populate_whole_day(self):
        teacher = Teacher.objects.create(
            name="Hardworking Teacher",
            subject_taught=Subjectslist.english,
            availability_choice=Teacheravailability.available
        )
        self.assertEqual(len(teacher.availability), 11)


class SchedulerAlgorithmTests(TestCase):
    def setUp(self):
        self.math = Subject.objects.create(subject_title=Subjectslist.math)
        self.science = Subject.objects.create(subject_title=Subjectslist.science)

        self.section = Section.objects.create(
            name="Rizal",
            grade_level=Grade_level.grade_7,
            room=Roomtype.classroom
        )
        self.section.subjects.add(self.math, self.science)

    def test_successful_assignment(self):
        teacher = Teacher.objects.create(
            name="Mr. Math",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.morning, # [1..6]
            max_weekly_loads=5
        )

        assignments = assign_teachers_to_sections([self.section], [teacher])

        # Dig into the dictionary result
        # Structure: assignments['Rizal'][4] -> Data
        # Note: Subjectslist.math value is 4
        math_assignment = assignments['Rizal'][Subjectslist.math]

        self.assertIsNotNone(math_assignment, "Math teacher should be assigned")
        self.assertEqual(math_assignment['teacher'].name, "Mr. Math")
        # Ensure the slot chosen is within Morning (1-6)
        self.assertIn(math_assignment['slot'], [1, 2, 3, 4, 5, 6])

    def test_subject_mismatch(self):
        teacher = Teacher.objects.create(
            name="Mr. Math",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.available
        )

        assignments = assign_teachers_to_sections([self.section], [teacher])
        
        science_assignment = assignments['Rizal'][Subjectslist.science]

        if isinstance(science_assignment, dict):
            self.fail("Science was assigned to a Math teacher!")
        
        self.assertEqual(science_assignment, "UNASSIGNED")

    def test_availability_mismatch(self):
        self.section.availability = [7, 8, 9, 10, 11]
        self.section.save()

        teacher = Teacher.objects.create(
            name="Mr. Morning",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.morning
        )

        assignments = assign_teachers_to_sections([self.section], [teacher])
        math_assignment = assignments['Rizal'][Subjectslist.math]

        self.assertEqual(math_assignment, "UNASSIGNED", "Should not assign due to time conflict")

    def test_max_load_constraint(self):
        teacher = Teacher.objects.create(
            name="Overloaded Teacher",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.available,
            max_weekly_loads=0  
        )

        assignments = assign_teachers_to_sections([self.section], [teacher])
        math_assignment = assignments['Rizal'][Subjectslist.math]

        self.assertEqual(math_assignment, "UNASSIGNED", "Should not assign due to max load")