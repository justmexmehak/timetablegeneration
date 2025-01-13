from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    lectureno = models.IntegerField()
    duration = models.IntegerField()
    instructor_name = models.CharField(max_length=255)
    start_hr = models.CharField(max_length=5)
    end_hr = models.CharField(max_length=5)

    def __str__(self):
        return self.name
