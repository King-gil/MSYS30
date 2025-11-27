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

class Subject(models.Model):
    subject_title = models.IntegerField(choices=Subjectslist.choices)
    sessions_per_week = models.IntegerField(default=5, editable=False)
    duration_minutes = models.IntegerField(default=60, editable=False)

    def __str__(self):
        return f"{self.get_subject_title_display()}"

class Section(models.Model): 
    name = models.CharField(max_length=100)
    grade_level = models.IntegerField(choices=Grade_level.choices)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return f"{self.grade_level} - {self.name}"

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    max_weekly_hours = models.IntegerField(default=30)
    subject_taught = models.IntegerField(choices=Subjectslist.choices)

    def __str__(self):
        return f"{self.name} - {self.get_subject_taught_display()}"

class Days(models.TextChoices):
    monday = "M", "Monday"
    tuesday = "T", "Tuesday"
    wednesday = "W", "Wednesday"
    thursday = "TH", "Thursday"
    friday = "F", "Friday"
    saturday = "S", "Saturday"

class Roomtype(models.TextChoices):
    classroom = "C", "Classroom"
    laboratory = "L", "Laboratory"
    gym = "G", "Gymnasium"

class Room(models.Model):
    room_number = models.IntegerField()
    capacity = models.IntegerField(default=30, editable=False)
    type = models.TextField(choices=Roomtype.choices)

    def __str__(self):
        return f"{self.room_number}"