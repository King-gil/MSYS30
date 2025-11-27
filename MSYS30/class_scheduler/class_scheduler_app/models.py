from django.db import models

class Grade_level(models.IntegerChoices):
    grade_7 = 7, 'Grade 7'
    grade_8 = 8, 'Grade 8'
    grade_9 = 9, 'Grade 9'
    grade_10 = 10, 'Grade 10'

class Subjectslist(models.IntegerChoices):
    science = 1, "Science"
    filipino = 2, "Filipino"
    english = 3, "English"
    math = 4, "Mathematics"
    ap = 5, "Araling Panlipunan"
    esp  = 6, "Edukasyon sa Pagpapakatao"
    tle = 7, "Technology and Livelihood Education"
    mapeh = 8, "MAPEH"
    homeroom = 9, "Homeroom Guidance Program"

class Roomtype(models.TextChoices):
    classroom = "Classroom", "Classroom"
    laboratory = "Laboratory", "Laboratory"

class Subject(models.Model):
    subject_title = models.IntegerField(choices=Subjectslist.choices)

    def __str__(self):
        return f"{self.get_subject_title_display()}"

def default_availability():
    return list(range(1, 12))

class Section(models.Model): 
    name = models.CharField(max_length=100)
    grade_level = models.IntegerField(choices=Grade_level.choices)
    subjects = models.ManyToManyField(Subject, blank=True)
    room = models.TextField(choices=Roomtype.choices, default=Roomtype.classroom)
    availability = models.JSONField(default=default_availability)

    def __str__(self):
        return f"{self.grade_level} - {self.name}"

class Teacheravailability(models.TextChoices):
    unavailable = "Unavailable", "Unavailable"
    morning = "Available Morning Weekly", "Available Morning Weekly"
    afternoon = "Available Afternoon Weekly", "Available Afternoon Weekly"
    available = "Available Whole Day Weekly", "Available Whole Day Weekly"

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subject_taught = models.IntegerField(choices=Subjectslist.choices)
    availability_choice = models.TextField(
        choices=Teacheravailability.choices,
        default=Teacheravailability.unavailable
    )
    availability = models.JSONField(default=list, blank=True)

    def save(self, *args, **kwargs):
        if self.availability_choice == Teacheravailability.unavailable:
            self.availability = []
        elif self.availability_choice == Teacheravailability.morning:
            self.availability = [1,2,3,4,5,6]
        elif self.availability_choice == Teacheravailability.afternoon:
            self.availability = [7,8,9,10,11]
        elif self.availability_choice == Teacheravailability.available:
            self.availability = [1,2,3,4,5,6,7,8,9,10,11]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_subject_taught_display()}"
