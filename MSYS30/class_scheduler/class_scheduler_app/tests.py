from django.test import TestCase
from .models import Section, Teacher, Subject, Subjectslist, Teacheravailability, Grade_level, Roomtype
# Assuming your algorithm function is in a file named algorithm.py in the same app
from .algorithm import assign_teachers_to_sections

class TeacherModelTests(TestCase):
    """
    Tests specific to the Teacher model logic (specifically the save method)
    """
    def test_availability_auto_populate_morning(self):
        """Test if selecting 'Morning' automatically sets availability to [1-6]"""
        teacher = Teacher.objects.create(
            name="Morning Teacher",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.morning
        )
        # Check if the JSON field was populated correctly
        expected_availability = [1, 2, 3, 4, 5, 6]
        self.assertEqual(teacher.availability, expected_availability)

    def test_availability_auto_populate_unavailable(self):
        """Test if selecting 'Unavailable' clears the list"""
        teacher = Teacher.objects.create(
            name="Busy Teacher",
            subject_taught=Subjectslist.science,
            availability_choice=Teacheravailability.unavailable
        )
        self.assertEqual(teacher.availability, [])

    def test_availability_auto_populate_whole_day(self):
        """Test if selecting 'Available' sets [1-11]"""
        teacher = Teacher.objects.create(
            name="Hardworking Teacher",
            subject_taught=Subjectslist.english,
            availability_choice=Teacheravailability.available
        )
        self.assertEqual(len(teacher.availability), 11)


class SchedulerAlgorithmTests(TestCase):
    """
    Tests the interaction between your Models and the Algorithm.
    """
    def setUp(self):
        # 1. Create Subjects
        self.math = Subject.objects.create(subject_title=Subjectslist.math)
        self.science = Subject.objects.create(subject_title=Subjectslist.science)

        # 2. Create a Section (Available all day by default)
        self.section = Section.objects.create(
            name="Rizal",
            grade_level=Grade_level.grade_7,
            room=Roomtype.classroom
        )
        # Add subjects to section
        self.section.subjects.add(self.math, self.science)

    def test_successful_assignment(self):
        """
        Scenario: Teacher matches subject and has overlapping availability.
        Result: Teacher should be assigned.
        """
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
        """
        Scenario: Section needs Science, Teacher teaches Math.
        Result: No assignment.
        """
        teacher = Teacher.objects.create(
            name="Mr. Math",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.available
        )

        # Only pass the Math teacher, but check for Science assignment
        assignments = assign_teachers_to_sections([self.section], [teacher])
        
        # Subjectslist.science value is 1
        science_assignment = assignments['Rizal'][Subjectslist.science]
        
        # Should be UNASSIGNED or None depending on your algo output
        # Based on previous code, it might be the string "UNASSIGNED" or None
        if isinstance(science_assignment, dict):
            self.fail("Science was assigned to a Math teacher!")
        
        # If your algo returns "UNASSIGNED" string:
        self.assertEqual(science_assignment, "UNASSIGNED")

    def test_availability_mismatch(self):
        """
        Scenario: Section is available PM, Teacher is available AM.
        Result: No assignment.
        """
        # Manually change section availability to PM only [7, 8, 9, 10, 11]
        self.section.availability = [7, 8, 9, 10, 11]
        self.section.save()

        # Teacher available AM only [1, 2, 3, 4, 5, 6]
        teacher = Teacher.objects.create(
            name="Mr. Morning",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.morning
        )

        assignments = assign_teachers_to_sections([self.section], [teacher])
        math_assignment = assignments['Rizal'][Subjectslist.math]

        self.assertEqual(math_assignment, "UNASSIGNED", "Should not assign due to time conflict")

    def test_max_load_constraint(self):
        """
        Scenario: Teacher has max_load = 0.
        Result: No assignment.
        """
        teacher = Teacher.objects.create(
            name="Overloaded Teacher",
            subject_taught=Subjectslist.math,
            availability_choice=Teacheravailability.available,
            max_weekly_loads=0  # Cannot take any classes
        )

        assignments = assign_teachers_to_sections([self.section], [teacher])
        math_assignment = assignments['Rizal'][Subjectslist.math]

        self.assertEqual(math_assignment, "UNASSIGNED", "Should not assign due to max load")