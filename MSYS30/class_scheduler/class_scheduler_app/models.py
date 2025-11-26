from django.db import models

class grade_level(models.IntegerChoices):
    grade_7 = 7, 'Grade 7'
    grade_8 = 8, 'Grade 8'
    grade_9 = 9, 'Grade 9'
    grade_10 = 10, 'Grade 10'

class subjectslist(models.IntegerChoices):
    recess = 0, "Recess"
    lunch_break = 1, "Lunch Break"
    science = 2, "Science"
    filipino = 3, "Filipino"
    english = 4, "English"
    math = 5, "Mathematics"
    ap = 6, "Araling Panlipunan"
    esp  = 7, "Edukasyon sa Pagpapakatao"
    tle = 8, "Technology and Livelihood Education"
    mapeh = 9, "MAPEH"
    homeroom = 10, "HGP"

class section(models.Model): 
    name = models.CharField(max_length=100)
    grade_level = models.IntegerField(choices=grade_level.choices)

    def __str__(self):
        return f"{self.grade_level} - {self.name}"
    
class student(models.Model):
    name = models.CharField(max_length=300)
    section = models.ForeignKey(section, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.section})"

class teacher(models.Model):
    name = models.CharField(max_length=200)
    max_weekly_hours = models.IntegerField(default=30)
    subject_taught = models.IntegerField(choices=subjectslist.choices)

    def __str__(self):
        return f"{self.teacher}"

class days(models.TextChoices):
    monday = "M", "Monday"
    tuesday = "T", "Tuesday"
    wednesday = "W", "Wednesday"
    thursday = "TH", "Thursday"
    friday = "F", "Friday"
    saturday = "S", "Saturday"

class teacheravailability(models.Model):
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE)
    day = models.TextField(choices=days.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)


class roomtype(models.TextChoices):
    classroom = "C", "Classroom"
    laboratory = "L", "Laboratory"
    gym = "G", "Gymnasium"

class buildings(models.TextChoices):
    luneta = "L", "Luneta"
    intramuros = "I", "Intramuros"
    binondo = "B", "Binondo"


class room(models.Model):
    building = models.TextField(choices=buildings.choices)
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    type = models.TextField(choices=roomtype.choices)

    def __str__(self):
        return f"{self.building}, {self.room_number}"

class subject(models.Model):
    subject_title = models.IntegerField(choices=subjectslist.choices)
    grade_level = models.IntegerField(choices=grade_level.choices)
    sessions_per_week = models.IntegerField()
    duration_minutes = models.IntegerField()

class timeslot(models.Model):
    day = models.TextField(choices=days.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

class scheduleentry(models.Model):
    section = models.ForeignKey(section, on_delete=models.CASCADE)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(timeslot, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Schedule Entries"

        constraints = [

            models.UniqueConstraint(
                fields=['teacher', 'timeslot'],
                name = 'unique_teacher_slot'
            ),

            models.UniqueConstraint(
                fields=['room', 'timeslot'],
                name='unique_room_slot'
            ),

            models.UniqueConstraint(
                fields=['section', 'timeslot'],
                name='unique_section_slot'
            )
        ]

    def __str__(self):
        return f"{self.section} | {self.subject} | {self.timeslot}"